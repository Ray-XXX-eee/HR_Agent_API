import os
import pprint
import streamlit as st
from app.UI.UI2API_client import API_upload_doc, API_upload_doc_multi
from app.UI.chat import chat_interface
from app.UI.sidebar import SidebarUI
import certifi

# Set SSL certs
os.environ["SSL_CERT_FILE"] = certifi.where()

class MainUI:
    def __init__(self):
        # self.sidebar = sidebar_ui
        self.uploaded_files = None
        self.selected_files = None
        self.file_to_process = {}
        self.jd_checkbox = False
        self.cv_checkbox = False
        # self.option = None
        self.DATA_DIR = "data"  # remove later
        os.mkdir(self.DATA_DIR) if not os.path.exists(self.DATA_DIR) else None
    
    def store_file(self, file, tag):
        if file is not None:
            self.file_to_process[f"{tag}_{file.name}"] = [file, tag]
        
    def display_options(self):
        """Display radio button for document option and file uploader or selector."""
                
        # Main UI layout
        col1, col_spacer, col2 = st.columns([1, 0.05, 1])  # Adding a small spacer for a vertical line

        with col1:
            st.header("📜 Job Description")
            jd_checkbox = st.checkbox("Enable JD Upload",key="jd_checkbox")
            if jd_checkbox:
                jd_option = st.radio("Select JD Option:", ["Upload New", "Select Existing"], horizontal=True, key="jd_radio")
                if jd_option == "Upload New":
                    jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="jd_upload")
                    self.store_file(jd_file, "jd")
                else:
                    st.selectbox("Select Existing JD:", ["JD1.pdf", "JD2.pdf", "JD3.pdf"],key='jd_select_box')  # Replace with dynamic options


        with col_spacer:
            st.markdown("<div style='border-left: 2px solid gray; height: 100%;'></div>", unsafe_allow_html=True)

        with col2:
            st.header("📄 Resume")
            resume_checkbox = st.checkbox("Enable Resume Upload",key="cv_checkbox")
            if resume_checkbox:
                resume_option = st.radio("Select Resume Option:", ["Upload New", "Select Existing"], horizontal=True, key="resume_radio")
                if resume_option == "Upload New":
                    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_upload")
                    self.store_file(resume_file, "cv")
                else:
                    st.selectbox("Select Existing Resume:", ["Resume1.pdf", "Resume2.pdf", "Resume3.pdf"],key='cv_select_box')  # Replace dynamically

# Process Button
    def process_documents(self):
        """Process the selected or uploaded document(s)."""
        if not self.file_to_process:
            st.warning("Select a JD or CV.")
            return

        if st.button("Process PDF"):
            responses = API_upload_doc_multi(self.file_to_process)
            for response in responses:
                st.write(response)
                # st.write(response.get("final_doc", {}))


            # if st.button("Process"):
            #     if self.jd_checkbox and jd_file:
            #         st.subheader("📄 Processed JD:")
            #         st.write("Embedded JD Viewer Here (Replace with actual embedding logic)")
            #     if self.cv_checkbox and resume_file:
            #         st.subheader("📄 Processed Resume:")
            #         st.write("Embedded Resume Viewer Here (Replace with actual embedding logic)")
                    
    
    def display_chat_comp(self):
            """Call chat interface from chat.py."""
            chat_interface()  # Calls the modular chat function