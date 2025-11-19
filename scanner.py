# Scanner for SimpCalc Language

# Jade Connery B. Ramos (225198)
# Rafael Angelo A. Sese (225807)
# Gian Carlo D. Valencia (226584)

import os

# Keywords mapping
KEYWORDS = {
    "PRINT": "Print",
    "IF": "If",
    "ELSE": "Else",
    "ENDIF": "Endif",
    "SQRT": "Sqrt",
    "AND": "And",
    "OR": "Or",
    "NOT": "Not"
}

# Scanner Class
class Scanner:
    def __init__(self, input_path):
        with open(input_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
        self.i = 0
        self.n = len(self.text)
        self.buffer = []
        self.line = 1

    # Utility function to add token to buffer
    def add(self, type_, lexeme):
        token = f"{type_.ljust(17)}{lexeme}"
        return token

    # Get current line number
    def getlinenum(self):
        return self.line

    # Add error message to buffer
    def add_error(self, msg):
        lineno = self.getlinenum()
        full = f"{msg}(Error at Line {lineno})"
        self.buffer.append(full)
        self.buffer.append("Error")

    # get next token
    def gettoken(self):
        if self.buffer:
            return self.buffer.pop(0)

        while self.i < self.n:
            c = self.text[self.i]

            # whitespace + line counter
            if c.isspace():
                if c == '\n':
                    self.line += 1
                self.i += 1
                continue


            # Comments
            if c == '/' and self.i + 1 < self.n and self.text[self.i+1] == '/':
                self.i += 2
                # skip to end of line
                while self.i < self.n and self.text[self.i] != '\n':
                    self.i += 1
                continue

            # Strings
            if c == '"':
                start = self.i
                self.i += 1
                closed = False
                # scan until closing quote
                while self.i < self.n:
                    if self.text[self.i] == '"':
                        self.i += 1
                        closed = True
                        break
                    if self.text[self.i] == '\n':
                        self.add_error("Lexical Error: Unterminated string ")
                        return self.gettoken()
                    self.i += 1
                if closed:
                    return self.add("String", self.text[start:self.i])

            # Identifiers
            if c.isalpha() or c == '_':
                start = self.i
                self.i += 1

                # continue while alphanumeric or underscore
                while self.i < self.n and (self.text[self.i].isalnum() or self.text[self.i] == '_'):
                    self.i += 1
                lex = self.text[start:self.i]

                # Check if keyword
                if lex in KEYWORDS:
                    return self.add(KEYWORDS[lex], lex)
                else:
                    return self.add("Identifier", lex)

            # Numbers
            if c.isdigit():
                start = self.i
                while self.i < self.n and self.text[self.i].isdigit():
                    self.i += 1

                # Fraction
                if self.i < self.n and self.text[self.i] == '.':
                    if self.i + 1 < self.n and self.text[self.i+1].isdigit():
                        self.i += 1
                        while self.i < self.n and self.text[self.i].isdigit():
                            self.i += 1
                    else:
                        self.i += 2
                        self.add_error("Lexical Error: Invalid number format ")
                        return self.gettoken()

                # Exponent
                if self.i < self.n and self.text[self.i] in 'eE':
                    j = self.i + 1
                    if j < self.n and self.text[j] in '+-':
                        j += 1
                    if j < self.n and self.text[j].isdigit():
                        j += 1
                        while j < self.n and self.text[j].isdigit():
                            j += 1
                        token = self.text[start:j]
                        self.i = j
                        return self.add("Number", token)
                    else:
                        if j < self.n and self.text[j].isalpha():
                            j += 1
                        self.i = j
                        self.add_error("Lexical Error: Invalid number format ")
                        return self.gettoken()

                lex = self.text[start:self.i]
                return self.add("Number", lex)

            # Leading dot
            if c == '.':
                self.i += 1
                self.add_error("Lexical Error: Illegal character/character sequence ")
                return self.gettoken()

            # Multi-character operators
            multi_tokens = {
                ':=': "Assign",
                '**': "Raise",
                '<=': "LTEqual",
                '>=': "GTEqual",
                '!=': "NotEqual"
            }
            # Check multi-character operators
            for op, typ in multi_tokens.items():
                if self.text[self.i:self.i+len(op)] == op:
                    self.i += len(op)
                    return self.add(typ, op)

            # Single-character tokens
            single_tokens = {
                ';': "Semicolon",
                ':': "Colon",
                ',': "Comma",
                '(': "LeftParen",
                ')': "RightParen",
                '+': "Plus",
                '-': "Minus",
                '*': "Multiply",
                '/': "Divide",
                '<': "LessThan",
                '=': "Equal",
                '>': "GreaterThan",
                '_': "Identifier"
            }

            if c in single_tokens:
                self.i += 1
                if c == '_':
                    return self.add("Identifier", "_")
                return self.add(single_tokens[c], c)

            # Unknown character
            self.i += 2
            self.add_error("Lexical Error: Illegal character/character sequence ")
            return self.gettoken()

        # End of file
        return self.add("EndofFile", "")

# Scan input file and write tokens to output file
def scan_file(input_path, output_path):
    scanner = Scanner(input_path)
    tokens = []
    while True:
        token = scanner.gettoken()
        tokens.append(token)
        if token.startswith("EndofFile"):
            break
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(tokens))

# main function
def main():
    found = False
    # Scan all sample_input*.txt files
    for filename in os.listdir('.'):
        if filename.startswith("sample_input") and filename.endswith(".txt"):
            output_name = filename.replace("sample_input", "sample_output_scan")
            scan_file(filename, output_name)
            found = True
            print(f"Scanned {filename}, Output: {output_name}")

    # If no files found
    if not found:
        print("No sample_input*.txt files found.")
    print("Scanning completed.")


if __name__ == "__main__":
    main()
