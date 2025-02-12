from dataclasses import dataclass

@dataclass
class Section:
    name: str
    url: str

@dataclass
class Company:
    companyName: str
    address: str
    phoneNumber1: str
    phoneNumber2: str
    phoneNumber3: str
    employeeCount: int
    revenue: float
    director: str
    companyPage: str

