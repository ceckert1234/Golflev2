
import streamlit as st
import pandas as pd
import random

# Load the cleaned data from GitHub raw URL
df = pd.read_csv("https://raw.githubusercontent.com/your-username/your-repo/main/Cleaned_Top_20_Golfers_March_2025_with_Wins_and_Majors.txt")
df.columns = df.columns.str.strip()

# Color scheme
colors = {
    "correct": "green",
    "close": "yellow",
    "incorrect": "gray"
}

def give_hint(target, guess):
    hints = {}
    if guess["Nationality"] == target["Nationality"]:
        hints["Nationality"] = ("Correct", colors["correct"])
    else:
        hints["Nationality"] = ("Incorrect", colors["incorrect"])
    if guess["College"] == target["College"]:
        hints["College"] = ("Correct", colors["correct"])
    else:
        hints["College"] = ("Incorrect", colors["incorrect"])
    for field in ["Age", "PGA Card Year", "PGA Tour Wins", "Major Wins"]:
        diff = abs(guess[field] - target[field])
        if diff == 0:
            color = colors["correct"]
        elif diff <= 2:
            color = colors["close"]
        else:
            color = colors["incorrect"]
        hints[field] = (str(guess[field]), color)
    return hints

def main():
    st.set_page_config(page_title="PGA Tour Weddle", layout="centered")
    st.title("🏌️ PGA Tour Weddle Game")

    if "target" not in st.session_state:
        st.session_state.target = df.sample(1).iloc[0]
        st.session_state.attempts = []
        st.session_state.max_attempts = 5
        st.session_state.game_over = False

    target = st.session_state.target
    all_names = df["Name"].tolist()

    guess_name = st.selectbox("Guess a PGA Tour or LIV player:", [""] + all_names)

    if st.button("Submit Guess") and not st.session_state.game_over and guess_name != "":
        guess_row = df[df["Name"] == guess_name].iloc[0]
        hints = give_hint(target, guess_row)
        st.session_state.attempts.append((guess_name, hints))

        if guess_name == target["Name"]:
            st.success(f"🎉 Correct! The player was {target['Name']}.")
            st.session_state.game_over = True
        elif len(st.session_state.attempts) >= st.session_state.max_attempts:
            st.error(f"💀 Out of guesses! The player was {target['Name']}.")
            st.session_state.game_over = True

    if st.session_state.attempts:
        st.subheader("Your Guesses")
        for i, (name, hint_set) in enumerate(st.session_state.attempts, 1):
            st.markdown(f"**Guess {i}: {name}**")
            cols = st.columns(len(hint_set))
            for col, (key, (val, color)) in zip(cols, hint_set.items()):
                col.markdown(f'<div style="background-color:{color}; padding:8px; border-radius:5px; text-align:center"><b>{key}</b><br>{val}</div>', unsafe_allow_html=True)
            st.markdown("---")

    if st.session_state.game_over:
        if st.button("Play Again"):
            st.session_state.clear()

if __name__ == "__main__":
    main()
