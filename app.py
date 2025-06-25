# from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename
# import os

# from app.parse_with_docling import extract_pdf_to_markdown
# from app.loader import load_text_chunks, load_tables
# from app.rag_model import rag_answer
# from app.tapas_model import is_table_query, select_table_by_content, markdown_to_dataframe, tapas_answer

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load default data
# text_chunks = load_text_chunks("data/text_chunks.md")
# tables = load_tables("data/tables.md")


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/upload", methods=["POST"])
# def upload_file():
#     global text_chunks, tables

#     if "file" not in request.files:
#         return "No file part", 400

#     file = request.files["file"]
#     if file.filename == "":
#         return "No selected file", 400

#     filename = secure_filename(file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(file_path)

#     # Run docling processing
#     extract_pdf_to_markdown(file_path)

#     # Reload processed data
#     text_chunks = load_text_chunks("data/text_chunks.md")
#     tables = load_tables("data/tables.md")

#     return "File uploaded and processed", 200


# @app.route("/query", methods=["POST"])
# def handle_query():
#     q = request.json.get("question", "")
#     if not q:
#         return jsonify({"error": "No question provided"}), 400

#     if is_table_query(q):
#         table_entry = select_table_by_content(tables, q)
#         df = markdown_to_dataframe(table_entry["table"])
#         answer = tapas_answer(df, q)
#         return jsonify({"source": "TAPAS", "title": table_entry["title"], "answer": answer})
#     else:
#         answer = rag_answer(text_chunks, q)
#         return jsonify({"source": "RAG", "answer": answer})


# if __name__ == "__main__":
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     app.run(debug=True)


#--------------------------------------------------------------------------------------------------------------

# index.html path issue 

# from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename
# import os

# # Setup correct path for templates
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# app = Flask(__name__, template_folder=TEMPLATES_DIR)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Import project modules
# from app.parse_with_docling import extract_pdf_to_markdown
# from app.loader import load_text_chunks, load_tables
# from app.rag_model import rag_answer
# from app.tapas_model import is_table_query, select_table_by_content, markdown_to_dataframe, tapas_answer

# # Load default data
# text_chunks = load_text_chunks(os.path.join(BASE_DIR, "data/text_chunks.md"))
# tables = load_tables(os.path.join(BASE_DIR, "data/tables.md"))


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/upload", methods=["POST"])
# def upload_file():
#     global text_chunks, tables

#     if "file" not in request.files:
#         return "No file part", 400

#     file = request.files["file"]
#     if file.filename == "":
#         return "No selected file", 400

#     filename = secure_filename(file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(file_path)

#     # Run docling processing
#     extract_pdf_to_markdown(file_path)

#     # Reload processed data
#     text_chunks = load_text_chunks(os.path.join(BASE_DIR, "data/text_chunks.md"))
#     tables = load_tables(os.path.join(BASE_DIR, "data/tables.md"))

#     return "File uploaded and processed", 200


# @app.route("/query", methods=["POST"])
# def handle_query():
#     q = request.json.get("question", "")
#     if not q:
#         return jsonify({"error": "No question provided"}), 400

#     if is_table_query(q):
#         table_entry = select_table_by_content(tables, q)
#         df = markdown_to_dataframe(table_entry["table"])
#         answer = tapas_answer(df, q)
#         return jsonify({"source": "TAPAS", "title": table_entry["title"], "answer": answer})
#     else:
#         answer = rag_answer(text_chunks, q)
#         return jsonify({"source": "RAG", "answer": answer})


# if __name__ == "__main__":
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     print(f"Templates directory: {TEMPLATES_DIR}")
#     app.run(debug=True)




#---------------------------------------------------------------------------------------------------

# UPDATE - 3

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

# === Base Paths ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# === Initialize Flask ===
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === Project Module Imports ===
from app.parse_with_docling import extract_pdf_to_markdown
from app.loader import load_text_chunks, load_tables
from app.rag_model import rag_answer, get_or_build_index
from app.tapas_model import is_table_query, select_table_by_content, markdown_to_dataframe, tapas_answer

# === Load initial data ===
text_chunks = load_text_chunks(os.path.join(DATA_DIR, "text_chunks.md"))
tables = load_tables(os.path.join(DATA_DIR, "tables.md"))
index, embeddings = get_or_build_index(text_chunks)

# === Routes ===

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    global text_chunks, tables, index, embeddings

    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # ✅ Parse and generate text_chunks.md and tables.md
    extract_pdf_to_markdown(file_path)

    # ✅ Reload updated markdown content
    text_chunks = load_text_chunks(os.path.join(DATA_DIR, "text_chunks.md"))
    tables = load_tables(os.path.join(DATA_DIR, "tables.md"))

    # ✅ Rebuild FAISS index for new chunks
    index, embeddings = get_or_build_index(text_chunks)

    return "File uploaded and processed", 200


@app.route("/query", methods=["POST"])
def handle_query():
    global text_chunks, tables, index, embeddings

    q = request.json.get("question", "")
    if not q:
        return jsonify({"error": "No question provided"}), 400

    if is_table_query(q):
        table_entry = select_table_by_content(tables, q)
        df = markdown_to_dataframe(table_entry["table"])
        answer = tapas_answer(df, q)
        return jsonify({
            "source": "TAPAS",
            "title": table_entry["title"],
            "answer": answer
        })
    else:
        answer = rag_answer(text_chunks, q, index, embeddings)
        return jsonify({
            "source": "RAG",
            "answer": answer
        })


if __name__ == "__main__":
    print(f"📂 Templates: {TEMPLATES_DIR}")
    print(f"📂 Static: {STATIC_DIR}")
    print(f"📂 Uploads: {UPLOAD_FOLDER}")
    app.run(debug=True)
