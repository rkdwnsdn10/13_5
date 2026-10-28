import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="학교 10대 생활 수칙 통합 감지 무한 사이렌",
    page_icon="🚨",
    layout="centered",
)

# 세션 이력 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

st.title("🚨 학교 10대 생활 수칙 실시간 통합 감지 사이렌")
st.caption(
    "교내 10대 위반 수칙 및 유사 발음 음성이 들리면 끄기 전까지 비상 사이렌이 계속 울립니다."
)

# 사이드바 감지 규칙 설정
st.sidebar.header("⚙️ 교내 10대 수칙 감지 키워드 설정")

# 1. 욕설 및 비속어
banned_words_input = st.sidebar.text_input(
    "1️⃣ 욕설/비속어/유사발음",
    value="씨발, 시발, 십팔, 개새끼, 미친, 바보, 빡통, 좆, 닥쳐",
)
banned_words = [w.strip() for w in banned_words_input.split(",") if w.strip()]

# 2. 학교 종합 규칙 위반 키워드 (10대 수칙)
school_rules_input = st.sidebar.text_input(
    "2️⃣ 교내 10대 수칙 위반 키워드",
    value="담배, 흡연, 꽁초, 스마트폰, 핸드폰, 폰제출, 뛰어, 소란, 부셔, 무단외출, 월담, 담치기, 싸움, 폭력, 협박, 커닝, 부정행위, 반항, 사복",
)
school_words = [w.strip() for w in school_rules_input.split(",") if w.strip()]

# 자바스크립트 전용 배열 변환
banned_words_js = str(banned_words)
school_words_js = str(school_words)

# ---------------------------------------------------------
# 통합 항시 음성 감지 & 유사 발음 분석 & 무한 사이렌 엔진
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
            padding: 12px;
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            color: #222;
            min-height: 45px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>🎙️ 실시간 교내 10대 수칙 감지기</h3>
        <button id="startBtn" class="btn" onclick="startContinuousListening()">▶️ 마이크 항시 감지 시작</button>
        <button id="stopAlarmBtn" class="btn btn-stop" onclick="stopAlarmSound()">🛑 경고음 끄기 (소리 정지)</button>
        
        <div id="status" class="status-box">상태: 감지 대기 중 ('▶️ 마이크 항시 감지 시작'을 누르세요)</div>
        <div id="transcript" class="transcript-box">음성 인식 내용이 여기에 실시간으로 표시됩니다...</div>
    </div>

    <script>
        let recognition = null;
        let isListening = false;
        let alarmInterval = null;
        let audioCtx = null;

        const bannedWords = {banned_words_js};
        const schoolWords = {school_words_js};

        // 한글 초성 분리 알고리즘 (유사 발음 검출용)
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

        // 유사도 매칭 (비슷한 발음도 자동 검출)
        function checkSimilarPronunciation(input, target) {{
            const cleanInput = input.replace(/\\s+/g, '');
            const cleanTarget = target.replace(/\\s+/g, '');
            
            if (cleanInput.includes(cleanTarget)) return true;

            const inputCho = getHangulChosung(cleanInput);
            const targetCho = getHangulChosung(cleanTarget);
            
            if (inputCho.includes(targetCho) && targetCho.length >= 2) {{
                return true;
            }}

            return false;
        }}

        // 무한 비상 사이렌 발령
        function triggerSirenLoop() {{
            if (!audioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) audioCtx = new AudioContext();
            }}
            if (audioCtx && audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}

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

        // 소리 정지
        function stopAlarmSound() {{
            if (alarmInterval) {{
                clearInterval(alarmInterval);
                alarmInterval = null;
            }}
            if (audioCtx) {{
                audioCtx.suspend();
            }}
            document.getElementById('status').innerText = isListening ? "상태: 🟢 감지 중 (음성 모니터링 활성화)" : "상태: 감지 대기 중";
            document.getElementById('status').style.color = isListening ? "green" : "#d90429";
        }}

        // 실시간 음성 항시 감지
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
                document.getElementById('status').innerText = "상태: 🟢 마이크 항시 감지 중... (교내 수칙 위반 감지 시 사이렌)";
                document.getElementById('status').style.color = "green";
                document.getElementById('startBtn').disabled = true;
            }};

            recognition.onresult = function(event) {{
                let currentText = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    currentText += event.results[i][0].transcript;
                }}
                document.getElementById('transcript').innerText = "🗣️ 인식된 음성: " + currentText;

                // 1. 욕설 및 유사 발음 감지
                for (let word of bannedWords) {{
                    if (checkSimilarPronunciation(currentText, word)) {{
                        document.getElementById('status').innerText = "🚨 [비상] 욕설/유사발음 감지: '" + word + "'";
                        document.getElementById('status').style.color = "red";
                        triggerSirenLoop();
                        return;
                    }}
                }}

                // 2. 학교 10대 위반 수칙 키워드 감지
                for (let word of schoolWords) {{
                    if (checkSimilarPronunciation(currentText, word)) {{
                        document.getElementById('status').innerText = "🚨 [학교 수칙 위반 감지]: '" + word + "' 관련 행위 포착!";
                        document.getElementById('status').style.color = "red";
                        triggerSirenLoop();
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
    </script>
</body>
</html>
"""

components.html(full_engine_html, height=310)

# ---------------------------------------------------------
# 학교 10대 필수 규정 세부 안내
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 감지 대상 교내 10대 생활 수칙")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
    - **1️⃣ 바른 언어 사용**: 욕설, 비속어, 비하 발언 및 유사 발음
    - **2️⃣ 교내 완전 금연**: 화장실, 교사 뒤편, 전자담배 포함
    - **3️⃣ 스마트폰 사용 제한**: 수업 중 무단 사용, 게임, 미제출
    - **4️⃣ 복도 침묵 & 통행**: 복도 질주, 고성방가, 소란 행위
    - **5️⃣ 무단 외출 금지**: 월담, 담치기, 수업 시간 무단 이탈
    """
    )
with col2:
    st.markdown(
        """
    - **6️⃣ 교내 폭력 예방**: 싸움, 위협, 협박, 갈취 행위 엄금
    - **7️⃣ 공공 기물 보호**: 기물 파손, 시설물 훼손 및 낙서
    - **8️⃣ 정직한 평가**: 시험 중 부정행위, 커닝, 답안 공유
    - **9️⃣ 교권 보호**: 교사 지시 불응, 수업 방해, 반항
    - **🔟 용의 복장 규정**: 무단 사복 착용 및 복장 위반
    """
    )

# ---------------------------------------------------------
# 감지 이력 리포트 (Pandas)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📜 실시간 음성 및 위반 기록 이력")

manual_log = st.text_input(
    "📝 직접 위반
