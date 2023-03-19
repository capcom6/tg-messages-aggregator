import pydantic


class Account(pydantic.BaseModel):
    phone: str
    pass
