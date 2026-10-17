# PHẦN 1: Database (CSDL quan hệ)
## II. SQL CƠ BẢN
1. DDL
CREATE TABLE:
CREATE DATABASE library;
USE library;

ALTER TABLE:
ALTER TABLE books
ADD type VARCHAR(10);       //add thêm 1 cột ‘type’

2. DML (lệnh)
- CREATE TABLE:
CREATE TABLE books (
	id primary key,
    name VARCHAR(100),
    author VARCHAR(100),
    year INT
);

- INSERT:
INSERT INTO books
VALUES 
(1, 'Conan', 'AB', 1994), 
(2, 'Doraemon', 'BC', 1001);

- SELECT (XEM DỮ LIỆU)
select * from books  //XEM ALL DỮ LIỆU CỦA BOOKS 

select name, year        //chỉ xem cột name, year
from books

- UPDATE (SỬA DỮ LIỆU)
UPDATE books
SET name = 'Doraemon New',
    author = 'Fujiko'
WHERE id = 1;

- DELETE 
delete from books
where id = 2;                    //xoá dòng có id = 2

delete from books;        //xoá các dòng trong bảng (bảng vẫn còn nhưng empty)


3. Query

- WHERE (LỌC DỮ LIỆU THEO ĐK)
select * from books

where name = ‘Doraemon’;     
where year > 2000;             
where year <> 2000;                            //khác 
where year > 1990 and id < 5              //và  (cả 2 đk)
where id in (1, 2, 3)                               //nằm trong danh sách đã nêu
where year between 1000 and 2000    //nằm trong khoảng (tính cả 2 đầu)
where name like ‘D’                              //tìm theo mẫu kí tự


- ORDER BY (SX DỮ LIỆU)
	ASC: tăng dần
	DESC: giảm dần
	select * from books
	order by year asc, name desc;
- GROUP BY 
SELECT type , COUNT(*) AS total FROM books
GROUP BY type;               //COUNT(*): đếm trong bảng mỗi type có bn cái
(vd này có 2 type A, 1 type B)
SELECT type, SUM(price) AS total      
FROM books
GROUP BY type;            //SUM(  ): tính tổng price từ ‘type’ của bảng books cho vào cột total
  
	AVG(  )
	MIN(  )
	MAX(  )

- HAVING (LỌC CÁC NHÓM)
SELECT type, COUNT(*) AS total
FROM books
GROUP BY type
HAVING COUNT(*) >= 2;         //dem so type >=2 trong bang books

- JOIN (KẾT HỢP DỮ LIỆU TỪ NHIỀU BẢNG)
CROSS JOIN: ghép mọi dòng bên trái với mọi dòng bên phải (không cần điều kiện)
INNER JOIN: chỉ lấy dòng khớp ở cả 2 dòng
LEFT JOIN: tất cả bên trái + phần khớp bên phải
RIGHT JOIN: tất cả bên phải + phần khớp bên trái
FULL JOIN: giữ tất cả 2 bên (dùng UNION)
SELF JOIN: bảng nối với chính nó

4. Aggregate functions (hàm tổng hợp) nhận nhiều dòng và trả về một giá trị duy nhất

## III. INDEX
1. Index (chỉ mục) là một cấu trúc dữ liệu phụ mà database tạo ra cho một hoặc nhiều cột, giúp tìm dòng nhanh hơn mà không phải đọc cả bảng.
2. Khi nào nên / ko nên
NÊN đánh index khi cột:
- thường xuyên nằm trong WHERE
- cột dùng JOIN, ORDER BY, GROUP BY
- cột có nhiều giá trị khác nhau
KHÔNG NÊN khi:
- bảng nhỏ, ít gtri khác nhau.
- Bảng ghi dữ liệu liên tục (vì mỗi lần ghi SQL phải cập nhật index nên lâu)
3. Thực hành:

## IV. PHÂN TRANG
1. Phân trang khi bảng có 1 triệu dòng mà chạy SELECT * FROM books thì database phải đọc và gửi 1 tr lần -> chậm, khi này ta chia dữ liệu thành từng trang nhỏ (phân trang), mỗi lần lấy 1 trang -> nhanh.
2. Offset-based pagination: LIMIT + OFFSET (lấy N dòng sau khi bỏ qua M dòng)

