import warnings
# Suppress structural warning alerts right from line 1
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st
from graph import compiled_factory_graph

st.set_page_config(page_title="AI Content Factory", page_icon="🏭", layout="wide")
st.title("🏭 Multi-Agent Content Production Factory")
st.subheader("Orchestrated with LangGraph Self-Correction Loops & Gemini 2.5 Flash")

# User topic query text box
user_topic = st.text_input("Enter a technical topic for report production (e.g., 'Humanoid Robots market trends 2026'):")

if user_topic:
    log_col, doc_col = st.columns([1, 1])
    
    with log_col:
        st.markdown("### ⚙️ Factory Production Log")
        
        # Setup clean placeholder areas for live status step tracking updates
        r_status = st.empty()
        w_status = st.empty()
        c_status = st.empty()
        
        # 1. Initialize initial dict memory parameters for graph state ingestion
        initial_state = {
            "topic": user_topic,
            "research_notes": "",
            "article_draft": "",
            "critic_feedback": "",
            "loop_count": 0
        }
        
        r_status.info("🔄 Researcher: Crawling the live internet for data...")
        
        try:
            # 2. Execute the compiled LangGraph factory engine pipeline directly
            final_state = compiled_factory_graph.invoke(initial_state)
            
            r_status.success("✅ Researcher: Live fact extraction complete!")
            
            # Extract tracking metrics out of the completed state dictionary memory
            loops_run = final_state.get("loop_count", 1)
            raw_notes = final_state.get("research_notes", "No notes found.")
            final_report = final_state.get("article_draft", "No document compiled.")
            last_feedback = final_state.get("critic_feedback", "")
            
            # 3. Print structural log outputs depending on whether the loop triggered rewrites
            if loops_run > 1:
                w_status.warning(f"⚠️ Writer: Developed initial draft, but executed {loops_run - 1} revision loop cycles based on Critic notes.")
                c_status.error(f"❌ Critic Feedback Log:\n\n{last_feedback}")
            else:
                w_status.success("✅ Writer: Initial report draft met all production guidelines perfectly!")
                c_status.success("✅ Critic Assessment: Document approved instantly with zero formatting rejections!")
                
            with st.expander("🔎 Audit Raw Researcher Notes"):
                st.write(raw_notes)
                
        except Exception as e:
            st.error(f"Factory Pipeline Stopped: {str(e)}")
            final_report = ""

    with doc_col:
        st.markdown("### 📄 Completed Production Report")
        if final_report:
            st.markdown("---")
            st.markdown(final_report)
            st.markdown("---")
            st.balloons() # Play completion animation graphic
        else:
            st.info("Awaiting manufacturing workflow triggers to present document summaries.")
