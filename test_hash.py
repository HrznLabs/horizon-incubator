from bs4 import BeautifulSoup
import hashlib
import base64

with open('Verticals/ridesDAO/RidesVertical_Complete_Spec.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

hashes = []
for script in scripts:
    if script.string:
        content = script.string
        hash_val = base64.b64encode(hashlib.sha256(content.encode('utf-8')).digest()).decode('utf-8')
        hashes.append(f"'sha256-{hash_val}'")

print("Hashes from bs4: ", " ".join(hashes))
