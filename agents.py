import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.environ.get("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"


def call_gemini(system_prompt: str, user_message: str) -> str:
    """Single Gemini call. Returns the text response."""

    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_prompt
    )

    response = model.generate_content(user_message)

    return response.text


def proponent_agent(decision: str, context: str = "") -> str:
    """Argues FOR the decision."""

    system_prompt = """
You are the Proponent Agent in a structured multi-agent debate system.

YOUR ONLY JOB: Argue as strongly and specifically as possible FOR the decision.

STRICT RULES:
- Give exactly 3 arguments, each with a bold title
- Each argument: 2-3 sentences, specific to THIS decision
- Never mention risks, downsides, or "on the other hand"
- You are 100% committed to this decision being the right choice

FORMAT:
Argument 1: [Title]
[explanation]

Argument 2: [Title]
[explanation]

Argument 3: [Title]
[explanation]
"""

    context_section = (
        f"\n\nAdditional context: {context}"
        if context
        else ""
    )

    user_message = f"Decision: {decision}{context_section}"

    return call_gemini(system_prompt, user_message)


def critic_agent(
    decision: str,
    proponent_output: str,
    context: str = ""
) -> str:
    """Rebuts the Proponent and argues AGAINST."""

    system_prompt = """
You are the Critic Agent in a structured multi-agent debate.

YOUR ONLY JOB: Argue as strongly as possible AGAINST the decision.

You have been given the Proponent's argument.
ATTACK IT SPECIFICALLY.

STRICT RULES:
- Rebut each of the Proponent's 3 arguments by name
- Find the weakest assumption in each Proponent argument
- Never acknowledge any merit in the Proponent's position
- Be specific — quote or reference the Proponent's exact claims
- 2-3 sentences per rebuttal. Precise and surgical.

FORMAT:
Rebuttal to "[Argument Title]": [attack]

Counter-Argument:
[new point]
"""

    context_section = (
        f"\n\nAdditional context: {context}"
        if context
        else ""
    )

    user_message = f"""
Decision: {decision}{context_section}

The Proponent has argued:

--- PROPONENT ARGUMENT ---
{proponent_output}
--- END PROPONENT ARGUMENT ---

Now rebut these arguments specifically and argue AGAINST the decision.
"""

    return call_gemini(system_prompt, user_message)

def moderator_agent(
    decision: str,
    proponent_output: str,
    critic_output: str,
    context: str = ""
) -> dict:
    """Synthesizes debate. Returns structured dict with verdict."""

    system_prompt = """
You are the Moderator Agent in a structured debate system.

You have read both the Proponent and Critic arguments.

YOUR JOB: Find what BOTH sides missed. You are not a summarizer.

You are completely neutral. Your value is in surfacing blind spots and hidden assumptions.

RETURN ONLY VALID JSON. No markdown. No code blocks. No explanation. Just JSON.

Use this exact structure:

{
  "key_arguments_for": ["arg1", "arg2", "arg3"],
  "key_arguments_against": ["arg1", "arg2", "arg3"],
  "hidden_assumptions": ["assumption1", "assumption2"],
  "top_risks": ["risk1", "risk2", "risk3"],
  "blind_spots": ["non-obvious thing both missed"],
  "questions_to_answer_first": ["q1", "q2", "q3"],
  "verdict": "2-3 sentence balanced conclusion",
  "confidence_score": 7,
  "lean": "FOR or AGAINST or NEUTRAL"
}
"""

    context_section = (
        f"\n\nUser context: {context}"
        if context
        else ""
    )

    user_message = f"""
Decision: {decision}{context_section}

--- PROPONENT ARGUED ---
{proponent_output}

--- CRITIC ARGUED ---
{critic_output}

--- NOW PRODUCE YOUR JSON ANALYSIS ---
"""

    raw_response = call_gemini(
        system_prompt,
        user_message
    )

    cleaned = (
        raw_response
        .strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        return {
            "verdict": raw_response,
            "confidence_score": 5,
            "lean": "NEUTRAL",
            "error": True
        }
def run_debate(decision: str, context: str = "") -> dict:
    """Run the full debate pipeline. Returns complete debate_state dict."""

    debate_state = {
        "decision": decision,
        "context": context,
        "proponent_output": "",
        "critic_output": "",
        "moderator_output": {}
    }

    print("[1/3] Running Proponent Agent...")

    debate_state["proponent_output"] = proponent_agent(
        decision,
        context
    )

    print("✓ Proponent complete")

    print("[2/3] Running Critic Agent...")

    debate_state["critic_output"] = critic_agent(
        decision,
        debate_state["proponent_output"],
        context
    )

    print("✓ Critic complete")

    print("[3/3] Running Moderator Agent...")

    debate_state["moderator_output"] = moderator_agent(
        decision,
        debate_state["proponent_output"],
        debate_state["critic_output"],
        context
    )

    print("✓ Moderator complete")

    return debate_state

result = run_debate(
    "Should we rebuild our monolith as microservices?",
    "50k daily users, 8 engineers, deployment painful"
)

print("\n" + "=" * 60)
print("PROPONENT OUTPUT")
print("=" * 60)
print(result["proponent_output"])

print("\n" + "=" * 60)
print("CRITIC OUTPUT")
print("=" * 60)
print(result["critic_output"])

print("\n" + "=" * 60)
print("MODERATOR OUTPUT")
print("=" * 60)

print(
    json.dumps(
        result["moderator_output"],
        indent=2
    )
)

print(
    f"\n⚖️ Verdict: "
    f"{result['moderator_output'].get('verdict', 'N/A')}"
)

print(
    f"📊 Confidence: "
    f"{result['moderator_output'].get('confidence_score', '?')}/10"
)

print(
    f"📈 Lean: "
    f"{result['moderator_output'].get('lean', 'NEUTRAL')}"
)