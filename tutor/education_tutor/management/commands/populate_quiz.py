from django.core.management.base import BaseCommand
from education_tutor.models import ProgrammingLanguage, Question

class Command(BaseCommand):
    help = 'Populate database with quiz questions'

    def handle(self, *args, **kwargs):
        languages = {
            "Python": [
                {"text": "What is the correct file extension for Python files?", "options": [".py", ".pyt", ".pt", ".python"], "answer": ".py"},
                {"text": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "answer": "def"},
                {"text": "Which data type is immutable in Python?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
                {"text": "Which symbol is used for single-line comments in Python?", "options": ["//", "#", "/* */", "--"], "answer": "#"},
                {"text": "Which Python module is used for regular expressions?", "options": ["regex", "re", "reg", "pattern"], "answer": "re"},
                {"text": "Which function converts a string to an integer?", "options": ["int()", "str()", "float()", "chr()"], "answer": "int()"},
                {"text": "What is used to handle exceptions in Python?", "options": ["try-except", "catch", "throw", "finally"], "answer": "try-except"},
                {"text": "What will `3 // 2` return in Python?", "options": ["1.5", "1", "2", "0"], "answer": "1"},
                {"text": "Which library is used for data manipulation in Python?", "options": ["NumPy", "Pandas", "Matplotlib", "Seaborn"], "answer": "Pandas"},
                {"text": "Which function is used to read user input?", "options": ["input()", "get()", "read()", "scan()"], "answer": "input()"},
                {"text": "Which operator is used for exponentiation?", "options": ["^", "**", "//", "*"], "answer": "**"},
                {"text": "What is the output of `bool('False')`?", "options": ["False", "True", "Error", "None"], "answer": "True"},
                {"text": "What keyword is used to define a class in Python?", "options": ["class", "define", "struct", "object"], "answer": "class"},
                {"text": "Which Python structure allows key-value pairs?", "options": ["List", "Tuple", "Set", "Dictionary"], "answer": "Dictionary"},
                {"text": "Which statement is used to exit a loop?", "options": ["stop", "exit", "break", "return"], "answer": "break"},
            ],
            "JavaScript": [
                {"text": "Which keyword is used to declare a variable in JavaScript?", "options": ["var", "int", "string", "let"], "answer": "var"},
                {"text": "Which function is used to print content to the console?", "options": ["print()", "console.log()", "log()", "write()"], "answer": "console.log()"},
                {"text": "Which operator is used for strict equality comparison?", "options": ["==", "!=", "===", "=>"], "answer": "==="},
                {"text": "Which JavaScript method is used to select an element?", "options": ["querySelector()", "getElement()", "find()", "select()"], "answer": "querySelector()"},
                {"text": "Which object represents the browser window?", "options": ["document", "window", "navigator", "screen"], "answer": "window"},
                {"text": "Which function removes the last element of an array?", "options": ["remove()", "pop()", "shift()", "splice()"], "answer": "pop()"},
                {"text": "Which method is used to add an element to the end of an array?", "options": ["push()", "add()", "append()", "insert()"], "answer": "push()"},
                {"text": "Which statement is used to loop through an object’s properties?", "options": ["for", "while", "forEach", "for...in"], "answer": "for...in"},
                {"text": "Which JavaScript function is used to parse a string into an integer?", "options": ["parseInt()", "toInt()", "int()", "Number()"], "answer": "parseInt()"},
                {"text": "Which function is used to delay execution?", "options": ["setTimeout()", "setInterval()", "delay()", "wait()"], "answer": "setTimeout()"},
            ],
            "Java": [
                {"text": "Which method is the entry point of a Java program?", "options": ["start()", "main()", "run()", "execute()"], "answer": "main()"},
                {"text": "Which keyword is used to define a class in Java?", "options": ["define", "class", "struct", "public"], "answer": "class"},
                {"text": "Which operator is used for string concatenation in Java?", "options": ["+", "&", "*", "/"], "answer": "+"},
                {"text": "Which access modifier allows access within the same package?", "options": ["private", "protected", "public", "default"], "answer": "default"},
                {"text": "What is the default value of a boolean variable in Java?", "options": ["true", "false", ""https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps"", "0"], "answer": "false"},
            ],
            "C++": [
                {"text": "Which operator is used to allocate memory dynamically in C++?", "options": ["malloc", "allocate", "new", "memory"], "answer": "new"},
                {"text": "Which keyword is used to define a class in C++?", "options": ["define", "class", "struct", "object"], "answer": "class"},
                {"text": "Which library is used for input and output in C++?", "options": ["iostream", "stdio", "cstdio", "fstream"], "answer": "iostream"},
            ],
            "Go": [
                {"text": "What is the keyword used to declare a function in Go?", "options": ["define", "func", "function", "method"], "answer": "func"},
                {"text": "Which keyword is used to declare a variable in Go?", "options": ["var", "int", "string", "let"], "answer": "var"},
                {"text": "Which package is used for input/output operations in Go?", "options": ["io", "fmt", "input", "scan"], "answer": "fmt"},
            ],
        }

        for lang_name, questions in languages.items():
            language, created = ProgrammingLanguage.objects.get_or_create(name=lang_name)
            for q in questions:
                Question.objects.create(
                    language=language,
                    text=q["text"],
                    option1=q["options"][0],
                    option2=q["options"][1],
                    option3=q["options"][2],
                    option4=q["options"][3],
                    correct_option=q["answer"]
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated quiz data!"))
