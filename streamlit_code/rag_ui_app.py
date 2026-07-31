"""Streamlit UI for RAG System"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add the workspace path to sys.path so we can import rag_core
workspace_path = "/Workspace/Users/draxop7536@gmail.com/RAG_1"
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)

from rag_core import initialize_rag_system

# Page configuration
st.set_page_config(
    page_title="RAG Q&A System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 RAG Question Answering System</h1>', unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
    st.session_state.initialized = False
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY1", ""),
        help="Enter your Groq API key or set GROQ_API_KEY1 environment variable"
    )
    
    # Vector store path
    vector_store_path = st.text_input(
        "Vector Store Path",
        value="/Workspace/Users/draxop7536@gmail.com/RAG_1/Data/Vector_Store_3f5994b2",
        help="Path to your ChromaDB vector store"
    )
    
    # Model selection
    model_name = st.selectbox(
        "LLM Model",
        ["llama-3.1-8b-instant", "gemma2-9b-it", "llama3-70b-8192"],
        help="Select the Groq model to use"
    )
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        top_k = st.slider("Number of documents to retrieve", 1, 10, 5)
        min_score = st.slider("Minimum relevance score", 0.0, 1.0, 0.2, 0.05)
    
    st.markdown("---")
    
    # Initialize button
    if st.button("🚀 Initialize RAG System", type="primary", use_container_width=True):
        if not groq_api_key:
            st.error("❌ Please provide a Groq API key")
        elif not os.path.exists(vector_store_path):
            st.error(f"❌ Vector store path does not exist: {vector_store_path}")
        else:
            with st.spinner("Initializing RAG system..."):
                try:
                    rag_pipeline, retriever, embedding_mgr, vectorstore = initialize_rag_system(
                        vector_store_path=vector_store_path,
                        groq_api_key=groq_api_key,
                        model_name=model_name
                    )
                    st.session_state.rag_pipeline = rag_pipeline
                    st.session_state.retriever = retriever
                    st.session_state.initialized = True
                    st.success("✅ RAG system initialized successfully!")
                except Exception as e:
                    st.error(f"❌ Error initializing RAG system: {str(e)}")
    
    # System status
    st.markdown("---")
    st.subheader("📊 System Status")
    if st.session_state.initialized:
        st.success("🟢 System Ready")
        st.info(f"📝 Queries answered: {len(st.session_state.history)}")
    else:
        st.warning("🔴 System Not Initialized")
        st.info("Click 'Initialize RAG System' to start")

# Main content area
if not st.session_state.initialized:
    st.info("👈 Please configure and initialize the RAG system in the sidebar to begin.")
    
    # Example questions
    st.subheader("📝 Example Questions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - In which year was the new constitution adopted?
        - How many members did the Constituent Assembly originally have?
        - What are the fundamental rights in the constitution?
        """)
    with col2:
        st.markdown("""
        - Who was the chairman of the drafting committee?
        - What is Article 370 about?
        - When was the first amendment made?
        """)
else:
    # Query interface
    st.subheader("💬 Ask a Question")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["🔍 Query", "📚 Retrieved Documents", "📜 History"])
    
    with tab1:
        # Question input
        question = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="Type your question here...",
            key="question_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
        with col2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.rerun()
        
        if ask_button and question.strip():
            with st.spinner("🔍 Searching and generating answer..."):
                try:
                    result = st.session_state.rag_pipeline.query(
                        question=question,
                        top_k=top_k,
                        min_score=min_score
                    )
                    
                    # Store in history
                    st.session_state.history.append(result)
                    st.session_state.last_result = result
                    
                    # Display answer
                    st.markdown("### 💡 Answer")
                    st.success(result['answer'])
                    
                    # Display confidence
                    confidence = result['confidence']
                    if confidence >= 0.7:
                        confidence_class = "confidence-high"
                        emoji = "🟢"
                    elif confidence >= 0.4:
                        confidence_class = "confidence-medium"
                        emoji = "🟡"
                    else:
                        confidence_class = "confidence-low"
                        emoji = "🔴"
                    
                    st.markdown(
                        f'{emoji} <span class="{confidence_class}">Confidence: {confidence:.2%}</span>',
                        unsafe_allow_html=True
                    )
                    
                    # Display sources
                    if result['sources']:
                        st.markdown("### 📚 Sources")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"Source {i}: {source['source']} (Page {source['page']}) - Score: {source['score']:.2%}"):
                                st.text(source['preview'])
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        # Show retrieved documents from last query
        if 'last_result' in st.session_state and st.session_state.last_result['sources']:
            st.subheader("📄 Retrieved Documents (Last Query)")
            for i, source in enumerate(st.session_state.last_result['sources'], 1):
                st.markdown(f"**Document {i}**")
                st.markdown(f"- **Source:** {source['source']}")
                st.markdown(f"- **Page:** {source['page']}")
                st.markdown(f"- **Relevance Score:** {source['score']:.2%}")
                with st.expander("Show full preview"):
                    st.text(source['preview'])
                st.markdown("---")
        else:
            st.info("No documents retrieved yet. Ask a question in the Query tab.")
    
    with tab3:
        # Show query history
        st.subheader("📜 Query History")
        if st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history), 1):
                with st.expander(f"Query {len(st.session_state.history) - i + 1}: {item['question'][:100]}..."):
                    st.markdown(f"**Question:** {item['question']}")
                    st.markdown(f"**Answer:** {item['answer']}")
                    st.markdown(f"**Confidence:** {item['confidence']:.2%}")
                    st.markdown(f"**Sources:** {len(item['sources'])}")
        else:
            st.info("No query history yet.")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: gray; font-size: 0.9rem;">'
    '🤖 RAG System powered by Groq LLM | Built with Streamlit'
    '</div>',
    unsafe_allow_html=True
)
