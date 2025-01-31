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
class Price:
    name: str
    value: str