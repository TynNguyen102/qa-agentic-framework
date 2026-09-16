---
name: 29-mobile-feature-testing
description: Design or execute mobile feature testing across mobile web, native, or hybrid apps using a risk-based device and OS matrix and mobile lifecycle scenarios. Use when functionality must be validated on phones or tablets.
---

# Mobile Feature Testing

First classify the product:

- Mobile web: Playwright emulation is useful, but critical behavior still needs real-device validation.
- Native or hybrid: use the project's Appium and platform-driver conventions.

If the platform, build source, supported devices, minimum OS, or device access is unknown, return `NEED_CONFIG`.

## Procedure

1. Build a representative matrix by platform, OS, screen, hardware class, locale, network, and risk.
2. Cover install, upgrade, first launch, permissions, lifecycle, background/foreground, force close, rotation, interruption, low network/offline, deep links, push, keyboard, biometrics, secure storage, and data synchronization as applicable.
3. Validate touch behavior, responsive layout, accessibility, battery/memory signals, and platform conventions.
4. Use clean and upgrade states, deterministic accounts/data, logs, screenshots/video, and backend readback.
5. Distinguish emulator/simulator evidence from real-device evidence.

## Output Contract

Return app type, device matrix, build, scenarios, platform-specific expected results, automation route, execution status, evidence, defects, and device gaps.

## Chọn tool (bổ sung 2026-09-16)

Skill này có nhắc tên tool cụ thể ở trên. Tên tool là **mặc định hiện tại của workspace**, không phải
ràng buộc cứng — việc chọn tool đi qua `Config/QA-Agent/tool-adapters.yaml`:

1. Xác định **capability** cần dùng (vd `ui_browser_automation`, `api_testing`,
   `acceptance_suite_runner`, `load_and_performance`, `database_query`).
2. Đọc `Projects/<ACTIVE_PROJECT>/Config/tool-inventory.yaml` — tool `NOT_INSTALLED`/`NOT_CONFIGURED`
   thì coi như **không có**, dù được nhắc tên ở đây.
3. Chọn adapter `rank` thấp nhất **thực sự khả dụng**.
4. Không adapter nào khả dụng ⇒ trả `NEED_CONFIG: <capability>_ADAPTER_UNAVAILABLE`.
   **Không** claim đã chạy.

Đổi adapter **không** đổi contract: `outputs` phải giữ nguyên hình dạng để skill sau dùng được.
