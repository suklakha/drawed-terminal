import streamlit as st
import google.generativeai as genai

# 1. Setup the Webpage Look
st.set_page_config(page_title="D.R.A.W.E.D. Terminal", page_icon="⚙️")
st.title("D.R.A.W.E.D. Terminal")
st.caption("Defence Research, Aerospace, & Warfare Engineering Directorate")

# 2. Grab the secret API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("System Error: API Key missing. Please check configuration.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Create chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System Online. D.R.A.W.E.D. protocols initiated. Awaiting engineering parameters..."}]

# 4. Show past messages on screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Handle when you type a message
if user_input := st.chat_input("Enter query here..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        # This keeps the AI acting like D.R.A.W.E.D.
        persona = "You are D.R.A.W.E.D., a formal and elite engineering AI directorate for a school project. Answer analytically. Query: "
        response = model.generate_content(persona + user_input)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})