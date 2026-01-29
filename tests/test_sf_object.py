
from salesforce_mcp.objects.LeadObject import LeadObject
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.LeadRecord import LeadRecord
import pytest
class TestSfObject:
    def setup_method(self):
        self.session = SalesforceSession(
        domain="bigthink.my.salesforce.com",
        client_id="dummy",
        client_secret="dummy",
        username="user",
        password="pass")
        self.lead_object = LeadObject(self.session)

    def test_create(self, mocker):
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        # mock record creation
        mock_post_response = mocker.Mock()
        mock_post_response.status_code = 201
        mock_post_response.json.return_value = {"Id": "mock_id"}

        # Patch post once and set side_effect for two calls
        mock_post = mocker.patch.object(self.session.session, "post")
        mock_post.side_effect = [mock_token_response, mock_post_response]

        lead = LeadRecord(LastName="Weiss",Company="Test Company")
        result = self.lead_object.create(lead)
        assert result["Id"] == "mock_id"

    def test_update(self, mocker):
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_patch_response = mocker.Mock()
        mock_patch_response.status_code = 204
        mock_patch_response.json.return_value = {}

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_patch = mocker.patch.object(self.session.session, "patch", return_value=mock_patch_response)

        lead = LeadRecord(LastName="Weiss", Company="Test Company")
        self.lead_object.update(lead, "mock_id")

        mock_post.assert_called_once()
        mock_patch.assert_called_once()

    def test_get(self, mocker):
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_get_response = mocker.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {"Id": "mock_id", "LastName": "Weiss", "Company": "Test Company"}

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_get = mocker.patch.object(self.session.session, "get", return_value=mock_get_response)

        result = self.lead_object.get("mock_id")

        assert isinstance(result, LeadRecord)
        assert result.Id == "mock_id"
        assert result.LastName == "Weiss"
        assert result.Company == "Test Company"

        mock_post.assert_called_once()
        mock_get.assert_called_once()

    def test_delete(self, mocker):
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_delete_response = mocker.Mock()
        mock_delete_response.status_code = 204
        mock_delete_response.json.return_value = {}

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_delete = mocker.patch.object(self.session.session, "delete", return_value=mock_delete_response)

        result = self.lead_object.delete("mock_id")

        assert result is True

        mock_post.assert_called_once()
        mock_delete.assert_called_once()





