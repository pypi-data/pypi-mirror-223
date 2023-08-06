# -*- coding: utf-8 -*-
"""


Author: ken
Date: 2023/8/5
"""
import random
import string


def generate_random_digits_str(digits: int) -> str:
    """
    隨機產生0-9 + 英文字母的隨機碼
    :param digits: 欲產生的碼數
    :return:
    """
    all_characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(all_characters) for _ in range(digits))
    return random_string