import json, os

tweets_file  = "/Users/hayleyso/Desktop/HLTH 453/tweets_100.jsonl"   # your collected tweets (1 tweet per line, JSON)
tweets_txt   = "/Users/hayleyso/Desktop/HLTH 453/tweets.txt"     # required output: tweet text per line
labels_txt   = "/Users/hayleyso/Desktop/HLTH 453/labels.txt"     # required output: matching label per line

# Load all tweet objects
with open(tweets_file, "r", encoding="utf-8") as f:
    tweets = [json.loads(line) for line in f]

# Load what we have already labeled (if files exist)
labeled_texts, labeled_labels = [], []
if os.path.exists(tweets_txt) and os.path.exists(labels_txt):
    with open(tweets_txt, "r", encoding="utf-8") as ft, \
         open(labels_txt, "r", encoding="utf-8") as fl:
        labeled_texts = [line.rstrip("\n") for line in ft]
        labeled_labels = [line.rstrip("\n") for line in fl]

print(f"Already labeled {len(labeled_labels)} tweets. Resuming...\n")

with open(tweets_txt, "a", encoding="utf-8") as ft, \
     open(labels_txt, "a", encoding="utf-8") as fl:
    for i, t in enumerate(tweets, 1):
        text = t["text"].replace("\n", " ")
        if i <= len(labeled_labels):
            # Skip already-labeled tweets
            continue

        print(f"\nTweet {i}/{len(tweets)}\n{'-'*60}\n{text}\n{'-'*60}")
        while True:
            c = input("[p]ositive / [n]egative / [q]uit: ").strip().lower()
            if c in ("p", "n", "q"):
                break
            print("Please enter p, n, or q.")

        if c == "q":
            break
        label = "positive" if c == "p" else "negative"
        ft.write(text + "\n")
        fl.write(label + "\n")
        ft.flush()
        fl.flush()

print("\nProgress saved. You can run this script again to continue.")