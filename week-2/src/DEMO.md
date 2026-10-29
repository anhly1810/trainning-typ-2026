# Demo — Book API

Project đã chạy thật, kết nối MySQL 8.0 local (`book_api_db`), test bằng
PowerShell `Invoke-RestMethod` (tương đương cURL/Postman). Dưới đây là log
request/response thật đã chạy trong lúc build project.

File Postman collection để tự test lại: [`postman_collection.json`](./postman_collection.json).

## 1. Tạo Author (POST /api/authors/)

Request:

```json
{ "name": "Robert C. Martin", "bio": "Software craftsman" }
```

Response `201 Created`:

```json
{
  "id": 1,
  "name": "Robert C. Martin",
  "bio": "Software craftsman",
  "created_at": "2026-10-29T15:43:08.440454Z"
}
```

## 2. Tạo Book (POST /api/books/) — quan hệ ManyToOne tới Author

Request:

```json
{ "title": "Clean Code", "author": 1, "price": "120000.00", "published_year": 2008, "quantity": 15 }
```

Response `201 Created`:

```json
{
  "id": 1,
  "title": "Clean Code",
  "author": 1,
  "author_name": "Robert C. Martin",
  "price": "120000.00",
  "published_year": 2008,
  "quantity": 15,
  "created_at": "2026-10-29T15:43:16.863444Z",
  "updated_at": "2026-10-29T15:43:16.863468Z"
}
```

## 3. Phân trang (GET /api/books/?page=1&size=5)

Sau khi tạo 12 sách, gọi với `size=5`:

```json
{
  "page": 1,
  "size": 5,
  "totalPages": 3,
  "totalElements": 12,
  "data": [ "... 5 books ..." ]
}
```

→ `totalPages = ceil(12 / 5) = 3`, đúng công thức phân trang, dữ liệu lấy thật từ MySQL.

## 4. Lỗi 404 — GET /api/books/999/ (không tồn tại)

```json
{ "code": 404, "message": "No Book matches the given query.", "details": null }
```

## 5. Lỗi 400 — POST /api/books/ thiếu field + giá trị sai

Request: `{ "author": 1, "price": "-5", "published_year": 1800 }` (thiếu `title`, `price` âm)

```json
{
  "code": 400,
  "message": "Request failed",
  "details": {
    "title": ["This field is required."],
    "price": ["price must be >= 0"]
  }
}
```

→ Chuẩn hoá đúng format `{code, message, details}`, phân biệt rõ lỗi client (4xx).

## 6. Update (PUT /api/books/1/)

Request: `{ "title": "Clean Code (2nd Edition)", "author": 1, "price": "150000.00", "published_year": 2008, "quantity": 20 }`

Response `200 OK` — trả về book đã cập nhật với `updated_at` mới.

## 7. Search (GET /api/books/?search=clean)

Trả về danh sách sách có `title` hoặc tên tác giả chứa "clean" (dùng DRF `SearchFilter`).

## 8. Delete (DELETE /api/books/2/)

Response `200 OK`:

```json
{ "code": 200, "message": "Book deleted", "details": null }
```

---

Tổng cộng 10 API CRUD hoạt động (5 cho Author, 5 cho Book), đều có phân trang (list) và
error response chuẩn, kết nối MySQL thật qua Django ORM — vượt yêu cầu tối thiểu 5 API.
