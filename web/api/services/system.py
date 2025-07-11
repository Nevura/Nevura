import socket
import subprocess
from ..models.system import SystemInfo

def get_timezone() -> str:
    try:
        return subprocess.check_output(["timedatectl"], encoding="utf-8").split("Time zone:")[1].split()[0]
    except Exception:
        try:
            with open("/etc/timezone", "r") as tz:
                return tz.read().strip()
        except FileNotFoundError:
            return "UTC"

def get_os_version() -> str:
    try:
        return subprocess.check_output(["lsb_release", "-ds"], encoding="utf-8").strip().strip('"')
    except Exception:
        return "Unknown"

def fetch_system_info() -> SystemInfo:
    return SystemInfo(
        hostname=socket.gethostname(),
        timezone=get_timezone(),
        os_version=get_os_version()
    )