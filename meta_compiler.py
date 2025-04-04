# meta_compiler.py

import os
class MetaLangError(Exception):
    """Meta语言错误基类"""
    def __init__(self, line_number, code, reason):
        self.line_number = line_number
        self.code = code
        self.reason = reason

    def __str__(self):
        return (
            f"\n{self.__class__.__name__} : {self.reason}\n"
            f"所在位置 : 行 {int((self.line_number+1)/2)}\n"
            f"    {self.code}\n"
            f"     ^\n"
            f"CompilerError : <{self.__class__.__name__}>\n"
        )

class Error(MetaLangError):
    """语法错误"""
    pass

class TokenType:
    CLASS = 'CLASS'
    FUNCTION = 'FUNCTION'
    MAIN = 'MAIN'
    DATA = 'DATA'  # 替换 var 和 vector 为 data
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    SEMI = ';'
    RETURN = 'RETURN'
    IDENTIFIER = 'IDENTIFIER'
    EOF = 'EOF'
    COMMA = 'COMMA'
    ASSIGN = 'ASSIGN'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    BOOL = 'BOOL'
    DOT = 'DOT'
    INPUT = 'INPUT'
    READLINE = 'READLINE'
    LBRACKET = '['
    RBRACKET = ']'
    COLON = ':'
    POINTER = 'POINTER'  # 添加指针符号 *
    DEREF = 'DEREF'      # 添加解引用符号 ^
    LT = '<'       # 小于符号，用于模板开始
    GT = '>'       # 大于符号，用于模板结束
    COMMA = ','    # 逗号，用于分隔模板参数
    POINTER = '&'
    DEREF = '^'
    OWNER = 'OWNER'  # 用于所有权转移
    REF = 'REF'      # 用于引用
    ARROW = 'ARROW'
    DELETE = 'DELETE'
    EXCLAMATION = '!'  # 添加宏标识符
    GET = 'GET'  # 添加get模板支持
    INCLUDE = 'INCLUDE'

class Token:
    def __init__(self, type_, value=None, line_number=1):
        self.type = type_
        self.value = value
        self.line_number = line_number

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line_number = 1
        self.current_char = self.text[self.pos] if self.text else None

    def error(self, msg):
        raise Error(self.line_number, "", msg)

    def advance(self):
        if self.current_char == '\n':  # 在移动前检查当前字符是否是换行符
            self.line_number += 1
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line_number += 1  # 遇到换行符时增加行数
            self.advance()

    def get_identifier(self):
        result = []
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result.append(self.current_char)
            self.advance()
        return ''.join(result)

    def get_string(self):
        result = []
        self.advance()  # 跳过引号
        while self.current_char is not None and self.current_char != '"':
            result.append(self.current_char)
            self.advance()
        if self.current_char == '"':
            self.advance()
        return ''.join(result)

    def get_number(self):
        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()
        return ''.join(result)

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LT, '<', self.line_number)
            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GT, '>', self.line_number)
            if self.current_char == '-' and self.text[self.pos:self.pos+2] == '->':
                self.advance()
                self.advance()
                return Token(TokenType.ARROW, '->', self.line_number)
            if self.current_char == 'r' and self.text[self.pos:self.pos+3] == 'ref':
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.REF, 'ref', self.line_number)
            if self.current_char == 'g' and self.text[self.pos:self.pos+3] == 'get':
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.GET, 'get', self.line_number)
            if self.current_char == 'i' and self.text[self.pos:self.pos+7] == 'include':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.INCLUDE, 'include', self.line_number)
            if self.current_char == 'd' and self.text[self.pos:self.pos+6] == 'delete':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.DELETE, 'delete', self.line_number)
            if self.current_char == '!':
                self.advance()
                return Token(TokenType.EXCLAMATION, '!', self.line_number)
            if self.current_char == 'o' and self.text[self.pos:self.pos+5] == 'owner':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.OWNER, 'owner', self.line_number)
            if self.current_char == 'c' and self.text[self.pos:self.pos+5] == 'class':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.CLASS, 'class', self.line_number)
            if self.current_char == 't' and self.text[self.pos:self.pos+4] == 'type':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.CLASS, 'class', self.line_number)
            if self.current_char == 'f' and self.text[self.pos:self.pos+8] == 'function':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.FUNCTION, 'function', self.line_number)
            if self.current_char == 'f' and self.text[self.pos:self.pos+2] == 'fn':
                self.advance()
                self.advance()
                return Token(TokenType.FUNCTION, 'function', self.line_number)
            if self.current_char == 'M' and self.text[self.pos:self.pos+3] == 'Main':
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.MAIN, 'Main', self.line_number)
            if self.current_char == 'd' and self.text[self.pos:self.pos+4] == 'data':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.DATA, 'data', self.line_number)
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line_number)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line_number)
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line_number)
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line_number)
            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMI, ';', self.line_number)
            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.line_number)
            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.line_number)
            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':', self.line_number)
            if self.current_char == 'r' and self.text[self.pos:self.pos+6] == 'return':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.RETURN, 'return', self.line_number)
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line_number)
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=', self.line_number)
            if self.current_char == '.':
                self.advance()
                return Token(TokenType.DOT, '.', self.line_number)
            if self.current_char == '"':
                string_value = self.get_string()
                return Token(TokenType.STRING, string_value, self.line_number)
            if self.current_char.isdigit():
                number_value = self.get_number()
                return Token(TokenType.NUMBER, int(number_value), self.line_number)
            if self.current_char == 't' and self.text[self.pos:self.pos+4] == 'true':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.BOOL, True, self.line_number)
            if self.current_char == 'f' and self.text[self.pos:self.pos+5] == 'false':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.BOOL, False, self.line_number)
            if self.current_char == 'i' and self.text[self.pos:self.pos+5] == 'input':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.INPUT, 'input', self.line_number)
            if self.current_char == 'r' and self.text[self.pos:self.pos+8] == 'readline':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.READLINE, 'readline', self.line_number)
            if self.current_char == '&' and self.text[self.pos:self.pos+2] != '&&':
                self.advance()
                return Token(TokenType.POINTER, '&', self.line_number)
            if self.current_char == '^':
                self.advance()
                return Token(TokenType.DEREF, '^', self.line_number)
            if self.current_char.isalpha():
                ident = self.get_identifier()
                if ident == 'Main':
                    return Token(TokenType.MAIN, 'Main', self.line_number)
                return Token(TokenType.IDENTIFIER, ident, self.line_number)
            self.error(f"无效的字符: {self.current_char}")
        return Token(TokenType.EOF)
    def get_array_dimension(self):
        """解析数组维度"""
        dimensions = []
        while self.current_char == '[':
            self.eat(TokenType.LBRACKET)
            if self.current_char == ']':  # 动态数组
                dimensions.append(None)
                self.eat(TokenType.RBRACKET)
            else:  # 固定长度数组
                if self.current_char.isdigit():
                    dim_size = self.get_number()
                    dimensions.append(int(dim_size))
                    self.eat(TokenType.RBRACKET)
                else:
                    self.error("无效的数组维度")
        return dimensions
        
