from dataclasses import dataclass
from typing import List


@dataclass
class Delta:

    kind: str

    function: str

    line: int

    inputs: List[str]

    outputs: List[str]

    effects: List[str]

    evidence: str