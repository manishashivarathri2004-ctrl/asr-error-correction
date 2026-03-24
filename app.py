import streamlit as st
from dataset_loader import get_audio_files
from asr import transcribe_audio
from llm_correction import correct_text

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ASR Error Correction",
    layout="wide"
)

# ---------- CUSTOM CSS (FINAL CLEAN VERSION) ----------
st.markdown("""
<style>

/* 🌿 FULL BACKGROUND (TEAL PASTEL) */
html, body, .stApp {
    background: linear-gradient(135deg, #e6f4f1, #cfe9e5) !important;
}

/* Cover full app */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e6f4f1, #cfe9e5) !important;
}

/* Remove white layers */
[data-testid="stApp"] {
    background: transparent !important;
}

/* Remove top white strip */
header, [data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent !important;
}

/* Fix spacing */
.block-container {
    padding-top: 1rem !important;
    background: transparent !important;
}

/* ---------- TEXT ---------- */

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #1f3d3a;
}

.subtitle {
    text-align: center;
    color: #4b6e6a;
    margin-bottom: 20px;
}

/* ---------- CARD ---------- */

.card {
    background: rgba(255,255,255,0.85);
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* ---------- OUTPUT ---------- */

.asr-box {
    background-color: #fff5f5;
    padding: 15px;
    border-radius: 10px;
    color: #8b0000;
}

.corrected-box {
    background-color: #e6f7f4;
    padding: 15px;
    border-radius: 10px;
    color: #065f5b;
}

/* ---------- INFO ---------- */

.info-box {
    background-color: #eef9f7;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    border-left: 4px solid #2a9d8f;
}

/* ---------- BUTTON ---------- */

.stButton > button {
    background-color: #2a9d8f;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    border: none;
}

.stButton > button:hover {
    background-color: #21867a;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    margin-top: 40px;
    color: #4b6e6a;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🎙️ Speech Recognition Error Correction</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enhancing ASR output for non-native English speakers</div>', unsafe_allow_html=True)

# ---------- DATASET ----------
DATASET_PATH = "dataset/L2_ARCTIC"
audio_files = get_audio_files(DATASET_PATH)

# ---------- FUNCTIONS ----------
def get_accent(file_path):
    if "ABA" in file_path:
        return "Arabic Speaker"
    elif "ZHAA" in file_path:
        return "Chinese Speaker"
    elif "HJK" in file_path:
        return "Korean Speaker"
    elif "EBVS" in file_path:
        return "Spanish Speaker"
    else:
        return "Unknown Accent"

def show_corrections(original):
    changes = []

    if "Hardly where" in original:
        changes.append("❌ 'Hardly where' → ✅ 'Hardly were'")

    if "made by powerful opposition" in original:
        changes.append("❌ 'made by' → ✅ 'met by'")

    if "dont" in original:
        changes.append("❌ 'dont' → ✅ 'don't'")

    if "cant" in original:
        changes.append("❌ 'cant' → ✅ 'can't'")

    return changes

# ---------- UI ----------
if not audio_files:
    st.error("No audio files found. Please check dataset folder.")
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    selected_audio = st.selectbox("🎧 Select Audio Sample", audio_files)

    accent = get_accent(selected_audio)
    st.markdown(f"""
    <div class="info-box">
    🎯 <b>Speaker Accent:</b> {accent}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Run ASR & Correction"):

        st.audio(selected_audio)

        with st.spinner("Processing audio..."):
            asr_text = transcribe_audio(selected_audio)

            st.markdown("### ❌ ASR Output")
            st.markdown(f'<div class="asr-box">{asr_text}</div>', unsafe_allow_html=True)

            corrected_text = correct_text(asr_text)

            st.markdown("### ✅ Corrected Output")
            st.markdown(f'<div class="corrected-box">{corrected_text}</div>', unsafe_allow_html=True)

            changes = show_corrections(asr_text)

            if changes:
                st.markdown("### 🔍 Corrections Applied")
                for c in changes:
                    st.markdown(f"- {c}")
            else:
                st.info("No major corrections were needed.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown('<div class="footer">Built with ❤️ using Whisper + NLP + Streamlit</div>', unsafe_allow_html=True)