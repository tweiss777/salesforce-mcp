from  salesforce_mcp.objects.AccountObject import AccountObject
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.AccountRecord import AccountRecord
class TestAccountObject:
    def setup_method(self):
        self.session = SalesforceSession(
        domain="bigthink.my.salesforce.com",
        client_id="dummy",
        client_secret="dummy",
        username="user",
        password="pass")
        self.account_object = AccountObject(self.session)

    def test_create(self,mocker): 
        # create mock token
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        # create mock record
        mock_post_response = mocker.Mock()
        mock_post_response.status_code = 201
        mock_post_response.json.return_value = {"Id": "mock_id"}

        # mock and post
        mock_post = mocker.patch.object(self.session.session,'post')
        mock_post.side_effect = [mock_token_response, mock_post_response]
        acc = AccountRecord(Name="Test Account")
        result = self.account_object.create(acc)

        # test assetions
        assert mock_post.call_count == 2
        assert result["Id"] == "mock_id"

    def test_get(self,mocker):
        # mock token response
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        # mock get response
        mock_get_response = mocker.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "Id": "mock_id",
            "Name": "Test Acc"
        }

        # mock get and post requests
        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_get = mocker.patch.object(self.session.session, "get", return_value=mock_get_response)

        # fetch result
        result = self.account_object.get("mock_id")

        # assertions
        assert isinstance(result, AccountRecord)
        assert mock_post.call_count == 1
        assert mock_get.call_count == 1
        assert result.Id == "mock_id"
        assert result.Name == "Test Acc"

    def test_update(self, mocker):
        # mock token (post request)
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_patch_response = mocker.Mock()
        mock_patch_response.status_code = 204
        mock_patch_response.json.return_value = {}

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_patch = mocker.patch.object(self.session.session, "patch", return_value=mock_patch_response)

        acc_to_update = AccountRecord(Name="Updated Account")
        result = self.account_object.update("mock_id", acc_to_update)

        assert mock_post.call_count == 1
        assert mock_patch.call_count == 1
        assert result is True

    def test_delete(self, mocker):
        # mock token (post request)
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        mock_delete_response = mocker.Mock()
        mock_delete_response.status_code = 204
        mock_delete_response.json.return_value = {}

        mock_post = mocker.patch.object(self.session.session, "post", return_value=mock_token_response)
        mock_delete = mocker.patch.object(self.session.session, "delete", return_value=mock_delete_response)

        result = self.account_object.delete("mock_id")

        assert mock_post.call_count == 1
        assert mock_delete.call_count == 1
        assert result is True
