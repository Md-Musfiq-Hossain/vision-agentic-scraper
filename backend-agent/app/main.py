from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware
from app.browser.automation import VisionBrowser
from app.schemas.coordinate import ScrapeRequest  

app = FastAPI(title="Vision-Agentic Scraper - Agent Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Vision-Agentic Scraper - backend-agent"}

@app.post("/api/v1/ingest")
async def ingest_page_layout(payload: ScrapeRequest):
    browser_engine = VisionBrowser()
    result = await browser_engine.capture_page_snapshot(str(payload.url)) 
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error occurred."))
        
    return result