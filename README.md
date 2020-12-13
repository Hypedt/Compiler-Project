# CS4110-Lexical-Analyzer
 Implement a lexical analyzer for a simple object-oriented programming language called Toy. Your program should be able to (1) translate any input Toy program into a sequence of tokens, and (2) create a symbol table using the trie structure for all keywords and user-defined identifiers.

# Python Version 3.9.0
Python 3.x is required. Preferably the same version. Also have PLY version 3.11 installed, but we included the yacc and lex file.
If the yacc.py and lex.py included doesn't work, have the PLY plugins installed

# To Run: 
#On PyCharm: 
Run toy.py for project 1. It will output to a text file.

Run parser.py for project 2
Enter in the text file you wish to test.
Test Cases starts with "p2_input##"
The "##" indicates the digits of file such as "p2_input01"

#On Python IDLE
Go to File > Open > Project Directory > Open "parser.py"
Afterwards, go to Run > Run Module (F5)

#On Terminal
Change into the project directory and then type "python parser.py"

#On other IDEs
Refer to user manual of the specific IDE to open the project and run parser.py

# Outputs:
The output files are generated as CSV files that will show the actions of the given inputs in the inputted files. 
They can be opened using excels, google sheets, etc.
They will be all generated inside the same directory as the project.
