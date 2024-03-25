from dataclasses import dataclass
from typing import List, Dict, Any, Union

from snake_ai.record_model import RecordModel


@dataclass
class PersistentData:
    epoch: int
    record: int
    record_models: List[Union[Dict[str, Any], RecordModel]]
