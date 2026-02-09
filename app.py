import streamlit as st
import json
import os
import datetime


# ===============================
# CONFIG
# ===============================
MEMORY_FILE = "memory.json"


# ===============================
# MEMORY SYSTEM
# ===============================
def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_memory(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ===============================
# ADAPTIVE RISK ENGINE (FIXED)
# ===============================
def check_risk(task, memory):

    base_risky = ["hack", "illegal", "attack", "steal", "bypass"]

    text = task.lower()

    score = 0
    matched = []


    # Count ALL occurrences
    for word in base_risky:

        count = text.count(word)

        if count > 0:
            score += count * 20
            matched.append(f"{word} x{count}")


    # Learn from past BLOCKED tasks
    learned_words = []

    for item in memory:

        if item["status"] == "BLOCKED":

            learned_words.extend(
                item["task"].lower().split()
            )


    # Learning bonus
    for lw in set(learned_words):

        if lw in text:
            score += 10


    # Risk level decision
    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"


    return level, score, matched


# ===============================
# UI SETUP
# ===============================
st.set_page_config(
    page_title="AI Safety Prototype",
    layout="wide"
)

st.title("🛡️ AI Safety Prototype")
st.subheader("Monitor • Block • Learn • Evolve")


left, right = st.columns(2)

memory = load_memory()


# ===============================
# LEFT PANEL (INPUT)
# ===============================
with left:

    st.header("📝 Submit Task")

    task = st.text_area(
        "Enter Task",
        placeholder="Example: hack hack hack system"
    )

    submit = st.button("Run Safety Check")


    if submit and task.strip():

        level, score, matched = check_risk(task, memory)

        status = "ALLOWED"

        if level == "HIGH":
            status = "BLOCKED"


        record = {
            "time": str(datetime.datetime.now()),
            "task": task,
            "risk_level": level,
            "risk_score": score,
            "status": status,
            "matched": matched
        }


        memory.append(record)

        save_memory(memory)


        # SHOW RESULT
        if status == "BLOCKED":

            st.error(
                f"🚫 BLOCKED — Risk: {level} ({score})"
            )

        else:

            st.success(
                f"✅ ALLOWED — Risk: {level} ({score})"
            )


        if matched:

            st.warning(
                "🧩 Matched: " + ", ".join(matched)
            )



# ===============================
# RIGHT PANEL (DASHBOARD)
# ===============================
with right:

    st.header("📊 System Dashboard")


    total = len(memory)

    blocked = len([
        m for m in memory if m["status"] == "BLOCKED"
    ])

    allowed = total - blocked


    st.metric("Total Tasks", total)
    st.metric("Blocked", blocked)
    st.metric("Allowed", allowed)

    st.divider()


    st.subheader("📚 Learning History")


    if memory:

        for item in reversed(memory[-12:]):

            color = "🟢" if item["status"] == "ALLOWED" else "🔴"


            st.markdown(f"""
**{color} {item['status']}**  
🕒 {item['time']}  
📌 {item['task']}  
⚠️ Risk: {item['risk_level']} ({item['risk_score']})  
🧩 Matched: {", ".join(item["matched"]) if item["matched"] else "None"}
---
""")

    else:

        st.info("No history yet.")
