import unittest
import os
from core.executor2 import execute

class TestExecutor(unittest.TestCase):

    def setUp(self) -> None:
        open("out.txt", "w").close()
        open("translated.php", "w").close()
    def test_simple_arithmetic_output(self):
        pseudocode = 'scrie(2+1)'
        result=execute(pseudocode,"","out.txt","translated.php")
        self.assertEqual(result, '3')

    def test_variable_assignment(self):
        pseudocode = 'a<--3\nscrie(a)'
        result=execute(pseudocode,"","out.txt","translated.php")
        self.assertEqual(result, '3')

    def test_input_and_loop(self):
        pseudocode = """
         citeste(a)
         pentru i<--1,10 executa
            a<-- a+1
         sf_pentru
         scrie(a)
        """
        result=execute(pseudocode,"1","out.txt","translated.php")
        self.assertEqual(result, '11')
    def test_synthax_error_crash(self):
        pseudocode = "a<--3\nscrie a"
        try:
            execute(pseudocode,"","out.txt","translated.php")
            assert False
        except ValueError:
            assert True

    def tearDown(self) -> None:
        path=["out.txt","translated.php"]
        for p in path:
            if os.path.exists(p):
                os.remove(p)


if __name__ == '__main__':
    unittest.main()
