import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="실시간 음성 욕설 자동 감지기", page_icon="🚨", layout="centered"
)

# 세션 이력 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

st.title("🚨 실시간 음성 욕설 & 금지어 자동 감지기")
st.caption(
    "마이크를 켜두면 브라우저가 음성을 실시간 분석하여 욕설 감지 시 즉시 사이렌이 울립니다."
)

# 사이드바 설정
st.sidebar.header("⚙️ 음성 감지 규칙 설정")
banned_words_input = st.sidebar.text_input(
    "🚫 감지할 욕설/금지어 (쉼표 구분)",
    value="바보, 멍청이, 짜증, 씨발, 개새끼, 미친",
)
banned_words = [w.strip() for w in banned_words_input.split(",") if w.strip()]

st.sidebar.info(
    "💡 마이크 음성 인식이 활성화되면 말을 할 때마다 실시간으로 욕설 여부를 검사합니다."
)

# 자바스크립트 기반 실시간 음성 인식(Web Speech API) & 오디오 합성 엔진
banned_words_js = str(banned_words)

speech_and_sound_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        .container {{
            border: 2px solid #FF4B4B;
            border-radius: 10px;
            padding: 15px;
            background-color: #FFF5F5;
            text-align: center;
            font-family: sans-serif;
        }}
        .btn {{
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }}
        .btn-stop {{
            background-color: #555555;
        }}
        .status {{
            font-weight: bold;
            margin-top: 10px;
            color: #333;
        }}
        .transcript-box {{
            margin-top: 10px;
            padding: 10px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            min-height: 40px;
            color: #111;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>🎙️ 실시간 음성 모니터링</h3>
        <button id="startBtn" class="btn" onclick="startRecognition()">▶️ 음성 자동 감지 시작</button>
        <button id="stopBtn" class="btn btn-stop" onclick="stopRecognition()" disabled>⏹️ 감지 중지</button>
        <div id="status" class="status">상태: 대기 중</div>
        <div id="transcript" class="transcript-box">마이크 버튼을 누르고 말씀하세요...</div>
    </div>

    <script>
        let recognition = null;
        let isListening = false;
        const bannedWords = {banned_words_js};

        // 오디오 사이렌 발생 함수
        function playSiren() {{
            try {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (!AudioContext) return;
                const ctx = new AudioContext();
                if (ctx.state === 'suspended') {{
                    ctx.resume();
                }}
                
                const masterGain = ctx.createGain();
                masterGain.gain.setValueAtTime(1.0, ctx.currentTime);
                masterGain.connect(ctx.destination);

                [600, 900, 1200].forEach((baseFreq, i) => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = i % 2 === 0 ? 'sawtooth' : 'square';

                    osc.frequency.setValueAtTime(baseFreq, ctx.currentTime);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.3);
                    osc.frequency.linearRampToValueAtTime(baseFreq, ctx.currentTime + 0.6);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.9);

                    gain.gain.setValueAtTime(0.3, ctx.currentTime);
                    osc.connect(gain);
                    gain.connect(masterGain);

                    osc.start(ctx.currentTime);
                    osc.stop(ctx.currentTime + 1.0);
                }});
            }} catch(e) {{
                console.error("Audio error:", e);
            }}
        }}

        // 음성 인식 시작
        function startRecognition() {{
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert("이 브라우저는 음성 인식을 지원하지 않습니다. Chrome 브라우저를 사용해 주세요.");
                return;
            }}

            recognition = new SpeechRecognition();
            recognition.lang = 'ko-KR';
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = function() {{
                isListening = true;
                document.getElementById('status').innerText = "상태: 🔴 음성 감지 중... (말을 하면 실시간으로 분석합니다)";
                document.getElementById('status').style.color = "red";
                document.getElementById('startBtn').disabled = true;
                document.getElementById('stopBtn').disabled = false;
            }};

            recognition.onresult = function(event) {{
                let currentTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    currentTranscript += event.results[i][0].transcript;
                }}
                document.getElementById('transcript').innerText = "인식된 음성: " + currentTranscript;

                // 욕설/금지어 실시간 비교
                for (let word of bannedWords) {{
                    if (currentTranscript.includes(word)) {{
                        playSiren();
                        document.getElementById('status').innerText = "🚨 [경고] 욕설 감지됨!! (" + word + ")";
                        
                        // 인식 스트림 리셋
                        recognition.stop();
                        setTimeout(() => {{ if(isListening) recognition.start(); }}, 1200);
                        break;
                    }}
                }}
            }};

            recognition.onerror = function(event) {{
                console.error("Speech Recognition Error:", event.error);
            }};

            recognition.onend = function() {{
                if (isListening) {{
                    recognition.start(); // 자동 재연결로 계속 듣기 유지
                }} else {{
                    document.getElementById('status').innerText = "상태: 대기 중";
                    document.getElementById('status').style.color = "#333";
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('stopBtn').disabled = true;
                }}
            }};

            recognition.start();
        }}

        function stopRecognition() {{
            isListening = false;
            if (recognition) {{
                recognition.stop();
            }}
        }}
    </script>
</body>
</html>
"""

components.html(speech_and_sound_html, height=280)

st.markdown("---")
st.subheader("💡 사용 방법 안내")
st.markdown(
    """
1. **Chrome(크롬) 브라우저**에서 앱에 접속합니다.
2. 위 화면의 **`▶️ 음성 자동 감지 시작`** 버튼을 누르고 브라우저 마이크 권한을 허용합니다.
3. 마이크에 대고 말을 시작하면 **실시간으로 말을 인식**합니다.
4. 설정한 금지어(예: *바보*, *멍청이* 등)를 말하는 순간 **입력할 필요 없이 자동으로 즉시 강렬한 사이렌**이 울립니다!
"""
)
