import streamlit as st
import datetime

# ---------------------------------------------------------
# Page Configuration & CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="정기운 선생님을 위한 Smart Classroom Dashboard",
    page_icon="🏫",
    layout="wide"
)

# 네이비/블루 대시보드 톤 맞춤 CSS 적용
st.markdown("""
<style>
    /* 배경색 및 기본 폰트 설정 */
    .main {
        background-color: #f4f7fa;
    }
    
    /* 대시보드 상단 헤더 타이틀 */
    .dash-header {
        text-align: center;
        color: #1a2b4c;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    .dash-sub {
        text-align: center;
        color: #5a6b82;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }

    /* 상단 네이비 카드 스타일 */
    .top-card {
        background-color: #1e3a8a;
        color: white;
        padding: 18px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        text-align: left;
    }
    .top-card-label {
        font-size: 0.9rem;
        color: #bfdbfe;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .top-card-val {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffffff;
    }

    /* 하단 대시보드 섹션 카드 박스 */
    .content-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        height: 100%;
    }
    .box-title {
        color: #1e293b;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 6px;
        display: inline-block;
    }

    /* 알림 리스트 아이템 */
    .alert-item-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 12px 15px;
        border-radius: 8px;
        border-left: 5px solid #f59e0b;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    .alert-item-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 12px 15px;
        border-radius: 8px;
        border-left: 5px solid #ef4444;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    .alert-item-info {
        background-color: #e0f2fe;
        color: #075985;
        padding: 12px 15px;
        border-radius: 8px;
        border-left: 5px solid #0284c7;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 화면 상단 탭 구성
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📊 대시보드 메인", "💌 앱 소개 & 사용 방법"])

# ---------------------------------------------------------
# TAB 1: 고급 네이비 스타일 메인 대시보드
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="dash-header">대 시 보 드</div>', unsafe_allow_html=True)
    # 1학년 13반으로 수정 적용 부분
    st.markdown(f'<div class="dash-sub">1학년 13반 · {datetime.date.today().strftime("%Y년 %m월 %d일")} 현재 · 정기운 선생님을 위한 실시간 통합 알림센터</div>', unsafe_allow_html=True)

    # 1. 상단 블루 요약 카운터
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
            <div class="top-card-label">📮 도착한 익명 편지</div>
            <div class="top-card-val">3 개</div>
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

    # 2. 하단 알림 및 관리 현황 구획
    left_col, right_col = st.columns([1.2, 0.8])

    with left_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📢 실시간 학급 주요 알림</div>', unsafe_allow_html=True)
        
        # 청소 알림
        st.markdown("""
        <div class="alert-item-warning">
            <b>🧹 청소 상태 알림</b><br>
            교실 바닥, 책상 주변, 쓰레기통, 분리수거, 칠판·교탁, 창가·사물함 구역 확인이 필요합니다. (완료율 0%)
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

        # 익명 소통함 알림
        st.markdown("""
        <div class="alert-item-info">
            <b>📮 익명 편지 알림</b><br>
            새로운 편지 3건 도착: "선생님 항상 수업 재미있게 해주셔서 감사합니다!..."
        </div>
        """, unsafe_allow_html=True)

        # 경고음 알림
        st.markdown("""
        <div class="alert-item-warning">
            <b>🔔 경고음 발생 알림</b><br>
            오늘 수업 시간 집중 유도 경고음이 총 <b>3회</b> 누적되었습니다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📋 4대 학급 기능 항목 요약</div>', unsafe_allow_html=True)

        st.markdown("""
        * **🔔 경고음 카운트**: `3회` (주의)
        * **⚠️ 벌점 관리**: `2명` 등록 완료
        * **📮 익명 편지**: `3건` 미확인
        * **🧹 청소 평가**: `6구역` 점검 필요
        """)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("💡 각 기능의 상세 내역은 알림 피드 및 앱 소개 탭을 참고하세요.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: 정기운 선생님 앱 소개 및 사용 설명
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
    1. **🔔 경고음 기능**
       - 수업 집중이 필요하거나 경고가 필요한 순간 작동된 하루 경고음 누적 횟수를 모니터링합니다.
    2. **📋 벌점제도 기능**
       - 벌점을 받은 학생이 몇 명인지, 어떤 학생이 어떤 사유로 벌점을 받았는지 한눈에 파악합니다.
    3. **📮 익명소통함 기능**
       - 학생들이 마음을 담아 보낸 익명 편지 수량을 실시간 알림으로 확인합니다.
    4. **🧹 청소 상태 체크 기능**
       - 교실 구역별 청소 필요 유무와 완료율을 대시보드 알림 형태로 체크합니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
