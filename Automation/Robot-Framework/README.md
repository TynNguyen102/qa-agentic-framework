# Robot-Framework

Thư mục này **để trống có chủ đích**.

Bộ test Robot-Framework là **tài sản của từng project**, không phải của khung. Khung chỉ quy định
chỗ đặt và quy ước, không mang theo test case của project khác.

Khi dùng cho một project mới:
1. Dựng `KeywordLibraries/`, `Libs/`, `Resources/`, `Tests/` theo quy ước của đội.
2. Giữ biến môi trường và thông tin đăng nhập ở file `*.local.*` (đã có trong `.gitignore`).
3. Nếu bộ test đủ lớn, cân nhắc tách sang repo automation riêng thay vì để trong control plane.
