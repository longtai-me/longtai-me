import json
import requests

# 設定多個資料來源
SOURCES = {
    "experiences": "https://raw.githubusercontent.com/longtai-me/longtai-me/refs/heads/main/public/json/experiences.json",
    "support": "https://raw.githubusercontent.com/longtai-me/longtai-me/refs/heads/main/public/json/support.json",
    "certificate": "https://raw.githubusercontent.com/longtai-me/longtai-me/refs/heads/main/public/json/certificate.json"
}

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status() # 確保請求成功
    return response.json()

def render_experiences(data):
    table = "| 年份 | 項目 | 描述 | 角色 |\n| :--- | :--- | :--- | :--- |\n"
    sorted_data = sorted(data, key=lambda x: x.get('years', '0'), reverse=True)
    for exp in sorted_data:
        title = f"[{exp.get('title')}]({exp.get('link')})" if exp.get('link') else exp.get('title')
        table += f"| {exp.get('years', '')} | {title} | {exp.get('subtitle', '')} | {exp.get('role', '')} |\n"
    return table

def render_support(data):
    table = "| 項目 | 描述 | 角色 |\n| :--- | :--- | :--- |\n"
    for supp in data:
        title = f"[{supp.get('title')}]({supp.get('link')})" if supp.get('link') else supp.get('title')
        table += f"| {title} | {supp.get('subtitle', '')} | {supp.get('desc', '')} |\n"
    return table

def render_certificate(data):
    # 修正點：確保表頭與下方填入的資料欄位數量一致 (皆為 4 欄)
    table = "| 證書 | 發證單位 | 日期 | 驗證連結 |\n| :--- | :--- | :--- | :--- |\n"
    for cert in data:
        # 將證書名稱結合點擊連結
        title = f"[{cert.get('name')}]({cert.get('link')})" if cert.get('link') else cert.get('name')
        # 產生 4 欄： 證書(含連結) | 發證單位 | 日期 | 驗證連結文字
        table += f"| {title} | {cert.get('organization', '')} | {cert.get('date', '')} | [Verify]({cert.get('link', '')}) |\n"
    return table

def update_section(readme, section_id, new_content):
    start_tag = f""
    end_tag = f""
    if start_tag in readme and end_tag in readme:
        header = readme.split(start_tag)[0]
        footer = readme.split(end_tag)[1]
        return f"{header}{start_tag}\n\n{new_content}\n{end_tag}{footer}"
    return readme

if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()

    # 1. 處理經歷區塊
    try:
        exp_data = fetch_data(SOURCES["experiences"])
        readme_content = update_section(readme_content, "experiences", render_experiences(exp_data))
    except Exception as e:
        print(f"Experiences 處理失敗: {e}")

    # 2. 處理贊助/支援區塊
    try:
        supp_data = fetch_data(SOURCES["support"])
        readme_content = update_section(readme_content, "support", render_support(supp_data))
    except Exception as e:
        print(f"Support JSON 尚未就緒或發生錯誤: {e}")

    # 3. 處理證書區塊
    try:
        cert_data = fetch_data(SOURCES["certificate"])
        readme_content = update_section(readme_content, "certificate", render_certificate(cert_data))
    except Exception as e:
        print(f"Certificate JSON 尚未就緒或發生錯誤: {e}")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)