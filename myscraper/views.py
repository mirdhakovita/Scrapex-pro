from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def home(request):
    scraped_data = []
    url = ""
    
    if request.method == "POST":
        url = request.POST.get("url", "")
        if url:
            try:
                # वेबसाइट से डेटा खींचने का इंजन
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                
                # वेबसाइट के सभी लिंक्स (Links) और टेक्स्ट निकालना
                for link in soup.find_all("a", href=True):
                    text = link.text.strip()
                    href = link["href"]
                    if text and href.startswith("http"):
                        scraped_data.append({"text": text, "url": href})
            except Exception as e:
                scraped_data.append({"text": "Error: Link sahi nahi hai ya website block hai", "url": "#"})

    return render(request, "index.html", {"data": scraped_data, "url": url})