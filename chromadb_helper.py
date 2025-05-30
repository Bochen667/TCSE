from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import chromadb
import os
from pathlib import Path
from PyPDF2 import PdfReader

# 初始化 Flask
app = Flask(__name__)

# 嵌入模型
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 使用 Persistent 模式
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="rag_docs")

# 讀取一份檔案內容（支援 .txt 和 .pdf）
def read_file(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return ""

# 增量更新模組資料
def update_module_data(module):
    module_path = Path(f"database/{module}")
    if not module_path.exists():
        print(f"[WARN] 模組 '{module}' 找不到對應資料夾")
        return

    existing_ids = set(collection.get(where={"module": module})["ids"])
    added_count = 0

    for file in module_path.glob("*"):
        if file.suffix.lower() not in [".txt", ".pdf"]:
            continue

        file_id = f"{module}_{file.name}"
        if file_id in existing_ids:
            continue

        content = read_file(str(file))
        if not content.strip():
            continue

        embedding = embedder.encode([content])[0].tolist()
        collection.add(
            documents=[content],
            embeddings=[embedding],
            ids=[file_id],
            metadatas=[{"module": module, "filename": file.name}]
        )
        added_count += 1

    print(f"[INFO] 模組 '{module}' 已增量更新，共新增 {added_count} 筆資料")

# 查詢 API
@app.route("/rag", methods=["POST"])
def rag_search():
    data = request.get_json()
    query = data.get("query", "").strip()
    module = data.get("module", "").strip()

    if not query:
        return jsonify({"error": "Query is required"}), 400
    if not module:
        return jsonify({"error": "Module is required"}), 400

    # 增量更新資料
    update_module_data(module)

    # 查詢
    query_vec = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_vec,
        n_results=3,
        where={"module": module}
    )

    documents = results.get("documents", [[]])[0]
    return jsonify({"context": "\n".join(documents)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)