import streamlit as st
import datetime
import requests

# ---------------------------------------------------------
# Page Configuration & Warm Aesthetics CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="정기운 선생님을 위한 Smart Classroom Dashboard",
    page_icon="🏫",
    layout="wide"
)

st.markdown("""
<style>
    /* 1. 전체 배경: 따뜻한 파스텔 그래디언트 (아이보리~피치 샌드 톤) */
    .stApp {
        background: linear-gradient(135deg, #fdfbf7 0%, #f5efe6 50%, #eef2e6 100%);
        background-attachment: fixed;
    }
    
    /* 2. 상단 메인 배너: 따뜻한 오렌지 테라코타 그래디언트 */
    .school-banner {
        background: linear-gradient(135deg, #e07a5f 0%, #f4a261 100%);
        color: white;
        padding: 28px 24px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 20px -5px rgba(224, 122, 95, 0.25);
        margin-bottom: 24px;
    }
    .school-banner h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .school-banner p {
        font-size: 1.05rem;
        color: #fff3eb;
        margin: 0;
        font-weight: 500;
    }

    /* 3. 상단 핵심 지표 카드 (따뜻한 부드러운 흰색 카드) */
    .top-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border: 1px solid #eadbc8;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(180, 150, 120, 0.08);
        text-align: left;
        transition: transform 0.2s ease;
    }
    .top-card-label {
        font-size: 0.95rem;
        color: #7f5539;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .top-card-val {
        font-size: 1.9rem;
        font-weight: 800;
        color: #9c6644;
    }

    /* 4. 메인 컨텐츠 박스 */
    .content-box {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e6ccb2;
        box-shadow: 0 6px 15px rgba(180, 150, 120, 0.07);
        margin-bottom: 20px;
    }
    .box-title {
        color: #6b705c;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 18px;
        border-bottom: 3px solid #ddbea9;
        padding-bottom: 8px;
        display: inline-block;
    }

    /* 5. 따뜻한 톤 알림 카드들 */
    .alert-item-warning {
        background-color: #fff3b0;
        color: #7f5539;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #e76f51;
        margin-bottom: 12px;
        font-size: 0.98rem;
    }
    .alert-item-danger {
        background-color: #ffe5d9;
        color: #9d0208;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #d00000;
        margin-bottom: 12px;
        font-size: 0.98rem;
    }
    .alert-item-info {
        background-color: #f0efeb;
        color: #432818;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #99582a;
        margin-bottom: 12px;
        font-size: 0.98rem;
    }
    .alert-item-success {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #66bb6a;
        margin-bottom: 12px;
        font-size: 0.98rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Cloud DB API Helper Functions
# ---------------------------------------------------------
JSONBIN_URL = "https://api.jsonbin.io/v3/b/66fa1e17e41b4d34e439f012"

def load_cloud_data():
    try:
        res = requests.get(JSONBIN_URL, headers={"X-Bin-Meta": "false"}, timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {
        "alarm_count": 0,
        "demerits": [],
        "anonymous_letters": [],
        "cleaning_zones": {
            "교실 바닥": "확인 필요", "책상 주변": "확인 필요", "쓰레기통": "확인 필요",
            "분리수거": "확인 필요", "칠판·교탁": "확인 필요", "창가·사물함": "확인 필요"
        }
    }

# 데이터 실시간 로드
cloud_data = load_cloud_data()
st.session_state["alarm_count"] = cloud_data.get("alarm_count", 0)
st.session_state["demerits"] = cloud_data.get("demerits", [])
st.session_state["anonymous_letters"] = cloud_data.get("anonymous_letters", [])
st.session_state["cleaning_zones"] = cloud_data.get("cleaning_zones", {})

# ---------------------------------------------------------
# 메인 대시보드 UI
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🌾 메인 대시보드", "☕ 앱 소개 & 사용 설명"])

with tab1:
    st.markdown(f"""
    <div class="school-banner">
        <h1>🏫 1학년 13반 Warm Classroom</h1>
        <p>정기운 선생님을 위한 실시간 학급 관리 통합 대시보드 · {datetime.date.today().strftime("%Y년 %m월 %d일")}</p>
    </div>
    """, unsafe_allow_html=True)

    # 청소 상태 연동
    total_zones = len(st.session_state["cleaning_zones"])
    clean_zones = [z for z, status in st.session_state["cleaning_zones"].items() if status == "깨끗함"]
    needed_zones = [z for z, status in st.session_state["cleaning_zones"].items() if status == "확인 필요"]
    completion_rate = int((len(clean_zones) / total_zones) * 100) if total_zones > 0 else 0

    # 상단 요약 카운터
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="top-card">
            <div class="top-card-label">🔔 오늘 발생 경고음</div>
            <div class="top-card-val">{st.session_state['alarm_count']} 회</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="top-card">
            <div class="top-card-label">💌 도착한 익명 편지</div>
            <div class="top-card-val">{len(st.session_state['anonymous_letters'])} 개</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="top-card">
            <div class="top-card-label">⚠️ 벌점 수여 학생</div>
            <div class="top-card-val">{len(st.session_state['demerits'])} 명</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="top-card">
            <div class="top-card-label">🧹 청소 필요 구역</div>
            <div class="top-card-val">{len(needed_zones)} 곳</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 하단 알림 피드
    left_col, right_col = st.columns([1.2, 0.8])

    with left_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📢 실시간 학급 주요 알림</div>', unsafe_allow_html=True)
        
        # 1) 청소 상태
        if needed_zones:
            zones_str = ", ".join(needed_zones)
            st.markdown(f"""
            <div class="alert-item-warning">
                <b>🧹 청소 상태 알림</b><br>
                {zones_str} 구역 점검이 필요합니다. (청소 완료율: {completion_rate}%)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-item-success">
                <b>🧹 청소 완료 알림</b><br>
                모든 구역 청소가 '깨끗함' 상태입니다! (완료율 100%)
            </div>
            """, unsafe_allow_html=True)

        # 2) 벌점 내역
        if st.session_state["demerits"]:
            demerit_details = "<br>".join([f"<b>{d.get('학생','미상')}</b> 학생 (사유: {d.get('사유','-')} / 벌점 {d.get('벌점',1)}점)" for d in st.session_state["demerits"]])
            st.markdown(f"""
            <div class="alert-item-danger">
                <b>⚠️ 벌점 수여 알림</b><br>
                {demerit_details}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-item-success">
                <b>⚠️ 벌점 관리 현황</b><br>
                현재 부과된 벌점 내역이 없습니다.
            </div>
            """, unsafe_allow_html=True)

        # 3) 익명 편지
        letter_count = len(st.session_state["anonymous_letters"])
        if letter_count > 0:
            latest = st.session_state["anonymous_letters"][-1]
            st.markdown(f"""
            <div class="alert-item-info">
                <b>💌 익명소통함 알림</b><br>
                새로운 편지가 총 <b>{letter_count}건</b> 도착했습니다! (최신: [{latest.get('category','의견')}] "{latest.get('content','')[:25]}...")
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-item-info">
                <b>💌 익명소통함 알림</b><br>
                현재 도착한 익명 편지가 없습니다.
            </div>
            """, unsafe_allow_html=True)

        # 4) 경고음 발생
        st.markdown(f"""
        <div class="alert-item-warning">
            <b>🔔 경고음 발생 알림</b><br>
            오늘 수업 시간 집중 유도 경고음이 총 <b>{st.session_state['alarm_count']}회</b> 발생했습니다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📋 4대 학급 기능 항목 요약</div>', unsafe_allow_html=True)

        st.markdown(f"""
        * **🔔 경고음 카운트**: `{st.session_state['alarm_count']}회` 누적
        * **⚠️ 벌점 관리**: `{len(st.session_state['demerits'])}명` 부과
        * **💌 익명소통함**: `{len(st.session_state['anonymous_letters'])}건` 수신
        * **🧹 청소 평가**: `{len(needed_zones)}구역` 점검 필요 (완료율 `{completion_rate}%`)
        """)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🔄 대시보드 실시간 새로고침", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown('<div class="box-title">💌 정기운 선생님께 드리는 글</div>', unsafe_allow_html=True)
    st.success("""
    ### 👋 매일 학생들을 챙기느라 바쁘신 정기운 선생님!

    저희가 선생님을 위해 선생님을 돕는 앱을 만들었어요.  
    이 앱을 선생님이 잘 이용해 주시기를 바래요.

    이 앱은 총 4가지 기능이 있고 선생님의 필요에 따라 좌측 사이드바 메뉴에 들어가서 사용하시면 돼요.  
    잘 사용 하시길 바래요. ✨
    """)
    st.markdown('</div>', unsafe_allow_html=True)
