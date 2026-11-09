"""Offline mock LLM response layer for demonstration; no external API required."""
from src.pipeline import answer_with_policy, clean_and_load

def ask(question):
    _, _, _, policies = clean_and_load()
    return answer_with_policy(question, policies)

if __name__ == "__main__":
    question = input("Ask a customer support question: ")
    print(ask(question))
