# Parser for SimpCalc Language

# Jade Connery B. Ramos (225198)
# Rafael Angelo A. Sese (225807)
# Gian Carlo D. Valencia (226584)

import os

class ParseError(Exception):
    pass

# Parser Class
class Parser:
    def __init__(self, tokens, output_file, input_file_name):
        self.tokens = tokens
        self.index = 0
        self.current_token = tokens[0][0] if tokens else 'EndofFile'
        self.current_lexeme = tokens[0][1] if tokens else ''
        self.current_line = tokens[0][2] if tokens else 1
        self.output_file = output_file
        self.input_file_name = input_file_name

    # Logging function
    def log(self, message):
        if self.output_file:
            with open(self.output_file, 'a') as f:
                f.write(message + '\n')

    # Advance to next token
    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index][0]
            self.current_lexeme = self.tokens[self.index][1]
            self.current_line = self.tokens[self.index][2]
        else:
            self.current_token = "EndofFile"
            self.current_lexeme = ""
            self.current_line = self.tokens[-1][2] if self.tokens else 1

    # Get current line number
    def getlinenum(self):
        return self.current_line

    # Match expected token
    def match(self, expected):
        if self.current_token == expected:
            self.advance()
        else:
            raise ParseError(f"Parse Error: {expected} expected. (Error at Line {self.getlinenum()})")

    # Main parse function
    def parse(self):
        if self.output_file:
            open(self.output_file, 'w').close()  # clear file
        try:
            self.Prg()
            if self.current_token == "EndofFile":
                self.log(f"{self.input_file_name} is a valid SimpCalc program")
            else:
                raise ParseError(f"Parse Error: Unexpected tokens after program end. (Error at Line {self.getlinenum()})")
        except ParseError as pe:
            self.log(str(pe))

    # Grammar Productions

    # Prg → Blk EndOfFile
    def Prg(self):
        self.Blk()
        self.match("EndofFile")

    # Blk → Stm Blk | ϵ
    def Blk(self):
        while self.current_token in ["Identifier", "Print", "If"]:
            self.Stm()

    # Stm → Identifier := Exp ; | PRINT(Arg Argfollow) ; | IF Cnd : Blk Iffollow
    def Stm(self):
        if self.current_token == "Identifier":
            self.match("Identifier")
            self.match("Assign")
            self.Exp()
            self.match("Semicolon")
            self.log("Assignment Statement Recognized")

        elif self.current_token == "Print":
            self.match("Print")
            self.match("LeftParen")
            self.Arg()
            self.Argfollow()
            self.match("RightParen")
            self.match("Semicolon")
            self.log("Print Statement Recognized")

        elif self.current_token == "If":
            self.match("If")
            self.log("If Statement Begins")
            self.Cnd()
            self.match("Colon")
            self.Blk()
            self.Iffollow()
            self.log("If Statement Ends")

        else:
            raise ParseError(f"Parse Error: Statement expected. (Error at Line {self.getlinenum()})")

    # Argfollow → , Arg Argfollow | ϵ
    def Argfollow(self):
        while self.current_token == "Comma":
            self.match("Comma")
            self.Arg()

    # Arg → String | Exp
    def Arg(self):
        if self.current_token == "String":
            self.match("String")
        else:
            self.Exp()

    # Iffollow → ENDIF ; | ELSE Blk ENDIF ;
    def Iffollow(self):
        if self.current_token == "Endif":
            self.match("Endif")
            self.match("Semicolon")
        elif self.current_token == "Else":
            self.match("Else")
            self.Blk()
            self.match("Endif")
            self.match("Semicolon")
        else:
            raise ParseError(f"Parse Error: Incomplete if Statement. (Error at Line {self.getlinenum()})")

    # Exp → Trm Trmfollow
    def Exp(self):
        self.Trm()
        self.Trmfollow()

    # Trmfollow → + Trm Trmfollow | - Trm Trmfollow | ϵ
    def Trmfollow(self):
        while self.current_token in ["Plus", "Minus"]:
            self.match(self.current_token)
            self.Trm()

    # Trm → Fac Facfollow
    def Trm(self):
        self.Fac()
        self.Facfollow()

    # Facfollow → * Fac Facfollow | / Fac Facfollow | ϵ
    def Facfollow(self):
        while self.current_token in ["Multiply", "Divide"]:
            self.match(self.current_token)
            self.Fac()

    # Fac → Lit Litfollow
    def Fac(self):
        self.Lit()
        self.Litfollow()

    # Litfollow → ** Lit Litfollow | ϵ
    def Litfollow(self):
        while self.current_token == "Raise":
            self.match("Raise")
            self.Lit()

    # Lit → -Val | Val
    def Lit(self):
        if self.current_token == "Minus":
            self.match("Minus")
            self.Val()
        else:
            self.Val()

    # Val → Identifier | Number | Sqrt(Exp) | (Exp)
    def Val(self):
        if self.current_token == "Identifier":
            self.match("Identifier")
        elif self.current_token == "Number":
            self.match("Number")
        elif self.current_token == "Sqrt":
            self.match("Sqrt")
            self.match("LeftParen")
            self.Exp()
            self.match("RightParen")
        elif self.current_token == "LeftParen":
            self.match("LeftParen")
            self.Exp()
            self.match("RightParen")
        else:
            raise ParseError(f"Parse Error: Symbol expected. (Error at Line {self.getlinenum()})")

    # Cnd → Exp Rel Exp
    def Cnd(self):
        self.Exp()
        if self.current_token in ["LessThan", "Equal", "GreaterThan", "LTEqual", "GTEqual", "NotEqual"]:
            self.Rel()
            self.Exp()
        else:
            raise ParseError(f"Parse Error: Missing relational operator. (Error at Line {self.getlinenum()})")

    # Rel → < | = | > | <= | >= | !=
    def Rel(self):
        if self.current_token in ["LessThan", "Equal", "GreaterThan", "LTEqual", "GTEqual", "NotEqual"]:
            self.advance()
        else:
            raise ParseError(f"Parse Error: Relational operator expected. (Error at Line {self.getlinenum()})")

# Load tokens from scanner output file
def load_tokens(filename):
    tokens = []
    with open(filename, 'r') as file:
        line_num = 1
        for line in file:
            parts = line.rstrip('\n').strip().split()
            if not parts:
                line_num += 1
                continue
            if len(parts) == 1:
                tokens.append((parts[0], "", line_num))
            else:
                token_type = parts[0]
                lexeme = ' '.join(parts[1:])
                tokens.append((token_type, lexeme, line_num))
            line_num += 1
    return tokens


# main function
if __name__ == "__main__":
    found = False

    for filename in os.listdir('.'):
        if filename.startswith("sample_output_scan") and filename.endswith(".txt"):

            # Determine original scanner input filename
            parser_output_file = filename.replace("sample_output_scan", "sample_output_parse")
            number_part = filename.replace("sample_output_scan", "").replace(".txt", "")

            if number_part == "":
                original_input_file = "sample_input.txt"
            else:
                original_input_file = f"sample_input{number_part}.txt"

            tokens = load_tokens(filename)

            # Create parser and pass the original input filename
            parser = Parser(tokens, parser_output_file, original_input_file)
            parser.parse()

            print(f"Parsed {filename}, Output: {parser_output_file}")
            found = True

    if not found:
        print("No scanner output files found matching pattern 'sample_output_scan*.txt'.")
    print("Parsing completed.")
