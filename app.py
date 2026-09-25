import streamlit as st
import datetime
import json

st.set_page_config(page_title="LifeOS", page_icon="🧠", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
   .room-card {background: #0e1a14; border: 1px solid #2aff7a; border-radius: 12px; padding: 20px; margin: 10px 0;}
   .big-title {font-size: 38px; font-weight: 800; color: white;}
   .sub {color: #aaffaa;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">LifeOS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Your AI Assistant For Managing Your Entire Life, Not Just Chatting — Automate • Organize • Achieve</div>', unsafe_allow_html=True)
st.divider()

# --- State ---
if "data" not in st.session_state:
    st.session_state.data = {
        "Household": {"items": ["NEPA bill ₦15k - Due Oct 1", "Buy rice & stew"], "budget": 50000},
        "Trip": {"items": ["Book Warri to Lagos bus", "Airbnb for 4"], "budget": 250000, "paid": 100000},
        "Wedding": {"items": ["Book hall", "150 guests"], "budget": 1200000},
        "Hustle": {"items": ["Finish LifeOS MVP", "Post TikTok"], "budget": 0},
    }

tabs = st.tabs(["🏠 Household Room", "✈️ Trip Room", "💒 Wedding Room", "📚 Hustle Room", "🤖 LifeOS AI"])

# --- ROOM 1 ---
with tabs[0]:
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Household Room")
        st.caption("Bills • Shopping • Chores — Shared with family")
        new = st.text_input("Add bill/task", placeholder="e.g. Pay rent 300k", key="h_in")
        if st.button("Add", key="h_btn") and new:
            st.session_state.data["Household"]["items"].append(new)
            st.toast("Added to Household!")
        for i, item in enumerate(st.session_state.data["Household"]["items"]):
            st.checkbox(item, key=f"h_{i}")
    with col2:
        st.markdown('<div class="room-card">3 tasks due today • Synced<br><br>💰 Monthly: ₦45k spent<br>🔔 AI: 2 bills due in 3 days</div>', unsafe_allow_html=True)
        st.text_input("Invite Link", value="lifeos.app/join/household-warri123", disabled=True)
        st.button("📋 Copy Invite Link", key="copy_h")

# --- ROOM 2 ---
with tabs[1]:
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Trip Room - Detty December Lagos")
        st.caption("Budget • Itinerary • Tickets")
        budget = st.session_state.data["Trip"]["budget"]
        paid = st.session_state.data["Trip"]["paid"]
        st.progress(paid/budget)
        st.write(f"**₦{paid:,} paid / ₦{budget:,} total** — 2 friends never pay")
        new = st.text_input("Add trip task", placeholder="e.g. Buy beach outfit", key="t_in")
        if st.button("Add to Trip", key="t_btn") and new:
            st.session_state.data["Trip"]["items"].append(new)
        for item in st.session_state.data["Trip"]["items"]:
            st.checkbox(item, key=f"t_{item}")
    with col2:
        st.markdown('<div class="room-card">✈️ Japan trip • 5 days • On track<br><br>👥 Allen, Emeka, Tega, Jane<br>💸 You owe: ₦30k</div>', unsafe_allow_html=True)
        st.button("👥 Invite Friends", key="copy_t", use_container_width=True)
        st.button("💸 Remind Owing Friends (AI)", key="remind", use_container_width=True)

# --- ROOM 3 & 4 ---
with tabs[2]:
    st.subheader("Wedding Room")
    st.metric("Guests", "150", "12 confirmed today")
    st.metric("Budget Tracked", "₦1.2M", "₦200k left")
    st.info("AI: Vendor 'DJ Warri' never confirm. Make I remind am?")

with tabs[3]:
    st.subheader("Student/Hustle Room")
    c1, c2, c3 = st.columns(3)
    c1.metric("Goals", "3 Active", "1 Completed")
    c2.metric("Earnings", "₦85k", "This month ↑")
    c3.metric("Deadlines", "2 Due", "Tomorrow")

# --- AI CHAT ---
with tabs[4]:
    st.subheader("Ask LifeOS")
    st.caption("One AI wey know everything about your Rooms")
    prompt = st.chat_input("Ask: Pay my NEPA & plan weekend trip...")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            st.success(f"Done! ✅\n\nI understood: '{prompt}'\n\n- Added to Household Room\n- Set reminder for {datetime.date.today() + datetime.timedelta(days=2)}\n- Notified everyone in that Room\n\nWetin next?")
    else:
        st.markdown("Try: `How much remain for our trip?` / `Remind us to pay rent` / `Summarize my week`")

# --- Sidebar Monetize ---
with st.sidebar:
    st.markdown("### LifeOS Premium")
    st.write("Unlock Forever")
    st.markdown("## ₦5,000")
    st.write("✅ Unlimited Rooms\n✅ AI Budgeting\n✅ Document Scanner\n✅ Invite Unlimited People")
    st.text_input("Palmpay Number", "9029508840", disabled=True)
    st.button("I Don Pay - Unlock", type="primary", use_container_width=True)
    st.divider()
    st.caption("Built for Warri Hustlers • Sell Faster. Earn More. Rest Well.")
