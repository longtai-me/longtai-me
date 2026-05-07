import json
import requests

JSON_URL = "https://raw.githubusercontent.com/long-tai-0925/NEW-ME/refs/heads/main/public/json/experiences.json"

def fetch_data():
    response = requests.get(JSON_URL)
    return response.json()

def generate_markdown_table(data):
    # 建立表格標頭
    table = "| 年份 | 項目 | 描述 / 主題 | 角色 / 成績 |\n"
    table += "| :--- | :--- | :--- | :--- |\n"
    
    # 按照年份由新到舊排序
    sorted_data = sorted(data, key=lambda x: x.get('years', '0'), reverse=True)
    
    for exp in sorted_data:
        years = exp.get('years', '')
        # 如果有連結就做成超連結，否則純文字
        title = exp.get('title', '')
        link = exp.get('link', '')
        title_display = f"[{title}]({link})" if link else title
        
        subtitle = exp.get('subtitle', '')
        role = exp.get('role', '')
        
        table += f"| {years} | {title_display} | {subtitle} | {role} |\n"
    
    return table

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    start_tag = "<!-- START_SECTION:experiences -->"
    end_tag = "<!-- END_SECTION:experiences -->"
    
    # 確保標記存在，避免報錯
    if start_tag in readme and end_tag in readme:
        header = readme.split(start_tag)[0]
        footer = readme.split(end_tag)[1]
        updated_readme = f"{header}{start_tag}\n\n{new_content}\n{end_tag}{footer}"
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)
    else:
        print("未在 README.md 中找到標記標籤")

if __name__ == "__main__":
    try:
        data = fetch_data()
        table_content = generate_markdown_table(data)
        update_readme(table_content)
        print("README 已成功更新！")
    except Exception as e:
        print(f"發生錯誤: {e}")
