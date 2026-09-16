<!--
Repo này là KHUNG dùng chung, không phải nơi chứa việc của một project cụ thể.
Trước khi mở PR, hỏi: thay đổi này có đúng cho MỌI project dùng khung không?
Nếu nó chỉ đúng cho một project → nó thuộc về Projects/<tên>/ trong bản clone của đội đó.
-->

## Thay đổi gì

<!-- Một đoạn ngắn. Nói điều gì đổi, không kể quá trình. -->

## Vì sao

<!-- Vấn đề có thật nào dẫn tới thay đổi này. Nếu là bài học rút ra từ một sự cố,
     ghi rõ sự cố đó — phần "vì sao" là thứ giữ được giá trị lâu nhất. -->

## Loại thay đổi

- [ ] Skill (`.claude/skills/`, `.agents/skills/`) — nhớ sửa **cả hai** mirror
- [ ] Config / schema (`Config/QA-Agent/`)
- [ ] Governance (`governance/`) — **cần cổng G6**, xem `governance/HUMAN_APPROVAL_GATES.md`
- [ ] Tool (`tools/`)
- [ ] Hook (`.claude/hooks/`)
- [ ] Template / scaffold
- [ ] Tài liệu

## Tự kiểm trước khi xin review

- [ ] **Không** có tên thật: sản phẩm, công ty, người, khách hàng
- [ ] **Không** có host nội bộ, IP, mã ticket thật, ID trang wiki, tên máy
- [ ] **Không** có secret: token, mật khẩu, cookie phiên, file `.env`, `*.local.*`
- [ ] Ví dụ trong tài liệu dùng placeholder (`<project>`, `DEMO-123`, `qauser01`, `example.local`)
- [ ] Đã chạy `python tools/sanitize-check.py` ở máy — báo **SACH**
- [ ] Sửa skill thì đã sửa đồng bộ cả `.claude/skills/` lẫn `.agents/skills/`
- [ ] `Projects/` vẫn rỗng (chỉ còn `Projects/README.md`)

> CI sẽ chạy lại các mục trên. Nhưng máy quét chỉ bắt được thứ nó **biết cách tìm** —
> nó không hiểu ngữ nghĩa. Vẫn phải tự đọc lại diff bằng mắt trước khi bấm mở PR.

## Ảnh hưởng tới người đang dùng khung

<!-- Ai pull bản này về thì có phải làm gì thêm không? Có phá cái gì đang chạy không?
     Nếu có: viết rõ các bước họ cần làm. Nếu không: ghi "không cần làm gì". -->
