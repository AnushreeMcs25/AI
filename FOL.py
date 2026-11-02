def is_variable(x):
    return x[0].islower() or x.startswith('?')

def parse(s):
    s = s.strip()
    if '(' not in s:
        return s
    name = s[:s.index('(')].strip()
    args = s[s.index('(') + 1:-1]
    return (name, [parse(x) for x in split_args(args)])

def split_args(s):
    result = []
    start = 0
    depth = 0

    for i, ch in enumerate(s):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            result.append(s[start:i].strip())
            start = i + 1

    result.append(s[start:].strip())
    return result

def apply(term, subst):
    while isinstance(term, str) and term in subst:
        term = subst[term]

    if isinstance(term, tuple):
        return (term[0], [apply(x, subst) for x in term[1]])

    return term

def occurs(var, term, subst):
    term = apply(term, subst)

    if var == term:
        return True

    if isinstance(term, tuple):
        return any(occurs(var, x, subst) for x in term[1])

    return False

def unify(x, y, subst):
    x = apply(x, subst)
    y = apply(y, subst)

    if x == y:
        return subst

    if isinstance(x, str) and is_variable(x):
        if occurs(x, y, subst):
            return None
        subst[x] = y
        return subst

    if isinstance(y, str) and is_variable(y):
        if occurs(y, x, subst):
            return None
        subst[y] = x
        return subst

    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None

        for a, b in zip(x[1], y[1]):
            subst = unify(a, b, subst)

            if subst is None:
                return None

        return subst

    return None

def display(term):
    if isinstance(term, tuple):
        return term[0] + "(" + ", ".join(display(x) for x in term[1]) + ")"
    return term

print("UNIFICATION ALGORITHM")
print("---------------------")

e1 = input("Enter first expression: ")
e2 = input("Enter second expression: ")

try:
    p1 = parse(e1)
    p2 = parse(e2)

    if not isinstance(p1, tuple) or not isinstance(p2, tuple):
        print("Unification Failed")

    elif p1[0] != p2[0] or len(p1[1]) != len(p2[1]):
        print("Unification Failed")

    else:
        result = unify(p1, p2, {})

        if result is None:
            print("Unification Failed")
        else:
            print("\nUnification Successful")
            print("\nSubstitution Set:")

            if result:
                for key, value in result.items():
                    print(key, "=", display(value))
            else:
                print("NIL")

            print("\nUnified Expression 1:", display(apply(p1, result)))
            print("Unified Expression 2:", display(apply(p2, result)))

except:
    print("Invalid Expression")



output1:
UNIFICATION ALGORITHM
---------------------
Enter first expression: P(f(a),g(y))
Enter second expression: P(X,X)
Unification Failed



output 2:
UNIFICATION ALGORITHM
---------------------
Enter first expression: Q(a,g(x,a),f(y))
Enter second expression: Q(a,g(f(b),a),x)

Unification Successful

Substitution Set:
x = f(b)
y = b

Unified Expression 1: Q(a, g(f(b), a), f(b))
Unified Expression 2: Q(a, g(f(b), a), f(b))
