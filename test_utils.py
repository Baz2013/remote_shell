# -*- coding:utf-8 -*-
"""
test the function in utils.py
"""

import unittest
import utils


class TestMain(unittest.TestCase):
    def test_split_copy_command(self):
        self.assertIn('/abc/123/a.txt', utils.split_copy_command('src = /abc/123/a.txt dest=/def/user/'))
        self.assertIn('/def/user/', utils.split_copy_command('src = /abc/123/a.txt dest=/def/user/'))
        self.assertNotIn('src', utils.split_copy_command('src = /abc/123/a.txt dest=/def/user/'))

    def test_strip_comment(self):
        self.assertEqual('abc', utils._strip_comment('abc#def#123'))
        self.assertEqual('abc', utils._strip_comment('abc   # def#123'))
        self.assertEqual('abc', utils._strip_comment('abc   #'))
        self.assertEqual(None, utils._strip_comment('#abc   '))
        self.assertEqual('abc', utils._strip_comment('abc'))

    def test_get_host(self):
        self.assertIn('10.xx.xx.231', utils.get_hosts(
            {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
            'logger_test'))
        self.assertIn('10.xx.xx.231', utils.get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger_test'))
        self.assertIn('10.xx.xx.232', utils.get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger_test'))
        self.assertIn('10.xx.xx.232', utils.get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger'))
        self.assertIn('10.xx.xx.84:8081', utils.get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger'))

    def test_exactly_get_host(self):
        self.assertIn('10.xx.xx.231', utils.exactly_get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger_test'))
        self.assertIn('10.xx.xx.232', utils.exactly_get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger_test'))
        self.assertNotIn('10.xx.xx.84:8081', utils.exactly_get_hosts(
                {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'], 'logger': ['10.xx.xx.84:8081', '10.xx.xx.85:8081']},
                'logger_test'))
        self.assertIn('10.xx.xx.231', utils.exactly_get_hosts(
            {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'],
             'logger': ['10.xx.xx.84', '10.xx.xx.85'],
             'pro_logger': ['10.xx.xx.90', '10.xx.xx.91']},
            'logger_test|pro_logger'))
        self.assertIn('10.xx.xx.90', utils.exactly_get_hosts(
            {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'],
             'logger': ['10.xx.xx.84', '10.xx.xx.85'],
             'pro_logger': ['10.xx.xx.90', '10.xx.xx.91']},
            'logger_test|pro_logger'))
        self.assertIn('10.xx.xx.91', utils.exactly_get_hosts(
            {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'],
             'logger': ['10.xx.xx.84', '10.xx.xx.85'],
             'pro_logger': ['10.xx.xx.90', '10.xx.xx.91']},
            'logger_test|pro_logger'))
        self.assertNotIn('10.xx.xx.84', utils.exactly_get_hosts(
            {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'],
             'logger': ['10.xx.xx.84', '10.xx.xx.85'],
             'pro_logger': ['10.xx.xx.90', '10.xx.xx.91']},
            'logger_test|pro_logger'))
        self.assertIn('10.xx.xx.232', utils.exactly_get_hosts(
            {'logger_test': ['10.xx.xx.231', '10.xx.xx.232'],
             'logger': ['10.xx.xx.84', '10.xx.xx.85'],
             'pro_logger': ['10.xx.xx.90', '10.xx.xx.91']},
            'logger_test|pro_logger|abc_logger'))


if __name__ == '__main__':
    unittest.main()