# entry point for the actual mcp server
import logging
import sys
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP

from salesforce_mcp.objects.AccountObject import AccountObject
from salesforce_mcp.objects.LeadObject import LeadObject
from salesforce_mcp.objects.OpportunityObject import OpportunityObject
from salesforce_mcp.services.SalesforceSession import SalesforceSession
from salesforce_mcp.types.AccountRecord import AccountRecord
from salesforce_mcp.types.LeadRecord import LeadRecord
from salesforce_mcp.types.OpportunityRecord import OpportunityRecord
from salesforce_mcp.utils.credentials import get_credentials
from salesforce_mcp.utils.soql import SoqlModule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)

load_dotenv()

mcp: FastMCP = FastMCP(
    name="Salesforce MCP",
    instructions="""
        This server queues salesforce REST API to fetch data from the CRM.
        ...
    """,
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
            client_secret=credentials.client_secret,
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
            client_secret=credentials.client_secret,
        )
        lead_object = LeadObject(sf_session)

        operation = operation.lower()

        if operation == "create":
            if not last_name or not company:
                raise ValueError(
                    "LastName and Company are required for creating a Lead"
                )

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
                custom_fields=custom_fields or {},
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
                custom_fields=custom_fields or {},
            )
            result = lead_object.update(lead_id, lead_data)
            return {
                "success": True,
                "operation": "update",
                "lead_id": lead_id,
                "result": result,
            }

        elif operation == "delete":
            if not lead_id:
                raise ValueError("lead_id is required for delete operation")

            result = lead_object.delete(lead_id)
            return {
                "success": True,
                "operation": "delete",
                "lead_id": lead_id,
                "deleted": result,
            }

        elif operation == "get":
            if not lead_id:
                raise ValueError("lead_id is required for delete operation")
            result = lead_object.get(lead_id)
            return {
                "success": True,
                "operation": "delete",
                "lead_id": lead_id,
                "result": result,
            }
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
            client_secret=credentials.client_secret,
        )
        opportunity_object = OpportunityObject(sf_session)

        operation = operation.lower()

        if operation == "create":
            if not name or not stage_name or not close_date:
                raise ValueError(
                    "Name, StageName, and CloseDate are required for creating an Opportunity"
                )

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
                custom_fields=custom_fields or {},
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
                custom_fields=custom_fields or {},
            )
            result = opportunity_object.update(opportunity_data, opportunity_id)
            return {
                "success": True,
                "operation": "update",
                "opportunity_id": opportunity_id,
                "result": result,
            }

        elif operation == "delete":
            if not opportunity_id:
                raise ValueError("opportunity_id is required for delete operation")

            result = opportunity_object.delete(opportunity_id)
            return {
                "success": True,
                "operation": "delete",
                "opportunity_id": opportunity_id,
                "deleted": result,
            }

        elif operation == "get":
            if not opportunity_id:
                raise ValueError("opportunity_id is required for get operation")
            result = opportunity_object.get(opportunity_id)
            return {
                "success": True,
                "operation": "get",
                "opportunity_id": opportunity_id,
                "result": result,
            }

        else:
            raise ValueError(
                f"Invalid operation: {operation}. Must be one of: create, update, delete, get"
            )

    except Exception as err:
        raise err


