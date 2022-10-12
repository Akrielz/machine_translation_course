from googletrans import Translator


def translate_text(texts, target_language, source_language, translator):
    # Translate the text to the target language
    translated_texts = translator.translate(texts, dest=target_language, src=source_language).text
    print(translated_texts)
    return translated_texts


def translate_text_chain(texts, languages, translator):
    for i in range(len(languages) - 1):
        texts = translate_text(texts, languages[i + 1], languages[i], translator)
    return texts


def main():
    # Use Google API to translate the sentences from file "input.txt" to French
    # and write the translated sentences to file "output.txt"

    # read sentences from file "input.txt"
    with open("input.txt", "r") as f:
        sentences = f.readlines()

    sentences = [sentence.strip() for sentence in sentences]

    # read the languages from file "langs.txt"
    with open("langs.txt", "r") as f:
        languages = f.readlines()

    languages = [lang.strip() for lang in languages]
    print(languages)

    # Create a translator object
    translator = Translator()

    # Translate the sentences
    translated_sentences = []
    for sentence in sentences:
        print(f"\n{sentence}")
        translated_sentences.append(translate_text_chain(sentence, languages, translator))

    # write the translated sentences to file "output.txt"
    with open("output.txt", "w") as f:
        for sentence in translated_sentences:
            f.write(sentence + "\n")


if __name__ == "__main__":
    main()
