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

            # 2. AI 解題 (具備自動降檔與備援機制)
            st.write("🧠 AI 正在思考解法...")
            
            prompt = f"""
            你是一位 IOI 級別的頂尖 C++ 演算法選手。請為這道 ZeroJudge 題目撰寫可以一次 AC 的 C++ 程式碼。

            【嚴格規範】：
            1. 必須考慮時間複雜度，請加入 `ios_base::sync_with_stdio(false); cin.tie(0);` 來優化 I/O。
            2. 測資可能極大，請預設使用 `long long` 避免整數溢位 (Overflow)。
            3. ZeroJudge 通常有多筆測資，請務必使用 `while (cin >> ...)` 的方式讀取到 EOF。
            4. 注意邊界條件 (Edge cases)，例如 N=0 或空字串的情況。
            5. 只輸出純 C++ 代碼，絕對不要包含 Markdown 標籤 (如 ```cpp) 或任何解釋性文字，否則會導致編譯錯誤。

            題目敘述如下：
            {content.get_text()}
            """
            
            # 建立模型備援池：先試最強的 Pro，不行就換最新的 Flash，最後是 2.0 Flash
            model_pool = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"]
            code = ""
            
            for model_name in model_pool:
                try:
                    ai_res = self.client.models.generate_content(model=model_name, contents=prompt)
                    code = ai_res.text.strip().replace('```cpp', '').replace('```', '').strip()
                    st.success(f"✅ 成功使用大腦：{model_name}")
                    st.code(code, language='cpp')
                    break  # 成功生成代碼，跳出迴圈
                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                        st.warning(f"⚠️ `{model_name}` 額度耗盡，自動切換下一個模型...")
                        continue  # 繼續嘗試下一個模型
                    else:
                        st.error(f"發生未知的 AI 錯誤: {err_msg}")
                        return

            if not code:
                st.error("❌ 所有 AI 模型的額度都已用盡！請等待幾分鐘，或在左側更換新的 API Key。")
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
                    st.error("評分結果非 AC，請檢查代碼邏輯或重試。")
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