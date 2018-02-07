#!/usr/bin/env python3
import json
import random

with open("german_word_markov.json", "r") as f:
    markov_data = json.load(f)

order = markov_data["order"]
initials = markov_data["initials"]
finals = markov_data["finals"]
sequences = markov_data["sequences"]


def generate_sentence(min_num_words=5):
    initial = random.choice(initials)
    sentence = [initial]
    while sentence[-1] not in finals or len(sentence) < min_num_words:
        print(len(sentence))
        try:
            sentence += random.choice(sequences[sentence[-1]])
        except KeyError:
            sentence[-1] += "."
            sentence.append(random.choice(initials))

    sentence[-1] += "."
    sentence = " ".join(sentence)
    return(sentence)

