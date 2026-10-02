import streamlit as st
import json
import os
from src.services.gemini_service import extract_candidate_skills, extract_market_skills
from src.services.gap_engine import calculate_market_frequencies, analyze_gaps
from src.ui.charts import render_candidate_radar_chart, render_readiness_gauge, render_gap_matrix
from src.services.roadmap_service import generate_roadmap, get_chat_response
from src.db.supabase_client import save_analysis
from src.services.github_service import fetch_github_portfolio_context
import uuid

def load_presets():
    preset_path = os.path.join(os.path.dirname(__file__), "..", "data", "presets.json")
    try:
        with open(preset_path, "r", encoding="utf-8") as f:
            return json.load(f).get("presets", [])
    except Exception as e:
        st.error(f"Failed to load presets: {e}")
        return []

def process_analysis():
    with st.spinner("🧠 Analyzing Resume vs Target JDs... (Extracting Market Tensors)"):
        resume_text = st.session_state["resume_text"]
        jds = st.session_state["jds"]
        
        # 1. Extract candidate skills using Gemini strict JSON
        cand_skills = extract_candidate_skills(resume_text)
        
        # 2. Extract and format market skills using Gemini
        jd_analyses = extract_market_skills(jds)
        
        # 3. Mathematical Gap Engine
        freq = calculate_market_frequencies(jd_analyses)
        result = analyze_gaps(cand_skills, freq)
        
        st.session_state["gap_matrix"] = result["gap_matrix"]
        st.session_state["readiness_score"] = result["readiness_score"]
        st.session_state["market_frequencies"] = freq
        st.session_state["analysis_complete"] = True
        
        # 4. Save to Supabase (Background)
        if "user_id" not in st.session_state:
            st.session_state["user_id"] = str(uuid.uuid4())
        try:
            save_analysis(
                st.session_state["user_id"],
                st.session_state.get("user_email", "anonymous"),
                {"resume": resume_text[:500] + "...(truncated)", "target_role": st.session_state.get("selected_preset", "custom")}, 
                result["gap_matrix"]
            )
        except Exception:
            pass
            
        # Clear previous roadmap and chat history for new analysis
        if "roadmap" in st.session_state:
            del st.session_state["roadmap"]
        st.session_state.messages = []
        
        st.success("✅ Analysis Complete & Saved! Check the other tabs for your intelligence.")

