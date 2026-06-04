import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st
from graph import compiled_graph

st.set_page_config(page_title="Autonomous Research Team", page_icon="🤖", layout="wide")
st.title("🤖 Autonomous Multi-Agent Research System")
st.subheader("Orchestrated with LangGraph & Gemini 2.5 Flash")

user_topic = st.text_input("Enter a complex research topic or query:")

if user_topic:
    log_col, output_col = st.columns([1, 2])
    
    with log_col:
        st.markdown("### ⚙️ Agent Execution Log Timeline")
        research_status = st.empty()
        writer_status = st.empty()
        
        research_status.info("🔄 Researcher Agent: Searching the live internet for facts...")
        initial_input_state = {"topic": user_topic, "research_notes": "", "final_article": ""}
        
        try:
            final_output_state = compiled_graph.invoke(initial_input_state)
            research_status.success("✅ Researcher Agent: Data extracted and notes cleaned!")
            writer_status.info("🔄 Writer Agent: Formatting notes into a cohesive article...")
            
            completed_report = final_output_state.get("final_article", "Failed to compile report.")
            raw_collected_notes = final_output_state.get("research_notes", "No notes found.")
            
            writer_status.success("✅ Writer Agent: Professional report compiled successfully!")
            
            with st.expander("🔎 Audit Raw Researcher Notes"):
                st.write(raw_collected_notes)
                
        except Exception as e:
            st.error(f"Execution failed: {str(e)}")
            completed_report = ""

    with output_col:
        st.markdown("### 📄 Completed Autonomous Research Report")
        if completed_report:
            st.markdown("---")
            st.markdown(completed_report)
            st.markdown("---")
            st.balloons()
        else:
            st.info("Awaiting workflow completion logs to output report summaries.")
