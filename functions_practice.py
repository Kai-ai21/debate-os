def proponent_agent(decision: str) -> str:
    return f"Regarding '{decision}': I strongly argue FOR this because it creates opportunities."

print(proponent_agent("Should I quit college?"))
print(proponent_agent("Should I learn AI?"))
print(proponent_agent("Should I start a startup?"))