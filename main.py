from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

import json
import traceback

from graph import build_debate_graph, DebateState

from database.database import SessionLocal          # ← NEW
from database import crud
from database.schemas import DebateCreate           # ← direct import                 # ← NEW


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

        # ── Accumulate state across stream steps ──────────── ← NEW
        accumulated = {                                        # ← NEW
            "proponent_output": "",                           # ← NEW
            "critic_output": "",                              # ← NEW
            "moderator_output": {},                           # ← NEW
        }                                                     # ← NEW

        try:

            yield {
                "event": "status",
                "data": "Starting debate..."
            }

            for step in debate_graph.stream(initial_state):

                node_name = list(step.keys())[0]
                update = step[node_name]

                if node_name == "proponent":

                    accumulated["proponent_output"] = update.get(   # ← NEW
                        "proponent_output", ""                       # ← NEW
                    )                                                # ← NEW

                    yield {
                        "event": "proponent",
                        "data": update.get("proponent_output", "")
                    }

                elif node_name == "critic":

                    accumulated["critic_output"] = update.get(      # ← NEW
                        "critic_output", ""                         # ← NEW
                    )                                               # ← NEW

                    yield {
                        "event": "critic",
                        "data": update.get("critic_output", "")
                    }

                elif node_name == "moderator":

                    mod_output = update.get("moderator_output", {})
                    print("\n===== MODERATOR OUTPUT =====")
                    print(json.dumps(mod_output, indent=2))
                    print("============================\n")

                    accumulated["moderator_output"] = mod_output    # ← NEW

                    yield {
                        "event": "moderator",
                        "data": json.dumps(mod_output)
                    }

            # ── Save to PostgreSQL after stream completes ─── ← NEW
            try:                                                     # ← NEW
                debate_data = DebateCreate(                 # ← NEW
                    topic=request.decision,                         # ← NEW
                    context=request.context or None,                # ← NEW
                    proponent_argument=accumulated["proponent_output"] or None,   # ← NEW
                    critic_argument=accumulated["critic_output"] or None,         # ← NEW
                    moderator_verdict=accumulated["moderator_output"].get(        # ← NEW
                        "verdict"                                   # ← NEW
                    ),                                              # ← NEW
                    decision=accumulated["moderator_output"].get(   # ← NEW
                        "decision"                                  # ← NEW
                    ),                                              # ← NEW
                    confidence_score=accumulated["moderator_output"].get(        # ← NEW
                        "confidence_score"                          # ← NEW
                    ),                                              # ← NEW
                    lean=accumulated["moderator_output"].get(       # ← NEW
                        "lean"                                      # ← NEW
                    ),                                              # ← NEW
                )                                                   # ← NEW
                                                                    # ← NEW
                db = SessionLocal()                                 # ← NEW
                try:                                                                 # ← NEW
                    saved = crud.create_debate(db, debate_data)     # ← NEW
                    debate_id = saved.id                            # ← NEW
                    db.close()                                      # ← NEW
                except Exception:                                   # ← NEW
                    db.rollback()                                   # ← NEW
                    db.close()                                      # ← NEW
                    raise                                           # ← NEW
                                                                    # ← NEW
                yield {                                             # ← NEW
                    "event": "saved",                              # ← NEW
                    "data": json.dumps({"debate_id": debate_id})   # ← NEW
                }                                                   # ← NEW
                                                                    # ← NEW
            except Exception as db_error:                          # ← NEW
                # DB failure does not kill the debate response.    # ← NEW
                # The frontend already received all content.       # ← NEW
                # Log the error and continue to the done event.   # ← NEW
                traceback.print_exc()                              # ← NEW
                yield {                                            # ← NEW
                    "event": "save_error",                        # ← NEW
                    "data": str(db_error)                         # ← NEW
                }                                                  # ← NEW

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