from pydantic import BaseModel, Field


class PostAccountRequest(BaseModel):
    phone: str = Field(regex=r"^7\d{10}$")


class PatchAccountSessionRequest(BaseModel):
    request_id: str
    code: str
    password: str | None
