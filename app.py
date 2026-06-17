import streamlit as st
import time
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;450;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0B0F1A;
    color: #DDE3F0;
  }
  .hero { padding: 3rem 0 2rem 0; text-align: center; }
  .hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; letter-spacing: 0.18em;
    color: #5B7FFF; text-transform: uppercase; margin-bottom: 0.75rem;
  }
  .hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem; font-weight: 700; line-height: 1.1;
    color: #FFFFFF; margin: 0; letter-spacing: -0.02em;
  }
  .hero-title span { color: #5B7FFF; }
  .hero-sub {
    margin-top: 0.9rem; font-size: 1rem; color: #8896B3;
    max-width: 540px; margin-left: auto; margin-right: auto;
  }
  .input-card {
    background: #141927; border: 1px solid #1E2740;
    border-radius: 14px; padding: 2rem 2.4rem; margin: 1.5rem auto;
  }
  .input-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem; letter-spacing: 0.14em;
    color: #5B7FFF; text-transform: uppercase; margin-bottom: 0.4rem;
  }
  .step-card {
    background: #141927; border: 1px solid #1E2740;
    border-radius: 12px; padding: 1.2rem 1.3rem;
    position: relative; margin-bottom: 0.8rem;
  }
  .step-card.active  { border-color: #5B7FFF; background: #141E35; }
  .step-card.done    { border-color: #22C55E; }
  .step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; color: #3D4F72; letter-spacing: 0.1em; margin-bottom: 0.4rem;
  }
  .step-name { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 0.92rem; color: #DDE3F0; }
  .step-desc { font-size: 0.78rem; color: #5A6A8A; margin-top: 0.25rem; }
  .step-badge {
    position: absolute; top: 0.9rem; right: 0.9rem;
    font-size: 0.75rem; letter-spacing: 0.08em;
    font-family: 'IBM Plex Mono', monospace;
  }
  .badge-waiting { color: #5A6A8A; }
  .badge-active  { color: #5B7FFF; }
  .badge-done    { color: #22C55E; }
  .pipeline-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600; font-size: 1.1rem; color: #DDE3F0; margin-bottom: 1rem;
  }
  .result-panel {
    background: #141927; border: 1px solid #1E2740;
    border-radius: 12px; padding: 1.6rem 1.8rem; margin-bottom: 1.2rem;
  }
  .result-header { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1rem; }
  .result-icon {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
  }
  .icon-search { background: #1A2E55; }
  .icon-scrape { background: #1B2B1B; }
  .icon-report { background: #2B1F1A; }
  .icon-critic { background: #251B30; }
  .result-title { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 1rem; color: #DDE3F0; }
  .result-body { font-size: 0.88rem; line-height: 1.7; color: #9AAAC8; white-space: pre-wrap; }
  .divider { border: none; border-top: 1px solid #1E2740; margin: 2rem 0; }
  .stTextInput > div > div > input {
    background: #0B0F1A !important; border: 1px solid #1E2740 !important;
    border-radius: 8px !important; color: #DDE3F0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #5B7FFF !important;
    box-shadow: 0 0 0 3px rgba(91,127,255,0.15) !important;
  }
  .stTextInput > label { display: none !important; }
  .stButton > button {
    background: #5B7FFF !important; color: #FFFFFF !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    font-size: 0.95rem !important; padding: 0.65rem 2rem !important;
    width: 100% !important;
  }
  .stButton > button:hover { background: #4A6EEE !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; }
</style>""", unsafe_allow_html=True)


def result_panel(icon, icon_cls, title, content):
    st.markdown(f"""
<div class="result-panel">
  <div class="result-header">
    <div class="result-icon {icon_cls}">{icon}</div>
    <span class="result-title">{title}</span>
  </div>
  <div class="result-body">{content}</div>
</div>""", unsafe_allow_html=True)


STEPS = [
    ("01", "Search Agent",  "Gathers recent web information"),
    ("02", "Reader Agent",  "Scrapes & extracts deep content"),
    ("03", "Writer Chain",  "Drafts the full research report"),
    ("04", "Critic Chain",  "Reviews & scores the report"),
]


def render_pipeline(active=-1, done_up_to=0):
    html = '<div style="padding: 1rem 0;"><div class="pipeline-title">Pipeline</div>'
    for i, (num, name, desc) in enumerate(STEPS):
        if i < done_up_to:
            cls = "done"
            badge_cls = "badge-done"
            badge = "&#10003; DONE"
        elif i == active:
            cls = "active"
            badge_cls = "badge-active"
            badge = "&#9881; RUNNING"
        else:
            cls = ""
            badge_cls = "badge-waiting"
            badge = "WAITING"
        html += f"""
        <div class="step-card {cls}">
          <div class="step-num">{num}</div>
          <div class="step-name">{name}</div>
          <div class="step-desc">{desc}</div>
          <div class="step-badge {badge_cls}">{badge}</div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False

st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Multi-Agent Research System</div>
  <h1 class="hero-title">Deep Research,<br><span>On Demand</span></h1>
  <p class="hero-sub">Enter any topic. Four specialised agents will search, scrape, write, and critique a full research report for you.</p>
</div>""", unsafe_allow_html=True)

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">Research Topic</div>', unsafe_allow_html=True)
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        topic = st.text_input(
            label="topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            disabled=st.session_state.running,
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        run_clicked = st.button(
            "Run Research" if not st.session_state.running else "Running...",
            disabled=st.session_state.running or not topic.strip(),
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    pipeline_placeholder = st.empty()
    with pipeline_placeholder.container():
        render_pipeline(active=-1, done_up_to=0)

if run_clicked and topic.strip():
    st.session_state.running = True
    st.session_state.results = None

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    status_placeholder = st.empty()

    from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

    state = {}

    try:
        # Stage 1: Search
        with pipeline_placeholder.container():
            render_pipeline(active=0, done_up_to=0)
        status_placeholder.info("Search Agent is working...")

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result["messages"][-1].content

        # Stage 2: Reader
        with pipeline_placeholder.container():
            render_pipeline(active=1, done_up_to=1)
        status_placeholder.info("Reader Agent is scraping top resources...")

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result["messages"][-1].content

        # Stage 3: Writer
        with pipeline_placeholder.container():
            render_pipeline(active=2, done_up_to=2)
        status_placeholder.info("Writer is drafting the report...")

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })

        # Stage 4: Critic
        with pipeline_placeholder.container():
            render_pipeline(active=3, done_up_to=3)
        status_placeholder.info("Critic is reviewing the report...")

        state["feedback"] = critic_chain.invoke({"report": state["report"]})

        # All done
        with pipeline_placeholder.container():
            render_pipeline(active=-1, done_up_to=4)
        status_placeholder.success("Pipeline complete!")

        st.session_state.results = state

    except Exception as e:
        status_placeholder.error(f"Pipeline error: {e}")

    finally:
        st.session_state.running = False

if st.session_state.results:
    r = st.session_state.results
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("#### Results")

    tab_report, tab_search, tab_scrape, tab_critic = st.tabs([
        "Final Report", "Search Results", "Scraped Content", "Critic Feedback"
    ])
    with tab_report:
        result_panel("📄", "icon-report", "Research Report", r.get("report", ""))
    with tab_search:
        result_panel("🔍", "icon-search", "Search Agent Output", r.get("search_results", ""))
    with tab_scrape:
        result_panel("📖", "icon-scrape", "Scraped Content", r.get("scraped_content", ""))
    with tab_critic:
        result_panel("🔎", "icon-critic", "Critic Feedback", r.get("feedback", ""))

    st.download_button(
        label="Download Report as .txt",
        data=r.get("report", ""),
        file_name=f"research_report_{int(time.time())}.txt",
        mime="text/plain",
    )
