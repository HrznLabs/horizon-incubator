import re

with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "r") as f:
    html = f.read()

# Replace toc a styles
old_toc_a = """        .toc a { color: #00ff88; text-decoration: none; transition: color 0.2s ease; border-radius: 4px; }
        .toc a:hover { color: #00d9ff; }"""

new_toc_a = """        .toc a {
            color: #00ff88;
            text-decoration: none;
            transition: all 0.2s ease;
            border-radius: 4px;
            padding: 4px 8px;
            margin-left: -8px;
            display: inline-block;
        }
        .toc a:hover {
            color: #00d9ff;
            background: rgba(0, 217, 255, 0.1);
            text-decoration: underline;
            text-underline-offset: 4px;
        }"""

html = html.replace(old_toc_a, new_toc_a)

with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "w") as f:
    f.write(html)
