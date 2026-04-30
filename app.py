import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
from google import genai

# --- 網頁介面標題 ---
st.set_page_config(page_title="真・AC 自動機", page_icon="🤖")
st.title("🤖 真・AC 自動機 (ZeroJudge)")
st.caption("2026 未來版 - 自動抓題、AI 解題、一鍵 AC")

# --- 側邊欄設定區 ---
with st.sidebar:
    st.header("🔑 個人憑證設定")
    gemini_key = st.text_input("Gemini API Key", type="password", help="請至 Google AI Studio 申請")
    session_id = st.text_input("ZeroJudge JSESSIONID", help="從瀏覽器 Cookies 取得")
    
    st.divider()
    st.markdown("""
    ### 使用說明
    1. 填入你的 **Gemini API Key**。
    2. 登入 ZeroJudge，抓取 **JSESSIONID**。
    3. 輸入題目編號（如 `a001`）後點擊「開始攻克」。
    """)

# --- AC 自動機邏輯 ---
class ACAutomaton:
    def __init__(self, key, sid):
        self.session = requests.Session()
        self.base_url = "https://zerojudge.tw"
        self.client = genai.Client(api_key=key)
        cookie = requests.cookies.create_cookie(name='JSESSIONID', value=sid)
        self.session.cookies.set_cookie(cookie)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def check_login(self):
        res = self.session.get(f"{self.base_url}/UserStatistic")
        return "登出" in res.text

    def run_process(self, pid):
        # 1. 抓題
        with st.status(f"正在攻克題目 {pid}...", expanded=True) as status:
            st.write("🔍 正在抓取題目敘述...")
            res = self.session.get(f"{self.base_url}/ShowProblem?problemid={pid}")
            soup = BeautifulSoup(res.text, 'html.parser')
            content = soup.find('div', id='problem_content')
            if not content:
                st.error("找不到題目內容，請檢查編號。")
                return

            # 2. AI 解題
            st.write("🧠 AI 正在思考解法 (Gemini 2.5)...")
            prompt = f"你是一個資深競賽選手。請寫出這題 ZeroJudge 的 C++ 代碼。只輸出代碼，不要 Markdown 標籤：\n{content.get_text()}"
            
            try:
                ai_res = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                code = ai_res.text.strip().replace('```cpp', '').replace('```', '').strip()
                st.code(code, language='cpp')
            except Exception as e:
                st.error(f"AI 思考失敗: {e}")
                return

            # 3. 提交
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

            # 4. 監控
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

# --- 主程式介面 ---
target_pid = st.text_input("題目編號", value="a001", placeholder="例如: d485")

if st.button("🚀 開始攻克", type="primary"):
    if not gemini_key or not session_id:
        st.warning("請先在側邊欄填入 API Key 和 JSESSIONID！")
    else:
        bot = ACAutomaton(gemini_key, session_id)
        if bot.check_login():
            bot.run_process(target_pid)
        else:
            st.error("JSESSIONID 無效或已過期，請重新從瀏覽器取得。")