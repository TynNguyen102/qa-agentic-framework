# Browser & Device Compatibility — Common Testcase Checklist

## Meta
- prefix: `CHK-BRW`
- coverage_type: `state_preservation_refresh_back_forward_and_multi_tab`, `responsive_browser_device_locale_theme_and_zoom`, `accessibility_semantics_keyboard_focus_reflow_and_assistive_technology`
- applies_when: always applicable to any screen — select the sub-items relevant to this project's
  actual supported browser/device matrix (check the project's NFR/test plan; do not assume every
  browser below is in scope)
- status: DRAFT — see `INDEX.md`

---

## 1. Navigation (áp dụng gần như mọi màn)

- **CHK-BRW-001 · High** — Bấm nút Back của browser sau khi navigate từ List sang Detail → quay về List, **giữ nguyên trạng thái filter/sort/trang đã có trước đó** (không reset về mặc định, trừ khi thiết kế xác nhận ngược lại).
- **CHK-BRW-002 · Medium** — Bấm Back sau khi vừa submit form thành công → không tự động submit lại; form ở trạng thái rỗng hoặc view-mode.
- **CHK-BRW-003 · High** — F5 refresh trên trang List đang có filter active → theo đúng thiết kế (giữ nguyên nếu encode trong URL, hoặc reset có chủ đích) — không crash, không 404.
- **CHK-BRW-004 · Medium** — F5 refresh trên trang Detail → load lại đúng record đó, không 404 nếu record còn tồn tại.
- **CHK-BRW-005 · Medium** — Hard refresh (Ctrl+Shift+R, clear cache) → trang load lại từ server, dữ liệu mới nhất, không white screen.

## 2. Multi-tab

- **CHK-BRW-020 · Medium** — Mở List ở tab 1, Detail ở tab 2 cùng lúc → thao tác ở tab 2 rồi quay lại tab 1 refresh → dữ liệu tab 1 cập nhật đúng, không conflict session.
- **CHK-BRW-021 · High** — Logout ở tab 1 → thao tác tiếp ở tab 2 bị redirect login ở lần action tiếp theo, không tiếp tục dùng được session cũ.
- **CHK-BRW-022 · Low** — Ctrl+Click mở record trong tab mới → tab mới mở đúng trang, giữ nguyên session.

## 3. Keyboard & Accessibility

- **CHK-BRW-040 · Medium** — Tab key di chuyển qua các field trong form đúng thứ tự (top-left → phải → xuống), không bỏ sót, không kẹt.
- **CHK-BRW-041 · Medium** — Enter key submit form nếu đó là hành vi mặc định thiết kế; không submit nhầm nếu Enter chỉ để xuống dòng trong textarea.
- **CHK-BRW-042 · Low** — Escape đóng modal/popup; nếu đang có dữ liệu chưa lưu thì có confirm discard hoặc tự đóng theo đúng thiết kế.

## 4. Cross-browser / Responsive (chọn theo ma trận hỗ trợ thật của dự án)

- **CHK-BRW-060 · High** — Layout đúng trên trình duyệt chính thức được hỗ trợ (theo NFR/test plan của dự án — không tự giả định Chrome/Firefox/Safari/Edge nếu chưa xác nhận phạm vi).
- **CHK-BRW-061 · Medium** — Zoom 150%/75% → layout không vỡ, không cắt chữ, không overlap.
- **CHK-BRW-062 · Medium** — Độ phân giải nhỏ (nếu responsive/tablet trong phạm vi hỗ trợ) → menu/sidebar collapse đúng, không vỡ.

## 5. Phi chức năng

- **CHK-BRW-080 · Medium** — Thời gian load trang lần đầu (cold load) nằm trong ngưỡng NFR đã xác nhận của dự án — không tự đặt số nếu chưa có SLO.
- **CHK-BRW-081 · Low** — Sử dụng liên tục 15-20 phút (navigate/filter/mở detail nhiều lần) không có dấu hiệu memory leak rõ rệt (chậm dần bất thường).
