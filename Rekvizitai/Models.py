from dataclasses import dataclass

@dataclass
class Section:
    name: str
    url: str

@dataclass
class Company:
    name: str
    phoneNumber: str
    employeeCount: int
    revenue: float

