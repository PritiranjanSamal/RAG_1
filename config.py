import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VECTOR_STORE_PATH = "/Workspace/Users/draxop7536@gmail.com/RAG_1/Data/Vector_Store_e8f730ef"            #768
#"/Workspace/Users/draxop7536@gmail.com/RAG_1/Data/Vector_Store_3f5994b2"                               #384
# os.path.join(
#     BASE_DIR,
#     "Data",
#     "Vector_Store"
# )

PDF_DIRECTORY = os.path.join(
    BASE_DIR,
    "Data",
    "PDF"
)

COLLECTION_NAME = "pdf_documents"

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"        #768
# "all-MiniLM-L6-v2"                             #384


GROQ_API_KEY = os.getenv("GROQ_API_KEY1")

LLM_MODEL = "llama-3.1-8b-instant" #"llama-3.3-70b-versatile"
# "llama-3.1-8b-instant"

TEMPERATURE = 0.1

MAX_TOKENS = 1024

TOP_K = 5  # Number of documents to retrieve

MIN_SCORE = 0.05  # Minimum score threshold (matching notebook success)