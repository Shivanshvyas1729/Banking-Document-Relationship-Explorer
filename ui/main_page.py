"""
ui/main_page.py
===============

Main entry UI page for BankDocLink.
Handles document upload, session state management, and file listing.
"""

import os
import sys
# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pathlib import Path

import config
from core.document_uploader import DocumentUploader
from utils.error_handling import InvalidFileError


def inject_custom_css():
    """Injects custom CSS to style the Streamlit application with premium aesthetics."""
    st.markdown(
        """
        <style>
        /* Import premium font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

        /* Apply font family globally */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Top header gradient */
        .title-container {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .title-container h1 {
            margin: 0;
            font-weight: 700;
            font-size: 2.5rem;
            color: white !important;
        }

        .title-container p {
            margin: 0.5rem 0 0 0;
            font-weight: 300;
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Document list header */
        .section-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1e3c72;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
        }

        /* Custom buttons styling */
        div.stButton > button {
            border-radius: 8px;
            border: 1px solid #ff4b4b;
            color: #ff4b4b;
            background-color: transparent;
            transition: all 0.3s ease;
            font-weight: 500;
            width: 100%;
        }

        div.stButton > button:hover {
            background-color: #ff4b4b;
            color: white;
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.2);
        }
        
        /* Upload box adjustment */
        .uploadedFile {
            border-radius: 8px;
            border: 1px dashed #2a5298;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render():
    """Renders the main page interface."""
    # 1. Page Configuration
    st.set_page_config(
        page_title="BankDocLink — Relationship Explorer",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject custom styles
    inject_custom_css()

    # Initialize DocumentUploader in session state
    if "uploader" not in st.session_state:
        st.session_state.uploader = DocumentUploader()
    uploader = st.session_state.uploader

    # Initialize processed file tracker in session state
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    # 2. Sidebar Navigation
    with st.sidebar:
        st.markdown("<h2 style='color:#1e3c72; font-weight:700;'>🏦 BankDocLink</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.9rem; color:#64748b; margin-top:-10px;'>Analyze & connect banking documents</p>", unsafe_allow_html=True)
        st.divider()

        option = st.radio(
            "Navigation",
            ["📤 Upload Documents", "🔍 Document Insights", "🕸️ Relationship Explorer", "💬 Ask & Query"]
        )

        st.divider()
        st.markdown(
            f"""
            <div style='font-size:0.8rem; color:#64748b;'>
                <b>Limits:</b><br>
                • Max Docs/Session: {config.MAX_DOCUMENTS_PER_SESSION}<br>
                • Supported formats: {', '.join(config.SUPPORTED_FILE_TYPES).upper()}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Main Dashboard Routing
    if option == "📤 Upload Documents":
        # Header banner
        st.markdown(
            """
            <div class="title-container">
                <h1>Document Upload Center</h1>
                <p>Upload files to parse, index, and explore relationships between banking documents.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Split layout for uploading and listing
        col_upload, col_list = st.columns([1, 1], gap="large")

        with col_upload:
            st.markdown("<div class='section-header'>Select Files to Upload</div>", unsafe_allow_html=True)
            
            # File Uploader
            uploaded_files = st.file_uploader(
                "Upload files (PDF, DOCX, TXT)",
                accept_multiple_files=True,
                type=config.SUPPORTED_FILE_TYPES,
                label_visibility="collapsed"
            )

            if uploaded_files:
                new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
                
                if new_files:
                    try:
                        uploaded_docs = uploader.upload_files(new_files)
                        # Register as processed
                        for f in new_files:
                            st.session_state.processed_files.add(f.name)
                        st.success(f"Successfully uploaded {len(uploaded_docs)} document(s)!")
                        st.rerun()
                    except InvalidFileError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"An unexpected error occurred during upload: {str(e)}")

        with col_list:
            st.markdown("<div class='section-header'>Uploaded Documents Registry</div>", unsafe_allow_html=True)
            
            docs = uploader.get_file_list()
            if not docs:
                st.info("No documents uploaded yet in this session.")
            else:
                st.markdown(
                    f"Showing **{len(docs)}** of **{config.MAX_DOCUMENTS_PER_SESSION}** maximum allowed documents."
                )
                
                # Render document list with native styled rows
                for doc in docs:
                    file_path = Path(doc.path)
                    file_size_kb = 0.0
                    if file_path.exists():
                        file_size_kb = file_path.stat().st_size / 1024.0

                    # Determine file icon
                    suffix = file_path.suffix.lower()
                    if suffix == ".pdf":
                        icon = "📄 PDF"
                    elif suffix == ".docx":
                        icon = "📝 DOCX"
                    else:
                        icon = "📝 TXT"

                    with st.container(border=True):
                        c_icon, c_info, c_action = st.columns([2, 5, 2], gap="small")
                        with c_icon:
                            st.markdown(f"<b style='font-size:0.95rem;'>{icon}</b>", unsafe_allow_html=True)
                        with c_info:
                            st.markdown(
                                f"""
                                <div style='line-height:1.2;'>
                                    <span style='font-size:0.95rem; font-weight:600; color:#1e293b;'>{doc.name}</span><br>
                                    <span style='font-size:0.8rem; color:#64748b;'>Size: {file_size_kb:.1f} KB</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with c_action:
                            if st.button("Delete", key=f"del_{doc.id}"):
                                uploader.remove_file(doc.id)
                                # Remove from processed files registry to allow re-upload
                                if doc.name in st.session_state.processed_files:
                                    st.session_state.processed_files.remove(doc.name)
                                st.rerun()

    else:
        # Placeholder views for navigation options that will be implemented in subsequent phases
        st.markdown(
            f"""
            <div class="title-container">
                <h1>{option[2:]}</h1>
                <p>Explore cross-document intelligence and relations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.info(
            f"The **{option[2:]}** view will be fully implemented and wired up in a later phase. "
            "Please upload documents in the **Upload Documents** section first!"
        )


if __name__ == "__main__":
    render()