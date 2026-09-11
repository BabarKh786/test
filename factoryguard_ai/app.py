import streamlit as st
from pathlib import Path
from database.db import init_db
from database.repository import create_factory, get_factory, list_documents, list_findings, list_actions
from rag.ingest import ingest_uploaded_documents
from analysis.router import analyze_input
from ui.dashboard import render_dashboard
from ui.knowledge_base import render_knowledge_base
from ui.audit import render_audit
from ui.findings import render_findings
from ui.corrective_actions import render_corrective_actions
from ui.reports import render_reports

st.set_page_config(page_title="FactoryGuard AI", page_icon="🛡️", layout="wide")

init_db()

if "factory_id" not in st.session_state:
    st.session_state.factory_id = None

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
.metric-card {padding: 1rem; border: 1px solid rgba(128,128,128,.25); border-radius: 14px;}
.small-muted {color: #777; font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ FactoryGuard")
    st.caption("AI Food Safety & Quality Assistant")
    page = st.radio("Navigate", [
        "Dashboard", "AI Audit", "Knowledge Base",
        "Findings", "Corrective Actions", "Reports"
    ])
    st.divider()
    st.caption("Powered by GPT-OSS 120B via Groq • FAISS RAG")

if not st.session_state.factory_id:
    st.title("Set up your factory")
    st.write("Create a lightweight factory profile. You can start analysis after this.")
    with st.form("factory_setup"):
        name = st.text_input("Factory / Business Name *")
        business_type = st.selectbox("Business Type *", ["Bakery", "Dairy", "Beverage", "Snacks", "Restaurant / Cloud Kitchen", "Meat / Poultry", "Other"])
        product = st.text_input("Primary Food Product *")
        country = st.text_input("Country *", value="Pakistan")
        submitted = st.form_submit_button("Create Factory", type="primary")
    if submitted:
        if not all([name.strip(), product.strip(), country.strip()]):
            st.error("Please complete all required fields.")
        else:
            st.session_state.factory_id = create_factory(name.strip(), business_type, product.strip(), country.strip())
            st.rerun()
    st.stop()

factory = get_factory(st.session_state.factory_id)

if page == "Dashboard":
    render_dashboard(factory)
elif page == "Knowledge Base":
    render_knowledge_base(factory)
elif page == "AI Audit":
    render_audit(factory)
elif page == "Findings":
    render_findings(factory)
elif page == "Corrective Actions":
    render_corrective_actions(factory)
elif page == "Reports":
    render_reports(factory)
