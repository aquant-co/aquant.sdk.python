from pydantic import BaseModel


class UserRoleCreateRequest(BaseModel):
    name: str
    description: str
