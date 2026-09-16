# Postman Collections

Lưu API collections/environments phục vụ manual/API regression.

## Ingestion safe-assurance suite

- `ingestion-safe-assurance/`: Postman Collection v3 chạy local, không gửi kết
  quả lên Postman Cloud.
- `ingestion-sit.template.postman_environment.json`: template không chứa secret.
- `../../tools/run_ingestion_postman.mjs`: runner tạo runtime environment quyền
  `0600`, inject secret từ process environment, capture/redact CLI report local
  và xóa runtime environment sau khi chạy.

Các mode:

```bash
node tools/run_ingestion_postman.mjs contract
node tools/run_ingestion_postman.mjs unauth
node tools/run_ingestion_postman.mjs unauth-inventory
node tools/run_ingestion_postman.mjs readonly
node tools/run_ingestion_postman.mjs safe
```

> Đây là tool riêng cho ingestion API cũ (`tools/run_ingestion_postman.mjs`), không liên quan tới
> workflow QA của dự án đang active — biến `INGESTION_SIT_*` không còn trong `.env.example` (đã xoá
> 2026-08-26 theo yêu cầu anh, không dùng tool ingestion cũ trên workflow này nữa); nếu cần chạy tool này, tự set
> biến bên dưới thủ công, không mong đợi `.env.example` điền sẵn.

`readonly` và `safe` yêu cầu `INGESTION_SIT_TENANT_ID` cùng một trong hai cách auth:

- `INGESTION_SIT_ACCESS_TOKEN`; hoặc
- `INGESTION_SIT_CLIENT_SECRET`, `INGESTION_SIT_USERNAME`, `INGESTION_SIT_PASSWORD` để runner tự
  lấy password-grant token trong memory.

Không paste token vào collection, command line hoặc file được commit. Có thể
dùng `node --env-file=.env tools/run_ingestion_postman.mjs readonly` với file
`.env` gitignored và quyền `0600`. Suite hiện không chứa request làm thay đổi
dữ liệu.

CLI report được ghi dưới `testing-output/ingestion-api/<run_id>/raw/`; thư mục
`raw/` đã được gitignore. Collection v3/multi-protocol chỉ hỗ trợ CLI reporter
khi chạy local không đăng nhập; runner không dùng Cloud reporting.

## Detailed request report

Sinh Newman-style HTML từ evidence đã redact:

```bash
node tools/generate_ingestion_api_detailed_report.mjs
```

Report hiển thị từng method/API, path/query/header đã truyền, request body,
expected, actual status/response metadata và từng assertion PASS/FAIL. Output
mặc định:
`Outputs/cross-sprint/ingestion-api-postman-detailed-2026-07-19.html`.
