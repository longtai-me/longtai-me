import json
import requests

# 設定多個資料來源
SOURCES = {
    "experiences": "https://raw.githubusercontent.com/long-tai-0925/NEW-ME/refs/heads/main/public/json/experiences.json",
    "support": "https://raw.githubusercontent.com/long-tai-0925/NEW-ME/refs/heads/main/public/json/support.json"
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
    # 這裡根據你的 support.json 結構調整
    table = "| 項目 | 描述 | 角色 |\n| :--- | :--- | :--- |\n"
    for supp in data:
        # 修正點：確保對應到你 JSON 的 Key，如果 JSON 是 link/title/subtitle/role 結構：
        title = f"[{supp.get('title')}]({supp.get('link')})" if supp.get('link') else supp.get('title')
        table += f"| {title} | {supp.get('subtitle', '')} | {supp.get('desc', '')} |\n"
    return table

def update_section(readme, section_id, new_content):
    start_tag = f"<!-- START_SECTION:{section_id} -->"
    end_tag = f"<!-- END_SECTION:{section_id} -->"
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
        # 修正點：將原先誤植的 proj_data 改為 supp_data，並對應正確的 Key
        supp_data = fetch_data(SOURCES["support"])
        readme_content = update_section(readme_content, "support", render_support(supp_data))
    except Exception as e:
        print(f"Support JSON 尚未就緒或發生錯誤: {e}")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