SELECT id, name FROM books
ORDER BY id
LIMIT 3 OFFSET 0;    -- trang 1       --lấy 3 dòng, bỏ qua 0 dòng theo thứ tự id, gồm cột id và name

- có cách viết rút gọn: LIMIT 3 OFFSET 3 = LIMIT 3, 3
- ƯU ĐIỂM:
  + Nhảy dc tới trang bất kỳ: dùng công thức OFFSET = (số trang -1) * số dòng
    VD: muốn tới trang 50 (mỗi trang 3 dòng): SELECT ì, name from books ORDER BY id LIMIT 3 OFFSET 147;
- NHƯỢC ĐIỂM:
  + càng về sau càng chậm
  + dễ bị lệch khi thay đổi dữ liệu
3. Cursor-based pagination: WHERE id > last_id LIMIT N (nhớ dòng cuối cùng đã xem và lấy các dòng sau đó)
SELECT id, name FROM books
ORDER BY id
LIMIT 3;     --dòng cuối id=3, đây là cursor
SELECT id, name FROM books
WHERE id > 3
ORDER BY id
LIMIT 3;     --đọc tiếp 3 dòng tiếp theo khi id > 3
SELECT id, name FROM books
WHERE id > 6
ORDER BY id
LIMIT 3;     --đọc tiếp 3 dòng tiếp theo khi id > 6

- ƯU ĐIỂM:
  + luôn nhanh dù ở trang nào, nhảy thẳng tới trang cần tìm, ko phải đọc ròi vứt dòng nào.
  + ko bị lệch khi thay đổi dữ liệu.
- NHƯỢC ĐIỂM:
  + không nhảy tới trang bất kỳ, phải đi tuần tự
##  V. Locking trong Database
1. Tại sao cần lock?
- Khi nhiều người cùng thao tác trên cùng một dòng dữ liệu tại cùng một lúc, kết quả có thể sai, khi này ts cần lock.
2. Optimistic Locking (Không khóa, chỉ kiểm tra lúc ghi xem có ai sửa trước không)
- Không dùng khóa của database mà thêm một cột version vào bảng, mỗi lần sửa thì version + 1.
    UPDATE products
    SET stock = 9, version = version + 1
    WHERE id = 1 AND version = 0;     -- 0 là version đã đọc lúc đầu
3. Pessimistic Locking (Khóa dòng ngay từ lúc đọc, người khác phải chờ)
- Dùng SELECT ... FOR UPDATE để khóa các dòng được chọn cho đến khi commit.
    START TRANSACTION;
    SELECT stock FROM products WHERE id = 1 FOR UPDATE;   -- khóa dòng id = 1
    UPDATE products SET stock = stock - 1 WHERE id = 1;
    COMMIT;                                                -- nhả khóa

  + FOR UPDATE: khoá ghi, người khác không được đọc để sửa hay ghi
  + FOR SHARE: khóa đọc, nhiều người cùng đọc được, nhưng không ai ghi được
  + FOR UPDTE NOWAIT: Nếu dòng đang bị khóa thì báo lỗi ngay, không chờ
  + FOR UPDTAE SKIP LOKED: Bỏ qua các dòng đang bị khóa

4. So sánh: khi nào dùng cái nào?
- Pessimistic: khi nhiều ng cùng tranh 1 dòng và sai là hỏng.
- Optimistic: Ít khi tranh nhau.
5. Demo: chạy 2 transaction đồng thời để thấy lock hoạt động
  ## VI. Transaction
- Transaction là gì? là một nhóm câu lệnh SQL được xử lý như một khối duy nhất: hoặc thành công hết, hoặc hủy hết.
- Khi nào cần gom nhiều thao tác vào 1 transaction? Khi có từ 2 thao tác trở lên mà thao tác này chỉ đúng nếu thao tác kia cũng xong
- COMMIT, ROLLBACK   --xem VD trong queries.sql
Ví dụ: chuyển tiền — trừ tài khoản A + cộng tài khoản B phải thành công cùng nhau, fail thì rollback cả hai
