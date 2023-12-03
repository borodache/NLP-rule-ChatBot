from utils import transform_answer_according_to_keyword
import timer
from constants import c_write_here, c_minutes_to_measure

import streamlit as st
import random
import re
import json
import pathlib


reflection_personal_pronouns = {"i": "you", "he": "he", "she": "she", "it": "it", "we": "you",
                                "they": "they", "you": "I", "me": "you", "him": "him",
                                "her": "her", "us": "you", "my": "your", "myself": "yourself", "yourself": "myself",
                                "mine": "yours", "yours": "mine"}
supporting_verbs_from_positive_to_negative = \
    {"is": "isn't", "are": "aren't", "am": "am not", "was": "wasn't", "were": "weren't", "has": "hasn't",
     "have": "haven't", "had": "hadn't", "will": "won't", "do": "don't", "yes": "no", "can": "can't",
     "could": "couldn't", "did": "didn't", "should": "shouldn't", "would": "wouldn't"}

supporting_verbs_from_negative_to_positive = {val: key for key, val in supporting_verbs_from_positive_to_negative.items()}
supporting_verbs_from_negative_to_positive.update({"not": ""})

keywords_to_answers_file = pathlib.Path("./keywords_to_answers.json")
with open(keywords_to_answers_file.joinpath(), "r") as f_keywords_to_answers:
    keywords_to_answers = json.load(f_keywords_to_answers)
keywords_to_answers = {keyword.lower(): answers for keyword, answers in keywords_to_answers}

pattern_punctuation = re.compile(r'[ ,.?!]+')

common_mistakes_correction = {"I aren't": "I am not", "aren't I": "isn't I", "I are": "I am", "are I": "am I",
                              "you am not": "you aren't", "you am": "you are", "am not you": "aren't you",
                              "am you": "are you"}

key_for_streamlit = 0


def conversation():
    """
    This function is actually the main function in this file and in the whole project, it runs the bot and the
    user's talking turns one after another. At first it searchs for a keyword, if it found it will give one of the
    answers from the keywords, otherwise it will use logic (convert negative to positive or the other way around),
    If the conversion don't do anything, it will return one of the default arguments it has.
    :return: No return (void - None)
    """
    # print("Argument Clinic: You have 5 minutes to argue")
    st.write(f"Argument Clinic: You have {c_minutes_to_measure} minutes to argue")
    timer.start()
    global key_for_streamlit
    user_sentence = None

    if timer.stop():
        return
    else:
        if user_sentence is None:
            user_sentence = st.text_input("You: ", placeholder=c_write_here, key=key_for_streamlit)  # , value="", max_chars=None, key="abc", type="default")
        else:
            key_for_streamlit += 1

        if len(user_sentence) > 0:
            results = keywords(user_sentence)

            for idx, result in enumerate(results):
                if re.search("always", result) or re.search("never", result) or re.search("stop", result) \
                        or re.search("start", result) or re.search("love", result) or re.search("hate", result):
                    result = reflect(result)
                    results[idx] = result

            if not results:
                results = logic(user_sentence)

            results_final = []
            for rl in results:
                if rl.strip().lower() != user_sentence.strip().lower():
                    results_final.append(rl)

            if results_final:
                # print("Argument Clinic:", random.choice(results_final))
                st.text(f"Argument Clinic: {random.choice(results_final)}")
            else:
                # print("Argument Clinic:", random.choice(["Haven't I told you before?", "I have already told you once",
                #                                          "Can't you use your time in a better way?"]))
                st.text(f"Argument Clinic: {random.choice(['Have not I told you before?', 'I have already told you once', 'Cannot you use your time in a better way?'])}")

            user_sentence = None


def keywords(sentence):
    """
    find all answers for user's input according to the keywords in the json file.
    for providing an answer it runs the utils.transform_answer_according_to_keyword function in order to substitute
    groups matched in the regex.
    :param sentence: user's input
    :return: a list of possible answers
    """
    rets = []
    for keyword_regex, answers in keywords_to_answers.items():
        if re.search(keyword_regex, sentence.strip().lower()):
            for answer in answers:
                answer = transform_answer_according_to_keyword(keyword_regex, sentence, answer)
                rets.append(answer)

    return rets


