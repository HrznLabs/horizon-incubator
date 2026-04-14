import hashlib
import base64
import re

with open('Verticals/ridesDAO/RidesVertical_Complete_Spec.html', 'r') as f:
    content = f.read()

# Update HTML: insert toast-container
toast_html = '    <!-- 🎨 Palette UX Optimization: Toast notifications container for screen reader and visual feedback -->\n    <div id="toast-container" aria-live="polite" aria-atomic="true" style="position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 10000; display: flex; flex-direction: column; gap: 10px; pointer-events: none;"></div>\n</body>'
content = content.replace('</body>', toast_html)

# Update JS in the 3rd script block
js_search = "            document.body.addEventListener('click', async (e) => {"
js_replace = """            const showToast = (message, isError = false) => {
                const container = document.getElementById('toast-container');
                if (!container) return;

                const toast = document.createElement('div');
                toast.textContent = message;
                toast.style.cssText = `
                    background: ${isError ? '#ff6b6b' : '#00ff88'};
                    color: ${isError ? '#fff' : '#1a1a2e'};
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    opacity: 0;
                    transform: translateY(20px);
                    transition: opacity 0.3s ease, transform 0.3s ease;
                `;
                container.appendChild(toast);

                toast.offsetHeight; // trigger reflow
                toast.style.opacity = '1';
                toast.style.transform = 'translateY(0)';

                setTimeout(() => {
                    toast.style.opacity = '0';
                    toast.style.transform = 'translateY(20px)';
                    setTimeout(() => toast.remove(), 300);
                }, 3000);
            };

            document.body.addEventListener('click', async (e) => {"""
content = content.replace(js_search, js_replace)

js_search2 = """                    btn.setAttribute('aria-label', 'Copied!');

                    setTimeout(() => {"""
js_replace2 = """                    btn.setAttribute('aria-label', 'Copied!');

                    // 🎨 Palette UX Optimization: Show toast notification for better visual and screen reader feedback
                    showToast('✅ Link copied to clipboard');

                    setTimeout(() => {"""
content = content.replace(js_search2, js_replace2)

js_search3 = """                    console.error('Failed to copy link to clipboard.');
                }
            });"""
js_replace3 = """                    console.error('Failed to copy link to clipboard.');
                    showToast('❌ Failed to copy link', true);
                }
            });"""
content = content.replace(js_search3, js_replace3)

# Recalculate CSP hashes
script_pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
scripts = script_pattern.findall(content)

hashes = []
for script in scripts:
    digest = hashlib.sha256(script.encode('utf-8')).digest()
    b64 = base64.b64encode(digest).decode('utf-8')
    hashes.append(f"'sha256-{b64}'")

# Use regex to replace the old script-src hashes
csp_pattern = re.compile(r"script-src ([^;]+);")
def replacer(match):
    original = match.group(1)
    parts = original.split(' ')
    # Keep URLs (like https://cdn...) and replace sha256
    new_parts = []
    for p in parts:
        if p.startswith("'sha256-"):
            continue
        new_parts.append(p)

    # Prepend new hashes
    final_parts = hashes + new_parts
    return "script-src " + " ".join(final_parts) + ";"

content = csp_pattern.sub(replacer, content)

with open('test_output.html', 'w') as f:
    f.write(content)
