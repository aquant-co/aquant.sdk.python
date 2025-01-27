from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field


class Metadata(BaseModel):
    department: str | None = Field(None, description="Department of the user")
    preferred_language: str | None = Field(
        None, description="User's preferred language"
    )
    timezone: str | None = Field(None, description="User's timezone")


class CustomClaims(BaseModel):
    plan: str | None = Field(None, description="User's subscription plan")
    features: list[str] | None = Field(
        None, description="Features enabled for the user"
    )


class JWTTokenPayload(BaseModel):
    sub: UUID4 = Field(..., description="User ID (Subject)")
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email of the user")
    roles: list[str] = Field(..., description="Roles assigned to the user")
    permissions: list[str] = Field(..., description="Permissions assigned to the user")
    organization_id: UUID4 = Field(
        ..., description="Organization ID the user belongs to"
    )
    organization_name: str = Field(..., description="Name of the organization")
    session_id: UUID4 = Field(..., description="Unique session identifier for the user")
    ip_address: str = Field(..., description="IP address of the user")
    device_id: str = Field(..., description="Unique identifier for the user's device")
    iat: datetime = Field(..., description="Issued At timestamp")
    exp: datetime = Field(..., description="Expiration timestamp")
    auth_time: datetime = Field(..., description="Authentication timestamp")
    metadata: Metadata = Field(..., description="Additional metadata about the user")
    custom_claims: CustomClaims = Field(
        ..., description="Custom claims for application-specific logic"
    )
