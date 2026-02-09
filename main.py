# entry point for the actual mcp server
from salesforce_mcp.utils.soql import SoqlModule
from salesforce_mcp.objects.LeadObject import LeadObject
from salesforce_mcp.types.LeadRecord import LeadRecord
from salesforce_mcp.objects.OpportunityObject import OpportunityObject
from salesforce_mcp.types.OpportunityRecord import OpportunityRecord
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from dotenv import load_dotenv
from fastmcp import FastMCP
import logging, sys
from salesforce_mcp.utils.credentials import get_credentials
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr)
    ],
)

load_dotenv()

mcp: FastMCP = FastMCP(
    name="Salesforce MCP",
    instructions="""
        This server queues salesforce REST API to fetch data from the CRM.
        ...
    """
)


@mcp.tool(
    name="run_soql",
    description="""Queries Salesforce for data using soql.
        Any object or field that is not salesforce defined ends with __c
    """,
)
def run_soql(query: str):
    try:
        credentials = get_credentials()
        sf_session = SalesforceSession(
            domain=credentials.url,
            username=credentials.username,
            password=credentials.password,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret
        )
        soql = SoqlModule(sf_session)
        results = soql.execute_soql(query)
        return results
    except Exception as e:
        logging.error("Error occured while executing query")
        logging.error(e)
        raise e


@mcp.tool(
    name="run_lead_operation",
    description="""Runs CRUD operations for creating, updating, deleting, and fetching a Lead from Salesforce.
    
    Operations:
    - create: Creates a new Lead (requires LastName and Company)
    - update: Updates an existing Lead (requires lead_id)
    - delete: Deletes a Lead (requires lead_id)
    - get: Fetches a Lead by ID (requires lead_id)
    
    All Salesforce custom fields must end with __c.
    """,
)
def run_lead_operation(
        operation: str,
        lead_id: Optional[str] = None,
        # Required fields
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        # Standard fields
        first_name: Optional[str] = None,
        salutation: Optional[str] = None,
        title: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile_phone: Optional[str] = None,
        fax: Optional[str] = None,
        website: Optional[str] = None,
        lead_source: Optional[str] = None,
        status: Optional[str] = None,
        rating: Optional[str] = None,
        industry: Optional[str] = None,
        annual_revenue: Optional[float] = None,
        number_of_employees: Optional[int] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
        description: Optional[str] = None,
        owner_id: Optional[str] = None,
        is_converted: Optional[bool] = None,
        # Custom fields
        custom_fields: Optional[Dict[str, Any]] = None,
):
    """
    Perform CRUD operations on Salesforce Leads.
    
    Args:
        operation: One of 'create', 'update', 'delete', or 'get'
        lead_id: Required for update, delete, and get operations
        last_name: Lead's last name (required for create)
        company: Lead's company (required for create)
        first_name: Lead's first name
        salutation: Lead's salutation (e.g., 'Mr.', 'Ms.', 'Dr.')
        title: Lead's job title
        email: Lead's email address
        phone: Lead's phone number
        mobile_phone: Lead's mobile phone number
        fax: Lead's fax number
        website: Lead's website
        lead_source: Source of the lead (e.g., 'Web', 'Phone Inquiry', 'Partner Referral')
        status: Lead status (e.g., 'Open', 'Contacted', 'Qualified', 'Unqualified')
        rating: Lead rating (e.g., 'Hot', 'Warm', 'Cold')
        industry: Lead's industry
        annual_revenue: Lead's annual revenue
        number_of_employees: Number of employees at lead's company
        street: Street address
        city: City
        state: State/Province
        postal_code: Postal/ZIP code
        country: Country
        description: Description or notes about the lead
        owner_id: Salesforce User ID of the lead owner
        is_converted: Whether the lead has been converted
        custom_fields: Dictionary of custom Salesforce fields (e.g., {"My_Field__c": "value"})
    """
    try:
        credentials = get_credentials()
        sf_session = SalesforceSession(
            domain=credentials.url,
            username=credentials.username,
            password=credentials.password,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret
        )
        lead_object = LeadObject(sf_session)

        operation = operation.lower()

        if operation == "create":
            if not last_name or not company:
                raise ValueError("LastName and Company are required for creating a Lead")

            lead_data = LeadRecord(
                LastName=last_name,
                Company=company,
                FirstName=first_name,
                Salutation=salutation,
                Title=title,
                Email=email,
                Phone=phone,
                MobilePhone=mobile_phone,
                Fax=fax,
                Website=website,
                LeadSource=lead_source,
                Status=status,
                Rating=rating,
                Industry=industry,
                AnnualRevenue=annual_revenue,
                NumberOfEmployees=number_of_employees,
                Street=street,
                City=city,
                State=state,
                PostalCode=postal_code,
                Country=country,
                Description=description,
                OwnerId=owner_id,
                IsConverted=is_converted,
                custom_fields=custom_fields or {}
            )
            result = lead_object.create(lead_data)
            return {"success": True, "operation": "create", "result": result}

        elif operation == "update":
            if not lead_id:
                raise ValueError("lead_id is required for update operation")

            lead_data = LeadRecord(
                LastName=last_name,
                Company=company,
                FirstName=first_name,
                Salutation=salutation,
                Title=title,
                Email=email,
                Phone=phone,
                MobilePhone=mobile_phone,
                Fax=fax,
                Website=website,
                LeadSource=lead_source,
                Status=status,
                Rating=rating,
                Industry=industry,
                AnnualRevenue=annual_revenue,
                NumberOfEmployees=number_of_employees,
                Street=street,
                City=city,
                State=state,
                PostalCode=postal_code,
                Country=country,
                Description=description,
                OwnerId=owner_id,
                IsConverted=is_converted,
                custom_fields=custom_fields or {}
            )
            result = lead_object.update(lead_id, lead_data)
            return {"success": True, "operation": "update", "lead_id": lead_id, "result": result}

        elif operation == "delete":
            if not lead_id:
                raise ValueError("lead_id is required for delete operation")

            result = lead_object.delete(lead_id)
            return {"success": True, "operation": "delete", "lead_id": lead_id, "deleted": result}

        elif operation == "get":
            if not lead_id:
                raise ValueError("lead_id is required for delete operation")
            result = lead_object.get(lead_id)
            return {"success": True, "operation": "delete", "lead_id": lead_id, "result": result}
    except Exception as err:
        raise err


