# Tuần 2 - Book API (Django + Django REST Framework + MySQL)

Bài tập Tuần 2: xây dựng RESTful API quản lý sách (Book), có phân trang,
error response chuẩn, và kết nối MySQL thật qua Django ORM. Quan hệ
`Author` (1) - `Book` (N): một tác giả có nhiều sách (OneToMany /
ManyToOne qua `ForeignKey`).

## Công nghệ

- Python 3 + Django 6
- Django REST Framework (DRF)
- MySQL (qua PyMySQL, không cần build driver C)
- python-decouple để đọc cấu hình từ file `.env`

## Cấu trúc project

```
tuan2-book-api/
├── bookapi/            # Project settings (settings.py, urls.py)
├── books/              # App: models, serializers, views, pagination, exception handler
│   ├── models.py       # Author, Book (ForeignKey)
│   ├── serializers.py  # Validate price, published_year
│   ├── pagination.py   # {data, page, size, totalPages, totalElements}
│   ├── exceptions.py   # Chuẩn hóa error response {code, message, details}
│   ├── views.py        # ModelViewSet cho Author, Book
│   └── urls.py
├── requirements.txt
├── .env.example
└── manage.py
```

## Cài đặt & chạy

1. Tạo và kích hoạt virtual environment, cài dependency:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Tạo database MySQL:

```sql
CREATE DATABASE book_api_db CHARACTER SET utf8mb4;
```

3. Copy `.env.example` thành `.env` và điền thông tin kết nối MySQL:

```powershell
Copy-Item .env.example .env
```

4. Chạy migration và khởi động server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # (tuỳ chọn, để vào /admin)
python manage.py runserver
```

Server chạy tại `http://127.0.0.1:8000/`.

## API Endpoints

### Author

| Method | URL                 | Mô tả               |
|--------|---------------------|---------------------|
| GET    | /api/authors        | Danh sách, có phân trang |
| GET    | /api/authors/{id}   | Chi tiết 1 author   |
| POST   | /api/authors        | Tạo author          |
| PUT    | /api/authors/{id}   | Cập nhật author      |
| DELETE | /api/authors/{id}   | Xoá author           |

### Book

| Method | URL                        | Mô tả                                   |
|--------|----------------------------|------------------------------------------|
| GET    | /api/books?page=1&size=10  | Danh sách sách, có phân trang             |
| GET    | /api/books?search=harry    | Tìm theo title hoặc tên author            |
| GET    | /api/books/{id}            | Chi tiết 1 sách                           |
| POST   | /api/books                 | Tạo sách mới                              |
| PUT    | /api/books/{id}            | Cập nhật sách                             |
| DELETE | /api/books/{id}            | Xoá sách                                  |

### Ví dụ request / response

**POST /api/books**

```json
{
  "title": "Clean Code",
  "author": 1,
  "price": "120000.00",
  "published_year": 2008,
  "quantity": 15
}
```

**GET /api/books?page=1&size=10** → `200 OK`

```json
{
  "data": [
    {
      "id": 1,
      "title": "Clean Code",
      "author": 1,
      "author_name": "Robert C. Martin",
      "price": "120000.00",
      "published_year": 2008,
      "quantity": 15,
      "created_at": "2026-10-29T10:00:00Z",
      "updated_at": "2026-10-29T10:00:00Z"
    }
  ],
  "page": 1,
  "size": 10,
  "totalPages": 1,
  "totalElements": 1
}
```

**GET /api/books/999** (không tồn tại) → `404 Not Found`

```json
{
  "code": 404,
  "message": "Not found.",
  "details": null
}
```

**POST /api/books** thiếu field bắt buộc → `400 Bad Request`

```json
{
  "code": 400,
  "message": "Request failed",
  "details": {
    "title": ["This field is required."]
  }
}
```

## Test bằng Postman / cURL

Ví dụ cURL:

```powershell
curl http://127.0.0.1:8000/api/books/
curl -X POST http://127.0.0.1:8000/api/books/ -H "Content-Type: application/json" -d "{\"title\":\"Dune\",\"author\":1,\"price\":\"99000\",\"published_year\":1965,\"quantity\":10}"
```

Import file `postman_collection.json` vào Postman để có sẵn các request mẫu
(Author CRUD + Book CRUD + phân trang).
