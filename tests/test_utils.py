from salesforce_mcp.utils.dataClassMapper import dict_to_dataclass
from salesforce_mcp.utils.soql import SoqlResult
from dataclasses import is_dataclass
import pytest



class TestUtils:
    def test_dict_to_dataclass(self):
        mock_dict = {
            "totalSize": 12,
            "records": {"Id": "Dummy results"}
        }
        mapped_soql_result = dict_to_dataclass(mock_dict,SoqlResult)
        assert is_dataclass(mapped_soql_result) and isinstance(mapped_soql_result, SoqlResult)
        assert mapped_soql_result.totalSize == 12
        pass


