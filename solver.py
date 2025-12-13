import time
from typing import Optional

import pyautogui as pg
import pyscreeze
import pytesseract
import requests
from bs4 import BeautifulSoup

pytesseract.pytesseract.tesseract_cmd = "./binaries/Tesseract-OCR/tesseract.exe"

FULLSCREEN_BUTTON_IMG = "./assets/fullscreen.png"
# NEXT_BUTTON_IMG = "./assets/next.png"
SUBMIT_BUTTON_IMG = "./assets/submit.png"
SUBMIT_ASSESSMENT_IMG = "./assets/submit-assessment.png"
MAX_EXAMS = 19
QUESTION_WORDS = ["what", "why", "which", "when", "where", "who", "how"]

curr_exam = 1
next_button_pos = None
submit_button_pos = None
fullscreen_button_pos = None


def get_soup() -> BeautifulSoup:
    url = ""

    match curr_exam:
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
        case _:
            url = f"https://itexamanswers.net/it-essentials-version-8-0-chapter-{curr_exam}-exam-answers-ite-v8-0.html"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    return soup


soup = get_soup()


def click_button(button_image, button_pos) -> bool:
    """
    Clicks the button matching the image

    :param button_image: Button image
    :param button_pos: Button position
    :return: Button click successful
    :rtype: bool
    """
    if button_pos:
        pg.click(button_pos)
    else:
        try:
            button_pos = pyscreeze.locateCenterOnScreen(
                button_image, grayscale=True, confidence=0.8
            )
            click_button(button_image, button_pos)
        except pyscreeze.ImageNotFoundException:
            return False

    return True


def open_exam():
    pg.hotkey("alt", "tab")
    pg.press("home")
    click_fullscreen()


# NOTE: This is currently unused
# def click_next():
#     """
#     Clicks the next button
#     """
#     global next_button_pos
#     click_button(NEXT_BUTTON_IMG, next_button_pos)


def click_submit():
    """
    Clicks the submit button
    """
    global submit_button_pos
    click_button(SUBMIT_BUTTON_IMG, submit_button_pos)


def click_fullscreen():
    """
    Clicks the fullscreen button
    """
    global fullscreen_button_pos
    if click_button(FULLSCREEN_BUTTON_IMG, fullscreen_button_pos):
        # This is to remove the fullscreen popup
        time.sleep(0.5)
        pg.moveTo(None, 0)
        pg.move(0, 500)


def search_question() -> Optional[list[str]]:
    global curr_exam, soup

    # Parse the question from screenshot
    question_img = pg.screenshot()
    text = pytesseract.image_to_string(question_img)
    text = text.split("\n")
    question = ""

    # Find question words (what, where etc.) in text
    for i in text:
        lower_text = i.lower()
        for j in QUESTION_WORDS:
            if j in lower_text:
                question = lower_text
                break

        if question:
            break

    while curr_exam <= MAX_EXAMS:
        # Find question
        for i in soup.find_all("strong"):
            if question in i.text.lower():
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
        click_fullscreen()
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
