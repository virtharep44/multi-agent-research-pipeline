#  ResearchMind — Multi-Agent AI Research Pipeline

> **Automatically research any topic using a team of AI agents.**
> Powered by LangChain, LangGraph, Mistral AI, and Tavily. Deployed on Streamlit Community Cloud.

 


##  Live Demo
https://multi-agent-research-pipeline-gnksvyxgcpapayf8u4st8o.streamlit.app
 


##  What is ResearchMind?

ResearchMind is a multi-agent AI pipeline that takes any research topic and returns a fully written, structured research report — automatically. Instead of a single AI doing everything, four specialized agents work together in a pipeline orchestrated by LangGraph, each handling a distinct part of the research process.

Just type a topic (or speak it using voice input), hit **Research**, and get a complete report in seconds.

---

##  The Four Agents

| Agent | Role |

 🔍 **Search Agent** | Searches the web for relevant, up-to-date information using Tavily API |
📄 **Reader / Scraper Agent** | Reads and extracts detailed content from web pages |
✍️ **Writer Agent** | Synthesizes all findings into a clean, structured research report |
🎯 **Critic Agent** | Reviews the report and improves it for quality, accuracy, and clarity |

---

##  Features

- 🔎 **Real-time web search** via Tavily API
- 🤖 **Mistral AI** as the language model backbone ("mistral-small-latest" )
- 🔗 **LangGraph** for multi-agent orchestration and workflow management
- 🖥️ **Streamlit UI** with dark indigo/violet theming
- 📊 **Live step-by-step progress** — watch each agent work in real time
- 📑 **Tabbed results** — Report, Sources, and Raw Output views
- 📥 **Download your report** as a `.txt` file
- 🎙️ **Voice input** — speak your research query (Web Speech API)
- 🔊 **Text-to-speech output** — listen to the generated report

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [LangChain](https://langchain.com) | Agent framework and tooling |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Multi-agent workflow orchestration |
| [Mistral AI](https://mistral.ai) | Language model ("mistral-small-latest") |
| [Tavily](https://tavily.com) | Web search API |
| [Streamlit](https://streamlit.io) | UI and cloud deployment |
| Python 3.10+ | Core language |

---

##  Local Setup & Installation

### Prerequisites

- Python 3.10 or higher
- A [Mistral AI API key](https://console.mistral.ai/)
- A [Tavily API key](https://tavily.com)

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/virtharep44/multi-agent-research-pipeline.git
cd multi-agent-research-pipeline
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set up your API keys

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Step 4 — Run the app

```bash
streamlit run app.py
```

##  Project Structure

```
multi-agent-research-pipeline/
│
├── app.py              # Streamlit UI — main entry point
├── agents.py           # Agent definitions (Search, Reader, Writer, Critic)
├── pipeline.py         # LangGraph workflow orchestration
├── tools.py            # Tavily search and web scraping tools
├── requirements.txt    # Python dependencies
└── README.md


## Deploying to Streamlit Community Cloud

1. **Push your code** to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** → select your repository and `app.py`
4. Go to **Settings → Secrets** and add your keys:

```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

5. Click **Deploy** — your app will be live in minutes!


 

## 🙋‍♀️ Author

**[@virtharep44](https://github.com/virtharep44)**

Built from scratch as a hands-on AI project using LangChain, LangGraph, Mistral AI, Tavily, and Streamlit.

---

> ⭐ If you found this useful, consider starring the repo!
