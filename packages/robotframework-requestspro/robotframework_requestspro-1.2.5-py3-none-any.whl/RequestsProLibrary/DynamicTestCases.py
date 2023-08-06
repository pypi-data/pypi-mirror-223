from robot.api import logger
from robot.parsing.model import TestCase
from robot.parsing.model.statements import KeywordCall
from typing import List
import pandas as pd


class DynamicTestCases(object):
    """A Robot Framework test library to dynamically add test cases to the current suite."""

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.suite = None

    def _start_suite(self, suite, result):
        self.suite = suite

    def add_test_case(self, name: str, doc: str, tags: List[str], kwname: str, **kwargs):
        test_case = TestCase(name=name, tags=tags, doc=doc)

        for arg_name, arg_value in kwargs.items():
            keyword_call = KeywordCall(keyword='Set Test Variable', args=[f'${{{arg_name}}}', arg_value])
            test_case.body.add_step(keyword_call)

        keyword_call = KeywordCall(keyword=kwname)
        for arg_name in kwargs:
            keyword_call.add(arg_name=f'${{{arg_name}}}')
        test_case.body.add_step(keyword_call)

        self.suite.tests.append(test_case)
        logger.info(f"Added test case '{name}' with keyword '{kwname}' and keyword arguments: {kwargs}")

    def read_test_data_and_add_test_cases(self, csv_file_path: str):
        try:
            df = pd.read_csv(csv_file_path)
            for _, row in df.iterrows():
                name = row.get('test_name', '')
                doc = row.get('test_scenario', '')
                tags = row.get('test_tags', '').split(',')
                kwname = row.get('keyword', '')
                kwargs = {col[:-2]: row[col] for col in df.columns if col.endswith('_v')}
                self.add_test_case(name=name, doc=doc, tags=tags, kwname=kwname, **kwargs)
            logger.info(f"Successfully added test cases from '{csv_file_path}'.")
        except Exception as e:
            logger.error(f"Error occurred while reading test data from '{csv_file_path}': {e}")
