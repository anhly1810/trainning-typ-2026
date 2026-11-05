## TUẦN 5: CACHING & REDIS
# 1. Tìm hiểu Caching
- Caching là kỹ thuật lưu trữ bản sao dữ liệu ở 1 lớp lưu trữ tạm thời có tốc độ truy xuất cực nhanh (thường là RAM thay vì ổ cứng HDD/SSD).
- Mục đích: Khi có yêu cầu lấy dữ liệu, hệ thống sẽ ưu tiên đọc từ Cache thay vì phải truy vấn Database gốc. Việc này giúp giảm độ trễ, tăng tốc độ phản hồi và giảm tải áp lực cho Database.
- Application-level cache vs Distributed cache:
  + Application-level Cache (Local Cache): Dữ liệu được lưu trực tiếp trên RAM của chính máy chủ đang chạy ứng dụng (App Server). Truy xuất cực kỳ nhanh (không qua mạng), nhưng có nhược điểm là không đồng bộ. Nếu hệ thống có 3 App Server, mỗi server sẽ giữ một bản cache riêng, dễ dẫn đến sai lệch dữ liệu.
  + Distributed Cache (Cache phân tán): Cấu trúc một hoặc nhiều server Cache độc lập (như Redis, Memcached) đứng tách biệt với App Server. Các App Server đều gọi qua mạng để lấy cache từ đây. Dù chậm hơn Local Cache một chút do độ trễ mạng, nhưng đảm bảo dữ liệu đồng nhất trên toàn hệ thống và dễ dàng mở rộng.
- Khi nào nên cache, khi nào KHÔNG nên cache?
  + Nên dùng: Dữ liệu được đọc nhiều hơn ghi, dữ liệu ít thay đổi hoặc kết quả của các phép tính toán phức tạp tốn thời gian.
  + Không nên dùng: Dữ liệu thay đổi liên tục theo thời gian thực (giá chứng khoán tính bằng giây), dữ liệu cá nhân hóa cao ít được truy cập lại, hoặc các hệ thống ghi nhiều hơn đọc

# 2. Chiến lược Caching
- Cache-aside: ứng dụng đóng vai trò chủ đạo. Khi cần dữ liệu, ứng dụng sẽ hỏi Cache trước.
  + Nếu có dữ liệu (cache hit): Lấy và trả về ngay.
  + Nếu ko có (cache miss): Ứng dụng gọi xuống DB để lấy dữ liệu -> trả về cho client -> đồng thời lưu dữ liệu đó vào cache để dùng cho lần sau.
  + Khi nào dùng: Đây là chiến lược phổ biến nhất, linh hoạt, rất phù hợp cho các hệ thống đọc nhiều. Nếu Cache sập, ứng dụng vẫn lấy được dữ liệu từ DB (dù chậm hơn).
- Write-through: Khi ứng dụng cần ghi dữ liệu, nó sẽ ghi vào Cache, sau đó hệ thống tự động ghi đồng bộ ngay lập tức vào DB.
  + Khi nào dùng: Khi yêu cầu tính nhất quán (Consistency) tuyệt đối giữa Cache và DB. Tuy nhiên, tốc độ ghi sẽ chậm hơn vì phải đợi hoàn thành ở cả 2 nơi.
# 3. Redis cơ bản
- Redis (Remote Dictionary Server) là một hệ quản trị cơ sở dữ liệu lưu trữ trực tiếp trên bộ nhớ (In-memory Data Structure Store) theo mô hình Key-Value. Tốc độ đọc/ghi của nó có thể đạt hàng trăm nghìn request/giây.
- Kiểu dữ liệu:
  + String: Chứa chuỗi đơn giản, số, hoặc chuỗi JSON. Dùng nhiều nhất để cache object.
  + Hash: lưu trữ các đối tượng dưới dạng key-value
  + List: DS các chuỗi có ký tự
  + Set: Tập hợp các chuỗi ko có thứ tự và ko trùng lặp.
  + Sorted set: Giống set nhưng mỗi phần tử có gắn thêm điểm số để sắp xếp.
- Các lệnh cơ bản:
  + GET key: lấy gtri của key.
  + Set key value: Lưu giá trị
  + DEL key: xoá
  + EXPIRE key seconds: cài đặt thời gian tự huỷ
  + TTL key: Kiểm tra xem key còn sông đc bn giây
- Cài đặt bằng docker:
docker run -d --name redis-server -p 6379:6379 redis

# 4. Implement - Tích hợp Redis vào project
# 5. Các vấn đề thường gặp
- TTL (time-to-live): là thời gian sống của dữ liệu trong cache.
  Vấn đề: TTL quá dài sẽ làm người dùng thấy dữ liệu cũ (Stale data). Đặt quá ngắn sẽ làm mất tác dụng của cache vì phải gọi DB liên tục. Lập trình viên phải cân nhắc tùy vào loại dữ liệu (Tỷ giá tiền tệ TTL = 1 phút; Profile User TTL = 1 giờ).
- Cache Invalidation (Hủy Cache): Khi dữ liệu dướ DB bị cập nhật (VD người dùng đổi tên), dữ liệu trong cache chưa hết hạn, TTL sẽ trở thành dẽ liệu sai. Vì vậy bất cứ khi nào gọi API Update/Delete thay đổi DB thành công, ứng dụng phải gọi lệnh DEL key để xóa chủ động xóa key đó trong Redis. Khi người dùng gọi GET, ứng dụng sẽ bị Cache Miss và tự động kéo dữ liệu mới nhất từ DB lên tạo lại Cache.
- Cache Avalanche (Bão tuyết / Sạt lở Cache): Có hàng chục ngàn key được lưu vào cache cùng một thời điểm và có cùng chung một khoảng thời gian TTL (ví dụ 1 tiếng). Đúng 1 tiếng sau, toàn bộ ngàn key đó biến mất cùng một lúc. Lúc này hàng ngàn request từ user lao tới không thấy cache sẽ đánh thẳng xuống DB, làm sập DB ngay lập tức.
  -> Thêm yếu tố ngẫu nhiên (Jitter) vào TTL. Ví dụ thay vì set cố định 3600 giây, hãy set: 3600 + Random(0 -> 300). Như vậy các key sẽ rụng lác đác, không tạo áp lực sốc cho DB.
- Cache Penetration (Xuyên thấu Cache): Hacker cố tình query liên tục vào một ID không bao giờ tồn tại (ví dụ: GET /users/-999). Vì DB không có ID này, nên bước "Lưu vào cache" bị bỏ qua. Các request tiếp theo với ID -999 lại xuyên qua Cache và đánh thẳng vào DB, gây quá tải.
  -> Nếu query DB không có (null), hãy lấy chính giá trị null (hoặc mảng rỗng) đó lưu vào Redis với TTL ngắn (khoảng 30 giây). Các request tiếp theo sẽ hit cache và nhận về chuỗi rỗng mà không chạm tới DB.

