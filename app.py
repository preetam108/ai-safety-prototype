import streamlit as st
import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_risk(task):
    blocked = ["hack", "illegal", "attack", "fraud"]
    return any(word in task.lower() for word in blocked)


st.set_page_config(page_title="AI Safety System")

st.title("🛡️ AI Safety Prototype")
st.caption("Monitor • Block • Learn")

task = st.text_area("Enter Task")

if st.button("Run Agent"):

    if task.strip() == "":
        st.warning("Enter a task first")
    else:

        risk = check_risk(task)

        memory = load_memory()

        memory.append({
            "task": task,
            "risk": risk
        })

        save_memory(memory)

        if risk:
            st.error("❌ Blocked: Risk Detected")
        else:
            st.success("✅ Safe: Task Approved")
            st.write("Agent executed safely")


st.subheader("📚 Learning History")

for i, item in enumerate(load_memory()):
    st.write(f"{i+1}. {item['task']} | Risk: {item['risk']}")
