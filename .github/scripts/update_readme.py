import json
import traceback
import requests

# 設定多個資料來源
SOURCES = {
    "experiences": "https://raw.githubusercontent.com/longtai-me/longtai-me/refs/heads/main/public/json/experiences.json",
    "support": "https://raw.githubusercontent.com/longtai-me/longtai-me/refs/heads/main/public/json/support.json",
    "certificate": "https://raw.githubusercontent.com/longtai-me/longtai-me/refs/heads/main/public/json/certificate.json"
}

HEADERS = {
    "User-Agent": "longtai-me-readme-updater"
}


def fetch_data(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def render_experiences(data):
    table = "| 年份 | 項目 | 描述 | 角色 |\n"
    table += "| :--- | :--- | :--- | :--- |\n"

    sorted_data = sorted(
        data,
        key=lambda x: x.get("years", "0"),
        reverse=True
    )

    for exp in sorted_data:
        title = (
            f"[{exp.get('title')}]({exp.get('link')})"
            if exp.get("link")
            else exp.get("title", "")
        )

        table += (
            f"| {exp.get('years', '')} "
            f"| {title} "
            f"| {exp.get('subtitle', '')} "
            f"| {exp.get('role', '')} |\n"
        )

    return table


def render_support(data):
    table = "| 項目 | 描述 | 角色 |\n"
    table += "| :--- | :--- | :--- |\n"

    for supp in data:
        title = (
            f"[{supp.get('title')}]({supp.get('link')})"
            if supp.get("link")
            else supp.get("title", "")
        )

        table += (
            f"| {title} "
            f"| {supp.get('subtitle', '')} "
            f"| {supp.get('desc', '')} |\n"
        )

    return table


def render_certificate(data):
    table = "| 證書 | 發證單位 | 日期 | 驗證 |\n"
    table += "| :--- | :--- | :--- | :--- |\n"

    sorted_data = sorted(
        data,
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    for cert in sorted_data:
        title = (
            f"{cert.get('name')}"
            if cert.get("link")
            else cert.get("name", "")
        )

        verify = (
            f"[Verify]({cert.get('link')})"
            if cert.get("link")
            else "-"
        )

        table += (
            f"| {title} "
            f"| {cert.get('organization', '')} "
            f"| {cert.get('date', '')} "
            f"| {verify} |\n"
        )

    return table


def update_section(readme, section_id, new_content):
    start_tag = f"<!--START_SECTION:{section_id}-->"
    end_tag = f"<!--END_SECTION:{section_id}-->"

    if start_tag not in readme or end_tag not in readme:
        print(f"[WARN] 找不到 section: {section_id}")
        return readme

    start_index = readme.index(start_tag) + len(start_tag)
    end_index = readme.index(end_tag)

    updated = (
        readme[:start_index]
        + "\n\n"
        + new_content.strip()
        + "\n\n"
        + readme[end_index:]
    )

    print(f"[OK] 更新 section: {section_id}")

    return updated


if __name__ == "__main__":

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()

        # Experiences
        try:
            exp_data = fetch_data(SOURCES["experiences"])
            exp_table = render_experiences(exp_data)

            readme_content = update_section(
                readme_content,
                "experiences",
                exp_table
            )

        except Exception as e:
            print(f"[ERROR] Experiences 處理失敗: {e}")
            traceback.print_exc()

        # Support
        try:
            supp_data = fetch_data(SOURCES["support"])
            supp_table = render_support(supp_data)

            readme_content = update_section(
                readme_content,
                "support",
                supp_table
            )

        except Exception as e:
            print(f"[ERROR] Support 處理失敗: {e}")
            traceback.print_exc()

        # Certificate
        try:
            cert_data = fetch_data(SOURCES["certificate"])
            cert_table = render_certificate(cert_data)

            readme_content = update_section(
                readme_content,
                "certificate",
                cert_table
            )

        except Exception as e:
            print(f"[ERROR] Certificate 處理失敗: {e}")
            traceback.print_exc()

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

        print("[DONE] README 更新完成")

    except Exception as e:
        print(f"[FATAL] 主流程失敗: {e}")
        traceback.print_exc()