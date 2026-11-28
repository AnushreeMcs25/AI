
import matplotlib.pyplot as plt
premises = [
    "~Eats(x) | Likes(John,x)",
    "Food(Apple)",
    "Food(Vegetables)",
    "~Eats(y,z) | Killed(y) | Food(z)",
    "Eats(Anil,Peanuts)",
    "Alive(Anil)",
    "~Eats(Anil,w) | Eats(Harry,w)",
    "Killed(g) | Alive(g)",
    "~Alive(k) | ~Killed(k)"
]

query = "Likes(John,Peanuts)"


fig, ax = plt.subplots(figsize=(10, 7))

pos = {
    "a": (0.8, 6),
    "b": (3.0, 6),
    "c": (1.9, 5),
    "d": (4.2, 5),
    "e": (2.8, 4),
    "f": (5.0, 4),
    "g": (3.9, 3),
    "h": (5.9, 3),
    "i": (4.9, 2),
    "j": (7.0, 2),
    "empty": (5.95, 1)
}

labels = {
    "a": "~likes(John, Peanuts)",
    "b": "~food(x) V likes(John, x)",
    "c": "~food(Peanuts)",
    "d": "~eats(y, z) V killed(y) V food(z)",
    "e": "~eats(y, Peanuts) V killed(y)",
    "f": "eats(Anil, Peanuts)",
    "g": "killed(Anil)",
    "h": "~alive(k) V ~killed(k)",
    "i": "~alive(Anil)",
    "j": "alive(Anil)",
    "empty": "{ }"
}

edges = [
    ("a", "c", ""),
    ("b", "c", "{Peanuts/x}"),
    ("c", "e", ""),
    ("d", "e", "{Peanuts/z}"),
    ("e", "g", ""),
    ("f", "g", "{Anil/y}"),
    ("g", "i", ""),
    ("h", "i", "{Anil/k}"),
    ("i", "empty", ""),
    ("j", "empty", "")
]


for start, end, sub in edges:

    x1, y1 = pos[start]
    x2, y2 = pos[end]

    ax.plot(
        [x1, x2],
        [y1, y2],
        color="black",
        linewidth=1
    )

    if sub:
        ax.text(
            (x1+x2)/2,
            (y1+y2)/2,
            sub,
            fontsize=9,
            ha="center",
            bbox=dict(facecolor="white", edgecolor="none")
        )


for key, value in labels.items():

    x, y = pos[key]

    ax.text(
        x, y,
        value,
        fontsize=9,
        ha="center",
        va="center"
    )


ax.text(
    6.35, 0.65,
    "Hence proved.",
    fontsize=11,
    fontweight="bold"
)

ax.axis("off")
ax.set_xlim(0, 8.2)
ax.set_ylim(0.3, 6.6)

plt.title("Proof by Resolution", fontsize=16)
plt.tight_layout()
plt.show()


output :

