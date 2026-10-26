"""Branch configuration: which Eldamo languages form each research branch.

stage orders the languages of one conceptual period from primitive (0)
to the latest stage; era separates Tolkien's late (1950-73), middle (1930-50)
and early (1910-20s: Qenya, Gnomish) conceptions.
"""

BRANCHES = {
    'quenya': {
        'title': 'Quenya / Qenya',
        'path': {'late': 'Primitive Elvish → Ancient Quenya → Quenya',
                 'middle': 'Middle Primitive Elvish → Middle Ancient Quenya → Middle Quenya',
                 'early': 'Early Primitive Elvish → Early Quenya (Qenya)'},
        'languages': [
            # code, marker, name, era, stage
            ('p', '✶', 'Primitive Elvish', 'late', 0),
            ('aq', 'AQ.', 'Ancient Quenya', 'late', 1),
            ('q', 'Q.', 'Quenya', 'late', 2),
            ('mp', 'ᴹ✶', 'Middle Primitive Elvish', 'middle', 0),
            ('maq', 'ᴹAQ.', 'Middle Ancient Quenya', 'middle', 1),
            ('mq', 'ᴹQ.', 'Middle Quenya', 'middle', 2),
            ('ep', 'ᴱ✶', 'Early Primitive Elvish', 'early', 0),
            ('eq', 'ᴱQ.', 'Early Quenya', 'early', 1),
        ],
    },
    'sindarin': {
        'title': 'Sindarin / Noldorin',
        'path': {'late': 'Primitive Elvish → Ancient Telerin → Old Sindarin → Sindarin',
                 'middle': 'Middle Primitive Elvish → Old Noldorin → Noldorin',
                 'early': 'Early Primitive Elvish → Gnomish'},
        'languages': [
            ('p', '✶', 'Primitive Elvish', 'late', 0),
            ('at', 'AT.', 'Ancient Telerin', 'late', 1),
            ('os', 'OS.', 'Old Sindarin', 'late', 2),
            ('s', 'S.', 'Sindarin', 'late', 3),
            ('mp', 'ᴹ✶', 'Middle Primitive Elvish', 'middle', 0),
            ('on', 'ON.', 'Old Noldorin', 'middle', 1),
            ('n', 'N.', 'Noldorin', 'middle', 2),
            ('ep', 'ᴱ✶', 'Early Primitive Elvish', 'early', 0),
            ('g', 'G.', 'Gnomish', 'early', 1),
        ],
    },
}

ERAS = ('late', 'middle', 'early')
ERA_NAMES = {'late': 'поздняя', 'middle': 'средняя', 'early': 'ранняя'}

# Stress model of each stage (shared.stress). Primitive Elvish and the ancient
# stages keep the old initial stress; the stress shift to the Latin-like
# pattern ("before the Q. accent shift", OP1, PE19/58) separates them from
# Quenya and Sindarin proper. Forms that mark stress with an acute keep it.
STRESS = {
    'p': 'initial', 'mp': 'initial',
    'aq': 'initial', 'maq': 'initial', 'q': 'latin', 'mq': 'latin',
    'at': 'initial', 'os': 'initial', 'on': 'initial', 's': 'latin-sindarin', 'n': 'latin-sindarin',
    # early conception: primitive initial stress; Qenya stress like Quenya; Gnomish not modelled
    'ep': 'initial', 'eq': 'latin', 'g': None,
}


def languages(branch: str) -> dict:
    return {code: {'code': code, 'marker': marker, 'name': name, 'era': era, 'stage': stage}
            for code, marker, name, era, stage in BRANCHES[branch]['languages']}
