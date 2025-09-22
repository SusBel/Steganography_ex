# access_control_v3.py
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    GUEST = "guest"

def permissions_for(role: Role):
    if role is Role.ADMIN:
        return {"Accsess_all", "Change_all"}
    if role is Role.EMPLOYEE:
        return {"Accsess_all"}
    if role is Role.GUEST:
        return {"Accsess_public"}
    return set()

class Person:
    def __init__(self, name: str, role: Role):
        self.name = name
        self.role = role

    def can(self, action: str) -> bool:
        return action in permissions_for(self.role)

if __name__ == "__main__":
    Benyay = Person("Benyay", Role.ADMIN)
    Asik = Person("Asik", Role.EMPLOYEE)
    Shon = Person("Shon", Role.GUEST)

    print(f"{Asik.name} can access everything? {Asik.can('Accsess_all')}")
    print(f"{Shon.name} can change things? {Shon.can('Change_all')}")
    print(f"{Benyay.name} can change things? {Benyay.can('Change_all')}")
