#!/usr/bin/env python3
"""UserPromptSubmit hook — nhắc luật ĐỊNH DẠNG CÂU TRẢ LỜI mỗi lượt.

Vì sao cần hook này (ghi lại để người sau không xoá nhầm):
Luật "mọi mã Jira phải là link bấm được + mọi file phải là link tương đối + trả kết quả bằng bảng"
nằm ở `Projects/<ACTIVE_PROJECT>/CLAUDE.md`. Ngày 2026-09-16 một phiên làm việc dài đã vi phạm luật
này vì phiên đó không mở file project CLAUDE.md — luật có mà không được nạp vào ngữ cảnh.
Lead chốt hai lớp chặn: (A) ghim luật vào root `CLAUDE.md`, (B) hook này nhắc lại mỗi lượt prompt.

Hook này CỐ Ý luôn bắn (không phụ thuộc từ khoá) vì đây là luật định dạng áp cho MỌI câu trả lời,
không phải luật theo ngữ cảnh như `prompt_skill_nudge.py`.

Nó chỉ NHẮC, không chặn gì — UserPromptSubmit không chặn được output, và không nên chặn.
"""
import json
import sys

REMINDER = (
    "📐 Định dạng câu trả lời (luật Lead, root CLAUDE.md + Projects/<ACTIVE_PROJECT>/CLAUDE.md):\n"
    "- Mọi mã Jira → link bấm được: [DEMO-1234](https://YOUR-SITE.atlassian.net/browse/DEMO-1234), "
    "kể cả ticket cũ nhắc lại.\n"
    "- Mọi file workspace → link tương đối bấm được: [tên](đường/dẫn.md). KHÔNG viết path trần "
    "trong backtick.\n"
    "- Kết quả trả về bằng BẢNG, không phải văn xuôi. Văn xuôi chỉ dùng cho đính chính/cảnh báo "
    "không xếp bảng được.\n"
    "- API ghi full host+path (https://dev-api.example.local/...); ticket ghi mã+link, không URL trần."
)


def main():
    # Đọc và bỏ payload stdin — hook này không phụ thuộc nội dung prompt.
    try:
        sys.stdin.read()
    except Exception:
        pass

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER,
        }
    }))


if __name__ == "__main__":
    main()
