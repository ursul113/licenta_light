import unittest
from core.lexer import Lexer
import os
class   TestLexer(unittest.TestCase):
    def setUp(self) -> None:
        open("out.txt", "w").close()
        open("translated.php", "w").close()

    def test_correct_code(self):
        pseudocode="a<--3"
        l=Lexer(pseudocode,"out.txt")
        result=l.f()
        self.assertEqual(result,"")
    def test_lexical_error(self):
        pseudocode = "$a<--3"
        l=Lexer(pseudocode,"out.txt")
        result = l.f()
        self.assertEqual(result, "Error at line 1: $a<--3")

    def tearDown(self) -> None:
        path = ["out.txt", "translated.php"]
        for p in path:
            if os.path.exists(p):
                os.remove(p)

if __name__ == '__main__':
    unittest.main()
