import time
from typing import Optional

import pyautogui as pg
import pyperclip
import pyscreeze
import requests
from bs4 import BeautifulSoup

SUBMIT_ASSESSMENT_IMG = "./assets/submit-assessment.png"
MAX_EXAMS = 33

curr_exam = 1
curr_question = 1


def get_soup() -> BeautifulSoup:
    url = ""

    match curr_exam:
        # Checkpoint exams
        case 15:
            url = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-1-chapters-1-4-answers.html"
        case 16:
            url = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-2-chapters-5-6-answers.html"
        case 17:
            url = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-3-chapters-7-8-answers.html"
        case 18:
            url = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-4-chapters-10-11-answers.html"
        case 19:
            url = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-5-chapters-12-13-answers.html"
        # Summary quizzes
        case 20:
            url = "https://itexamanswers.net/it-essentials-8-module-1-quiz-answers-introduction-to-personal-computer-hardware.html"
        case 21:
            url = "https://itexamanswers.net/it-essentials-8-module-2-quiz-answers-pc-assembly.html"
        case 22:
            url = "https://itexamanswers.net/it-essentials-8-module-3-quiz-answers-advanced-computer-hardware-quiz-answers.html"
        case 23:
            url = "https://itexamanswers.net/it-essentials-8-module-4-quiz-answers-preventive-maintenance-and-troubleshooting.html"
        case 24:
            url = "https://itexamanswers.net/it-essentials-8-module-5-quiz-answers-networking-concepts.html"
        case 25:
            url = "https://itexamanswers.net/it-essentials-8-module-6-quiz-answers-applied-networking.html"
        case 26:
            url = "https://itexamanswers.net/it-essentials-8-module-7-quiz-answers-laptops-and-other-mobile-devices.html"
        case 27:
            url = "https://itexamanswers.net/it-essentials-8-module-8-quiz-answers-printers.html"
        case 28:
            url = "https://itexamanswers.net/it-essentials-v7-01-chapter-9-quiz-answers.html"
        case 29:
            url = "https://itexamanswers.net/it-essentials-8-module-10-quiz-answers-windows-installation.html"
        case 30:
            url = "https://itexamanswers.net/it-essentials-8-module-11-quiz-answers-windows-configuration.html"
        case 31:
            url = "https://itexamanswers.net/it-essentials-8-module-12-quiz-answers-mobile-linux-and-macos-operating-systems.html"
        case 32:
            url = "https://itexamanswers.net/it-essentials-8-module-13-quiz-answers-security.html"
        case 33:
            url = "https://itexamanswers.net/it-essentials-8-module-14-quiz-answers-the-it-professional.html"
        # Module exam
        case _:
            url = f"https://itexamanswers.net/it-essentials-version-8-0-chapter-{curr_exam}-exam-answers-ite-v8-0.html"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    return soup


soup = get_soup()


def open_exam():
    pg.hotkey("alt", "tab")


def click_submit():
    """
    Clicks the submit button
    """
    pg.hotkey("ctrl", "f")
    time.sleep(0.1)
    pg.write("Submit")
    time.sleep(0.1)
    pg.press("esc")
    pg.press("enter")


def get_question() -> str:
    global curr_question
    question = ""

    pg.hotkey("ctrl", "f")
    time.sleep(0.5)
    pg.write(f"Question {curr_question}")
    curr_question += 1

    time.sleep(0.5)
    pg.press("esc")
    pg.hotkey("ctrl", "a")
    pg.hotkey("ctrl", "f")
    pg.hotkey("ctrl", "c")
    time.sleep(0.1)
    pg.press("esc")
    question = pyperclip.paste()

    return question


def search_question() -> Optional[list[str]]:
    global curr_exam, soup
    question = get_question()

    while curr_exam <= MAX_EXAMS:
        # Find question
        for i in soup.find_all("strong"):
            if i.text in question:
                # Find answer
                options = i.parent.find_next_sibling("ul") if i.parent else None
                answer = (
                    [
                        option.text
                        for option in options.find_all(
                            "li", {"class": "correct_answer"}
                        )
                    ]
                    if options
                    else None
                )

                return answer

        curr_exam += 1
        soup = get_soup()

    return None


def tick_answer(answer: list[str]):
    for i in answer:
        pg.hotkey("ctrl", "f")
        pg.write(i)
        pg.press("enter", presses=2)
        time.sleep(0.5)
        pg.press("esc")
        pg.press("enter")
        time.sleep(0.5)


if __name__ == "__main__":
    solving = True
    open_exam()

    while solving:
        answer = search_question()
        if answer:
            tick_answer(answer)
            click_submit()

        # Stop program when "Submit My Assessment" page is reached
        try:
            pyscreeze.locateOnScreen(
                SUBMIT_ASSESSMENT_IMG, grayscale=True, confidence=0.8
            )
            solving = False
        except pyscreeze.ImageNotFoundException:
            pass
