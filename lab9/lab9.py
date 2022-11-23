import re

from transformers import pipeline


def split_words(sentence):
    words = re.findall(r"[\w']+|[\-.,!?;@:/()\]\[{}'\"]", sentence)
    return words


def compute_n_gram(sentences, n):
    # compute n-gram
    n_gram = {}
    for sentence in sentences:
        words = sentence
        for i in range(len(words) - n + 1):
            compound_word = " ".join(words[i:i + n])
            compound_word = compound_word.lower()

            n_gram[compound_word] = n_gram.get(compound_word, 0) + 1

    return n_gram


def compute_n_gram_probabilities(n_gram, n_gram_prev):
    n_gram_probabilities = {}
    for word, count_cur in n_gram.items():
        words = word.split()
        prev_word = " ".join(words[:-1])

        count_prev = n_gram_prev.get(prev_word, 0) + len(n_gram_prev)

        n_gram_probabilities[word] = (count_cur + 1) / count_prev

    return n_gram_probabilities


def predict_next_word(n_gram_probabilities, n_gram_prev, prev_word):
    max_prob = 0
    max_word = None

    for word, prob in n_gram_probabilities.items():
        if not word.startswith(prev_word):
            continue

        if prob > max_prob:
            max_prob = prob
            max_word = word.split()[-1]

    if max_word is None:
        # choose the most common word
        max_count = 0
        for word, count in n_gram_prev.items():
            if count > max_count:
                max_count = count
                max_word = word.split()[-1]

    return max_word


def tag_pos(sentences, pipe):
    output = pipe(sentences)

    pos = []
    words = []
    for sentence in output:
        pos.append([token["entity_group"] for token in sentence])
        words.append([token["word"] for token in sentence])

    return pos, words


def predict_on_sentence(sentence, n_gram, n_gram_prev, pipe, n=2):
    pos, _ = tag_pos([sentence], pipe)
    prev_pos = " ".join(pos[0][-n + 1:]).lower()

    next_pos = predict_next_word(n_gram, n_gram_prev, prev_pos)

    return next_pos, pos[0]


def main():
    # read from input.txt
    with open("input.txt", "r") as f:
        sentences_ro = f.readlines()

    # strip
    sentences_ro = [sentence.strip() for sentence in sentences_ro]

    pipe = pipeline("token-classification", "wietsedv/xlm-roberta-base-ft-udpos28-ro", aggregation_strategy="first")
    pos, words = tag_pos(sentences_ro, pipe)

    tri_gram = compute_n_gram(pos, 3)
    bi_gram = compute_n_gram(pos, 2)

    # compute n-gram probabilities
    tri_gram_probabilities = compute_n_gram_probabilities(tri_gram, bi_gram)

    # predict
    sentence = "Maria sare in"
    next_pos, pos = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, pipe, n=3)

    print(pos + [next_pos])


if __name__ == "__main__":
    main()
