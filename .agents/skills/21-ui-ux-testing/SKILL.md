---
name: 21-ui-ux-testing
description: Test UI behavior and UX conformance against approved designs, journeys, component rules, responsive states, validation, permissions, and locale expectations. Use for evidence-based UI and interaction review.
---

# UI and UX Testing

Compare behavior with approved requirements, design sources, and component standards. Do not report personal taste as a defect.
Read the frontend/UI, UX/usability, accessibility and business-flow dimensions in `Config/QA-Agent/professional-coverage-model.yaml`.

## Procedure

1. Confirm design version, supported viewport and browser matrix, persona, role, locale, and theme.
2. Cover layout, typography, content, component consistency, navigation, deep links, route guards, responsive breakpoints, loading, empty, error, disabled, success, partial, stale and permission-denied states.
3. Test forms, validation timing, messages, focus behavior, destructive confirmations, feedback, recovery, and state preservation.
4. Check refresh/back/forward/multi-tab state preservation, long content, localization, dates, time zones, numeric formats, zoom, permissions and realistic data extremes.
5. Verify UI enforcement against direct API behavior where client-only validation/hidden actions could be bypassed; route accessibility and usability depth to workflows 07/19 and 16.
6. Capture expected-source references and visual/behavioral evidence. Separate implementation defect, design inconsistency, usability issue, accessibility issue and enhancement.

## Output Contract

Return coverage-unit and journey/component, viewport/browser/device, role/state/data, design or requirement source, expected, actual, API/readback when required, evidence, classification, severity, recommendation and residual risk.

## Bổ sung 2026-09-07 — Cross-module blast radius (bắt buộc trước khi test)

Trước khi thiết kế/chạy E2E hoặc UI/UX, đọc `Projects/<ACTIVE_PROJECT>/Knowledge-Base/Domain-Rules/_cross-module-map.md`:

- Xác định module đang test **là consumer của shared component/logic nào** (pagination · filter-chip/search-box/table-display · BasePage/NavPage · ProtectPage route-guard · RBAC · SLA/breach counter · verdict model · whitelist→alert · node error classifier · CMDB asset data…).
- US **chỉ DÙNG** shared đó → test thêm invariant của shared ngay trên màn này.
- US **SỬA chính shared** đó → regression **TOÀN BỘ module ở cột "Blast radius"** của map, nêu rõ trong scope — không chỉ test màn đang làm. Đây là câu trả lời cho "module khác làm giống thì logic bên này có ảnh hưởng không".
- Hit **INFERRED** phải soi live (mở đúng component/struct/collection) xác minh trước khi tính là ảnh hưởng — không tự tin liệt kê chung với CONFIRMED.

Cùng recall `Defects/INDEX.md` + `Domain-Rules/<module>/_overview.md` (như recall-gate skill 01). Phát hiện shared MỚI → ghi vào `_cross-module-map.md` (kỷ luật chưng cất, skill 13/33).

## Bổ sung 2026-09-16 — Layer test RESPONSIVE / VỠ KHUNG (BẮT BUỘC, Lead + BA chốt)

BA yêu cầu test UI **theo góc người dùng**: app/platform phải trông chuyên nghiệp, **resize/thu hẹp KHÔNG được vỡ, bể, chồng chữ**. Kiểm chức năng đúng là chưa đủ — phải test "mọi trường hợp mà vẫn đẹp". Case thật khơi ra luật này: `DEMO-7575` — bảng câu trả lời AI Copilot bị crush trong panel docked hẹp.

### Bắt buộc: mọi màn/panel có BẢNG hoặc NỘI DUNG RỘNG phải test ở nhiều bề rộng

| Mốc bề rộng | Đại diện |
|---|---|
| Full / expanded | màn đầy đủ hoặc panel mở rộng |
| Docked / panel hẹp (~450–500px) | side-panel (vd Copilot "Example AI"), drawer, split-view |
| Tablet (~768px) | |
| Mobile (~400px) | |

Ở MỌI mốc, nội dung phải **đọc được và không vỡ khung**. Đây là layer riêng, không gộp chung với test chức năng.

### Các dấu hiệu "VỠ / BỂ" phải bắt (fail nếu gặp)

- **Chữ vỡ từng ký tự/âm tiết** — cột co dưới ngưỡng, header/giá trị wrap 1 ký tự/dòng (vd `HIGH`→`HI/G/H`, `2026-05-13`→`20/26/-0/5/-13`). Đây là lỗi, không phải thẩm mỹ.
- **Bảng rộng thiếu `overflow-x:auto` và/hoặc `min-width` cột** → tự co cột tới mức crush thay vì cho cuộn ngang.
- **Tràn ngang** — `document.scrollWidth > window.innerWidth` (body rộng hơn viewport) làm cả trang scroll ngang.
- **Chồng/đè, cắt cụt** — text đè lên nhau, truncate không tooltip, nút/label tràn khỏi panel.
- **Scroll lên/xuống kẹt** — nội dung/dialog dài phải cuộn được tới nút hành động (Send/Cancel); dialog dài mà không scroll tới được nút = fail.

### Cách ĐO (runtime, không phán bằng mắt suông)

- Playwright `setViewportSize` qua các mốc trên; ở mỗi mốc **chụp ảnh** + đo:
  - Tràn ngang: `document.scrollWidth - window.innerWidth`.
  - **Crush cột**: đếm ô `<td>/<th>` có `width < 48px` trong khi text > 5 ký tự (wrap nhiều dòng). Ghi số ô vỡ / tổng ô.
- ⚠️ **Metric "overflow = 0" KHÔNG đủ để PASS**: bảng có thể tự co cột tới mức vỡ ký tự mà `scrollWidth` vẫn khít container (không tràn). PHẢI đo crush riêng — đã suýt kết luận nhầm "không tràn = ổn" ở DEMO-7575.
- Oracle: mockup (nếu có) + chuẩn UI chuyên nghiệp + yêu cầu BA. Báo UI/UX defect khi **chữ không đọc được / khung vỡ**, không phải "gu cá nhân".

Ghi số đo (bao nhiêu ô vỡ ở bề rộng nào) vào evidence; log bug `[FE][UI/UX]` kèm ảnh đã che nếu vỡ.
