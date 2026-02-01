from pydantic import BaseModel
from typing import List, Optional

class ProductResponse(BaseModel):
    id: str 
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] 

    class Config:
        from_attributes = True 

    
class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None


class BulkDeleteRequest(BaseModel):
    ids: List[str]


class ProductStatsByCategory(BaseModel):
    category: str
    count: int
    avg_price: float


class CustomerCreate(BaseModel):
    email: str
    password: str

class CustomerResponse(BaseModel):
    id: str 
    email: str
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    product_id: str
    customer_id: str
    review_text: str
    rating: int


class ReviewResponse(ReviewCreate):
    id: str  

    class Config:
        from_attributes = True 

class OrderCreate(BaseModel):
    customer_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str

class OrderResponse(OrderCreate):
    id: str  

    class Config:
        from_attributes = True  


class PaymentCreate(BaseModel):
    order_id: str
    amount: float
    payment_method: str
    payment_status: str


class PaymentResponse(PaymentCreate):
    id: str  
    class Config:
        from_attributes = True