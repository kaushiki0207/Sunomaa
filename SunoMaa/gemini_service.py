import os
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))

# Keep the same model name to avoid changing output expectations.
MODEL_NAME = "gemini-2.5-flash"

import json

def analyze_symptoms(data: dict):

    prompt = f"""
You are a women's health assistant.

Patient Data:
Age: {data['age']}
Hot flashes: {data['hot_flashes']}
Mood swings: {data['mood_swings']}
Chest pain: {data['chest_pain']}
Sleep issues: {data['sleep_issue']}
Irregular periods: {data['irregular_period']}

Return STRICT JSON only in this format:

{{
  "risk_level": "LOW or MEDIUM or HIGH",
  "possible_cause": "short explanation",
  "lifestyle_advice": "short suggestions",
  "doctor_consult": "when to see doctor",
  "reassurance": "supportive message"
}}

Rules:
- If chest pain is False, do NOT mention emergency.
- If all symptoms are False, risk_level must be LOW.
- Keep response under 120 words.
- Return only valid JSON. No markdown.
"""

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    text = response.text.strip()

    # Remove accidental markdown ```json blocks
    if text.startswith("```"):
        text = text.split("```")[1]

    try:
        return json.loads(text)
    except:
        return {
            "risk_level": "UNKNOWN",
            "possible_cause": text,
            "lifestyle_advice": "",
            "doctor_consult": "",
            "reassurance": ""
        }
