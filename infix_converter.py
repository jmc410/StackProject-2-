import re
from stack import Stack


class InfixToPostfixConverter:

    def __init__(self):
        """Set up the operator precedence rules."""
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2
        }

    def tokenize(self, expression):

        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Expression can't be empty.")

        pattern = r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|[()+*/-]"

        tokens = re.findall(pattern, expression)
        remaining = re.sub(pattern, "", expression)

        if remaining.strip():
            raise ValueError(
                "Expression contains an invalid token."
            )

        return tokens

    def is_operand(self, token):
        """Checks whether a token is an operand."""
        return re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?",
            token
        ) is not None

    def convert(self, expression):
        """
        Converts an infix expression to postfix notation.

        Raises a ValueError: If the expression is malformed.
        """

        tokens = self.tokenize(expression)

        operators = Stack()
        output = []

        expect_operand = True

        for token in tokens:

            if self.is_operand(token):

                if not expect_operand:
                    raise ValueError(
                        "Misplaced an operand: " + token
                    )

                output.append(token)
                expect_operand = False

            elif token == "(":

                if not expect_operand:
                    raise ValueError(
                        "Missing an operator before '('"
                    )

                operators.push(token)
                expect_operand = True

            elif token == ")":

                if expect_operand:
                    raise ValueError(
                        "Misplaced or empty parentheses."
                    )

                found_opening = False

                while not operators.is_empty():

                    if operators.peek() == "(":
                        operators.pop()
                        found_opening = True
                        break

                    output.append(operators.pop())

                if not found_opening:
                    raise ValueError(
                        "Mismatched parentheses, missing '('"
                    )

                expect_operand = False

            elif token in self.precedence:

                if expect_operand:
                    raise ValueError(
                        "Misplaced operator: " + token
                    )

                while (
                    not operators.is_empty()
                    and operators.peek() != "("
                    and self.precedence[operators.peek()]
                    >= self.precedence[token]
                ):
                    output.append(operators.pop())

                operators.push(token)
                expect_operand = True

            else:
                raise ValueError(
                    "Invalid token: " + token
                )

        if expect_operand:
            raise ValueError(
                "Expression ends with an incomplete operation."
            )

        # Remove any remaining operators.
        while not operators.is_empty():

            operator = operators.pop()

            if operator == "(":
                raise ValueError(
                    "Mismatched parentheses, missing ')'"
                )

            output.append(operator)

        return " ".join(output)


# Tests for the InfixToPostfixConverter
if __name__ == "__main__":

    converter = InfixToPostfixConverter()

    print("Testing Infix to Postfix Converter")

    valid_tests = [
        ("A + B", "A B +"),
        ("A + B * C", "A B C * +"),
        ("( A + B ) * C", "A B + C *"),
        ("A * B + C / D", "A B * C D / +"),
        ("( A + B ) * ( C - D )",
         "A B + C D - *"),
        ("A + B * C - D / E",
         "A B C * + D E / -"),
        ("A * ( B + C ) / D",
         "A B C + * D /"),
        ("( A + B * C ) / ( D - E )",
         "A B C * + D E - /"),
        ("A + ( B - C ) * D",
         "A B C - D * +"),
        ("( A + B * ( C - D ) ) / E",
         "A B C D - * + E /"),
        ("A - B + C", "A B - C +"),
        ("A / B * C", "A B / C *")
    ]

    for expression, expected in valid_tests:

        result = converter.convert(expression)

        assert result == expected

        print(expression, "->", result)

    invalid_tests = [
        "A + B ) C",
        "A + B ; C",
        "+ A B",
        "A + * B",
        "A B + C",
        "A + ) B * C (",
        "( A + B",
        "A + B )",
        "A +",
        "( )",
        ""
    ]

    for expression in invalid_tests:

        try:
            converter.convert(expression)
            print("ERROR: Invalid expression accepted:",
                  expression)

        except ValueError as error:
            print("Correctly rejected:",
                  expression, "-", error)

    # Test deeply nested parentheses as required by instructions.
    nested = "(((((((( A + B ))))))))"

    assert converter.convert(nested) == "A B +"

    print("Nested parentheses test passed.")
    print("Converter tests completed!")