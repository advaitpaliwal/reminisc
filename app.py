from chat import ReminiscChat
import streamlit as st

# Set up the title and create a ReminiscChat instance
st.title("Reminisc")
chat = ReminiscChat()

# Check and manage the session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the past conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧠"):
        # Process the user input using the ReminiscChat instance
        stream = chat.process_message(prompt)
        response = st.write_stream(stream)

        # Save the assistant's response in the session
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
