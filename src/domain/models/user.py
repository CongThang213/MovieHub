from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

from src.domain.enums.account_type import AccountType


@dataclass
class User:
    id: str = None
    name: str = ""
    email: str = ""
    account_type: AccountType = AccountType.CUSTOMER
    date_of_birth: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.now)

    def get_age(self) -> Optional[int]:
        if self.date_of_birth:
            today = date.today()
            age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
            return age
        return None
