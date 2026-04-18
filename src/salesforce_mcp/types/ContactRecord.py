from dataclasses import dataclass
from typing import Optional, Dict, Any

from salesforce_mcp.types.SFRecord import SFRecord


@dataclass
class ContactRecord(SFRecord):
    # ===== Required (Salesforce-enforced) =====
    LastName: str = None

    # ===== Common Standard Fields =====
    FirstName: Optional[str] = None
    Salutation: Optional[str] = None
    MiddleName: Optional[str] = None
    Suffix: Optional[str] = None

    Name: Optional[str] = None  # Read-only composite full name
    Email: Optional[str] = None
    Phone: Optional[str] = None
    HomePhone: Optional[str] = None
    MobilePhone: Optional[str] = None
    OtherPhone: Optional[str] = None
    Fax: Optional[str] = None

    Title: Optional[str] = None
    Department: Optional[str] = None

    MailingStreet: Optional[str] = None
    MailingCity: Optional[str] = None
    MailingState: Optional[str] = None
    MailingPostalCode: Optional[str] = None
    MailingCountry: Optional[str] = None
    MailingStateCode: Optional[str] = None
    MailingCountryCode: Optional[str] = None

    OtherStreet: Optional[str] = None
    OtherCity: Optional[str] = None
    OtherState: Optional[str] = None
    OtherPostalCode: Optional[str] = None
    OtherCountry: Optional[str] = None
    OtherStateCode: Optional[str] = None
    OtherCountryCode: Optional[str] = None

    EmailBouncedReason: Optional[str] = None
    EmailBouncedDate: Optional[str] = None  # Datetime string

    DoNotCall: Optional[bool] = None
    HasOptedOutOfEmail: Optional[bool] = None
    HasOptedOutOfFax: Optional[bool] = None

    Birthdate: Optional[str] = None  # Date string (YYYY-MM-DD)
    Description: Optional[str] = None

    LeadSource: Optional[str] = None
    Department: Optional[str] = None

    OwnerId: Optional[str] = None
    AccountId: Optional[str] = None
    ReportsToId: Optional[str] = None

    AssistantName: Optional[str] = None
    AssistantPhone: Optional[str] = None

    Languages__c: Optional[str] = None  # Standard UI field often mapped to custom; keep as text

    Level__c: Optional[str] = None  # Often used in standard orgs as a picklist; keep generic

    # ===== System / Metadata (read-only in most contexts) =====
    Id: Optional[str] = None
    IsDeleted: Optional[bool] = None
    CreatedDate: Optional[str] = None
    CreatedById: Optional[str] = None
    LastModifiedDate: Optional[str] = None
    LastModifiedById: Optional[str] = None
    SystemModstamp: Optional[str] = None
    LastActivityDate: Optional[str] = None
    LastCURequestDate: Optional[str] = None
    LastCUUpdateDate: Optional[str] = None
    LastViewedDate: Optional[str] = None
    LastReferencedDate: Optional[str] = None

    # ===== Custom fields container =====
    # Any additional custom Salesforce fields should be passed via this dict
    # using their API names, e.g. {"My_Custom_Field__c": "value"}
    custom_fields: Optional[Dict[str, Any]] = None