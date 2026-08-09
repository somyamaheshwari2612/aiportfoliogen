import os
import json
import re
from google import genai

def generate_portfolio_json(resume_text, prompt):
    """
    Implements the Gemini API call using google-genai.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please configure .env")

    client = genai.Client(api_key=api_key)
    
    full_prompt = f"{prompt}\n\nHere is the user's resume text to parse and convert:\n{resume_text}"
    
    try:
        # Use application/json to enforce JSON response formatting
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        )
    except Exception as e:
        raise RuntimeError(f"Failed to communicate with Gemini API: {e}")
        
    if not response or not response.text:
        raise ValueError("Received empty response from Gemini API.")
        
    text = response.text.strip()
    
    # Robustly extract the JSON block to ignore any conversational filler
    # Finds the first '{' and the last '}'
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
        text = text[start_idx:end_idx+1]
        
    text = text.strip()
    
    # Sometimes Gemini hallucinates markdown list dashes before JSON keys when it gets confused
    # e.g., `, - "technologies":` instead of `, "technologies":`
    text = re.sub(r'([{,])\s*-\s*"', r'\1 "', text)
    
    try:
        data = json.loads(text)
        
        # Check if the AI determined this is not a resume
        if data.get("is_resume") is False:
            reason = data.get("rejection_reason", "Hold up! 🛑 This doesn't look like a resume! Please upload a valid resume.")
            raise ValueError(reason)
            
        return data
    except json.JSONDecodeError:
        raise ValueError("Gemini returned incomplete JSON. Please try again.")

