import re


def transform_answer_according_to_keyword(keyword_regex: str, sentence:str, answer: str):
    """
    This function returns the answer after group changing in keyword detection (\1, \2, etc.)
    :param keyword_regex: the keyword the should be found in sentence
    :param sentence: user's input
    :param answer: one of the answer's in json
    :return: answer in json after swaping the group with its match (e.g. %1 with \1)
    """
    matches = re.finditer(keyword_regex, sentence)  # , re.MULTILINE

    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            group = str(match.group(groupNum))
            answer = re.sub(f"%{groupNum}", group, answer)

    return answer