def logic(sentence):
    """
    Since the rules in the English language is not having double "no", we first start by checking if we can change the
    sentence from negative to positive. If there was no change it means the sentence is positive and we should turn it
    into negative.
    If that had failed to, it's only since the sentence is positive but have no matching supporting verbs,
    then we add a negative supporting verb after a personal pronouns.


    :param sentence: user's input
    :return: changed sentiment answer of the chat bot
    """
    f_changed, new_sentence = sentence_change_sign(sentence, "negative_to_positive")
    if not f_changed:
        f_changed, new_sentence = sentence_change_sign(sentence, "positive_to_negative")
        if not f_changed:
            f_changed, new_sentence = add_negative_word(new_sentence)

    if f_changed:
        new_sentence = reflect(new_sentence)
        new_sentence = new_sentence[0].upper() + new_sentence[1:]

        # if new_sentence[-1] == '?' and f_changed:
        #     new_sentence2 = "I think you are asking the wrong question. The right one is: " + new_sentence
        #     return [new_sentence, new_sentence2]
        # else:
        return [new_sentence]
    else:
        return []


def sentence_change_sign(sentence, sign):
    """
    changing the sentiment of the sentence to the other way around (positive -> negative or negative -> positive)

    :param sentence: user's input
    :param sign: shows direction of change sentiment, either "negative_to_positive" or  "positive_to_negative"
    :return: changed sentiment bot answer (take into consideration that reflection of the personal pronouns should be
    done later)
    """
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
        # Check if the word is in the list of changing supporting verbs words
        # if not f_changed and word_without_punctuation.lower() in change_supporting_verbs_according_to_sign:
        if not f_changed and word_without_punctuation.lower() in change_supporting_verbs_according_to_sign:
            # change the word
            sign_word = change_supporting_verbs_according_to_sign[word_without_punctuation.lower()]
            if word_without_punctuation.lower() != 'yes' and word_without_punctuation.lower() != 'no' \
                    and word_without_punctuation.lower() != 'not':
                f_changed = True
        else:
            # Keep the word as is
            sign_word = word_without_punctuation

        # add the punctuation after the word
        sign_word += word[len(word_without_punctuation):]

        # Add the changed word to the changed sentence
        if sign_word:
            changed_sentence.append(sign_word)

    # Join the words back into a sentence
    return f_changed, " ".join(changed_sentence)


def add_negative_word(sentence):
    """
    This function is called only if "sentence_change_sign" function failed for both direction (negative -> positive and
    positive -> negative). It adds the relevant supporting verb according to the personal pronoun.

    :param sentence: user's input
    :return: answer of bot with additional supporting verb
    """
    words = sentence.strip().split()

    additional_supporting_verb = None
    words_without_punctuation = pattern_punctuation.split(sentence.strip())
    for idx, (word, word_without_punctuation) in enumerate(zip(words, words_without_punctuation)):
        if word_without_punctuation.lower() in reflection_personal_pronouns:
            if word_without_punctuation.lower() in {"he", "she", "it"}:
                additional_supporting_verb = "doesn't"
            else:
                additional_supporting_verb = "don't"
            break

    if additional_supporting_verb and idx < len(words) - 1:
        return True, " ".join(words[:idx + 1] + [additional_supporting_verb] + words[idx + 1:])
    else:
        return False, " ".join(words)


def reflect(sentence):
    """

    :param sentence: user's parsed input after change of sentiment
    :return: ChatBot final answer after change of sentiment (done in previous called functions) and reflected personal
    pronouns (for example: "you" -> "I", "I" -> "you", etc.)
    """
    # Split the sentence into words
    words = sentence.strip().split()

    # Initialize the reflected sentence
    reflected_sentence = []

    # Iterate through the words
    words_without_punctuation = pattern_punctuation.split(sentence.strip())
    for word, word_without_punctuation in zip(words, words_without_punctuation):
        # Check if the word is in the list of reflectional words
        if word_without_punctuation.lower() in reflection_personal_pronouns:
            # Reflect the word
            reflected_word = reflection_personal_pronouns[word_without_punctuation.lower()]
        else:
            # Keep the word as is
            reflected_word = word_without_punctuation

        # add the punctuation after the word
        reflected_word += word[len(word_without_punctuation):]

        # Add the reflected word to the reflected sentence
        reflected_sentence.append(reflected_word)

    # Join the words back into a sentence
    new_sentence = " ".join(reflected_sentence)
    # change common mistakes of mismatch between personal pronoun and additional verb
    for mistake, correction in common_mistakes_correction.items():
        new_sentence = new_sentence.replace(mistake, correction)
    new_sentence = re.sub(" I$", r" me", new_sentence)
    new_sentence = re.sub(" I([,.?!]+)", r" me\1", new_sentence)

    return new_sentence


if __name__ == "__main__":
    conversation()
