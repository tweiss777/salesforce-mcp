from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.utils.soql import SoqlModule
from dataclasses import dataclass
import pytest

@dataclass()
class Lead:
    Id: str
    Company: str
    LastName: str


class TestSoql:
    def setup_method(self):
        self.session = SalesforceSession(
            domain="bigthink.my.salesforce.com",
            client_id="dummy",
            client_secret="dummy",
            username="user",
            password="pass"
        )
        self.soql_instance = SoqlModule(self.session)

    def test_execute_soql(self, mocker):
        #  mock authentication
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}
        mocker.patch.object(self.session.session, "post", return_value=mock_token_response)

        # mock get request
        mock_get_response = mocker.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "totalSize": 1,
            "records":[
                {
                    "Id": "112ss",
                    "Company": "Dummy",
                    "LastName": "bar"
                }

            ]
        }
        mocker.patch.object(self.session.session, "get", return_value=mock_get_response)

        # mock query
        soql_result = self.soql_instance.execute_soql("SELECT Id, Name, LastName FROM Lead LIMIT 1", Lead)
        self.session.session.post.asset_called_once()
        self.session.session.get.asset_called_once()
        assert len(soql_result.records) >= 1
        assert soql_result.records[0].Id == "112ss"


    def test_execute_soql_no_type(self, mocker):
        #  mock authentication
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}
        mocker.patch.object(self.session.session, "post", return_value=mock_token_response)

        # mock get request
        mock_get_response = mocker.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "totalSize": 1,
            "records": [
                {
                    "Id": "112ss",
                    "Company": "Dummy",
                    "LastName": "bar"
                }

            ]
        }
        mocker.patch.object(self.session.session, "get", return_value=mock_get_response)

        # mock query
        soql_result = self.soql_instance.execute_soql("SELECT Id, Name, LastName FROM Lead LIMIT 1")
        self.session.session.post.asset_called_once()
        self.session.session.get.asset_called_once()
        assert len(soql_result.records) >= 1
        assert soql_result.records[0]["Id"] == "112ss"
