# NLP-rule-ChatBot

Introduction
The Python Argument Clinic will be an interactive program inspired by the Monty Python "Argument Clinic" sketch. 
This project aims to create a playful command-line application where users can have a mock argument with an automated response system.
This project is a basic Python programming practice project. The NLP part here isn't the most crucial here, but basically it imitates how chatbots were built in the very beginning of NLP (50 years ago). This ChatBot works in the same way as the Argument Clinic in Monty Python, and it's target is to make an argument...


## files
1. keywords_to_answers.json - a json file saving the keywords to search in the user's input, and a set of relevant 
answers. 
2. main.py - the file that should be run, it is the file that makes the ChatBot conversation
3. timer.py - A file that measures the conversation lasts for only 5 minutes. 
4. utils.py - A utils file, contains only one function, a helper function to the keywords_to_answers.json, it swaps 
groups matched in the user's input, with its value in the ChatBot answer

## How to run?
clone the repository for your local computer, and run the main.py file.