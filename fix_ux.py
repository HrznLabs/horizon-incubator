import re

with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "r") as f:
    html = f.read()

# I want to add custom scrollbar styles to the mermaid diagrams because they overflow horizontally

css_to_add = """
        /* 🎨 Palette UX Optimization: Custom scrollbars for overflowing mermaid diagrams */
        .mermaid::-webkit-scrollbar {
            height: 8px;
        }
        .mermaid::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
        }
        .mermaid::-webkit-scrollbar-thumb {
            background: rgba(0, 217, 255, 0.3);
            border-radius: 4px;
        }
        .mermaid::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 217, 255, 0.6);
        }
"""

if css_to_add not in html:
    html = html.replace(".mermaid:focus-visible {", css_to_add + "\n        .mermaid:focus-visible {")

    with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "w") as f:
        f.write(html)
    print("CSS added.")
else:
    print("CSS already exists.")
