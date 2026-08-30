"""
FastAPI REST Server for IP-SAKTI Sahayak
Provides endpoints to execute Layers 7, 8, and 9 and access the statutory registry.
"""

from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from .core.schema import (
    UpstreamAgentOutput,
    LanguageCode,
    AyurvedaCategory,
    Jurisdiction
)
from .core.mock_upstream import list_mock_scenarios, get_mock_scenario
from .core.constants import STATUTORY_REGISTRY, DOMAIN_GLOSSARY
from .pipeline import IPSaktiPipeline, PipelineExecutionResult

app = FastAPI(
    title="IP-SAKTI Sahayak API",
    description="Layers 7 (Verification), 8 (Confidence & Escalation), and 9 (Multilingual) for Ayurveda IP & Regulatory Compliance",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = IPSaktiPipeline()


class ProcessScenarioRequest(BaseModel):
    scenario_id: str
    target_language: Optional[LanguageCode] = LanguageCode.EN


class ProcessCustomRequest(BaseModel):
    product_name: str
    raw_user_query: str
    category: AyurvedaCategory
    ingredients: List[str] = []
    target_jurisdiction: Jurisdiction = Jurisdiction.INDIA
    target_language: Optional[LanguageCode] = LanguageCode.EN


@app.get("/api/scenarios")
def get_scenarios():
    return list_mock_scenarios()


@app.get("/api/scenarios/{scenario_id}")
def get_scenario_detail(scenario_id: str):
    try:
        data = get_mock_scenario(scenario_id)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/process-scenario", response_model=PipelineExecutionResult)
def process_scenario(req: ProcessScenarioRequest):
    try:
        upstream_data = get_mock_scenario(req.scenario_id)
        result = pipeline.process(upstream_data, target_language=req.target_language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/process-custom", response_model=PipelineExecutionResult)
def process_custom(req: ProcessCustomRequest):
    draft_text = (
        f"### IP & Regulatory Assessment: {req.product_name}\n\n"
        f"1. **Classification**: Evaluated under {req.category.value}.\n"
        f"2. **Patentability**: Assessed for novelty, inventive step, and Section 3(p) traditional knowledge exclusions.\n"
        f"3. **Licensing**: Subject to AYUSH Rule 158B manufacturing licensing requirements and Biological Diversity Act obligations."
    )

    upstream_data = UpstreamAgentOutput(
        query_id=f"QRY-CUSTOM-{os.urandom(2).hex().upper()}",
        raw_user_query=req.raw_user_query,
        product_name=req.product_name,
        detected_category=req.category,
        botanical_and_herbal_ingredients=req.ingredients,
        proposed_use_or_claim="Therapeutic / wellness formulation",
        target_jurisdiction=req.target_jurisdiction,
        synthesis_draft_text=draft_text,
        extracted_claims=[],
        citations_referenced=[],
        retrieved_evidence=[]
    )

    result = pipeline.process(upstream_data, target_language=req.target_language)
    return result


@app.get("/api/glossary")
def get_glossary():
    return DOMAIN_GLOSSARY


@app.get("/api/statutes")
def get_statutes():
    return STATUTORY_REGISTRY


# Mount static web UI if directory exists
web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
if os.path.exists(web_dir):
    app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")
