debate_state = {
    "decision": "Should I learn AI or Embedded Systems?",
    "proponent_output": "",
    "critic_output": "",
    "confidence_score": 0
}

print(debate_state["decision"])

debate_state["proponent_output"] = "AI has far more job opportunities in 2025."

print(f"The Proponent argued: {debate_state['proponent_output']}")