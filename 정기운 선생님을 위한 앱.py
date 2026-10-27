import streamlit as st
import datetime

# ---------------------------------------------------------
# Page Configuration & CSS Styling (학교 일러스트 테마 적용)
# ---------------------------------------------------------
st.set_page_config(
    page_title="정기운 선생님을 위한 Smart Classroom Dashboard",
    page_icon="🏫",
    layout="wide"
)

# 학교 배경 감성 CSS (학교 패턴 및 감성 폰트/카드 디자인)
st.markdown("""
<style>
    /* 학교 교실 분위기의 백그라운드 색상 및 은은한 도트 패턴 */
    .stApp {
        background-color: #f8fafc;
        background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* 대시보드 상단 학교 일러스트 배너 */
    .school-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.2);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .school-banner h1 {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .school-banner p {
        font-size: 1.05rem;
        color: #e0f2fe;
        margin: 0;
    }

    /* 상단 요약 지표 카드 */
    .top-card {
        background: #ffffff;
        border: 2px solid #cbd5e1;
        padding: 18px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: left;
    }
    .top-card-label {
        font-size: 0.9rem;
        color: #475569;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .top-card-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e3a8a;
    }

    /* 학급 알림 박스 카드 */
    .content-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .box-title {
        color: #1e293b;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 18px;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 6px;
        display: inline-block;
    }

    /* 알림 리스트 바 */
    .alert-item-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #f59e0b;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
    .alert-item-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #ef4444;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
    .alert-item-info {
        background-color: #f3e8ff;
        color: #6b21a8;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #a855f7;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 상단 탭 구성 (요청하신 2개 탭만 남김)
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📊 대시보드 메인", "📖 앱 소개 & 사용 설명"])

# ---------------------------------------------------------
# TAB 1: 메인 대시보드
# ---------------------------------------------------------
with tab1:
    # 상단 학교 배너
    st.markdown(f"""
    <div class="school-banner">
        <h1>🏫 1학년 13반 Smart Classroom</h1>
        <p>정기운 선생님을 위한 실시간 학급 관리 통합 대시보드 · {datetime.date.today().strftime("%Y년 %m월 %d일")}</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. 상단 요약 카운터 Card
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="top-card">
            <div class="top-card-label">🔔 오늘 발생 경고음</div>
            <div class="top-card-val">3 회</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="top-card">
            <div class="top-card-label">💌 도착한 마음우체통 편지</div>
            <div class="top-card-val">0 개</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="top-card">
            <div class="top-card-label">⚠️ 벌점 수여 학생</div>
            <div class="top-card-val">2 명</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="top-card">
            <div class="top-card-label">🧹 청소 필요 구역</div>
            <div class="top-card-val">6 곳</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. 하단 알림 피드 & 실시간 현황
    left_col, right_col = st.columns([1.2, 0.8])

    with left_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📢 실시간 학급 주요 알림</div>', unsafe_allow_html=True)
        
        # 청소 알림
        st.markdown("""
        <div class="alert-item-warning">
            <b>🧹 청소 상태 알림</b><br>
            교실 바닥, 책상 주변, 쓰레기통, 분리수거, 칠판·교탁, 창가·사물함 구역 점검이 필요합니다. (청소 완료율: 0%)
        </div>
        """, unsafe_allow_html=True)

        # 벌점 알림
        st.markdown("""
        <div class="alert-item-danger">
            <b>⚠️ 벌점 수여 알림</b><br>
            <b>김철수</b> 학생 (사유: 수업 시간 지각 / 벌점 2점)<br>
            <b>이영희</b> 학생 (사유: 청소 시간 무단 탈주 / 벌점 3점)
        </div>
        """, unsafe_allow_html=True)

        # 우리 반 마음우체통 알림
        st.markdown("""
        <div class="alert-item-info">
            <b>💌 우리 반 마음우체통 알림</b><br>
            현재 도착한 익명 편지가 없습니다.
        </div>
        """, unsafe_allow_html=True)

        # 경고음 알림
        st.markdown("""
        <div class="alert-item-warning">
            <b>🔔 경고음 발생 알림</b><br>
            오늘 수업 시간 집중 유도 경고음이 총 <b>3회</b> 발생했습니다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📋 4대 학급 기능 항목 요약</div>', unsafe_allow_html=True)

        st.markdown("""
        * **🔔 경고음 카운트**: `3회` 누적
        * **⚠️ 벌점 관리**: `2명` 부과
        * **💌 우리 반 마음우체통**: `0건` 미확인
        * **🧹 청소 평가**: `6구역` 점검 필요 (완료율 `0%`)
        """)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("💡 주요 실시간 현황은 알림 피드 및 옆의 사용 설명 탭을 참고해 주세요.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: 앱 소개 & 사용 설명
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown('<div class="box-title">💌 정기운 선생님께 드리는 글</div>', unsafe_allow_html=True)
    
    st.success("""
    ### 👋 매일 학생들을 챙기느라 바쁘신 정기운 선생님!

    저희가 선생님을 위해 선생님을 돕는 앱을 만들었어요.  
    이 앱을 선생님이 잘 이용해 주시기를 바래요.

    이 앱은 총 4가지 기능이 있고 선생님의 필요에 따라 페이지에 들어가서 사용하시면 돼요.  
    잘 사용 하시길 바래요. ✨
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="box-title">📖 앱의 4가지 주요 기능 및 활용법</div>', unsafe_allow_html=True)

    st.markdown("""
    1. **🔔 경고음 기능**: 하루 동안 작동된 집중 유도 경고음 누적 횟수를 모니터링합니다.
    2. **📋 벌점제도 기능**: 벌점을 받은 학생 수와 구체적인 사유를 한눈에 확인합니다.
    3. **💌 우리 반 마음우체통 기능**: 학생들이 보낸 익명 고민/건의/칭찬 편지 수량을 확인합니다.
    4. **🧹 청소 상태 체크 기능**: 교실 6개 구역의 청소 상태 및 완료율을 체크합니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
