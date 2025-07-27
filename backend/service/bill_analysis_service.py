import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def analyze_bill(file_path):
    # Use Gemini API for image-to-text (upload image and prompt)
    with open(file_path, "rb") as img_file:
        img_bytes = img_file.read()
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "Extract all relevant bill details (items, quantity, price, date, vendor, total, etc) from this purchase bill image. Return as JSON."
    response = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": img_bytes}
    ], stream=False)
    full_text = response.text if hasattr(response, 'text') else str(response)
    # Try to parse JSON if possible, else fallback
    import json
    try:
        parsed = json.loads(full_text)
        details = parsed
        details["bill_image"] = file_path
        details["raw_text"] = full_text
    except Exception:
        # Try to extract JSON from inside code block in raw_text
        import re
        match = re.search(r"```json\\s*(\{.*?\})\\s*```", full_text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
                details = parsed
                details["bill_image"] = file_path
                details["raw_text"] = full_text
            except Exception:
                details = {
                    "item": "Could not parse",
                    "quantity": None,
                    "price": None,
                    "bill_image": file_path,
                    "raw_text": full_text
                }
        else:
            details = {
                "item": "Could not parse",
                "quantity": None,
                "price": None,
                "bill_image": file_path,
                "raw_text": full_text
            }
    return details
