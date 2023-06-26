# 과제 하면서 배운 내용을 정리하는 중입니다. (아마 파이썬 관련...)

# With First Commit
## Compiled vs Interpreted
### compiled languages
- Assembler, COBOL, PL/I, C/C++
- translated by running the source code through a compiler
- very efficient code that can be executed any number of times
- overhead for the translation incurred just once (when the source is compiled; thereafter, it need only be loaded and executed.)

### interpreted language
- must be parsed, interpreted, and executed each time the program is run
- usually less efficient than compiled programs 
- speed of development faster?
- interpreter assigns a type to all the variables at run-time(type decided based on value)

Java™, can be either interpreted or compiled.

파이썬은 자바랑 달리 함수를 쓰는 코드가 위에 있는게 문제가 되길래 찾아보았다.

[Dynamic Typing](https://www.educative.io/answers/what-is-dynamic-typing)

[Compiled vs Interpreted](https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-compiled-versus-interpreted-languages)


# 2023 06 25

## lambda expression
Small anonymous functions can be created with the **lambda** keyword. 
This function returns the sum of its two arguments: lambda a, b: a+b. 
Lambda functions can be used wherever function objects are required. 
They are syntactically restricted to a single expression. 
Semantically, they are just syntactic sugar for a normal function definition. 
Like nested function definitions, lambda functions can reference variables from the containing scope:


## Functions are first class objects
- functions behave like any other object, such as an int or a list. 
- this means you can use functions as arguments to other functions, store functions as dictionary values, or return a function from another function. 

## Function argumnents
### Call by “object reference”
- strings and tuples -> cannot be directly modified (immutable). 
- Atomic variables such as *integers or floats are always immutable*. (If you perform any operation that seems to modify an integer, such as addition or subtraction, it actually creates a new integer object with the updated value. The original integer object remains unchanged.)
- lists and dictionaries -> can be directly modified (mutable). 
Passing mutable variables as function arguments can have different outcomes, depedning on what is done to the variable inside the function. When we call
```
x = [1,2,3] # mutable
f(x)
```
what is passsed to the function is a copy of the name x that refers to the content (a list) [1, 2, 3]. If we use this copy of the name to change the content directly (e.g. x[0] = 999) within the function, then x chanes outside the funciton as well. However, if we reassgne x within the function to a new object (e.g. another list), then the copy of the name x now points to the new object, but x outside the function is unhcanged.

[Python functions](https://people.duke.edu/~ccc14/sta-663/FunctionsSolutions.html)