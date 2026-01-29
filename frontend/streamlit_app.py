import streamlit as st
import requests
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Agentic RAG Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API configuration
BACKEND_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 100%; 
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .status-online {
        background-color: #4caf50;
        color: white;
    }
    .status-offline {
        background-color: #f44336;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "metrics" not in st.session_state:
    st.session_state.metrics = {}

if "backend_status" not in st.session_state:
    st.session_state.backend_status = "checking"

# Check backend health
def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        if response.status_code == 200:
            return "online"
        return "offline"
    except:
        return "offline"

# Update backend status
st.session_state.backend_status = check_backend_health()

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 Agentic RAG")
    st.markdown("---")
    
    # System Status
    st.markdown("#### System Status")
    if st.session_state.backend_status == "online":
        st.markdown('<span class="status-badge status-online">● Online</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-offline">● Offline</span>', unsafe_allow_html=True)
        st.error("Backend is not running. Please start the FastAPI server.")
    st.markdown("")
    
    # Backend URL
    st.markdown("#### Backend Server")
    st.code(BACKEND_URL, language=None)
    
    # Conversation ID
    st.markdown("#### Conversation ID")
    st.code(st.session_state.conversation_id[:8] + "...", language=None)
    
    # New Chat button
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.metrics = {}
        st.rerun()
    
    st.markdown("---")
    
    # Performance Metrics
    if st.session_state.metrics:
        st.markdown("#### Performance Metrics")
        
        metrics = st.session_state.metrics
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Iterations", metrics.get("iterations", 0))
            st.metric("Tool Calls", metrics.get("tool_calls", 0))
        
        with col2:
            st.metric("Duration", f"{metrics.get('duration_seconds', 0):.2f}s")
            st.metric("Tokens", metrics.get("tokens_used", 0))
        
        # Search queries
        if metrics.get("search_queries"):
            st.markdown("**Search Queries:**")
            for i, query in enumerate(metrics["search_queries"], 1):
                st.markdown(f"{i}. {query}")
        
        # Tool latencies
        if metrics.get("tool_latency_ms"):
            st.markdown("**Tool Latencies:**")
            for item in metrics["tool_latency_ms"]:
                st.markdown(f"- {item['tool']}: {item['latency_ms']:.2f}ms")
        
        # Errors
        if metrics.get("errors", 0) > 0:
            st.error(f"❌ Errors: {metrics['errors']}")

    st.markdown("---")
    st.markdown("#### About")
    st.markdown("""
    This is an **Agentic RAG** system powered by:
    - FastAPI backend (port 8000)
    - OpenAI GPT models
    - ChromaDB vector storage
    - Streamlit frontend (port 8501)
    """)
    
    st.markdown("---")
    st.markdown("#### Actions")
    if st.button("🔄 Refresh Backend Status", use_container_width=True):
        st.session_state.backend_status = check_backend_health()
        st.rerun()

# Main chat interface
st.title("💬 Agentic RAG Chat")
st.markdown("Ask me anything about your documents!")

# Display warning if backend is offline
if st.session_state.backend_status == "offline":
    st.warning("⚠️ Backend server is not running. Please start it with: `uvicorn backend.main:app --reload`")

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me anything about your documents...", disabled=st.session_state.backend_status == "offline"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.markdown(f"""
    <div class="chat-message user-message">
        <strong>👤 You</strong><br>
        {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Generate response from backend
    with st.spinner("🤔 Thinking..."):
        try:
            # Call backend API
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "query": prompt,
                    "conversation_id": st.session_state.conversation_id
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_response = data.get("output", "No response generated")
                metrics = data.get("metrics", {})
                
                # Update metrics
                st.session_state.metrics = metrics
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
                # Rerun to display the new message
                st.rerun()
            else:
                error_message = f"Error: Backend returned status code {response.status_code}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                
        except requests.exceptions.Timeout:
            error_message = "Error: Request timed out. The backend might be processing a complex query."
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            
        except requests.exceptions.ConnectionError:
            error_message = "Error: Could not connect to backend. Please ensure the FastAPI server is running."
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Powered by FastAPI + Streamlit + OpenAI GPT & ChromaDB</div>",
    unsafe_allow_html=True
)
