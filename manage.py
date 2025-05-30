from flask import Flask, request, jsonify
from flask_cors import CORS  # 解決跨來源問題
from flask import Response
import requests
import json


def analysis_module(module, code, user_input):
    

    chromadb_response =  requests.post("http://localhost:5001/rag",  json={"query": code,"module":"analysis"}   )      
    # 解析回傳結果

    if chromadb_response.status_code == 200:
        data = chromadb_response.json()
        # print("查詢結果（context）：")
        # print(data["context"])
    else:
        print("查詢失敗，錯誤碼：", chromadb_response.status_code)
        print(chromadb_response.text)

    RAG_data = data.get('context', '')


    response = requests.post(
    "http://localhost:11434/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
            "model": "codellama:13b",
            "messages": [ 
                {
                    "role": "system",
                    "content": f'''
                    請嚴格遵守以下規則：
                    1.回答一定要是繁體中文
                    2.所有內容都必須參考以下資料內容：{RAG_data}！
                    3.不得添加與任務無關的內容或英文說明。

                    你的任務如下：
                    你是一位專業的程式碼審查專家，請幫我完成以下任務且每個內容至少要100字：
                    1. 閱讀這段程式碼  
                    2.解釋它的功能與流程 
                    3.標出可能會出錯的地方 
                    4.提出優化建議（可選）請使用條列方式清楚說明。
                    再次提醒：所有對話內容必須使用【繁體中文】，不得混用英文或其他語言。
                    '''  
                },
                {
                    "role": "user",
                    "content": '''
                    請用繁體中文說明這段程式碼的功能與流程，並指出可能會出錯的地方。請使用條列方式清楚說明。\n
                    程式碼如下：\n{code}\n'''
                }
            ]
        }
    )
    

    
    reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    # reply= reply.replace("\n", "<br>").replace("\t", "&emsp;")
    # print(reply)
    response_json = json.dumps({"reply":reply}, ensure_ascii=False)
    return Response(response=response_json, status=200, content_type="application/json; charset=utf-8")

def conversation_module(module, code, user_input):
# data = request.json
    # user_input = data.get("user_input","")
    # code = data.get("code","")
 

    chromadb_response =  requests.post("http://localhost:5001/rag",json={"query": user_input,"module":"conversation"})     # 用 JSON 格式傳送資料
    
    # 解析回傳結果
    if chromadb_response.status_code == 200:
        data = chromadb_response.json()
        # print("查詢結果（context）：")
        # print(data["context"])
    else:
        print("查詢失敗，錯誤碼：", chromadb_response.status_code)
        print(chromadb_response.text)

    RAG_data = data.get('context', '')
    # print(user_input)

    response = requests.post(
    "http://localhost:11434/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
            "model": "deepseek-r1:7b",
            "messages": [ 
                {
                    "role": "system",
                    "content": f'''
                    你是一位 podcast 腳本編劇，擅長撰寫【助教與學生之間的程式學習對話】。

                    教材內容：{code}
                    大綱:{user_input}

                    任務目標如下：
                    請你根據以下【教學目標】，撰寫一段自然、富有教育意義的繁體中文對話。對話應呈現「助教一步步引導學生」的過程，幫助學生理解程式是如何逐步寫出來的。

                    ---

                    【腳色設定】
                    - 助教（T）：熟悉程式設計，擅長引導與提問，不直接給答案。
                    - 學生（S）：剛開始學習，有邏輯思考力但缺乏程式經驗。

                    【教學目標】
                    - 幫助學生理解程式邏輯


                    【風格與要求】
                    - 全程使用【繁體中文】
                    - 助教需透過提問與提示，引導學生思考並逐步完成程式邏輯
                    - 學生會試著回答，有錯助教可引導修正
                    - 對話長度約 10~14 輪
                    - 對話中可適度嵌入小段程式碼（簡單清楚）

                    請注意：
                    1. 所有對話請使用【繁體中文】，不可混用英文或其他語言  
                    2. 請確保整段內容都涵蓋「內容大綱」的重點  
                    '''
                },
                {
                    "role": "user",
                    "content": 
                    '''
                    現在，請開發 Podcast 對話。
                    語言：繁體中文
                    
                    輸出要求：
                    腳本格式：腳本應由主持人先開口。對話由主持人與來賓交替進行，一次一行。每一行前面請不要加上說話者名字。
                    輸出內容：最終腳本僅應包含對話內容。請勿在輸出中加入任何 XML 標籤或其他格式。
                    請依照這些指示，創作一段內容豐富又引人入勝的高品質 Podcast 對話腳本。
                    ''' 
                }
            ]
        }
    )
    

    
    reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    # reply= reply.replace("\n", "<br>").replace("\t", "&emsp;")
    response_json = json.dumps({"reply":reply}, ensure_ascii=False)
    return Response(response=response_json, status=200, content_type="application/json; charset=utf-8")

def conclusion_module(module, code, user_input):
  

    chromadb_response =  requests.post("http://localhost:5001/rag", json={"query": user_input,"module":"conclusion"})       # 用 JSON 格式傳送資料
        
    # 解析回傳結果
    if chromadb_response.status_code == 200:
        data = chromadb_response.json()
        # print("查詢結果（context）：")
        # print(data["context"])
    else:
        print("查詢失敗，錯誤碼：", chromadb_response.status_code)
        print(chromadb_response.text)
    
    RAG_data = data.get('context', '')

    response = requests.post(
    "http://localhost:11434/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
            "model": "qwen:7b",
            "messages": [ 
                {
                    "role": "system",
                    "content":  f'''
                    你是一位專業 podcast 腳本編劇，請根據以下【對話內容】，撰寫一段自然、口語、具啟發性的小結語，由「助教」作為總結發言。
                    '''
                },
                {
                    "role": "user",
                    "content":
                    f'''
                    host：助教
                    guest：學生
                    language：繁體中文
                    ---
                    【對話內容】: {user_input}
                    ---
                    ✦ 結尾風格與要求：
                    1. 使用【繁體中文】
                    2. 自然口語、有點輕鬆但有教育意義
                    3. 概括本次學習的關鍵步驟與原則
                    4. 可鼓勵學生思考下一步或延伸學習方向
                    '''
                }
            ]
        }
    )
    

    
    reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    
    # reply= reply.replace("\n", "<br>").replace("\t", "&emsp;")
    response_json = json.dumps({"reply":reply}, ensure_ascii=False)
    return Response(response=response_json, status=200, content_type="application/json; charset=utf-8")


app = Flask(__name__)
CORS(app)  # 允許 Streamlit 存取此 API
@app.route("/manage", methods=["POST"])
def manage():
    data = request.json
    module = data.get("module","")
    code = data.get("code","")
    user_input = data.get("user_input","")
    
    if module == "analysis":
        return analysis_module(module, code, user_input)    
    
    if module == "conversation":
        return conversation_module(module, code, user_input)
        
    if module == "conclusion":
        return conclusion_module(module, code, user_input)
        
    else  :
        return jsonify({"error": "Invalid module"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=4000)