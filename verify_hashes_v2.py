import re
import hashlib
import base64

def calculate_sha256(content):
    # Hash the raw bytes
    return base64.b64encode(hashlib.sha256(content.encode('utf-8')).digest()).decode('utf-8')

with open('Verticals/ridesDAO/RidesVertical_Complete_Spec.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Improved regex to only match <script> tags without src attribute
# Or, more robustly, match all <script> tags and check if they have src
script_tag_pattern = re.compile(r'<script([^>]*)>(.*?)</script>', re.DOTALL)
matches = script_tag_pattern.findall(html_content)

print(f"Total script tags found: {len(matches)}")

inline_scripts = []
for attrs, content in matches:
    if 'src=' not in attrs and content.strip():
        inline_scripts.append(content)

print(f"Found {len(inline_scripts)} inline scripts.")

for i, script_content in enumerate(inline_scripts):
    sha256_hash = calculate_sha256(script_content)
    print(f"Script {i+1} hash: sha256-{sha256_hash}")
