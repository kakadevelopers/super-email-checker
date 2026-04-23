from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import dns.resolver

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCAM_DOMAINS = {
    'paypaal.com': 'paypal.com',
    'hblbannk.com': 'hbl.com',
    'habibbannk.com': 'habibbank.com',
}

DISPOSABLE = ['mailinator.com', '10minutemail.com', 'tempmail.com', 'yopmail.com']

@app.get("/check")
def check_email(email: str):
    if '@' not in email:
        return {"email": email, "valid": False, "reason": "Invalid email format"}
    
    domain = email.split('@')[1]
    
    if domain in SCAM_DOMAINS:
        return {"email": email, "valid": False, "reason": f"⚠️ SCAM! Ye fake hai. Asli: {SCAM_DOMAINS[domain]}"}
    
    if domain in DISPOSABLE:
        return {"email": email, "valid": False, "reason": "❌ Temporary email, account mat banao"}
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return {"email": email, "valid": False, "reason": "Format galat hai"}
    
    try:
        dns.resolver.resolve(domain, 'MX')
        return {"email": email, "valid": True, "reason": "✅ Email valid hai"}
    except:
        return {"email": email, "valid": False, "reason": "Domain exist nahi karta"}

@app.get("/")
def home():
    return {"name": "Email Validator", "status": "live"}
