# 📚 Book Review Project

A Django REST Framework-based project for managing **Users, Books, and Reviews**.  
This project demonstrates **authentication, CRUD operations, ORM queries, pagination, and API documentation** using **Swagger (drf-spectacular)**.

---

## 🚀 Features
- **User Authentication** with JWT (`djangorestframework-simplejwt`)
- **Book Management** (CRUD with average rating & review counts)
- **Review System** (one review per user per book, prevents duplicates)
- **Custom API Responses**
- **Swagger API Docs** (`drf-spectacular`)
- **ORM Query Utilities** for analytical queries
- **Database Schema Diagram** included

---

## 🛠️ Tech Stack
- **Backend**: Django 4.2, Django REST Framework
- **Auth**: JWT (SimpleJWT)
- **Database**: PostgreSQL (recommended) or SQLite (default)
- **API Docs**: drf-spectacular
- **Deployment Ready**: Production practices included

---

## 📂 Project Structure
book_review_project/
│── users/ # User app (custom user model + auth)
│── books/ # Books app
│── reviews/ # Reviews app
│── queries/ # Reusable ORM queries
│── utils/ # Custom utilities (e.g., custom_response)
│── book_review_project/ # Project settings
│── manage.py
│── requirements.txt
│── README.md

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/book_review_project.git
cd book_review_project
2️⃣ Create Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Database Setup
Update book_review_project/settings.py with your PostgreSQL credentials
(or keep SQLite for quick testing).

Run migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
5️⃣ Create Superuser
bash
Copy code
python manage.py createsuperuser
6️⃣ Run Development Server
bash
Copy code
python manage.py runserver
📖 API Documentation
Swagger UI: http://127.0.0.1:8000/api/docs/

Schema (OpenAPI JSON): http://127.0.0.1:8000/api/schema/

🔑 Authentication
Register: POST /api/users/register/

Login (JWT): POST /api/users/login/

Refresh Token: POST /api/users/token/refresh/

Use the JWT access token in headers:

makefile
Copy code
Authorization: Bearer <your_token>
📚 Endpoints
Users
POST /api/users/register/ → Register new user

POST /api/users/login/ → Login & get JWT

GET /api/users/most-active/ → Most active reviewer

GET /api/users/active-users/ → Users with >5 reviews

Books
GET /api/books/ → List books with avg rating + review count

POST /api/books/ → Add new book (admin only)

GET /api/books/top-rated/ → Top 3 rated books

Reviews
GET /api/reviews/ → List all reviews (paginated)

POST /api/reviews/ → Add new review

GET /api/reviews/book/<book_id>/ → Reviews for a given book

📝 Example ORM Queries
Located in queries/review_queries.py

1. Top 3 Books
python
Copy code
from queries.review_queries import top_books
print(top_books())
2. Users with >5 Reviews
python
Copy code
from queries.review_queries import active_users
print(active_users())
3. Most Active User
python
Copy code
from queries.review_queries import most_active_user
print(most_active_user())
4. Reviews for Book
python
Copy code
from queries.review_queries import reviews_for_book
print(reviews_for_book(book_id=1))
🗂️ Database Schema
Entity Relationship Diagram (ERD)

(See schema.png in repo — exported from dbdiagram.io )

Users → can post multiple reviews

Books → can have multiple reviews

Reviews → link Users ↔ Books with rating & comment