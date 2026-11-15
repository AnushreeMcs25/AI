import re
facts = set()
rules = []
counter = 0

def clean(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()

def singular(word):
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word

def entity(text):
    return clean(text).replace(" ", "_")

def predicate(text):
    words = clean(text).split()
    words = [w for w in words if w not in
             ("a", "an", "the", "very", "really", "extremely")]
    return "_".join(singular(w) for w in words)

def add_rule(body, head):
    rules.append((body, head))

def new_object():
    global counter
    counter += 1
    return "object_" + str(counter)

def parse(sentence):
    s = clean(sentence)

    m = re.fullmatch(
        r"it is a crime for an? (.+?) to sell (.+?) to (.+)", s
    )
    if m:
        person, item, destination = m.groups()

        add_rule([
            (predicate(person), ("?x",)),
            ("sells", ("?x", "?y", "?z")),
            (predicate(item), ("?y",)),
            ("hostile", ("?z",))
        ], ("criminal", ("?x",)))

        return True

    m = re.fullmatch(
        r"enemy of (.+?) is known as (.+)", s
    )
    if m:
        country, result = m.groups()

        add_rule([
            ("enemy", ("?x", entity(country)))
        ], (predicate(result), ("?x",)))

        return True

    m = re.fullmatch(
        r"(.+?) is (?:an? )?enemy of (.+)", s
    )
    if m:
        subject, country = m.groups()

        facts.add((
            "enemy",
            (entity(subject), entity(country))
        ))

        return True

    m = re.fullmatch(
        r"(.+?) has some (.+)", s
    )
    if m:
        subject, item = m.groups()

        obj = new_object()

        facts.add((predicate(item), (obj,)))
        facts.add(("owns", (entity(subject), obj)))

        return True

    m = re.fullmatch(
        r"all (?:of the )?(.+?) were sold to (.+?) by (.+)", s
    )
    if m:
        item, destination, person = m.groups()

        add_rule([
            (predicate(item), ("?y",)),
            ("owns", (entity(destination), "?y"))
        ], ("sells", (entity(person), "?y", entity(destination))))

        return True

    m = re.fullmatch(
        r"all (.+?) are (.+)", s
    )
    if m:
        subject, result = m.groups()

        add_rule([
            (predicate(subject), ("?x",))
        ], (predicate(result), ("?x",)))

        return True

    m = re.fullmatch(
        r"(.+?) are (.+)", s
    )
    if m:
        subject, result = m.groups()

        add_rule([
            (predicate(subject), ("?x",))
        ], (predicate(result), ("?x",)))

        return True

    m = re.fullmatch(
        r"all (.+?) can (.+)", s
    )
    if m:
        subject, action = m.groups()

        add_rule([
            (predicate(subject), ("?x",))
        ], ("can_" + predicate(action), ("?x",)))

        return True

    m = re.fullmatch(
        r"(.+?) can (.+)", s
    )
    if m:
        subject, action = m.groups()

        facts.add((
            "can_" + predicate(action),
            (entity(subject),)
        ))

        return True

    m = re.fullmatch(
        r"(.+?) is an? (.+?) citizen", s
    )
    if m:
        subject, nationality = m.groups()

        facts.add((
            predicate(nationality),
            (entity(subject),)
        ))

        return True

    m = re.fullmatch(
        r"(.+?) is an? (.+)", s
    )
    if m:
        subject, category = m.groups()

        facts.add((
            predicate(category),
            (entity(subject),)
        ))

        return True

    m = re.fullmatch(
        r"(.+?) (likes|loves|hates|knows|helps|owns|teaches|visits) (.+)",
        s
    )
    if m:
        subject, relation, obj = m.groups()

        facts.add((
            relation,
            (entity(subject), entity(obj))
        ))

        return True

    return False

def unify(pattern, values, substitution):
    for p, v in zip(pattern, values):
        if p.startswith("?"):
            if p in substitution and substitution[p] != v:
                return None
            substitution[p] = v
        elif p != v:
            return None

    return substitution

def match_body(body, substitution):
    if not body:
        yield substitution
        return

    name, arguments = body[0]

    for fact_name, fact_arguments in list(facts):
        if name == fact_name and len(arguments) == len(fact_arguments):
            new_sub = unify(
                arguments,
                fact_arguments,
                substitution.copy()
            )

            if new_sub is not None:
                yield from match_body(body[1:], new_sub)

def forward_chaining(query):
    while True:
        new_facts = set()

        for body, head in rules:
            for sub in match_body(body, {}):
                name, arguments = head

                values = tuple(
                    sub.get(arg, arg) for arg in arguments
                )

                new_facts.add((name, values))

        new_facts -= facts

        if not new_facts:
            break

        facts.update(new_facts)

    return query in facts

def make_query(text):
    s = clean(text)

    m = re.fullmatch(
        r"(.+?) (likes|loves|hates|knows|helps|owns|teaches|visits) (.+)",
        s
    )
    if m:
        subject, relation, obj = m.groups()
        return (relation, (entity(subject), entity(obj)))

    m = re.fullmatch(r"(.+?) can (.+)", s)
    if m:
        subject, action = m.groups()
        return ("can_" + predicate(action), (entity(subject),))

    m = re.fullmatch(r"(.+?) is (?:an? )?(.+)", s)
    if m:
        subject, category = m.groups()
        return (predicate(category), (entity(subject),))

    return None

print("FORWARD REASONING")

n = int(input("Enter number of statements: "))

for i in range(n):
    sentence = input("Enter statement " + str(i + 1) + ": ")

    if not parse(sentence):
        print("Statement format not supported:", sentence)

query_text = input("Enter query: ")
query = make_query(query_text)

if query is None:
    print("\nQuery format not supported.")
elif forward_chaining(query):
    print("\nQuery is proved.")
else:
    print("\nQuery could not be proved.")


output:

FORWARD REASONING
Enter number of statements: 7
Enter statement 1:  It is a crime for an American to sell weapons to hostile nations
Enter statement 2: Country A has some missiles
Enter statement 3: All of the missiles were sold to country A by Robert
Enter statement 4: Missiles are weapons
Enter statement 5:  Enemy of America is known as hostile
Enter statement 6: Robert is an American
Enter statement 7: Country A is an enemy of America
Enter query:  Robert is criminal

Query is proved.
