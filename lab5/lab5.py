from collections import defaultdict
from pprint import pprint


def ibm_model_1(sentences_en, sentences_du, num_steps=5):
    # extract the words for each sentence
    words_en = [sentence.split() for sentence in sentences_en]
    words_du = [sentence.split() for sentence in sentences_du]

    # add null tokens to each en sentence
    words_du = [[None] + sentence for sentence in words_du]

    # Initialize t(e|f) uniformly
    t = defaultdict(lambda: defaultdict(lambda: 1.0))

    for i in range(num_steps):
        # Initialize count(e|f) and total(f) to 0
        count = defaultdict(lambda: defaultdict(lambda: 0.0))
        total = defaultdict(lambda: 0.0)

        # For each sentence pair (e, f) in the training data
        for sentence_en, sentence_du in zip(words_en, words_du):
            # set total_s = 0 for all words e in the source sentence
            total_s = defaultdict(lambda: 0.0)

            # For each word e in the English sentence
            for e in sentence_en:
                # For each word f in the German sentence
                for f in sentence_du:
                    # total_s[e] += t(e|f)
                    total_s[e] += t[e][f]

            # For each word e in the English sentence
            for e in sentence_en:
                # For each word f in the German sentence
                for f in sentence_du:
                    # Increase count(e|f) by the alignment probability
                    count[e][f] += t[e][f] / total_s[e]

                    # Increase total(f) by the alignment probability
                    total[f] += t[e][f] / total_s[e]

        # For each English word e
        for e in count:
            # For each German word f
            for f in count[e]:
                # Set t(e|f) = count(e|f) / total(f)
                t[e][f] = count[e][f] / total[f]

    # convert to a dict
    t = {word_en: dict(t[word_en]) for word_en in t.keys()}
    return t


def main():
    # read en mini
    with open("en_mini.txt", "r") as f:
        en = f.read().splitlines()

    # read du mini
    with open("du_mini.txt", "r") as f:
        du = f.read().splitlines()

    t = ibm_model_1(en, du, 100)
    pprint(t)


if __name__ == "__main__":
    main()