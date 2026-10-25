"""Branch configuration: which Eldamo languages form each research branch.

stage orders the languages of one conceptual period from primitive (0)
to the latest stage; era separates Tolkien's late and middle conceptions.
"""

BRANCHES = {
    'quenya': {
        'title': 'Quenya / Qenya',
        'path': {'late': 'Primitive Elvish → Ancient Quenya → Quenya',
                 'middle': 'Middle Primitive Elvish → Middle Ancient Quenya → Middle Quenya'},
        'languages': [
            # code, marker, name, era, stage
            ('p', '✶', 'Primitive Elvish', 'late', 0),
            ('aq', 'AQ.', 'Ancient Quenya', 'late', 1),
            ('q', 'Q.', 'Quenya', 'late', 2),
            ('mp', 'ᴹ✶', 'Middle Primitive Elvish', 'middle', 0),
            ('maq', 'ᴹAQ.', 'Middle Ancient Quenya', 'middle', 1),
            ('mq', 'ᴹQ.', 'Middle Quenya', 'middle', 2),
        ],
    },
    'sindarin': {
        'title': 'Sindarin / Noldorin',
        'path': {'late': 'Primitive Elvish → Ancient Telerin → Old Sindarin → Sindarin',
                 'middle': 'Middle Primitive Elvish → Old Noldorin → Noldorin'},
        'languages': [
            ('p', '✶', 'Primitive Elvish', 'late', 0),
            ('at', 'AT.', 'Ancient Telerin', 'late', 1),
            ('os', 'OS.', 'Old Sindarin', 'late', 2),
            ('s', 'S.', 'Sindarin', 'late', 3),
            ('mp', 'ᴹ✶', 'Middle Primitive Elvish', 'middle', 0),
            ('on', 'ON.', 'Old Noldorin', 'middle', 1),
            ('n', 'N.', 'Noldorin', 'middle', 2),
        ],
    },
}

ERAS = ('late', 'middle')

# Stress model of each stage (shared.stress). Primitive Elvish and the ancient
# stages keep the old initial stress; the stress shift to the Latin-like
# pattern ("before the Q. accent shift", OP1, PE19/58) separates them from
# Quenya and Sindarin proper. Forms that mark stress with an acute keep it.
STRESS = {
    'p': 'initial', 'mp': 'initial',
    'aq': 'initial', 'maq': 'initial', 'q': 'latin', 'mq': 'latin',
    'at': 'initial', 'os': 'initial', 'on': 'initial', 's': 'latin-sindarin', 'n': 'latin-sindarin',
}


def languages(branch: str) -> dict:
    return {code: {'code': code, 'marker': marker, 'name': name, 'era': era, 'stage': stage}
            for code, marker, name, era, stage in BRANCHES[branch]['languages']}
