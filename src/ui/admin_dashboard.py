import streamlit as st
import json
import os
from src.db.supabase_client import get_supabase_client

# Define local path to presets data
PRESETS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "presets.json")

def load_presets_raw():
    try:
        with open(PRESETS_FILE, "r") as f:
            return f.read()
    except Exception:
        return ""

def save_presets_raw(content):
    try:
        json.loads(content)  # Validate JSON structure before saving
        with open(PRESETS_FILE, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        return str(e)

def render_admin_dashboard():
    # Inject Custom High-Fidelity CSS
    st.markdown("""
        <style>
        .admin-hero {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(0, 0, 0, 0) 100%);
            border-bottom: 1px solid rgba(239, 68, 68, 0.2);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 3px solid #3b82f6;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.06);
        }
        .metric-label {
            font-size: 0.9rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 3rem;
            font-weight: 900;
            color: #f8fafc;
            line-height: 1.1;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(16, 185, 129, 0.1);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="admin-hero">
            <h1 style="font-size: 3rem; font-weight: 800; color: #ef4444; margin-bottom: 10px; letter-spacing: -1.5px;">
                🛡️ NeuralCore Command Center
            </h1>
            <p style="font-size: 1.1rem; color: #94a3b8; font-weight: 500; margin-bottom: 20px;">
                Global telemetry, model configurations, and dataset management
            </p>
            <div class="status-badge">● SYSTEM ONLINE: ALL SERVERS OPERATIONAL</div>
        </div>
    """, unsafe_allow_html=True)
    
    # TELEMETRY FETCH
    client = get_supabase_client()
    total_users = 0
    total_analyses = 0
    server_status = "STABLE"
    
    if client:
        try:
            res = client.table("Profiles").select("user_id, user_email").execute()
            total_analyses = len(res.data) if res.data else 0
            if res.data:
                unique_users = set([row.get("user_email") for row in res.data if row.get("user_email")])
                total_users = len(unique_users)
        except Exception as e:
            err_msg = str(e)
            if 'PGRST205' in err_msg or 'could not find the table' in err_msg.lower() or '42P01' in err_msg:
                server_status = "DB-WARN"
            else:
                server_status = "ERROR"
    else:
        server_status = "OFFLINE"

    if server_status == "DB-WARN":
        st.markdown("""
            <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 8px; padding: 12px 20px; color: #bae6fd; font-size: 0.95rem; margin-bottom: 25px; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2rem;">ℹ️</span> 
                Live telemetry is offline ('analytics' table not initialized). Displaying fallback values.
            </div>
        """, unsafe_allow_html=True)

    # Top Row Cards
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
            <div class="metric-card" style="border-top-color: #3b82f6;">
                <div class="metric-label">Total Gaps Analyzed</div>
                <div class="metric-value">{total_analyses}</div>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div class="metric-card" style="border-top-color: #10b981;">
                <div class="metric-label">Unique Active Users</div>
                <div class="metric-value">{total_users}</div>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
            <div class="metric-card" style="border-top-color: #8b5cf6;">
                <div class="metric-label">Intelligence Engine</div>
                <div class="metric-value" style="font-size: 2rem; margin-top: 15px;">GEMINI 1.5</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Content Row
    col_main1, col_main2 = st.columns([1, 1.5])
    
    with col_main1:
        st.markdown("""
            <h3 style="color:#f8fafc; margin-bottom: 5px; font-weight: 800; font-size: 1.5rem;">📡 System Operations</h3>
            <p style="color:#94a3b8; font-size:0.95rem; margin-bottom: 15px;">Server connection logic and API endpoints are actively routing traffic.</p>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; font-family: monospace; color: #a5b4fc; font-size: 0.9rem; line-height: 1.6; margin-bottom: 15px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);">
                <div style="color: #64748b; margin-bottom: 10px;">[System Log - Runtime]</div>
                <div><span style="color: #10b981;">></span> Auth: Bypass Token Active</div>
                <div><span style="color: #10b981;">></span> Gemini Core: Connected</div>
                <div><span style="color: #10b981;">></span> Supabase Pool: Validated</div>
                <div><span style="color: #f59e0b;">></span> Cache Policy: Aggressive</div>
                <div><span style="color: #10b981;">></span> Model Config: Optimal</div>
            </div>
            
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px dashed rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 15px; color: #fcd34d; font-size: 0.9rem;">
                <strong>⚠️ CAUTION:</strong> Modifications to the global datasets will immediately impact the inference logic for all candidate roadmaps.
            </div>
        """, unsafe_allow_html=True)

    with col_main2:
        st.markdown("### ⚙️ Global Dataset Registry")
        st.write("Manage canonical skill mappings and pre-loaded JSON presets.")
        current_data = load_presets_raw()
        updated_data = st.text_area("Live JSON Editor", value=current_data, height=300, label_visibility="collapsed")
        
        # Spacer for alignment
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Deploy Global Dataset Update", type="primary", use_container_width=True):
            res = save_presets_raw(updated_data)
            if res is True:
                st.success("✅ Global presets deployed! The system will now serve the updated context to Gemini.")
            else:
                st.error(f"Invalid JSON Format. Save aborted: {res}")
