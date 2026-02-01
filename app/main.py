from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductStatsByCategory, BulkDeleteRequest, CustomerCreate, CustomerResponse, ReviewCreate, ReviewResponse, OrderCreate, OrderResponse, PaymentCreate, PaymentResponse
from app.crud import ProductCRUD, CustomerCRUD, ReviewCRUD, OrderCRUD, PaymentCRUD
from app.db import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5500", "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5500", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_customer_crud() -> CustomerCRUD:
    return CustomerCRUD(get_db())


def get_product_crud() -> ProductCRUD:
    return ProductCRUD(get_db())


def get_review_crud() -> ReviewCRUD:
    return ReviewCRUD(get_db())


def get_order_crud() -> OrderCRUD:
    return OrderCRUD(get_db())


def get_payment_crud() -> PaymentCRUD:
    return PaymentCRUD(get_db())


@app.post("/signup/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, crud: CustomerCRUD = Depends(get_customer_crud)):
    existing_user = await crud.db.find_one({"email": customer.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_customer(customer)


@app.post("/login/")
async def login_customer(email: str, password: str, crud: CustomerCRUD = Depends(get_customer_crud)):
    user = await crud.authenticate_customer(email, password)
    return {"message": "Login successful", "user_id": user.id, "email": user.email}


@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.create_product(product)


@app.get("/products/", response_model=list[ProductResponse])
async def get_products(crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.get_all_products()


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.get_product_by_id(product_id)


@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductCreate, crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.update_product(product_id, product)


@app.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: str, crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.delete_product(product_id)


@app.patch("/products/{product_id}", response_model=ProductResponse)
async def partial_update_product(product_id: str, product: ProductUpdate, crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.partial_update_product(product_id, product)


@app.post("/products/bulk-delete")
async def bulk_delete_products(body: BulkDeleteRequest, crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.bulk_delete_products(body.ids)


@app.get("/products/stats/aggregation", response_model=list[ProductStatsByCategory])
async def get_products_stats(crud: ProductCRUD = Depends(get_product_crud)):
    return await crud.get_products_stats_by_category()


@app.post("/reviews/", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, crud: ReviewCRUD = Depends(get_review_crud)):
    return await crud.create_review(review)


@app.get("/products/{product_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews(product_id: str, crud: ReviewCRUD = Depends(get_review_crud)):
    return await crud.get_reviews_by_product_id(product_id)


@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, crud: OrderCRUD = Depends(get_order_crud)):
    return await crud.create_order(order)


@app.get("/customers/{customer_id}/orders", response_model=list[OrderResponse])
async def get_orders_by_customer_id(customer_id: str, crud: OrderCRUD = Depends(get_order_crud)):
    return await crud.get_orders_by_customer_id(customer_id)


@app.post("/payments/", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, crud: PaymentCRUD = Depends(get_payment_crud)):
    return await crud.create_payment(payment)


@app.get("/payments/{order_id}", response_model=PaymentResponse)
async def get_payment_by_order_id(order_id: str, crud: PaymentCRUD = Depends(get_payment_crud)):
    return await crud.get_payment_by_order_id(order_id)
