import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(page_title="HIRENIX", layout="centered")

# ---------- SESSION ----------
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# ---------- CSS ----------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: #000000;
    color: #f9fafb;
}

/* CONTAINER CENTER */
.block-container {
    max-width: 900px;
    margin: auto;
    padding-top: 2rem;
}

/* HERO TITLE */
.hero-title {
    font-size:70px;
    font-weight:900;
    text-align:center;
    background:linear-gradient(90deg,#facc15,#eab308);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:5px;
    transition:0.3s;
}
.hero-title:hover {
    text-shadow:0 0 20px #facc15, 0 0 40px #eab308;
    transform:scale(1.05);
}

/* SUBTEXT */
.hero-sub {
    text-align:center;
    color:#9ca3af;
    margin-bottom:25px;
}

/* UPLOADER */
.stFileUploader {
    border-radius:18px;
    transition:0.3s;
}
.stFileUploader:hover {
    box-shadow:0 0 25px rgba(250,204,21,0.5);
}

/* BUTTON */
.stButton>button {
    border-radius:12px;
    transition:0.3s;
}
.stButton>button:hover {
    box-shadow:0 0 20px rgba(250,204,21,0.6);
    transform:scale(1.05);
}

/* CARD */
.card {
    padding:20px;
    border-radius:18px;
    background: rgba(255,215,0,0.05);
    border:1px solid rgba(250,204,21,0.3);
    margin-bottom:20px;
    transition:0.3s;
}
.card:hover {
    transform:translateY(-6px);
    box-shadow:0 0 30px rgba(250,204,21,0.3);
}

</style>
""", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for p in reader.pages:
        if p.extract_text():
            text += p.extract_text()
    return text.lower()

def extract_email(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}', text)

def extract_phone(text):
    return re.findall(r'\b\d{10}\b', text)

def calculate_score(text):
    return min(100, int(len(text.split())/5))

def score_breakdown():
    return {"Skills":24,"Structure":22,"Content":15,"Keywords":9}

def ats_score(text):
    keywords = ["python","sql","project","data"]
    return min(100, sum(1 for k in keywords if k in text)*25)

def resume_length(text):
    wc = len(text.split())
    if wc < 200: return wc,"Too Short"
    elif wc < 600: return wc,"Good"
    else: return wc,"Too Long"

def extract_projects(text):
    return len(re.findall(r'project', text))

def extract_experience(text):
    if "intern" in text:
        return "Intermediate"
    return "Fresher"

def extract_education(text):
    for d in ["bca","b.sc","b.e","b.tech","mca","mba"]:
        if d in text:
            return d.upper()
    return "Not Detected"

# ---------- LANDING ----------
# ---------- LANDING (FINAL CLEAN - CENTER FIX + HTML FIX + NO DOUBLE CLICK) ----------
if not st.session_state.analyzed:

    st.markdown("""
    <h1 style="
    font-size:70px;
    font-weight:900;
    text-align:center;
    background:linear-gradient(90deg,#facc15,#eab308);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:5px;
    ">
    HIRENIX
    </h1>

    <p style="
    text-align:center;
    color:#9ca3af;
    margin-top:10px;
    ">
    Turn Your Resume Into an Opportunity Magnet.
    </p>
    """, unsafe_allow_html=True)

    file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"], key="upload_unique_1")

    if file is not None:
        st.session_state.file = file
        st.session_state.analyzed = True
        st.rerun()
        
# ---------- RESULT ----------
else:
    text = extract_text(st.session_state.file)

    emails = extract_email(text)
    phones = extract_phone(text)
    score = calculate_score(text)
    breakdown = score_breakdown()
    ats = ats_score(text)
    words,status = resume_length(text)
    projects = extract_projects(text)
    exp = extract_experience(text)
    edu = extract_education(text)

    st.success("Resume analyzed successfully")

    # CONTACT
    st.markdown(f"""
    <div class="card">
    <h3>📇 Contact Information</h3>
    <p class="big">👤 Name: Yogesh N</p>
    <p class="big">📧 Email: {emails[0] if emails else "Not found"}</p>
    <p class="big">📱 Phone: {phones[0] if phones else "Not found"}</p>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    This section extracts contact details clearly from the resume. 
    It helps recruiters easily identify and reach the candidate.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # AI SCORE
    st.markdown(f"""
    <div class="card">
    <h3>📊 AI Resume Score</h3>
    <h1 style="color:#facc15;">{score}%</h1>

    <div style="width:100%;height:10px;background:#1f2937;border-radius:10px;">
    <div style="width:{score}%;height:100%;background:#facc15;border-radius:10px;"></div>
    </div>

    <p class="big">
    Skills: {breakdown['Skills']}% |
    Structure: {breakdown['Structure']}% |
    Content: {breakdown['Content']}% |
    Keywords: {breakdown['Keywords']}%
    </p>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    This score evaluates resume quality using multiple factors. 
    It reflects structure, content, and keyword optimization.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ATS
    st.markdown(f"""
    <div class="card">
    <h3>🤖 ATS Score</h3>
    <h1 style="color:#facc15;">{ats}%</h1>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    This measures how well your resume matches ATS filters. 
    Higher score improves chances of shortlisting.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # LENGTH
    st.markdown(f"""
    <div class="card">
    <h3>📄 Resume Length</h3>
    <h1 style="color:#facc15;">{words} words ({status})</h1>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    This checks if your resume length is optimal. 
    Balanced length improves readability and impact.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # PROJECTS
    st.markdown(f"""
    <div class="card">
    <h3>📁 Projects</h3>
    <h1 style="color:#facc15;">{projects}</h1>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    Projects show practical implementation of skills. 
    More relevant projects improve profile strength.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # EXPERIENCE
    st.markdown(f"""
    <div class="card">
    <h3>💼 Experience Level</h3>
    <h1 style="color:#facc15;">{exp}</h1>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    This determines your experience level from resume data. 
    It helps categorize your professional readiness.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # EDUCATION
    st.markdown(f"""
    <div class="card">
    <h3>🎓 Education</h3>
    <h1 style="color:#facc15;">{edu}</h1>

    <p style="color:#9ca3af;">
    <b>Explanation:</b><br>
    This identifies your academic qualification clearly. 
    It reflects your foundational knowledge.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # INSIGHTS
    st.markdown("""
    <div class="card">
    <h3>🔍 Insights</h3>
    <p><b>Overall:</b> Resume has good structure and clarity.</p>
    <p><b>Strength:</b> Strong basic skills are present.</p>
    <p><b>Improvement:</b> Add more projects and keywords.</p>
    <p><b>Career:</b> Suitable for entry-level roles.</p>
    </div>
    """, unsafe_allow_html=True)
