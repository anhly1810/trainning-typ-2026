## Authentication & Authorization

# 1. KN
- Authentication (Xác thực): Quá trình hệ thống kiểm tra danh tính của người dùng.
- Authorization (Phân quyền): Quá trình kiểm tra xem người dùng đã xác thực có quyền truy cập vào tài nguyên cụ thể hay không.
# 2. Phân biệt cơ chế xác thực
1. Session-based (Xác thực có lưu trạng thái - Stateful)
- Client gửi username/password, server ktra DB, nếu đúng tạo 1 session lưu vào bộ nhớ hoặc DB của server.
  Server trả về 1 mã Session ID qua HTTP Cookie. Ở các request sau, trình duyệt tự động gửi Cookie chứa
  Session ID lên, từ đó Server sẽ biết user nào đang thao tác.
2. Token-based (Xác thực không lưu trạng thái - Stateless)
- Client gửi username/pass, server check DB, nếu đúng thì dùng secret key để ký và tạo 1 chuối mã (token)
  Server trả toàn token cho client, ko lưu gì ở DB. Các request sau client tự đính kèm token vào HTTP Header
  server chỉ cần dùng Secret key để giải mã và xác mình token đó có hợp lệ không.
3. Khi nào dùng cái nào?
- sd session cho ứng dụng web truyền thống.
- sd token cho các hệ thống RESTful API, Mobile App, Single Page App (React, Vue) và Microservices.
# 3. JWT (JSON Web Token)
1. KN: Là một tiêu chuẩn mở định nghĩa cách truyền tải thông tin an toàn giữa client và server dưới dạng
2. một đối tượng JSON. Dữ liệu này được xác thực và đáng tin cậy nhờ vào chữ ký điện tử.
3. Cấu trúc
- Header: Chứa thông tin về loại token và thuật toán dùng để ký
- Payload: Chứa dữ liệu nghiệp vụ (user ID, Role, thời gian hết hạn), Payload chỉ dc mã hoá định dạng Base64.
- Signature: dấu mộc điện tử, dc tạo = cách lấy Header + Payload + Secret Key rồi đem đi băm (hash), để đảm bảo
- token ko bị sửa đổi dọc đường.
4. Lợi ích của JWT: kích thước gọn nhẹ, truyền đi nhanh, giảm tải cho DB vì server tự xác minh đc role/id ngay trong Payload.
5. Hạn chế và rủi ro bảo mật: Vì server ko lưu JWT nên ko thể huỷ hoặc thay đổi thông tin của 1 JWT trc khi nó hết hạn.
  Nếu vô tình để lộ dữ liệu cá nhân vào Payload, ai cũng đọc đc, nếu server lộ Secret key, toàn bộ hệ thống có thể bị giả mạo.  
# 4. Password Hashing  
- Tại sao không lưu password dạng plain text? Nếu lưu dạng văn bản gốc, khi hệ thống bị tấn công (Data Breach), hacker sẽ chiếm
  được toàn bộ mật khẩu của người dùng, dẫn đến mất tài khoản và ảnh hưởng tới các dịch vụ khác nếu user dùng chung mật khẩu.
- Tại sao không dùng MD5/SHA? (brute force, rainbow table) Tốc độ quá nhanh: MD5/SHA sinh ra để kiểm tra tính toàn vẹn dữ liệu cực nhanh.
  Hacker có thể dùng sức mạnh máy tính để thử hàng tỷ mật khẩu mỗi giây (Brute force).
- Dùng bcrypt/argon2: salt, cost factor: Trước khi băm, thuật toán sẽ sinh ra một chuỗi ký tự ngẫu nhiên (Salt) và ghép vào mật khẩu gốc.
  Nhờ vậy, hai người dùng chung mật khẩu "123456" sẽ sinh ra hai mã hash hoàn toàn khác nhau, vô hiệu hóa hoàn toàn Rainbow table.
  Cost Factor (Work Factor): Cơ chế làm chậm cố ý. Lập trình viên có thể cấu hình để thuật toán tốn 0.5 - 1 giây cho một lần băm.
  Với user đăng nhập, 1 giây chờ là bình thường. Nhưng với hacker chạy Brute force 1 tỷ mật khẩu, chúng sẽ mất hàng chục năm.
