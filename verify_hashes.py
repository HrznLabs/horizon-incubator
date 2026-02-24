import re
import hashlib
import base64
import requests

def calculate_sha256(content):
    return base64.b64encode(hashlib.sha256(content.encode('utf-8')).digest()).decode('utf-8')

def get_sri_hash(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return "sha384-" + base64.b64encode(hashlib.sha384(response.content).digest()).decode('utf-8')

with open('Verticals/ridesDAO/RidesVertical_Complete_Spec.html', 'r') as f:
    html_content = f.read()

# Extract script contents
# This regex is a bit simplistic, it assumes script tags don't have attributes other than what we see
# We need to be careful to capture the content exactly as it is in the file
script_pattern = re.compile(r'<script(?:[^>]*)>(.*?)</script>', re.DOTALL)
scripts = script_pattern.findall(html_content)

# Filter out the empty script tag or the src script tag
# The first script tag has a src attribute, so the content is empty in the regex match if it's self-closing or empty
# Wait, the src script tag: <script src="..." ...></script> matches empty string.
# We need to filter those out.
inline_scripts = [s for s in scripts if s.strip()]

print(f"Found {len(inline_scripts)} inline scripts.")

calculated_hashes = []
for i, script_content in enumerate(inline_scripts):
    # browsers calculate hash on the content between <script> and </script>
    # including newlines and indentation.
    # The regex capture group (.*?) should capture it exactly.

    # However, I need to make sure I'm not capturing the one with src attribute if it has no content.
    # In the file:
    # <script src="..." ...></script> -> content is empty string.
    # <script>...</script> -> content is the code.

    # Let's verify what we captured.
    # print(f"--- Script {i} ---")
    # print(script_content)
    # print("----------------")

    sha256_hash = calculate_sha256(script_content)
    calculated_hashes.append(sha256_hash)
    print(f"Script {i} hash: sha256-{sha256_hash}")

# Check SRI
mermaid_url = "https://cdn.jsdelivr.net/npm/mermaid@11.12.2/dist/mermaid.min.js"
print(f"Calculating SRI for {mermaid_url}...")
sri_hash = get_sri_hash(mermaid_url)
print(f"SRI hash: {sri_hash}")
