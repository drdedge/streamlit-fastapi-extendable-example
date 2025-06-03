import streamlit as st
from utils.api_client import APIClient
import requests
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Document Processing Service",
    page_icon="📄",
    layout="wide"
)

# Initialize API client
api_client = APIClient()

# Title and description
st.title("📄 Document Processing Service")
st.markdown("""
This service processes various document types and converts them to formatted outputs.
Simply upload your file and provide the required information to get started.
""")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Upload Document")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=None,  # Accept all file types
        help="Currently supports .txt files. More formats coming soon!"
    )
    
    # Form for additional data
    with st.form("upload_form"):
        issuer_id = st.text_input(
            "Issuer ID",
            placeholder="Enter your issuer ID",
            help="Your unique identifier"
        )
        
        user_email = st.text_input(
            "Email Address",
            placeholder="user@example.com",
            help="Email address for notifications"
        )
        
        submit_button = st.form_submit_button("Process Document")

with col2:
    st.header("Processing Status")
    status_placeholder = st.empty()

# Initialize session state for job tracking
if 'job_id' not in st.session_state:
    st.session_state.job_id = None
if 'job_status' not in st.session_state:
    st.session_state.job_status = None
if 'download_url' not in st.session_state:
    st.session_state.download_url = None
if 'processed_filename' not in st.session_state:
    st.session_state.processed_filename = None

# Process file when form is submitted
if submit_button and uploaded_file:
    if not issuer_id or not user_email:
        st.error("Please fill in all required fields")
    else:
        try:
            # Show processing status
            with status_placeholder.container():
                with st.spinner("Uploading file..."):
                    # Upload file
                    response = api_client.upload_file(
                        uploaded_file,
                        issuer_id,
                        user_email
                    )
                    job_id = response["job_id"]
                
                # Show job info
                st.info(f"Job ID: {job_id}")
                
                # Create a progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Poll for status
                with st.spinner("Processing document..."):
                    status_map = {
                        "queued": 10,
                        "validating": 25,
                        "processing": 50,
                        "converting": 75,
                        "completed": 100,
                        "failed": 0
                    }
                    
                    try:
                        # Wait for completion
                        final_status = api_client.wait_for_completion(job_id)
                        
                        # Update progress based on status
                        current_status = final_status["status"]
                        progress = status_map.get(current_status, 0)
                        progress_bar.progress(progress / 100)
                        status_text.text(f"Status: {final_status['message']}")
                        
                        if final_status["status"] == "completed":
                            st.success("✅ Document processed successfully!")
                            
                            # Store results in session state
                            st.session_state.job_id = job_id
                            st.session_state.job_status = "completed"
                            st.session_state.download_url = api_client.get_download_url(job_id)
                            st.session_state.processed_filename = f"{uploaded_file.name.replace('.txt', '')}_processed.docx"
                            
                        else:
                            st.error(f"❌ Processing failed: {final_status['message']}")
                            st.session_state.job_status = "failed"
                            
                    except TimeoutError:
                        st.error("⏱️ Processing timed out. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Error during processing: {str(e)}")
                        
        except Exception as e:
            st.error(f"❌ Upload failed: {str(e)}")

# Display download button if job is completed
if st.session_state.job_status == "completed" and st.session_state.download_url:
    with col2:
        st.info(f"Job ID: {st.session_state.job_id}")
        st.success("✅ Document processed successfully!")
        
        # Fetch the file for download
        response = requests.get(st.session_state.download_url)
        if response.status_code == 200:
            st.download_button(
                label="📥 Download Processed Document",
                data=response.content,
                file_name=st.session_state.processed_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_button"
            )
        
        # Add clear button to reset state
        if st.button("🔄 Process Another File", key="clear_button"):
            st.session_state.job_id = None
            st.session_state.job_status = None
            st.session_state.download_url = None
            st.session_state.processed_filename = None
            st.rerun()

# Instructions section
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. **Upload a file**: Click on the file uploader and select a file from your computer
    2. **Enter your details**: Provide your Issuer ID and email address
    3. **Process the document**: Click the "Process Document" button
    4. **Wait for processing**: The system will validate, process, and convert your document
    5. **Download the result**: Once complete, download your formatted DOCX file
    
    **Currently Supported**: 
    - Text files (.txt) → Formatted DOCX
    
    **Coming Soon**: 
    - PDF extraction
    - Image text recognition (OCR)
    - CSV/Excel processing
    """)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and FastAPI")