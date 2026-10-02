import streamlit as st
import pandas as pd
import plotly.express as px

def render_candidate_radar_chart(gap_matrix):
    """
    Renders a stunning Plotly Polar Radar (Spider) chart comparing the candidate's
    proven skills against the market requirement frequency.
    """
    if not gap_matrix:
        st.warning("No gap matrix data available.")
        return
        
    # Take top 10 most demanded skills to avoid cluttering the radar
    sorted_matrix = sorted(gap_matrix, key=lambda x: x["frequency"], reverse=True)[:10]
    
    skills = []
    market_vals = []
    cand_vals = []
    
    for item in sorted_matrix:
        skills.append(item["skill"])
        market_vals.append(item["frequency"])
        # Normalize evidence level (0, 1, 2) to match the 0-100 scale of market frequency
        # 2 (Demonstrated) = 100, 1 (Theoretical) = 50, 0 (Missing) = 0
        cand_vals.append(item["evidence_level"] * 50)
        
    df = pd.DataFrame(dict(
        r = market_vals + cand_vals,
        theta = skills + skills,
        Entity = ['Market Standard']*len(skills) + ['Candidate Proficiency']*len(skills)
    ))
    
    fig = px.line_polar(
        df, 
        r='r', 
        theta='theta', 
        color='Entity', 
        line_close=True,
        color_discrete_sequence=['#38bdf8', '#10b981'],
        title="Candidate Fit vs. Market Demand"
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        title_font_size=20,
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_readiness_gauge(readiness_score):
    """
    Renders a simple metric for the readiness score.
    """
    st.metric(label="Overall Readiness Score", value=f"{readiness_score}%", delta="Target: 100%", delta_color="off")

def render_gap_matrix(gap_matrix):
    """
    Renders the color-coded gap matrix using pandas styler.
    """
    if not gap_matrix:
        st.warning("No gap matrix data available. Please run the analysis first.")
        return

    df = pd.DataFrame(gap_matrix)
    
    # Map evidence level to status strings
    level_map = {2: "Demonstrated", 1: "Theoretical", 0: "Missing"}
    df["Status"] = df["evidence_level"].map(level_map)
    
    display_df = df[["skill", "Status", "frequency", "category", "justification"]].copy()
    display_df.rename(columns={
        "skill": "Skill", 
        "frequency": "Market Freq (%)", 
        "category": "Category",
        "justification": "Evidence Details"
    }, inplace=True)
    
    def highlight_status(val):
        if val == 'Demonstrated':
            return 'background-color: rgba(34, 197, 94, 0.2); color: #16a34a;' 
        elif val == 'Theoretical':
            return 'background-color: rgba(234, 179, 8, 0.2); color: #d97706;' 
        elif val == 'Missing':
            return 'background-color: rgba(239, 68, 68, 0.2); color: #dc2626;' 
        return ''

    # Apply modern dynamic table styles that adapt to dark/light natively
    styled_df = display_df.style.map(highlight_status, subset=['Status'])
    
    st.dataframe(styled_df, use_container_width=True, height=500)
    
    high_priority = df[df["is_high_priority"]]
    if not high_priority.empty:
        st.subheader("🚨 High Priority Gaps")
        for _, row in high_priority.iterrows():
            st.error(f"**{row['skill']}** ({row['frequency']}% market demand) - Current Status: {level_map[row['evidence_level']]}")
