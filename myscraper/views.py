from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import csv

def home(request):
    scraped_data = []
    url = ""
    
    if request.method == "POST":
        url = request.POST.get("url", "")
        action = request.POST.get("action", "") # बटन चेक करने के लिए
        
        if url:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                
                for link in soup.find_all("a", href=True):
                    text = link.text.strip()
                    href = link["href"]
                    if text and href.startswith("http"):
                        scraped_data.append({"text": text, "url": href})
                        
                # 📥 अगर यूजर ने एक्सेल डाउनलोड बटन दबाया है
                if action == "download" and scraped_data:
                    response = HttpResponse(content_type='text/csv; charset=utf-8')
                    response['Content-Disposition'] = 'attachment; filename="scraped_data.csv"'
                    
                    writer = csv.writer(response)
                    writer.writerow(['Text/Title', 'URL Path']) # एक्सेल की हेडिंग
                    for item in scraped_data:
                        writer.writerow([item['text'], item['url']])
                    return response
                    
            except Exception as e:
                scraped_data.append({"text": "Error: Link sahi nahi hai ya website block hai", "url": "#"})

    return render(request, "index.html", {"data": scraped_data, "url": url})