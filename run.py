import os
from scanner import scan_file
from parser import Parser, load_tokens

def main():
    # Run scanner on all sample input files
    for filename in os.listdir('.'):
        if filename.startswith("sample_input") and filename.endswith(".txt"):
            output_scan_file = filename.replace("sample_input", "sample_output_scan")
            scan_file(filename, output_scan_file)

    # Run parser on all scanner output files
    for filename in os.listdir('.'):
        if filename.startswith("sample_output_scan") and filename.endswith(".txt"):
            parser_output_file = filename.replace("sample_output_scan", "sample_output_parse")

            # determine original scanner inputfile
            number_part = filename.replace("sample_output_scan", "").replace(".txt", "")
            if number_part == "":
                original_input_file = "sample_input.txt"
            else:
                original_input_file = f"sample_input{number_part}.txt"

            tokens = load_tokens(filename)
            parser = Parser(tokens, parser_output_file, original_input_file)
            parser.parse()

if __name__ == "__main__":
    main()
