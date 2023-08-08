from dataclasses import dataclass, asdict

from happy_python import dict_to_pretty_json


@dataclass
class ZySystemdServiceProp:
    """
    see 'man org.freedesktop.systemd1'
    """
    exec_start: str
    exec_stop: str
    exec_reload: str
    type: str
    pid_file: str
    main_pid: int
    exec_main_pid: int

    def asdict(self):
        return asdict(self)

    def asjson(self):
        return dict_to_pretty_json(self.asdict())
