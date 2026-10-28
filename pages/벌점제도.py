import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="쌤 화남 지수표",
    page_icon="😡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 커스텀 CSS (깔끔한 UI 연출)
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #7F8C8D;
        margin-bottom: 25px;
    }
    .score-card {
        background-color: #FFF5F5;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 2px solid #FEB2B2;
        margin-bottom: 20px;
    }
    .score-number {
        font-size: 3rem;
        font-weight: bold;
        color: #E53E3E;
    }
    .status-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #C53030;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 데이터 초기화 (Session State 사용)
if "records" not in st.session_state:
    # 샘플 데이터 초기 생성
    st.session_state.records = [
        {
            "date": "2026-09-26",
            "day": "금",
            "category": "수업 중 떠들기",
            "score": -5,
            "student": "김하율",
            "detail": "수업 시간 친구와 잡담",
        },
        {
            "date": "2026-09-25",
            "day": "목",
            "category": "지각",
            "score": -10,
            "student": "김하율",
            "detail": "1교시 10분 지각",
        },
        {
            "date": "2026-09-24",
            "day": "수",
            "category": "휴대폰 사용",
            "score": -10,
            "student": "김하율",
            "detail": "수업 중 유튜브 시청",
        },
        {
            "date": "2026-09-22",
            "day": "화",
            "category": "수업 방해 행동",
            "score": -5,
            "student": "김하율",
            "detail": "장난치다 걸림",
        },
        {
            "date": "2026-09-20",
            "day": "일",
            "category": "규칙 위반",
            "score": -10,
            "student": "김하율",
            "detail": "청소 안 하고 하교",
        },
    ]

# 벌점 항목 및 기본 점수 정의
VIOLATION_RULES = {
    "수업 중 떠들기": {"score": -5, "icon": "💬"},
    "수업 방해 행동": {"score": -5, "icon": "📣"},
    "지각": {"score": -10, "icon": "⏰"},
    "휴대폰 사용": {"score": -10, "icon": "📱"},
    "규칙 위반": {"score": -10, "icon": "⚠️"},
    "기타": {"score": -5, "icon": "💬"},
}

# 헤더
st.markdown("<div class='main-title'>쌤 화남 지수표 😡</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>조금 더 바른 행동이 더 좋은 우리 반을 만들어요! ✨</div>",
    unsafe_allow_html=True,
)

# 탭 구성 (하단/상단 네비게이션)
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 홈", "✏️ 벌점 기록하기", "📊 기록 & 통계", "📜 규칙 안내"]
)

# -------------------------------------------------------------------
# TAB 1: 홈 (대시보드)
# -------------------------------------------------------------------
with tab1:
    col_user, col_setting = st.columns([4, 1])
    with col_user:
        st.subheader("안녕하세요! 2학년 3반 👋")

    # 총 벌점 계산 (음수를 양수로 변환하여 표시)
    total_score = abs(
        sum(item["score"] for item in st.session_state.records)
    )

    # 화남 지수 단계 설정
    if total_score < 10:
        status_emoji = "😇"
        status_msg = "선생님이 아주 온화한 상태입니다!"
    elif total_score < 25:
        status_emoji = "😐"
        status_msg = "조금만 더 조심해요!"
    elif total_score < 40:
        status_emoji = "😠"
        status_msg = "선생님의 눈썹이 파르르 떨리고 있습니다!"
    else:
        status_emoji = "💥"
        status_msg = "경고! 선생님 폭발 직전입니다!"

    st.markdown(
        f"""
    <div class='score-card'>
        <div style='font-size: 1.1rem; color: #555;'>현재 누적 벌점</div>
        <div class='score-number'>{total_score}점 {status_emoji}</div>
        <div class='status-text'>{status_msg}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("---")
    st.subheader("📋 최근 벌점 기록")

    if st.session_state.records:
        recent_records = sorted(
            st.session_state.records, key=lambda x: x["date"], reverse=True
        )[:5]
        for rec in recent_records:
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                icon = VIOLATION_RULES.get(rec["category"], {}).get(
                    "icon", "📌"
                )
                st.write(f"{icon} **{rec['category']}** ({rec['student']})")
            with col2:
                st.caption(f"{rec['date']}")
            with col3:
                st.markdown(
                    f"<span style='color: red; font-weight: bold;'>{rec['score']}점</span>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("아직 등록된 벌점 기록이 없습니다.")

# -------------------------------------------------------------------
# TAB 2: 벌점 기록하기
# -------------------------------------------------------------------
with tab2:
    st.subheader("✏️ 벌점 기록하기")
    st.write("위반 항목 및 내용을 입력해 주세요.")

    student_name = st.text_input("학생 이름", value="김하율")
    selected_category = st.selectbox(
        "위반 항목 선택", list(VIOLATION_RULES.keys())
    )

    rule_info = VIOLATION_RULES[selected_category]
    st.info(
        f"선택한 항목: **{selected_category}** ({rule_info['icon']}) → 기본 감점: **{rule_info['score']}점**"
    )

    detail_text = st.text_area(
        "상세 내용 (선택사항)", placeholder="예) 수업 시간에
