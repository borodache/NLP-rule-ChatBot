from timer import Timer

import random
import re
import json


class ChatBot:
    def __init__(self):
        self.reflection_personal_pronouns = {"i": "you", "he": "he", "she": "she", "it": "it", "we": "you",
                                             "they": "they", "you": "I", "me": "you", "him": "him",
                                             "her": "her", "us": "you", "my": "your"}
        self.supporting_verbs_from_positive_to_negative = \
            {"is": "isn't", "are": "aren't", "am": "am not", "was": "wasn't", "were": "weren't", "has": "hasn't",
             "have": "haven't", "had": "hadn't", "will": "won't", "do": "don't"}

        self.supporting_verbs_from_negative_to_positive = {val: key for key, val in self.supporting_verbs_from_positive_to_negative.items()}
        self.supporting_verbs_from_negative_to_positive.update({"no": "", "not": "", "never": "always"})
        with open("C:\\Users\\borod\\PycharmProjects\\Bar Ilan University Course\\NLP rule chatbot\\keywords_to_answers.json", "r") as f:
            self.keywords_to_answers = json.load(f)

        self.keywords_to_answers = {re.compile(keyword): answers for keyword, answers in self.keywords_to_answers}

    def conversation(self):
        # while True:
        #     user_sentence = input("ChatBot: For how long do you want to argue? Please answer in minutes. ")
        #     if user_sentence.strip().isdigit():
        #         time_minutes = int(user_sentence)
        #         timer = Timer(time_minutes)
        #         timer.start()
        #         break

        # while not timer.stop():
        while True:
            user_sentence = input("You: ")
            if user_sentence.lower() == "stop talking!":
                print("ChatBot: I will never Stop Talking!")
                break

            results = chat_bot.keywords(user_sentence)
            result_logic = chat_bot.logic(user_sentence)
            if result_logic.lower() != user_sentence.lower():
                results.append(result_logic)
            # print("ChatBot:", random.choice(results))
            print("ChatBot:", results)

    def keywords(self, sentence):
        rets = []
        for keyword_compiled, answers in self.keywords_to_answers.items():
            if keyword_compiled.search(sentence.lower()):
                rets += answers

        return rets

    def logic(self, sentence):
        f_changed, new_sentence = self.sentence_from_negative_to_positive(sentence)
        if not f_changed:
            f_changed, new_sentence = self.sentence_from_positive_to_negative(sentence)
            if not f_changed:
                new_sentence = self.add_negative_word(new_sentence)

        new_sentence = chat_bot.reflect(new_sentence)
        new_sentence = new_sentence.replace("I aren't", "I am not")
        new_sentence = new_sentence.replace("aren't I", "isn't I")
        new_sentence = new_sentence.replace("I are", "I am")
        new_sentence = new_sentence.replace("are I", "am I")
        new_sentence = new_sentence.replace("you am not", "you aren't")
        new_sentence = new_sentence.replace("you am", "you are")
        new_sentence = new_sentence.replace("am not you", "aren't you")
        new_sentence = new_sentence.replace("am you", "are you")

        new_sentence = new_sentence[0].upper() + new_sentence[1:]

        return new_sentence

    def add_negative_word(self, sentence):
        words = sentence.strip().split()

        for idx, word in enumerate(words):
            if word.lower() in self.reflection_personal_pronouns:
                if word.lower() in {"he", "she", "it"}:
                    additional_word = "doesn't"
                else:
                    additional_word = "don't"
                break

        return " ".join(words[:idx + 1] + [additional_word] + words[idx + 1:])

    def sentence_from_negative_to_positive(self, sentence):
        # Split the sentence into words
        words = sentence.strip().split()

        # List of words that, when found, should be negated
        # Initialize the negated sentence
        positive_sentence = []

        # Iterate through the words
        f_negative = False
        for word in words:
            # Check if the word is in the list of negatable words
            if not f_negative and word.lower() in self.supporting_verbs_from_negative_to_positive:
                # Negate the word
                positive_word = self.supporting_verbs_from_negative_to_positive[word.lower()]
                f_negative = True
            else:
                # Keep the word as is
                positive_word = word

            # Add the negated word to the negated sentence
            if positive_word:
                positive_sentence.append(positive_word)

        # Join the words back into a sentence
        return f_negative, " ".join(positive_sentence)

    def sentence_from_positive_to_negative(self, sentence):
        # Split the sentence into words
        words = sentence.strip().split()

        # List of words that, when found, should be negated

        # Initialize the negated sentence
        negative_sentence = []

        # Iterate through the words
        f_positive = False
        for word in words:
            # Check if the word is in the list of negatable words
            if not f_positive and word.lower() in self.supporting_verbs_from_positive_to_negative:
                # Negate the word
                negative_word = self.supporting_verbs_from_positive_to_negative[word.lower()]
                f_positive = True
            else:
                # Keep the word as is
                negative_word = word

            # Add the negated word to the negated sentence
            negative_sentence.append(negative_word)

        # Join the words back into a sentence
        return f_positive, " ".join(negative_sentence)

    def reflect(self, sentence):
        # Split the sentence into words
        words = sentence.strip().split()

        # List of words that, when found, should be negated

        # Initialize the negated sentence
        reflected_sentence = []

        # Iterate through the words
        for word in words:
            # Check if the word is in the list of negatable words
            if word.lower() in self.reflection_personal_pronouns:
                # Negate the word
                reflected_word = self.reflection_personal_pronouns[word.lower()]
            else:
                # Keep the word as is
                reflected_word = word

            # Add the negated word to the negated sentence
            reflected_sentence.append(reflected_word)

        # Join the words back into a sentence
        return " ".join(reflected_sentence)


chat_bot = ChatBot()
chat_bot.conversation()
