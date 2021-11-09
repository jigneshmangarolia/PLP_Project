import sys
import lexer

def parseError(msg):
    print("Parse Error: " + msg + " at line " + str(lexer.line))

def lex():
    global nextToken
    global input
    [nextToken, input] = lexer.lex(input)

def parseVal():
    good = nextToken[0] == lexer.INT_TOKEN or nextToken[0] == lexer.ID_TOKEN
    if (not good) and nextToken[0] == lexer.LEXEME and nextToken[1] == "-":
        lex()
        good = nextToken[0] == lexer.ID_TOKEN
    if good:
        lex()
    else:
        parseError("Expected value")
    return good

def parseValList():
    if parseVal():
        if nextToken[0] == lexer.LEXEME and nextToken[1] == ",":
            lex()
            return parseValList()
        else:
            return True
    else:
        return False

def parseCmp():
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected Comparison operator")
        return False
    
    if nextToken[1] == "<" or nextToken[1] == "=" or nextToken[1] == "<=":
        lex()
        return True
    else:
        parseError("Expected Comparison operator")
        return False

def parseCmd():
    global nextToken
    global input
    if nextToken[0] != lexer.LEXEME:
        parseError("Expected command got: " + str(nextToken))
        return False

    if nextToken[1] == "get":
        lex()
        if nextToken[0] == lexer.ID_TOKEN:
            lex()
            return True
        else:
            parseError("Expected ID")
            return False
    elif nextToken[1] == "print":
        lex()
        return parseVal()
    elif nextToken[1] == "sum":
        lex()
        if parseValList():
            if nextToken[0] == lexer.LEXEME and nextToken[1] == "->":
                lex()
                if nextToken[0] != lexer.ID_TOKEN:
                    parseError("Expected ID after ->")
                    return False
                else:
                    lex()
                    return True
            else:
                parseError("Expected ->")
                return False
        else:
            return False
    elif nextToken[1] == "product":
        lex()
        if parseValList():
            if nextToken[0] == lexer.LEXEME and nextToken[1] == "->":
                lex()
                if nextToken[0] != lexer.ID_TOKEN:
                    parseError("Expected ID after ->")
                    return False
                else:
                    lex()
                    return True
            else:
                parseError("Expected ->")
                return False
        else:
            return False
    elif nextToken[1] == "modulo":
        lex()
        if parseVal() and parseVal():
            if nextToken[0] == lexer.LEXEME and nextToken[1] == "->":
                lex()
                if nextToken[0] != lexer.ID_TOKEN:
                    parseError("Expected ID after ->")
                    return False
                else:
                    lex()
                    return True
            else:
                parseError("Expected ->")
                return False
        else:
            return False
    elif nextToken[1] == "divide":
        lex()
        if parseVal() and parseVal():
            if nextToken[0] == lexer.LEXEME and nextToken[1] == "->":
                lex()
                if nextToken[0] != lexer.ID_TOKEN:
                    parseError("Expected ID after ->")
                    return False
                else:
                    lex()
                    return True
            else:
                parseError("Expected ->")
                return False
        else:
            return False
    elif nextToken[1] == "if":
        lex()
        if parseCmp():
            if parseVal():
                if parseProg():
                    if nextToken[0] == lexer.LEXEME and nextToken[1] == "end":
                        lex()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    elif nextToken[1] == "while":
        lex()
        if parseCmp():
            if parseVal():
                if parseProg():
                    if nextToken[0] == lexer.LEXEME and nextToken[1] == "end":
                        lex()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    # elif nextToken[1] == "do":
    #     lex()
    #     if parseCmp():
    #         if parseVal():
    #             if parseProg():
    #                 if nextToken[0] == lexer.LEXEME and nextToken[1] == "end":
    #                     lex()
    #                     return True
    #                 else:
    #                     return False
    #             else:
    #                 return False
    #         else:
    #             return False
    #     else:
    #         return False
    # elif nextToken[1] == "for":
    #     lex()
    #     if parseCmp():
    #         if parseVal():
    #             if parseProg():
    #                 if nextToken[0] == lexer.LEXEME and nextToken[1] == "end":
    #                     lex()
    #                     return True
    #                 else:
    #                     return False
    #             else:
    #                 return False
    #         else:
    #             return False
    #     else:
    #         return False
    else:
        parseError("Invalid command")
        return False



def parseProg():
    if parseCmd():
        if nextToken[0] != lexer.END_OF_INPUT and not (nextToken[0] == lexer.LEXEME and nextToken[1] == "end"):
            return parseProg()
        else:
            return True
    else:
        return False


input = list(sys.stdin.read())
lex()

if nextToken[0] == lexer.ERROR:
    print("Lex Error: ",nextToken[1])
else:
    if parseProg():
        if nextToken[0] != lexer.END_OF_INPUT:
          print("Parse Error: unrecognized trailing characters")
        else:
          print("Valid Program")

