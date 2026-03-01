from salesforce_mcp.objects.SFObject import SfObject, RecordResult
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.AccountRecord import AccountRecord


class AccountObject(SfObject):
    def __init__(self, sf_session: SalesforceSession, api_version: str = "61.0"):
        """
        Initialize the AccountObject with a Salesforce session.

        Args:
            sf_session: The Salesforce session instance for API calls
            api_version: The Salesforce API version to use (default: "61.0")
        """
        super().__init__(sf_session)
        self.account_endpoint = f"services/data/v{api_version}/sobjects/Account/"

    def create(self, data: AccountRecord) -> RecordResult:
        """
        Create a new Account record.

        Args:
            data: The AccountRecord containing the account information to create

        Returns:
            RecordResult containing the new record's ID and success status
        """
        mapped_fields = data.to_salesforce_payload()
        # For create, don't include the trailing slash with ID
        response = self.sf_session.create(self.account_endpoint.rstrip('/'), mapped_fields)
        return response

    def update(self, record_id: str, data: AccountRecord) -> bool:
        """
        Update an existing Account record.

        Args:
            record_id: The Salesforce ID of the account to update
            data: The AccountRecord containing the updated account information

        Returns:
            True if the update was successful
        """
        mapped_fields = data.to_salesforce_payload()
        self.sf_session.update(self.account_endpoint, id=record_id, body=mapped_fields)
        return True

    def delete(self, record_id: str) -> bool:
        """
        Delete an Account record.

        Args:
            record_id: The Salesforce ID of the account to delete

        Returns:
            True if the deletion was successful
        """
        self.sf_session.delete(self.account_endpoint + record_id)
        return True

    def get(self, record_id: str) -> AccountRecord:
        """
        Get an Account record by ID.

        Args:
            record_id: The Salesforce ID of the account to retrieve

        Returns:
            AccountRecord containing the account information
        """
        response = self.sf_session.get(self.account_endpoint + record_id)
        return AccountRecord(**response)
