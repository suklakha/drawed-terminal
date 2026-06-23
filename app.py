import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="D.R.A.W.E.D. Terminal", page_icon="⚙️")
st.title("D.R.A.W.E.D. Terminal")
st.caption("Defence Research, Aerospace, & Warfare Engineering Directorate")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("System Error: API Key missing. Please check configuration.")
    st.stop()

# --- THE FIX: Auto-detect the correct AI engine for your key ---
@st.cache_resource
def get_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()
# ---------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System Online. D.R.A.W.E.D. protocols initiated. Awaiting engineering parameters..."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Enter query here..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        persona = "You are D.R.A.W.E.D., a formal and elite engineering AI directorate. Answer analytically. Query: "
        try:
            response = model.generate_content(persona + user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Critical System Failure. Error details: {e}")