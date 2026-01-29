from salesforce_mcp.objects.SFObject import SfObject, RecordResult
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.LeadRecord import LeadRecord


class LeadObject(SfObject):
    def __init__(self, sf_session: SalesforceSession, api_version: str= "61.0"):
        super().__init__(sf_session)
        self.lead_endpoint = f"services/data/v{api_version}/sobjects/Lead/"

    def create(self, data: LeadRecord) -> RecordResult:
        """Create a new Lead record"""
        mapped_fields = data.to_salesforce_payload()
        # For create, don't include the trailing slash with ID
        response = self.sf_session.create(self.lead_endpoint.rstrip('/'), mapped_fields)
        return response

    def update(self, record_id: str, data: LeadRecord) -> bool:
        """Update an existing Lead record"""
        mapped_fields = data.to_salesforce_payload()
        self.sf_session.update(self.lead_endpoint, id=record_id, body=mapped_fields)
        return True

    def delete(self, record_id: str) -> bool:
        """Delete a Lead record"""
        self.sf_session.delete(self.lead_endpoint + record_id)
        return True

    def get(self, record_id: str) -> LeadRecord:
        """Get a Lead record by ID"""
        response = self.sf_session.get(self.lead_endpoint + record_id)
        return LeadRecord(**response)

