import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="실시간 음성 항시 감지 무한 사이렌",
    page_icon="🚨",
    layout="centered",
)

# 세션 이력 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []
if "last_detected" not in st.session_state:
    st.session_state.last_detected = ""

st.title("🚨 실시간 음성 항시 감지 & 무한 사이렌")
st.caption(
    "마이크를 켜두면 항상 켜진 상태로 음성을 분석하며, 욕설 감지 시 끄기 전까지 사이렌이 계속 울립니다."
)

# 사이드바 설정
st.sidebar.header("⚙️ 음성 감지 규칙 설정")
banned_words_input = st.sidebar.text_input(
    "🚫 감지할 욕설/금지어 목록 (쉼표 구분)",
    value="바보, 멍청이, 짜증, 씨발, 개새끼, 미친, 시발, 좆",
)
banned_words = [w.strip() for w in banned_words_input.split(",") if w.strip()]

# 자바스크립트 전용 배열 포맷 변환
banned_words_js = str(banned_words)

# ---------------------------------------------------------
# 통합 항시 음성 감지 & 무한 사이렌 자바스크립트 엔진
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
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            margin: 5px;
        }}
        .btn-stop {{
            background-color: #333333;
        }}
        .status-box {{
            font-size: 17px;
            font-weight: bold;
            margin: 15px 0;
            padding: 10px;
            border-radius: 5px;
            background: #ffffff;
            border: 1px solid #ffccd5;
            color: #d90429;
        }}
        .transcript-box {{
            margin-top: 10px;
            padding: 10px;
            background: #fafafa;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            color: #222;
            min-height: 45px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>🎙️ 실시간 마이크 항시 감지 및 알림</h3>
        <button id="startBtn" class="btn" onclick="startContinuousListening()">▶️ 마이크 항시 감지 시작</button>
        <button id="stopAlarmBtn" class="btn btn-stop" onclick="stopAlarmSound()">🛑 경고음 끄기 (소리 정지)</button>
        
        <div id="status" class="status-box">상태: 감지 대기 중 (시작 버튼을 눌러주세요)</div>
        <div id="transcript" class="transcript-box">마이크로 하시는 말씀이 여기에 실시간으로 표시됩니다...</div>
    </div>

    <script>
        let recognition = null;
        let isListening = false;
        let alarmInterval = null;
        let audioCtx = null;
        const bannedWords = {banned_words_js};

        // 연속 사이렌 오디오 발령
        function triggerSirenLoop() {{
            if (!audioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) audioCtx = new AudioContext();
            }}
            if (audioCtx && audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}

            if (alarmInterval) return; // 이미 울리고 있다면 중복 방지

            function playSirenTone() {{
                if (!audioCtx) return;
                const masterGain = audioCtx.createGain();
                masterGain.gain.setValueAtTime(1.0, audioCtx.currentTime);
                masterGain.connect(audioCtx.destination);

                [600, 900, 1200].forEach((baseFreq, i) => {{
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = i % 2 === 0 ? 'sawtooth' : 'square';

                    osc.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 600, audioCtx.currentTime + 0.3);
                    osc.frequency.linearRampToValueAtTime(baseFreq, audioCtx.currentTime + 0.6);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 600, audioCtx.currentTime + 0.9);

                    gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
                    osc.connect(gain);
                    gain.connect(masterGain);

                    osc.start(audioCtx.currentTime);
                    osc.stop(audioCtx.currentTime + 0.95);
                }});
            }}

            playSirenTone();
            alarmInterval = setInterval(playSirenTone, 1000); // 1초 간격 무한 반복
        }}

        // 사이렌 정지
        function stopAlarmSound() {{
            if (alarmInterval) {{
                clearInterval(alarmInterval);
                alarmInterval = null;
            }}
            if (audioCtx) {{
                audioCtx.suspend();
            }}
            document.getElementById('status').innerText = isListening ? "상태: 🟢 마이크 항시 감지 중..." : "상태: 감지 대기 중";
            document.getElementById('status').style.color = isListening ? "green" : "#d90429";
        }}

        // 실시간 항시 음성 감지
        function startContinuousListening() {{
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert("이 브라우저는 음성 인식을 지원하지 않습니다. Chrome(크롬) 브라우저를 이용해 주세요.");
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
                document.getElementById('status').innerText = "상태: 🟢 마이크 항시 감지 중... (욕설을 말하면 사이렌이 울립니다)";
                document.getElementById('status').style.color = "green";
                document.getElementById('startBtn').disabled = true;
            }};

            recognition.onresult = function(event) {{
                let currentText = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    currentText += event.results[i][0].transcript;
                }}
                document.getElementById('transcript').innerText = "인식된 음성: " + currentText;

                // 욕설 단어 감지 검사
                for (let word of bannedWords) {{
                    if (currentText.includes(word)) {{
                        document.getElementById('status').innerText = "🚨 [비상] 욕설 감지됨: " + word + " (소리 정지를 누르세요)";
                        document.getElementById('status').style.color = "red";
                        triggerSirenLoop(); // 무한 사이렌 가동
                        break;
                    }}
                }}
            }};

            recognition.onerror = function(event) {{
                console.log("Speech Recognition Error:", event.error);
            }};

            // 마이크 끊김 방지 - 항상 다시 켜기 (Always-On)
            recognition.onend = function() {{
                if (isListening) {{
                    try {{
                        recognition.start();
                    }} catch(e) {{
                        console.log("Restarting listening...", e);
                    }}
                }}
            }};

            recognition.start();
        }}
    </script>
</body>
</html>
"""

components.html(full_engine_html, height=310)

# ---------------------------------------------------------
# 수동 발령 및 이력 입력 영역
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📝 수동 이력 기록 및 텍스트 검사")

manual_text = st.text_input(
    "🗣️ 직접 텍스트로 테스트하거나 기록할 내용 작성",
    placeholder="예: 바보라고 말했을 때 이력 저장 테스트...",
)

if st.button("🔍 텍스트 감지 테스트", type="primary"):
    if manual_text:
        detected = [w for w in banned_words if w in manual_text]
        if detected:
            st.error(f"🚨 **[욕설 감지]**: `{', '.join(detected)}` 단어가 포착되었습니다.")
            log_time = time.strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.detection_logs.insert(
                0,
                {
                    "시각": log_time,
                    "입력 내용": manual_text,
                    "감지 단어": ", ".join(detected),
                    "상태": "🚨 사이렌 발령",
                },
            )
        else:
            st.success("✅ 감지된 금지어가 없습니다.")

# 이력 대시보드
st.markdown("---")
st.subheader("📜 실시간 음성 감지 기록 이력")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 이력 전체 초기화"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 감지된 이력이 없습니다.")
