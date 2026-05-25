import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# LNMU की वेबसाइट का मुख्य यूआरएल
URL = "https://www.lnmu.ac.in/"

def scrape_university_notices():
    try:
        # वेबसाइट से डेटा मंगाना
        response = requests.get(URL, timeout=15)
        if response.status_code != 200:
            print("वेबसाइट लोड नहीं हो पाई।")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # नए नोटिस स्टोर करने के लिए लिस्ट
        live_updates = []
        
        # वेबसाइट के लिंक्स और एंकर टैग्स को खंगालना
        links = soup.find_all('a')
        
        id_counter = 1
        for link in links:
            text = link.get_text().strip()
            href = link.get('href')
            
            if text and href:
                # केवल सेमेस्टर 1 से 8 और यूजी (ग्रेजुएशन) से जुड़े जरूरी कीवर्ड्स को खोजना
                keywords = ["semester", "ug", "part", "examination", "admission", "result", "b.a", "b.sc", "b.com"]
                if any(key in text.lower() for key in keywords):
                    
                    # कैटेगरी तय करना
                    category = "general"
                    if "admis" in text.lower() or "नामांकन" in text:
                        category = "admission"
                    elif "exam" in text.lower() or "परीक्षा" in text:
                        category = "exam"
                    elif "resul" in text.lower() or "परिणाम" in text:
                        category = "result"
                        
                    # लिंक को पूरा करना अगर वह अधूरा हो
                    if href.startswith('/'):
                        href = URL + href
                        
                    live_updates.append({
                        "id": id_counter,
                        "title": text,
                        "category": category,
                        "date": datetime.now().strftime("%d %b %Y"),
                        "link": href
                    })
                    id_counter += 1
                    
                    # टॉप 5 जरूरी नोटिस ही रखना ताकि ऐप भारी न हो
                    if id_counter > 5:
                        break
                        
        # अगर कोई लाइव नोटिस नहीं मिला तो पुराना सुरक्षित रखना
        if not live_updates:
            print("कोई नया नोटिस नहीं मिला।")
            return

        # डेटा को JSON फॉर्मेट में तैयार करना
        output_data = {
            "semester_updates": live_updates,
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        
        # notices.json फ़ाइल में डेटा राइट करना
        with open('notices.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print("सफलतापूर्वक डेटा अपडेट हो गया है भाई!")

    except Exception as e:
        print(f"त्रुटि आई: {e}")

if __name__ == "__main__":
    scrape_university_notices()
