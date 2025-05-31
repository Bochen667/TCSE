※所有測試都是使用本地端ollama模型，請務必要使用Dify本地端匯入TCSE-Dify.yml及安裝對應ollama模型才可以正常執行<br>
<br>
TCSE-Dify是透過Dify平台開發的前端，在Dify本地或Dify Cloud 匯入TCSE-Dify.yml即可<br>
manage.py是後端程式，用於處理Dify平台的http response並回傳LLM回復<br>
chromabd_helper.py用於RAG，改進LLM回復能力，強化回復的準確度<br>
<br>
系統架構大約分成5個區塊，1~3均使用ollama模型，具體模型名稱可以在manage.py內查看<br>
1.CODE分析(ollama)<br>
2.腳本製作(ollama)<br>
3.結論製作(ollama)<br>
4.腳本修正(Grok API)<br>
5.語音合成 (Whisper API)(openAI whisper):轉換成prodcast語音檔<br>

