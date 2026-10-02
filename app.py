import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe UI Enhancements
st.markdown("""
<style>
    /* Safe Action Buttons */
    .stButton>button {
        border-radius: 30px !important; /* Pill shaped */
        border: none !important;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%) !important; /* Emerald to Blue */
        color: white !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        transition: transform 0.2s !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        color: white !important;
    }
    
    /* Differentiated UI Styles */
    .feature-card {
        background: rgba(255,255,255,0.02); /* Glass look */
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 4px solid #3b82f6; /* Accent left border */
        border-radius: 8px; /* Sharper corners */
        padding: 18px 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        background: rgba(255,255,255,0.05);
        transform: translateX(5px);
    }
    .feature-text h4 {
        color: #f8fafc;
        margin: 0 0 6px 0;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    .feature-text p {
        color: #cbd5e1;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .auth-header-circle {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #10b981, #0ea5e9);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
    }
    .pill-badge {
        background: transparent;
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 20px;
        border: 1px solid #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

from src.ui.dashboard import render_dashboard
from src.db.supabase_client import get_supabase_client

def render_auth_page():
    # Robust Custom HTML/CSS that doesn't depend on fragile Streamlit 'data-testid' tags.
    st.markdown("""
        <style>
        .glow-title {
            font-size: 4.5rem;
            font-weight: 900;
            background: -webkit-linear-gradient(45deg, #0ea5e9, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            letter-spacing: -3px;
            margin-bottom: 0px;
            padding-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.25rem;
            font-weight: 500;
            margin-bottom: 3.5rem;
            letter-spacing: 1px;
        }
        .feature-box {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-top: 4px solid #0ea5e9;
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .feature-box:hover {
            transform: translateY(-5px);
            background: rgba(30, 41, 59, 0.6);
        }
        .feature-box.purple { border-top-color: #8b5cf6; }
        .feature-box.pink { border-top-color: #ec4899; }
        .feature-box.emerald { border-top-color: #10b981; }
        
        div.stTabs [data-baseweb="tab-list"] {
            justify-content: center !important;
            gap: 20px;
            margin-bottom: 15px;
        }
        div.stTabs [aria-selected="true"] {
            border-bottom: 3px solid #0ea5e9 !important;
            color: white !important;
        }
        </style>
        
        <h1 class="glow-title">NeuralCore <span style="font-size: 2.5rem; vertical-align: super; background: none; -webkit-text-fill-color: #0ea5e9;">OS</span></h1>
        <p class="subtitle">Next-Generation Autonomous Career Intelligence</p>
    """, unsafe_allow_html=True)
    
    col1, col_center, col2 = st.columns([1, 1.4, 1])
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <div style="font-size: 2.2rem; margin-bottom: 10px;">🧩</div>
                <h4 style="color:#f8fafc; font-size:1.15rem; margin-bottom:5px; font-weight: 800;">Precision Match</h4>
                <p style="color:#94a3b8; font-size:0.95rem; line-height: 1.4;">Map unstructured resume skills dynamically directly to complex market tensors.</p>
            </div>
            <div class="feature-box purple">
                <div style="font-size: 2.2rem; margin-bottom: 10px;">⚡</div>
                <h4 style="color:#f8fafc; font-size:1.15rem; margin-bottom:5px; font-weight: 800;">Gemini Inference</h4>
                <p style="color:#94a3b8; font-size:0.95rem; line-height: 1.4;">Powered natively by Google's advanced multimodal LLM architecture framework.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_center:
        with st.container():
            tab_in, tab_up, tab_admin = st.tabs(["LOG IN", "REGISTER", "ADMINISTRATOR"])
            
            with tab_in:
                st.markdown("<br>", unsafe_allow_html=True)
                login_email = st.text_input("EMAIL ADDRESS", placeholder="candidate@neuralcore.ai", key="login_email")
                login_password = st.text_input("PASSWORD", type="password", key="login_pass")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Authenticate Platform", type="primary", use_container_width=True):
                    if not login_email or not login_password:
                        st.error("Credentials required.")
                    else:
                        client = get_supabase_client()
                        if client:
                            try:
                                res = client.auth.sign_in_with_password({"email": login_email, "password": login_password})
                                st.session_state["authenticated"] = True
                                st.session_state["user_email"] = login_email
                                user_metadata = res.user.user_metadata if res.user else {}
                                st.session_state["user_name"] = user_metadata.get("full_name", login_email.split('@')[0])
                                st.rerun()
                            except Exception as e:
                                st.error(f"Authentication Failed: {e}")
                        else:
                            st.session_state["authenticated"] = True
                            st.session_state["user_email"] = login_email
                            st.session_state["user_name"] = "Demo User"
                            st.rerun()
                            
            with tab_up:
                st.markdown("<br>", unsafe_allow_html=True)
                full_name = st.text_input("FULL NAME", placeholder="Jane Doe")
                profession = st.text_input("TARGET ALIGNMENT", placeholder="Data Scientist")
                reg_email = st.text_input("ACCOUNT EMAIL", placeholder="create@neuralcore.ai", key="reg_email")
                reg_password = st.text_input("SECURE PASSWORD", type="password", key="reg_pass")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Initialize Deep Profile", type="primary", use_container_width=True):
                    if not reg_email or not reg_password or not full_name:
                        st.error("Missing required metadata.")
                    else:
                        client = get_supabase_client()
                        if client:
                            try:
                                res = client.auth.sign_up({
                                    "email": reg_email, 
                                    "password": reg_password,
                                    "options": {"data": {"full_name": full_name, "profession": profession}}
                                })
                                st.success("Initialization valid. Proceed to LOG IN.")
                            except Exception as e:
                                st.error(f"Registration Failed: {e}")
                        else:
                            st.warning("Systems offline in preview mode.")
                            
            with tab_admin:
                st.markdown("<br>", unsafe_allow_html=True)
                st.error("Authorized personnel only. Intrusions will be logged to telemetry engine.")
                
                admin_email = st.text_input("OPERATOR ID", placeholder="sysadmin@neuralcore.ai", key="admin_e")
                admin_pass = st.text_input("PASSPHRASE", type="password", key="admin_p")
                admin_key = st.text_input("ROOT SECRETS", type="password", key="admin_k")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Establish Root Uplink", type="primary", use_container_width=True):
                    system_key = os.getenv("ADMIN_SECRET_KEY")
                    if admin_key == system_key and system_key:
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = admin_email
                        st.session_state["is_admin_session"] = True
                        st.rerun()
                    else:
                        st.error("Unauthorized. NeuralCore root validation failed.")
                        
    with col2:
        st.markdown("""
            <div class="feature-box pink">
                <div style="font-size: 2.2rem; margin-bottom: 10px;">🗺️</div>
                <h4 style="color:#f8fafc; font-size:1.15rem; margin-bottom:5px; font-weight: 800;">Autonomous Action</h4>
                <p style="color:#94a3b8; font-size:0.95rem; line-height: 1.4;">Generates hyper-personalized tactical project roadmaps to bridge gaps.</p>
            </div>
            <div class="feature-box emerald">
                <div style="font-size: 2.2rem; margin-bottom: 10px;">🛡️</div>
                <h4 style="color:#f8fafc; font-size:1.15rem; margin-bottom:5px; font-weight: 800;">Central Command</h4>
                <p style="color:#94a3b8; font-size:0.95rem; line-height: 1.4;">Live telemetry tracking and dynamic pre-computation dataset injection.</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    if not os.getenv("GEMINI_API_KEY"):
        st.warning("⚠️ GEMINI_API_KEY not found in .env")
        
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        
    if not st.session_state["authenticated"]:
        render_auth_page()
    else:
        user_email = st.session_state.get('user_email', "")
        
        # Universal Sign-Out Button
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        st.sidebar.markdown(f"<div style='font-size:0.8rem; color:#94a3b8; letter-spacing:1px; text-transform:uppercase;'>ACTIVE SESSION</div>", unsafe_allow_html=True)
        st.sidebar.markdown(f"<div style='font-weight:700; color:#38bdf8; margin-bottom:15px; word-break:break-all;'>{user_email}</div>", unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Disconnect Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
        # Secure Role Based Access Control (RBAC) 
        is_admin = False
        if st.session_state.get("is_admin_session", False):
            is_admin = True
        else:
            env_admin = os.getenv("ADMIN_EMAIL")
            if env_admin:
                is_admin = (user_email.lower() == env_admin.strip().lower())
            else:
                # Fallback if .env is missing the variable
                is_admin = "admin" in user_email.lower()
        
        if is_admin:
            st.sidebar.divider()
            st.sidebar.markdown("### 🛡️ Admin Module Active")
            
            from src.ui.admin_dashboard import render_admin_dashboard
            render_admin_dashboard()
        else:
            render_dashboard()

if __name__ == "__main__":
    main()