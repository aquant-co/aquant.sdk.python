from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Schema for JWT response after successful login/authentication
    """
    access_token: str
    token_type: str = "bearer"