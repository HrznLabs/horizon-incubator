import re
import hashlib
import base64

with open('Verticals/ridesDAO/RidesVertical_Complete_Spec.html', 'r') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
print("Found scripts:", len(scripts))

for i, script in enumerate(scripts):
    if not script.strip():
        print(f"Script {i}: Empty (likely src attribute)")
        continue
    digest = hashlib.sha256(script.encode('utf-8')).digest()
    b64 = base64.b64encode(digest).decode('utf-8')
    print(f"Script {i}:\n{script[:100]}...\nHash: 'sha256-{b64}'\n")

print("CSP Meta Tag:")
csp = re.search(r'<meta http-equiv="Content-Security-Policy" content="(.*?)">', content)
if csp:
    print(csp.group(1))