def render_dashboard():
    # Inject Custom High-Fidelity Dashboard CSS
    st.markdown("""
        <style>
        .dash-hero {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(15, 23, 42, 0.3) 100%);
            border: 1px solid rgba(56, 189, 248, 0.15);
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
        }
        .step-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 5px solid #38bdf8;
            border-radius: 12px;
            padding: 20px 25px;
            margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        .step-header {
            font-size: 1.3rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 5px;
        }
        .step-desc {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 10px;
        }
        /* Style Streamlit Tabs for Candidate */
        div.stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background: rgba(15, 23, 42, 0.4);
            padding: 10px 20px 0px 20px;
            border-radius: 12px 12px 0 0;
            border: 1px solid rgba(255,255,255,0.05);
            border-bottom: none;
        }
        div.stTabs [data-baseweb="tab"] {
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        div.stTabs [aria-selected="true"] {
            color: #38bdf8 !important;
            border-bottom-color: #38bdf8 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Safe Hero Section
    st.markdown("""
        <div class="dash-hero">
            <h1 style="font-size: 3.8rem; font-weight: 900; letter-spacing: -1.5px; color: #f8fafc; margin-bottom: 10px;">
                ⚡ NeuralCore <span style="color: #38bdf8;">Intelligence</span>
            </h1>
            <p style="font-size: 1.15rem; font-weight: 400; color: #94a3b8; max-width: 650px; margin: 0 auto;">
                Eliminate the guesswork. Inject your context and let our inference engine dynamically map your precise skill deficiencies against real-world market intelligence.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Init state
    if "analysis_complete" not in st.session_state:
        st.session_state["analysis_complete"] = False
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📥 ENGINE INGESTION", 
        "📊 MARKET INTEL", 
        "🧩 GAP MATRIX", 
        "🗺️ AUTONOMOUS ACTION PLAN"
    ])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="step-card">
                <div class="step-header">⚙️ Phase 1: Establish Inference Baseline</div>
                <div class="step-desc">Establish the market requirement threshold by loading industry presets or pasting a specific Job Description.</div>
            </div>
        """, unsafe_allow_html=True)
        
        jd_mode = st.radio("Select Target Market Data Source:", ["🗂️ Pre-Loaded Industry Presets", "📝 Paste Custom JD"], horizontal=True)
        
        if jd_mode == "🗂️ Pre-Loaded Industry Presets":
            presets = load_presets()
            cols = st.columns(max(len(presets), 1))
            for i, preset in enumerate(presets):
                with cols[i]:
                    if st.button(f"Load '{preset['name']}'", use_container_width=True):
                        st.session_state["selected_preset"] = preset["id"]
                        st.session_state["jds"] = preset["job_descriptions"]
                        st.success(f"Loaded {len(preset['job_descriptions'])} canonical JDs into RAM.")
                        
            if "jds" in st.session_state and st.session_state["jds"]:
                with st.expander("👁️ Inspect Loaded Market Tensors (Raw Text)", expanded=False):
                    for idx, jd in enumerate(st.session_state["jds"]):
                        st.markdown(f"**Dataset {idx+1}:**\n{jd}")
        else:
            custom_jd = st.text_area("Paste a specific Job Description text here:", height=150, placeholder="The AI will scrape technical skills required explicitly from this text...")
            if custom_jd:
                st.session_state["jds"] = [custom_jd]
                st.session_state["selected_preset"] = "custom"
                    
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="step-card" style="border-left-color: #10b981;">
                <div class="step-header">👤 Phase 2: Inject Candidate Context</div>
                <div class="step-desc">Upload unstructured PDF data or raw text to be normalized by the Language Model.</div>
            </div>
        """, unsafe_allow_html=True)
        
        resume_mode = st.radio("Provide Context Payload:", ["Secure PDF Upload", "Raw Text Buffer"], horizontal=True, label_visibility="collapsed")
        resume_text_buffer = ""
        
        if resume_mode == "Secure PDF Upload":
            uploaded_file = st.file_uploader("Drop Resume PDF into extraction layer", type=["pdf"], label_visibility="collapsed")
            if uploaded_file is not None:
                import pypdf
                try:
                    pdf_reader = pypdf.PdfReader(uploaded_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    resume_text_buffer = text
                    st.success("PDF Extraction Successful — Ready for NLP pipeline!")
                    with st.expander("👁️ Verify Extracted Text Buffer"):
                        st.text(resume_text_buffer)
                except Exception as e:
                    st.error(f"Extraction Error: {e}")
        else:
            resume_text_buffer = st.text_area("Paste unstructured text matrix:", height=200, label_visibility="collapsed")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.session_state["github_url"] = st.text_input("🔗 Attach Live GitHub Portfolio (Optional):", placeholder="https://github.com/username")
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Centered massive run button
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            if st.button("🚀 INITIALIZE CORE INFERENCE PIPELINE", type="primary", use_container_width=True):
                if not resume_text_buffer:
                    st.warning("⚠️ Critical: Candidate context missing. Upload resume before executing.")
                elif "jds" not in st.session_state or not st.session_state["jds"]:
                    st.warning("⚠️ Critical: Market parameters missing. Load a Preset or Paste a JD.")
                else:
                    github_context = ""
                    if st.session_state.get("github_url"):
                        with st.spinner("🔗 Scraping Live GitHub Repositories..."):
                            github_context = fetch_github_portfolio_context(st.session_state["github_url"])
                            
                    st.session_state["resume_text"] = resume_text_buffer + "\n\n" + github_context
                    process_analysis()

    with tab2:
        st.header("Intelligence Radar & Scores")
        if st.session_state.get("analysis_complete"):
            col1, col2 = st.columns([1, 2])
            with col1:
                render_readiness_gauge(st.session_state.get("readiness_score", 0))
            with col2:
                render_candidate_radar_chart(st.session_state.get("gap_matrix", []))
        else:
            st.info("Run analysis in the Ingestion tab first.")
            
    with tab3:
        st.header("Skill Gap Matrix")
        if st.session_state.get("analysis_complete"):
            render_gap_matrix(st.session_state.get("gap_matrix", []))
        else:
            st.info("Run analysis in the Ingestion tab first.")
            
    with tab4:
        st.header("Project-First Roadmap")
        if st.session_state.get("analysis_complete"):
            if "roadmap" not in st.session_state:
                with st.spinner("🧠 Generating AI Roadmap based on gap priorities..."):
                    st.session_state["roadmap"] = generate_roadmap(st.session_state["gap_matrix"])
            
            st.markdown(st.session_state["roadmap"])
            
            st.markdown("---")
            st.subheader("💬 AI Career Agent")
            
            # Simple chat UI
            if "messages" not in st.session_state:
                st.session_state.messages = []
                
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    
            if prompt := st.chat_input("Ask about your gaps or roadmap (e.g. Why is Docker high priority?)..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                    
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = get_chat_response(st.session_state.messages, st.session_state.get("gap_matrix", []))
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.info("Run analysis in the Ingestion tab first.")
