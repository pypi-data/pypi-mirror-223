import dbus
from happy_python import HappyLog

from zymod.systemd import ZySystemdManager
from .zy_systemd_service_prop import ZySystemdServiceProp


class ZySystemdService:
    def __init__(self, name: str):
        self.hlog = HappyLog.get_instance()
        self.name = name
        self.manager = ZySystemdManager()
        self.bus = dbus.SystemBus()
        self.obj_timer = self.bus.get_object(bus_name='org.freedesktop.systemd1',
                                             object_path=self.manager.get_unit(self.name))

        self.interface_props = dbus.Interface(object=self.obj_timer,
                                              dbus_interface='org.freedesktop.DBus.Properties')

    def get_prop(self, name: str):
        props = self.interface_props.GetAll('org.freedesktop.systemd1.Service')

        return props[name]

    def get_props(self) -> ZySystemdServiceProp:
        exec_start = self.get_prop('ExecStart')
        exec_stop = self.get_prop('ExecStop')
        exec_reload = self.get_prop('ExecReload')
        type_ = self.get_prop('Type')
        pid_file = self.get_prop('PIDFile')
        main_pid = self.get_prop('MainPID')
        exec_main_pid = self.get_prop('ExecMainPID')

        return ZySystemdServiceProp(exec_start=exec_start, exec_stop=exec_stop,
                                    exec_reload=exec_reload, type=type_,
                                    pid_file=pid_file, main_pid=main_pid,
                                    exec_main_pid=exec_main_pid)
