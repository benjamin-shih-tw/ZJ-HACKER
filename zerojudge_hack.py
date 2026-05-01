import requests
from bs4 import BeautifulSoup
import sys

# ================= 你的設定區 =================
USERNAME = 'your_username'     # 替換成你的 ZeroJudge 帳號
PASSWORD = 'your_password'     # 替換成你的 ZeroJudge 密碼
PROBLEM_ID = 'a001'            # 替換成你要提交的題目編號
CODE_FILE = 'solution.cpp'     # 你的程式碼檔案路徑
# ZeroJudge 語言代碼參考 (需確認當前網頁實際 value)：
# C: 'c', C++: 'cpp', Python: 'python', Java: 'java'
# just test
LANGUAGE = 'cpp'               
# ==============================================

# ZeroJudge 網址端點
BASE_URL = 'https://zerojudge.tw'
LOGIN_URL = f'{BASE_URL}/Login'
SUBMIT_URL = f'{BASE_URL}/SubmitCode'

def main():
    # 使用 Session 自動處理 Cookie
    session = requests.Session()
    
    # 1. 模擬登入
    print("[*] 嘗試登入 ZeroJudge...")
    # 根據網頁表單，傳遞帳號密碼
    login_payload = {
        'account': USERNAME,
        'passwd': PASSWORD,
    }
    
    # 發送 POST 請求進行登入
    res_login = session.post(LOGIN_URL, data=login_payload)
    res_login.encoding = 'utf-8'
    
    # 檢查是否登入成功 (通常登入後頁面會出現帳號名稱或「登出」字眼)
    if "登出" not in res_login.text:
        print("[-] 登入失敗！請檢查帳號密碼，或網站是否有加上圖形驗證碼。")
        sys.exit(1)
        
    print("[+] 登入成功！")

    # 2. 讀取要提交的程式碼
    try:
        with open(CODE_FILE, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except FileNotFoundError:
        print(f"[-] 找不到檔案：{CODE_FILE}")
        sys.exit(1)

    # 3. 模擬提交程式碼
    print(f"[*] 準備提交題目 {PROBLEM_ID}...")
    
    # 這裡的 key 必須完全符合 ZeroJudge 網頁表單上的 name 屬性
    submit_payload = {
        'problemid': PROBLEM_ID,
        'language': LANGUAGE,
        'code': code_content
    }
    
    res_submit = session.post(SUBMIT_URL, data=submit_payload)
    
    if res_submit.status_code == 200:
        print("[+] 提交請求已送出！")
        print("[*] 請至 ZeroJudge 網頁的「解題動態」確認實際的評測結果 (AC / WA / CE 等)。")
    else:
        print(f"[-] 提交失敗，HTTP 狀態碼：{res_submit.status_code}")

if __name__ == "__main__":
    main()