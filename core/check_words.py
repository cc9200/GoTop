# -*- coding: utf-8 -*-



FALSE = (
    "不",
    "错误",
    '没有'
)


def parse_false(question):
    """

    :param question:
    :return:
    """
    for item in FALSE:
        if item in question:
            question = question.replace(item, "")
            return question, False

    return question, True