MOD = []
default_code = ''  # 定义为全局变量
class Parser: 
    CPP_KEYWORDS = [
        'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto',
        'bitand', 'bitor', 'bool', 'break', 'case', 'catch',
        'char', 'char16_t', 'char32_t', 'class', 'compl', 'const',
        'constexpr', 'const_cast', 'continue', 'decltype', 'default',
        'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum',
        'explicit', 'export', 'extern', 'false', 'float', 'for',
        'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable',
        'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr',
        'operator', 'or', 'or_eq', 'private', 'protected', 'public',
        'register', 'reinterpret_cast', 'return', 'short', 'signed',
        'sizeof', 'static', 'static_assert', 'static_cast', 'struct',
        'switch', 'template', 'this', 'thread_local', 'throw', 'true',
        'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned',
        'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while',
        'xor', 'xor_eq'
    ]
    TYPE_MAP = {
        'nbr': ['short', 'int', 'long', 'long long', 'float', 'double', 'long double'],
        'int':['short','int','long','long long'],
        'int16':['short int'],
        'int32':['int'],
        'int64':['long long int'],
        'int128':['__int128'],
        'infint':['BigInt'],
        'float':['float','double','long double'],
        'float32':['float'],
        'float64':['double'],
        'float128':['long double'],
        'str': ['string', 'const char*'],
        'cstr': ['const char*'],
        'char': ['char'],
        'bool': ['bool'],
        'any': ['std::any'],
        'void': ['void'],
        'all': ['short','int','long','long long','float','double','long double','string','const char*','bool'],
        'object': ['std::any'],
        'auto': ['auto']
    }

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
        self.variables = {}  # 存储局部变量信息
        self.class_variables = {}  # 存储类成员变量信息

    def error(self, msg):
        raise Error(self.current_token.line_number, "", msg)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            self.error(f"预期 {token_type}，得到 {self.current_token.type}")

    def peek_next_token(self):
        current_pos = self.lexer.pos
        current_token = self.current_token
        next_token = self.lexer.next_token()
        self.lexer.pos = current_pos
        self.current_token = current_token
        return next_token
    def parse_include_statement(self):
        global default_code
        self.eat(TokenType.INCLUDE)
        module_name = self.current_token.value
        self.eat(TokenType.STRING)
        self.eat(TokenType.SEMI)
        if module_name == 'math.meta':
            default_code+='''
namespace math{
    long double pow(long double a,long double b){
        if(a==1) return 1;
        if(b==0) return 1;
        return std::pow(a,b);
    }
    long double sqrt(long double a,long double b){
        return std::pow(a,1.0/b);
    }
    long double log(long double a,long double b){
        return std::log(b)/std::log(a);
    }
}
'''
            MOD.append('math')
        else:
            self.error(f"不支持的模块：{module_name}")
        return f'// 导入模块 {module_name}'
    def parse_index_expression(self):
        if self.current_token.type == TokenType.NUMBER:
            index = str(self.current_token.value)
            self.eat(TokenType.NUMBER)
        elif self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            if var_name not in self.variables and var_name not in self.class_variables:
                self.error(f"使用未声明的变量: {var_name}")
            index = var_name
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error("无效的索引表达式")
        return index

    def parse_subscript_or_slice(self, var_name):
        self.eat(TokenType.LBRACKET)
        start_index = self.parse_index_expression()
        self.eat(TokenType.RBRACKET)
        
        # 检查索引是否超出数组大小
        if var_name in self.variables:
            dimensions = self.variables[var_name]['dimensions']
            if dimensions[0] is not None and int(start_index) >= dimensions[0]:
                self.error(f"数组索引 {start_index} 超出声明的大小 {dimensions[0]}")
        return f'{var_name}[{start_index}]'
    def parse_get_template(self):
        self.eat(TokenType.GET)
        self.eat(TokenType.LT)
        
        # 解析模板类型参数
        type_param = self.current_token.value
        if type_param not in self.TYPE_MAP:
            self.error(f"不支持的 get 模板类型: {type_param}")
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.GT)
        self.eat(TokenType.LPAREN)
        
        # 解析变量名
        var_name = self.current_token.value
        if var_name not in self.variables and var_name not in self.class_variables:
            self.error(f"使用未声明的变量: {var_name}")
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.RPAREN)
        
        # 获取对应的C++类型
        cpp_type = self.TYPE_MAP[type_param][0]  # 取第一个映射类型

        if cpp_type in ['void','auto']:
            self.error(f"不支持的 get 模板类型：{cpp_type}")
        
        return f"any_cast<{cpp_type}>({var_name})"
    def parse_expression(self):
        if self.current_token.type == TokenType.STRING:
            value = f'"{self.current_token.value}"'  # 确保字符串被正确包裹
            self.eat(TokenType.STRING)
            return value
        elif self.current_token.type == TokenType.NUMBER:
            value = str(self.current_token.value)
            self.eat(TokenType.NUMBER)
            return value
        elif self.current_token.type == TokenType.BOOL:
            value = "true" if self.current_token.value else "false"
            self.eat(TokenType.BOOL)
            return value
        elif self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            # 检查是否是数组下标或切片
            if self.current_token.type == TokenType.LBRACKET:
                return self.parse_subscript_or_slice(var_name)
            return var_name
        elif self.current_token.type in [TokenType.POINTER, TokenType.DEREF]:
            return self.parse_pointer_expression()
        elif self.current_token.type == TokenType.INPUT or self.current_token.type == TokenType.READLINE:
            is_inline=False
            func_name = self.current_token.value
            self.eat(self.current_token.type)
            if self.current_token.type==TokenType.EXCLAMATION:
                self.eat(TokenType.EXCLAMATION)
                is_inline=True
            self.eat(TokenType.LPAREN)
            args = []
            if self.current_token.type != TokenType.RPAREN:
                if self.current_token.type == TokenType.STRING:
                    args.append(f'"{self.current_token.value}"')
                    self.eat(TokenType.STRING)
                elif self.current_token.type == TokenType.IDENTIFIER:
                    var_name = self.current_token.value
                    if var_name not in self.variables and var_name not in self.class_variables:
                        self.error(f"使用未声明的变量: {var_name}")
                    args.append(var_name)
                    self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.RPAREN)
            if is_inline:
                if func_name=="input":
                    return self.generate_inline_input(args)
                elif func_name=="readline":
                    return self.generate_inline_readline(args)
            else:
                return f'{func_name}({",".join(args)})'
        elif self.current_token.type == TokenType.IDENTIFIER and self.peek_next_token().type == TokenType.LPAREN:
            func_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LPAREN)
            args = []
            while self.current_token.type != TokenType.RPAREN:
                if self.current_token.type == TokenType.STRING:
                    args.append(f'"{self.current_token.value}"')
                    self.eat(TokenType.STRING)
                elif self.current_token.type == TokenType.NUMBER:
                    args.append(str(self.current_token.value))
                    self.eat(TokenType.NUMBER)
                elif self.current_token.type == TokenType.BOOL:
                    args.append("true" if self.current_token.value else "false")
                    self.eat(TokenType.BOOL)
                elif self.current_token.type == TokenType.IDENTIFIER:
                    if self.current_token.value not in self.variables and self.current_token.value not in self.class_variables:
                        self.error(f"使用未声明的变量: {self.current_token.value}")
                    args.append(self.current_token.value)
                    self.eat(TokenType.IDENTIFIER)
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RPAREN)
            return f'{func_name}({", ".join(args)})'
        elif self.current_token.type == TokenType.GET:
            return self.parse_get_template()
        else:
            self.error("不支持的表达式")

    def parse_print_statement(self):
        is_inline=False
        self.eat(TokenType.IDENTIFIER)  # 吃掉 print
        if self.current_token.type == TokenType.EXCLAMATION:
            self.eat(TokenType.EXCLAMATION)
            is_inline=True
        self.eat(TokenType.LPAREN)
        args = []
        while self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.GET:
                return self.parse_get_template()
            elif self.current_token.type == TokenType.STRING:
                args.append(f'"{self.current_token.value}"')
                self.eat(TokenType.STRING)
            elif self.current_token.type == TokenType.NUMBER:
                args.append(str(self.current_token.value))
                self.eat(TokenType.NUMBER)
            elif self.current_token.type == TokenType.BOOL:
                args.append("true" if self.current_token.value else "false")
                self.eat(TokenType.BOOL)
            elif self.current_token.type == TokenType.IDENTIFIER:
                var_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                # 检查是否是数组下标或切片
                if self.current_token.type == TokenType.LBRACKET:
                    args.append(self.parse_subscript_or_slice(var_name))
                elif var_name in self.variables:
                    args.append(var_name)
                elif var_name in self.class_variables:
                    args.append(f"this->{var_name}")
                else:
                    self.error(f"使用未声明的变量: {var_name}")
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMI)
        if is_inline:
            return self.generate_inline_print(args)
        else:
            return f"cout << {' << '.join(args)} << endl;"
    def check_type_compatibility(self, var_name, value_type, is_class_variable=False):
        variables = self.class_variables if is_class_variable else self.variables
        if var_name not in variables:
            return False
        
        var_type = variables[var_name]['type']
        
        if 'variant' in var_type:
            type_list = var_type.split('<')[1].split('>')[0].split(',')
            type_list = [t.strip() for t in type_list]
            return value_type in type_list
        
        if var_type == 'std::any':
            return True
        
        return var_type == value_type

    def parse_data_declaration(self, is_class_variable=False):
        self.eat(TokenType.DATA)
        
        # 检查是否是模板化数据类型
        if self.current_token.type == TokenType.LT:
            self.eat(TokenType.LT)
            template_params = []
            while self.current_token.type != TokenType.GT:
                if self.current_token.type == TokenType.IDENTIFIER:
                    param = self.current_token.value
                    if param not in self.TYPE_MAP:
                        self.error(f"未知的模板类型: {param}")
                    template_params.append(param)
                    self.eat(TokenType.IDENTIFIER)
                    if self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                else:
                    self.error("模板参数必须是标识符")
            self.eat(TokenType.GT)
            
            # 将模板参数映射到实际的C++类型
            cpp_types = []
            for param in template_params:
                cpp_types.extend(self.TYPE_MAP[param])
            
            # 生成variant类型字符串
            if len(cpp_types) == 1:
                base_type = cpp_types[0]  # 单一类型直接使用
            else:
                base_type = f"std::variant<{', '.join(cpp_types)}>"
        else:
            base_type = "std::any"  # 默认为 std::any
        
        # 获取数组维度
        dimensions = self.get_array_dimension()
        
        # 获取变量名列表
        var_names = []
        while self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            var_names.append(var_name)
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            else:
                break
        
        # 根据维度生成数组类型
        array_type = base_type
        for dim in dimensions:
            if dim is None:  # 动态数组
                array_type = f"std::vector<{array_type}>"
            else:  # 固定长度数组
                array_type = f"std::array<{array_type}, {dim}>"
        
        # 存储变量信息
        declarations = []
        for var_name in var_names:
            if var_name in self.CPP_KEYWORDS:
                var_name = f"{var_name}_"
            
            if is_class_variable:
                self.class_variables[var_name] = {'type': array_type, 'dimensions': dimensions, 'owner': True, "borrowed_by": None}
            else:
                self.variables[var_name] = {'type': array_type, 'dimensions': dimensions, 'owner': True, "borrowed_by": None}
            
            # 检查是否有赋值操作
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                expr = self.parse_expression()
                self.eat(TokenType.SEMI)
                declarations.append(f"{array_type} {var_name} = {expr};")
            else:
                self.eat(TokenType.SEMI)
                # 如果是动态数组，直接声明
                if dimensions and dimensions[0] is None:
                    declarations.append(f"{array_type} {var_name};")
                # 如果是固定长度数组，初始化为空
                elif dimensions and dimensions[0] is not None:
                    declarations.append(f"{array_type} {var_name} = {{}};")
                # 如果不是数组，声明变量
                else:
                    declarations.append(f"{array_type} {var_name};")
        
        return "\n".join(declarations)

    def parse_ref(self):
        self.eat(TokenType.REF)
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)  # 吃掉等号
        source_var = self.parse_expression()  # 解析右侧表达式
        self.eat(TokenType.SEMI)  # 吃掉分号

        # 检查变量是否存在
        if source_var not in self.variables:
            self.error(f"使用未声明的变量: {source_var}")

        # 检查是否可以借用
        if not self.variables[source_var]['owner']:
            self.error(f"变量 {source_var} 不拥有所有权，无法借用")

        # 更新借用信息
        self.variables[var_name] = {
            'type': self.variables[source_var]['type'],
            'dimensions': self.variables[source_var]['dimensions'],
            'owner': False,  # 借用变量不拥有所有权
            'borrowed_by': source_var  # 记录借用来源
        }

        return f"auto& {var_name} = {source_var};"

    def parse_delete(self):
        self.eat(TokenType.DELETE)
        if self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            self.eat(TokenType.RBRACKET)
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.SEMI)
            return self.delete_array(var_name)
        else:
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.SEMI)
            return self.delete_variable(var_name)
        
    def delete_variable(self, var_name):
        if var_name not in self.variables:
            self.error(f"使用未声明的变量: {var_name}")

        var_info = self.variables[var_name]
        if var_info['deleted']:
            self.error(f"变量 {var_name} 已被销毁，无法再次销毁")

        # 如果变量拥有所有权，销毁所有借用
        if var_info['owner']:
            for var in self.variables.values():
                if var['borrowed_by'] == var_name:
                    var['deleted'] = True

        # 销毁变量
        self.variables[var_name]['deleted'] = True
        return f"// 销毁变量 {var_name}"
    
    def delete_array(self, var_name):
        if var_name not in self.variables:
            self.error(f"使用未声明的变量: {var_name}")

        var_info = self.variables[var_name]
        if var_info['deleted']:
            self.error(f"数组 {var_name} 已被销毁，无法再次销毁")

        # 如果数组拥有所有权，销毁所有借用
        if var_info['owner']:
            for var in self.variables.values():
                if var['borrowed_by'] == var_name:
                    var['deleted'] = True

        # 销毁数组
        self.variables[var_name]['deleted'] = True
        return f"// 销毁数组 {var_name}"

    def parse_owner(self):
        self.eat(TokenType.OWNER)
        source_var = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ARROW)  # 吃掉箭头
        target_var = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.SEMI)  # 吃掉分号

        # 检查变量是否存在
        if source_var not in self.variables:
            self.error(f"使用未声明的变量: {source_var}")
        if target_var not in self.variables:
            self.error(f"使用未声明的变量: {target_var}")

        # 检查所有权规则
        if not self.variables[source_var]['owner']:
            self.error(f"变量 {source_var} 不拥有所有权，无法执行所有权转移")
        if self.variables[target_var]['owner']:
            self.error(f"变量 {target_var} 拥有所有权，无法作为借用目标")
        if self.variables[target_var]['borrowed_by'] != source_var:
            self.error(f"变量 {target_var} 不是 {source_var} 的借用")

        # 更新所有权信息
        self.variables[source_var]['owner'] = False
        self.variables[source_var]['borrowed_by'] = None
        self.variables[target_var]['owner'] = True
        self.variables[target_var]['borrowed_by'] = source_var

        return f"// 所有权从 {source_var} 转移到 {target_var}"
    
    def parse_pointer_expression(self):
        if self.current_token.type == TokenType.POINTER:
            self.eat(TokenType.POINTER)
            var_name = self.current_token.value
            if var_name not in self.variables and var_name not in self.class_variables:
                self.error(f"使用未声明的变量: {var_name}")
            self.eat(TokenType.IDENTIFIER)
            return f"&{var_name}"
        elif self.current_token.type == TokenType.DEREF:
            self.eat(TokenType.DEREF)
            var_name = self.current_token.value
            if var_name not in self.variables and var_name not in self.class_variables:
                self.error(f"使用未声明的变量: {var_name}")
            self.eat(TokenType.IDENTIFIER)
            return f"*{var_name}"
        else:
            self.error("无效的指针操作")

    def parse_template_parameters(self):
        self.eat(TokenType.LT)
        params = []
        while self.current_token.type != TokenType.GT:
            if self.current_token.type == TokenType.IDENTIFIER:
                param = self.current_token.value
                if param not in self.TYPE_MAP:
                    self.error(f"未知的模板类型: {param}")
                params.append(param)
                self.eat(TokenType.IDENTIFIER)
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            else:
                self.error("模板参数必须是标识符")
        self.eat(TokenType.GT)
        return params

    def parse(self):
        statements = []
        
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.CLASS:
                class_decl = self.parse_class_declaration()
                statements.append({
                    'type': 'class',
                    'data': class_decl
                })
            elif self.current_token.type == TokenType.DATA:
                statements.append(self.parse_data_declaration())
            elif self.current_token.type == TokenType.DELETE:
                statements.append(self.parse_delete())
            elif self.current_token.type == TokenType.INCLUDE:
                statements.append(self.parse_include_statement())
            else:
                self.error("无效的语句")
        
        return statements

    def parse_class_declaration(self):
        self.eat(TokenType.CLASS)
        class_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LBRACE)
        
        class_vars = []
        functions = []
        
        while self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.DATA:
                class_vars.append(self.parse_data_declaration(is_class_variable=True))
            elif self.current_token.type == TokenType.FUNCTION:
                func = self.parse_function_declaration()
                functions.append(func)
            else:
                self.error("类中只能包含变量声明和函数声明")
        
        self.eat(TokenType.RBRACE)
        
        return {
            'name': class_name,
            'variables': class_vars,
            'functions': functions
        }

    def parse_function_declaration(self):
        self.eat(TokenType.FUNCTION)
        func_name = self.current_token.value
        if self.current_token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
        elif self.current_token.type == TokenType.MAIN:
            self.eat(TokenType.MAIN)
        self.eat(TokenType.LPAREN)
        
        params = []
        while self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.IDENTIFIER:
                param_name = self.current_token.value
                params.append(param_name)
                self.eat(TokenType.IDENTIFIER)
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            else:
                self.error("函数参数必须是标识符")
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        previous_variables = self.variables
        self.variables = {}
        
        statements = []
        while self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.DATA:
                statements.append(self.parse_data_declaration())
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == 'print':
                statements.append(self.parse_print_statement())
            elif self.current_token.type == TokenType.IDENTIFIER and self.peek_next_token().type == TokenType.ASSIGN:
                statements.append(self.parse_assignment_statement())
            elif self.current_token.type == TokenType.IDENTIFIER and self.peek_next_token().type == TokenType.LPAREN:
                func_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                args = []
                while self.current_token.type != TokenType.RPAREN:
                    if self.current_token.type == TokenType.STRING:
                        args.append(f'"{self.current_token.value}"')
                        self.eat(TokenType.STRING)
                    elif self.current_token.type == TokenType.NUMBER:
                        args.append(str(self.current_token.value))
                        self.eat(TokenType.NUMBER)
                    elif self.current_token.type == TokenType.BOOL:
                        args.append("true" if self.current_token.value else "false")
                        self.eat(TokenType.BOOL)
                    elif self.current_token.type == TokenType.IDENTIFIER:
                        if self.current_token.value not in self.variables and self.current_token.value not in self.class_variables:
                            self.error(f"使用未声明的变量: {self.current_token.value}")
                        args.append(self.current_token.value)
                        self.eat(TokenType.IDENTIFIER)
                    if self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                self.eat(TokenType.RPAREN)
                self.eat(TokenType.SEMI)
                statements.append(f'{func_name}({", ".join(args)});')
            elif self.current_token.type == TokenType.RETURN:
                self.eat(TokenType.RETURN)
                if self.current_token.type == TokenType.SEMI:
                    self.eat(TokenType.SEMI)
                    statements.append("return;")
                else:
                    expr = self.parse_expression()
                    self.eat(TokenType.SEMI)
                    statements.append(f"return {expr};")
            elif self.current_token.type == TokenType.REF:
                statements.append(self.parse_ref())
            elif self.current_token.type == TokenType.OWNER:
                statements.append(self.parse_owner())
            elif self.current_token.type == TokenType.DELETE:
                statements.append(self.parse_delete())
            else:
                self.error("无效的语句")
        
        self.eat(TokenType.RBRACE)
        self.variables = previous_variables
        
        return {
            'name': func_name,
            'params': params,
            'body': statements
        }

    def parse_assignment_statement(self):
        var_name = self.current_token.value
        if var_name not in self.variables and var_name not in self.class_variables:
            self.error(f"使用未声明的变量: {var_name}")
        
        self.eat(TokenType.IDENTIFIER)
        
        # 检查是否是数组下标赋值
        if self.current_token.type == TokenType.LBRACKET:
            # 解析数组下标表达式
            subscript = self.parse_subscript_or_slice(var_name)
            self.eat(TokenType.ASSIGN)
            # 解析赋值表达式
            expr = self.parse_expression()
            self.eat(TokenType.SEMI)
            return f"{subscript} = {expr};"
        else:
            # 普通变量赋值
            self.eat(TokenType.ASSIGN)
            expr = self.parse_expression()
            self.eat(TokenType.SEMI)
            prefix = "this->" if var_name in self.class_variables else ""
            return f"{prefix}{var_name} = {expr};"
        
    def parse_template_parameters(self):
        """解析模板参数"""
        self.eat(TokenType.LT)
        params = []
        while self.current_token.type != TokenType.GT:
            if self.current_token.type == TokenType.IDENTIFIER:
                param = self.current_token.value
                if param not in self.TYPE_MAP:
                    self.error(f"未知的模板类型: {param}")
                params.append(param)
                self.eat(TokenType.IDENTIFIER)
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            else:
                self.error("模板参数必须是标识符")
        self.eat(TokenType.GT)
        return params
    def get_array_dimension(self):
        """解析数组维度"""
        dimensions = []
        while self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            if self.current_token.type == TokenType.RBRACKET:  # 动态数组
                dimensions.append(None)
                self.eat(TokenType.RBRACKET)
            else:  # 固定长度数组
                if self.current_token.type == TokenType.NUMBER:
                    dim_size = self.current_token.value
                    dimensions.append(dim_size)
                    self.eat(TokenType.NUMBER)
                else:
                    self.error("无效的数组维度")
                self.eat(TokenType.RBRACKET)
        return dimensions
    def parse_macro(self):
        self.eat(TokenType.EXCLAMATION)
        macro_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        
        args = []
        while self.current_token.type != TokenType.RPAREN:
            args.append(self.parse_expression())
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        
        if macro_name == 'print':
            return self.generate_inline_print(args)
        elif macro_name == 'input':
            return self.generate_inline_input(args)
        elif macro_name == 'readline':
            return self.generate_inline_readline(args)
        else:
            self.error(f"未知的宏: {macro_name}")

    def generate_inline_print(self, args):
        return f"cout << {' << '.join(args)} << endl;"

    def generate_inline_input(self, args):
        prompt = args[0] if args else '""'
        return f"\n    cout << {prompt}; \n    getline(cin, {self.current_token.value});"

    def generate_inline_readline(self, args):
        return f"string {self.current_token.value}; getline(cin, {self.current_token.value});"

    def parse_statement(self):
        if self.current_token.type == TokenType.EXCLAMATION:
            return self.parse_macro()
        elif self.current_token.type == TokenType.IDENTIFIER:
            if self.peek_next_token().type == TokenType.ASSIGN:
                return self.parse_assignment_statement()
            elif self.peek_next_token().type == TokenType.LPAREN:
                return self.parse_function_call()
            elif self.peek_next_token().type == TokenType.LBRACKET:
                return self.parse_subscript_or_slice()
            else:
                self.error(f"未知的标识符使用: {self.current_token.value}")
        elif self.current_token.type == TokenType.DATA:
            return self.parse_data_declaration()
        elif self.current_token.type == TokenType.DELETE:
            return self.parse_delete()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.current_token.type == TokenType.REF:
            return self.parse_ref()
        elif self.current_token.type == TokenType.OWNER:
            return self.parse_owner()
        else:
            self.error(f"无效的语句: {self.current_token.type}")

