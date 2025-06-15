from core.lexer import Lexer
from core.synthax import Parser
import subprocess
import os
def execute(pseudocode,keyboard_input,lexer_file="core/out.txt", output_file="core/translated.php"):
    l=Lexer(pseudocode,lexer_file)
    errs=l.f()
    if errs!="":
        return errs
    p=Parser(pseudocode,keyboard_input,output_file)
    p.parse()
    result = subprocess.run(['php',output_file ], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return "Error running PHP script: "+result.stdout