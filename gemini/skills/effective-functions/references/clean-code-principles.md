# Clean Code Principles (Functions)

Building blocks of software should be solid and easy to understand.

## 1. Single Responsibility Principle (SRP)
A function should do one thing and do it well. If a function's name includes "and", it's a candidate for splitting.

## 2. Pure Functions & Side Effects
- **Pure Functions**: Given the same input, always return the same output with no observable side effects. This makes testing and reasoning about code much easier.
- **Isolate Side Effects**: Keep side effects (I/O, global state changes) isolated and clearly documented.

## 3. Signature & Arguments
- **Number of Arguments**: Prefer 0 to 2 arguments. If you need 3 or more, use an object/dictionary.
- **Avoid Flag Arguments**: Passing a boolean flag to a function is a sign that the function is doing more than one thing. Split it into two functions.

## 4. Readability Techniques
- **Guard Clauses**: Exit early to avoid nested `if` statements.
- **Meaningful Names**: Use verbs for function names and describe what the function does, not how it does it.
- **Fail Fast**: Validate inputs at the beginning of the function.

## 5. Command-Query Separation (CQS)
A function should either change the state of an object (command) or return data (query), but never both.
