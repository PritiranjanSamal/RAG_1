# RAG System UI Deployment Guide

## 🎯 Overview

You now have three ways to use your RAG system:

1. **Import as a module** in notebooks (easiest for testing)
2. **Run Streamlit locally** in a notebook cell
3. **Deploy as a Databricks App** (production-ready web app)

---

## 🚀 Option 1: Import as Module (Quick Testing)

### In any notebook:

```python
import sys
sys.path.insert(0, '/Workspace/Users/draxop7536@gmail.com')

from rag_core import initialize_rag_system
import os

# Initialize
rag_pipeline, retriever, _, _ = initialize_rag_system(
    vector_store_path="/Workspace/Users/draxop7536@gmail.com/RAG_1/Data/Vector_Store_3f5994b2",
    groq_api_key=os.getenv("GROQ_API_KEY1"),
    model_name="llama-3.1-8b-instant"
)

# Query
result = rag_pipeline.query("Your question here?")
print(result['answer'])
```

**Benefits:**
- Simplest approach
- Reuse your logic across multiple notebooks
- No UI needed for programmatic access

---

## 🖥️ Option 2: Run Streamlit Locally

### Step 1: Install Streamlit

```python
%pip install streamlit
dbutils.library.restartPython()
```

### Step 2: Move files to RAG_1 folder

First, let's organize the files:

```python
import shutil
import os

# Move rag_core.py to RAG_1 folder
src = "/Workspace/Users/draxop7536@gmail.com/rag_core.py"
dst = "/Workspace/Users/draxop7536@gmail.com/RAG_1/rag_core.py"
if os.path.exists(src):
    shutil.copy(src, dst)
    print(f"✅ Copied rag_core.py to RAG_1")

# Move rag_ui_app.py to RAG_1 folder  
src = "/Workspace/Users/draxop7536@gmail.com/rag_ui_app.py"
dst = "/Workspace/Users/draxop7536@gmail.com/RAG_1/rag_ui_app.py"
if os.path.exists(src):
    shutil.copy(src, dst)
    print(f"✅ Copied rag_ui_app.py to RAG_1")
```

### Step 3: Update rag_ui_app.py path reference

Edit line 11 in `rag_ui_app.py` to:
```python
workspace_path = "/Workspace/Users/draxop7536@gmail.com/RAG_1"
```

### Step 4: Run Streamlit

```python
%sh
cd /Workspace/Users/draxop7536@gmail.com/RAG_1
streamlit run rag_ui_app.py --server.port=8501 --server.headless=true
```

**Note:** You'll get a URL like `http://localhost:8501` - this works in Databricks notebooks with port forwarding.

---

## 🌐 Option 3: Deploy as Databricks App (Recommended for Production)

### Prerequisites

1. Your workspace must support Databricks Apps (contact your admin if unsure)
2. You need the Databricks CLI installed

### Step 1: Prepare App Directory Structure

Your `RAG_1` folder should have:
```
RAG_1/
├── app.yaml           # Already created
├── rag_ui_app.py      # Move here
├── rag_core.py        # Move here
└── Data/
    └── Vector_Store_3f5994b2/
```

### Step 2: Store Your Groq API Key in Secrets

```bash
# Create a secret scope (one time only)
databricks secrets create-scope groq

# Add your API key
databricks secrets put-secret groq api_key
# (This will open an editor - paste your key and save)
```

### Step 3: Update app.yaml

The `app.yaml` is already created, but verify it contains:

```yaml
command: ["streamlit", "run", "rag_ui_app.py", "--server.port=8080"]

env:
  - name: GROQ_API_KEY1
    value: "${secrets/groq/api_key}"
```

### Step 4: Create a requirements.txt (optional but recommended)

In RAG_1 folder:

```txt
streamlit>=1.28.0
langchain-groq
langchain-core
chromadb
sentence-transformers
numpy
python-dotenv
```

### Step 5: Deploy Using Databricks CLI

```bash
# Navigate to workspace
cd /Workspace/Users/draxop7536@gmail.com/RAG_1

# Create the app
databricks apps create rag-qa-system \
  --source-code-path . \
  --description "RAG Question Answering System"

# Start the app
databricks apps start rag-qa-system

# Get the app URL
databricks apps get rag-qa-system
```

### Step 6: Access Your App

You'll receive a URL like:
```
https://<workspace-url>/apps/rag-qa-system
```

Open it in your browser and use the UI!

---

## 🔧 Using the UI

### Sidebar Configuration

1. **Groq API Key**: Enter your API key (or it will auto-load from env)
2. **Vector Store Path**: Path to your ChromaDB store
3. **LLM Model**: Choose from available Groq models
4. **Advanced Settings**:
   - `top_k`: Number of documents to retrieve (1-10)
   - `min_score`: Minimum relevance threshold (0-1)

### Main Interface

- **Query Tab**: Ask questions and get answers
- **Retrieved Documents Tab**: See which documents were used
- **History Tab**: View all past queries

### Features

- 💡 **Color-coded confidence**: Green (high), Yellow (medium), Red (low)
- 📚 **Source citations**: See which documents contributed to answers  
- 📊 **Query history**: Track all your questions
- ⚙️ **Flexible configuration**: Adjust retrieval parameters on the fly

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'rag_core'"
**Solution**: Ensure `rag_core.py` is in the same directory as `rag_ui_app.py` or update the sys.path in the UI file.

### Issue: "Vector store path does not exist"
**Solution**: Verify the path to your ChromaDB vector store is correct in the sidebar.

### Issue: "No Groq API key provided"
**Solution**: Either:
- Enter it manually in the sidebar
- Set `GROQ_API_KEY1` environment variable
- Configure Databricks secrets (for Apps)

### Issue: "ChromaDB lock error"
**Solution**: Make sure no other process is using the vector store. Restart Python kernel if needed.

---

## 🔄 Updating Your App

If you deployed as a Databricks App:

```bash
# Stop the app
databricks apps stop rag-qa-system

# Update files in RAG_1 folder

# Restart
databricks apps start rag-qa-system
```

---

## 📝 Next Steps

1. **Test the module import** in your notebook (cells already added)
2. **Try Streamlit locally** to see the UI in action
3. **Deploy as a Databricks App** for a permanent web interface
4. **Customize the UI** - modify `rag_ui_app.py` to add features
5. **Share with team** - give them the app URL

---

## 📦 File Summary

| File | Purpose | Location |
|------|---------|----------|
| `rag_core.py` | Core RAG logic (reusable) | `/Users/draxop7536@gmail.com/` or `RAG_1/` |
| `rag_ui_app.py` | Streamlit UI | `/Users/draxop7536@gmail.com/` or `RAG_1/` |
| `app.yaml` | Databricks App config | `RAG_1/` |
| `dataIngesation.ipynb` | Original notebook + tests | `RAG_1/` |

---

**Questions?** The UI is fully functional and ready to use! 🎉
