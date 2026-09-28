# Phiếu Phản Ánh — K4 Level 3A, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng trả lời mẫu bên dưới mỗi câu bằng nội dung của bạn.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Thái Hữu Tuấn  Mã học viên: L3A202602465

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Một tình huống cụ thể là lúc deploy phiên bản mới nhưng quên cấu hình
> `AGENT_API_KEY` trên platform. Nếu khóa có mặc định là `"changeme"`, service
> vẫn báo khởi động thành công và endpoint `/ask` có thể bị người khác gọi bằng
> khóa dễ đoán, làm phát sinh chi phí. Khi trường này bắt buộc, process dừng ngay
> ở bước khởi động và log chỉ thẳng biến còn thiếu, nên tôi sửa cấu hình trước
> khi service nhận traffic.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Dòng log tôi thu được khi gọi `/ask`:
>
> ```json
> {"event":"ask_completed","level":"info","timestamp":"2026-09-28T13:08:01.882649+00:00","user_id":"exercise-user","tokens_in":2,"tokens_out":34,"cost_usd":2.07e-05}
> ```
>
> Với log này tôi có thể lọc và đếm số lần `ask_completed` theo `user_id` để
> điều tra người dùng nào gọi nhiều, đồng thời tổng hợp `cost_usd` hoặc số token
> để tạo dashboard và cảnh báo chi phí. Một câu `print("đã trả lời xong")` không
> có cấu trúc trường, thời gian, user hay chi phí để máy truy vấn chính xác.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 1.73 GB |
| Multi-stage | 271 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Tôi build bản một stage từ Dockerfile ban đầu dùng `python:3.11` và đo được
> 1.73 GB; bản hiện tại dùng `python:3.11-slim` và multi-stage là 271 MB. Phần
> chênh lệch chủ yếu đến từ base image Python đầy đủ chứa nhiều công cụ và thư
> viện hệ thống không cần ở runtime. Multi-stage chỉ mang dependency đã cài từ
> builder sang runtime slim, không mang toàn bộ môi trường build và các file
> không cần thiết vào image chạy thật.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Sau khi tôi thay đổi một dòng trong `app/main.py` rồi build lại, các layer
> `WORKDIR`, `COPY requirements.txt`, `pip install` và copy dependency từ
> builder đều hiện `CACHED`. Layer `COPY app ./app` và các layer đứng sau nó
> phải chạy lại. Nếu đặt `COPY . .` trước `RUN pip install`, mọi thay đổi source
> đều làm checksum của layer copy đổi, khiến Docker phải cài lại toàn bộ
> dependency dù `requirements.txt` không thay đổi.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Nếu code Python có lỗ hổng thực thi lệnh, kẻ tấn công trước hết chạy lệnh với
> quyền của process trong container. Khi container chạy root, kết hợp thêm cấu
> hình nguy hiểm như privileged mode, mount Docker socket hoặc một lỗ hổng thoát
> container, quyền root đó có thể bị dùng để sửa file hoặc chiếm quyền cao trên
> host. Lệnh `USER appuser` cắt chuỗi ở bước đầu: mã bị khai thác chỉ có quyền
> của user thường trong container. Nó không thay thế việc vá lỗ hổng, nhưng làm
> giảm đáng kể phạm vi thiệt hại nếu ứng dụng bị chiếm quyền.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Người dùng có thể gửi tối đa 20 request trong 2 giây: gửi 10 request ngay
> trước thời điểm reset, ví dụ 10:00:59.x, rồi gửi thêm 10 request ngay sau đó,
> vào 10:01:00.x. Bộ đếm theo phút coi đây là hai cửa sổ khác nhau. Sliding
> window 60 giây vẫn nhìn thấy cả 20 request trong 60 giây gần nhất nên chặn
> lượt thứ 11.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit giới hạn tốc độ request trong cửa sổ ngắn, còn cost guard giới hạn
> tổng tiền đã dùng trong cả tháng. Một user chỉ gọi một request/phút nên rate
> limit cho qua, nhưng nếu đã gần hết ngân sách và request mới có chi phí ước
> tính vượt phần còn lại thì cost guard phải trả 402. Ngược lại, một user còn
> nguyên ngân sách nhưng gửi 11 request rất rẻ gần như cùng lúc sẽ bị rate limit
> trả 429 dù cost guard vẫn cho phép về mặt tiền.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu Redis mất kết nối, endpoint gộp bắt đầu trả lỗi cho cả ba container. Vì
> orchestrator dùng endpoint đó như liveness probe, nó kết luận cả ba process đã
> hỏng và lần lượt restart chúng. Redis vẫn chưa phục hồi nên các container mới
> lại fail probe và đi vào restart loop, làm cụm mất toàn bộ capacity dù code
> web vẫn sống. Khi Redis trở lại, container còn phải khởi động và qua probe lại
> mới nhận traffic. Tách `/health` và `/ready` tránh việc này: process vẫn sống,
> còn load balancer chỉ tạm ngừng gửi request cho instance chưa ready.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Khi gọi cùng `X-User-Id`, tôi quan sát `history_length` lần lượt là 0, 2 và 4;
> mỗi lượt trước thêm một message `user` và một message `assistant` vào Redis.
> Hai `ConversationStore` khác nhau vẫn đọc được cùng dữ liệu. Nếu dùng dict
> Python, mỗi container có một bản riêng nên request qua load balancer có thể
> thấy các số nhảy không đều như 0, 0, 2 hoặc quay về 0 khi sang container khác;
> restart container còn làm mất hẳn lịch sử của instance đó.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Lần deploy đầu trên Railway hoàn tất bước build nhưng khi gọi URL, cả
> `/health` và `/ready` đều trả `502 Application failed to respond`. Tôi xác
> nhận lỗi bằng `curl`, sau đó kiểm tra Source, Variables và Deployment Logs
> trên Railway. Service lúc đó chưa có các biến production và chưa chạy phiên
> bản mới nhất của cấu hình Docker. Tôi thêm `AGENT_API_KEY`, tham chiếu
> `REDIS_URL` từ Redis service, rồi push phiên bản đã đọc đúng `$PORT` để Railway
> redeploy. Sau lần deploy mới, `/health` trả 200, `/ready` trả 200 với
> `redis:true`, `/ask` không key trả 401 và có key hợp lệ trả 200.