def generate_cpp_code(statements):
    cpp_code = """\
#include <iostream>
#include <any>
#include <typeinfo>
#include <map>
#include <string>
#include <variant>
#include <vector>
#include <utility>
#include <iomanip>
#include <stdexcept>
#include <sstream>
#include <array>
#include <cmath>
#include <string>
#include <algorithm>

using namespace std;
"""
    cpp_code+=default_code
    cpp_code+="""
class BigInt {
private:
    std::vector<int> digits;
    bool is_negative = false;

public:
    // 构造函数
    BigInt() {}
    BigInt(const std::string& s) { from_string(s); }
    BigInt(long long n) { from_string(std::to_string(n)); }

    // 从字符串初始化
    void from_string(const std::string& s) {
        digits.clear();
        is_negative = (s[0] == '-');
        
        for (int i = s.size() - 1; i >= (is_negative ? 1 : 0); --i) {
            if (isdigit(s[i])) {
                digits.push_back(s[i] - '0');
            }
        }
        normalize();
    }

    // 移除前导零
    void normalize() {
        while (digits.size() > 1 && digits.back() == 0) {
            digits.pop_back();
        }
        if (digits.empty()) {
            digits.push_back(0);
        }
    }

    // 转换为字符串
    std::string to_string() const {
        std::string s;
        if (is_negative && !(digits.size() == 1 && digits[0] == 0)) {
            s += '-';
        }
        for (int i = digits.size() - 1; i >= 0; --i) {
            s += std::to_string(digits[i]);
        }
        return s;
    }

    // 加法
    BigInt operator+(const BigInt& other) const {
        if (is_negative != other.is_negative) {
            return *this - (-other);
        }
        
        BigInt result;
        result.is_negative = is_negative;
        
        int carry = 0;
        int max_len = std::max(digits.size(), other.digits.size());
        
        for (int i = 0; i < max_len || carry; ++i) {
            int sum = carry;
            if (i < digits.size()) sum += digits[i];
            if (i < other.digits.size()) sum += other.digits[i];
            
            result.digits.push_back(sum % 10);
            carry = sum / 10;
        }
        
        return result;
    }

    // 减法
    BigInt operator-(const BigInt& other) const {
        if (is_negative != other.is_negative) {
            return *this + (-other);
        }
        if (abs() < other.abs()) {
            return -(other - *this);
        }
        
        BigInt result;
        result.is_negative = is_negative;
        
        int borrow = 0;
        for (int i = 0; i < digits.size(); ++i) {
            int diff = digits[i] - borrow;
            if (i < other.digits.size()) diff -= other.digits[i];
            
            if (diff < 0) {
                diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            
            result.digits.push_back(diff);
        }
        
        result.normalize();
        return result;
    }

    // 取负
    BigInt operator-() const {
        BigInt result = *this;
        result.is_negative = !is_negative;
        return result;
    }

    // 绝对值
    BigInt abs() const {
        BigInt result = *this;
        result.is_negative = false;
        return result;
    }

    // 比较运算符
    bool operator<(const BigInt& other) const {
        if (is_negative != other.is_negative) {
            return is_negative;
        }
        if (digits.size() != other.digits.size()) {
            return (digits.size() < other.digits.size()) ^ is_negative;
        }
        for (int i = digits.size() - 1; i >= 0; --i) {
            if (digits[i] != other.digits[i]) {
                return (digits[i] < other.digits[i]) ^ is_negative;
            }
        }
        return false;
    }

    bool operator==(const BigInt& other) const {
        return is_negative == other.is_negative && digits == other.digits;
    }

    bool operator!=(const BigInt& other) const { return !(*this == other); }
    bool operator<=(const BigInt& other) const { return *this < other || *this == other; }
    bool operator>(const BigInt& other) const { return !(*this <= other); }
    bool operator>=(const BigInt& other) const { return !(*this < other); }

    // 输出运算符
    friend std::ostream& operator<<(std::ostream& os, const BigInt& num) {
        return os << num.to_string();
    }
};
// 先声明 operator<< 以便后续使用
ostream& operator<<(ostream& os, const any& value);

// 自定义异常类
class MetaRuntimeError : public runtime_error {
public:
    MetaRuntimeError(const string& msg) : runtime_error(msg) {}
};
// 为 __int128 类型重载 << 运算符
ostream& operator<<(ostream& os, __int128& value) {
    std::ostringstream oss;
    if (value < 0) {
        oss.put('-');
        value = -value;
    }
    bool is_first = true;
    do {
        int digit = value % 10;
        value /= 10;
        if (is_first) {
            oss.put('0' + digit);
            is_first = false;
        } else {
            oss.put('0' + digit);
        }
    } while (value > 0);
    std::string result = oss.str();
    std::reverse(result.begin(), result.end());
    return os << result;
}

// 自定义 __int128 转换为字符串的函数
string to_string(__int128 value) {
    std::ostringstream oss;
    if (value < 0) {
        oss.put('-');
        value = -value;
    }
    do {
        int digit = value % 10;
        value /= 10;
        oss.put('0' + digit);
    } while (value > 0);
    std::string result = oss.str();
    std::reverse(result.begin(), result.end());
    return result;
}
// 类型转换和检查工具函数
namespace MetaUtils {
    template<typename T>
    T safe_any_cast(const any& value) {
        try {
            return any_cast<T>(value);
        } catch (const bad_any_cast& e) {
            throw MetaRuntimeError("类型转换错误: " + string(e.what()));
        }
    }

    bool is_numeric(const any& value) {
        const type_info& tid = value.type();
        return tid == typeid(int) || tid == typeid(double) || 
               tid == typeid(float) || tid == typeid(long) ||
               tid == typeid(long long) || tid == typeid(short);
    }

    double to_double(const any& value) {
        if (value.type() == typeid(int)) return any_cast<int>(value);
        if (value.type() == typeid(double)) return any_cast<double>(value);
        if (value.type() == typeid(float)) return any_cast<float>(value);
        if (value.type() == typeid(long)) return any_cast<long>(value);
        if (value.type() == typeid(long long)) return any_cast<long long>(value);
        if (value.type() == typeid(short)) return any_cast<short>(value);
        throw MetaRuntimeError("无法转换为数值类型");
    }
}

ostream& operator<<(ostream& os, const any& value) {
    if (!value.has_value()) {
        return os << "null";
    }
    
    const type_info& tid = value.type();
    
    try {
        if (tid == typeid(int)) os << any_cast<int>(value);
        else if (tid == typeid(double)) os << any_cast<double>(value);
        else if (tid == typeid(float)) os << any_cast<float>(value);
        else if (tid == typeid(long)) os << any_cast<long>(value);
        else if (tid == typeid(long long)) os << any_cast<long long>(value);
        else if (tid == typeid(short)) os << any_cast<short>(value);
        else if (tid == typeid(string)) os << any_cast<string>(value);
        else if (tid == typeid(bool)) os << boolalpha << any_cast<bool>(value);
        else if (tid == typeid(const char*)) os << any_cast<const char*>(value);
        else if (tid == typeid(__int128)) os << to_string(any_cast<__int128>(value));
        // 处理 variant 类型
        else if (tid.name() == string("std::variant<const char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >")) {
            try {
                os << get<const char*>(any_cast<variant<const char*, string>>(value));
            } catch (...) {
                try {
                    os << get<string>(any_cast<variant<const char*, string>>(value));
                } catch (...) {
                    os << "[variant_error]";
                }
            }
        }
        // 处理其他 variant 组合
        else if (tid.name() == string("std::variant<short, int, long, long long, float, double, long double>")) {
            try {
                os << MetaUtils::to_double(value);
            } catch (...) {
                os << "[numeric_variant_error]";
            }
        }
        else if (tid.name() == string("std::variant<bool>")) {
            os << boolalpha << any_cast<bool>(value);
        }
        else os << "[unknown_type:" << tid.name() << "]";
    } catch (const bad_any_cast& e) {
        os << "[any_cast_error:" << e.what() << "]";
    }
    return os;
}

// 算术运算符重载
any operator+(const any& lhs, const any& rhs) {
    if (MetaUtils::is_numeric(lhs) && MetaUtils::is_numeric(rhs)) {
        return MetaUtils::to_double(lhs) + MetaUtils::to_double(rhs);
    }
    
    if (lhs.type() == typeid(string) && rhs.type() == typeid(string)) {
        return any(any_cast<string>(lhs) + any_cast<string>(rhs));
    }
    
    stringstream ss;
    ss << lhs << rhs;
    return any(ss.str());
}

any operator-(const any& lhs, const any& rhs) {
    if (MetaUtils::is_numeric(lhs) && MetaUtils::is_numeric(rhs)) {
        return MetaUtils::to_double(lhs) - MetaUtils::to_double(rhs);
    }
    throw MetaRuntimeError("不支持的减法操作类型");
}

any operator*(const any& lhs, const any& rhs) {
    if (MetaUtils::is_numeric(lhs) && MetaUtils::is_numeric(rhs)) {
        return MetaUtils::to_double(lhs) * MetaUtils::to_double(rhs);
    }
    throw MetaRuntimeError("不支持的乘法操作类型");
}

any operator/(const any& lhs, const any& rhs) {
    if (MetaUtils::is_numeric(lhs) && MetaUtils::is_numeric(rhs)) {
        double rhs_val = MetaUtils::to_double(rhs);
        if (rhs_val == 0) throw MetaRuntimeError("除零错误");
        return MetaUtils::to_double(lhs) / rhs_val;
    }
    throw MetaRuntimeError("不支持的除法操作类型");
}

// 比较运算符重载
bool operator==(const any& lhs, const any& rhs) {
    if (lhs.type() != rhs.type()) return false;
    if (MetaUtils::is_numeric(lhs) && MetaUtils::is_numeric(rhs)) {
        return MetaUtils::to_double(lhs) == MetaUtils::to_double(rhs);
    }
    if (lhs.type() == typeid(string)) {
        return any_cast<string>(lhs) == any_cast<string>(rhs);
    }
    if (lhs.type() == typeid(bool)) {
        return any_cast<bool>(lhs) == any_cast<bool>(rhs);
    }
    return false;
}

bool operator!=(const any& lhs, const any& rhs) {
    return !(lhs == rhs);
}

bool operator<(const any& lhs, const any& rhs) {
    if (MetaUtils::is_numeric(lhs) && MetaUtils::is_numeric(rhs)) {
        return MetaUtils::to_double(lhs) < MetaUtils::to_double(rhs);
    }
    if (lhs.type() == typeid(string)) {
        return any_cast<string>(lhs) < any_cast<string>(rhs);
    }
    throw MetaRuntimeError("不支持的比较操作类型");
}

bool operator>(const any& lhs, const any& rhs) {
    return rhs < lhs;
}

bool operator<=(const any& lhs, const any& rhs) {
    return !(lhs > rhs);
}

bool operator>=(const any& lhs, const any& rhs) {
    return !(lhs < rhs);
}

// 输入运算符重载
istream& operator>>(istream& is, any& value) {
    string input;
    getline(is, input);
    
    try {
        if (input.find('.') != string::npos) {
            value = stod(input);
        } else {
            value = stoi(input);
        }
    } catch (...) {
        value = input;
    }
    return is;
}

class Meta {
public:
    // 类成员变量声明
    any input(const string& prompt = "") {
        cout << prompt;
        string value;
        getline(cin, value);
        try {
            if (value.find('.') != string::npos) {
                return any(stod(value));
            } else {
                return any(stoi(value));
            }
        } catch (...) {
            return any(value);
        }
    }

    any readline(const string& prompt = "") {
        string value;
        cout << prompt;
        getline(cin, value);
        return any(value);
    }
"""
    
    for stmt in statements:
        if isinstance(stmt, dict) and stmt['type'] == 'macro':
            cpp_code += f"        {stmt['code']}\n"
        if isinstance(stmt, dict) and stmt['type'] == 'class':
            class_data = stmt['data']
            for var_decl in class_data['variables']:
                if 'string' in var_decl:
                    var_decl = var_decl.replace('string', 'std::string')
                cpp_code += f"    {var_decl}\n"
            cpp_code += "\n"
            for func in class_data['functions']:
                params = ', '.join(['any ' + p for p in func['params']])
                cpp_code += f"    any {func['name']}({params}) {{\n"
                for line in func['body']:
                    if 'string' in line:
                        line = line.replace('string', 'std::string')
                    cpp_code += f"        {line}\n"
                cpp_code += "    }\n"
    
    cpp_code += """};
    
int main() {
    Meta meta;
    try{
        meta.Main();
    }catch(const bad_any_cast& e){
        cout<<"Error : 类型读取异常\\n";
        cout<<"CompilerError : <"<<e.what()<<">\\n";
    }catch(...){
        cout<<"Error : 未知运行时错误\\n";
        cout<<"CompilerError : <UnknowRuntimeError>\\n";
    }
    return 0;
}
"""
    return cpp_code

