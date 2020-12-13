import yacc
from toy import tokens, lexer
import logging
import csv


# <----- GRAMMAR ----->
def p_Program(p):
    '''
    Program : Declaration Program
            | Declaration
    '''


def p_Declaration(p):
    '''
    Declaration : VariableDeclaration
                | FunctionDeclaration
                | ClassDeclaration
                | InterfaceDeclaration
    '''


def p_VariableDeclaration(p):
    '''
    VariableDeclaration : Variable SEMICOLON
    '''


def p_Variable(p):
    '''
    Variable : Type ID
             | ID ID
    '''


def p_Type(p):
    '''
    Type : INT
         | DOUBLE
         | BOOLEAN
         | STRING
         | Type LEFTBRACKET RIGHTBRACKET
         | ID LEFTBRACKET RIGHTBRACKET
    '''


def p_FunctionDeclaration(p):
    '''
    FunctionDeclaration : Type ID LEFTPAREN Formals RIGHTPAREN StatementBlock
                        | Type ID LEFTPAREN RIGHTPAREN StatementBlock
                        | ID ID LEFTPAREN Formals RIGHTPAREN StatementBlock
                        | ID ID LEFTPAREN RIGHTPAREN StatementBlock
                        | VOID ID LEFTPAREN Formals RIGHTPAREN StatementBlock
                        | VOID ID LEFTPAREN RIGHTPAREN StatementBlock
    '''


def p_Formals(p):
    '''
    Formals : Variable COMMA Formals
            | Variable
    '''


def p_ClassDeclaration(p):
    '''
    ClassDeclaration : CLASS ID EXTENDS ID LEFTBRACE Fields RIGHTBRACE
                     | CLASS ID IMPLEMENTS IdList LEFTBRACE Fields RIGHTBRACE
                     | CLASS ID EXTENDS ID IMPLEMENTS IdList LEFTBRACE Fields RIGHTBRACE
                     | CLASS ID LEFTBRACE Fields RIGHTBRACE
                     | CLASS ID EXTENDS ID LEFTBRACE RIGHTBRACE
                     | CLASS ID IMPLEMENTS IdList LEFTBRACE RIGHTBRACE
                     | CLASS ID EXTENDS ID IMPLEMENTS IdList LEFTBRACE RIGHTBRACE
                     | CLASS ID LEFTBRACE RIGHTBRACE
    '''


def p_IdList(p):
    '''
    IdList : ID COMMA IdList
           | ID
    '''


def p_Fields(p):
    '''
    Fields : Field Fields
           | Field
    '''


def p_Field(p):
    '''
    Field : VariableDeclaration
          | FunctionDeclaration
    '''


def p_InterfaceDeclaration(p):
    '''
    InterfaceDeclaration : INTERFACE ID LEFTBRACE Prototypes RIGHTBRACE
                         | INTERFACE ID LEFTBRACE RIGHTBRACE
    '''


def p_Prototypes(p):
    '''
    Prototypes : Prototype Prototypes
               | Prototype
    '''


def p_Prototype(p):
    '''
    Prototype : Type ID LEFTPAREN Formals RIGHTPAREN SEMICOLON
              | Type ID LEFTPAREN RIGHTPAREN SEMICOLON
              | ID ID LEFTPAREN Formals RIGHTPAREN SEMICOLON
              | ID ID LEFTPAREN RIGHTPAREN SEMICOLON
              | VOID ID LEFTPAREN Formals RIGHTPAREN SEMICOLON
              | VOID ID LEFTPAREN RIGHTPAREN SEMICOLON
    '''


def p_StatementBlock(p):
    '''
    StatementBlock : LEFTBRACE VaribleDeclarations Statements RIGHTBRACE
                   | LEFTBRACE Statements RIGHTBRACE
                   | LEFTBRACE VaribleDeclarations RIGHTBRACE
                   | LEFTBRACE RIGHTBRACE
    '''


def p_VaribleDeclarations(p):
    '''
    VaribleDeclarations : VariableDeclaration VaribleDeclarations
                        | VariableDeclaration
    '''


def p_Statements(p):
    '''
    Statements : Statement Statements
               | Statement
    '''


def p_Statement(p):
    '''
    Statement : Expression SEMICOLON
              | SEMICOLON
              | IfStatement
              | WhileStatement
              | ForStatement
              | BreakStatement
              | ReturnStatement
              | PrintStatement
              | StatementBlock
    '''


def p_IfStatement(p):
    '''
    IfStatement : IF LEFTPAREN Expression RIGHTPAREN Statement ELSE Statement
                | IF LEFTPAREN Expression RIGHTPAREN Statement
    '''


def p_WhileStatement(p):
    '''
    WhileStatement : WHILE LEFTPAREN Expression RIGHTPAREN Statement
    '''


def p_ForStatement(p):
    '''
    ForStatement : FOR LEFTPAREN Expression SEMICOLON Expression SEMICOLON Expression RIGHTPAREN Statement
                 | FOR LEFTPAREN SEMICOLON Expression SEMICOLON Expression RIGHTPAREN Statement
                 | FOR LEFTPAREN Expression SEMICOLON Expression SEMICOLON RIGHTPAREN Statement
                 | FOR LEFTPAREN SEMICOLON Expression SEMICOLON RIGHTPAREN Statement
    '''


def p_BreakStatement(p):
    '''
    BreakStatement : BREAK SEMICOLON
    '''


