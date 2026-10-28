import datetime
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="쌤 화남 지수표",
    page_icon="😡",
    layout="centered"
)

# 배경색(파란색 계열) 및 글자색(검정색/높은 가독성) 커스텀 CSS
st.markdown(
    """
    <style>
    /* 전체 앱 배경색을 파란색 계열로 변경 */
    .stApp {
        background-color: #EBF8FF;
        color: #1A202C;
    }
    
    /* 기본 글자색 및 타이틀/헤더 색상을 검정색으로 지정 */
    h1, h2, h3, h4, h5, h6, p, label, div, span, li {
        color: #1A202C !important;
    }
    
    /* 카드 및 메트릭 배경을 하얀색으로 깔끔하게 처리하여 가독성 증대 */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #CBD5E0;
    }
    
    /* metric 내부 텍스트 색상 정리 */
    [data-testid="stMetricLabel"] {
        color: #2D3748 !important;
        font-weight: bold;
    }
    [data-testid="stMetricValue"] {
        color: #E53E3E !important;
        font-weight: bold;
    }
    
    /* 입력창 및 셀렉트박스 배경/글자색 조절 */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        border-radius: 8px;
    }
    
    /* 탭 메뉴 디자인 스타일링 */
    button[data-baseweb="tab"] {
        font-weight: bold;
        color: #2B6CB0 !important;
    }
    button[aria-selected="true"] {
        color: #1A365D !important;
        border-bottom-color: #2B6CB0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 데이터 초기화 (Session State 사용)
if "records" not in st.session_state:
    st.session_state.records = [
        {"date": "2026-09-26", "day": "금", "category": "수업 중 떠들기", "score": -5, "student": "김하율", "detail": "수업 시간 친구와 대화"},
        {"date": "2026-09-25", "day": "목", "category": "지각", "score": -10, "student": "김하율", "detail": "1교시 지각"},
        {"date": "2026-09-24", "day": "수", "category": "휴대폰 사용", "score": -10, "student": "김하율", "detail": "수업 중 휴대폰 사용"},
        {"date": "2026-09-22", "day": "화", "category": "수업 방해 행동", "score": -5, "student": "김하율", "detail": "수업 방해"},
        {"date": "2026-09-20", "day": "일", "category": "규칙 위반", "score": -10, "student": "김하율", "detail": "학급 규칙 위반"}
    ]

# 위반 항목 및 점수
RULES = {
    "수업 중 떠들기": {"score": -5, "icon": "💬"},
    "수업 방해 행동": {"score": -5, "icon": "📣"},
    "지각": {"score": -10, "icon": "⏰"},
    "휴대폰 사용": {"score": -10, "icon": "📱"},
    "규칙 위반": {"score": -10, "icon": "⚠️"},
    "기타": {"score": -5, "icon": "💬"}
}

# 메인 타이틀
st.title("쌤 화남 지수표 😡")
st.caption("조금 더 바른 행동이 더 좋은 우리 반을 만들어요!")
st.write("---")

# 탭 메뉴 구성
tab1, tab2, tab3, tab4 = st.tabs(["🏠 홈", "✏️ 벌점 기록하기", "📊 통계 & 내역", "📜 규칙 안내"])

# -------------------------------------------------------------------
# TAB 1: 홈 화면
# -------------------------------------------------------------------
with tab1:
    st.subheader("안녕하세요! 2학년 3반 👋")
    
    # 누적 벌점 계산 (양수로 표시)
    total_score = abs(sum(r["score"] for r in st.session_state.records))
    
    # 상태 판정
    if total_score < 10:
        emoji, status = "😇", "선생님이 온화한 상태입니다."
    elif total_score < 25:
        emoji, status = "😐", "조금만 더 조심해요!"
    elif total_score < 40:
        emoji, status = "😠", "선생님이 화나기 직전입니다!"
    else:
        emoji, status = "💥", "선생님 폭발 직전!"

    # 벌점 현황 카드
    st.metric(label="현재 누적 벌점", value=f"{total_score}점 {emoji}", delta=status, delta_color="inverse")
    
    st.write("---")
    st.subheader("📋 최근 기록")
    
    if st.session_state.records:
        for rec in reversed(st.session_state.records[-5:]):
            st.write(f"**{rec['category']}** ({rec['student']}) | {rec['date']} | :red[{rec['score']}점]")
    else:
        st.info("등록된 벌점 기록이 없습니다.")

# -------------------------------------------------------------------
# TAB 2: 벌점 기록하기
# -------------------------------------------------------------------
with tab2:
    st.subheader("위반 항목을 선택해주세요")
    
    student_name = st.text_input("학생 이름", value="김하율")
    category = st.selectbox("위반 항목", list(RULES.keys()))
    
    selected_rule = RULES[category]
    st.info(f"선택 항목: **{category}** ({selected_rule['icon']}) → 감점: **{selected_rule['score']}점**")
    
    detail = st.text_input("상세 내용 (선택사항)", placeholder="예) 수업 시간 중 잡담")
    record_date = st.date_input("날짜 선택", datetime.date.today())
    
    if st.button("기록하기", use_container_width=True, type="primary"):
        days = ["월", "화", "수", "목", "금", "토", "일"]
        day_name = days[record_date.weekday()]
        
        new_data = {
            "date": record_date.strftime("%Y-%m-%d"),
            "day": day_name,
            "category": category,
            "score": selected_rule["score"],
            "student": student_name,
            "detail": detail if detail else category
        }
        st.session_state.records.append(new_data)
        st.success(f"{student_name} 학생에게 {selected_rule['score']}점이 부과되었습니다.")
        st.rerun()

# -------------------------------------------------------------------
# TAB 3: 통계 및 내역
# -------------------------------------------------------------------
with tab3:
    st.subheader("📊 주간 벌점 현황")
    
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["abs_score"] = df["score"].abs()
        
        # 요일별 집계
        day_order = ["월", "화", "수", "목", "금", "토", "일"]
        grouped = df.groupby("day")["abs_score"].sum().reindex(day_order, fill_value=0)
        
        # 기본 차트 출력
        st.bar_chart(grouped)
        
        st.write("---")
        st.subheader("📜 상세 벌점 내역")
        for rec in reversed(st.session_state.records):
            st.write(f"- **{rec['date']} ({rec['day']})** | {rec['student']} | {rec['category']} ({rec['score']}점)")
            if rec["detail"]:
                st.caption(f"  사유: {rec['detail']}")
    else:
        st.info("기록된 데이터가 없습니다.")

# -------------------------------------------------------------------
# TAB 4: 규칙 안내
# -------------------------------------------------------------------
with tab4:
    st.subheader("📜 규칙 안내")
    st.warning("📣 이런 행동은 벌점이 부과될 수 있어요!")
    
    st.write("1. **수업 중 떠들기**: -5점")
    st.write("2. **수업 방해 행동**: -5점")
    st.write("3. **지각**: -10점")
    st.write("4. **휴대폰 사용**: -10점")
    st.write("5. **규칙 위반**: -10점")
    st.write("6. **기타**: -5점")
    
    st.write("---")
    st.success("💜 서로를 배려하고, 바른 행동을 함께 만들어가요!")
