from fastapi import FastAPI
import dns.resolver
import re

app = FastAPI()

def is_valid_email(email: str):
    # 1. Syntax check
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        return False, "❌ Invalid email format"

    # 2. Domain + MX Record check - REAL VALIDATION
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True, "✅ Valid & Deliverable"
    except:
        return False, "❌ Domain doesn't accept emails"

@app.get("/")
def home():
    return {"name": "Super Email Checker Pro", "status": "Live"}

@app.get("/check")
def check_email(email: str):
    valid, reason = is_valid_email(email)
    return {"email": email, "valid": valid, "reason": reason}
