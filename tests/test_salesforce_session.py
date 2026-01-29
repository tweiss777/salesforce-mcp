from salesforce_mcp.services.SalesforceSession import SalesforceSession
import pytest
class TestSalesforceSession:
    """Unit tests for SalesforceSession domain validation."""
    def setup_method(self):
        self.session = SalesforceSession(
        domain="bigthink.my.salesforce.com",
        client_id="dummy",
        client_secret="dummy",
        username="user",
        password="pass"
    )

    def test_validate_domain(self) -> None:
        """Verify that a list of known-good Salesforce domains passes validation."""
        domains: list[str] = [
            "bigthink.my.salesforce.com",
            "salesforce.com",
            "bigthink--devbox.sandbox.salesforce.com",
            "www.bigthink--devbox.sandbox.salesforce.com",
        ]
        try:
            # If any domain is invalid, _validate_domain will raise, causing the test to fail.
            for domain in domains:
                SalesforceSession._validate_domain(domain)
            assert True, "All validations pass"
        except:
            assert False, "Exception was not supposed to be thrown"

    def test_invalid_domain(self):
        """Verify that a list of known-good Salesforce domains fails validation."""
        domains: list[str] = [
            "https://bigthink.my.salesforce.com",
            "http://salesforce.com",
            "https://bigthink--devbox.sandbox.salesforce.com",
        ]
        for domain in domains:
            try:
                SalesforceSession._validate_domain(domain)
                assert False, f"{domain} was supposed to be valid"
            except:
                continue


    def test_authenticate_returns_token(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "fake-token"}
        mocker.patch.object(self.session.session, "post", return_value=mock_response)

        # Call the method under test
        token = self.session.authenticate()
        # Assertions
        assert token == "fake-token"
        self.session.session.post.assert_called_once()
        called_url = self.session.session.post.call_args[0][0]
        assert "https://bigthink.my.salesforce.com/services/oauth2/token" in called_url

    def test_get_method(self, mocker):
        # setup mock token response
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}
        mocker.patch.object(self.session.session, "post", return_value=mock_token_response)

        # setup mock get response
        mock_get_response = mocker.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {"mock_field": "mock_response"}
        mocker.patch.object(self.session.session, "get", return_value=mock_get_response)
        result = self.session.get('sobject/lead?id=00x1111AX')

        # Assertions
        self.session.session.post.asset_called_once()
        self.session.session.get.asset_called_once()
        called_token_url = self.session.session.post.call_args[0][0]
        called_get_url = self.session.session.get.call_args[0][0]
        assert result["mock_field"] == "mock_response"
        assert "https://bigthink.my.salesforce.com/services/oauth2/token" in called_token_url
        assert "https://bigthink.my.salesforce.com/sobject/lead?id=00x1111AX" in called_get_url

    def test_post_method(self, mocker):
        # mock the token authentication
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

        mock_payload = {
            "Company": "Test",
            "LastName": "Weiss"
        }
        result = self.session.create("sobject/lead", mock_payload)
        print(result)
        # Assertions
        self.session.session.post.asset_called_once()
        called_post_url = self.session.session.post.call_args[0][0]
        assert result["Id"] == "mock_id"
        assert "https://bigthink.my.salesforce.com/sobject/lead" in called_post_url


    def test_patch_method(self, mocker):
        # mock the token authentication
        mock_token_response = mocker.Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "fake-token"}

        # mock record creation
        mock_patch_response = mocker.Mock()
        mock_patch_response.status_code = 204

        mocker.patch.object(self.session.session, "post")
        mocker.patch.object(self.session.session, "patch")

        mock_payload = {
            "Company": "Test",
            "LastName": "Weiss"
        }
        route = "sobject/lead/"
        mock_id = "mock_id"
        result = self.session.update(route, id=mock_id, body=mock_payload)
        print(result)
        # Assertions
        self.session.session.patch.assert_called_once()
        self.session.session.post.assert_called_once()
        called_patch_url = self.session.session.patch.call_args[0][0]
        assert "https://bigthink.my.salesforce.com/sobject/lead/mock_id" in called_patch_url

