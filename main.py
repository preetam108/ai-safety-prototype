import json
from datetime import datetime

MEMORY_FILE = "memory.json"

# Load past learning
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save learning
def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Risk checker (Policy Gate)
def check_risk(task):
    risky_words = ["hack", "steal", "attack", "bypass", "illegal"]
    for word in risky_words:
        if word in task.lower():
            return "HIGH"
    return "LOW"

# Main agent loop
def run_agent(task):
    memory = load_memory()

    risk = check_risk(task)

    log = {
        "time": str(datetime.now()),
        "task": task,
        "risk": risk
    }

    memory.append(log)
    save_memory(memory)

    return risk


if __name__ == "__main__":
    print("AI Safety Agent Started")

    while True:
        task = input("Enter task: ")

        risk = run_agent(task)

        print("Risk Level:", risk)

        if risk == "HIGH":
            print("⚠️ Blocked by Safety Layer")
        else:
            print("✅ Allowed")
