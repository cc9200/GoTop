# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""
import ctypes
import os
import multiprocessing
import time
from argparse import ArgumentParser
from multiprocessing import Value

import keyboard

import operator
from functools import partial
from terminaltables import AsciiTable

from config import api_key
from config import api_version
from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import enable_chrome
from config import image_compress_level
from config import prefer
from core.android import analyze_current_screen_text
from core.android import save_screen
from core.baiduzhidao import baidu_count
from core.check_words import parse_false
from core.chrome_search import run_browser
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.ocr.spaceocr import get_text_from_image as ocrspace_get_text

if prefer[0] == "baidu":
    get_text_from_image = partial(bai_get_text,
                                  app_id=app_id,
                                  app_key=app_key,
                                  app_secret=app_secret,
                                  api_version=api_version,
                                  timeout=5)

elif prefer[0] == "ocrspace":
    get_test_from_image = partial(ocrspace_get_text, api_key=api_key)


def parse_args():
    parser = ArgumentParser(description="Million Hero Assistant")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()


def parse_question_and_answer(text_list):
    question = ""
    start = 0
    for i, keyword in enumerate(text_list):
        question += keyword
        if "?" in keyword:
            start = i + 1
            break
    question = question.split(".")[-1]
    question, true_flag = parse_false(question)
    return true_flag, question, text_list[start:]


def pre_process_question(keyword):
    """
    strip charactor and strip ?
    :param question:
    :return:
    """
    for char, repl in [("“", ""), ("”", ""), ("？", "")]:
        keyword = keyword.replace(char, repl)

    keyword = keyword.split(r"．")[-1]
    keywords = keyword.split(" ")
    
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    keywords = keyword.strip('下列')
    return keyword


def main():
    
    args = parse_args()
    timeout = args.timeout
    
    print(os.popen('adb devices').read())
    print('''
          1.冲顶大会
          2.芝士超人
          3.百万英雄
    
    ''')
    choice=input('本次答题的APP是')
    choice=int(choice)
    if enable_chrome:
        question_obj = Value(ctypes.c_char_p, "".encode("utf-8"))
        browser_daemon = multiprocessing.Process(target=run_browser, args=(question_obj,))
        browser_daemon.daemon = True
        browser_daemon.start()

    def __inner_job(index=choice):
        start = time.time()
        
        text_binary = analyze_current_screen_text(
            directory=data_directory,
            compress_level=image_compress_level[1],
            index=choice
        )
        keywords = get_text_from_image(
            image_data=text_binary,
        )
        ##print('中国',keywords)
        if not keywords:
            print("failed")
            return
        ##true_flag,问题是否为正向问题，选择错误项的问题为反向问题
        true_flag, question, answers = parse_question_and_answer(keywords)
        
        print('\n',question)
    

        # notice browser
        if enable_chrome:
            with question_obj.get_lock():
                question_obj.value = question
                keyboard.press("space")

        search_question = pre_process_question(question)
        summary = baidu_count(search_question, answers, timeout=timeout)
        summary_li = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
        data = [("选项", "相关度")]
        for a, w in summary_li:
            data.append((a, w))
        table = AsciiTable(data)
        print(table.table)

        print("*" * 36)
        if true_flag:
            print("肯定回答(**)： ", summary_li[0][0])
            print("否定回答(  )： ", summary_li[-1][0])
        else:
            print("肯定回答(  )： ", summary_li[0][0])
            print("否定回答(**)： ", summary_li[-1][0])
        print("*" * 36)

        end = time.time()
        print("use {0} 秒".format(end - start))
        save_screen(
            directory=data_directory
        )

    while True:
        print("""
    请在答题开始前就运行程序，
    答题开始的时候按Enter预测答案
                """)

        enter = input("按Enter键开始，输入字母q回车退出...")
        if enter == 'q':
            break
        try:
            __inner_job()
        except Exception as e:
            print(str(e))

        print("欢迎下次使用")


if __name__ == "__main__":
    main()