class CodeOptimizer:
    @staticmethod
    def optimize(code):
        # 自动在赋值语句中添加空格
        code = code.replace('=', ' = ')
        # 处理函数调用时的参数空格
        code = code.replace('(', ' ( ')
        code = code.replace(')', ' ) ')
        # 处理逗号分隔的参数
        code = code.replace(',', ' , ')

        code = code.replace(';',' ;')
        # 处理字符串中的空格（避免影响字符串内容）
        optimized_code = []
        inside_string = False
        for char in code:
            if char == '"':
                inside_string = not inside_string
            if char == ' ' and not inside_string:
                optimized_code.append(char)
            else:
                optimized_code.append(char)
        return ''.join(optimized_code)

def compile_meta(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        meta_code = f.read()

    # 对代码进行优化
    optimizer = CodeOptimizer()
    optimized_code = optimizer.optimize(meta_code)

    lexer = Lexer(optimized_code)
    parser = Parser(lexer)
    try:
        statements = parser.parse()
    except SyntaxError as e:
        print(e)
        return

    cpp_code = generate_cpp_code(statements)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cpp_code)

    print(f"编译完成，生成文件: {output_file}")

    # 编译cpp文件，添加C++17支持
    os.system(f"g++ -std=c++17 -O2 {output_file} -o {output_file.strip('.cpp')}.exe")
    print(f"编译cpp文件完成，生成文件: {os.path.splitext(output_file)[0]}.exe")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python meta_compiler.py <input.meta>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)

    base_name = os.path.splitext(input_file)[0]
    output_file = base_name + ".cpp"

    compile_meta(input_file, output_file)