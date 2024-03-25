from dataclasses import dataclass


@dataclass
class RecordModel:
    record: int
    reward: float
    model_name: str
