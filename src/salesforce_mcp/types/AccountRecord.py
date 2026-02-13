from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from salesforce_mcp.types.SFRecord import SFRecord


@dataclass
class AccountRecord(SFRecord):
    # Identifiers
    Name: str = None
    Id: Optional[str] = None
    AccountNumber: Optional[str] = None

    # Classification
    Type: Optional[str] = None
    Industry: Optional[str] = None
    Ownership: Optional[str] = None
    Rating: Optional[str] = None
    AccountSource: Optional[str] = None

    # Financial
    AnnualRevenue: Optional[Decimal] = None
    NumberOfEmployees: Optional[int] = None
    Sic: Optional[str] = None
    SicDesc: Optional[str] = None
    TickerSymbol: Optional[str] = None

    # Contact Info
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    Site: Optional[str] = None

    # Addresses (flattened for REST payloads)
    BillingStreet: Optional[str] = None
    BillingCity: Optional[str] = None
    BillingState: Optional[str] = None
    BillingPostalCode: Optional[str] = None
    BillingCountry: Optional[str] = None

    ShippingStreet: Optional[str] = None
    ShippingCity: Optional[str] = None
    ShippingState: Optional[str] = None
    ShippingPostalCode: Optional[str] = None
    ShippingCountry: Optional[str] = None

    # Relationships (REST uses Ids)
    ParentId: Optional[str] = None
    OwnerId: Optional[str] = None
    RecordTypeId: Optional[str] = None

    # Misc
    Description: Optional[str] = None
    Id: Optional[str] = None
