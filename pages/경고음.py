import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="학교 생활 수칙 음성 & 원클릭 경고 사이렌",
    page_icon="🚨",
    layout="centered",
)

# 세션 이력 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

st.title("🚨 학교 생활 수칙 음성 & 원클릭 경고 사이렌")
st.caption(
    "마이크 감지를 켜고 끌 수 있으며, 욕설 자동 감지 및 9대 수칙 원클릭 경고를 제공합니다."
)

# 사이드바 설정
st.sidebar.header("⚙️ 음성 감지 설정")
banned_words_input = st.sidebar.text_input(
    "🚫 자동 감지 욕설/유사발음 목록 (쉼표 구분)",
    value="씨발, 시발, 십팔, 개새끼, 미친, 바보, 빡통, 좆, 닥쳐",
)
banned_words = [w.strip() for w in banned_words_input.split(",") if w.strip()]
banned_words_js = str(banned_words)

# ---------------------------------------------------------
# 마이크 ON/OFF 스위치 및 무한 사이렌 통합 엔진
# ---------------------------------------------------------
full_engine_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        .container {{
            border: 2px solid #FF4B4B;
            border-radius: 10px;
            padding: 20px;
            background-color: #FFF5F5;
            text-align: center;
            font-family: 'Malgun Gothic', sans-serif;
        }}
        .btn {{
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            margin: 4px;
        }}
        .btn-start {{
            background-color: #2b8a3e;
        }}
        .btn-pause {{
            background-color: #fd7e14;
        }}
        .btn-siren {{
            background-color: #e03131;
        }}
        .btn-stop {{
            background-color: #343a40;
        }}
        .status-box {{
            font-size: 16px;
            font-weight: bold;
            margin: 15px 0;
            padding: 12px;
            border-radius: 6px;
            background: #ffffff;
            border: 1px solid #ffccd5;
            color: #d90429;
        }}
        .transcript-box {{
            margin-top: 10px;
            padding: 10px;
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            color: #222;
            min-height: 40px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>🎙️ 실시간 마이크 음성 감지 컨트롤러</h3>
        
        <button id="startBtn" class="btn btn-start" onclick="startContinuousListening()">▶️ 마이크 감지 켜기 (ON)</button>
        <button id="pauseBtn" class="btn btn-pause" onclick="stopContinuousListening()" disabled>⏸️ 마이크 감지 끄기 (OFF)</button>
        <button id="triggerManualBtn" class="btn btn-siren" onclick="triggerSirenLoop('수동 사이렌 발령')">🚨 비상 사이렌 켜기</button>
        <button id="stopAlarmBtn" class="btn btn-stop" onclick="stopAlarmSound()">🛑 경고음 끄기 (소리 정지)</button>
        
        <div id="status" class="status-box">상태: ⚪ 마이크가 꺼져 있습니다 ('▶️ 마이크 감지 켜기'를 누르세요)</div>
        <div id="transcript" class="transcript-box">마이크 인식 내용이 여기에 실시간으로 표시됩니다...</div>
    </div>

    <script>
        let recognition = null;
        let isListening = false;
        let alarmInterval = null;
        let audioCtx = null;

        const bannedWords = {banned_words_js};

        const CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
        function getHangulChosung(str) {{
            let result = "";
            for (let i = 0; i < str.length; i++) {{
                let code = str.charCodeAt(i) - 44032;
                if (code >= 0 && code <= 11172) {{
                    result += CHO[Math.floor(code / 588)];
                }} else {{
                    result += str.charAt(i);
                }}
            }}
            return result;
        }}

        function checkSimilarPronunciation(input, target) {{
            const cleanInput = input.split(' ').join('');
            const cleanTarget = target.split(' ').join('');
            
            if (cleanInput.includes(cleanTarget)) return true;

            const inputCho = getHangulChosung(cleanInput);
            const targetCho = getHangulChosung(cleanTarget);
            
            if (inputCho.includes(targetCho) && targetCho.length >= 2) {{
                return true;
            }}
            return false;
        }}

        function triggerSirenLoop(reason) {{
            if (!audioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) audioCtx = new AudioContext();
            }}
            if (audioCtx && audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}

            document.getElementById('status').innerText = "🚨 [비상 경고 사이렌 작동 중]: " + reason;
            document.getElementById('status').style.color = "red";

            if (alarmInterval) return;

            function playSirenTone() {{
                if (!audioCtx) return;
                const masterGain = audioCtx.createGain();
                masterGain.gain.setValueAtTime(1.0, audioCtx.currentTime);
                masterGain.connect(audioCtx.destination);

                [650, 1000, 1350].forEach((baseFreq, i) => {{
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = i % 2 === 0 ? 'sawtooth' : 'square';

                    osc.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 650, audioCtx.currentTime + 0.3);
                    osc.frequency.linearRampToValueAtTime(baseFreq, audioCtx.currentTime + 0.6);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 650, audioCtx.currentTime + 0.9);

                    gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
                    osc.connect(gain);
                    gain.connect(masterGain);

                    osc.start(audioCtx.currentTime);
                    osc.stop(audioCtx.currentTime + 0.95);
                }});
            }}

            playSirenTone();
            alarmInterval = setInterval(playSirenTone, 1000);
        }}

        function stopAlarmSound() {{
            if (alarmInterval) {{
                clearInterval(alarmInterval);
                alarmInterval = null;
            }}
            if (audioCtx) {{
                audioCtx.suspend();
            }}
            document.getElementById('status').innerText = isListening ? "상태: 🟢 마이크 켜짐 (욕설 감지 활성화)" : "상태: ⚪ 마이크가 꺼져 있습니다";
            document.getElementById('status').style.color = isListening ? "green" : "#343a40";
        }}

        // 마이크 감지 켜기 (ON)
        function startContinuousListening() {{
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert("Chrome(크롬) 브라우저에서 사용해 주세요.");
                return;
            }}

            if (!audioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) audioCtx = new AudioContext();
            }}
            if (audioCtx && audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}

            recognition = new SpeechRecognition();
            recognition.lang = 'ko-KR';
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = function() {{
                isListening = true;
                document.getElementById('status').innerText = "상태: 🟢 마이크 켜짐 (욕설 감지 활성화)";
                document.getElementById('status').style.color = "green";
                document.getElementById('startBtn').disabled = true;
                document.getElementById('pauseBtn').disabled = false;
            }};

            recognition.onresult = function(event) {{
                let currentText = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    currentText += event.results[i][0].transcript;
                }}
                document.getElementById('transcript').innerText = "🗣️ 인식된 음성: " + currentText;

                for (let word of bannedWords) {{
                    if (checkSimilarPronunciation(currentText, word)) {{
                        triggerSirenLoop("욕설/유사발음 포착 ('" + word + "')");
                        return;
                    }}
                }}
            }};

            recognition.onerror = function(event) {{
                console.log("Speech Error:", event.error);
            }};

            recognition.onend = function() {{
                if (isListening) {{
                    try {{
                        recognition.start();
                    }} catch(e) {{
                        console.log("Restarting speech...", e);
                    }}
                }}
            }};

            recognition.start();
        }}

        // 마이크 감지 끄기 (OFF)
        function stopContinuousListening() {{
            isListening = false;
            if (recognition) {{
                recognition.stop();
            }}
            document.getElementById('status').innerText = "상태: ⚪ 마이크가 꺼져 있습니다";
            document.getElementById('status').style.color = "#343a40";
            document.getElementById('startBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = true;
        }}
    </script>
</body>
</html>
"""

components.html(full_engine_html, height=310)

# ---------------------------------------------------------
# 학교 규칙 위반 원클릭 경고음 버튼 영역 (9개 수칙)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📢 학교 수칙 위반 원클릭 경고 버튼")
st.caption(
    "위반 수칙 버튼을 누르면 이력에 즉시 기록되며, 화면 상단의 비상 사이렌이 울립니다."
)


def log_violation(rule_name):
    log_time = time.strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.detection_logs.insert(
        0,
        {
            "시각": log_time,
            "위반 수칙": rule_name,
            "상태": "🚨 사이렌 발령",
        },
    )


col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "🚬 교내 무단 흡연!", use_container_width=True, type="primary"
    ):
        log_violation("🚬 교내 무단 흡연")
        st.warning(
            "🚨 '교내 무단 흡연' 사이렌이 발령되었습니다. 상단 오디오 판의 '🚨 비상 사이렌 켜기'를 누르면 사이렌이 지속 발령됩니다."
        )

    st.write("")

    if st.button("📱 수업 중 스마트폰!", use_container_width=True):
        log_violation("📱 수업 중 스마트폰 무단 사용")
        st.info("🚨 '스마트폰 무단 사용' 위반이 기록되었습니다.")

    st.write("")

    if st.button("🏃‍♂️ 복도 질주 / 소란!", use_container_width=True):
        log_violation("🏃‍♂️ 복도 질주 및 소란")
        st.info("🚨 '복도 질주 및 소란' 위반이 기록되었습니다.")

with col2:
    if st.button(
        "🏃‍♀️ 무단 외출 / 월담!", use_container_width=True, type="primary"
    ):
        log_violation("🏃‍♀️ 무단 외출 및 월담")
        st.warning("🚨 '무단 외출 / 월담' 위반이 기록되었습니다.")

    st.write("")

    if st.button(
        "👊 교내 폭력 / 위협!", use_container_width=True, type="primary"
    ):
        log_violation("👊 교내 폭력 및 위협")
        st.warning("🚨 '교내 폭력 및 위협' 위반이 기록되었습니다.")

    st.write("")

    if st.button("🔨 공공 기물 파손!", use_container_width=True):
        log_violation("🔨 공공 기물 파손 및 낙서")
        st.info("🚨 '기물 파손' 위반이 기록되었습니다.")

with col3:
    if st.button("📝 시험 부정행위!", use_container_width=True):
        log_violation("📝 시험 중 부정행위(커닝)")
        st.info("🚨 '시험 부정행위' 위반이 기록되었습니다.")

    st.write("")

    if st.button("🛑 교사 지시 불응!", use_container_width=True):
        log_violation("🛑 교사 지시 불응 및 수업 방해")
        st.info("🚨 '지시 불응' 위반이 기록되었습니다.")

    st.write("")

    if st.button("👔 교복 / 용의 미흡!", use_container_width=True):
        log_violation("👔 교복 및 용의 복장 위반")
        st.info("🚨 '복장 위반' 위반이 기록되었습니다.")

# ---------------------------------------------------------
# 위반 이력 리포트 (Pandas)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📜 실시간 수칙 위반 기록 이력")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 이력 전체 초기화"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 기록된 위반 이력이 없습니다.")
