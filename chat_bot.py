import timer
from utils import transform_answer_according_to_keyword

import random
import re
import json


reflection_personal_pronouns = {"i": "you", "he": "he", "she": "she", "it": "it", "we": "you",
                                "they": "they", "you": "I", "me": "you", "him": "him",
                                "her": "her", "us": "you", "my": "your", "myself": "yourself", "yourself": "myself"}
supporting_verbs_from_positive_to_negative = \
    {"is": "isn't", "are": "aren't", "am": "am not", "was": "wasn't", "were": "weren't", "has": "hasn't",
    "have": "haven't", "had": "hadn't", "will": "won't", "do": "don't", "yes": "no", "can": "can't", "could": "couldn't"}

supporting_verbs_from_negative_to_positive = {val: key for key, val in supporting_verbs_from_positive_to_negative.items()}
supporting_verbs_from_negative_to_positive.update({"not": "", "never": "always"})
with open(".\\keywords_to_answers.json", "r") as f:
    keywords_to_answers = json.load(f)

# keywords_to_answers = {re.compile(keyword.lower()): answers for keyword, answers in keywords_to_answers}
keywords_to_answers = {keyword.lower(): answers for keyword, answers in keywords_to_answers}
pattern_punctuation = re.compile(r'[ ,.?!]+')


def conversation():
    timer.start()
    print("Argument Clinic: You have 5 minutes to argue")

    while not timer.stop():
        user_sentence = input("You: ")
        results = keywords(user_sentence)
        results *= 10
        result_logic = logic(user_sentence)
        for rl in result_logic:
            if rl.lower() != user_sentence.lower():
                results.append(rl)
        if results:
            print("Argument Clinic:", random.choice(results))
        else:
            print("Argument Clinic:", random.choice(["No Comment!", "Can't you use your time in a better way?"]))


def keywords(sentence):
    rets = []
    for keyword_regex, answers in keywords_to_answers.items():
        if re.search(keyword_regex, sentence.lower()):
            for answer in answers:
                answer = transform_answer_according_to_keyword(keyword_regex, sentence, answer)
                rets.append(answer)

    return rets


def logic(sentence):
    f_changed, new_sentence = sentence_change_sign(sentence)
    if not f_changed:
        f_changed, new_sentence = sentence_change_sign(sentence, "positive_to_negative")
        if not f_changed:
            new_sentence = add_negative_word(new_sentence)

    new_sentence = reflect(new_sentence)
    new_sentence = new_sentence.replace("I aren't", "I am not")
    new_sentence = new_sentence.replace("aren't I", "isn't I")
    new_sentence = new_sentence.replace("I are", "I am")
    new_sentence = new_sentence.replace("are I", "am I")
    new_sentence = new_sentence.replace("you am not", "you aren't")
    new_sentence = new_sentence.replace("you am", "you are")
    new_sentence = new_sentence.replace("am not you", "aren't you")
    new_sentence = new_sentence.replace("am you", "are you")
    new_sentence = re.sub(" I([ ,.?!]*)$", r" me\1", new_sentence)

    new_sentence = new_sentence[0].upper() + new_sentence[1:]

    if new_sentence[-1] == '?':
        new_sentence2 = "I think you are asking the wrong question. The right one is: " + new_sentence
        return [new_sentence] * 5 + [new_sentence2]
    else:
        return [new_sentence]


def add_negative_word(sentence):
    words = sentence.strip().split()

    additional_word = None
    words_without_punctuation = pattern_punctuation.split(sentence.strip())
    for idx, (word, word_without_punctuation) in enumerate(zip(words, words_without_punctuation)):
        if word_without_punctuation.lower() in reflection_personal_pronouns:
            if word_without_punctuation.lower() in {"he", "she", "it"}:
                additional_word = "doesn't"
            else:
                additional_word = "don't"
            break

    if additional_word:
        return " ".join(words[:idx + 1] + [additional_word] + words[idx + 1:])
    else:
        return " ".join(words)


def sentence_change_sign(sentence, sign: str = "negative_to_positive"):
    # Split the sentence into words
    words = sentence.strip().split()
    words = [word for word in words if re.match(r"\w+", word)]
    words_without_punctuation = pattern_punctuation.split(sentence.strip())

    # List of words that, when found, should be negated
    # Initialize the negated sentence
    changed_sentence = []

    if sign == "negative_to_positive":
        change_supporting_verbs_according_to_sign = supporting_verbs_from_negative_to_positive
    elif sign == "positive_to_negative":
        change_supporting_verbs_according_to_sign = supporting_verbs_from_positive_to_negative

    # Iterate through the words
    f_changed = False
    for word, word_without_punctuation in zip(words, words_without_punctuation):
        # Check if the word is in the list of negatable words
        # if not f_changed and word_without_punctuation.lower() in change_supporting_verbs_according_to_sign:
        if word_without_punctuation.lower() in change_supporting_verbs_according_to_sign:
            # Negate the word
            sign_word = change_supporting_verbs_according_to_sign[word_without_punctuation.lower()]
            # if word_without_punctuation.lower() != 'no' and word_without_punctuation.lower() != 'yes':
            f_changed = True
        else:
            # Keep the word as is
            sign_word = word_without_punctuation

        sign_word += word[len(word_without_punctuation):]

        # Add the negated word to the negated sentence
        if sign_word:
            changed_sentence.append(sign_word)

    # Join the words back into a sentence
    return f_changed, " ".join(changed_sentence)


def reflect(sentence):
    # Split the sentence into words
    words = sentence.strip().split()

    # List of words that, when found, should be negated

    # Initialize the negated sentence
    reflected_sentence = []

    # Iterate through the words
    words_without_punctuation = pattern_punctuation.split(sentence.strip())
    for word, word_without_punctuation in zip(words, words_without_punctuation):
        # Check if the word is in the list of negatable words
        if word_without_punctuation.lower() in reflection_personal_pronouns:
            # Negate the word
            reflected_word = reflection_personal_pronouns[word_without_punctuation.lower()]
        else:
            # Keep the word as is
            reflected_word = word_without_punctuation

        reflected_word += word[len(word_without_punctuation):]

        # Add the negated word to the negated sentence
        reflected_sentence.append(reflected_word)

    # Join the words back into a sentence
    return " ".join(reflected_sentence)


conversation()