def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression SEMICOLON
                    | RETURN SEMICOLON
    '''


def p_PrintStatement(p):
    '''
    PrintStatement : PRINTLN LEFTPAREN ExpressionList RIGHTPAREN SEMICOLON
    '''


def p_ExpressionList(p):
    '''
    ExpressionList : Expression COMMA ExpressionList
                   | Expression
    '''


def p_Expression(p):
    '''
    Expression : LValue ASSIGN Expression
               | Constant
               | LValue
               | THIS
               | Call
               | LEFTPAREN Expression RIGHTPAREN
               | UminusExpression
               | Expression ArithmaticOperator Expression
               | Expression CompareOperator Expression
               | Expression LogicalOperator Expression
               | NOT Expression
               | READLN LEFTPAREN RIGHTPAREN
               | NEW LEFTPAREN ID RIGHTPAREN
               | NEWARRAY LEFTPAREN INTCONSTANT COMMA Type RIGHTPAREN
               | NEWARRAY LEFTPAREN INTCONSTANT COMMA ID RIGHTPAREN
    '''


def p_UminusExpression(p):
    '''
    UminusExpression : MINUS Expression %prec UMINUS
    '''


def p_ArithmaticOperator(p):
    '''
    ArithmaticOperator : PLUS
                       | MINUS
                       | MULT
                       | DIV
                       | MOD
    '''


def p_CompareOperator(p):
    '''
    CompareOperator : LESS
                    | LESSEQUAL
                    | GREATER
                    | GREATEREQUAL
                    | EQUAL
                    | NOTEQUAL
    '''


def p_LogicalOperator(p):
    '''
    LogicalOperator : AND
                    | OR
    '''


def p_LValue(p):
    '''
    LValue : ID
           | LValue LEFTBRACKET Expression RIGHTBRACKET
           | LValue PERIOD ID
           | ID PERIOD ID
           | ID LEFTBRACKET Expression RIGHTBRACKET
    '''


def p_Call(p):
    '''
    Call : ID LEFTPAREN Actuals RIGHTPAREN
         | ID LEFTPAREN RIGHTPAREN
         | ID PERIOD ID LEFTPAREN Actuals RIGHTPAREN
         | ID PERIOD ID LEFTPAREN RIGHTPAREN
    '''


def p_Actuals(p):
    '''
    Actuals : ExpressionList
    '''


def p_Constant(p):
    '''
    Constant : INTCONSTANT
             | DOUBLECONSTANT
             | STRINGCONSTANT
             | BOOLEANCONSTANT
             | NULL
    '''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error!")


precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NOTEQUAL'),
    ('nonassoc', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NOT', 'UMINUS'),
    ('left', 'LEFTBRACKET', 'PERIOD')
)

#---- Process the extension txt to csv ---- #
def genOutFileName(newName):
    out = ''
    for s in newName.split('.'):
        if s.find('txt') >= 0:
            out += '.csv'
        else:
            out += s
    return out

# function process values
def clean_data(d_list: list) -> dict:
    data_dict = {
        'Stack': None,
        'Action': None,
    }

    acum = ''
    for element in d_list:
        for char in element:
            acum += char
            if acum in data_dict:
                key = acum
                element = element[element.index(':') + 1:]
                element = element.rstrip('\n')
                data_dict[key] = element
        acum = ''

    # print(data_dict) # debug purposes
    return data_dict


if __name__ == '__main__':
    # craete logging object
    logging.basicConfig(
        level=logging.DEBUG,
        filename="debug_output.txt",
        filemode='w',
        format='%(filename)10s:%(lineno)4d:%(message)s'
    )
    log = logging.getLogger()
    # args for yacc debug=True,debuglog=log when debugging

    # Build the parser
    parser = yacc.yacc(debug=True, debuglog=log)

    # use code below to parse a txt file,replace
    # sample_input.txt with the name of the file
    try:
        file = open(input('\nEnter input file name: '), 'r')
    except IOError:
        print('I/O error encountered')
    if file.mode == 'r':
        debug_info = parser.parse(file.read(), lexer, debug=log)

    # ---------- beginning of output processing ------------------ #
    buffer = []
    t_data = []
    tmp_group = []
    data_list = []
    b_string = 'PARSE DEBUG START'  # beginning line
    e_string = 'PARSE DEBUG END'  # ending line of debug
    d_string = 'Done'  # last line of log file
    key_list = ['Stack', 'Action']
    nBuffer = []
    acum_tmp = ''
    sp_counter = 0
    data_dict = []

    with open('debug_output.txt', encoding='utf-8') as f:
        for line in f:
            if line != '\n':
                if b_string not in line and e_string not in line and d_string not in line:
                    line = line.replace('yacc.py:', '')
                    line = line[line.index(':') + 1:]
                    buffer.append(line)

    for line in buffer:
        for character in line:
            acum_tmp += character
            if acum_tmp in key_list:
                nBuffer.append(line)
                sp_counter += 1
                if (sp_counter % 2) == 0:
                    nBuffer.append('\n')
        acum_tmp = ''
    nBuffer.append('\n')  # takes care of trailing newline

    for line in nBuffer:
        if line == '\n':
            tmp_dict = clean_data(tmp_group)
            data_dict.append(tmp_dict)
            tmp_group = []
        else:
            tmp_group.append(line)

    # ------generate csv file-----#
    # change filename as seen fit with '.csv' extension
    # 'output.csv'
    filename = genOutFileName(file.name)
    try:
        with open(filename, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=key_list)
            file.flush()
            writer.writeheader()
            for data in data_dict:
                writer.writerow(data)
            file.close()
            print('csv file created!')
    except IOError:
        print('I/O error encountered')