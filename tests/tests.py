from ddgs import DDGS

text = DDGS().text("semen", safesearch="off")

for i, result in enumerate(text):
    print(f"[{i}] {result["title"]}")
    print(result["href"])
    print()
