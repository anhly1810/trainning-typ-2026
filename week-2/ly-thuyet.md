# Tuần 2: Framework, RESTful API và ORM — Lý thuyết
## Phần 1: Framework & RESTful API

### 1. Lựa chọn Framework
Dùng **Django** trên nền Python. Django cung cấp sẵn ORM, hệ thống migration và admin site.
Khi kết hợp với **Django REST Framework**, gọi tắt là DRF, việc xây RESTful API rất nhanh và
theo chuẩn, nhờ có sẵn serializer, viewset, router, pagination và exception handling.

### 2. Cấu trúc project

Khởi tạo bằng `django-admin startproject bookapi .` rồi `python manage.py startapp books`.

- `bookapi/` — project, chứa `settings.py` để cấu hình DB, app, DRF và `urls.py` là route gốc
- `books/` — app chứa toàn bộ logic nghiệp vụ:
  - `models.py` — định nghĩa Entity, tương đương "models" trong sơ đồ MVC
  - `serializers.py` — convert giữa Model ↔ JSON, validate dữ liệu, tương đương phần
    "controller" xử lý input
  - `views.py` — xử lý request, gọi ORM, trả response, đóng vai trò routes + controllers
  - `urls.py` — mapping URL → ViewSet, tức phần routes
  - `migrations/` — lịch sử thay đổi schema database
- File cấu hình: `.env` chứa `SECRET_KEY` và thông tin kết nối DB, không commit lên GitHub —
  tương tự `application.properties` của Spring Boot. Đọc bằng thư viện `python-decouple`.

### 3. Xây dựng RESTful API

- **HTTP Methods** dùng đúng ngữ nghĩa: `GET` để đọc, `POST` để tạo, `PUT` để cập nhật toàn bộ,
  `DELETE` để xoá. `ModelViewSet` của Django REST Framework tự map các method này tới
  `list/retrieve/create/update/destroy`.
- **Mapping URL → hàm xử lý**: dùng `DefaultRouter` của DRF, tự sinh route kiểu
  `/api/books/`, `/api/books/{id}/` từ 1 ViewSet, không cần khai báo tay từng route.
- **Xử lý Request**:
  - Path Variable: `/api/books/{id}/` → DRF tự inject vào `self.kwargs['pk']`
  - Query Param: `/api/books/?page=1&size=10&search=clean` → đọc qua
    `request.query_params`
  - Request Body: JSON → DRF tự parse vào `request.data`, serializer validate
- **Xử lý Response**: luôn trả JSON qua `JSONRenderer`, status code đúng ngữ nghĩa:
  - `200 OK` — thành công với GET, PUT, DELETE
  - `201 Created` — tạo mới thành công với POST
  - `400 Bad Request` — dữ liệu client gửi sai, lỗi validate
  - `404 Not Found` — không tìm thấy resource
  - `500 Internal Server Error` — lỗi phía server
- **Error Handling**: viết custom `EXCEPTION_HANDLER` cho DRF tại `books/exceptions.py` để
  mọi lỗi như validate, not found, server error... đều trả về cùng 1 cấu trúc thống nhất:

```json
{ "code": 400, "message": "Request failed", "details": { "title": ["This field is required."] } }
```

  Phân biệt rõ 4xx là lỗi do client — thiếu field, sai kiểu dữ liệu, không tồn tại resource —
  và 5xx là lỗi do server — bug, mất kết nối DB... Cách làm: bắt riêng `DRF APIException`
  → trả 4xx có message rõ ràng, còn exception không xác định → trả 500 kèm nội dung lỗi.

### 4. Pagination trong API

Áp dụng công thức phân trang tuần 1: `LIMIT size OFFSET (page-1)*size` và
`totalPages = ceil(totalElements / size)`. Công thức được đưa vào response thông qua custom
`PageNumberPagination` tại `books/pagination.py`, trả đúng format:

```json
{ "data": [...], "page": 1, "size": 10, "totalPages": 3, "totalElements": 25 }
```

Dùng được bằng `GET /api/books/?page=1&size=10`.

---

## Phần 2: Tích hợp Database — ORM

### 1. ORM là gì? Lợi ích?

**ORM — Object-Relational Mapping** là kỹ thuật ánh xạ giữa bảng trong database quan hệ
và object/class trong code — một dòng trong bảng `books` tương ứng 1 object `Book`,
một cột tương ứng 1 attribute.

**Lợi ích:**
- Không phải viết SQL tay cho các thao tác CRUD cơ bản → code ngắn, nhanh hơn
- Thao tác với object/class quen thuộc trong ngôn ngữ lập trình thay vì chuỗi SQL
- Tự quản lý migration: thay đổi schema theo lịch sử, có thể rollback
- Hạn chế SQL Injection vì query được build qua API, tham số tự động escape
- Dễ đổi database engine giữa SQLite, MySQL, PostgreSQL mà gần như không đổi code
- Hỗ trợ sẵn quan hệ giữa các bảng như OneToMany, ManyToOne, ManyToMany qua khai báo field

**Đánh đổi:** SQL sinh ra đôi khi không tối ưu bằng SQL viết tay, cần hiểu cơ chế ORM để
tránh vấn đề N+1 query.

### 2. Sử dụng ORM trong Django — Django ORM

- Định nghĩa Entity bằng class kế thừa `models.Model`, mỗi field là 1 cột:

--python
class Author(models.Model):
    name = models.CharField(max_length=150)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    price = models.DecimalField(max_digits=10, decimal_places=2)


- `ForeignKey` trên `Book` trỏ về `Author` tạo quan hệ **ManyToOne**: nhiều Book → 1 Author.
  Ngược lại, `author.books.all()` chính là quan hệ **OneToMany**: 1 Author → nhiều Book.
- Các thao tác ORM dùng trong project:
  - `Book.objects.all()` / `.filter(...)` — SELECT, tương ứng LIMIT/OFFSET khi phân trang
  - `Book.objects.select_related("author")` — JOIN sẵn với bảng Author, tránh N+1 query
  - `Book.objects.create(...)` — INSERT
  - `instance.save()` — UPDATE
  - `instance.delete()` — DELETE
- Migration: `python manage.py makemigrations` sinh file migration mô tả thay đổi schema,
  rồi `python manage.py migrate` áp dụng vào database thật — ở đây là MySQL 8.0 chạy local.
