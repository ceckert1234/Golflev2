
import streamlit as st
import pandas as pd
import random

# Load the cleaned data
df = pd.read_csv("https://raw.githubusercontent.com/ceckert1234/Golflev2/refs/heads/main/Top_20_Golfers_March_2025_with_Wins_and_Majors.txt")
df.columns = df.columns.str.strip()

# Colors
colors = {
    "correct": "green",
    "close": "yellow",
    "incorrect": "gray"
}

def give_hint(target, guess):
    hints = {}

    # Nationality
    if guess["Nationality"] == target["Nationality"]:
        hints["Nationality"] = (guess["Nationality"], colors["correct"])
    else:
        hints["Nationality"] = (guess["Nationality"], colors["incorrect"])

    # College
    if guess["College"] == target["College"]:
        hints["College"] = (guess["College"], colors["correct"])
    else:
        hints["College"] = (guess["College"], colors["incorrect"])

    # Numerical fields with up/down arrows
    for field in ["Age", "PGA Card Year", "PGA Tour Wins", "Major Wins"]:
        guess_val = guess[field]
        target_val = target[field]
        diff = abs(guess_val - target_val)

        if field == "Major Wins":
            if diff == 0:
                color = colors["correct"]
            elif diff == 1:
                color = colors["close"]
            else:
                color = colors["incorrect"]
        else:
            if diff == 0:
                color = colors["correct"]
            elif diff <= 2:
                color = colors["close"]
            else:
                color = colors["incorrect"]

        # Directional arrow
        if guess_val < target_val:
            arrow = "↑"
        elif guess_val > target_val:
            arrow = "↓"
        else:
            arrow = ""

        hints[field] = (f"{guess_val} {arrow}", color)

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
