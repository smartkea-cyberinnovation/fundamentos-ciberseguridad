"""Syllabus coverage and shipped exam assets, independent of browser grading."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build
from exam_build import BANK, validate_bank
from check_release import validate_html_assets
from bilingual import collect_en


class IntroExamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es = build.collect()
        cls.bank = json.loads(BANK.read_text(encoding='utf-8'))
        cls.ids = {r['id'] for r in cls.es['resources']}

    def test_all_twelve_topics_have_questions_and_existing_study_references(self):
        validate_bank(self.bank, self.ids)
        self.assertEqual(len(self.bank['questions']), 100)
        self.assertEqual({q['topic'] for q in self.bank['questions']}, {f'T{i:02}' for i in range(1,13)})

    def test_old_readings_keep_ids_and_new_foundations_have_both_editions(self):
        en = collect_en(self.es, build.HERE/'locales/en', build.markdown, build.read_text)
        for course in (self.es, en):
            self.assertEqual([r['id'] for r in course['resources'][:40]], [f'D{i:02}' for i in range(1,41)])
            self.assertEqual([r['id'] for r in course['resources'][40:]], [f'D{i:02}' for i in range(41,47)])
            for resource in course['resources'][40:]:
                self.assertGreater(len(resource['html']), 2000, resource['id'])
                self.assertGreaterEqual(len(resource['toc']), 4, resource['id'])
                self.assertNotIn('<!--', resource['html'])
                self.assertTrue(resource['slides'])
                self.assertNotIn('/../', resource['source'])

    def test_bank_rejects_missing_duplicate_ambiguous_and_unresolved_items(self):
        mutations = (
            lambda x: x['questions'].pop(),
            lambda x: x['questions'][1].update(id=x['questions'][0]['id']),
            lambda x: x['questions'][0].update(correctOptionId='z'),
            lambda x: x['questions'][0]['options'][1].update(text=x['questions'][0]['options'][0]['text']),
            lambda x: x['questions'][0]['study'].update(url='../#/recurso/D99'),
            lambda x: x['questions'][0]['study'].update(url='https://external.example/'),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                data = deepcopy(self.bank); mutate(data)
                with self.assertRaises(ValueError): validate_bank(data, self.ids)


class NestedAssetsTests(unittest.TestCase):
    def test_directory_indexes_relative_assets_and_queries_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {'index.html':'<a href="sistemas/?lang=en">OS</a><a href="examen/">Test</a>',
                       'sistemas/index.html':'<a href="../">Campus</a>',
                       'examen/index.html':'<script src="model.mjs"></script><a href="../#/recurso/D41">Study</a>',
                       'examen/model.mjs':'export const ok=true;'}
            files={}
            for name, content in sources.items():
                path=root/name; path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content);files[name]=path
            validate_html_assets(files)
            (root/'examen/index.html').write_text('<script src="missing.js"></script>')
            with self.assertRaises(ValueError): validate_html_assets(files)
            (root/'examen/index.html').write_text('<a href="../../private/">Outside</a>')
            with self.assertRaises(ValueError): validate_html_assets(files)


if __name__ == '__main__': unittest.main()
