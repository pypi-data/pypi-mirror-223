"""mdk utility functions & classes"""

import hashlib
import json
import os
from pathlib import Path
import pkg_resources
import re
import socket
import subprocess
from typing import List, TypeVar, Optional, NoReturn
import shlex
import sys
import time
import pathlib
import platform

import click

T = TypeVar('T')

CONFIG_FILENAME: str = "mdk.json"
CONFIG_EXTENSION_FILENAME: str = "ext.mdk.json"
CONFIG_EXTENSION_USER_PATH: str = ".config/mdk/mdk.json"

OPTS_HASH_LABEL_KEY = 'com.matician.mdk.opts_hash'

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

def version_tuple(s):
    'Raises ValueError if version string is invalid.'
    return tuple(int(x) for x in s.split('.'))


def version_string(v):
    'Inverse of version_tuple.'
    return '.'.join(str(x) for x in v)


VERSION = version_tuple(pkg_resources.require("mdk")[0].version)


class ContainerInspect:

    def __init__(self, inspect_output):
        self.created = False
        self.started = False
        self.status = 'not created'
        self.image = ''
        self.id = ''
        self.command = ''
        self.opts_hash = ''
        try:
            [container_info] = inspect_output
        except ValueError:
            pass    # container not found, keep the defaults
        else:
            self._parse_info(container_info)

    def _parse_info(self, info):
        self.created = True
        self.started = info['State']['Running']
        self.status = info['State']['Status']
        self.image = info['Config']['Image']
        self.id = info['Id']
        self.command = ' '.join(shlex.quote(x) for x in [info['Path']] + info['Args'])
        self.opts_hash = info['Config']['Labels'].get(OPTS_HASH_LABEL_KEY, '')


