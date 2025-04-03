# 具体代码请访问具体版本目录
# Meta 编译器
Meta 是一种支持动态和静态类型的编译型编程语言，目前仍在开发中。
[访问 Meta github仓库](https://github.com/yezixi-dhufhf/meta-lang)

## 使用须知
作者使用 **Windows 10** 调试，其他平台未尝试。如果您使用其他操作系统，可能需要自行调整。

您需要以下条件才能使用 Meta 语言：
1. **GCC 6+** 且配置好环境变量（建议使用 GCC 8+，作者调试使用 GCC 9.2.0）。
2. **Python 3.x** 且配置好环境变量（作者调试使用 Python 3.13.0）。
3. **Meta 编译器** (`meta_compiler.py`)。

如果您不确定是否满足条件，请按照以下步骤测试：

### Python 环境测试
首先打开终端，输入以下命令
`python -V`
如果正常，应弹出以下内容(以 Python 3.13.0 举例)：
```batch
Python 3.13.0
```
如果不是类似的内容，请检查环境变量或安装情况
---
### C++ 环境测试
首先打开终端，输入以下命令
`gcc --version`
如果正常，应弹出(以 gcc 9.2.0 举例)：
```batch
gcc (tdm64-1) 9.2.0
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```
如果不是类似的内容，请检查环境变量或安装情况
---
### Meta 获取
[获取 Meta](https://github.com/yezixi-dhufhf/meta-lang)

## Meta 语言简介
Meta 语言的实现过程如下：
1. **通过 `Lexer` 类进行 Token 分析**：将源代码分解为基本的语法单元（Token）。
2. **通过 `Parser` 类进行语法分析**：解析 Token 序列，生成抽象语法树（AST）。
3. **通过 `generate_cpp_code` 函数生成 C++ 代码**：将 AST 转换为 C++ 代码。
4. **编译 C++ 代码生成可执行文件**：使用 GCC 编译生成的 C++ 代码。

# Meta 教程
## 编译 Meta
先切换到编译器所在目录，然后通过终端执行以下命令：
```batch
python meta_compiler.py path\your_file_name
```
会在当前目录下生成一个 *.cpp* 文件和 *.exe* 文件
如果你不是使用 Windows 系统，请使用`g++ your_file_name.cpp -o your_file_name`重新编译

## "Hello, World" 程序教程
您可以实现您的第一个程序：Hello, World!
```meta
class Meta{
    function Main(){
        print("Hello, World!");
        return 0;
    }
}
```
它会在控制台输出 *Hello, World!*
其他详情请访问[Meta 的 github 仓库](https://github.com/yezixi-dhufhf/meta-lang)

## 其他
**该语言开源且免费，任何人都可以下载和修改**
**最终解释权与所有权归我所有！！！**