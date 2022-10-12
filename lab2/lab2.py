from google.cloud import translate_v2


def translate_word(word):
    # Use Google API to translate the word from English to French
    # and return the translated word

    # translate the word
    translate_client = translate_v2.Client()
    translation = translate_client.translate(word, target_language="fr")
    word_fr = translation["translatedText"]

    return word_fr


def translate(sentence_en):
    # Use Google API to translate the sentence from English to French
    # and return the translated sentence

    # split the sentence into words
    words = sentence_en.split()

    # translate each word
    words_fr = []
    for word in words:
        words_fr.append(translate_word(word))

    # join the words into a sentence
    sentence_fr = " ".join(words_fr)

    return sentence_fr


def main():
    # Use Google API to translate the sentences from file "input.txt" to French
    # and write the translated sentences to file "output.txt"

    # read sentences from file "input.txt"
    with open("input.txt", "r") as f:
        sentences_en = f.readlines()

    # strip
    sentences_en = [sentence.strip() for sentence in sentences_en]

    # Use Google API to translate the sentences from file "input.txt" to French
    # and write the translated sentences to file "output.txt"
    with open("output.txt", "w") as f:
        for sentence_en in sentences_en:
            f.write(translate(sentence_en))


if __name__ == "__main__":
    main()