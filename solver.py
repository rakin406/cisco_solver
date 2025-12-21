import time
from enum import Enum
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup


class ExamAnswers(Enum):
    MODULE_1 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-1-exam-answers-ite-v8-0.html"
    MODULE_2 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-2-exam-answers-ite-v8-0.html"
    MODULE_3 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-3-exam-answers-ite-v8-0.html"
    MODULE_4 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-4-exam-answers-ite-v8-0.html"
    CHECKPOINT_MODULES_1_TO_4 = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-1-chapters-1-4-answers.html"
    MODULE_5 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-5-exam-answers-ite-v8-0.html"
    MODULE_6 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-6-exam-answers-ite-v8-0.html"
    CHECKPOINT_MODULES_5_TO_6 = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-2-chapters-5-6-answers.html"
    MODULE_7 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-7-exam-answers-ite-v8-0.html"
    MODULE_8 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-8-exam-answers-ite-v8-0.html"
    CHECKPOINT_MODULES_7_TO_8 = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-3-chapters-7-8-answers.html"
    MODULE_9 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-9-exam-answers-ite-v8-0.html"
    FINAL_MODULES_1_TO_9 = "https://itexamanswers.net/it-essentials-7-0-final-exam-chapters-1-9-answers-full.html"
    MODULE_10 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-10-exam-answers-ite-v8-0.html"
    MODULE_11 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-11-exam-answers-ite-v8-0.html"
    CHECKPOINT_MODULES_10_TO_11 = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-4-chapters-10-11-answers.html"
    MODULE_12 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-12-exam-answers-ite-v8-0.html"
    MODULE_13 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-13-exam-answers-ite-v8-0.html"
    CHECKPOINT_MODULES_12_TO_13 = "https://itexamanswers.net/ite-8-0-certification-checkpoint-exam-5-chapters-12-13-answers.html"
    MODULE_14 = "https://itexamanswers.net/it-essentials-version-8-0-chapter-14-exam-answers-ite-v8-0.html"
    FINAL_MODULES_10_TO_14 = "https://itexamanswers.net/it-essentials-7-0-final-exam-chapters-10-14-answers-full.html"
    IT_ESSENTIALS_FINAL = "https://itexamanswers.net/it-essentials-7-0-final-exam-composite-chapters-1-14-answers.html"


class Solver:
    def __init__(self, email: str, password: str):
        self.solving = False
        self.soup = None

        # Open netacad login page
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.netacad.com/")
        # FIX: Invalid selector
        login_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "btn btn--ghost loginBtn--lfDa2")
            )
        )
        login_button.click()

        # Login to netacad using user credentials
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys(email)
        username_field.send_keys(Keys.RETURN)
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # TODO: Handle invalid user credentials

        # Open course
        course = self.driver.find_element(By.ID, "it-essentials")
        course.click()

    def solve(self, answers_link: ExamAnswers):
        """
        Starts the solver
        """
        self.solving = True
        self.soup = self.get_soup(answers_link.value)

        while self.solving:
            answer = self.search_question()
            if answer:
                self.tick_answer(answer)
                self.click_submit()

                # Stop program when "Submit My Assessment" page is reached
                # try:
                #     pyscreeze.locateOnScreen(
                #         self.SUBMIT_ASSESSMENT_IMG, grayscale=True, confidence=0.8
                #     )
                #     self.stop()
                # except pyscreeze.ImageNotFoundException:
                #     pass
            elif not answer:
                self.stop()

    def stop(self):
        """
        Stops the solver

        :param self: self
        """
        self.solving = False

    def get_soup(self, answers_link: str) -> BeautifulSoup:
        page = requests.get(answers_link)
        soup = BeautifulSoup(page.content, "lxml")
        return soup

    def get_question(self) -> str:
        question = self.driver.find_elements(
            By.CLASS_NAME, "component__body-inner mcq__body-inner"
        )[-1].text
        return question

    def search_question(self) -> Optional[list[str]]:
        question = self.get_question()

        if not self.soup:
            return None

        # Find question
        for i in self.soup.find_all("strong"):
            if question in i.text:
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

        return None

    def tick_answer(self, answer: list[str]):
        # for i in answer:
        # TODO: Use selenium instead
        # pg.hotkey("ctrl", "f")
        # pg.press("backspace")
        # pg.write(i)
        # time.sleep(0.5)
        # pg.hotkey("shift", "enter")
        # time.sleep(0.5)
        # pg.press("esc")
        # pg.press("enter")
        # time.sleep(0.5)
        pass

    def click_submit(self):
        """
        Clicks the submit button
        """
        # TODO: Use selenium instead
        # pg.hotkey("ctrl", "f")
        # pg.press("backspace")
        # time.sleep(0.1)
        # pg.write("Submit")
        # time.sleep(0.1)
        # pg.press("esc")
        # pg.press("enter")
        pass
