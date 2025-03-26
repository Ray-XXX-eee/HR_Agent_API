import os
import streamlit as st

class SidebarUI:
    def __init__(self):
        self.selected_model = st.session_state.get("selected_model", "gemma2-9b-it")
        self.temperature = st.session_state.get("temperature", 0.0)

    # def choose_model(self):
    #     """Display model selection dropdown and temperature slider."""
    #     with st.sidebar.expander("Choose Model:"):
    #         self.selected_model = st.selectbox("Select Model", ["gemma2-9b-it", "llama3-8b-8192"])
    #         self.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1)
    #     return self.selected_model, self.temperature
    
    def choose_model(self):
        """Display model selection dropdown and temperature slider with conditional submit button."""
        with st.sidebar.expander("Choose Model:"):
            # Store previous values
            previous_model = st.session_state.get("selected_model", "gemma2-9b-it")
            previous_temperature = st.session_state.get("temperature", 0.5)

            # Create widgets
            self.selected_model = st.selectbox("Select Model", ["gemma2-9b-it", "llama3-8b-8192"], index=["gemma2-9b-it", "llama3-8b-8192"].index(previous_model),key="model_select")
            self.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, value=previous_temperature)

            # Check if values have changed
            changes_made = (self.selected_model != previous_model) or (self.temperature != previous_temperature)

            st.session_state.selected_model = self.selected_model
            st.session_state.temperature = self.temperature
            # Display Submit button only if changes are detected
            if changes_made:
                if st.button("➤"):
                    # Update session state with new values
                    st.session_state.selected_model = self.selected_model
                    st.session_state.temperature = self.temperature

                    # Hide the button by resetting `changes_made`
                    st.rerun()
            # print ("model name - ", st.session_state.selected_model,"temp - ",  st.session_state.temperature)

        # return self.selected_model, self.temperature

    def display_trial_info(self, if_trial_available_func, trial_value):
        """Display trial usage information."""
        if if_trial_available_func():
            with st.sidebar.expander(f"Trial Left: {trial_value}"):
                st.write(f"You have {trial_value} query trials left")
        else:
            with st.sidebar.expander("No Trial Left, enter your own API key below 👇"):
                st.text_input("Enter your Groq API key to continue:")

    def display_doc_details(self):
        """Display document details from session state."""
        with st.sidebar.expander("📄 Document Details", expanded=True):  # Ensure it's expanded
            if "metadata" in st.session_state and st.session_state.metadata:
                for file, pages in st.session_state.metadata.items():
                    st.write(f"✅ `{os.path.basename(file)}` - **{pages} pages**")

                total_chunks = len(st.session_state.get("final_doc", []))
                total_tokens = sum(len(chunk) for chunk in st.session_state.final_doc)

                st.write(f"📌 **Total Chunks:** {total_chunks}")
                st.write(f"🔢 **Approximate Token Size:** {total_tokens} characters")
            else:
                st.write("⚠️ No document details available. Upload a document to view details.")


    def display_upgrade_link(self):
        """Ensure Upgrade link stays at the bottom of the sidebar."""
        # Create an empty container at the end of the sidebar
        for _ in range(20):  # Adjust the range to create enough space
            st.sidebar.write("")

        # Now place the upgrade link
        st.sidebar.markdown(
            '<div style="text-align: center; font-weight: bold;">'
            '<a href="#" target="_blank" style="color: #007bff; text-decoration: none;">🔼 Upgrade for more features</a>'
            '</div>',
            unsafe_allow_html=True
        )

