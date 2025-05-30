TCSE-Dify是透過Dify平台開發的前端，匯入yml檔案即可<br>
manage.py是後端程式，用於處理Dify平台的http response並回傳LLM回復<br>
chrombd_helper.py用於RAG，改進LLM回復能力，強化回復的準確度<br>

系統架構大約分成4個區塊，1~3均使用ollama模型，模型名稱可以在Dify平台的註解上查看
1.CODE分析模組
2.腳本製作模組
3.結論製作模組
4.TTS模組

