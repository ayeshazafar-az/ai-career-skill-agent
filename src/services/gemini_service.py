import google.generativeai as genai
import json
import os
import streamlit as st

def clean_json_response(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Gemini API Key missing in environment")
        return None
    genai.configure(api_key=api_key)
    # Using flash model for fast structured output
    # By specifying response_mime_type, we force strict JSON
    return genai.GenerativeModel('gemini-3.5-flash-lite', generation_config={"response_mime_type": "application/json"})

def extract_candidate_skills(resume_text):
    """
    Extracts and normalizes skills from the resume, assigning an evidence level.
    Returns a list of structured skill dictionaries.
    """
    model = get_gemini_client()
    if not model:
        return []
    
    prompt = f"""
    You are an expert technical recruiter and skill gap analyst.
    Analyze the following resume and extract all technical skills.
    Normalize the skills (e.g. Postgres -> PostgreSQL, React.js -> React).
    Categorize into: 'Core Foundations', 'Languages & Frameworks', 'Tools & DevOps'.
    For each skill, determine its evidence level:
    - 2 (Demonstrated): Backed by project descriptions, metrics, or work experience.
    - 1 (Theoretical): Present only in a bulleted skills list or coursework with no proof.
    
    Output strictly as JSON in this format:
    {{
       "skills": [
          {{
              "name": "Skill Name",
              "category": "Category",
              "evidence_level": 1 or 2,
              "justification": "Short reason for the evidence level"
          }}
       ]
    }}
    
    Resume Text:
    {resume_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = clean_json_response(response.text)
        return result.get("skills", [])
    except Exception as e:
        st.error(f"Error extracting candidate skills: {e}")
        return []

def extract_market_skills(jd_texts):
    """
    Extracts and normalizes required skills from a list of job descriptions.
    Returns a flat list of normalized skill names per JD, or aggregated.
    """
    model = get_gemini_client()
    if not model:
        return []

    combined_jds = "\n\n--- NEXT JD ---\n\n".join(jd_texts)
    
    prompt = f"""
    You are an expert technical recruiter and talent market analyst.
    Analyze the following job descriptions and extract all REQUIRED and PREFERRED technical skills.
    Normalize the skills to standard names (e.g. Postgres -> PostgreSQL, React.js -> React).
    Maintain the mapping of skills to each job description so we can count frequency.
    
    Output strictly as JSON in this format:
    {{
       "jd_analysis": [
          {{
              "jd_index": 1,
              "skills": ["React", "Node.js", "PostgreSQL"]
          }}
       ]
    }}
    
    Job Descriptions:
    {combined_jds}
    """
    
    try:
        response = model.generate_content(prompt)
        result = clean_json_response(response.text)
        return result.get("jd_analysis", [])
    except Exception as e:
        st.error(f"Error extracting market skills: {e}")
        return []
