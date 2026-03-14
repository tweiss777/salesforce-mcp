from salesforce_mcp.objects.SFObject import SfObject, RecordResult
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.ContactRecord import ContactRecord


class ContactObject(SfObject):
    def __init__(self, sf_session: SalesforceSession, api_version: str = "61.0"):
        """
        Initialize the ContactObject with a Salesforce session.

        Args:
            sf_session: The Salesforce session instance for API calls.
            api_version: The Salesforce API version to use (default: "61.0").
        """
        super().__init__(sf_session)
        self.contact_endpoint = f"services/data/v{api_version}/sobjects/Contact/"

    def create(self, data: ContactRecord) -> RecordResult:
        """
        Create a new Contact record.

        Args:
            data: The ContactRecord containing the contact information to create.

        Returns:
            RecordResult containing the new record's ID and success status.
        """
        mapped_fields = data.to_salesforce_payload()
        # For create, don't include the trailing slash with ID
        response = self.sf_session.create(self.contact_endpoint.rstrip("/"), mapped_fields)
        return response

    def update(self, record_id: str, data: ContactRecord) -> bool:
        """
        Update an existing Contact record.

        Args:
            record_id: The Salesforce ID of the contact to update.
            data: The ContactRecord containing the updated contact information.

        Returns:
            True if the update was successful.
        """
        mapped_fields = data.to_salesforce_payload()
        self.sf_session.update(self.contact_endpoint, id=record_id, body=mapped_fields)
        return True

    def delete(self, record_id: str) -> bool:
        """
        Delete a Contact record.

        Args:
            record_id: The Salesforce ID of the contact to delete.

        Returns:
            True if the deletion was successful.
        """
        self.sf_session.delete(self.contact_endpoint + record_id)
        return True

    def get(self, record_id: str) -> ContactRecord:
        """
        Get a Contact record by ID.

        Args:
            record_id: The Salesforce ID of the contact to retrieve.

        Returns:
            ContactRecord containing the contact information.
        """
        response = self.sf_session.get(self.contact_endpoint + record_id)
        return ContactRecord(**response)