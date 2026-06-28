from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.browser.automation import VisionBrowser
from app.browser.vision_utils import CoordinateScaler
from app.schemas.coordinate import ScrapeRequest
from app.models.vlm_client import VisionModelClient

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
    return {"status": "ok", "service": "Vision-Agentic Scraper - Production Engine"}

@app.post("/api/v1/ingest")
async def ingest_page_layout(payload: ScrapeRequest):
    # 1. Capture web layout viewport screenshot
    browser_engine = VisionBrowser()
    browser_result = await browser_engine.capture_page_snapshot(str(payload.url))
    
    if not browser_result["success"]:
        raise HTTPException(status_code=500, detail=browser_result.get("error", "Browser automation failed to capture layout."))

    target = getattr(payload, "target_element", None)
    if not target:
        return browser_result

    # 2. Run multi-modal identification using OpenRouter (with max_tokens constraint)
    vlm = VisionModelClient()
    vlm_result = await vlm.analyze_screenshot(browser_result["base64_screenshot"], target)
    
    # Check if we were forced to fall back onto the mock layout due to upstream API outages
    if "Local Mock Recovery Engine" in vlm_result.get("provider_used", ""):
        return {
            "title": browser_result["title"],
            "current_url": browser_result["current_url"],
            "provider_used": vlm_result["provider_used"],
            "vlm_analysis": vlm_result["data"],
            "note": "Upstream cloud services are offline. Returning local safety boundaries."
        }
        
    if not vlm_result["success"]:
        raise HTTPException(status_code=502, detail=vlm_result.get("error", "VLM layout validation failed across all providers."))

    vlm_data = vlm_result["data"]
    
    # 3. Scale normalized VLM bounding output grid back to real absolute click paths
    if vlm_data.get("element_found") and "box_2d" in vlm_data:
        ymin, xmin, ymax, xmax = vlm_data["box_2d"]
        
        # Extrapolate geometric center coordinates
        center_x_model = (xmin + xmax) / 2
        center_y_model = (ymin + ymax) / 2
        
        absolute_click_point = CoordinateScaler.denormalize_from_vlm_grid(
            normalized_x = center_x_model,
            normalized_y = center_y_model,
            viewport_width = browser_result["viewport"]["width"],
            viewport_height = browser_result["viewport"]["height"]
        )
        vlm_data["absolute_click_target"] = absolute_click_point

    return {
        "title": browser_result["title"],
        "current_url": browser_result["current_url"],
        "provider_used": vlm_result["provider_used"],
        "vlm_analysis": vlm_data
    }