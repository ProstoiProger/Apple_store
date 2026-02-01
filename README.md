# Apple Store - E-commerce Web Application

A full-stack e-commerce web application for an Apple Store, built with FastAPI, MongoDB, and vanilla HTML/CSS/JavaScript.

## Features

- **Products**: Browse, add, edit, delete products. Bulk delete and stats by category
- **Authentication**: Sign up and login
- **Orders**: Place orders, view order history
- **Reviews**: Add and view product reviews
- **Payments**: Process payments for orders

## Tech Stack

- **Backend**: FastAPI, Motor (async MongoDB), Pydantic
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

```
endka/
├── app/
│   ├── main.py      # FastAPI routes
│   ├── crud.py      # Database operations
│   ├── db.py        # MongoDB connection
│   ├── schemas.py   # Pydantic models
│   └── models.py    # Data models
├── src/
│   ├── index.html   # Home page
│   ├── products.html
│   ├── product.html
│   ├── add-product.html
│   ├── edit-product.html
│   ├── auth.html
│   ├── orders.html
│   ├── checkout.html
│   ├── api.js       # API client
│   └── style.css
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Prerequisites

- Python 3.12+
- MongoDB (or Docker)
- Docker (optional, for containerized setup)

## Installation

1. Clone the repository and navigate to the project folder:
   ```bash
   cd endka
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file (optional):
   ```
   MONGO_URI=mongodb://localhost:27017
   ```

## Running the Project

### Option A: Docker (recommended)

Start MongoDB and FastAPI:
```bash
docker-compose up -d --build
```

### Option B: Local development

1. Start MongoDB (e.g. via Docker or local install):
   ```bash
   docker-compose up -d mongodb
   ```

2. Run the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Serve the frontend:
   ```bash
   cd src
   python -m http.server 5500
   ```
   Or run `serve-frontend.bat` from the project root.

## Access

- **Frontend**: http://127.0.0.1:5500
- **API Docs**: http://127.0.0.1:8000/docs
- **API Base**: http://127.0.0.1:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup/ | Create account |
| POST | /login/ | Login |
| GET | /products/ | List products |
| GET | /products/{id} | Get product |
| POST | /products/ | Create product |
| PUT | /products/{id} | Update product |
| PATCH | /products/{id} | Partial update |
| DELETE | /products/{id} | Delete product |
| POST | /products/bulk-delete | Bulk delete |
| GET | /products/stats/aggregation | Stats by category |
| POST | /reviews/ | Create review |
| GET | /products/{id}/reviews | Get reviews |
| POST | /orders/ | Create order |
| GET | /customers/{id}/orders | Get customer orders |
| POST | /payments/ | Create payment |
| GET | /payments/{order_id} | Get payment |

## Database

- **Database**: `apple_store`
- **Collections**: `products`, `customers`, `reviews`, `orders`, `payments`

## License

MIT
