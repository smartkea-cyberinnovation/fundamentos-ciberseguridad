#!/usr/bin/env python3
"""Functional acceptance of the built, self-contained exam in a real browser.

Run the campus build first, then execute this file. A missing browser is an error.
CAMPUS_EXAM_SITE_ROOT and CAMPUS_EXAM_PATH allow the same tests against worker-dist
and its /introduccion-ciberseguridad/examen/ prefix without changing application code.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys
from threading import Thread
import unittest
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from serve import Handler

KEY = 'fundamentos-ciberseguridad:exam:v1'
COURSE_KEY = 'fundamentos-ciberseguridad:progress:v1'
ENGINE = os.environ.get('CAMPUS_BROWSER', 'chromium')
SITE_ROOT = Path(os.environ.get('CAMPUS_EXAM_SITE_ROOT', str(HERE / 'dist')))
EXAM_PATH = os.environ.get('CAMPUS_EXAM_PATH', '/examen/')
SHOTS = Path(os.environ.get('CAMPUS_EXAM_SCREENSHOTS', str(HERE / 'qa/current' / ENGINE / 'screenshots')))


class ExamBrowserAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((SITE_ROOT / EXAM_PATH.strip('/') / 'questions.json').read_text(encoding='utf-8'))
        cls.questions = {question['id']: question for question in cls.data['questions']}
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(SITE_ROOT)))
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}{EXAM_PATH}'
        cls.playwright = sync_playwright().start()
        if ENGINE not in ('chromium', 'webkit', 'firefox'):
            raise ValueError('Unsupported browser engine')
        options = {'headless': True}
        executable = os.environ.get('CAMPUS_BROWSER_EXECUTABLE') or os.environ.get('CHROMIUM_EXECUTABLE')
        if executable:
            options['executable_path'] = executable
        cls.browser = getattr(cls.playwright, ENGINE).launch(**options)
        SHOTS.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        self.page = self.context.new_page()
        self.errors = []
        self.external = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))

        def local_only(route):
            if urlsplit(route.request.url).hostname not in ('127.0.0.1', 'localhost'):
                self.external.append(route.request.url)
                route.abort()
            else:
                route.continue_()
        self.page.route('**/*', local_only)

    def tearDown(self):
        try:
            self.assertEqual(self.errors, [])
            self.assertEqual(self.external, [])
        finally:
            self.context.close()

    def go(self):
        self.page.goto(self.base, wait_until='networkidle')
        expect(self.page.locator('#start-attempt')).to_be_visible()

    def start(self):
        self.go()
        self.page.locator('#start-attempt').click()
        expect(self.page.locator('#question-title')).to_be_visible()

    def state(self):
        return self.page.evaluate('(key) => JSON.parse(localStorage.getItem(key))', KEY)

    def current_question(self):
        return self.questions[self.page.locator('[data-question-id]').get_attribute('data-question-id')]

    def answer(self, correct=True):
        question = self.current_question()
        option = question['correctOptionId'] if correct else next(item['id'] for item in question['options'] if item['id'] != question['correctOptionId'])
        self.page.locator(f'input[name=answer][value="{option}"]').check()
        expect(self.page.locator('#answer-feedback')).to_be_visible()
        return question

    def test_01_start_20_unique_questions_and_keyboard_correction(self):
        self.go()
        expect(self.page.locator('html')).to_have_attribute('lang', 'es')
        expect(self.page).to_have_title('Introducción a la informática · Autoevaluación')
        self.page.screenshot(path=str(SHOTS / 'exam-home.png'), full_page=True)
        self.page.locator('#start-attempt').click()
        expect(self.page.locator('input[type=radio]')).to_have_count(4)
        state = self.state()
        self.assertEqual(len(state['questionIds']), 20)
        self.assertEqual(len(set(state['questionIds'])), 20)
        for order in state['optionOrders'].values():
            self.assertEqual(sorted(order), ['a', 'b', 'c', 'd'])
        question = self.current_question()
        self.page.locator(f'input[value="{question["correctOptionId"]}"]').focus()
        self.page.keyboard.press('Space')
        expect(self.page.locator('#answer-feedback')).to_contain_text('Respuesta correcta')
        expect(self.page.locator('#answer-explanation')).to_have_text(question['explanation'])
        expect(self.page.locator('input[type=radio]:disabled')).to_have_count(4)
        expect(self.page.locator('#answered-count')).to_have_text('1 de 20 respondidas')
        expect(self.page.locator('#answer-feedback')).to_be_focused()
        self.page.screenshot(path=str(SHOTS / 'exam-feedback.png'), full_page=True)

    def test_02_incorrect_answer_shows_solution_and_cannot_score_twice(self):
        self.start()
        question = self.answer(False)
        expect(self.page.locator('.answer-option.correct')).to_have_count(1)
        expect(self.page.locator('.answer-option.incorrect')).to_have_count(1)
        expect(self.page.locator('.answer-option.correct')).to_have_attribute('data-option-id', question['correctOptionId'])
        before = self.state()
        self.page.locator(f'input[value="{question["correctOptionId"]}"]').dispatch_event('change')
        self.assertEqual(self.state(), before)
        self.page.locator('#next-question').click()
        self.page.locator('#previous-question').click()
        expect(self.page.locator('#answer-feedback')).to_contain_text('Esta vez no es correcta')
        self.assertEqual(len(self.state()['answers']), 1)

    def test_03_reload_requires_explicit_resume_and_keeps_campus_progress(self):
        self.go()
        self.page.evaluate('([key,value]) => localStorage.setItem(key,value)', [COURSE_KEY, 'existing-campus-progress'])
        self.page.locator('#start-attempt').click()
        self.answer()
        self.page.locator('#next-question').click()
        original = self.state()
        self.page.reload()
        expect(self.page.locator('#resume-attempt')).to_have_text('Reanudar intento')
        expect(self.page.locator('#question-title')).to_have_count(0)
        self.page.locator('#resume-attempt').click()
        expect(self.page.locator('[data-question-id]')).to_have_attribute('data-question-id', original['questionIds'][1])
        self.assertEqual(self.state(), original)
        self.assertEqual(self.page.evaluate('(key) => localStorage.getItem(key)', COURSE_KEY), 'existing-campus-progress')

    def test_04_finish_pending_requires_confirmation_and_review_is_read_only(self):
        self.start()
        self.answer()
        self.page.locator('#finish-attempt').click()
        expect(self.page.locator('#confirm-dialog')).to_be_visible()
        expect(self.page.locator('#confirm-description')).to_contain_text('19 preguntas')
        expect(self.page.locator('#cancel-confirmation')).to_be_focused()
        self.page.keyboard.press('Escape')
        expect(self.page.locator('#confirm-dialog')).not_to_be_visible()
        expect(self.page.locator('#finish-attempt')).to_be_focused()
        self.assertEqual(self.state()['status'], 'active')
        self.page.locator('#finish-attempt').click()
        self.page.locator('#accept-confirmation').click()
        expect(self.page.locator('#result-grade')).to_have_text('0,5')
        expect(self.page.locator('#result-unanswered')).to_have_text('19')
        self.assertEqual(self.state()['status'], 'finished')
        self.page.locator('#review-mistakes').click()
        expect(self.page.locator('#answer-feedback')).to_contain_text('Sin responder')
        expect(self.page.locator('input[type=radio]:disabled')).to_have_count(4)
        expect(self.page.locator('.question-index button')).to_have_count(19)
        self.page.locator('#back-to-results').click()
        expect(self.page.locator('#result-grade')).to_have_text('0,5')

    def test_05_complete_attempt_scores_by_topic_and_starts_new_selection(self):
        self.start()
        original = self.state()
        for index in range(20):
            self.answer(correct=index < 10)
            if index < 19:
                self.page.locator('#next-question').click()
        expect(self.page.locator('#answered-count')).to_have_text('20 de 20 respondidas')
        self.page.locator('#finish-attempt').click()
        expect(self.page.locator('#result-grade')).to_have_text('5')
        expect(self.page.locator('#result-correct')).to_have_text('10')
        expect(self.page.locator('#result-incorrect')).to_have_text('10')
        expect(self.page.locator('#result-unanswered')).to_have_text('0')
        totals = self.page.locator('#topic-results tbody tr').evaluate_all('(rows) => rows.map(row => [...row.querySelectorAll("td")].map(cell => Number(cell.textContent)))')
        self.assertEqual([sum(row[index] for row in totals) for index in range(4)], [10, 10, 0, 20])
        self.page.screenshot(path=str(SHOTS / 'exam-results.png'), full_page=True)
        self.page.locator('#review-mistakes').click()
        expect(self.page.locator('.question-index button')).to_have_count(10)
        self.page.locator('#back-to-results').click()
        self.page.locator('#new-attempt-result').click()
        expect(self.page.locator('#answered-count')).to_have_text('0 de 20 respondidas')
        self.assertNotEqual(self.state()['questionIds'], original['questionIds'])

    def test_06_replacing_active_attempt_requires_confirmation(self):
        self.start()
        self.answer()
        original = self.state()
        self.page.locator('#restart-attempt').click()
        expect(self.page.locator('#confirm-dialog')).to_be_visible()
        self.page.locator('#cancel-confirmation').click()
        self.assertEqual(self.state(), original)
        self.page.locator('#restart-attempt').click()
        self.page.locator('#accept-confirmation').click()
        expect(self.page.locator('#answered-count')).to_have_text('0 de 20 respondidas')
        self.assertNotEqual(self.state()['questionIds'], original['questionIds'])

    def test_07_denied_local_storage_keeps_the_quiz_functional(self):
        self.context.add_init_script("Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('Denied', 'SecurityError'); } });")
        self.start()
        expect(self.page.locator('#storage-note')).to_be_visible()
        self.answer()
        expect(self.page.locator('#answered-count')).to_have_text('1 de 20 respondidas')
        self.page.locator('#pause-attempt').click()
        self.page.locator('#resume-attempt').click()
        expect(self.page.locator('#answer-feedback')).to_contain_text('Respuesta correcta')

    def test_08_corrupt_or_inconsistent_saved_attempt_is_rejected(self):
        self.go()
        self.page.evaluate('([key,value]) => localStorage.setItem(key,value)', [KEY, '{broken json'])
        self.page.reload()
        expect(self.page.locator('#storage-note')).to_contain_text('otra versión')
        expect(self.page.locator('#resume-attempt')).to_have_count(0)
        self.page.locator('#start-attempt').click()
        self.page.evaluate('(key) => { const state = JSON.parse(localStorage.getItem(key)); state.questionIds[1] = state.questionIds[0]; localStorage.setItem(key, JSON.stringify(state)); }', KEY)
        self.page.reload()
        expect(self.page.locator('#resume-attempt')).to_have_count(0)
        self.page.locator('#start-attempt').click()
        self.answer()
        expect(self.page.locator('#storage-note')).not_to_be_visible()

    def test_09_mobile_320px_and_modal_have_no_page_overflow(self):
        self.page.set_viewport_size({'width': 320, 'height': 740})
        self.start()
        self.answer(False)
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 321)
        self.page.screenshot(path=str(SHOTS / 'exam-mobile-320.png'), full_page=True)
        self.page.locator('#restart-attempt').click()
        expect(self.page.locator('#confirm-dialog')).to_be_visible()
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 321)
        self.page.locator('#cancel-confirmation').click()
        self.page.locator('#finish-attempt').click()
        self.page.locator('#accept-confirmation').click()
        expect(self.page.locator('#results-heading')).to_be_visible()
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 321)

    def test_10_invalid_bank_fails_closed_and_retry_recovers(self):
        def invalid_bank(route):
            route.fulfill(status=200, content_type='application/json', body='{"schemaVersion":1,"questions":[]}')
        self.page.route('**/questions.json', invalid_bank)
        self.page.goto(self.base)
        expect(self.page.locator('#load-error')).to_be_visible()
        expect(self.page.locator('#start-attempt')).to_have_count(0)
        self.page.unroute('**/questions.json', invalid_bank)
        self.page.locator('#retry-load').click()
        expect(self.page.locator('#start-attempt')).to_be_visible()

    def test_11_study_link_returns_to_the_correct_course_resource(self):
        self.start()
        question = self.answer()
        expect(self.page.locator('.study-link')).to_have_attribute('href', question['study']['url'])
        self.page.locator('.study-link').click()
        self.assertIn(question['study']['url'].split('#', 1)[1], self.page.url)
        expect(self.page.locator('#main article.prose')).to_be_visible()

    def test_12_finished_attempt_resumes_as_results(self):
        self.start()
        self.page.locator('#finish-attempt').click()
        self.page.locator('#accept-confirmation').click()
        expect(self.page.locator('#result-grade')).to_have_text('0')
        self.page.reload()
        expect(self.page.locator('#resume-attempt')).to_have_text('Ver último resultado')
        self.page.locator('#resume-attempt').click()
        expect(self.page.locator('#result-unanswered')).to_have_text('20')


if __name__ == '__main__':
    unittest.main(verbosity=2)