@mcp.tool(
    name="run_opportunity_operation",
    description="""Runs CRUD operations for creating, updating, deleting, and fetching an Opportunity from Salesforce.

    Operations:
    - create: Creates a new Opportunity (requires Name, StageName, and CloseDate)
    - update: Updates an existing Opportunity (requires opportunity_id)
    - delete: Deletes an Opportunity (requires opportunity_id)
    - get: Fetches an Opportunity by ID (requires opportunity_id)

    All Salesforce custom fields must end with __c.
    """,
)
def run_opportunity_operation(
        operation: str,
        opportunity_id: Optional[str] = None,
        # Required fields
        name: Optional[str] = None,
        stage_name: Optional[str] = None,
        close_date: Optional[str] = None,  # Format: YYYY-MM-DD
        # Standard fields
        account_id: Optional[str] = None,
        record_type_id: Optional[str] = None,
        is_private: Optional[bool] = None,
        description: Optional[str] = None,
        amount: Optional[float] = None,
        probability: Optional[float] = None,
        expected_revenue: Optional[float] = None,
        total_opportunity_quantity: Optional[float] = None,
        type: Optional[str] = None,
        next_step: Optional[str] = None,
        lead_source: Optional[str] = None,
        is_closed: Optional[bool] = None,
        is_won: Optional[bool] = None,
        forecast_category: Optional[str] = None,
        campaign_id: Optional[str] = None,
        pricebook2_id: Optional[str] = None,
        owner_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        contract_id: Optional[str] = None,
        synced_quote_id: Optional[str] = None,
        # Custom fields
        custom_fields: Optional[Dict[str, Any]] = None,
):
    """
    Perform CRUD operations on Salesforce Opportunities.

    Args:
        operation: One of 'create', 'update', 'delete', or 'get'
        opportunity_id: Required for update, delete, and get operations
        name: Opportunity name (required for create)
        stage_name: Stage name (required for create, e.g., 'Prospecting', 'Qualification', 'Closed Won')
        close_date: Close date in YYYY-MM-DD format (required for create)
        account_id: Associated Account ID
        record_type_id: Record Type ID
        is_private: Whether the opportunity is private
        description: Description or notes about the opportunity
        amount: Opportunity amount
        probability: Probability percentage (0-100)
        expected_revenue: Expected revenue
        total_opportunity_quantity: Total quantity
        type: Opportunity type (e.g., 'New Customer', 'Existing Customer')
        next_step: Next step in the sales process
        lead_source: Source of the opportunity
        is_closed: Whether the opportunity is closed
        is_won: Whether the opportunity is won
        forecast_category: Forecast category
        campaign_id: Associated Campaign ID
        pricebook2_id: Price Book ID
        owner_id: Salesforce User ID of the opportunity owner
        contact_id: Associated Contact ID
        contract_id: Associated Contract ID
        synced_quote_id: Synced Quote ID
        custom_fields: Dictionary of custom Salesforce fields (e.g., {"My_Field__c": "value"})
    """
    try:
        credentials = get_credentials()
        sf_session = SalesforceSession(
            domain=credentials.url,
            username=credentials.username,
            password=credentials.password,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret
        )
        opportunity_object = OpportunityObject(sf_session)

        operation = operation.lower()

        if operation == "create":
            if not name or not stage_name or not close_date:
                raise ValueError("Name, StageName, and CloseDate are required for creating an Opportunity")

            opportunity_data = OpportunityRecord(
                Name=name,
                StageName=stage_name,
                CloseDate=close_date,
                AccountId=account_id,
                RecordTypeId=record_type_id,
                IsPrivate=is_private,
                Description=description,
                Amount=amount,
                Probability=probability,
                ExpectedRevenue=expected_revenue,
                TotalOpportunityQuantity=total_opportunity_quantity,
                Type=type,
                NextStep=next_step,
                LeadSource=lead_source,
                IsClosed=is_closed,
                IsWon=is_won,
                ForecastCategory=forecast_category,
                CampaignId=campaign_id,
                Pricebook2Id=pricebook2_id,
                OwnerId=owner_id,
                ContactId=contact_id,
                ContractId=contract_id,
                SyncedQuoteId=synced_quote_id,
                custom_fields=custom_fields or {}
            )
            result = opportunity_object.create(opportunity_data)
            return {"success": True, "operation": "create", "result": result}

        elif operation == "update":
            if not opportunity_id:
                raise ValueError("opportunity_id is required for update operation")

            opportunity_data = OpportunityRecord(
                Name=name,
                StageName=stage_name,
                CloseDate=close_date,
                AccountId=account_id,
                RecordTypeId=record_type_id,
                IsPrivate=is_private,
                Description=description,
                Amount=amount,
                Probability=probability,
                ExpectedRevenue=expected_revenue,
                TotalOpportunityQuantity=total_opportunity_quantity,
                Type=type,
                NextStep=next_step,
                LeadSource=lead_source,
                IsClosed=is_closed,
                IsWon=is_won,
                ForecastCategory=forecast_category,
                CampaignId=campaign_id,
                Pricebook2Id=pricebook2_id,
                OwnerId=owner_id,
                ContactId=contact_id,
                ContractId=contract_id,
                SyncedQuoteId=synced_quote_id,
                custom_fields=custom_fields or {}
            )
            result = opportunity_object.update(opportunity_data, opportunity_id)
            return {"success": True, "operation": "update", "opportunity_id": opportunity_id, "result": result}

        elif operation == "delete":
            if not opportunity_id:
                raise ValueError("opportunity_id is required for delete operation")

            result = opportunity_object.delete(opportunity_id)
            return {"success": True, "operation": "delete", "opportunity_id": opportunity_id, "deleted": result}

        elif operation == "get":
            if not opportunity_id:
                raise ValueError("opportunity_id is required for get operation")
            result = opportunity_object.get(opportunity_id)
            return {"success": True, "operation": "get", "opportunity_id": opportunity_id, "result": result}

        else:
            raise ValueError(f"Invalid operation: {operation}. Must be one of: create, update, delete, get")

    except Exception as err:
        raise err

if __name__ == '__main__':
    try:
        logging.info("Starting MCP Server")
        mcp.run()

    except Exception as err:
        logging.error("Error initializing MCP server", exc_info=True)
        raise err