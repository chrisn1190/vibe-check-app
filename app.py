import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="VibeCheck Sports", page_icon="📈")
st.title("📈 VibeCheck: Sports Data Sidekick")
st.markdown("Stop betting on 'vibes'—start tracking them.")

# --- MOCK DATABASE (In a real app, this links to a CSV or Database) ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame([
        {'league': 'NBA', 'bet_type': 'Spread', 'result': 1},
        {'league': 'NFL', 'bet_type': 'Over/Under', 'result': 0},
        {'league': 'NBA', 'bet_type': 'Spread', 'result': 1},
    ])

# --- SIDEBAR: LOG A NEW BET ---
with st.sidebar:
    st.header("Log a Past Bet")
    l_input = st.selectbox("League", ["NBA", "NFL", "MLB", "NHL"])
    t_input = st.selectbox("Type", ["Spread", "Over/Under", "Moneyline"])
    r_input = st.radio("Outcome", ["Win", "Loss"])
    
    if st.button("Add to History"):
        new_data = {'league': l_input, 'bet_type': t_input, 'result': 1 if r_input == "Win" else 0}
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_data])], ignore_index=True)
        st.success("History Updated!")

# --- MAIN INTERFACE: VIBE CALCULATOR ---
st.subheader("Calculate Your Current Vibe")
col1, col2 = st.columns(2)

with col1:
    target_league = st.selectbox("Target League", ["NBA", "NFL", "MLB", "NHL"], key="target_l")
with col2:
    target_type = st.selectbox("Target Bet Type", ["Spread", "Over/Under", "Moneyline"], key="target_t")

# Algorithm Logic
history = st.session_state.history
l_win_rate = history[history['league'] == target_league]['result'].mean() if not history[history['league'] == target_league].empty else 0.5
t_win_rate = history[history['bet_type'] == target_type]['result'].mean() if not history[history['bet_type'] == target_type].empty else 0.5
vibe_score = int(((l_win_rate * 0.5) + (t_win_rate * 0.5)) * 100)

# Display Result
st.metric(label="Vibe Score", value=f"{vibe_score}/100")

if vibe_score > 60:
    st.balloons()
    st.success("High Vibe! This bet aligns with your winning patterns.")
elif vibe_score < 40:
    st.warning("Low Vibe. You historically struggle with this combination.")
else:
    st.info("Neutral Vibe. Proceed with caution.")

# Show History Table
with st.expander("View Your Betting History"):
    st.table(st.session_state.history)