@mcp.tool(
    name="run_account_operation",
    description="""Runs CRUD operations for creating, updating, deleting, and fetching an Account from Salesforce.

    Operations:
    - create: Creates a new Account (requires name)
    - update: Updates an existing Account (requires account_id)
    - delete: Deletes an Account (requires account_id)
    - get: Fetches an Account by ID (requires account_id)

    All Salesforce custom fields must end with __c.
    """,
)
def run_account_operation(
    operation: str,
    account_id: Optional[str] = None,
    # Required fields
    name: Optional[str] = None,
    # Classification
    type: Optional[str] = None,
    industry: Optional[str] = None,
    ownership: Optional[str] = None,
    rating: Optional[str] = None,
    account_source: Optional[str] = None,
    account_number: Optional[str] = None,
    # Financial
    annual_revenue: Optional[float] = None,
    number_of_employees: Optional[int] = None,
    sic: Optional[str] = None,
    sic_desc: Optional[str] = None,
    ticker_symbol: Optional[str] = None,
    # Contact info
    phone: Optional[str] = None,
    fax: Optional[str] = None,
    website: Optional[str] = None,
    site: Optional[str] = None,
    # Billing address
    billing_street: Optional[str] = None,
    billing_city: Optional[str] = None,
    billing_state: Optional[str] = None,
    billing_postal_code: Optional[str] = None,
    billing_country: Optional[str] = None,
    # Shipping address
    shipping_street: Optional[str] = None,
    shipping_city: Optional[str] = None,
    shipping_state: Optional[str] = None,
    shipping_postal_code: Optional[str] = None,
    shipping_country: Optional[str] = None,
    # Relationships
    parent_id: Optional[str] = None,
    owner_id: Optional[str] = None,
    record_type_id: Optional[str] = None,
    # Misc
    description: Optional[str] = None,
    # Custom fields
    custom_fields: Optional[Dict[str, Any]] = None,
):
    """
    Perform CRUD operations on Salesforce Accounts.

    Args:
        operation: One of 'create', 'update', 'delete', or 'get'
        account_id: Required for update, delete, and get operations
        name: Account name (required for create)
        type: Account type (e.g., 'Prospect', 'Customer', 'Partner')
        industry: Account industry
        ownership: Ownership type (e.g., 'Public', 'Private', 'Subsidiary')
        rating: Account rating (e.g., 'Hot', 'Warm', 'Cold')
        account_source: Source of the account
        account_number: Account number
        annual_revenue: Annual revenue
        number_of_employees: Number of employees
        sic: SIC code
        sic_desc: SIC description
        ticker_symbol: Stock ticker symbol
        phone: Primary phone number
        fax: Fax number
        website: Website URL
        site: Account site
        billing_street: Billing street address
        billing_city: Billing city
        billing_state: Billing state/province
        billing_postal_code: Billing postal/ZIP code
        billing_country: Billing country
        shipping_street: Shipping street address
        shipping_city: Shipping city
        shipping_state: Shipping state/province
        shipping_postal_code: Shipping postal/ZIP code
        shipping_country: Shipping country
        parent_id: Parent Account ID
        owner_id: Salesforce User ID of the account owner
        record_type_id: Record Type ID
        description: Description or notes about the account
        custom_fields: Dictionary of custom Salesforce fields (e.g., {"My_Field__c": "value"})
    """
    try:
        credentials = get_credentials()
        sf_session = SalesforceSession(
            domain=credentials.url,
            username=credentials.username,
            password=credentials.password,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
        )
        account_object = AccountObject(sf_session)

        operation = operation.lower()

        if operation == "create":
            if not name:
                raise ValueError("name is required for creating an Account")

            account_data = AccountRecord(
                Name=name,
                AccountNumber=account_number,
                Type=type,
                Industry=industry,
                Ownership=ownership,
                Rating=rating,
                AccountSource=account_source,
                AnnualRevenue=annual_revenue,
                NumberOfEmployees=number_of_employees,
                Sic=sic,
                SicDesc=sic_desc,
                TickerSymbol=ticker_symbol,
                Phone=phone,
                Fax=fax,
                Website=website,
                Site=site,
                BillingStreet=billing_street,
                BillingCity=billing_city,
                BillingState=billing_state,
                BillingPostalCode=billing_postal_code,
                BillingCountry=billing_country,
                ShippingStreet=shipping_street,
                ShippingCity=shipping_city,
                ShippingState=shipping_state,
                ShippingPostalCode=shipping_postal_code,
                ShippingCountry=shipping_country,
                ParentId=parent_id,
                OwnerId=owner_id,
                RecordTypeId=record_type_id,
                Description=description,
                custom_fields=custom_fields or {},
            )
            result = account_object.create(account_data)
            return {"success": True, "operation": "create", "result": result}

        elif operation == "update":
            if not account_id:
                raise ValueError("account_id is required for update operation")

            account_data = AccountRecord(
                Name=name,
                AccountNumber=account_number,
                Type=type,
                Industry=industry,
                Ownership=ownership,
                Rating=rating,
                AccountSource=account_source,
                AnnualRevenue=annual_revenue,
                NumberOfEmployees=number_of_employees,
                Sic=sic,
                SicDesc=sic_desc,
                TickerSymbol=ticker_symbol,
                Phone=phone,
                Fax=fax,
                Website=website,
                Site=site,
                BillingStreet=billing_street,
                BillingCity=billing_city,
                BillingState=billing_state,
                BillingPostalCode=billing_postal_code,
                BillingCountry=billing_country,
                ShippingStreet=shipping_street,
                ShippingCity=shipping_city,
                ShippingState=shipping_state,
                ShippingPostalCode=shipping_postal_code,
                ShippingCountry=shipping_country,
                ParentId=parent_id,
                OwnerId=owner_id,
                RecordTypeId=record_type_id,
                Description=description,
                custom_fields=custom_fields or {},
            )
            result = account_object.update(account_id, account_data)
            return {
                "success": True,
                "operation": "update",
                "account_id": account_id,
                "result": result,
            }

        elif operation == "delete":
            if not account_id:
                raise ValueError("account_id is required for delete operation")

            result = account_object.delete(account_id)
            return {
                "success": True,
                "operation": "delete",
                "account_id": account_id,
                "deleted": result,
            }

        elif operation == "get":
            if not account_id:
                raise ValueError("account_id is required for get operation")

            result = account_object.get(account_id)
            return {
                "success": True,
                "operation": "get",
                "account_id": account_id,
                "result": result,
            }

        else:
            raise ValueError(
                f"Invalid operation: {operation}. Must be one of: create, update, delete, get"
            )

    except Exception as err:
        raise err


if __name__ == "__main__":
    try:
        print("hello world")
        logging.info("Starting MCP Server")
        mcp.run()

    except Exception as err:
        logging.error("Error initializing MCP server", exc_info=True)
        raise err
