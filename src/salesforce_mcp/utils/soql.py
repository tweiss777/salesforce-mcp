from salesforce_mcp.services.SalesforceSession import SalesforceSession
from typing import TypeVar, Generic, Dict, Type, Optional
from dataclasses import dataclass
from urllib.parse import quote_plus
from salesforce_mcp.utils.dataClassMapper import dict_to_dataclass
T = TypeVar('T')

@dataclass
class SoqlResult(Generic[T]):
    totalSize: int
    records: list[T]

class SoqlModule:
    def __init__(self, sf_session: SalesforceSession, api_version = 61.0):
        self.sf_session = sf_session
        self.soql_endpoint = f"services/data/v{api_version}/query?q="

    def execute_soql[T](self,query: str, t: Optional[Type[T]]=None) -> SoqlResult[T]:
        try:
            encoded_query = quote_plus(query, safe='/')
            full_endpoint = self.soql_endpoint + encoded_query
            query_result: Dict[str,str] = self.sf_session.get(full_endpoint)
            records = [
                dict_to_dataclass(row, t) if t is not None else row for row in query_result.get('records', [])
            ]
            return SoqlResult(
                records=records,
                totalSize=query_result.get('totalSize', 0),
            )
        except Exception as e:
            raise e

