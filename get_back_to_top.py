with open("Verticals/ridesDAO/RidesVertical_Complete_Spec.html", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "back-to-top" in line:
        print(f"{i}: {line.strip()}")
