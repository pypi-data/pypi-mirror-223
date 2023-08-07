from .device import Device

class Room:
    id: str
    name: str
    devices: list[Device]
    household_id: str

    def __init__(self, id: str, name: str, devices: list[Device], household_id: str):
        self.id = id
        self.name = name
        self.devices = devices
        self.household_id = household_id

    def __str__(self) -> str:
        return f'<Room id={self.id} name={self.name} devices={self.devices} household_id={self.household_id}>'
    
    def __repr__(self) -> str:
        return self.__str__()