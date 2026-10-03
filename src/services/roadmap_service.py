import google.generativeai as genai
import os
import streamlit as st

def get_text_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3.5-flash-lite')

def generate_roadmap(gap_matrix):
    """
    Generates a project-first learning roadmap based on skill gaps.
    """
    model = get_text_model()
    if not model:
        return "⚠️ Gemini API key is missing. Please configure it in .env"
        
    high_priority = [g for g in gap_matrix if g.get("is_high_priority", False)]
    theoretical = [g for g in gap_matrix if g.get("evidence_level") == 1]
    
    gaps_summary = f"High Priority Missing/Theoretical Skills: {[g['skill'] for g in high_priority]}\n"
    gaps_summary += f"Theoretical Skills (Needs Project Proof): {[g['skill'] for g in theoretical]}"
    
    prompt = f"""
    You are an expert career coach and senior software architect.
    A candidate has the following skill gaps based on market demand:
    {gaps_summary}
    
    Generate a 3-step project-based learning roadmap to close these gaps.
    For each step, provide a specific, actionable micro-project that serves as proof of the skill.
    Focus on prerequisite logic (e.g., learn languages before frameworks).
    Keep it concise but highly actionable. Format nicely in markdown. Do not include generic advice.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating roadmap: {str(e)}"
        
def get_chat_response(messages, gap_matrix):
    """
    Responds to user questions using the gap matrix context.
    """
    model = get_text_model()
    if not model:
        return "⚠️ Gemini API key is missing. Please configure it in .env"
        
    context = "Candidate Skill Gaps Context from current analysis:\n"
    for g in gap_matrix:
        level_map = {2: "Demonstrated", 1: "Theoretical", 0: "Missing"}
        status = level_map.get(g.get('evidence_level'), "Unknown")
        context += f"- {g['skill']}: {g.get('frequency', 0)}% market demand, Candidate Status: {status}\n"
        
    system_prompt = f"""
    You are an AI Career Coach Agent embedded in a skill gap platform.
    Use the following gap matrix data to contextually answer the user's questions:
    {context}
    
    The user is asking you for career advice based on their current gap analysis.
    Be encouraging but data-driven. Keep answers very concise and professional.
    """
    
    history_text = system_prompt + "\n\n--- Conversation History ---\n"
    for m in messages:
        history_text += f"{m['role'].capitalize()}: {m['content']}\n"
    history_text += "Assistant: "
        
    try:
        response = model.generate_content(history_text)
        return response.text
    except Exception as e:
        return f"Error generating AI response: {str(e)}"
