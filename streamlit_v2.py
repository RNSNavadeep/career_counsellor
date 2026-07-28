import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from recommendation import recommend_career
from career_data.career_database import career_data, CAREER_DOMAINS
from memory import memory

st.set_page_config(
    page_title="AI Virtual Career Counsellor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp,p,div,h1,h2,h3,h4,h5,h6,label,input,select,textarea,.user-bubble,.bot-bubble,.career-card{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif!important;}
[data-testid="stIconMaterial"],[data-testid="stSidebarCollapseButton"] *,[data-testid="collapsedControl"] *{font-family:'Material Symbols Rounded','Material Icons'!important;}

.stApp{background:#0B1120!important;color:#F1F5F9!important;}
.block-container{max-width:1200px!important;padding-top:0!important;padding-bottom:5rem!important;}
header,footer,#MainMenu,[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;visibility:hidden!important;}

/* Sidebar */
section[data-testid="stSidebar"]{background:#0F172A!important;border-right:1px solid #1E293B!important;}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] div{color:#E2E8F0!important;}
section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3{color:#FFFFFF!important;font-weight:700!important;}

/* Selectbox */
div[data-baseweb="select"]>div{background:#1E293B!important;border:1px solid #334155!important;border-radius:10px!important;color:#FFFFFF!important;}
div[data-baseweb="select"] span,div[data-baseweb="select"] div,div[data-baseweb="select"] input{color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;background:transparent!important;}
div[data-baseweb="select"] [data-testid="stSelectboxVirtualDropdown"],
div[data-baseweb="select"] [class*="value"],
div[data-baseweb="select"] [class*="placeholder"],
div[data-baseweb="select"] [class*="singleValue"],
div[data-baseweb="select"] p{color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;}
div[data-baseweb="popover"]>div{background:#1E293B!important;border:1px solid #334155!important;}
div[data-baseweb="popover"] li{color:#E2E8F0!important;-webkit-text-fill-color:#E2E8F0!important;background:#1E293B!important;}
div[data-baseweb="popover"] li:hover,div[data-baseweb="popover"] li[aria-selected="true"]{background:#2563EB!important;color:#FFF!important;-webkit-text-fill-color:#FFF!important;}

/* Radio */
[data-testid="stRadio"] label{color:#E2E8F0!important;}

/* Expanders */
div[data-testid="stExpander"]{background:#1E293B!important;border:1px solid #334155!important;border-radius:12px!important;}
div[data-testid="stExpander"] summary,div[data-testid="stExpander"] summary *{color:#F1F5F9!important;font-weight:600!important;}
div[data-testid="stExpander"] p,div[data-testid="stExpander"] li,div[data-testid="stExpander"] span{color:#CBD5E1!important;}

/* Metrics */
[data-testid="metric-container"]{background:#1E293B!important;padding:14px!important;border-radius:12px!important;border:1px solid #334155!important;}
[data-testid="metric-container"] label{color:#94A3B8!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"] *{color:#38BDF8!important;font-weight:700!important;}

/* Buttons */
.stButton>button{width:100%!important;background:linear-gradient(135deg,#2563EB,#4F46E5)!important;color:#FFF!important;border:none!important;border-radius:10px!important;font-weight:700!important;font-size:14px!important;padding:8px 12px!important;transition:all 0.2s ease!important;}
.stButton>button:hover{background:linear-gradient(135deg,#1D4ED8,#4338CA)!important;transform:translateY(-1px)!important;box-shadow:0 4px 15px rgba(37,99,235,0.4)!important;}

/* Chat Input */
div[data-testid="stBottomBlockContainer"]{background:#0B1120!important;}
div[data-testid="stChatInput"]>div{background:#1E293B!important;border:2px solid #334155!important;border-radius:16px!important;}
div[data-testid="stChatInput"] textarea{color:#FFFFFF!important;font-size:15px!important;}
div[data-testid="stChatInput"] textarea::placeholder{color:#64748B!important;}
div[data-testid="stChatInput"] button{background:#2563EB!important;border-radius:10px!important;}

/* Transparent Streamlit wrappers everywhere */
[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stElementContainer"],.element-container{background:transparent!important;background-color:transparent!important;}

/* User bubble */
.user-bubble{background:linear-gradient(135deg,#2563EB 0%,#4F46E5 100%);color:#FFF!important;padding:14px 20px;border-radius:18px 18px 4px 18px;margin:10px 0 10px 80px;font-size:15px;font-weight:500;line-height:1.6;box-shadow:0 4px 12px rgba(37,99,235,0.3);}
.user-bubble *{color:#FFF!important;}
.user-label{font-size:12px;font-weight:700;color:#93C5FD;margin:0 0 4px 80px;letter-spacing:0.05em;}

/* Bot bubble */
.bot-bubble{background:#1E293B;color:#F1F5F9!important;padding:18px 22px;border-radius:18px 18px 18px 4px;margin:10px 80px 10px 0;font-size:15px;line-height:1.7;border-left:4px solid #3B82F6;box-shadow:0 4px 15px rgba(0,0,0,0.3);}
.bot-bubble *{color:#F1F5F9!important;background:transparent!important;}
.bot-bubble b,.bot-bubble strong{color:#FFFFFF!important;}
.bot-bubble i,.bot-bubble em{color:#93C5FD!important;}
.bot-label{font-size:12px;font-weight:700;color:#60A5FA;margin:0 0 4px 0;letter-spacing:0.05em;}

/* Career card */
.career-card{background:linear-gradient(145deg,#0F1E3D 0%,#1E293B 100%);border:1px solid #334155;border-left:5px solid #3B82F6;border-radius:16px;padding:22px 26px;margin:4px 80px 4px 0;}
.career-card *{color:#F1F5F9!important;background:transparent!important;}
.career-title{font-size:26px!important;font-weight:900!important;color:#60A5FA!important;margin:0 0 10px 0!important;display:block;}
.domain-badge{display:inline-block;background:#1E3A8A!important;color:#93C5FD!important;padding:3px 12px;border-radius:20px;font-size:13px;font-weight:700;border:1px solid #2563EB!important;margin-right:8px;margin-bottom:8px;}
.match-badge{display:inline-block;background:#065F46!important;color:#6EE7B7!important;padding:4px 14px;border-radius:20px;font-size:14px;font-weight:700;border:1px solid #059669!important;margin-bottom:12px;}
.skill-chip{display:inline-block;background:#1E3A8A!important;color:#93C5FD!important;padding:4px 12px;margin:3px;border-radius:16px;font-size:13px;font-weight:600;border:1px solid #2563EB!important;}
.section-hdr{color:#7DD3FC!important;font-size:13px!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:0.08em!important;margin:14px 0 6px 0!important;padding-bottom:4px!important;border-bottom:1px solid #1E3A8A!important;}
.section-body{color:#CBD5E1!important;font-size:15px!important;line-height:1.7!important;margin:6px 0 10px!important;}

::-webkit-scrollbar{width:7px;}
::-webkit-scrollbar-thumb{background:#2563EB;border-radius:10px;}
::-webkit-scrollbar-track{background:#0B1120;}
</style>
""", unsafe_allow_html=True)

# ── Session Init ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "type": "text",
            "content": (
                "👋 <b>Hello! I'm your AI Virtual Career Counsellor.</b><br><br>"
                "I analyse your skills and interests across <b>Tech, Arts &amp; Design, "
                "and Commerce &amp; Business</b> to find your perfect career path.<br><br>"
                "<b>Try asking things like:</b><br>"
                "💻 <i>'I love machine learning, Python, and neural networks'</i><br>"
                "🎨 <i>'I enjoy Figma wireframing and user experience design'</i><br>"
                "📈 <i>'I like digital marketing, SEO, and Google Ads'</i><br>"
                "💼 <i>'I want to work in financial modeling and equity research'</i><br><br>"
                "I'll give you <b>Roadmaps · Salary · Skills · Companies · Projects 🚀</b>"
            )
        }
    ]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;margin-bottom:8px;'>"
        "<span style='font-size:28px;font-weight:900;letter-spacing:4px;"
        "background:linear-gradient(135deg,#60A5FA,#A78BFA);-webkit-background-clip:text;"
        "-webkit-text-fill-color:transparent;background-clip:text;'>RNS</span>"
        "</div>"
        "<h2 style='text-align:center;color:#FFFFFF;margin-bottom:2px;'>🎓 AI Career</h2>"
        "<p style='text-align:center;color:#64748B;font-size:13px;margin:0 0 16px;'>Virtual Counsellor v2.0</p>",
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown("### 🎯 Filter by Domain")
    domain_choice = st.radio(
        "Stream",
        ["All Streams", "Tech", "Arts & Design", "Commerce & Business"],
        label_visibility="collapsed"
    )
    selected_domain_key = "All" if domain_choice == "All Streams" else domain_choice

    st.divider()
    st.markdown("### 💡 Quick Sample Queries")

    SAMPLE_MAP = {
        "Tech": [
            "Select a prompt...",
            "I love machine learning and Python",
            "I enjoy making dashboards using Power BI",
            "I want to become an AI Engineer",
            "I like ethical hacking and cybersecurity",
            "I enjoy frontend development with React",
            "I love Docker and Kubernetes"
        ],
        "Arts & Design": [
            "Select a prompt...",
            "I enjoy Figma prototyping and user research",
            "I love Photoshop, vector illustration, and branding",
            "I want to design intuitive mobile user interfaces",
            "I am interested in typography and visual aesthetics"
        ],
        "Commerce & Business": [
            "Select a prompt...",
            "I love digital marketing, SEO, and social media ads",
            "I want to be a Business Analyst using Agile and SQL",
            "I like financial modeling, valuation, and accounting",
            "I enjoy market research and Excel"
        ],
        "All": [
            "Select a prompt...",
            "I love machine learning and Python",
            "I enjoy Figma wireframing and user experience",
            "I love digital marketing, SEO, and Google Ads",
            "I want to do financial modeling and valuation",
            "I like ethical hacking and cybersecurity",
            "I enjoy business analysis and requirements gathering"
        ]
    }

    sample_prompts = SAMPLE_MAP.get(selected_domain_key, SAMPLE_MAP["All"])
    selected_prompt = st.selectbox("Sample Query", sample_prompts, label_visibility="collapsed")

    st.divider()
    st.markdown("### 📚 Career Explorer")
    available_careers = CAREER_DOMAINS.get(selected_domain_key, list(career_data.keys()))
    selected_career_name = st.selectbox(
        f"Explore {len(available_careers)} Careers",
        available_careers,
        label_visibility="collapsed"
    )

    if selected_career_name:
        c_info = career_data[selected_career_name]
        with st.expander(f"📌 {c_info['career']}", expanded=False):
            st.markdown(f"**Domain:** `{c_info.get('domain','General')}`")
            st.markdown(f"{c_info['description'][:200]}...")
            col1, col2, col3 = st.columns(3)
            col1.metric("Entry",  c_info["salary"].get("entry",  "N/A"))
            col2.metric("Mid",    c_info["salary"].get("mid",    "N/A"))
            col3.metric("Senior", c_info["salary"].get("senior", "N/A"))
            st.markdown("**Top Companies:**")
            for co in c_info["companies"][:4]:
                st.markdown(f"- {co}")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "type": "text",
                "content": "👋 <b>Chat cleared.</b> What career would you like to explore?"
            }
        ]
        memory.set_career(None)
        st.rerun()

    st.markdown(
        "<p style='text-align:center;font-size:12px;color:#334155;margin-top:10px;'>"
        "Powered by NLTK · Rasa · Streamlit</p>",
        unsafe_allow_html=True
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#2563EB 0%,#4F46E5 100%);
            padding:26px 30px;border-radius:20px;margin-bottom:20px;
            box-shadow:0 12px 30px rgba(0,0,0,0.4);
            border:1px solid rgba(255,255,255,0.12);text-align:center;">
  <h1 style="font-size:36px;font-weight:900;color:#FFFFFF;margin:0 0 6px;letter-spacing:-0.5px;">
    🎓 AI Virtual Career Counsellor
  </h1>
  <p style="font-size:16px;color:#BFDBFE;margin:0;font-weight:500;">
    NLP-Powered Recommendation Engine &nbsp;·&nbsp; Tech &nbsp;·&nbsp; Arts &nbsp;·&nbsp; Commerce
  </p>
</div>
""", unsafe_allow_html=True)

# ── Chat Renderer ─────────────────────────────────────────────────────────────
def render_message(msg):
    role  = msg["role"]
    mtype = msg.get("type", "text")

    if role == "user":
        st.markdown(
            f'<div class="user-label">YOU</div>'
            f'<div class="user-bubble">{msg["content"]}</div>',
            unsafe_allow_html=True
        )
        return

    # ── assistant: plain text ──
    if mtype == "text":
        st.markdown(
            f'<div class="bot-label">AI COUNSELLOR</div>'
            f'<div class="bot-bubble">{msg["content"]}</div>',
            unsafe_allow_html=True
        )
        return

    # ── assistant: career card ──
    if mtype == "career_card":
        d            = msg.get("data", {})
        career_name  = d.get("career", "")
        domain_name  = d.get("domain", "General")
        confidence   = d.get("confidence", 0)
        matched      = d.get("matched_keywords", [])
        description  = d.get("description", "")

        chips = "".join([f'<span class="skill-chip">{k}</span>' for k in matched if k])
        if not chips:
            chips = '<span class="skill-chip">Domain Interest</span>'

        st.markdown(f"""
<div class="bot-label">AI COUNSELLOR</div>
<div class="career-card">
  <span class="career-title">🎯 {career_name}</span>
  <span class="domain-badge">🏷️ {domain_name}</span>
  <span class="match-badge">🔥 {confidence}% Career Match</span>

  <div class="section-hdr">📖 Career Overview</div>
  <p class="section-body">{description}</p>

  <div class="section-hdr">✅ Matched Keywords</div>
  <div style="margin:6px 0 10px;">{chips}</div>

  <div class="section-hdr">💡 Ask Me Follow-Ups</div>
  <p style="color:#94A3B8;font-size:14px;margin:6px 0;">
    Try: <b style="color:#60A5FA;">Roadmap</b> &nbsp;·&nbsp;
    <b style="color:#60A5FA;">Salary</b> &nbsp;·&nbsp;
    <b style="color:#60A5FA;">Skills</b> &nbsp;·&nbsp;
    <b style="color:#60A5FA;">Companies</b> &nbsp;·&nbsp;
    <b style="color:#60A5FA;">Projects</b>
  </p>
</div>
""", unsafe_allow_html=True)


# ── Render History ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    render_message(msg)

# ── Follow-Up Buttons ─────────────────────────────────────────────────────────
user_query = None
active_career = memory.get_career()

if active_career:
    st.markdown(
        f"<p style='color:#60A5FA;font-size:14px;font-weight:700;margin:12px 0 6px;'>"
        f"⚡ Quick Follow-Ups for <b style='color:#FFFFFF;'>{active_career['career']}</b>:</p>",
        unsafe_allow_html=True
    )
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("📍 Roadmap",    key="btn_roadmap"):
        user_query = f"give me roadmap for {active_career['career']}"
    elif c2.button("💰 Salary",   key="btn_salary"):
        user_query = f"what is the salary for {active_career['career']}"
    elif c3.button("🛠️ Skills",   key="btn_skills"):
        user_query = f"what skills are needed for {active_career['career']}"
    elif c4.button("🏢 Companies", key="btn_companies"):
        user_query = f"which companies hire {active_career['career']}"
    elif c5.button("💡 Projects", key="btn_projects"):
        user_query = f"give me project ideas for {active_career['career']}"

# ── Sample Prompt ─────────────────────────────────────────────────────────────
if selected_prompt != "Select a prompt..." and not user_query:
    user_query = selected_prompt

# ── Chat Input ────────────────────────────────────────────────────────────────
chat_input = st.chat_input(
    "Type your interests or ask follow-ups (e.g., 'I love Figma and UI design' or 'salary')..."
)
if chat_input:
    user_query = chat_input

# ── Process Query ─────────────────────────────────────────────────────────────
if user_query:
    st.session_state.messages.append({
        "role": "user", "type": "text", "content": user_query
    })

    lower_q = user_query.lower().strip()

    if lower_q in {"hi", "hello", "hey", "good morning", "good evening", "good afternoon"}:
        reply_msg = {
            "role": "assistant",
            "type": "text",
            "content": "👋 <b>Hello!</b> Tell me about your interests in Tech, Arts, or Commerce and I'll find your perfect career!"
        }
    elif lower_q in {"bye", "goodbye", "exit", "quit", "thanks", "thank you"}:
        reply_msg = {
            "role": "assistant",
            "type": "text",
            "content": "👋 <b>Best of luck on your career journey!</b> Feel free to come back anytime! 🌟"
        }
    else:
        res = recommend_career(user_query)

        if res is None:
            reply_msg = {
                "role": "assistant",
                "type": "text",
                "content": (
                    "🤔 <b>I couldn't find a strong match for that query.</b><br><br>"
                    "Try describing your interests in more detail, such as:<br>"
                    "• <i>'I love machine learning and Python'</i><br>"
                    "• <i>'I enjoy Figma wireframing and UI UX design'</i><br>"
                    "• <i>'I like digital marketing, SEO, and Google Ads'</i><br>"
                    "• <i>'I enjoy financial modeling and valuation'</i>"
                )
            }
        elif isinstance(res, str):
            reply_msg = {"role": "assistant", "type": "text", "content": res}
        else:
            reply_msg = {"role": "assistant", "type": "career_card", "data": res}

    st.session_state.messages.append(reply_msg)
    st.rerun()

