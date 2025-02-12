from dataclasses import dataclass

@dataclass
class Section:
    name: str
    url: str

@dataclass
class Doctor:
    name: str
    position: str
    url: str

@dataclass
class Service:
    name: str
    value: str
    additionalValues: list[str]

@dataclass
class Procedure:
    name: str
    serviceTitleFields: list[str]
    services: list[Service]   

@dataclass
class ProcedureCategory:
    name: str
    subCategories: list[Procedure] 