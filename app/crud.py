from app.db import MongoDB, get_db
from app.models import Product, Customer, Review, Order, Payment
from app.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductStatsByCategory, CustomerCreate, CustomerResponse, ReviewCreate, ReviewResponse, OrderCreate, OrderResponse, PaymentCreate, PaymentResponse
from fastapi import HTTPException
from bson import ObjectId

class ProductCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("products") 

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        product_dict = product.dict()
        result = await self.db.insert_one(product_dict)
        product_dict["id"] = str(result.inserted_id)
        return ProductResponse(**product_dict)

    async def get_all_products(self) -> list[ProductResponse]:
        products = []
        async for product in self.db.find():
            product["id"] = str(product["_id"])
            products.append(ProductResponse(**product))
        return products

    async def get_product_by_id(self, product_id: str) -> ProductResponse:
        product = await self.db.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product["id"] = str(product["_id"])
        return ProductResponse(**product)

    async def update_product(self, product_id: str, product: ProductCreate) -> ProductResponse:
        update_result = await self.db.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product.dict()}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        updated_product = await self.db.find_one({"_id": ObjectId(product_id)})
        updated_product["id"] = str(updated_product["_id"])
        return ProductResponse(**updated_product)

    async def delete_product(self, product_id: str) -> ProductResponse:
        product = await self.db.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await self.db.delete_one({"_id": ObjectId(product_id)})
        product["id"] = str(product["_id"])
        return ProductResponse(**product)

    async def partial_update_product(self, product_id: str, update: ProductUpdate) -> ProductResponse:
        update_dict = {k: v for k, v in (update.model_dump() if hasattr(update, 'model_dump') else update.dict()).items() if v is not None}
        if not update_dict:
            return await self.get_product_by_id(product_id)
        update_result = await self.db.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_dict}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return await self.get_product_by_id(product_id)

    async def bulk_delete_products(self, product_ids: list[str]) -> dict:
        if not product_ids:
            return {"deleted_count": 0, "ids": []}
        object_ids = [ObjectId(pid) for pid in product_ids]
        result = await self.db.delete_many({"_id": {"$in": object_ids}})
        return {"deleted_count": result.deleted_count, "ids": product_ids}

    async def get_products_stats_by_category(self) -> list[ProductStatsByCategory]:
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}, "avg_price": {"$avg": "$price"}}},
            {"$sort": {"count": -1}}
        ]
        results = []
        async for doc in self.db.aggregate(pipeline):
            results.append(ProductStatsByCategory(
                category=doc["_id"],
                count=doc["count"],
                avg_price=round(doc["avg_price"], 2)
            ))
        return results

class CustomerCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("customers") 

    async def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        customer_dict = customer.dict()
        result = await self.db.insert_one(customer_dict)
        customer_dict["id"] = str(result.inserted_id)
        return CustomerResponse(**customer_dict)

    async def authenticate_customer(self, email: str, password: str) -> CustomerResponse:
        user = await self.db.find_one({"email": email})
        if user and password == user["password"]:
            user["id"] = str(user["_id"])
            return CustomerResponse(**user)
        raise HTTPException(status_code=401, detail="Invalid credentials")

class ReviewCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("reviews") 
    async def create_review(self, review: ReviewCreate) -> ReviewResponse:
        review_dict = review.dict()
        result = await self.db.insert_one(review_dict)
        review_dict["id"] = str(result.inserted_id)
        return ReviewResponse(**review_dict)

    async def get_reviews_by_product_id(self, product_id: str) -> list[ReviewResponse]:
        reviews = []
        async for review in self.db.find({"product_id": product_id}):
            review["id"] = str(review["_id"])
            reviews.append(ReviewResponse(**review))
        return reviews

class OrderCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("orders") 

    async def create_order(self, order: OrderCreate) -> OrderResponse:
        order_dict = order.dict()
        result = await self.db.insert_one(order_dict)
        order_dict["id"] = str(result.inserted_id)
        return OrderResponse(**order_dict)

    async def get_order_by_id(self, order_id: str) -> OrderResponse:
        order = await self.db.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order["id"] = str(order["_id"])
        return OrderResponse(**order)

    async def get_orders_by_customer_id(self, customer_id: str) -> list[OrderResponse]:
        orders = []
        async for order in self.db.find({"customer_id": customer_id}):
            order["id"] = str(order["_id"])
            orders.append(OrderResponse(**order))
        return orders

class PaymentCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("payments")  

    async def create_payment(self, payment: PaymentCreate) -> PaymentResponse:
        payment_dict = payment.dict()
        result = await self.db.insert_one(payment_dict)
        payment_dict["id"] = str(result.inserted_id)
        return PaymentResponse(**payment_dict)

    async def get_payment_by_order_id(self, order_id: str) -> PaymentResponse:
        payment = await self.db.find_one({"order_id": order_id})
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        payment["id"] = str(payment["_id"])
        return PaymentResponse(**payment)
