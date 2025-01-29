import requests
import os
from bs4 import BeautifulSoup

def download_paper(doi, output_dir):
    sci_hub_url = f"https://sci-hub.st/{doi}"
    response = requests.get(sci_hub_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        button = soup.find('button', id='download')
        if button:
            pdf_url = button['onclick'].split("'")[1]
            if not pdf_url.startswith('http'):
                pdf_url = 'https:' + pdf_url
            pdf_response = requests.get(pdf_url, stream=True)
            if pdf_response.status_code == 200:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                with open(f"{output_dir}/{doi.replace('/', '_')}.pdf", 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded: {doi}")
            else:
                print(f"Failed to download PDF: {doi}")
        else:
            print(f"Failed to find download button: {doi}")
    else:
        print(f"Failed to access Sci-Hub: {doi}")

def main():
    input_file = "test.txt"
    output_dir = "downloaded_papers"
    
    with open(input_file, 'r', encoding='utf-8') as file:
        dois = file.readlines()
    
    for doi in dois:
        doi = doi.strip()
        if doi:
            download_paper(doi, output_dir)

if __name__ == "__main__":
    main()