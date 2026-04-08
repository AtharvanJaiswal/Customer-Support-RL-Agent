import json

with open("grpo_dataset.json") as f:
    data = json.load(f)

clean = []

for d in data:
    r = d["response"].lower()

    if (
        len(r) > 20
        and "http" not in r
        and "www" not in r
        and "donate" not in r
        and "please help please help" not in r
    ):
        clean.append(d)

with open("clean_dataset.json", "w") as f:
    json.dump(clean, f, indent=2)

print("Clean samples:", len(clean))