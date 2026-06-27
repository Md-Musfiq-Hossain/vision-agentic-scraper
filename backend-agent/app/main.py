from fastapi import FastAPI

app = FastAPI(title="Vision-Agentic Scraper - Agent Core")

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "backend-agent"}