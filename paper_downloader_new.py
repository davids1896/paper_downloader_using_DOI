import os
import requests
from bs4 import BeautifulSoup
import time

# Sci-Hub 网址（可能需要更新）
SCI_HUB_URL = "https://sci-hub.st/"

# 读取DOI列表
def read_doi_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        dois = [line.strip() for line in f if line.strip()]
    return dois

# 获取Sci-Hub上的PDF链接
def get_pdf_url(doi):
    url = f"{SCI_HUB_URL}{doi}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        iframe = soup.find("iframe")
        if iframe and "src" in iframe.attrs:
            pdf_url = iframe["src"]
            if pdf_url.startswith("//"):
                pdf_url = "https:" + pdf_url
            return pdf_url
    except requests.RequestException as e:
        print(f"❌ DOI {doi} 访问失败: {e}")
    
    return None

# 下载PDF
def download_pdf(pdf_url, doi, save_dir="downloads"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    filename = os.path.join(save_dir, f"{doi.replace('/', '_')}.pdf")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    try:
        with requests.get(pdf_url, headers=headers, stream=True, timeout=15) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ 成功下载: {filename}")
    except requests.RequestException as e:
        print(f"❌ 下载 {doi} 失败: {e}")

# 批量下载文献
def batch_download(file_path):
    dois = read_doi_list(file_path)
    
    for doi in dois:
        print(f"🔍 处理 DOI: {doi}")
        pdf_url = get_pdf_url(doi)
        print(f"🔗 PDF链接: {pdf_url}")

        if pdf_url:
            download_pdf(pdf_url, doi)
        else:
            print(f"⚠️ 无法获取 {doi} 的PDF链接")
        
        time.sleep(3)  # 避免请求过快被封

if __name__ == "__main__":
    batch_download("test.txt")
