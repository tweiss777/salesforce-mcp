from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from salesforce_mcp.types.SFRecord import SFRecord


@dataclass
class LeadRecord(SFRecord):
    # ===== Required (Salesforce-enforced) =====
    LastName: str = None
    Company: str = None
    # ===== Common Standard Fields =====
    FirstName: Optional[str] = None
    Salutation: Optional[str] = None
    Title: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    MobilePhone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    LeadSource: Optional[str] = None
    Status: Optional[str] = None
    Rating: Optional[str] = None
    Industry: Optional[str] = None
    AnnualRevenue: Optional[float] = None
    NumberOfEmployees: Optional[int] = None
    Street: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    PostalCode: Optional[str] = None
    Country: Optional[str] = None
    Description: Optional[str] = None
    OwnerId: Optional[str] = None
    IsConverted: Optional[bool] = None
    # Redefine Id to ensure proper field order
    Id: Optional[str] = None
