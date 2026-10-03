import streamlit as st
import json
import os
from src.db.supabase_client import get_supabase_client

PRESETS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "presets.json"
)


def load_presets_raw() -> str:
    try:
        with open(PRESETS_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def save_presets_raw(content: str):
    try:
        json.loads(content)   # Validate before writing
        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        return str(e)


def render_admin_dashboard():
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
        <div style="margin-bottom:2rem;">
            <h1 style="font-size:2rem;font-weight:800;color:#f1f5f9;
                       letter-spacing:-0.5px;margin-bottom:4px;">
                🛡️ Admin Panel
            </h1>
            <p style="color:#64748b;font-size:0.95rem;margin:0;">
                Telemetry, system status, and global dataset management.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── Telemetry ─────────────────────────────────────────────────────────────
    client = get_supabase_client()
    total_analyses = 0
    total_users    = 0
    db_status      = "connected"

    if client:
        try:
            res = client.table("Profiles").select("user_id, user_email").execute()
            rows = res.data or []
            total_analyses = len(rows)
            total_users    = len({r.get("user_email") for r in rows if r.get("user_email")})
        except Exception as e:
            err = str(e)
            db_status = "table_missing" if any(
                k in err for k in ("PGRST205", "42P01", "could not find")
            ) else "error"
    else:
        db_status = "offline"

    # Status indicator
    status_map = {
        "connected":    ("#10b981", "● Database connected"),
        "table_missing": ("#f59e0b", "⚠ Profiles table not found — run DB setup"),
        "error":        ("#ef4444", "✕ Database error"),
        "offline":      ("#64748b", "○ Supabase not configured (demo mode)"),
    }
    status_color, status_text = status_map.get(db_status, ("#64748b", "Unknown"))

    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
                    border-radius:8px;padding:10px 16px;margin-bottom:24px;
                    display:flex;align-items:center;gap:10px;">
            <span style="color:{status_color};font-size:0.85rem;font-weight:600;">
                {status_text}
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Metric cards
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Analyses", total_analyses)
    with m2:
        st.metric("Unique Users", total_users)
    with m3:
        st.metric("AI Engine", "Gemini 3.5")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Dataset Editor ────────────────────────────────────────────────────────
    st.markdown("#### ⚙️ Global Dataset Registry")
    st.markdown("""
        <p style="color:#64748b;font-size:0.88rem;margin-bottom:16px;">
            Edit the pre-loaded industry job description presets.
            Changes take effect immediately for all users.
            The JSON must be valid before saving.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.2);
                    border-radius:8px;padding:12px 16px;margin-bottom:16px;
                    font-size:0.85rem;color:#fcd34d;">
            ⚠️ Changes to these presets affect the inference pipeline for all candidates.
        </div>
    """, unsafe_allow_html=True)

    current_data = load_presets_raw()
    updated_data = st.text_area(
        "presets.json",
        value=current_data,
        height=400,
        label_visibility="collapsed",
    )

    col_save, col_reset, _ = st.columns([1, 1, 3])
    with col_save:
        if st.button("💾  Save Changes", type="primary", use_container_width=True):
            result = save_presets_raw(updated_data)
            if result is True:
                st.success("✅ Presets saved and deployed.")
            else:
                st.error(f"Invalid JSON — not saved: {result}")
    with col_reset:
        if st.button("↩  Reset", type="secondary", use_container_width=True):
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── System Info ───────────────────────────────────────────────────────────
    st.markdown("#### 📡 System Status")
    import os as _os

    checks = [
        ("Gemini API key",   bool(_os.getenv("GEMINI_API_KEY")),   "configured", "missing — AI features will fail"),
        ("Supabase URL",     bool(_os.getenv("SUPABASE_URL")),     "configured", "not set — using demo mode"),
        ("Admin secret key", bool(_os.getenv("ADMIN_SECRET_KEY")), "configured", "not set"),
    ]

    for label, ok, good_msg, bad_msg in checks:
        color = "#10b981" if ok else "#f59e0b"
        icon  = "✓" if ok else "⚠"
        msg   = good_msg if ok else bad_msg
        st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;
                        border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="color:{color};font-size:1rem;width:20px;">{icon}</span>
                <span style="color:#e2e8f0;font-size:0.88rem;font-weight:600;width:160px;">{label}</span>
                <span style="color:{color};font-size:0.82rem;">{msg}</span>
            </div>
        """, unsafe_allow_html=True)
