import pytest
from salesforce_mcp.objects.OpportunityObject import OpportunityObject
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.OpportunityRecord import OpportunityRecord


class TestOpportunityObject:
    def setup_method(self):
        self.session = SalesforceSession(
        domain="bigthink.my.salesforce.com",
        client_id="dummy",
        client_secret="dummy",
        username="user",
        password="pass")
        self.opportunity_object = OpportunityObject(self.session)

    def test_create(self, mocker):
        # create mock token
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        # create mock record
        mock_post_response = mocker.Mock()
        mock_post_response.status_code = 201
        mock_post_response.json.return_value = {"Id": "mock_id"}

        mock_post = mocker.patch.object(self.session.session, "post")
        mock_post.side_effect = [mock_token_response, mock_post_response]
        opp = OpportunityRecord(Name="Test Opp", StageName="Application In", CloseDate="2026-12-12")
        result = self.opportunity_object.create(opp)
        assert mock_post.call_count == 2
        assert result["Id"] == "mock_id"

    def test_update(self,mocker):
        # mock token (post request)
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_patch_response = mocker.Mock()
        mock_patch_response.status_code = 204
        mock_patch_response.json.return_value = {}
        # mock patch request
        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_patch = mocker.patch.object(self.session.session, "patch", return_value=mock_patch_response)

        oppToUpdate = OpportunityRecord(Name="Test Opp", StageName="Application In", CloseDate="2026-12-12")
        self.opportunity_object.update(oppToUpdate, "mock_id")

        assert mock_post.call_count == 1
        assert mock_patch.call_count == 1

    def test_delete(self,mocker):
        # mock token (post request)
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_delete_response = mocker.Mock()
        mock_delete_response.status_code = 204
        mock_delete_response.json.return_value = {}

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_delete = mocker.patch.object(self.session.session, "delete", return_value=mock_delete_response)

        self.opportunity_object.delete("mock_id")

        assert mock_post.call_count == 1
        assert mock_delete.call_count == 1

    def test_get(self,mocker):
        # mock token (post request)
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_get_response = mocker.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "Id": "mock_id",
            "Name": "Test Opp",
            "StageName": "Application In",
            "CloseDate": "2026-12-12"
        }

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_get = mocker.patch.object(self.session.session, "get", return_value=mock_get_response)

        result = self.opportunity_object.get("mock_id")
        assert isinstance(result, OpportunityRecord)
        assert mock_post.call_count == 1
        assert mock_get.call_count == 1
        assert result.Id == "mock_id"
        assert result.Name == "Test Opp"
