from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Destination:
    """
    Understands a destination
    """

    description: str
    protocol: str
    port: Optional[int]
    endpoint: Optional[str]
    cidr: Optional[str]
    message: Optional[str]
    tls_versions: List[str]
