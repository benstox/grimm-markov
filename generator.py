#!/usr/bin/env python3
import json
import random
import re

with open("german_word_markov.json", "r") as f:
    markov_data = json.load(f)

order = markov_data["order"]
initials = markov_data["initials"]
finals = markov_data["finals"]
sequences = markov_data["sequences"]

print(f"Order {order}")


def generate_sentence(min_num_words=7):
    initial = random.choice(initials)
    sentence = initial.split()
    while sentence[-1] not in finals or len(sentence) < min_num_words:
        print(len(sentence))
        try:
            key_words = sentence[len(sentence) - (order - 1):]
            key_words = " ".join(key_words)
            sentence.append(random.choice(sequences[key_words]))
        except KeyError:
            if re.search(r"[A-Za-z0-9]$", sentence[-1]):
                sentence[-1] += "."
            sentence.append(random.choice(initials))
            sentence += random.choice(initials).split()

    if re.search(r"[A-Za-z0-9]$", sentence[-1]):
        sentence[-1] += "."
    sentence = " ".join(sentence)
    return(sentence)


print(generate_sentence())
