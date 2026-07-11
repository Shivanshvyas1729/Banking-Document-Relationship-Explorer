# from dataclasses import dataclass,field
# from html import entities
# from sys import exception
# from typing import List,Dict,Optional,Any 
# from docx import document
# from langchain_core.documents import Document as LCDocument
# from platformdirs import user_downloads_dir

# from utils.error_handling import handle_invalid_file


# class Document(LCDocument):
    
#     @property
#     def name(self) ->str:
#         return self.metadata.get("name","")
    
#     @property
#     def path(self):
#         return self.metadata.get("path","")
    
#     @property
#     def parsed_entities(self)-> dict:
#         if "parsed_entities" not in self.metadata:
#             self.metadata['parsed_entities'] = {
#                 "entities":[],
#                 "topics": [],
#                 "key_terms":[]
#             }

#         return self.metadata["parsed_entities"]
    
#     @parsed_entities.setter
#     def parsed_entities(self,value:dict):
#         if not isinstance(value,dict):
#             raise TypeError("parsed_entities must be a dictonary")
        
#         self.metadata = value

#     @property
#     def content(self):
#         return self.page_content
    
#     @content.setter
#     def content(self,value:str):
#         self.page_content = value




# from pathlib import Path
# from logging.handlers import RotatingFileHandler
# import os
# import logging

# # Available uvicorn log levels
# from uvicorn.config import LOG_LEVELS


# # Create logs directory path object
# LOG_DIR = Path('logs')

# # Create logs directory if it doesn't exist
# LOG_DIR.mkdir(exist_ok=True)

# # Full path for log file
# LOG_FILE = LOG_DIR / "app.log"

# # Get log level from environment variable
# # Default = INFO
# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


# def get_logger(name: str) -> logging.Logger:
#     """
#     Create and return a configured logger instance.
#     """

#     # Create/Get logger with given name
#     logger = logging.getLogger(name)

#     # Prevent adding duplicate handlers
#     # if logger already configured
#     if logger.handlers:
#         return logger

#     # Set logger level
#     logger.setLevel(LOG_LEVEL)

#     # Log message format
#     formatter = logging.Formatter(
#         fmt=(
#             "%(asctime)s | %(levelname)s | "
#             "%(name)s | %(filename)s:%(lineno)d | %(message)s"
#         ),
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )

#     # ---------------- Console Handler ----------------

#     # Print logs to terminal/console
#     console_handler = logging.StreamHandler()

#     # Apply log format
#     console_handler.setFormatter(formatter)

#     # ---------------- File Handler ----------------

#     # Rotating file handler:
#     # Creates new file after size limit reached
#     file_handler = RotatingFileHandler(
#         filename=LOG_FILE,
#         maxBytes=10 * 1024 * 1024,  # 10 MB max size
#         backupCount=5,              # Keep last 5 backup files
#         encoding="utf-8",
#     )

#     # Apply formatting to file logs
#     file_handler.setFormatter(formatter)

#     # ---------------- Add Handlers ----------------

#     # Add console output handler
#     logger.addHandler(console_handler)

#     # Add file logging handler
#     logger.addHandler(file_handler)

#     # Prevent logs from propagating
#     # to root logger multiple times
#     logger.propagate = False

#     # Return configured logger
#     return logger


# import config 

# class DocumentUploader:
#     def __init__(self,upload_dir:str | Path = "data/upload"):
#         self.upload_dir = upload_dir
#         self.upload_dir.mkdir(parents=True,exist_ok=True)
#         self.documents : Dict[str,Document] = {}


#     def upload_file(self,files:List)-> List[Document]:
#         uploaded_docs=[]

#         for file in files:
#             if len(self.documents)> config.MAX_DOCUMENTS_PER_SESSION:
#                 handle_invalid_file(
#                     filename=file.name,
#                     reasion =f"Maximum document limit of {config.MAX_DOCUMENTS_PER_SESSION} reached"
#                 )

#             # validate file extension 
#             filename = file.name
#             path = Path(filename)
#             suffix = path.suffix.lower().lstrip(".")

#             if suffix not in config.SUPPORTED_FILE_TYPES:
#                 handle_invalid_file(
#                     filename,
#                     f"unsupported file type {suffix}. Right now now these are supported {config.SUPPORTED_FILE_TYPES}"
#                 )

#             # save it
#             file_path = self.upload_dir / filename 

#             file_path.parent.mkdir()
#             if hasattr(file,"seek"):
#                 file.seek(0)
#             content_bytes = file.read()

#             with open(file_path,"wb") as f:
#                 f.write(content_bytes)

#             existing_id =None
#             for doc_id,doc in self.documents.items():
#                 if doc.name == filename:
#                     existing_id = doc.id
#                     break 
#             if existing_id:
#                 del self.documents[existing_id]

#             # register Documents
#             import uuid
#             doc_id = str(uuid.uuid4())

#             document = Document(
#                 id=doc_id,
#                 page_content="",
#                 metadata={
#                     "name":filename,
#                     "path":Path(file_path),
#                     "parsed_entities": {
#                         "entities":[],
#                         "topics":[],
#                         "key_terms":[],

#                     }
#                 }
#             )
#             self.documents[doc_id]= document
#             uploaded_docs.append(document)


#         return uploaded_docs 
    

#     def get_file_list(self)-> List[Document]:
#         return list(self.documents.values())
    
#     def remove_file(self,file_id:str):

#         if file_id in self.documents:
#             doc = self.documents[file_id]
#             file_path = doc.path
#             try:
#                 if file_path.exists() :
#                     file_path.unlink()

                


#             except Exception as e:
                
#                 pass 
#             del self.documents[file_id]
#             return True 
#         return False


    


                





            


            
