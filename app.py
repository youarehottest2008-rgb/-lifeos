import streamlit as st
import datetime, urllib.parse

st.set_page_config(page_title="LifeOS v2 - Real Chat", page_icon="🧠", layout="wide")

# --- ROOM SYSTEM ---
query = st.query_params
room_code = query.get("room", "MY-HOUSE")
room_code = room_code if isinstance(room_code, str) else "MY-HOUSE"

if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "MY-HOUSE": {"tasks": ["NEPA bill ₦15k - Due Oct 1", "Buy rice & stew"], "chat": []},
        "TRIP-DEC": {"tasks": ["Book Warri-Lagos bus", "Airbnb ₦100k paid"], "chat": []},
        "WEDDING": {"tasks": ["Book hall", "150 guests"], "chat": []},
        "HUSTLE": {"tasks": ["Post TikTok today"], "chat": []},
    }

# Ensure current room exists
if room_code not in st.session_state.rooms:
    st.session_state.rooms[room_code] = {"tasks": [], "chat": []}

st.markdown(f"# 🧠 LifeOS v2 — Room: `{room_code}`")
st.caption(f"Share this link, una go dey same Room + chat live!")

# Invite Link
base_url = "https://lifeos.streamlit.app"
invite_link = f"{base_url}/?room={room_code}"
st.code(invite_link, language=None)
wa_text = urllib.parse.quote(f"Join my LifeOS Room {room_code}: {invite_link}")
st.link_button("📲 Share Invite on WhatsApp", f"https://wa.me/?text={wa_text}")

st.divider()
room_names = list(st.session_state.rooms.keys())
selected = st.selectbox("Switch Room", room_names, index=room_names.index(room_code) if room_code in room_names else 0)

# If switched, update URL
if selected!= room_code:
    st.query_params["room"] = selected
    st.rerun()

current = st.session_state.rooms[selected]

# --- TABS ---
tab1, tab2 = st.tabs(["✅ Tasks", "💬 Family Chat"])

with tab1:
    st.subheader(f"Tasks for {selected}")
    new_task = st.text_input("Add new task/bill", key="task_input")
    if st.button("Add Task"):
        if new_task:
            current["tasks"].append(new_task)
            st.success("Added!")
            st.rerun()
    for i, t in enumerate(current["tasks"]):
        col1, col2 = st.columns([4,1])
        col1.checkbox(t, key=f"{selected}_task_{i}")
        if col2.button("❌", key=f"del_{selected}_{i}"):
            current["tasks"].pop(i)
            st.rerun()

with tab2:
    st.subheader(f"Live Chat - {selected}")
    st.caption("Type here, your family go see am when they refresh (V3 go be instant)")
    for msg in current["chat"]:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}:** {msg['text']} \n_{msg['time']}_")

    user_name = st.text_input("Your name", value="You", key="chat_name")
    chat_input = st.chat_input("Type message...")
    if chat_input:
        current["chat"].append({
            "user": user_name,
            "role": "user",
            "text": chat_input,
            "time": datetime.datetime.now().strftime("%H:%M")
        })
        # Simple AI auto-reply if they ask
        if "remind" in chat_input.lower() or "add" in chat_input.lower():
            current["chat"].append({
                "user": "LifeOS AI",
                "role": "assistant",
                "text": f"Got it! I added '{chat_input}' to tasks.",
                "time": datetime.datetime.now().strftime("%H:%M")
            })
            current["tasks"].append(chat_input)
        st.rerun()

with st.sidebar:
    st.markdown("### Create New Room")
    new_room = st.text_input("New Room code e.g. OKPE-HOUSE")
    if st.button("Create Room") and new_room:
        st.session_state.rooms[new_room.upper()] = {"tasks": [], "chat": []}
        st.query_params["room"] = new_room.upper()
        st.rerun()
    st.divider()
    st.markdown("### Premium ₦5k")
    st.write("Palmpay: 9029508840")
    st.button("Unlock Premium", type="primary", use_container_width=True)
