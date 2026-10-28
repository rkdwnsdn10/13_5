import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="학교 생활 수칙 무한 경고 사이렌",
    page_icon="🚨",
    layout="centered",
)


# 무한 반복 경고음 제어 자바스크립트 엔진 (Web Audio API)
def control_alarm_sound(action="start", sound_type="siren"):
    js_code = f"""
    <script>
    (function() {{
        try {{
            if (!window.alarmAudioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext
                
