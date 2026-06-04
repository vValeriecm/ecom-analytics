from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class SaleBase(BaseModel):
    transaction_id: str
    date: datetime
    product_name: str
    category: str
    quantity: int
    unit_price: float
    total_price: float
    region: str
    segment: str

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class KPIResponse(BaseModel):
    total_revenue: float
    aov: float
    total_orders: int
    growth_rate: float
    retention_rate: float

class SalesTrend(BaseModel):
    date: str
    total_price: float

class ProductPerformance(BaseModel):
    product_name: str
    total_price: float
    quantity: int

class CustomerInsights(BaseModel):
    segments: Dict[str, float]
    regions: Dict[str, float]
