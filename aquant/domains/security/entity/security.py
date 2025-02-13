from datetime import datetime

from pydantic import BaseModel, Field


class Security(BaseModel):
    asset: str | None = Field(None, description="Descrição do ativo")
    ticker: str = Field(..., description="Código do ativo")
    isin: str | None = Field(None, max_length=13, description="Código ISIN do ativo")
    cfi_code: str | None = Field(None, description="Código CFI do ativo")
    product: int | None = Field(None, description="Tipo de produto")
    type: int | None = Field(None, description="Tipo de ativo")
    sub_type: str | None = Field(None, description="Subtipo do ativo")
    name: str | None = Field(None, description="Nome do ativo")
    security_group: str | None = Field(None, description="Grupo de segurança do ativo")
    price_type: int = Field(0, description="Tipo de preço do ativo")
    currency: str | None = Field(None, description="Moeda do ativo")
    round_lot: int | None = Field(None, description="Lote padrão do ativo")
    tick_size_denominator: int | None = Field(
        None, description="Denominador do tamanho do tick"
    )
    min_order_quantity: int | None = Field(
        None, description="Quantidade mínima de ordem"
    )
    max_order_quantity: int | None = Field(
        None, description="Quantidade máxima de ordem"
    )
    min_price_increment: float | None = Field(
        None, description="Incremento mínimo de preço"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Data de criação do registro"
    )
    issued_at: datetime | None = Field(None, description="Data de emissão do ativo")
    issued_at_country: str | None = Field(
        None, max_length=2, description="País de emissão do ativo"
    )
    expires_at: datetime | None = Field(None, description="Data de expiração do ativo")
    expired_at: datetime | None = Field(
        None, description="Data de expiração efetiva do ativo"
    )

    class Config:
        from_attributes = True
