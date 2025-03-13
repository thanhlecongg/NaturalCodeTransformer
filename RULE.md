# Transformation Rules Mapping

Currently, our tool support 23 semantic-preserving transformation operators in the following table:

| ID  | Transformation Rule           | Description |
|-----|------------------------------|-------------|
| 1   | RenameVariable               | Renames a variable while preserving functionality. |
| 2   | For2While                    | Converts a `for` loop into a `while` loop. |
| 3   | While2For                    | Converts a `while` loop into a `for` loop. |
| 4   | Do2While                     | Transforms a `do-while` loop into a `while` loop. |
| 5   | IfElseIf2IfElse              | Refactors an `if-else-if` chain into a nested `if-else`. |
| 6   | IfElse2IfElseIf              | Converts an `if-else` structure into an `if-else-if` chain. |
| 7   | Switch2If                    | Replaces a `switch` statement with equivalent `if-else` logic. |
| 8   | Unary2Add                    | Replaces a unary operation with an equivalent addition. |
| 9   | Add2Equal                    | Converts an addition assignment (`+=`), e.g., `a +=b` into an equality assignment (`==`), e.g, `a = a + b`. |
| 10  | DivideVarDecl                | Splits multiple variable declarations into separate statements. |
| 11  | MergeVarDecl                 | Combines multiple variable declarations into a single statement. |
| 12  | SwapStatement                | Swaps the order of two statements without data-flow dependencies |
| 13  | ModifyConstant               | Replace value of a constant value by equivalent mathmatical expression. |
| 14  | ReverseIf                    | Reverses the condition in an `if` statement and swaps its branches. |
| 15  | If2CondExp                   | Converts an `if` statement into a conditional (`?:`) expression. |
| 16  | ConfExp2If                   | Converts a conditional (`?:`) expression into an `if` statement. |
| 17  | InfixDividing                | Splits an infix expression into smaller sub-expressions. |
| 18  | DividePrePostFix             | Separates pre/postfix expression into explicit statements. |
| 19  | DividingComposedIf           | Breaks down a complex `if` condition into multiple conditions. |
| 20  | LoopIfContinue2Else          | Converts a `continue` inside a loop into an `else` branch. |
| 21  | SwitchEqualExp               | Switch two sides of equality expression. |
| 22  | SwitchStringEqual            | Switch two sides of String equality. |
| 23  | SwitchRelation               | Switch two sides of relation expressional. |
