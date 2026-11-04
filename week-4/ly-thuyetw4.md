Tuần 4: Message Queue 

1. Tìm hiểu Message Queue (MQ)
- Message Queue là một phần mềm trung gian giúp các dịch vụ (services) trong hệ thống giao tiếp với nhau bằng cách gửi và nhận tin nhắn
   một cách bất đồng bộ.
- Tại sao cần MQ? 
Giả sử hệ thống xử lý tính năng "User đặt hàng".
Nếu xử lý Đồng bộ (Sync): Gọi tuần tự API Lưu đơn hàng (1s) → Cập nhật kho (1s) → Gửi Email (2s) → Ghi Log (1s). Khách hàng phải chờ 5s.
Nếu server gửi Email bị sập, toàn bộ quy trình đặt hàng sẽ thất bại (fail).
Giải pháp với MQ (Bất đồng bộ - Async): API Lưu đơn hàng xong (1s) → Đẩy một thông báo "Có đơn hàng mới" vào Queue (0.1s)
→ Trả kết quả báo thành công ngay cho người dùng (tổng chỉ mất 1.1s). Các dịch vụ Cập nhật kho, Gửi Email sẽ tự động đến Queue lấy tin nhắn để xử lý ngầm sau đó.
- Khi nào dùng MQ? Khi có các tác vụ nặng, tốn thời gian, hoặc cần kết nối các dịch vụ độc lập mà không cần kết quả trả về ngay lập tức.
- Khi nào gọi trực tiếp (Sync)? Khi nghiệp vụ yêu cầu kết quả tức thì (ví dụ: API kiểm tra số dư tài khoản ngân hàng để thanh toán).

2. Các mô hình Message Queue
- Point-to-Point (Mô hình Queue - 1-1): Một tin nhắn được gửi vào hàng đợi sẽ chỉ được tiêu thụ (xử lý) bởi một Consumer duy nhất.
 Ứng dụng: Phân chia đều khối lượng công việc. Ví dụ có 100 video cần render, 5 server (consumers) sẽ lấy dần từng video trong queue để xử lý, không ai bị trùng của ai.
- Publish/Subscribe (Mô hình Topic - 1-Nhiều): Khi một tin nhắn được xuất bản (publish) vào Topic, tất cả các Consumer đang "đăng ký theo dõi" (subscribe) Topic đó đều sẽ nhận được một bản sao của tin nhắn.
 Ứng dụng: Phát sóng sự kiện. Ví dụ sự kiện "User đăng ký", cả service Gửi Email Chào mừng và service Thống kê Data đều cần nhận sự kiện này để làm việc song song.

3. Kiến trúc Message Queue 
- RabbitMQ là một hệ thống MQ chuẩn mực và thân thiện để bắt đầu. Dưới đây là các khái niệm chính:
- Producer: Ứng dụng/Service tạo và đẩy tin nhắn vào hệ thống.
- Consumer: Ứng dụng/Service chờ lấy tin nhắn từ hệ thống ra để xử lý.
- Queue (Hàng đợi): Nơi lưu trữ tin nhắn chờ được xử lý. Hoạt động theo nguyên tắc Vào trước - Ra trước (FIFO).
- Exchange (Bưu điện): Trong RabbitMQ, Producer không bao giờ gửi tin nhắn thẳng vào Queue. Nó gửi cho Exchange. Exchange đóng vai trò như trung tâm phân loại, đọc nhãn (routing key) trên tin nhắn để quyết định đẩy nó vào Queue nào.
(Kafka sẽ có kiến trúc hơi khác một chút, sử dụng khái niệm Topic và Partition thay vì Exchange và Queue).


4. Luồng hoạt động (Implement Flow)
- Use case: User đăng ký tài khoản thành công → Gửi email welcome.
  + Client gửi request HTTP POST /register.
  + API (Producer) lưu thông tin user mới vào Database.
  + API (Producer) đóng gói dữ liệu thành JSON (VD: {userId: 1, email: "abc@gmail.com"}) và đẩy vào RabbitMQ.
  + API lập tức trả về HTTP 200 OK cho Client. Client thấy thông báo đăng ký thành công ngay lập tức.
  + Cùng lúc đó ở phía sau, một Worker (Consumer) chuyên xử lý email đang lắng nghe Queue.
    Nó lấy tin nhắn JSON kia ra, gọi API của Gmail/SendGrid để gửi thư. (Quá trình này mất vài giây nhưng Client không bị kẹt lại để chờ).

5. Các vấn đề cốt lõi khi dùng MQ
Việc dùng MQ giải quyết được tốc độ nhưng lại sinh ra các bài toán hệ thống cần xử lý:
- Duplicate Message (Tin nhắn bị gửi trùng): Do độ trễ mạng, 1 tin nhắn có thể bị gửi 2 lần. Code xử lý của Consumer phải có tính Idempotency (Lũy đẳng). Nghĩa là thao tác chạy 1 lần hay 100 lần với cùng 1 thông tin thì kết quả cũng không đổi (Ví dụ: Trước khi gửi email, phải check DB xem đơn hàng này "đã gửi email" chưa, nếu rồi thì bỏ qua).
- Message Loss (Mất tin nhắn): Nếu Consumer đang xử lý nửa chừng thì sập nguồn, tin nhắn có mất không? Để tránh việc này, MQ dùng Acknowledge (ACK). Chỉ khi Consumer làm xong và gửi tín hiệu ACK lại cho MQ, MQ mới xóa tin nhắn. Nếu mất kết nối mà chưa có ACK, MQ sẽ giao tin nhắn đó cho Consumer khác.
- Dead Letter Queue (DLQ): Nếu tin nhắn bị lỗi logic (ví dụ format email sai), Consumer xử lý thất bại liên tục, MQ sẽ ném lại vào Queue liên tục tạo thành vòng lặp vô tận. Giải pháp là cấu hình DLQ: Lỗi quá 3 lần thì ném tin nhắn đó sang một "Bãi rác thông minh" (DLQ) để lập trình viên vào xem lại thủ công.
- Message Ordering (Thứ tự tin nhắn): Trong môi trường phân tán nhiều Consumer, tin nhắn vào trước có thể bị Consumer xử lý chậm và xong sau. Nếu nghiệp vụ yêu cầu thứ tự tuyệt đối (VD: Cập nhật thông tin trước, Xóa thông tin sau), việc thiết kế routing/partition cần tính toán cực kỳ cẩn thận
