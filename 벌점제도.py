import streamlit as st
import datetime

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="쌤 화남 지수표 & 벌점 관리",
    page_icon="😡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 파스텔 UI 커스텀 CSS (이미지 스타일 반영)
st.markdown("""
    <style>
    .stApp {
        background-color: #EBF1FF;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
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

    /* 🔥 쌤 화남 지수 전용 배너 */
    .teacher-anger-card {
        background: linear-gradient(135deg, #FFEDD5 0%, #FEE2E2 100%);
        border: 2px solid #FECACA;
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        margin-bottom: 16px;
    }
    .teacher-anger-title {
        font-size: 15px;
        font-weight: 800;
        color: #991B1B;
    }
    .teacher-anger-score {
        font-size: 38px;
        font-weight: 900;
        color: #DC2626;
        margin: 4px 0;
    }
    .teacher-anger-status {
        font-size: 14px;
        font-weight: 700;
        color: #B91C1C;
    }
    .anger-detail-box {
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        padding: 10px;
        margin-top: 10px;
        font-size: 12px;
        color: #7F1D1D;
        text-align: left;
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

# 3. 세션 상태 안전 초기화 (오류 방지)
if "teacher_anger_level" not in st.session_state:
    st.session_state["teacher_anger_level"] = 35

if "is_teacher" not in st.session_state:
    st.session_state["is_teacher"] = False

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

# 4. 상단 헤더
st.markdown("""
    <div class="main-header">
        <h1>쌤 화남 지수표 & 벌점 관리 😡</h1>
        <p>조금 더 바른 행동이 더 좋은 우리 반을 만들어요!</p>
    </div>
""", unsafe_allow_html=True)

# 5. 🔥 선생님 화남 상세 상태 계산 함수
anger_val = st.session_state["teacher_anger_level"]

if anger_val < 25:
    anger_status = "😊 1단계: 평온함 (기분 아주 좋음!)"
    voice_status = "🔊 목소리: 상냥하고 유쾌함"
    face_status = "😃 표정: 미소를 짓고 계심"
    action_guide = "✨ 자유롭게 질문하고 발표하기 좋은 상태입니다!"
elif anger_val < 50:
    anger_status = "😐 2단계: 약간 화남 (주의 필요)"
    voice_status = "🔊 목소리: 평소보다 약간 낮아짐"
    face_status = "😐 표정: 무표정 유지 중"
    action_guide = "⚠️ 잡담을 줄이고 수업에 집중하세요!"
elif anger_val < 75:
    anger_status = "😡 3단계: 많이 화남 (경고 단계)"
    voice_status = "🔊 목소리: 크고 단호해짐"
    face_status = "😠 표정: 굳어있고 칠판을 세게 치심"
    action_guide = "🚨 조용히 하고 선생님 지시에 절대 복종하세요!"
else:
    anger_status = "🚨 4단계: 폭발 직전 (위험 상황!)"
    voice_status = "🔊 목소리: 한숨 또는 차가운 정적"
    face_status = "😡 표정: 매우 심각함"
    action_guide = "☠️ 숨소리도 죽이고 즉시 바른 자세를 취하세요!"

st.markdown(f"""
    <div class="teacher-anger-card">
        <div class="teacher-anger-title">🔥 선생님의 현재 화남 지수</div>
        <div class="teacher-anger-score">{anger_val} / 100</div>
        <div class="teacher-anger-status">{anger_status}</div>
        <div class="anger-detail-box">
            • <b>현재 상태:</b> {voice_status} | {face_status}<br/>
            • <b>행동 요령:</b> {action_guide}
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. 탭 구성
tab1, tab2, tab3 = st.tabs(["🏠 홈 현황", "🔒 선생님 전용 (작성)", "📜 학급 규칙"])

# -------------------------------
# [탭 1] 홈 현황
# -------------------------------
with tab1:
    # 🌟 [요청사항 반영] 홈 화면에서 선생님 화남 지수를 바로 수치로 작성/입력하는 칸
    st.write("### ✍️ 쌤 화남 지수 직접 작성하기")
    col_input, col_btn = st.columns([2, 1])
    
    with col_input:
        input_anger = st.number_input(
            "화남 지수 입력 (0~100)", 
            min_value=0, 
            max_value=100, 
            value=st.session_state["teacher_anger_level"],
            step=1,
            key="home_anger_input"
        )
    with col_btn:
        st.write("") # 버튼 위치 맞춤용 빈 공간
        st.write("")
        if st.button("적용하기", key="home_anger_btn", use_container_width=True):
            st.session_state["teacher_anger_level"] = int(input_anger)
            st.success("화남 지수가 반영되었습니다!")
            st.rerun()

    st.divider()

    # 학급 누적 벌점 표시
    total_score = sum(item["score"] for item in st.session_state["records"])
    
    st.markdown(f"""
        <div class="score-card">
            <div class="score-title">현재 학급 누적 벌점</div>
            <div class="score-number">{total_score}점</div>
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
# [탭 2] 선생님 전용 (1+1=2 퀴즈 인증)
# -------------------------------
with tab2:
    if not st.session_state["is_teacher"]:
        st.subheader("🔒 선생님 인증")
        st.write("선생님만 들어갈 수 있습니다. 아래 문제를 풀어주세요.")
        
        with st.form("teacher_auth_form"):
            answer = st.text_input("문제: 1 + 1 = ?", placeholder="답을 입력하세요")
            auth_submit = st.form_submit_button("인증하기", use_container_width=True)
            
            if auth_submit:
                if answer.strip() == "2":
                    st.session_state["is_teacher"] = True
                    st.success("선생님 인증이 완료되었습니다!")
                    st.rerun()
                else:
                    st.error("답이 틀렸습니다! 정답은 2 입니다.")
    else:
        # 선생님 인증 성공 시
        st.success("🔓 선생님 전용 관리 모드 실행 중")
        if st.button("로그아웃 (학생 모드로 전환)", type="secondary"):
            st.session_state["is_teacher"] = False
            st.rerun()

        st.write("---")
        
        # 벌점 부과 작성
        st.write("### ✍️ 벌점 위반 항목 기록")
        
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
                    # 벌점 추가 시 화남 지수 자동 상승
                    st.session_state["teacher_anger_level"] = min(100, st.session_state["teacher_anger_level"] + int(score))
                    st.success(f"'{category}' 항목(-{score}점)이 기록되었으며, 화남 지수가 상승했습니다!")
                    st.rerun()

# -------------------------------
# [탭 3] 학급 규칙 안내
# -------------------------------
with tab3:
    st.write("### 📢 학급 규칙 안내")
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