class MdkBackend:

    # settable publicly
    no_gpu = False
    nvidia = False

    def __init__(self):
        self.conf_version = ()
        self.conf_root = None
        self.conf_paths = []
        self.conf_data = []
        self._inspect = None

        # find nearest config file & sibling ext conf (add "_" to cwd b/c cwd().parents doesn't include cwd)
        for dir_path in (Path().cwd()/"_").parents:
            if (dir_path/CONFIG_FILENAME).is_file():
                self.conf_root = dir_path
                self.conf_paths.append(dir_path/CONFIG_FILENAME)
                self.conf_paths.append(dir_path/CONFIG_EXTENSION_FILENAME)
                break
        else:
            Log.fatal(f'{CONFIG_FILENAME} found in neither this directory nor any of its parents.')

        # find global user conf
        self.conf_paths.append(Path.home()/CONFIG_EXTENSION_USER_PATH)

        # load our configuration as a list of dicts, later configs override earlier ones
        self.conf_data = [json.load(open(path)) for path in self.conf_paths if path.is_file()]

        # ensure that we are new enough to properly parse this config
        conf_version = self.conf("mdk-version", str)
        if conf_version:
            try:
                conf_version = version_tuple(conf_version)
            except ValueError:
                Log.fatal(f'Config has invalid mdk-version {conf_version!r}.')
            if VERSION < conf_version:
                Log.fatal(f'Project requires mdk>={version_string(conf_version)} '
                          f'(current: {version_string(VERSION)})')
            self.conf_version = conf_version

    @property
    def inspect(self) -> ContainerInspect:
        if self._inspect is not None:
            return self._inspect

        # first check that docker is available
        try:
            subprocess.run(['docker', 'version'], stdout=subprocess.PIPE, check=True)
        except OSError:
            Log.fatal(f'Failed to run "docker" command. Is it installed?')

        # inspect container to get initial state
        proc = subprocess.run(['docker', 'inspect', self.container_name()],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc_out = json.loads(proc.stdout)  # docker returns valid JSON even if container is not found
        self._inspect = ContainerInspect(proc_out)
        return self._inspect

    def image_name(self) -> str:
        image_field = self.conf('image', required=True)
        if isinstance(image_field, str):
            return image_field
        elif isinstance(image_field, dict):
            arch = platform.machine()
            if arch in image_field:
                return image_field[arch]
            else:
                Log.fatal(f"mdk.json does not specify an image for {arch}")
        else:
            Log.fatal("Invalid type for \"image\"")

    def container_name(self) -> str:
        container_name = self.conf("name", str)
        if container_name:
            return container_name
        return "mdk" + str(self.conf_root).replace('/', '_')

    def opts_hash(self) -> str:
        data_to_hash = '\0'.join(self.build_docker_opts(log_info=False, include_nfs=False)).encode()
        return hashlib.sha1(data_to_hash).hexdigest()

    def is_up_to_date(self) -> bool:
        return self.opts_hash() == self.inspect.opts_hash

    def build_docker_opts(self, log_info=True, include_nfs=True) -> List[str]:
        """
        Constructs a list of docker options to run the container with.

        Args:
            log_info: If True, add logging. Mainly set to False for non-user facing functions.
            include_nfs: If True, include NFS in the options.
        """
        opt_builder: List[str] = []

        for volume in self.conf_list("volumes"):
            # valid volume string formats:
            # - <source>:<target>
            # - nfs(<host>:<source>):<target>
            try:
                vol_src, vol_tgt = volume.rsplit(':', 1)
            except ValueError:
                Log.fatal(f'Invalid volume string {volume!r}.')

            if not vol_tgt.startswith('/'):
                Log.fatal(f'Volume target {vol_tgt} is not an absolute path.')

            vol_nfs = re.fullmatch(r"nfs\((?P<host>[-\w\.]+):(?P<remote_dir>[^()]+)\)", vol_src)
            if vol_nfs:
                if not include_nfs:
                    # useful for calculating opts hash
                    continue
                try:
                    vol_host_ip = socket.gethostbyname(vol_nfs.group("host"))
                    socket.socket().connect((vol_host_ip, 111))
                except OSError:
                    Log.warning(f'Failed to connect to NFS server {vol_nfs.group("host")}, skipping volume mount.')
                    continue
                opt_builder += ["--mount",
                                f"type=volume,target={vol_tgt},volume-opt=type=nfs4,"
                                f"volume-opt=device={vol_nfs.group('host')}:{vol_nfs.group('remote_dir')},"
                                f'"volume-opt=o=fsc,addr={vol_host_ip}"']
            else:
                vol_src = os.path.expanduser(vol_src)
                vol_src = os.path.expandvars(vol_src)
                if vol_src == '..' or vol_src.startswith('../'):
                    Log.fatal('Volume sources may not start with ".." .')
                if vol_src == '.' or vol_src.startswith('./'):
                    vol_src = str(self.conf_root) + vol_src[1:]
                opt_builder += ['-v', vol_src + ':' + vol_tgt]

        if self.conf("shareX11", bool):
            opt_builder += [
                "-v", "/tmp/.X11-unix:/tmp/.X11-unix:rw",
                "--device", "/dev/dri:/dev/dri",
            ]
            display = os.getenv('DISPLAY')
            if display is not None:
                opt_builder += ["-e", f"DISPLAY={display}"]
            xauth_file = os.getenv('XAUTHORITY', None)
            if xauth_file is not None:
                opt_builder += ['-v', f"{xauth_file}:/tmp/.XAuthority",
                                "-e", "XAUTHORITY=/tmp/.XAuthority"]

        if self.conf("shareVulkan", bool):
            icds = []
            if "VK_ICD_FILENAMES" in os.environ:
                if log_info:
                    Log.log("VK_ICD_FILENAMES is set, using Vulkan ICD files from environment")
                # we do not set VK_ICD_FILENAMES in the container but rather put the files in the default location
                icds = os.environ["VK_ICD_FILENAMES"].split(':')
                icds = [pathlib.Path(icd) for icd in icds]
            else:
                path = pathlib.Path("/usr/share/vulkan/icd.d/")
                icds = os.listdir(path)
                icds = [path / icd for icd in icds]
            if len(icds) == 0:
                Log.warning("No Vulkan ICD files found. Is Vulkan setup to run on the host?")
            else:
                for icd in icds:
                    if icd.name.startswith("lvp_icd"):
                        if log_info:
                            Log.log(f"Found LavaPipe ICD file at {icd}. Ignoring as presumably you do not want to use a CPU Vulkan driver.")
                        continue
                    opt_builder += ["-v", f"{str(icd)}:/usr/share/vulkan/icd.d/{icd.name}:ro"]

        if self.conf("saveVSCode", bool):
            # persists VSCode extensions and settings
            vscpath = os.path.expanduser("~/.vscode-server-" + self.container_name())
            if not os.path.exists(vscpath):
                Log.log(f'Creating VSCode data directory on host at {vscpath}')
                os.makedirs(vscpath)
            opt_builder += [
                "-v", f"{vscpath}:/.vscode-server/"
            ]

        if self.conf("core-image", bool):
            opt_builder += ["-e", f"HOST_UID={os.getuid()}",
                            "-e", f"DOCKER_CONTAINER_NAME={self.container_name()}",
                            "-e", f"DOCKER_CONTAINER_ROOT={self.conf_root}",
                            "-e", f"DOCKER_IMAGE_NAME={self.image_name()}"]
        for env_var in self.conf_list("environment"):
            try:
                k, v = env_var.split('=', 1)
            except ValueError:
                Log.warning(f'Ignoring invalid environment variable entry {env_var!r}.')
                continue
            if v in ('$UID', '${UID}'):
                v = f'{os.getuid()}'
            elif v in ('$GID', '${GID}'):
                v = f'{os.getgid()}'
            else:
                v = os.path.expandvars(v)
            opt_builder += ['-e', k + '=' + v]

        workdir = self.conf('workdir', str)
        if workdir:
            opt_builder += ["-w", workdir]

        opt_builder += self.conf_list('options')

        # hacky way to allow overriding --gpus
        if self.no_gpu:
            opt_builder = [x for x in opt_builder if not x.startswith('--gpus=')]
            while '--gpus' in opt_builder:
                gpu_idx = opt_builder.index('--gpus')
                del opt_builder[gpu_idx:gpu_idx+2]

        if self.nvidia:
            opt_builder.extend(
                ["-e", "NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics"]
            )

        # old images required --tty to start and run properly
        if self.conf_version < (5, 0):
            opt_builder += ['--tty']

        # mount git to not having to explain yourself on every commit. Note that this is not the right
        # location but later when we start the container, we will symlink ~/.gitconfig to /.gitconfig
        gitconfig_path = os.path.expanduser("~/.gitconfig")
        if os.path.exists(gitconfig_path):
            opt_builder += ["-v", f"{gitconfig_path}:/.gitconfig"]

        return opt_builder

    def conf(self, key: str, expected_type: type = None, required=False) -> Optional[T]:
        # gather option in all configs
        all_data = [data[key] for data in self.conf_data if key in data]

        # case: conf option not found
        if not all_data:
            if required:
                Log.fatal(f'Key {key!r} missing in mdk.json.')
            return None

        # validate and return
        res = all_data[-1]
        if expected_type is None or isinstance(res, expected_type):
            return res
        Log.fatal(f'Key {key!r} expects a {expected_type.__name__}.')

    def conf_list(self, key: str) -> List[str]:
        all_data = [data[key] for data in self.conf_data if key in data]
        if all(isinstance(l, list) for l in all_data):
            res = [el for data in all_data for el in data]
            if all(isinstance(x, str) for x in res):
                return res
        Log.fatal(f'Key {key!r} expects a list of strings.')

    def status(self) -> None:
        def line(k, v):
            Log.log(f'  {k:11} {v}')
        Log.log('Container:')
        line('Name', self.container_name())
        line('Status', self.inspect.status)
        if self.inspect.created:
            line('Image', self.inspect.image)
            line('ID', self.inspect.id)
            line('Command', self.inspect.command)

    def cmd(self, *args: str, quiet=False) -> None:
        docker = 'nvidia-docker' if self.nvidia else 'docker'
        cmd = [docker] + [(self.container_name() if a == '@CONTAINER@' else a) for a in args]
        Log.cmd(cmd)
        code = subprocess.run(cmd, stdout=subprocess.PIPE if quiet else None).returncode
        if code != 0:
            Log.error(f'Command failed with exit code {code}!')
            sys.exit(code)

    def create(self, implicit=False, nogpu=False) -> None:
        if not self.inspect.created:
            Log.log('mdk.json configuration files in order of increasing precedence:')
            for path in self.conf_paths:
                Log.log(f'  {path}' + ('' if path.is_file() else ' (not found)'))
            self.cmd('create',
                     '--name', '@CONTAINER@',
                     '--label', f'{OPTS_HASH_LABEL_KEY}={self.opts_hash()}',
                     *self.build_docker_opts(),
                     self.image_name(),
                     quiet=True)
            Log.success(f'Container {self.container_name()} successfully created.')
        else:
            if not implicit:
                Log.success(f'Container {self.container_name()} already created.')
            if not self.is_up_to_date():
                Log.warning(f'Container {self.container_name()} is out of sync with mdk.json. '
                            f'Run "mdk up" to recreate the container.')

    def start(self, implicit=False, ensure_up_to_date=False) -> None:
        if ensure_up_to_date and self.inspect.created and not self.is_up_to_date():
            if click.confirm(f'Container {self.container_name()} is out sync with mdk.json. Recreate?', default=True):
                self.delete()
                self._inspect = None    # force ourselves to redo an inspect call
        self.create(implicit=True)
        if not self.inspect.started:
            self.cmd('start', '@CONTAINER@', quiet=True)
            Log.success(f'Container {self.container_name()} successfully started.')
            time.sleep(0.5)     # TODO: remove after upgrading images to setuid entrypoint
            if self.conf("saveVSCode", bool):
                Log.log("Setting up VSCode files...")
                # Checks if ~/.vscode-server exists. If it does, we assume the symlink has already been set up and do nothing.
                self.cmd('exec', '@CONTAINER@', 'bash', '-c', '[ -e ~/.vscode-server ] || ln -s /.vscode-server/ ~/.vscode-server')
            # Set up ~/.gitconfig if it has not already been done
            self.cmd('exec', '@CONTAINER@', 'bash', '-c', '[ -e ~/.gitconfig ] || ln -s /.gitconfig ~/.gitconfig')
        elif not implicit:
            Log.success(f'Container {self.container_name()} already started.')

    def stop(self, implicit=False) -> None:
        if self.inspect.started:
            self.cmd('stop', '@CONTAINER@', quiet=True)
            Log.success(f'Container {self.container_name()} successfully stopped.')
        elif not implicit:
            if self.inspect.created:
                Log.success(f'Container {self.container_name()} was not running.')
            else:
                Log.warning(f'Container {self.container_name()} does not exist.')

    def delete(self, implicit=False) -> None:
        self.stop(implicit=True)
        if self.inspect.created:
            self.cmd('rm', '@CONTAINER@', quiet=True)
            Log.success(f'Container {self.container_name()} successfully deleted.')
        elif not implicit:
            Log.warning(f'Container {self.container_name()} does not exist.')


class Log():
    @staticmethod
    def cmd(args) -> None:
        if sys.stdin.isatty():
            escaped = ' '.join(shlex.quote(a) for a in args)
            click.echo(click.style(f"$ {escaped}", fg="cyan"))

    @staticmethod
    def log(message) -> None:
        click.echo(message)

    @staticmethod
    def fatal(message) -> NoReturn:
        Log.error(message)
        sys.exit(1)

    @staticmethod
    def error(message) -> None:
        click.echo(f"{click.style('ERROR:', fg='red')} {message}")

    @staticmethod
    def success(message) -> None:
        click.echo(f"{click.style('SUCCESS:', fg='green')} {message}")

    @staticmethod
    def warning(message) -> None:
        click.echo(f"{click.style('WARNING:', fg='yellow')} {message}")
