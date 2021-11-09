import sys
import newLexer

def parseError(msg):
    print("Parse Error: " + msg + " at line " + str(lexer.line))