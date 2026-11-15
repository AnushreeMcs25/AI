
import re

def singular(word):
    word = word.lower().strip()

    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]

    return word

def constant(word):
    return word.strip().rstrip(".").capitalize()

def predicate(word):
    return singular(word).capitalize()

def make_literal(text):
    text = text.strip()
    neg = text.startswith("~")

    if neg:
        text = text[1:].strip()

    match = re.fullmatch(r"(\w+)\((.*?)\)", text)

    if not match:
        raise ValueError("Invalid literal: " + text)

    args = tuple(x.strip() for x in match.group(2).split(","))
    return (neg, match.group(1), args)

def parse_clause(text):
    return frozenset(make_literal(x) for x in text.split("|"))

def convert(sentence):
    s = sentence.lower().strip().rstrip(".")

    match = re.fullmatch(r"john likes all kinds? of (\w+)", s)
    if match:
        p = predicate(match.group(1))
        return [parse_clause(f"~{p}(x) | Likes(John,x)")]

    match = re.fullmatch(r"all (\w+) are (\w+)", s)
    if match:
        a, b = map(predicate, match.groups())
        return [parse_clause(f"~{a}(x) | {b}(x)")]

    match = re.fullmatch(r"(\w+) and (\w+) are (\w+)", s)
    if match:
        a, b, c = match.groups()
        return [
            parse_clause(f"{predicate(c)}({constant(a)})"),
            parse_clause(f"{predicate(c)}({constant(b)})")
        ]

    match = re.fullmatch(r"anyone who is alive implies not killed", s)
    if match:
        return [parse_clause("~Alive(x) | ~Killed(x)")]

    match = re.fullmatch(r"anyone who is not killed implies alive", s)
    if match:
        return [parse_clause("Killed(x) | Alive(x)")]

    match = re.fullmatch(
        r"anything anyone eats and (?:is )?not killed is (\w+)", s
    )
    if match:
        p = predicate(match.group(1))
        return [parse_clause(f"~Eats(x,y) | Killed(x) | {p}(y)")]

    match = re.fullmatch(
        r"(\w+) eats everything that (\w+) eats", s
    )
    if match:
        a, b = map(constant, match.groups())
        return [parse_clause(f"~Eats({b},x) | Eats({a},x)")]

    match = re.fullmatch(
        r"(\w+) eats (\w+) and (?:is )?still alive", s
    )
    if match:
        a, b = map(constant, match.groups())
        return [
            parse_clause(f"Eats({a},{b})"),
            parse_clause(f"Alive({a})")
        ]

    match = re.fullmatch(
        r"(\w+) (likes|eats|loves|knows) (\w+)", s
    )
    if match:
        a, verb, b = match.groups()
        return [parse_clause(
            f"{verb.capitalize()}({constant(a)},{constant(b)})"
        )]

    match = re.fullmatch(r"(\w+) is (?:a |an )?(\w+)", s)
    if match:
        a, b = match.groups()
        return [parse_clause(f"{predicate(b)}({constant(a)})")]

    raise ValueError("Sentence pattern not supported: " + sentence)

def is_variable(x):
    return x[0].islower()

def substitute(x, subst):
    while is_variable(x) and x in subst:
        x = subst[x]
    return x

def unify(a, b, subst):
    a = substitute(a, subst)
    b = substitute(b, subst)

    if a == b:
        return True

    if is_variable(a):
        subst[a] = b
        return True

    if is_variable(b):
        subst[b] = a
        return True

    return False

def apply_substitution(clause, subst):
    result = set()

    for neg, pred, args in clause:
        new_args = tuple(substitute(x, subst) for x in args)
        result.add((neg, pred, new_args))

    return frozenset(result)

def rename_variables(clause, number):
    mapping = {}
    result = set()

    for neg, pred, args in clause:
        new_args = []

        for arg in args:
            if is_variable(arg):
                if arg not in mapping:
                    mapping[arg] = arg + "_" + str(number)
                new_args.append(mapping[arg])
            else:
                new_args.append(arg)

        result.add((neg, pred, tuple(new_args)))

    return frozenset(result)

def canonicalize(clause):
    mapping = {}
    result = set()

    for neg, pred, args in sorted(clause, key=str):
        new_args = []

        for arg in args:
            if is_variable(arg):
                if arg not in mapping:
                    mapping[arg] = "v" + str(len(mapping))
                new_args.append(mapping[arg])
            else:
                new_args.append(arg)

        result.add((neg, pred, tuple(new_args)))

    return frozenset(result)

def resolve(c1, c2, number):
    c1 = rename_variables(c1, number)
    c2 = rename_variables(c2, number + 1)

    results = set()

    for l1 in c1:
        for l2 in c2:
            if l1[0] != l2[0] and l1[1] == l2[1]:
                if len(l1[2]) != len(l2[2]):
                    continue

                subst = {}
                valid = True

                for a, b in zip(l1[2], l2[2]):
                    if not unify(a, b, subst):
                        valid = False
                        break

                if valid:
                    new_clause = (c1 - {l1}) | (c2 - {l2})
                    new_clause = apply_substitution(new_clause, subst)

                    if not any(
                        (not neg, pred, args) in new_clause
                        for neg, pred, args in new_clause
                    ):
                        results.add(canonicalize(new_clause))

    return results

def resolution(kb, query):
    negated_query = frozenset({
        (not neg, pred, args)
        for neg, pred, args in query
    })

    clauses = [canonicalize(c) for c in kb]
    clauses.append(canonicalize(negated_query))

    known = set(clauses)
    number = 1

    while True:
        new_clauses = set()

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                results = resolve(clauses[i], clauses[j], number)
                number += 2

                for result in results:
                    if result not in known:
                        if len(result) == 0:
                            return True

                        new_clauses.add(result)

        if not new_clauses:
            return False

        known.update(new_clauses)
        clauses.extend(new_clauses)

        if len(known) > 5000:
            return False

print("FIRST ORDER LOGIC - RESOLUTION")

n = int(input("Enter number of premises: "))

knowledge_base = []

for i in range(n):
    sentence = input("Enter premise " + str(i + 1) + ": ")
    knowledge_base.extend(convert(sentence))

query_text = input("Enter query: ")
query_clauses = convert(query_text)

if len(query_clauses) != 1 or len(query_clauses[0]) != 1:
    print("Please enter a single positive atomic query.")
else:
    if resolution(knowledge_base, query_clauses[0]):
        print("\nEmpty clause obtained")
        print("Query is proved")
    else:
        print("\nEmpty clause not obtained")
        print("Query could not be proved")



output: 

FIRST ORDER LOGIC - RESOLUTION
Enter number of premises: 7
Enter premise 1: John likes all kind of food.
Enter premise 2: Apple and vegetables are food
Enter premise 3: Anything anyone eats and not killed is food.
Enter premise 4: Anil eats peanuts and still alive
Enter premise 5: Harry eats everything that Anil eats.
Enter premise 6: Anyone who is alive implies not killed
Enter premise 7: Anyone who is not killed implies alive
Enter query: John likes peanuts.

Empty clause obtained
Query is proved
