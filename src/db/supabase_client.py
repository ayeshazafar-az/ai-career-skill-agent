import os
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    
    if not url or not key or url == "your-supabase-project-url":
        # Missing or default configuration
        return None
        
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        return None

def save_analysis(user_id, user_email, profile_data, gap_matrix):
    """
    Saves the analysis to Supabase if configured.
    """
    client = get_supabase_client()
    if not client:
        return False
        
    try:
        client.table('Profiles').insert({
            "user_id": user_id,
            "user_email": user_email,
            "resume_text": profile_data.get("resume", ""),
            "target_role": profile_data.get("target_role", "unknown")
        }).execute()
        return True
    except Exception as e:
        print(f"PostgreSQL insert err: {e}")
        return False
