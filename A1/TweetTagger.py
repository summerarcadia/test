import json
import random

class TweetTagger:
    def __init__(self):
        # initialize empty lists
        self.tweets = []
        self.labels = []

    def load(self, tweets_filename, labels_filename=None):
        """Load tweets (one JSON tweet per line) and optional labels (one label per line).
        If labels_filename is None, create empty labels for each tweet.
        """
        self.tweets = []
        self.labels = []

        # load tweets: each line is a JSON string for one tweet
        with open(tweets_filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                tweet = json.loads(line)
                self.tweets.append(tweet)

        # load labels if provided
        if labels_filename:
            labels = []
            with open(labels_filename, "r", encoding="utf-8") as g:
                for line in g:
                    labels.append(line.strip())
            # adjust label count to match tweets
            if len(labels) < len(self.tweets):
                labels.extend([""] * (len(self.tweets) - len(labels)))
            elif len(labels) > len(self.tweets):
                labels = labels[:len(self.tweets)]
            self.labels = labels
        else:
            # no labels file → give each tweet an empty label
            self.labels = ["" for _ in self.tweets]

    def save(self, filename):
        """Save tweets to 'tweets_' + filename and labels to 'labels_' + filename."""
        tweets_out = "tweets_" + filename
        labels_out = "labels_" + filename

        with open(tweets_out, "w", encoding="utf-8") as tf:
            for tweet in self.tweets:
                tf.write(json.dumps(tweet) + "\n")

        with open(labels_out, "w", encoding="utf-8") as lf:
            for label in self.labels:
                lf.write(label + "\n")

    def label_tweets(self):
        """Interactively label each tweet by showing its text and reading user input."""
        if len(self.labels) != len(self.tweets):
            self.labels = ["" for _ in self.tweets]

        for i, tweet in enumerate(self.tweets):
            text = tweet.get("text", "")
            print(f"\nTweet {i+1}/{len(self.tweets)}:")
            print(text)
            label = input("Enter label for this tweet (press Enter to keep current): ").rstrip("\n")
            if label != "":
                self.labels[i] = label

    def count(self, label):
        """Return number of tweets labeled exactly as `label`."""
        return sum(1 for lab in self.labels if lab == label)

    def merge(self, another_tweet_tagger):
        """Merge another TweetTagger into this one."""
        if not isinstance(another_tweet_tagger, TweetTagger):
            raise TypeError("merge expects another TweetTagger object")
        self.tweets.extend(another_tweet_tagger.tweets)
        self.labels.extend(another_tweet_tagger.labels)

    def trim(self, label, count):
        """Remove non-English tweets, then keep at most `count` tweets with the given label."""
        # Phase 1: filter out non-English tweets
        filtered_tweets = []
        filtered_labels = []
        for tweet, lab in zip(self.tweets, self.labels):
            if tweet.get("lang") == "en":
                filtered_tweets.append(tweet)
                filtered_labels.append(lab)
        self.tweets = filtered_tweets
        self.labels = filtered_labels

        # Phase 2: reduce tweets with the target label if too many
        indices_with_label = [i for i, lab in enumerate(self.labels) if lab == label]
        if len(indices_with_label) <= count:
            return

        keep_indices = set(random.sample(indices_with_label, count))

        new_tweets = []
        new_labels = []
        for i, (tweet, lab) in enumerate(zip(self.tweets, self.labels)):
            if lab == label:
                if i in keep_indices:
                    new_tweets.append(tweet)
                    new_labels.append(lab)
                # else drop it
            else:
                new_tweets.append(tweet)
                new_labels.append(lab)

        self.tweets = new_tweets
        self.labels = new_labels


# --- Example usage and tests ---

if __name__ == "__main__":
    # Your files
    tweets_file = "tweets_fourtweets.txt"
    labels_file = "labels_fourtweets.txt"
    example_file = "example_tweet.json"

    # Test 1: load four tweets with labels
    tt1 = TweetTagger()
    tt1.load(tweets_file, labels_file)
    print("Count 'pos':", tt1.count("pos"))  # expect 2
    print("Count 'neg':", tt1.count("neg"))  # expect 2

    # Test 2: load single example tweet (no labels file)
    tt2 = TweetTagger()
    tt2.load(example_file)
    print("Loaded 1 tweet. Text:", tt2.tweets[0]["text"])
    print("Label:", repr(tt2.labels[0]))  # expect ""

    
