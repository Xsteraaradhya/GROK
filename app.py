
import streamlit as st
from xai import XAIClient

# Initialize the xAI client
api_key = st.secrets.get("XAI_API_KEY")  # Add your API key in Streamlit secrets.toml or via environment variable
if not api_key:
    st.error("Please set your XAI_API_KEY in Streamlit secrets.")
    st.stop()

client = XAIClient(api_key=api_key)

# Streamlit app title
st.title("Grok Chatbot powered by xAI")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask Grok anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Grok
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Call the xAI API (assuming chat completions similar to OpenAI format)
            response = client.chat.completions.create(
                model="grok-4",  # Use the latest model, adjust as needed
                messages=st.session_state.messages,
                stream=True  # Enable streaming for real-time response
            )

            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
