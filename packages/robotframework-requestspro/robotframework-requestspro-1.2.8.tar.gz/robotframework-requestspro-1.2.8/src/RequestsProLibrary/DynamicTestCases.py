from robot.api import logger
from typing import List
import pandas as pd


class DynamicTestCases(object):
    """A Robot Framework test library to dynamically add test cases to the current suite."""
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.current_suite = None

    def _start_suite(self, suite, result):
        self.current_suite = suite

    def add_test_case(self, name: str, doc: str, tags: List[str], kwname: str, **kwargs):
        """Adds a test case to the current suite.

        `name`: The test case name (str).
        `doc`: The documentation for the test case (str).
        `tags`: Tags to be associated with the test case (List of str).
        `kwname`: The keyword to call (str).
        `**kwargs`: Keyword arguments to be passed to the keyword.

        Example:
        | Add Test Case | Example Test Case | This is a dynamic test case | ['smoke'] | My Keyword | arg1=value1 | arg2=value2 |
        """
        test_case = self.current_suite.tests.create(name=name, doc=doc, tags=tags)
        args = []
        for arg_name, arg_value in kwargs.items():
            args.append(f'{arg_name}={arg_value}')
        test_case.body.create_keyword(name=kwname, args=args)
        # self.suite.tests.append(test_case)
        logger.info(f"Added test case '{name}' with keyword '{kwname}' and keyword arguments: {kwargs}")

    def read_test_data_and_add_test_cases(self, csv_file_path: str):
        """Reads test data from a CSV file and adds test cases dynamically.

        `csv_file_path`: The path to the CSV file containing test data.

        Example:
        | Read Test Data And Add Test Cases | /path/to/test_data.csv |
        """
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
