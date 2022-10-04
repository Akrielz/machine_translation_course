"""
The code is split into 3 parts:
    1. The function that read the lexicon from the file "lexicon.txt"
    2. The function that determine the part of speach of a word based on the lexicon
    3. The function that translates a sentence from English to French based on the lexicon and the rules from "rules.txt"

The function that read the lexicon from the file "lexicon.txt" is called "read_lexicon".
It returns 3 things:
    1. A dictionary that maps from a part of speach to a dictionary that maps from a word to a translation
    2. A dictionary that maps from a part of speach to a dictionary that maps from a translation to a word
    3. A list with all the parts of speach

The function that determine the part of speach of a word based on the lexicon is called "determine_part_of_speach".
It returns a list with all the parts of speach of the given word.

The function that translates a sentence from English to French based on the lexicon and the rules from "rules.txt" is called "translate_sentence".
Each rule is implemented manually.
It returns the translated sentence.

The main function is called "main".
It reads the sentences from the file "input.txt" and translates them from English to French.
It prints the original sentence and the translated sentence.
"""

import re


def read_lexicon():
    # read lexicon from file "lexicon.txt"
    with open("lexicon.txt", "r") as f:
        lexicon = f.readlines()

    # eliminate the first line
    lexicon = lexicon[1:]

    # read the lexicon into a dictionary
    en_to_fr = {}
    fr_to_en = {}
    read_rule = False

    all_parts_of_speach = set()

    for line in lexicon:
        line = line.strip()

        # if the line is empty, skip it
        if len(line) < 2:
            read_rule = True
            continue

        words = line.split(" ")

        if read_rule:
            read_rule = False
            part_of_speach = words[:-2]
            part_of_speach = " ".join(part_of_speach)

            all_parts_of_speach.add(part_of_speach)
            for word in words[:-2]:
                if word.isupper():
                    all_parts_of_speach.add(part_of_speach)

            en_to_fr[part_of_speach] = {}
            fr_to_en[part_of_speach] = {}
        else:
            arrow_index = words.index("->")
            english_word = " ".join(words[:arrow_index]).lower()
            french_word = " ".join(words[arrow_index + 1:]).lower()
            en_to_fr[part_of_speach][english_word] = french_word
            fr_to_en[part_of_speach][french_word] = english_word

    return en_to_fr, fr_to_en, all_parts_of_speach


def determine_part_of_speach(word, lang_dict):
    parts_of_speach = [part_of_speach for part_of_speach in lang_dict if word.lower() in lang_dict[part_of_speach]]

    additional_parts_of_speach = []
    for part_of_speach in parts_of_speach:
        words = part_of_speach.split()

        if words[0] == "PNOUN":
            additional_parts_of_speach.append("N")

        if len(words) == 1:
            continue

        for word in words:
            # if the whole word is written with capital letters
            if word.isupper():
                additional_parts_of_speach.append(words[-1])

    parts_of_speach.extend(additional_parts_of_speach)
    # remove duplicates but keep order
    parts_of_speach = list(dict.fromkeys(parts_of_speach))

    return parts_of_speach


def translate_sentence(sentence: str, en_to_fr: dict):
    """
    Considering the following rules:

    Rewritting rules
    <ADJ>   + <N>  ->     <N>   + <ADJ>

    POS identification rules
    The + <Masc N> -> Le + <Masc N>
    The + <Fem N> -> La + <Fem N>
    A + <Masc N> -> Un + <Masc N>
    A + <Fem N> -> Une + <Fem N>
    <DET> + saw -> <DET> + Fem N
    saw + <DET> -> V + <DET>
    <DET> + cane -> <DET> + Fem N
    <N> + cane -> <N> + <ADJ>

    Translate the given sentence from English to French
    In diamond brackets are the parts of speech
    """
    sentence = sentence.strip()

    # split the sentence into words considering punctuation words too
    words = re.findall(r"[\w']+|[.,!?;]", sentence)

    # eliminate the words that are empty
    words = [word.lower() for word in words if len(word) > 0]

    # determine the part of speach of each word
    parts_of_speach = [determine_part_of_speach(word, en_to_fr) for word in words]

    # a list with bools that indicate if the word has been translated
    translated = [False for _ in words]
    to_capitalize = [False for _ in words]
    to_capitalize[0] = True

    # mark to capitalize true for every word that is a PNOUN
    for i, part_of_speach in enumerate(parts_of_speach):
        if "PNOUN" in part_of_speach:
            to_capitalize[i] = True

    # apply rewriting rules
    just_rewrote = False
    for i in range(len(words) - 1):
        if just_rewrote:
            just_rewrote = False
            continue

        part_of_speach_1 = parts_of_speach[i]
        part_of_speach_2 = parts_of_speach[i + 1]

        if "ADJ" in part_of_speach_1 and "N" in part_of_speach_2:
            words[i], words[i + 1] = words[i + 1], words[i]
            parts_of_speach[i], parts_of_speach[i + 1] = parts_of_speach[i + 1], parts_of_speach[i]
            just_rewrote = True

    # apply pos rules
    for i in range(len(words) - 1):
        word_1 = words[i]
        word_2 = words[i + 1]

        part_of_speach_1 = parts_of_speach[i]
        part_of_speach_2 = parts_of_speach[i + 1]

        if word_1 == "the" and "N" in part_of_speach_2:
            if "Masc N" in part_of_speach_2:
                words[i] = "le"
                translated[i] = True
            elif "Fem N" in part_of_speach_2:
                words[i] = "la"
                translated[i] = True

        if word_1 == "a" and "N" in part_of_speach_2:
            if "Masc N" in part_of_speach_2:
                words[i] = "un"
                translated[i] = True
            elif "Fem N" in part_of_speach_2:
                words[i] = "une"
                translated[i] = True

        if "DET" in part_of_speach_1 and word_2 == "saw":
            words[i + 1] = en_to_fr["Fem N"]["saw"]
            translated[i + 1] = True

        if word_1 == "saw" and "DET" in part_of_speach_2:
            words[i] = en_to_fr["V"]["saw"]
            translated[i] = True

        if "DET" in part_of_speach_1 and word_2 == "cane":
            words[i + 1] = en_to_fr["Fem N"]["cane"]
            translated[i + 1] = True

        if "N" in part_of_speach_1 and word_2 == "cane":
            words[i + 1] = en_to_fr["ADJ"]["cane"]
            translated[i + 1] = True

    # translate the words that have not been translated
    for i in range(len(words)):
        if translated[i]:
            continue

        word = words[i]
        part_of_speach = parts_of_speach[i]

        for part in part_of_speach:
            try:
                words[i] = en_to_fr[part][word]
                break
            except KeyError:
                continue

    # capitalize the words that have to be capitalized
    for i in range(len(words)):
        if to_capitalize[i]:
            words[i] = words[i].capitalize()

    # translate the sentence
    translated_sentence = " ".join(words)

    # Remove the space before the punctuation
    translated_sentence = re.sub(r" ([.,!?;])", r"\1", translated_sentence)

    return translated_sentence


def main():
    # read sentences from file "input.txt"
    with open("input.txt", "r") as f:
        sentences_en = f.readlines()

    # strip
    sentences_en = [sentence.strip() for sentence in sentences_en]

    en_to_fr, fr_to_en, all_parts_of_speach = read_lexicon()

    # Apply the rules from "rules.txt" to the sentences in order to translate them from English to French
    for sentence_en in sentences_en:
        print(sentence_en)
        sentence_fr = translate_sentence(sentence_en, en_to_fr)
        print(sentence_fr + "\n")


if __name__ == "__main__":
    main()
