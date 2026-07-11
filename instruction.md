Edited 04_flowchart.md
Edited 04_flowchart.md
Viewed 01_scope.md:1-20

If you had to write this entire system yourself from scratch, here is the exact step-by-step order in which you should create the files, including why each step comes first and what logic goes inside.

---

### Step 1: Define the Contract (Models & Data Structure)
*   **Filename**: [`models/schemas.py`](file:///c:/Users/DELL/Desktop/internship1/models/schemas.py)
*   **Why start here?** You must define what a "Document" is before any parsing, uploader, or UI code can touch it. All modules need to agree on this structure.
*   **What you write**:
    1.  Import `langchain_core.documents.Document` as the base model.
    2.  Inherit from it to create a custom `Document` class.
    3.  Write property getters and setters for attributes like `id`, `name`, `path`, `content` (mapping to `page_content`), and `parsed_entities` (mapping to the internal `metadata` dictionary) to make it fully compatible with LangChain.
    4.  Add placeholder dataclasses for `Query`, `RetrievalResult`, and `Explanation`.

---

### Step 2: Establish the Error Boundaries
*   **Filename**: [`utils/error_handling.py`](file:///c:/Users/DELL/Desktop/internship1/utils/error_handling.py)
*   **Why start here?** The document uploader needs to reject bad files and throw specific errors. You must define these exceptions before you can write the logic that raises them.
*   **What you write**:
    1.  Define a custom exception: `class InvalidFileError(ValueError): pass`
    2.  Create a helper function `handle_invalid_file(filename, reason)` that logs the warning and raises the `InvalidFileError`.

---

### Step 3: Write the Core Business Logic
*   **Filename**: [`core/document_uploader.py`](file:///c:/Users/DELL/Desktop/internship1/core/document_uploader.py)
*   **Why start here?** This handles the actual mechanics of saving the files to disk, checking constraints, and managing the registry list.
*   **What you write**:
    1.  Implement `DocumentUploader` with an `__init__` that creates an uploads directory.
    2.  Write `upload_files(files)`: Validate suffixes against `config.SUPPORTED_FILE_TYPES`, check if `MAX_DOCUMENTS_PER_SESSION` is exceeded, write the bytes to disk, and instantiate your custom `Document` object.
    3.  Write `remove_file(file_id)`: Unlink the file from disk and remove it from your internal dictionary.
    4.  Write `get_file_list()`: Return all registered document objects.

---

### Step 4: Write the Backend Verification Tests
*   **Filename**: [`tests/test_document_uploader.py`](file:///c:/Users/DELL/Desktop/internship1/tests/test_document_uploader.py)
*   **Why start here?** Never write the UI before you prove the backend logic works. Running tests here saves you hours of UI debugging.
*   **What you write**:
    1.  Write a fixture to create a temporary directory for file uploads and clean it up afterward.
    2.  Write unit tests verifying valid uploads, invalid uploads (raising `InvalidFileError`), limit overflow enforcement, file removal from disk, and schema property getters/setters.
    3.  Run the tests using `pytest` to make sure they all pass.

---

### Step 5: Implement the User Interface
*   **Filename**: [`ui/main_page.py`](file:///c:/Users/DELL/Desktop/internship1/ui/main_page.py)
*   **Why start here?** The UI sits on top of the backend logic. It should only consume features that are already tested.
*   **What you write**:
    1.  Inject custom CSS styles (e.g. typography, cards, custom button borders).
    2.  Set up Streamlit page configs and sidebar navigation.
    3.  Initialize the `DocumentUploader` in `st.session_state` so uploaded files persist across page refreshes.
    4.  Render the `st.file_uploader` widget.
    5.  Catch `InvalidFileError` exceptions and display them gracefully in the UI.
    6.  Loop through `uploader.get_file_list()`, rendering card blocks for each document alongside a functional "Delete" button.

---

### Step 6: Create the Application Entry Point
*   **Filename**: [`app.py`](file:///c:/Users/DELL/Desktop/internship1/app.py)
*   **Why start here?** This is the single, clean file that Streamlit runs to start the entire system.
*   **What you write**:
    1.  Import and run the `render()` function from `ui/main_page.py`.