import re


def split_words(sentence):
    words = re.findall(r"[\w']+|[\-.,!?;@:/()\]\[{}'\"]", sentence)
    return words


def compute_n_gram(sentences, n):
    # compute n-gram
    n_gram = {}
    for sentence in sentences:
        words = split_words(sentence)
        for i in range(len(words) - n + 1):
            compound_word = " ".join(words[i:i+n])
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


def predict_on_sentence(sentence, n_gram, n_gram_prev, n=2):
    words = split_words(sentence)
    prev_word = " ".join(words[-n+1:]).lower()

    word = predict_next_word(n_gram, n_gram_prev, prev_word)

    return word


def main():
    # read from input.txt
    with open("big_input.txt", "r") as f:
        sentences_en = f.readlines()

    # strip
    sentences_en = [sentence.strip() for sentence in sentences_en]

    # compute bigram, unigram
    tri_gram = compute_n_gram(sentences_en, 3)
    bi_gram = compute_n_gram(sentences_en, 2)

    # compute n-gram probabilities
    tri_gram_probabilities = compute_n_gram_probabilities(tri_gram, bi_gram)

    # test sentence
    sentence = "Arta este"
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word
    word = predict_on_sentence(sentence, tri_gram_probabilities, bi_gram, n=3)
    sentence += " " + word

    print(sentence)


if __name__ == "__main__":
    main()