from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

import json
import traceback

from graph import build_debate_graph, DebateState


# ===================== CREATE APP =====================

app = FastAPI(
    title="Debate OS API",
    description="Multi-agent debate system powered by LangGraph and Gemini",
    version="1.0.0"
)


# ===================== CORS =====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================== BUILD GRAPH =====================

print("Building debate graph...")

debate_graph = build_debate_graph()

print("✓ Debate graph ready")


# ===================== PYDANTIC MODELS =====================

class DebateRequest(BaseModel):
    decision: str
    context: str = ""


# ===================== ENDPOINTS =====================

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "Debate OS API is live"
    }


@app.post("/debate")
async def run_debate(request: DebateRequest):

    # Business validation

    if not request.decision.strip():
        raise HTTPException(
            status_code=400,
            detail="Decision cannot be empty"
        )

    if len(request.decision) > 500:
        raise HTTPException(
            status_code=400,
            detail="Decision must be under 500 characters"
        )

    initial_state: DebateState = {
        "decision": request.decision,
        "context": request.context,
        "proponent_output": "",
        "critic_output": "",
        "moderator_output": {},
    }

    async def event_stream():

        try:

            yield {
                "event": "status",
                "data": "Starting debate..."
            }

            for step in debate_graph.stream(initial_state):

                node_name = list(step.keys())[0]
                update = step[node_name]

                if node_name == "proponent":

                    yield {
                        "event": "proponent",
                        "data": update.get("proponent_output", "")
                    }

                elif node_name == "critic":

                    yield {
                        "event": "critic",
                        "data": update.get("critic_output", "")
                    }

                elif node_name == "moderator":

                    mod_output = update.get("moderator_output", {})

                    yield {
                        "event": "moderator",
                        "data": json.dumps(mod_output)
                    }
            yield {
                "event": "done",
                "data": "Debate complete"
            }

        except Exception as e:

            traceback.print_exc()

            yield {
                "event": "error",
                "data": str(e)
            }

    return EventSourceResponse(event_stream())


# ===================== GLOBAL EXCEPTION HANDLER =====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )