from pydantic import BaseModel


class Bank(BaseModel):
    name: str

class BankResp(Bank):
    id: int