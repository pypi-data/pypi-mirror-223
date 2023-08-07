import dataclasses

@dataclasses.dataclass
class Valid:
    pass

@dataclasses.dataclass
class Error:
    text: str