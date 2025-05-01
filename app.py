import streamlit as st
import tempfile
import os
import json
from time import sleep
from Contract_analyssi_agent.agents import analyze_contract, load_document

st.set_page_config(
    page_title="AI Contract Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("📝 AI Contract Analyzer")

# Sidebar setup
with st.sidebar:
    st.header("Configuration")
    model = st.selectbox("Model", ["gpt-4o", "gpt-4", "gpt-3.5-turbo"], index=0)
    api_key = st.text_input("API Key", type="password")
    analysis_depth = st.select_slider("Analysis Depth", ["Basic", "Standard", "Comprehensive"], value="Standard")

# Upload document
uploaded_file = st.file_uploader("Upload Contract (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# Analysis button
if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name} ({round(uploaded_file.size / 1024, 2)} KB)")

    if st.button("🔍 Analyze Contract"):
        if not api_key:
            st.error("⚠️ Enter your API Key in the sidebar.")
            st.stop()

        os.environ["OPENAI_API_KEY"] = api_key

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getvalue())
            file_path = tmp.name

        status = st.status("Analyzing contract...", expanded=True)
        progress_bar = st.progress(0)

        try:
            status.update(label="Loading document...")
            contract_text = load_document(file_path)
            progress_bar.progress(0.2)

            status.update(label="Analyzing content...")
            max_tokens = {"Basic": 1000, "Standard": 2000, "Comprehensive": 4000}[analysis_depth]
            result = analyze_contract(contract_text, model_name=model, max_tokens=max_tokens)

            for i in range(3, 10):
                sleep(0.2)
                progress_bar.progress(i / 10)

            progress_bar.progress(1.0)
            status.update(label="✅ Analysis complete!", state="complete")

            st.session_state["result"] = result

        except Exception as e:
            status.update(label=f"❌ Analysis failed: {str(e)}", state="error")
            st.error(f"❌ Error: {str(e)}")

        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

# Display results
if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("Executive Summary")
    st.write(result.get("summary", "No summary available."))

    tabs = st.tabs(["Legal Analysis", "Risk Assessment", "Recommendations", "Key Clauses"])

    with tabs[0]:
        st.write(result.get("legal_analysis", "No legal analysis provided."))

    with tabs[1]:
        st.write(result.get("risk_assessment", "No risk assessment provided."))

    with tabs[2]:
        st.write(result.get("recommendations", "No recommendations provided."))

    with tabs[3]:
        clauses = result.get("clauses", [])
        if clauses:
            for clause in clauses:
                with st.expander(f"{clause['clause_type']} - {clause['importance']} Importance"):
                    st.markdown(f"**Clause Text:**\n{clause['clause_text']}")
                    if "explanation" in clause:
                        st.markdown(f"**Analysis:**\n{clause['explanation']}")
        else:
            st.write("No clauses analyzed.")

    # Export options
    st.download_button("Download JSON Report", json.dumps(result, indent=2), "report.json")