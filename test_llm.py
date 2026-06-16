import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# -------------------------
# PROONENT AGENT
# -------------------------

proponent_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
You are the Proponent Agent in a structured debate.

Your ONLY job is to argue strongly FOR the decision.

Give exactly 3 specific, concrete reasons.

Be persuasive, not balanced.
"""
)

decision = """
Should I drop out of IITM?

Context:
I have a startup idea,
6 months of runway,
and a team of 2.
"""

print("Generating Proponent argument...")

proponent_response = proponent_model.generate_content(decision)

proponent_output = proponent_response.text

# -------------------------
# CRITIC AGENT
# -------------------------

critic_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
You are the Critic Agent in a structured debate.

Your ONLY job is to argue strongly AGAINST the decision.

Give exactly 3 specific objections.

Attack weaknesses in the Proponent's reasoning.
"""
)

critic_input = f"""
Decision:
{decision}

Proponent Argument:
{proponent_output}
"""

print("Generating Critic argument...")

critic_response = critic_model.generate_content(critic_input)

critic_output = critic_response.text

# -------------------------
# PRINT RESULTS
# -------------------------

print("\n" + "=" * 60)
print("PROPONENT OUTPUT")
print("=" * 60)
print(proponent_output)

print("\n" + "=" * 60)
print("CRITIC OUTPUT")
print("=" * 60)
print(critic_output)

total_tokens = (
    proponent_response.usage_metadata.total_token_count
    + critic_response.usage_metadata.total_token_count
)

print(f"\nTotal Tokens Used: {total_tokens}")
