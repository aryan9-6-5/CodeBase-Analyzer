import streamlit as st
import os
from core.error_analyzer import ErrorAnalyzer
from core.code_scanner import CodeScanner
from core.llm_client import GeminiClient

st.set_page_config(
    page_title="AI Code Detective", 
    page_icon="🕵️", 
    layout="wide"
)

st.title("🕵️ AI Code Detective")
st.markdown("Your Smart Debugging & Learning Partner")

# Initialize components
@st.cache
def init_components():
    return {
        'analyzer': ErrorAnalyzer(),
        'scanner': CodeScanner(),
        'llm': GeminiClient()
    }

components = init_components()

# Sidebar
st.sidebar.header("🔧 Tools")
mode = st.sidebar.radio(
    "Choose Mode",
    ["🐛 Debug Assistant", "🔍 Code Health Check", "🎓 Learning Chat"]
)

if mode == "🐛 Debug Assistant":
    st.header("Debug Your Code")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Upload Your Code")
        uploaded_file = st.file_uploader("Choose a Python file", type=['py'])
        
        if uploaded_file:
            code_content = uploaded_file.read().decode('utf-8')
            st.code(code_content, language='python')
    
    with col2:
        st.subheader("🔥 Paste Your Error")
        error_traceback = st.text_area(
            "Paste the full traceback here:",
            height=300,
            placeholder="Traceback (most recent call last):\n  File ..."
        )
    
    if st.button("🕵️ Analyze Error", type="primary"):
        if uploaded_file and error_traceback:
            with st.spinner("Analyzing your error..."):
                analysis = components['analyzer'].analyze_error(
                    code_content, 
                    error_traceback,
                    components['llm']
                )
                
                st.success("Analysis Complete!")
                
                # Display results
                st.subheader("🎯 Root Cause")
                st.write(analysis['root_cause'])
                
                st.subheader("🔧 Suggested Fix")
                st.code(analysis['suggested_fix'], language='python')
                
                st.subheader("🎓 Why This Happened")
                st.info(analysis['explanation'])
                
                st.subheader("💡 How to Avoid This")
                st.warning(analysis['prevention_tips'])
        else:
            st.error("Please upload a Python file and paste the error traceback.")

elif mode == "🔍 Code Health Check":
    st.header("Code Health Scanner")
    st.write("Upload a Python project to get quality insights and learning recommendations.")
    
    # TODO: Implement code health scanning
    st.info("🚧 Coming in Phase 2 - Code Health Scanning")
    
elif mode == "🎓 Learning Chat":
    st.header("Interactive Learning")
    st.write("Ask questions about your code and get personalized explanations.")
    
    # TODO: Implement interactive chat
    st.info("🚧 Coming in Phase 3 - Interactive Learning Chat")