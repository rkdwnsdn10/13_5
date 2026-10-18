import datetime
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="정기운 선생님 통합 대시보드",
    page_icon="🔔",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 모바일 알림판 느낌을 주기 위한 커스텀 CSS 스타일 적용
st.markdown(
    """
    <style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 25px;
    }
    .notification-card {
        background-color: #F3F4F6;
        border-left: 5px solid #3B82F6;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .notification-title {
        font-weight: bold;
        color: #1F2937;
        font-size: 15px;
    }
    .notification-time {
        font-size: 12px;
        color: #9CA3AF;
        margin-top: 4px;
    }
    .notification-content {
        font-size: 14px;
        color: #4B5563;
        margin-top: 6px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 상단 타이틀 영역
st.markdown(
    '<div class="main-header">🔔 정기운 선생님 알림 & 대시보드</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="sub-header">실시간 시스템 알림 및 사용량 모니터링 (기준 날짜: {datetime.date.today().strftime("%Y-%m-%d")})</div>',
    unsafe_allow_html=True,
)

# 예외 처리 블록 시작
try:
    # 1. 상단 요약 지표 (사용 횟수 및 상태)
    st.markdown("### 📊 주요 사용량 요약")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="오늘 출석체크 조회", value="42회", delta="+5회 (어제 대비)"
        )

    with col2:
        st.metric(label="AI 학습 자료 생성", value="12회", delta="2회 대기중")

    with col3:
        st.metric(label="학부모 상담 알림", value="5건", delta="-1건")

    st.markdown("---")

    # 2. 스마트폰 알림 미리보기 보드 (메인 기능)
    st.markdown("### 📱 스마트폰 알림 피드 (미리보기 보드)")
    st.markdown(
        "<p style='font-size: 13px; color: #6B7280;'>기능 페이지로 이동하지 않고 최신 알림 내용을 바로 확인할 수 있습니다.</p>",
        unsafe_allow_html=True,
    )

    # 알림 데이터 리스트 (가상의 데이터)
    notifications = [
        {
            "title": "🚨 [긴급] 학부모 상담 요청",
            "time": "10분 전",
            "content": (
                "김민수 학생 학부모님께서 오후 4시 전화 상담을 요청하셨습니다."
            ),
        },
        {
            "title": "📌 [공지] 과제 제출 마감 알림",
            "time": "1시간 전",
            "content": (
                "3학년 2반 수학 수행평가 과제 제출 마감이 내일 자정으로"
                " 설정되었습니다."
            ),
        },
        {
            "title": "✨ [시스템] AI 문제 생성 완료",
            "time": "3시간 전",
            "content": (
                "요청하신 국어 영역 단원 평가 문제 10문항이 성공적으로"
                " 생성되었습니다."
            ),
        },
        {
            "title": "☕ [휴식] 리프레시 알림",
            "time": "5시간 전",
            "content": (
                "연속으로 2시간 동안 화면을 보고 계십니다. 잠시 눈의 피로를"
                " 풀어주세요."
            ),
        },
    ]

    # 알림 카드 렌더링
    for noti in notifications:
        st.markdown(
            f"""
            <div class="notification-card">
                <div class="notification-title">{noti['title']}</div>
                <div class="notification-time">{noti['time']}</div>
                <div class="notification-content">{noti['content']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. 추가 부가 정보 (사용량 추이 그래프)
    st.markdown("### 📈 주간 기능별 사용 횟수 통계")
    chart_data = {"월": 15, "화": 22, "수": 30, "목": 25, "금": 42}
    st.bar_chart(chart_data)

except Exception as e:
    st.error(
        f"앱을 실행하는 동안 오류가 발생했습니다. 관리자에게 문의해주세요. (오류 내용:"
        f" {e})"
    )

# 하단 푸터
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #9CA3AF; font-size: 12px;'>©"
    " 2026 Jeong Gi-un Teacher Dashboard. All rights reserved.</p>",
    unsafe_allow_html=True,
)
