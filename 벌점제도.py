import streamlit as st
import datetime
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="쌤 화남 지수표",
    page_icon="😡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 이미지 모티브 파스텔 UI 커스텀 CSS 스타일링
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background-color: #F0F4FF;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 메인 타이틀 파스텔 카드 */
    .header-card {
        background: linear-gradient(135deg, #6C5CE7 0%, #a29bfe 100%);
        padding: 24px;
        border-radius: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(108, 92, 231, 0.15);
        margin-bottom: 25px;
    }
    .header-card h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 800;
        color: white !important;
    }
    .header-card p {
        margin-top: 8px;
        font-size: 14px;
        opacity: 0.9;
    }

    /* 현황 카드 스타일 */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #E8EEFF;
    }
    .stat-score {
        font-size: 42px;
        font-weight: 900;
        color: #FF4757;
        margin: 10px 0;
    }
    .stat-status {
        font-size: 15px;
        font-weight: 600;
        color: #57606F;
    }

    /* 학급 규칙 리스트 카튼 */
    .rule-item {
        background-color: white;
        padding: 14px 18px;
        border-radius: 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        border-left: 5px solid #6C5CE7;
        font-weight: 600;
        color: #2D3436;
    }
    
    /* 버튼 커스텀 */
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 48px;
        background-color: #6C5CE7;
        color: white;
        font-weight: 700;
        border: none;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #5A49E0;
        border: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 초기화 (Session State)
if "records" not in st.session_state:
    st.session_state["records"] = [
        {"date": "2026-09-24", "category": "휴대폰 사용", "score": 10, "memo": "수업 시간 중 웹서핑"},
        {"date": "2026-09-25", "category": "지각", "score": 10, "memo": "1교시 15분 지각"},
        {"date": "2026-09-26", "category": "수업 중 떠들기", "score": 5, "memo": "짝꿍과 지속적인 대화"}
    ]

# 4. 앱 헤더
st.markdown("""
    <div class="header-card">
        <h1>🔥 쌤 화남 지수표</h1>
        <p>조금 더 바른 행동이 더 좋은 우리 반을 만들어용!</p>
    </div>
""", unsafe_allow_html=True)

# 5. 탭 구성 (이미지 하단 탭바 구조 반영)
tab1, tab2, tab3 = st.tabs(["🏠 홈 / 현황", "✍️ 화남 지수 기록", "📜 학급 규칙"])

# [탭 1] 홈 / 현황
with tab1:
    # 총 화남 지수 계산
    total_score = sum(item["score"] for item in st.session_state["records"])
    
    # 지수에 따른 상태 문구 설정
    if total_score < 15:
        status_msg = "😊 평온함! 아주 좋은 학급 분위기입니다."
    elif total_score < 35:
        status_msg = "⚠️ 주의 필요! 선생님의 눈치가 살짝 보이기 시작해요."
    elif total_score < 60:
        status_msg = "😡 화남 경고! 조심하지 않으면 폭발할 수 있어요!"
    else:
        status_msg = "🚨 위험 단계! 즉각적인 반성과 바른 행동이 필요합니다!"

    st.markdown(f"""
        <div class="stat-card">
            <div style="font-size:16px; font-weight:700; color:#2D3436;">현재 우리반 화남 누적 지수</div>
            <div class="stat-score">{total_score}점</div>
            <div class="stat-status">{status_msg}</div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📋 최근 화남 기록")
    if len(st.session_state["records"]) > 0:
        df = pd.DataFrame(st.session_state["records"])
        df = df.rename(columns={
            "date": "날짜",
            "category": "위반 항목",
            "score": "화남 지수(+점수)",
            "memo": "상세 내용"
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("아직 기록된 화남 지수가 없습니다. 참 잘했어요!")


# [탭 2] 화남 지수 추가/기록하기
with tab2:
    st.subheader("✍️ 선생님 화남 지수 작성하기")
    
    # 프리셋 카테고리 버튼
    st.write("**빠른 사유 선택**")
    col1, col2, col3 = st.columns(3)
    
    preset_cat = None
    preset_score = 5
    
    if col1.button("💬 수업 떠들기 (+5)"):
        preset_cat = "수업 중 떠들기"
        preset_score = 5
    if col2.button("📢 수업 방해 (+5)"):
        preset_cat = "수업 방해 행동"
        preset_score = 5
    if col3.button("⏰ 지각 (+10)"):
        preset_cat = "지각"
        preset_score = 10

    col4, col5, col6 = st.columns(3)
    if col4.button("📱 휴대폰 사용 (+10)"):
        preset_cat = "휴대폰 사용"
        preset_score = 10
    if col5.button("⚠️ 규칙 위반 (+10)"):
        preset_cat = "규칙 위반"
        preset_score = 10
    if col6.button("💬 기타 행동 (+5)"):
        preset_cat = "기타 행동"
        preset_score = 5

    st.divider()

    # 입력 폼
    with st.form("anger_form", clear_on_submit=True):
        category = st.text_input("위반/화난 항목", value=preset_cat if preset_cat else "수업 중 떠들기")
        
        # 화 난 수치 입력 (원하는 수치 적기)
        score = st.slider("선생님 화난 수치 (점수 부과)", min_value=1, max_value=50, value=preset_score, step=1)
        
        memo = st.text_area("상세 내용 (선택사항)", placeholder="예) 수업 시간에 친구와 계속 대화함")
        date_selected = st.date_input("날짜", datetime.date.today())

        submitted = st.form_submit_button("기록하기")

        if submitted:
            if not category.strip():
                st.error("위반 항목을 입력해주세요.")
            else:
                new_record = {
                    "date": str(date_selected),
                    "category": category,
                    "score": score,
                    "memo": memo if memo else "내용 없음"
                }
                st.session_state["records"].insert(0, new_record)
                st.success(f"'{category}' 항목으로 화남 수치 {score}점이 기록되었습니다!")
                st.rerun()


# [탭 3] 학급 규칙 안내
with tab3:
    st.subheader("📜 이런 행동은 선생님을 화나게 해요!")
    
    rules = [
        "1. 수업 시간에 떠들거나 장난치지 않기",
        "2. 수업을 방해하는 행동 하지 않기",
        "3. 정해진 시간 맞춰 지각하지 않기",
        "4. 수업 중 허락 없이 휴대폰 사용하지 않기",
        "5. 기본 학급 규칙 준수하기",
        "6. 기타 선생님이 판단하는 부적절한 행동 자제하기"
    ]
    
    for rule in rules:
        st.markdown(f'<div class="rule-item">{rule}</div>', unsafe_allow_html=True)

    st.info("💡 서로를 배려하고, 더 바른 행동을 함께 만들어가요!")
