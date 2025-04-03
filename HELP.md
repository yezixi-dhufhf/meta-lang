# Meta 编程语言教程

## 目录
1. [语言概述](#语言概述)
2. [基本语法](#基本语法) 
3. [变量与数据类型](#变量与数据类型)
4. [函数](#函数)
5. [类与对象](#类与对象)
6. [所有权系统](#所有权系统)
7. [输入输出](#输入输出)
8. [编译与执行](#编译与执行)

## 语言概述

Meta 是一种支持动态和静态类型的编译型编程语言，编译为C++代码后执行。它结合了现代语言的特性，包括：

- 所有权和借用系统（类似Rust）
- 模板支持  
- 动态类型（使用std::any）
- 类和方法

## 基本语法

### Hello World 程序

```meta
class Meta {
    function Main() {
        print("Hello, World!");
        return 0;
    }
}
```
## 变量与数据类型
### 变量声明
```meta
data x=100;
data y=3.14;
data name="Jone";
data flag=true;
```
- **第1行**：声明整数(int)，存为 any 类型
- **第2行**：声明浮点数(float)，存为 any 类型
- **第3行**：声明字符串(str)，存为 any 类型
- **第4行**：声明布尔(bool)，存为 any 类型

### 数组
```meta
data []vector;
data [5]array;
```
- **第1行**：创建一个动态数组
- **第2行**：创建一个长度为5的静态数组
*注：写成`data[] name`,`data[size] name`甚至`data                   [size]               name`也可以，但不够直观*

### 模板化类型
格式
```meta
data<type1,type2,type3,...> name;
data<type1,type2,type3,...> []name;
data<type1,type2,type3,...> [size]name;
```