from pydantic import BaseModel, Field, field_validator

class AccountCreate(BaseModel):
    account_id: str = Field(..., min_length=3, max_length=20)
    initial_balance: float = Field(..., ge=0)

    @field_validator("account_id")
    @classmethod
    def account_id_no_spaces(cls, v):
        if " " in v:
            raise ValueError("account_id cannot contain spaces")
        return v
