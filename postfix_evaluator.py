import re
from stack import Stack


class PostfixEvaluator:

    def __init__(self):
        self.operators = ["+", "-", "*", "/"]

    def is_number(self, token):
        """Checks whether a token is a valid number."""
        return re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)",
            token
        ) is not None

    def evaluate(self, expression):
        """
        Evaluate a postfix expression and return its result.

        Raises two errors in case of:
            ValueError: If the expression is malformed.
            ZeroDivisionError: If division by zero occurs.
        """

        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression can't be empty.")

        stack = Stack()
        tokens = expression.split()

        for token in tokens:

            if self.is_number(token):

                number = float(token)

                # Keep whole numbers as integers.
                if number.is_integer():
                    number = int(number)

                stack.push(number)

            elif token in self.operators:

                # An operator needs two operands.
                if stack.size() < 2:
                    raise ValueError(
                        "Not enough operands for operator "
                        + token
                    )

                right_operand = stack.pop()
                left_operand = stack.pop()

                if token == "+":
                    result = left_operand + right_operand

                elif token == "-":
                    result = left_operand - right_operand

                elif token == "*":
                    result = left_operand * right_operand

                else:
                    if right_operand == 0:
                        raise ZeroDivisionError(
                            "Can't divide by zero."
                        )

                    result = left_operand / right_operand

                stack.push(result)

            else:
                raise ValueError(
                    "Invalid token found: " + token
                )

        # A correct postfix expression must leave one result.
        if stack.size() != 1:
            raise ValueError(
                "Invalid postfix expression. "
                "The expression has too many operands."
            )

        return stack.pop()


# Tests for PostfixEvaluator
if __name__ == "__main__":

    evaluator = PostfixEvaluator()

    print("Testing The Postfix Evaluator")

    valid_tests = [
        ("5 3 +", 8),
        ("8 2 - 3 +", 9),
        ("5 3 8 * +", 29),
        ("6 2 / 3 +", 6.0),
        ("5 8 + 3 -", 10),
        ("5 3 + 8 *", 64),
        ("8 2 3 * + 6 -", 8),
        ("5 3 8 * + 2 /", 14.5),
        ("8 2 + 3 6 * -", -8),
        ("5 3 + 8 2 / -", 4.0),
        ("35 27 + 3 *", 186),
        ("23 30 15 * /", 23 / (30 * 15))
    ]

    for expression, expected in valid_tests:
        result = evaluator.evaluate(expression)
        assert abs(result - expected) < 0.000001
        print(expression, "=", result)

    invalid_tests = [
        "2 3 4 +",
        "20 29 9 * ;",
        "25 23 - +",
        "8 0 /",
        "5 +",
        "3 + 4",
        ""
    ]

    for expression in invalid_tests:
        try:
            evaluator.evaluate(expression)
            print("ERROR: Invalid expression was accepted:",
                  expression)
        except (ValueError, ZeroDivisionError):
            print("Invalid expression correctly rejected:",
                  expression)

    print("Postfix tests completed! -_-")