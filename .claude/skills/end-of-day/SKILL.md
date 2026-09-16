---
name: end-of-day
description: Chốt cuối ngày — tổng hợp việc đã làm, việc còn dở, việc bị chặn và việc cho ngày mai, rồi ghi vào CURRENT_STATE và audit-events. Dùng khi kết thúc buổi làm việc, hoặc khi anh nói "chốt ngày", "lưu việc cuối ngày", "hôm nay làm được gì". Đây là cặp đối xứng của daily-check.
---

# End of Day

Cặp đối xứng của `daily-check`. `daily-check` mở đầu ngày bằng cách hỏi *"có gì mới?"*;
skill này đóng ngày bằng cách trả lời *"hôm nay đã đổi được gì, và mai bắt đầu từ đâu?"*

Mục tiêu là **phiên làm việc ngày mai không phải dựng lại ngữ cảnh từ đầu** — dù là anh, một QC
khác, hay một phiên AI mới.

## Procedure

1. **Resolve dự án đang active** — đọc `project/active-project.yaml`. Nếu file liệt kê nhiều dự án
   và anh không nói rõ, hỏi trước khi làm.

2. **Thu thập việc đã làm trong ngày** — từ ba nguồn, không đoán:
   - `git log --since=midnight --oneline` trong workspace (commit hôm nay)
   - `Projects/<ACTIVE_PROJECT>/governance/audit-events/<YYYY>/<MM>/` — event có timestamp hôm nay
   - `Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md` — các mục đã ghi trong ngày
   - File mới/sửa chưa commit: `git status --short`

3. **Đối chiếu Jira live** — những gì đã đụng vào hôm nay:
   - Issue được tạo, sửa, comment, chuyển trạng thái bởi tài khoản đang dùng
   - JQL gợi ý: `project = <KEY> AND updated >= startOfDay() AND (reporter = currentUser() OR assignee = currentUser())`
   - Nếu Atlassian MCP không kết nối được, ghi `NOT_CHECKED` kèm lý do — **không suy đoán**

4. **Phân loại thành bốn nhóm** — đây là phần có giá trị nhất, đừng gộp:

   | Nhóm | Nghĩa là gì |
   |---|---|
   | **XONG** | Đã hoàn tất, có artifact hoặc bằng chứng cụ thể |
   | **ĐANG DỞ** | Bắt đầu rồi nhưng chưa xong — ghi rõ **dừng ở bước nào** |
   | **BỊ CHẶN** | Không tự đi tiếp được — ghi rõ **chặn bởi gì** và **chờ ai** |
   | **MAI LÀM** | Việc kế tiếp, ưu tiên theo deadline thật của Jira |

5. **Kiểm ba thứ dễ quên**:
   - Deadline trong 1–3 ngày tới mà chưa động tới
   - Live write đã làm hôm nay nhưng **chưa ghi audit event**
   - File đã sửa nhưng **chưa commit**

6. **Ghi lại** — hai chỗ, không bỏ chỗ nào:
   - Append vào `Projects/<ACTIVE_PROJECT>/CURRENT_STATE.md` một mục có ngày tháng
   - Tạo audit event trong `governance/audit-events/<YYYY>/<MM>/` theo `governance/audit-policy.yaml`

7. **Nhắc commit** — nếu còn thay đổi chưa commit thì nói rõ số file và đề nghị commit.
   **Không tự push** — push cần anh đồng ý trong phiên.

## Output Contract

Trả về **bốn bảng** theo đúng thứ tự nhóm ở bước 4. Mỗi dòng phải có bằng chứng cụ thể
(key Jira, đường dẫn file, hash commit) — không viết chung chung kiểu "đã review một số testcase".

Kèm:
- Đường dẫn file `CURRENT_STATE.md` và audit event vừa ghi
- Số thay đổi chưa commit, nếu có
- Nguồn nào không kiểm được và vì sao

## Hard rules

- **Không tuyên bố XONG nếu thiếu bằng chứng.** Không có artifact thì thuộc nhóm ĐANG DỞ.
- **Không gộp BỊ CHẶN vào ĐANG DỞ.** Hai nhóm này dẫn tới hành động khác nhau: một cái cần thời
  gian, một cái cần người khác. Gộp lại là cách nhanh nhất để một blocker nằm im cả tuần.
- **Không tự tạo, sửa, đóng issue Jira** trong lúc chốt ngày. Skill này chỉ đọc và ghi file local.
- **Không tự push.** Chỉ nhắc.
- Không ghi đè mục của ngày khác trong `CURRENT_STATE.md` — luôn append.
- Nếu một nguồn không kiểm được, ghi `NOT_CHECKED` kèm lý do. Phân biệt rõ với "đã kiểm và không có gì".
