from typing import Optional
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] = None

    class Config:
        from_attributes = True 


class Customer(BaseModel):
    id: str 
    email: str 
    password: str 

    class Config:
        from_attributes = True 

class Review(BaseModel):
    product_id: str
    customer_id: str
    review_text: str
    rating: int

    class Config:
        from_attributes = True

class Order(BaseModel):
    customer_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True

class Payment(BaseModel):
    order_id: str
    amount: float
    payment_method: str
    payment_status: str

    class Config:
        from_attributes = True