import re

with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "r") as f:
    html = f.read()

# I want to fix TOC links click target as previously requested, I'll use regex to make it more robust

pattern = re.compile(r'(\.toc a \{\s*color: #[0-9a-fA-F]+;\s*text-decoration: none;\s*transition:.*?\s*border-radius: 4px;)\s*\}', re.DOTALL)
match = pattern.search(html)

if match:
    replacement = match.group(1) + "\n            padding: 4px 8px;\n            margin-left: -8px;\n            display: inline-block;\n        }"
    html = html.replace(match.group(0), replacement)

    hover_pattern = re.compile(r'(\.toc a:hover \{\s*color: #[0-9a-fA-F]+;)\s*\}', re.DOTALL)
    hover_match = hover_pattern.search(html)
    if hover_match:
        hover_replacement = hover_match.group(1) + "\n            background: rgba(0, 217, 255, 0.1);\n            text-decoration: underline;\n            text-underline-offset: 4px;\n        }"
        html = html.replace(hover_match.group(0), hover_replacement)

    with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "w") as f:
        f.write(html)
    print("TOC styles modified")
else:
    print("Pattern not found or already modified")
