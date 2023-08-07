import dbus
from happy_python import HappyLog

from zymod.systemd import ZySystemdManager, ZySystemdUnitProp


class ZySystemdUnit:
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
        props = self.interface_props.GetAll('org.freedesktop.systemd1.Unit')
        return props[name]

    def get_props(self) -> ZySystemdUnitProp:
        prop_list = self.manager.list_units()

        for i in prop_list:
            if i.primary_unit_name == self.name:
                return ZySystemdUnitProp(active_state=i.active_state, desc=i.desc,
                                         load_state=i.load_state, object_path=i.object_path,
                                         primary_unit_name=i.primary_unit_name, sub_state=i.sub_state,
                                         followed=i.followed,job_object_path=i.job_object_path,job_id=i.job_id,
                                         job_type=i.job_type)
