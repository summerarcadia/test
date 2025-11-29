import json
# Input and output files
tweets_file = "/Users/hayleyso/Desktop/HLTH 453/tweets_100.jsonl"
labels_file = "/Users/hayleyso/Desktop/HLTH 453/output_path.txt"

with open(tweets_file, "r", encoding="utf-8") as f:
    tweets = [json.loads(line)["text"] for line in f]

labels = []
print("Press p for positive, n for negative. Press q to quit and save.\n")

for i, text in enumerate(tweets, 1):
    print(f"\nTweet {i}/{len(tweets)}:")
    print("-" * 60)
    print(text.replace("\n", " "))
    print("-" * 60)

    while True:
        choice = input("[p]ositive / [n]egative / [q]uit: ").strip().lower()
        if choice in ("p", "n", "q"):
            break
        else:
            print("Please enter p, n, or q.")

    if choice == "q":
        break
    labels.append("positive" if choice == "p" else "negative")

# Save labels collected so far
with open(labels_file, "w", encoding="utf-8") as out:
    out.write("\n".join(labels))

print(f"\nSaved {len(labels)} labels to {labels_file}")