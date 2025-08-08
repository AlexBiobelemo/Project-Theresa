import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error: {e}")


def get_combined_prompt(resume_text, jd_text):
    """Creates a single, combined prompt for parsing and analysis."""
    return f"""
    You are an expert ATS and a highly accurate resume parsing system.
    Your task is to analyze the following resume and job description, and also parse the resume's structure.
    Provide a single, detailed JSON object as your response. Do not include any explanatory text before or after the JSON object.

    The JSON object must have two top-level keys: "analysis_results" and "structured_resume".

    1. The "analysis_results" object must contain:
      - "match_score": An integer from 0-100.
      - "missing_keywords": A list of strings.
      - "resume_suggestions": A list of objects, each with "original" and "rewritten" keys.
      - "cover_letter_themes": A list of strings.

    2. The "structured_resume" object must contain:
      - "full_name": "string"
      - "contact_info": {{ "email": "string", "phone": "string", "linkedin": "string", "address": "string" }}
      - "summary": "string"
      - "work_experience": [{{ "job_title": "string", "company": "string", "location": "string", "dates": "string", "responsibilities": ["string", ...] }}]
      - "education": [{{ "degree": "string", "institution": "string", "location": "string", "graduation_date": "string" }}]
      - "skills": ["string", ...]

    Job Description:
    ```
    {jd_text}
    ```

    Resume Text:
    ```
    {resume_text}
    ```

    Now, provide the complete analysis and parsing in the specified single JSON format.
    """


#AI Function
def get_combined_ai_data(resume_text, jd_text):
    """
    Sends the resume and JD to the Gemini API for combined analysis and parsing.
    Returns:
        A Python dictionary with all data, or an error dictionary.
    """
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = get_combined_prompt(resume_text, jd_text)

        response = model.generate_content(prompt)

        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")

        full_data = json.loads(cleaned_response)
        return full_data

    except Exception as e:
        print(f"An error occurred during combined AI processing: {e}")
        return {"error": f"Failed to get data from AI. Details: {e}"}



def generate_full_cover_letter(resume_text, jd_text):
    """Sends a request to the Gemini API to generate a full cover letter."""
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = get_cover_letter_prompt(resume_text, jd_text)

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print(f"An error occurred during cover letter generation: {e}")
        return {"error": f"Failed to generate cover letter from AI. Details: {e}"}


def get_ai_analysis():
    return None


def get_structured_resume():
    return None


def get_cover_letter_prompt(resume_text, jd_text):
    """Creates a dedicated prompt for generating a full cover letter."""
    return f"""
    You are a professional career writer and hiring manager.
    Your task is to write a complete, compelling, and professional cover letter based on the provided resume and job description.

    Instructions:
    1. The tone must be professional, confident, and enthusiastic.
    2. The letter must be structured with a clear introduction, body, and conclusion.
    3. In the body, you must connect specific experiences and skills from the resume directly to the key requirements mentioned in the job description. Do not just list skills; explain how they apply.
    4. Keep the letter concise, ideally around 3-4 paragraphs.
    5. Do not use placeholders like "[Company Name]" or "[Your Name]". Write a generic but complete letter that the user can easily edit. Start with "Dear Hiring Manager,".

    **Job Description:**
    ```
    {jd_text}
    ```

    **Resume Text:**
    ```
    {resume_text}
    ```

    Now, write the complete cover letter.,
    """