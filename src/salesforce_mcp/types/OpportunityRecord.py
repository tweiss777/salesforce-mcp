from dataclasses import dataclass
from typing import Optional
from salesforce_mcp.types.SFRecord import SFRecord

@dataclass
class OpportunityRecord(SFRecord):
    # ===== Required (Salesforce-enforced) =====
    Name: str = None
    StageName: str = None
    CloseDate: str = None  # Format: YYYY-MM-DD

    # ===== Common Standard Fields =====
    IsDeleted: Optional[bool] = None
    AccountId: Optional[str] = None
    RecordTypeId: Optional[str] = None
    IsPrivate: Optional[bool] = None
    Description: Optional[str] = None
    Amount: Optional[float] = None
    Probability: Optional[float] = None
    ExpectedRevenue: Optional[float] = None
    TotalOpportunityQuantity: Optional[float] = None
    Type: Optional[str] = None
    NextStep: Optional[str] = None
    LeadSource: Optional[str] = None
    IsClosed: Optional[bool] = None
    IsWon: Optional[bool] = None
    ForecastCategory: Optional[str] = None
    ForecastCategoryName: Optional[str] = None
    CampaignId: Optional[str] = None
    HasOpportunityLineItem: Optional[bool] = None
    Pricebook2Id: Optional[str] = None
    OwnerId: Optional[str] = None
    CreatedDate: Optional[str] = None
    CreatedById: Optional[str] = None
    LastModifiedDate: Optional[str] = None
    LastModifiedById: Optional[str] = None
    SystemModstamp: Optional[str] = None
    LastActivityDate: Optional[str] = None
    LastViewedDate: Optional[str] = None
    LastReferencedDate: Optional[str] = None
    ContactId: Optional[str] = None
    ContractId: Optional[str] = None
    SyncedQuoteId: Optional[str] = None
    HasOpenActivity: Optional[bool] = None
    HasOverdueTask: Optional[bool] = None
    LastStageChangeDate: Optional[str] = None
    FiscalQuarter: Optional[int] = None
    FiscalYear: Optional[int] = None
    Fiscal: Optional[str] = None
    PushCount: Optional[int] = None
    AgeInDays: Optional[int] = None
    LastActivityInDays: Optional[int] = None
    LastStageChangeInDays: Optional[int] = None
    IsPriorityRecord: Optional[bool] = None
    Id: Optional[str] = None
