from fastapi import FastAPI, Header, HTTPException
import re

app = FastAPI()

API_KEY = "baby123"

@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    message = data.get("message", "").lower()

    scam_words = ["otp", "blocked", "verify", "link", "upi"]
    scam_detected = any(word in message for word in scam_words)

    # extraction
    urls = re.findall(r"https?://\S+", message)
    upi_ids = re.findall(r"\b\w+@\w+\b", message)

    return {
        "scam_detected": scam_detected,
        "scam_type": "Phishing" if scam_detected else "Unknown",
        "honeypot_active": scam_detected,
        "honeypot_reply": "I’m confused 😟 can you explain again?",
        "confidence_score": 0.85 if scam_detected else 0.2,
        "extracted_data": {
            "urls": urls,
            "upi_ids": upi_ids
        }
    }

