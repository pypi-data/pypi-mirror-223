from typing import List
from abc import (
    ABC,
    abstractmethod,
)

from aws_network_firewall.destination import Destination
from aws_network_firewall.suricata import SuricataRule, SuricataOption
from aws_network_firewall.suricata.host import Host


class EngineAbstract(ABC):
    def __init__(self, sources: List[Host], name: str, workload: str) -> None:
        self.__sources = sources
        self.__name = name
        self.__workload = workload

    @property
    def suricata_source(self) -> List[Host]:
        return self.__sources

    @abstractmethod
    def parse(self, destination: Destination) -> List[SuricataRule]:
        raise NotImplementedError

    def resolve_options(self, destination: Destination) -> List[SuricataOption]:
        message = (
            f"{destination.message} | {self.__workload} | {self.__name}"
            if destination.message
            else f"{self.__workload} | {self.__name}"
        )

        return [
            SuricataOption(name="msg", value=message),
            SuricataOption(name="sid", value="XXX", quoted_value=False),
            SuricataOption(name="rev", value="1", quoted_value=False),
        ]
