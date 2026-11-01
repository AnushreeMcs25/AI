import re
import itertools


class Sentence:
    def evaluate(self, model):
        pass

    def get_symbols(self):
        pass


class Symbol(Sentence):
    def __init__(self, name):
        self.name = name

    def evaluate(self, model):
        return model[self.name]

    def get_symbols(self):
        return {self.name}


class Not(Sentence):
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def get_symbols(self):
        return self.operand.get_symbols()


class And(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return self.left.evaluate(model) and self.right.evaluate(model)

    def get_symbols(self):
        return self.left.get_symbols() | self.right.get_symbols()


class Or(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return self.left.evaluate(model) or self.right.evaluate(model)

    def get_symbols(self):
        return self.left.get_symbols() | self.right.get_symbols()


class Implies(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return not self.left.evaluate(model) or self.right.evaluate(model)

    def get_symbols(self):
        return self.left.get_symbols() | self.right.get_symbols()


class Iff(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, model):
        return self.left.evaluate(model) == self.right.evaluate(model)

    def get_symbols(self):
        return self.left.get_symbols() | self.right.get_symbols()


class LogicParser:
    def __init__(self, text):
        text = text.replace("V", "|")
        text = text.replace("v", "|")
        text = text.replace("⬄", "<->")
        text = text.replace("↔", "<->")
        text = text.replace("→", "->")
        text = text.replace("¬", "~")
        text = text.replace("∧", "&")
        text = text.replace("∨", "|")

        pattern = r"<->|->|[()~&|]|[A-Za-z][A-Za-z0-9_]*"

        self.tokens = re.findall(pattern, text)
        remaining = re.sub(pattern, "", text)

        if remaining.strip() or not self.tokens:
            raise ValueError("Invalid expression: " + text)

        self.pos = 0

    def match(self, token):
        if self.pos < len(self.tokens):
            if self.tokens[self.pos] == token:
                self.pos += 1
                return True
        return False

    def parse(self):
        result = self.parse_iff()

        if self.pos != len(self.tokens):
            raise ValueError("Invalid expression")

        return result

    def parse_iff(self):
        left = self.parse_implies()

        while self.match("<->"):
            right = self.parse_implies()
            left = Iff(left, right)

        return left

    def parse_implies(self):
        left = self.parse_or()

        if self.match("->"):
            right = self.parse_implies()
            return Implies(left, right)

        return left

    def parse_or(self):
        left = self.parse_and()

        while self.match("|"):
            right = self.parse_and()
            left = Or(left, right)

        return left

    def parse_and(self):
        left = self.parse_not()

        while self.match("&"):
            right = self.parse_not()
            left = And(left, right)

        return left

    def parse_not(self):
        if self.match("~"):
            return Not(self.parse_not())

        if self.match("("):
            result = self.parse_iff()

            if not self.match(")"):
                raise ValueError("Missing closing bracket")

            return result

        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token):
                self.pos += 1
                return Symbol(token)

        raise ValueError("Invalid expression")


def generate_truth_table(symbols):
    return [
        dict(zip(symbols, values))
        for values in itertools.product(
            [True, False], repeat=len(symbols)
        )
    ]


def extract_relationships(text):
    expressions = {}

    if not text.strip() or text.strip().lower() == "no":
        return expressions

    pattern = r"(?:\(\s*[ivxlcdm]+\s*\)\s*)?([A-Za-z]\w*)\s*:"
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    if matches:
        for i, match in enumerate(matches):
            name = match.group(1)

            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

            expression = text[start:end].strip().strip(",;")

            if name in expressions:
                raise ValueError("Duplicate relationship: " + name)

            expressions[name] = LogicParser(expression).parse()

    else:
        parts = re.split(r"[;,]", text)

        for i, part in enumerate(parts):
            if part.strip():
                name = "expr" + str(i + 1)
                expressions[name] = LogicParser(part.strip()).parse()

    return expressions



def extract_queries(text):
    queries = []

    parts = re.split(
        r"\s+\band\b\s+",
        text,
        flags=re.IGNORECASE
    )

    for part in parts:
        if not re.search(r"\s+entails\s+", part, re.IGNORECASE):
            raise ValueError("Invalid query. Use A entails B")

        left, right = re.split(
            r"\s+entails\s+",
            part,
            maxsplit=1,
            flags=re.IGNORECASE
        )

        left = left.strip()
        right = right.strip()

        if not left or not right:
            raise ValueError("Missing expression in entailment")

        queries.append((left, right))

    return queries



def get_expression(value, expressions, name):
    if value in expressions:
        return expressions[value], value

    expression = LogicParser(value).parse()

    if name not in expressions:
        expressions[name] = expression

    return expression, name


def print_truth_table(expressions, table, symbols):
    headers = symbols + list(expressions.keys())

    rows = []

    for model in table:
        row = []

        for symbol in symbols:
            row.append("T" if model[symbol] else "F")

        for expression in expressions.values():
            row.append("T" if expression.evaluate(model) else "F")

        rows.append(row)

    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    print("\nCOMPLETE RELATIONSHIP TRUTH TABLE\n")

    print(" | ".join(
        headers[i].center(widths[i])
        for i in range(len(headers))
    ))

    print("-+-".join("-" * width for width in widths))

    for row in rows:
        print(" | ".join(
            row[i].center(widths[i])
            for i in range(len(row))
        ))


def check_entailment(a, b, table, symbols, name_a, name_b):
    counterexamples = []

    for index, model in enumerate(table, start=1):
        if a.evaluate(model) and not b.evaluate(model):
            counterexamples.append(index)

    print("\nChecking:", name_a, "entails", name_b)

    print("\nChecking:", name_a, "entails", name_b)

    if not counterexamples:
        print("Result: YES")
        print(name_a, "entails", name_b)
    else:
        print("Result: NO")
        print(name_a, "does not entail", name_b)

def main():
    print("PROPOSITIONAL LOGIC - TRUTH TABLE")
    print("---------------------------------")

    kb_text = input("Enter relationships : ")
    query_text = input("Enter entailment queries: ")

    try:
        expressions = extract_relationships(kb_text)
        queries = extract_queries(query_text)

        resolved_queries = []

        for i, (left, right) in enumerate(queries, start=1):
            a, name_a = get_expression(
                left, expressions, "Query" + str(i) + "_A"
            )

            b, name_b = get_expression(
                right, expressions, "Query" + str(i) + "_B"
            )

            resolved_queries.append((a, b, name_a, name_b))

        symbols = sorted(set().union(
            *(expression.get_symbols()
              for expression in expressions.values())
        ))

        table = generate_truth_table(symbols)

        print_truth_table(expressions, table, symbols)

        print("\nENTAILMENT RESULTS")
        print("---------------------------------")

        for a, b, name_a, name_b in resolved_queries:
            check_entailment(
                a, b, table, symbols, name_a, name_b
            )
            print("---------------------------------")

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()





output: 

PROPOSITIONAL LOGIC - TRUTH TABLE
---------------------------------
Enter relationships : (i) a: ¬(SVT)  (ii) b: (S&T)  (iii) c: TV¬T  (iv) d: ¬(S⬄S)  (v) e: ¬S -> ¬T
Enter entailment queries: a entails b and a entails c

COMPLETE RELATIONSHIP TRUTH TABLE

S | T | a | b | c | d | e
--+---+---+---+---+---+--
T | T | F | T | T | F | T
T | F | F | F | T | F | T
F | T | F | F | T | F | F
F | F | T | F | T | F | T

ENTAILMENT RESULTS
---------------------------------

Checking: a entails b

Checking: a entails b
Result: NO
a does not entail b
---------------------------------

Checking: a entails c

Checking: a entails c
Result: YES
a entails c
---------------------------------
