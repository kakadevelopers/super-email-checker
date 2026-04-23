
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import dns.resolver

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Email Checker API is live!"}

@app.get("/check")
def check_email(email: str = Query(...)):
    try:
        domain = email.split("@")[1]
        answers = dns.resolver.resolve(domain, "MX")
        if answers:
            return {"email": email, "valid": True, "reason": "✅ Valid & Deliverable"}
    except:
        return {"email": email, "valid": False, "reason": "❌ Domain doesn't accept emails"}
