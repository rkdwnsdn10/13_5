import streamlit as st
import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="쌤 화남 지수표 & 벌점 관리",
    page_icon="😡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 파스텔 UI 커스텀 CSS (이미지 스타일 반영)
st.markdown("""
    <style>
    /* 전체 배경색 (소프트 파스텔 블루) */
    .stApp {
        background-color: #EBF1FF;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 메인 타이틀 파스텔 카드 */
    .main-header {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        padding: 20px;
        border-radius: 24px;
        text-align: center;
        border: 2px solid #C7D2FE;
        margin-bottom: 16px;
    }
    .main-header h1 {
        color: #312E81 !important;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .main-header p {
        color: #4338CA;
        font-size: 13px;
        margin: 0;
    }

    /* 🔥 [추가] 쌤 화남 지수 전용 배너 */
    .teacher-anger-card {
        background: linear-gradient(135deg, #FFEDD5 0%, #FEE2E2 100%);
        border: 2px solid #FECACA;
        border-radius: 20px;
        padding: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    .teacher-anger-title {
        font-size: 15px;
        font-weight: 800;
        color: #991B1B;
    }
    .teacher-anger-score {
        font-size: 36px;
        font-weight: 900;
        color: #DC2626;
        margin: 4px 0;
    }
    .teacher-anger-status {
        font-size: 13px;
        font-weight: 700;
        color: #B91C1C;
    }

    /* 벌점 현황 카드 */
    .score-card {
        background-color: #FFF5F5;
        border: 1px solid #FFE4E6;
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        margin-bottom: 16px;
    }
    .score-title {
        font-size: 14px;
        font-weight: 700;
        color: #4B5563;
    }
    .score-number {
        font-size: 40px;
        font-weight: 900;
        color: #E11D48;
        margin: 4px 0;
    }
    .score-sub {
        font-size: 13px;
        color: #F43F5E;
        font-weight: 600;
    }

    /* 최근 기록 카드 */
    .record-card {
        background: white;
        padding: 12px 16px;
        border-radius: 16px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    /* 규칙 리스트 아이템 */
    .rule-box {
        background-color: white;
        padding: 14px 18px;
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #E5E7EB;
        font-size: 14px;
        font-weight: 600;
        color: #374151;
        display: flex;
        align-items: center;
    }
    .rule-num {
        background-color: #6366F1;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        margin-right: 12px;
    }

    /* 탭 메뉴 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 6px;
        border-radius: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 12px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 초기화 (세션 상태)
if "teacher_anger_level" not in st.session_state:
    st.session_state["teacher_anger_level"] = 35  # 기본 쌤 화남 지수 (0~100)

if "records" not in st.session_state:
    st.session_state["records"] = [
        {"date": "2026-09-26", "category": "수업 중 떠들기", "score": 5, "memo": "짝꿍과 지속적인 대화"},
        {"date": "2026-09-25", "category": "지각", "score": 10, "memo": "10분 지각"},
        {"date": "2026-09-24", "category": "휴대폰 사용", "score": 10, "memo": "수업 중 게임 및 웹서핑"}
    ]

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "수업 중 떠들기"
if "selected_score" not in st.session_state:
    st.session_state["selected_score"] = 5

# 4. 앱 상단 헤더
st.markdown("""
    <div class="main-header">
        <h1>쌤 화남 지수표 & 벌점 관리 😡</h1>
        <p>조금 더 바른 행동이 더 좋은 우리 반을 만들어요!</p>
    </div>
""", unsafe_allow_html=True)

# 5. 🔥 [추가 기능] 선생님 화남 지수 메인 표시판
anger_val = st.session_state["teacher_anger_level"]
if anger_val < 30:
    anger_status = "😊 평온함 (기분이 좋으셔요!)"
elif anger_val < 60:
    anger_status = "😐 약간 화남 (주의가 필요해요)"
elif anger_val < 80:
    anger_status = "😡 많이 화남 (조심하세요!)"
else:
    anger_status = "🚨 폭발 직전! (즉시 조용히 하세요!)"

st.markdown(f"""
    <div class="teacher-anger-card">
        <div class="teacher-anger-title">🔥 선생님의 현재 화남 지수</div>
        <div class="teacher-anger-score">{anger_val} / 100</div>
        <div class="teacher-anger-status">{anger_status}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 탭 구성 (홈 현황, 화남/벌점 기록, 학급 규칙)
tab1, tab2, tab3 = st.tabs(["🏠 홈 현황", "✍️ 화남 & 벌점 기록", "📜 학급 규칙"])

# -------------------------------
# [탭 1] 홈 현황
# -------------------------------
with tab1:
    total_score = sum(item["score"] for item in st.session_state["records"])
    
    st.markdown(f"""
        <div class="score-card">
            <div class="score-title">현재 학급 누적 벌점</div>
            <div class="score-number">{total_score}점</div>
            <div class="score-sub">{"조금만 더 조심해요!" if total_score >= 20 else "아주 훌륭한 학급이에요!"}</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 📋 최근 벌점 기록")
    if len(st.session_state["records"]) > 0:
        for rec in st.session_state["records"][:5]:
            st.markdown(f"""
                <div class="record-card">
                    <div>
                        <strong>{rec['category']}</strong> <small style="color:#9CA3AF;">({rec['date']})</small><br/>
                        <small style="color:#6B7280;">{rec['memo']}</small>
                    </div>
                    <div style="color:#E11D48; font-weight:800; font-size:16px;">-{rec['score']}점</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("아직 기록된 벌점이 없습니다.")

# -------------------------------
# [탭 2] 화남 수치 & 벌점 기록하기 (선생님 작성)
# -------------------------------
with tab2:
    # 🔥 [추가] 선생님 화남 지수 직접 설정 섹션
    st.write("### 🌡️ 선생님 화남 지수 직접 변경")
    new_anger = st.slider("선생님 본인의 현재 화남 수치 설정 (0 ~ 100)", min_value=0, max_value=100, value=st.session_state["teacher_anger_level"])
    if st.button("화남 지수 업데이트", use_container_width=True):
        st.session_state["teacher_anger_level"] = new_anger
        st.success(f"선생님 화남 지수가 {new_anger}점으로 변경되었습니다.")
        st.rerun()

    st.write("---")
    
    st.write("### ✍️ 벌점 위반 항목 기록")
    
    # 빠른 선택 버튼 UI
    col1, col2, col3 = st.columns(3)
    if col1.button("💬 수업 떠들기\n(-5점)", key="btn1", use_container_width=True):
        st.session_state["selected_category"] = "수업 중 떠들기"
        st.session_state["selected_score"] = 5
    if col2.button("📢 수업 방해\n(-5점)", key="btn2", use_container_width=True):
        st.session_state["selected_category"] = "수업 방해 행동"
        st.session_state["selected_score"] = 5
    if col3.button("⏰ 지각\n(-10점)", key="btn3", use_container_width=True):
        st.session_state["selected_category"] = "지각"
        st.session_state["selected_score"] = 10

    col4, col5, col6 = st.columns(3)
    if col4.button("📱 휴대폰 사용\n(-10점)", key="btn4", use_container_width=True):
        st.session_state["selected_category"] = "휴대폰 사용"
        st.session_state["selected_score"] = 10
    if col5.button("⚠️ 규칙 위반\n(-10점)", key="btn5", use_container_width=True):
        st.session_state["selected_category"] = "규칙 위반"
        st.session_state["selected_score"] = 10
    if col6.button("💬 기타\n(-5점)", key="btn6", use_container_width=True):
        st.session_state["selected_category"] = "기타 위반"
        st.session_state["selected_score"] = 5

    # 폼 입력
    with st.form("penalty_form", clear_on_submit=True):
        category = st.text_input("선택된 항목", value=st.session_state["selected_category"])
        score = st.number_input("부과할 벌점 수치 (점)", min_value=1, max_value=50, value=st.session_state["selected_score"])
        memo = st.text_area("상세 내용 (선택사항)", placeholder="예) 수업 시간에 친구와 계속 대화함")
        date_val = st.date_input("날짜", datetime.date.today())

        submitted = st.form_submit_button("벌점 기록하기", use_container_width=True)
        
        if submitted:
            if not category.strip():
                st.error("항목을 입력해 주세요.")
            else:
                new_data = {
                    "date": str(date_val),
                    "category": category,
                    "score": int(score),
                    "memo": memo if memo.strip() else "상세 내용 없음"
                }
                st.session_state["records"].insert(0, new_data)
                
                # 벌점이 기록될 때 선생님 화남 지수도 자동으로 +5점 상승하는 디테일 적용
                st.session_state["teacher_anger_level"] = min(100, st.session_state["teacher_anger_level"] + int(score))
                
                st.success(f"'{category}' 항목(-{score}점)이 기록되었습니다. (선생님 화남 지수도 증가했습니다)")
                st.rerun()

# -------------------------------
# [탭 3] 학급 규칙 안내
# -------------------------------
with tab3:
    st.write("### 📢 학급 규칙 안내")
    st.caption("이런 행동은 벌점이 부과되고 선생님을 화나게 만들어요!")
    
    rules = [
        "수업 시간에 떠들거나 장난치기",
        "수업을 방해하는 행동하기",
        "지각하기",
        "휴대폰 사용하기",
        "학급 규칙 위반하기",
        "기타 선생님이 판단하는 부적절한 행동"
    ]
    
    for idx, rule in enumerate(rules, 1):
        st.markdown(f"""
            <div class="rule-box">
                <span class="rule-num">{idx}</span>
                <span>{rule}</span>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <div style="background-color: #EEF2FF; padding: 16px; border-radius: 16px; text-align: center; margin-top: 20px; color: #4338CA; font-weight: 700;">
            💜 서로를 배려하고, 바른 행동을 함께 만들어가요!
        </div>
    """, unsafe_allow_html=True)
