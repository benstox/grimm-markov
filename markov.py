#!/usr/bin/env python3
import json

from collections import defaultdict

with open("german_text.txt", "r") as f:
    all_text = f.read()

sentences = all_text.split(".")
sentences = [sentence.strip() for sentence in sentences]

# word Markov
order = 3
initials = []
finals = []
sequences = defaultdict(list)
for sentence in sentences:
    words = sentence.split()
    if len(words) < order:
        continue
    initials.append(" ".join(words[:order - 1]))
    finals.append(words[-1])
    num_words = len(words)
    for i in range(num_words - (order - 1)):
        order_words = words[i:i + order]
        key_words = order_words[:order - 1]
        next_word = order_words[-1]
        sequences[" ".join(key_words)].append(next_word)

word_markov_data = {
    "order": order,
    "initials": initials,
    "finals": list(set(finals)),
    "sequences": sequences,
}

with open("german_word_markov.json", "w") as f:
    json.dump(word_markov_data, f)
