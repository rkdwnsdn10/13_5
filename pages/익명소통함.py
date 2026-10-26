
import streamlit as st
import json
import os
import re
import uuid
import csv
import io
import unicodedata
from datetime import datetime

st.set_page_config(
    page_title="마음우체통",
    page_icon="💌",
    layout="centered",
)

DATA_FILE = "messages.json"
MAX_LENGTH = 1000

BAD_WORDS = [
    "시발", "씨발", "씨팔", "병신", "븅신",
    "개새끼", "새끼", "좆", "지랄", "염병",
    "꺼져", "닥쳐", "미친놈", "미친년",
    "죽어", "죽여버려", "ㅅㅂ", "ㅂㅅ",
]

CATEGORIES = [
    "💭 고민 상담",
    "📚 수업 건의",
    "🤝 친구 관계",
    "🌷 칭찬과 감사",
    "📮 기타 의견",
]

STATUSES = ["새 의견", "확인 중", "답변·조치 완료"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');

.stApp {
    background: #FFF9F3;
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 800px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(135deg, #F9E5DD, #EEE5F8);
    padding: 30px 20px;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 24px;
}
.hero h1 {
    color: #55435E;
    font-size: 2.2rem;
    font-weight: 800;
}
.hero p {
    color: #75667B;
    line-height: 1.8;
}
div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 12px;
    min-height: 44px;
}
</style>
""", unsafe_allow_html=True)


def normalize_text(text):
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"[\W_]+", "", text)


def find_bad_words(text):
    normalized = normalize_text(text)
    found = []

    for word in BAD_WORDS:
        if normalize_text(word) in normalized:
            found.append(word)

    return list(set(found))


def load_messages():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return [
                item for item in data
                if isinstance(item, dict)
                and isinstance(item.get("id"), str)
                and isinstance(item.get("content"), str)
            ]

        return []

    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        st.error("저장된 의견을 읽지 못했습니다.")
        return []


def save_messages(messages):
    try:
        temp_file = DATA_FILE + ".tmp"

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(
                messages,
                file,
                ensure_ascii=False,
                indent=2,
            )

        os.replace(temp_file, DATA_FILE)
        return True

    except (OSError, TypeError, ValueError):
        st.error("저장에 실패했습니다. 잠시 후 다시 시도해 주세요.")
        return False


# 상단 화면
st.markdown("""
<div class="hero">
    <div style="font-size: 48px;">💌</div>
    <h1>우리 반 마음우체통</h1>
    <p>
        이름 없이 전하는 소중한 마음<br>
        고민도, 건의도, 칭찬도 편하게 남겨 주세요.
    </p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 🌼 이용 약속")
    st.markdown("""
    - 이름이나 학번 등 개인정보는 적지 마세요.
    - 욕설, 비하, 협박 등 부적절한 표현은 제한됩니다.
    - 서로를 존중하는 표현으로 작성해 주세요.
    - 긴급한 문제는 선생님이나 믿을 수 있는 어른에게 직접 알려 주세요.
    """)

page = st.radio(
    "화면 선택",
    ["✉️ 익명 의견 보내기", "🔐 선생님 관리실"],
    horizontal=True,
)

# 학생 화면
if page == "✉️ 익명 의견 보내기":
    st.markdown("## 편지 쓰기")
    st.caption("이름을 입력할 필요가 없습니다.")

    if "submission_count" not in st.session_state:
        st.session_state.submission_count = 0

    st.caption(
        f"현재 세션 제출 횟수: "
        f"{st.session_state.submission_count}/5"
    )

    with st.form("message_form"):
        category = st.selectbox("의견 종류", CATEGORIES)

        title = st.text_input(
            "제목 (선택)",
            max_chars=60,
            placeholder="예: 수업 시간에 건의하고 싶은 점",
        )

        content = st.text_area(
            "전하고 싶은 이야기",
            max_chars=MAX_LENGTH,
            height=180,
            placeholder="편하게 이야기해 주세요.",
        )

        confirmed = st.checkbox(
            "이용 약속을 읽었으며 개인정보를 작성하지 않았습니다."
        )

        submitted = st.form_submit_button(
            "💌 익명으로 보내기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if st.session_state.submission_count >= 5:
            st.error("현재 세션의 제출 횟수를 초과했습니다.")

        elif not content.strip():
            st.warning("내용을 입력해 주세요.")

        elif not confirmed:
            st.warning("이용 약속을 확인해 주세요.")

        else:
            bad_words = find_bad_words(title + " " + content)

            if bad_words:
                st.error(
                    "부적절한 표현이 감지되었습니다. "
                    "표현을 바꾸어 다시 작성해 주세요."
                )

            else:
                messages = load_messages()

                message = {
                    "id": uuid.uuid4().hex,
                    "created_at": datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    ),
                    "category": category,
                    "title": title.strip() or "(제목 없음)",
                    "content": content.strip(),
                    "status": "새 의견",
                }

                if save_messages([message] + messages):
                    st.session_state.submission_count += 1
                    st.success("편지를 전달했어요. 소중한 의견 고마워요! 💗")
                    st.caption(
                        "이름은 입력받지 않지만 완전한 익명성이나 "
                        "영구 보관이 보장되는 것은 아닙니다."
                    )

    st.markdown("---")
    st.caption(
        "마음우체통은 긴급 신고 창구가 아닙니다. "
        "도움이 급하게 필요한 상황에서는 선생님에게 직접 알려 주세요."
    )


# 선생님 관리 화면
else:
    st.markdown("## 🔐 선생님 관리실")

    try:
        admin_password = st.secrets.get("ADMIN_PASSWORD", "")
    except Exception:
        admin_password = ""

    if not admin_password:
        st.warning(
            "관리자 비밀번호가 설정되지 않았습니다. "
            "앱 설정의 Secrets에 ADMIN_PASSWORD를 추가해 주세요."
        )

    else:
        if "admin_logged_in" not in st.session_state:
            st.session_state.admin_logged_in = False

        if not st.session_state.admin_logged_in:
            with st.form("login_form"):
                password = st.text_input(
                    "관리자 비밀번호",
                    type="password",
                )
                login = st.form_submit_button(
                    "로그인",
                    type="primary",
                    use_container_width=True,
                )

            if login:
                if password and password == admin_password:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("비밀번호가 올바르지 않습니다.")

        if st.session_state.admin_logged_in:
            if st.button("로그아웃"):
                st.session_state.admin_logged_in = False
                st.rerun()

            messages = load_messages()

            col1, col2, col3 = st.columns(3)
            col1.metric("전체 의견", len(messages))
            col2.metric(
                "새 의견",
                sum(m.get("status") == "새 의견" for m in messages),
            )
            col3.metric(
                "완료",
                sum(
                    m.get("status") == "답변·조치 완료"
                    for m in messages
                ),
            )

            st.markdown("### 📬 도착한 편지")

            search = st.text_input("제목 또는 내용 검색")
            status_filter = st.selectbox(
                "상태 필터",
                ["전체"] + STATUSES,
            )
            category_filter = st.selectbox(
                "유형 필터",
                ["전체"] + CATEGORIES,
            )

            filtered = []

            for message in messages:
                if (
                    status_filter != "전체"
                    and message.get("status") != status_filter
                ):
                    continue

                if (
                    category_filter != "전체"
                    and message.get("category") != category_filter
                ):
                    continue

                searchable = (
                    message.get("title", "")
                    + " "
                    + message.get("content", "")
                ).casefold()

                if search.casefold() not in searchable:
                    continue

                filtered.append(message)

            if not filtered:
                st.info("표시할 편지가 없습니다.")

            for message in filtered:
                message_id = message["id"]
                current_status = message.get("status", "새 의견")

                if current_status not in STATUSES:
                    current_status = "새 의견"

                with st.expander(
                    f'{message.get("category", "기타 의견")} · '
                    f'{message.get("title", "(제목 없음)")} · '
                    f'{current_status}'
                ):
                    st.caption(
                        "접수 시간: "
                        + message.get("created_at", "알 수 없음")
                    )
                    st.write(message.get("content", ""))

                    new_status = st.selectbox(
                        "처리 상태",
                        STATUSES,
                        index=STATUSES.index(current_status),
                        key=f"status_{message_id}",
                    )

                    if st.button(
                        "상태 저장",
                        key=f"save_{message_id}",
                    ):
                        updated = []

                        for item in messages:
                            copied = item.copy()

                            if copied.get("id") == message_id:
                                copied["status"] = new_status

                            updated.append(copied)

                        if save_messages(updated):
                            st.success("상태를 저장했습니다.")
                            st.rerun()

            st.markdown("---")
            st.markdown("### 📥 의견 백업")

            if messages:
                buffer = io.StringIO()
                fields = [
                    "created_at",
                    "category",
                    "title",
                    "content",
                    "status",
                ]

                writer = csv.DictWriter(
                    buffer,
                    fieldnames=fields,
                    extrasaction="ignore",
                )
                writer.writeheader()

                for message in messages:
                    writer.writerow({
                        field: message.get(field, "")
                        for field in fields
                    })

                st.download_button(
                    "CSV 파일 다운로드",
                    data="\ufeff" + buffer.getvalue(),
                    file_name="maeum_mailbox_backup.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            st.warning(
                "파일 기반 저장은 영구 보관을 보장하지 않습니다. "
                "민감한 상담 내용을 장기간 보관하려면 "
                "별도의 데이터베이스와 보안 설정이 필요합니다."
            )


st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#95879A;'>"
    "💌 서로의 마음을 존중하는 우리 반"
    "</div>",
    unsafe_allow_html=True,
)
