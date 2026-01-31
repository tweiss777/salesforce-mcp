from salesforce_mcp.objects.SFObject import SfObject, RecordResult
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.OpportunityRecord import OpportunityRecord

class OpportunityObject(SfObject):
    def __init__(self, sf_session: SalesforceSession, api_version: str = '61.0'):
        super().__init__(sf_session)
        self.opportunity_endpoint = f"services/data/v{api_version}/sobjects/Opportunity/"

    def create(self, data: OpportunityRecord) -> RecordResult:
        """Create a new Opportunity Field"""
        mapped_fields = data.to_salesforce_payload()
        response = self.sf_session.create(self.opportunity_endpoint.rstrip('/'), mapped_fields)
        return response

    def update(self, data: OpportunityRecord, record_id: str) -> None:
        """Update an existing Opportunity record"""
        mapped_fields = data.to_salesforce_payload()
        self.sf_session.update(self.opportunity_endpoint, id=record_id, body=mapped_fields)

    def delete(self, record_id: str) -> bool:
        """Delete a Opportunity record"""
        self.sf_session.delete(self.lead_endpoint + record_id)
        return True

    def get(self, record_id: str) -> OpportunityRecord:
        response = self.sf_session.get(self.opportunity_endpoint + record_id)
        return OpportunityRecord(**response)


