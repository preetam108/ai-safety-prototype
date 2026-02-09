import streamlit as st
import json
import os
import datetime
import re

MEMORY_FILE = "memory.json"
LEARN_FILE = "learned_risks.json"


# ---------------- LOAD / SAVE ----------------

def load_file(path):
    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ---------------- LEARNING ENGINE ----------------

def extract_words(text):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    return list(set(words))


def update_learning(task, learned):

    words = extract_words(task)

    for w in words:
        if w not in learned:
            learned.append(w)

    return learned


# ---------------- RISK ENGINE ----------------

BASE_RISK = ["hack", "illegal", "attack", "steal", "bypass"]


def check_risk(task, learned):

    score = 0
    matched = []

    all_risks = list(set(BASE_RISK + learned))

    for word in all_risks:
        if word in task.lower():
            score += 15
            matched.append(word)

    if score >= 40:
        return "HIGH", score, matched
    elif score >= 20:
        return "MEDIUM", score, matched
    else:
        return "LOW", score, matched


# ---------------- UI ----------------

st.set_page_config(page_title="AI Safety Prototype", layout="wide")

st.title("🛡️ AI Safety Prototype")
st.subheader("Monitor • Block • Learn • Evolve")

left, right = st.columns(2)


memory = load_file(MEMORY_FILE)
learned = load_file(LEARN_FILE)


# ---------------- LEFT PANEL ----------------

with left:

    st.header("📝 Submit Task")

    task = st.text_area("Enter Task")

    submit = st.button("Run Safety Check")


    if submit and task:

        level, score, matched = check_risk(task, learned)

        status = "ALLOWED"

        if level == "HIGH":
            status = "BLOCKED"


        # Learn from blocked tasks
        if status == "BLOCKED":
            learned = update_learning(task, learned)
            save_file(LEARN_FILE, learned)


        record = {
            "time": str(datetime.datetime.now()),
            "task": task,
            "risk_level": level,
            "risk_score": score,
            "status": status,
            "matched": matched
        }

        memory.append(record)
        save_file(MEMORY_FILE, memory)


        # Result
        if status == "BLOCKED":
            st.error(f"🚫 Blocked — {level} ({score})")
            if matched:
                st.warning("⚠️ Detected: " + ", ".join(matched))
        else:
            st.success(f"✅ Allowed — {level} ({score})")


# ---------------- RIGHT PANEL ----------------

with right:

    st.header("📊 System Dashboard")

    total = len(memory)
    blocked = len([m for m in memory if m["status"] == "BLOCKED"])
    allowed = total - blocked

    st.metric("Total Tasks", total)
    st.metric("Blocked", blocked)
    st.metric("Allowed", allowed)

    st.metric("Learned Risks", len(learned))

    st.divider()

    st.subheader("🧠 Learned Risk Vocabulary")

    if learned:
        st.write(", ".join(sorted(learned)))
    else:
        st.info("No learned risks yet.")


    st.divider()

    st.subheader("📚 Learning History")

    if memory:

        for item in reversed(memory[-8:]):

            color = "🟢" if item["status"] == "ALLOWED" else "🔴"

            st.markdown(f"""
**{color} {item['status']}**  
🕒 {item['time']}  
📌 {item['task']}  
⚠️ Risk: {item['risk_level']} ({item['risk_score']})  
🧩 Matched: {", ".join(item["matched"])}
---
""")
    else:
        st.info("No history yet.")
