from pydantic import BaseModel

class PermissionCreatedRequest(BaseModel):
    name: str
    description: str