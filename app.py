import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #a09890;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
}

.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

.stTextInput > div > div > input::placeholder {
    color: #666666 !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}

/* Fix Chrome yellow autofill */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
    -webkit-text-fill-color: #000000 !important;
    -webkit-box-shadow: 0 0 0px 1000px white inset !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
    opacity: 0.95 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.4);
    background: rgba(255,140,50,0.04);
}
.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.7;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #555; }
.status-running  { color: #ff8c32; }
.status-done     { color: #50c878; }

.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cdc8bf;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.15);
}

.stSpinner > div { color: #ff8c32 !important; }

details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #a09890 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 2rem 0 1rem;
}

.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #605850;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    # ── Voice input component ──
    st.components.v1.html("""
    <div style="margin-bottom:0.8rem;">
        <button id="voiceBtn" onclick="toggleVoice()" style="
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,140,50,0.25);
            border-radius: 10px;
            color: #ff8c32;
            font-size: 0.9rem;
            font-family: 'DM Sans', sans-serif;
            letter-spacing: 0.05em;
            padding: 0.6rem 1rem;
            cursor: pointer;
            width: 100%;
            text-align: center;
            transition: all 0.2s;
        ">🎙&nbsp; Click to speak your topic</button>
        <div id="transcript" style="
            font-size: 0.75rem;
            color: #a09890;
            font-family: 'DM Mono', monospace;
            margin-top: 0.4rem;
            min-height: 1.2rem;
            letter-spacing: 0.05em;
            text-align: center;
        "></div>
    </div>

    <script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition, listening = false;

    function toggleVoice() {
        if (!SpeechRecognition) {
            document.getElementById('transcript').textContent = '⚠ Voice not supported. Please use Chrome or Edge.';
            return;
        }
        if (listening) {
            recognition.stop();
            return;
        }

        recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = true;
        recognition.continuous = false;

        const btn = document.getElementById('voiceBtn');
        const div = document.getElementById('transcript');

        recognition.onstart = () => {
            listening = true;
            btn.textContent = '⏹  Stop recording';
            btn.style.borderColor = '#ff5a1a';
            btn.style.background = 'rgba(255,90,26,0.12)';
            btn.style.color = '#ff5a1a';
            div.textContent = '● Listening…';
        };

        recognition.onresult = (e) => {
            const transcript = Array.from(e.results)
                .map(r => r[0].transcript).join('');
            div.textContent = transcript;

            if (e.results[e.results.length - 1].isFinal) {
                // Inject transcript into Streamlit's text input
                const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs.length > 0) {
                    const setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value'
                    ).set;
                    setter.call(inputs[0], transcript);
                    inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                }
                div.textContent = '✓ ' + transcript;
            }
        };

        recognition.onend = () => {
            listening = false;
            btn.textContent = '🎙\u00a0 Click to speak your topic';
            btn.style.borderColor = 'rgba(255,140,50,0.25)';
            btn.style.background = 'rgba(255,255,255,0.05)';
            btn.style.color = '#ff8c32';
        };

        recognition.onerror = (e) => {
            div.textContent = '⚠ Error: ' + e.error;
            listening = false;
            btn.textContent = '🎙\u00a0 Click to speak your topic';
            btn.style.borderColor = 'rgba(255,140,50,0.25)';
            btn.style.background = 'rgba(255,255,255,0.05)';
            btn.style.color = '#ff8c32';
        };

        recognition.start();
    }
    </script>
    """, height=85)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;
            padding:0.25rem 0.7rem;
            font-size:0.75rem;
            color:#a09890;
            font-family:'DM Sans',sans-serif;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

        # ── TTS for report ──
        report_text = r["writer"].replace('"', '\\"').replace('\n', ' ').replace('`', '')
        st.components.v1.html(f"""
        <div style="margin-top:0.8rem;">
            <button id="ttsReportBtn" onclick="toggleTTS('report')" style="
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,140,50,0.25);
                border-radius: 10px;
                color: #ff8c32;
                font-size: 0.85rem;
                font-family: 'DM Sans', sans-serif;
                padding: 0.5rem 1.2rem;
                cursor: pointer;
                transition: all 0.2s;
            ">🔊&nbsp; Read Report Aloud</button>
            <span id="ttsReportStatus" style="
                font-family:'DM Mono',monospace;
                font-size:0.72rem;
                color:#a09890;
                margin-left:0.8rem;
                letter-spacing:0.05em;
            "></span>
        </div>
        <script>
        var reportText = "{report_text}";
        var reportUtter = null;
        var reportPlaying = false;

        function toggleTTS(id) {{
            var btn = document.getElementById('ttsReportBtn');
            var status = document.getElementById('ttsReportStatus');
            if (reportPlaying) {{
                window.speechSynthesis.cancel();
                reportPlaying = false;
                btn.textContent = '🔊\u00a0 Read Report Aloud';
                btn.style.borderColor = 'rgba(255,140,50,0.25)';
                status.textContent = '';
                return;
            }}
            window.speechSynthesis.cancel();
            reportUtter = new SpeechSynthesisUtterance(reportText);
            reportUtter.rate = 1.0;
            reportUtter.pitch = 1.0;
            reportUtter.lang = 'en-US';
            reportUtter.onstart = () => {{
                reportPlaying = true;
                btn.textContent = '⏹\u00a0 Stop Reading';
                btn.style.borderColor = '#ff5a1a';
                btn.style.color = '#ff5a1a';
                status.textContent = '● Speaking…';
            }};
            reportUtter.onend = () => {{
                reportPlaying = false;
                btn.textContent = '🔊\u00a0 Read Report Aloud';
                btn.style.borderColor = 'rgba(255,140,50,0.25)';
                btn.style.color = '#ff8c32';
                status.textContent = '✓ Done';
            }};
            reportUtter.onerror = () => {{
                reportPlaying = false;
                btn.textContent = '🔊\u00a0 Read Report Aloud';
                status.textContent = '⚠ Error';
            }};
            window.speechSynthesis.speak(reportUtter);
        }}
        </script>
        """, height=60)

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)

        # ── TTS for critic ──
        critic_text = r["critic"].replace('"', '\\"').replace('\n', ' ').replace('`', '')
        st.components.v1.html(f"""
        <div style="margin-top:0.8rem;">
            <button id="ttsCriticBtn" onclick="toggleCriticTTS()" style="
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(80,200,120,0.25);
                border-radius: 10px;
                color: #50c878;
                font-size: 0.85rem;
                font-family: 'DM Sans', sans-serif;
                padding: 0.5rem 1.2rem;
                cursor: pointer;
                transition: all 0.2s;
            ">🔊&nbsp; Read Feedback Aloud</button>
            <span id="ttsCriticStatus" style="
                font-family:'DM Mono',monospace;
                font-size:0.72rem;
                color:#a09890;
                margin-left:0.8rem;
                letter-spacing:0.05em;
            "></span>
        </div>
        <script>
        var criticText = "{critic_text}";
        var criticUtter = null;
        var criticPlaying = false;

        function toggleCriticTTS() {{
            var btn = document.getElementById('ttsCriticBtn');
            var status = document.getElementById('ttsCriticStatus');
            if (criticPlaying) {{
                window.speechSynthesis.cancel();
                criticPlaying = false;
                btn.textContent = '🔊\u00a0 Read Feedback Aloud';
                btn.style.borderColor = 'rgba(80,200,120,0.25)';
                status.textContent = '';
                return;
            }}
            window.speechSynthesis.cancel();
            criticUtter = new SpeechSynthesisUtterance(criticText);
            criticUtter.rate = 1.0;
            criticUtter.pitch = 1.0;
            criticUtter.lang = 'en-US';
            criticUtter.onstart = () => {{
                criticPlaying = true;
                btn.textContent = '⏹\u00a0 Stop Reading';
                btn.style.borderColor = '#50c878';
                btn.style.color = '#50c878';
                status.textContent = '● Speaking…';
            }};
            criticUtter.onend = () => {{
                criticPlaying = false;
                btn.textContent = '🔊\u00a0 Read Feedback Aloud';
                btn.style.borderColor = 'rgba(80,200,120,0.25)';
                btn.style.color = '#50c878';
                status.textContent = '✓ Done';
            }};
            criticUtter.onerror = () => {{
                criticPlaying = false;
                btn.textContent = '🔊\u00a0 Read Feedback Aloud';
                status.textContent = '⚠ Error';
            }};
            window.speechSynthesis.speak(criticUtter);
        }}
        </script>
        """, height=60)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
