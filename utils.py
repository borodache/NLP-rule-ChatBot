import re


def transform_answer_according_to_keyword(keyword_regex: str, sentence:str, answer: str):
    matches = re.finditer(keyword_regex, sentence)  # , re.MULTILINE

    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            group = str(match.group(groupNum))
            answer = re.sub(f"%{groupNum}", group, answer)

    return answer

