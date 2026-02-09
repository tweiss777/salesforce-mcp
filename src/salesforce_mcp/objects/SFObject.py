from dataclasses import dataclass
from typing import TypeVar
from abc import ABC, abstractmethod
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.SFRecord import SFRecord

T = TypeVar('T')

@dataclass
class RecordResult:
    Id: str

class SfObject[T](ABC):

    def __init__(self, sf_session: SalesforceSession):
        self.sf_session = sf_session


    @abstractmethod
    def create(self, data:T) -> RecordResult:
        pass

    @abstractmethod
    def update(self, data: T, record_id: str) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def get(self, id: str) -> SFRecord:
        pass