"""Run the support ticket classification pipeline."""
from src.pipeline import clean_and_load, train_ticket_classifier
if __name__ == "__main__":
    _, _, tickets, _ = clean_and_load()
    _, accuracy = train_ticket_classifier(tickets)
    print(f"Ticket classifier test accuracy: {accuracy:.3f}")
