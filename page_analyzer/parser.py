import requests
from bs4 import BeautifulSoup


def parse_url(url):
    """Парсинг URL и возврат статуса, h1, title, description."""
    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code
        
        if status_code < 400:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            h1_tag = soup.find('h1')
            h1_content = h1_tag.get_text(strip=True) if h1_tag else None
            
            title_tag = soup.find('title')
            title_content = (
                title_tag.get_text(strip=True) if title_tag else None
            )

            meta_desc = soup.find('meta', attrs={'name': 'description'})
            desc_content = meta_desc.get('content', None) if meta_desc else None
            
            return status_code, h1_content, title_content, desc_content
        else:
            return status_code, None, None, None
    except requests.RequestException:
        return None, None, None, None 