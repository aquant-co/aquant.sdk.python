from pydantic import BaseModel

class RoleCreateRequest(BaseModel):
    name: str
    description: str
