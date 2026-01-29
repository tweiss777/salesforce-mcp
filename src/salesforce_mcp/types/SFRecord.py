from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class SFRecord:
    custom_fields: Dict[str, Any] = field(default_factory=dict, repr=False)

    def to_salesforce_payload(self) -> Dict[str, Any]:
        """
        Converts the record into a Salesforce-ready payload.
        - Removes None values
        - Merges custom fields
        """
        data = {
            k: v for k, v in vars(self).items()
            if v is not None and k != "custom_fields"
        }

        # Merge custom fields (expects Salesforce API names, e.g. My_Field__c)
        if self.custom_fields:
            data.update(self.custom_fields)
        return data
