import streamlit as st
from travel_agent import TravelAgent
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Check for required environment variables
if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not found in environment variables. Please create a .env file.")
    st.stop()

# Initialize the travel agent
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = TravelAgent()
        st.session_state.chat_history = []
    except Exception as e:
        st.error(f"Failed to initialize travel agent: {str(e)}")
        st.stop()

# Streamlit UI configuration
st.set_page_config(
    page_title="AI Travel Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stChatInput {position: fixed; bottom: 20px; width: 70%;}
    .stChatMessage {padding: 12px; border-radius: 8px;}
    .assistant-message {background-color: #f0f2f6;}
    .user-message {background-color: #e3f2fd;}
    .sidebar .sidebar-content {background-color: #f8f9fa;}
    </style>
    """, unsafe_allow_html=True)

# App Header
st.title("🌍 AI Travel Agent Pro")
st.markdown("""
    <div style='color: gray; margin-bottom: 20px;'>
    Get expert travel advice, hotel recommendations, and local insights for any destination worldwide.
    </div>
    """, unsafe_allow_html=True)

# Sidebar for quick access features
with st.sidebar:
    st.header("Quick Travel Tools")
    city = st.text_input("📍 Enter a city name", key="sidebar_city")
    
    if city:
        st.subheader(f"Tools for {city}")
        query_type = st.radio(
            "Select information type:",
            ["Famous Locations", "Hotels", "Distances", "Local Food"],
            index=0
        )
        
        if query_type == "Famous Locations":
            if st.button("Get Detailed City Guide", help="Comprehensive city overview"):
                with st.spinner(f"Researching the best of {city}..."):
                    response = st.session_state.agent.get_city_info(city)
                    st.session_state.chat_history.append(("system", f"City guide for {city}"))
                    st.session_state.chat_history.append(("assistant", response))
                    st.rerun()
        
        elif query_type == "Hotels":
            if st.button("Get Hotel Recommendations", help="Hotels for all budgets"):
                with st.spinner(f"Finding the best stays in {city}..."):
                    response = st.session_state.agent.get_hotels(city)
                    st.session_state.chat_history.append(("system", f"Hotels in {city}"))
                    st.session_state.chat_history.append(("assistant", response))
                    st.rerun()
        
        elif query_type == "Distances":
            col1, col2 = st.columns(2)
            with col1:
                location1 = st.text_input("From location", key="loc1")
            with col2:
                location2 = st.text_input("To location", key="loc2")
            
            if st.button("Calculate Travel Options"):
                with st.spinner(f"Finding best routes in {city}..."):
                    response = st.session_state.agent.get_distances(city, location1, location2)
                    st.session_state.chat_history.append(("system", 
                        f"Travel from {location1} to {location2} in {city}"))
                    st.session_state.chat_history.append(("assistant", response))
                    st.rerun()
        
        elif query_type == "Local Food":
            if st.button("Get Food Guide", help="Local dishes and best places to eat"):
                with st.spinner(f"Discovering culinary delights in {city}..."):
                    response = st.session_state.agent.get_food(city)
                    st.session_state.chat_history.append(("system", f"Food guide for {city}"))
                    st.session_state.chat_history.append(("assistant", response))
                    st.rerun()

# Main chat interface
st.header("Travel Planning Assistant")
st.markdown("Ask me anything about destinations, itineraries, or travel tips.")

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "assistant":
        with st.chat_message("assistant", avatar="🌍"):
            st.markdown(message)
    elif role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message)
    elif role == "system":
        with st.expander("📌 Pinned Information", expanded=False):
            st.markdown(message)

# User input with clear separation
user_input = st.chat_input("Ask me anything about travel...", key="chat_input")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    
    with st.chat_message("assistant", avatar="🌍"):
        with st.spinner("Researching your question..."):
            try:
                response = st.session_state.agent.general_conversation(user_input)
                st.markdown(response)
                st.session_state.chat_history.append(("assistant", response))
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append(("assistant", error_msg))