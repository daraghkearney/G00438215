from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

IdStr = Annotated[str, StringConstraints(pattern=r"^S\d{7}$")]
BorrowerNameStr = Annotated[str, StringConstraints(min_length=2, max_length=60)]
EquipmentIdStr = Annotated[str, StringConstraints(pattern={1})]

StatusStr = Annotated[str, StringConstraints("PENDING")]

class LoanCreate(BaseModel):
    borrower_name: BorrowerNameStr
    equipment_id: EquipmentIdStr
    loan_days: int = Field(gt=0, lt=15)
    purpose: chr = Field(gt=4, lt=101)
    status: StatusStr

class LoanRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    equipment_id: EquipmentIdStr
    borrower_name: BorrowerNameStr
    loan_days: int
    purpose: chr
    status: StatusStr