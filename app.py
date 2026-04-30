import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
from google import genai

st.set_page_config(page_title="真・AC 自動機", page_icon="🤖")
st.title("🤖 真・AC 自動機 (ZeroJudge - Gemini 版)")
st.caption("2026 未來版 - 自動抓題、Gemini AI 解題、一鍵 AC")

with st.sidebar:
    st.header("🔑 個人憑證設定")
    gemini_key = st.text_input("Gemini API Key", type="password", help="請至 Google AI Studio 申請")
    session_id = st.text_input("ZeroJudge JSESSIONID", help="從瀏覽器 Cookies 取得")
    st.divider()
    st.markdown("### 使用說明\n1. 填入 API Key\n2. 填入 JSESSIONID\n3. 輸入題號並開始")

class ACAutomaton:
    def __init__(self, key, sid):
        self.session = requests.Session()
        self.base_url = "https://zerojudge.tw"
        self.client = genai.Client(api_key=key)
        cookie = requests.cookies.create_cookie(name='JSESSIONID', value=sid)
        self.session.cookies.set_cookie(cookie)
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    def check_login(self):
        res = self.session.get(f"{self.base_url}/UserStatistic")
        return "登出" in res.text

    def run_process(self, pid):
        with st.status(f"正在攻克題目 {pid}...", expanded=True) as status:
            st.write("🔍 正在抓取題目敘述...")
            res = self.session.get(f"{self.base_url}/ShowProblem?problemid={pid}")
            soup = BeautifulSoup(res.text, 'html.parser')
            content = soup.find('div', id='problem_content')
            if not content:
                st.error("找不到題目內容，請檢查編號。")
                return

            st.write("🧠 Gemini 正在思考解法...")
            prompt = f"""
            你是一位 IOI 級別的頂尖 C++ 演算法選手。請為這道 ZeroJudge 題目撰寫可以一次 AC 的 C++ 程式碼。

            【致命要求：輸出格式必須 100% 一致】：
            1. 仔細閱讀題目的「輸出說明」。你的輸出文字、空格、大小寫、標點符號必須與範例完全一模一樣！
            2. 題目若要求印出特定字串（如 Two different roots），絕對不能只印數字。
            3. 算出 -0 請轉換為 0。

            【常規競賽規範】：
            4. 加入 `ios_base::sync_with_stdio(false); cin.tie(0);`。
            5. 預設使用 `long long` 避免溢位。
            6. 使用 `while (cin >> ...)` 讀取到 EOF。
            7. 只輸出純 C++ 代碼，絕對不要包含 Markdown 標籤 (如 ```cpp) 或是任何解釋文字。

            題目敘述如下：
            {content.get_text()}
            """
            
            model_pool = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"]
            code = ""
            
            for model_name in model_pool:
                try:
                    ai_res = self.client.models.generate_content(model=model_name, contents=prompt)
                    code = ai_res.text.strip().replace('```cpp', '').replace('```', '').strip()
                    st.success(f"✅ 成功使用大腦：{model_name}")
                    st.code(code, language='cpp')
                    break
                except Exception as e:
                    err_msg = str(e)
                    if any(keyword in err_msg for keyword in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]):
                        st.warning(f"⚠️ `{model_name}` 暫時無法使用，切換備用模型...")
                        continue
                    else:
                        st.error(f"發生未知的 AI 錯誤: {err_msg}")
                        return

            if not code:
                st.error("❌ 所有 AI 模型的額度都已用盡！")
                return

            st.write("🚀 正在提交代碼...")
            prob_url = f"{self.base_url}/ShowProblem?problemid={pid}"
            res_prob = self.session.get(prob_url)
            soup_prob = BeautifulSoup(res_prob.text, 'html.parser')
            payload = {'language': 'CPP', 'code': code, 'contestid': '0', 'problemid': pid, 'action': 'SubmitCode'}
            for tag in soup_prob.find_all('input', type='hidden'):
                if tag.get('name'): payload[tag.get('name')] = tag.get('value', '')
            
            self.session.headers.update({'X-Requested-With': 'XMLHttpRequest', 'Referer': prob_url})
            submit_res = self.session.post(f"{self.base_url}/Solution.api", data=payload).json()
            
            if not submit_res.get("success"):
                st.error(f"提交失敗: {submit_res.get('message')}")
                return

            sid = submit_res["data"]["solutionId"]
            st.write(f"⏳ 等待評分中 (ID: {sid})...")
            for _ in range(12):
                time.sleep(5)
                res_status = self.session.get(f"{self.base_url}/Submissions?solutionid={sid}")
                if "AC" in res_status.text:
                    status.update(label="✨ 題目已 AC (Accepted)！", state="complete")
                    st.balloons()
                    return
                elif any(x in res_status.text for x in ["WA", "CE", "TLE", "RE"]):
                    st.error("評分結果非 AC，請檢查代碼或重試。")
                    return
            st.warning("評分逾時。")

target_pid = st.text_input("題目編號", value="a006", placeholder="例如: a006")
if st.button("🚀 開始攻克", type="primary"):
    if not gemini_key or not session_id:
        st.warning("請先在側邊欄填入 API Key 和 JSESSIONID！")
    else:
        bot = ACAutomaton(gemini_key, session_id)
        if bot.check_login():
            bot.run_process(target_pid)
        else:
            st.error("JSESSIONID 無效或已過期。")