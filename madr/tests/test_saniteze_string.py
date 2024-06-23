from madr.tools.sanitize import sanitize_str

inputs = [
    'Machado de Assis',
    'Manuel        Bandeira',
    'Edgar Alan Poe         ',
    'Androides Sonham Com Ovelhas Elétricas?',
    '  breve  história  do tempo ',
    'O mundo assombrado pelos demônios',
]

expected_outputs = [
    'machado de assis',
    'manuel bandeira',
    'edgar alan poe',
    'androides sonham com ovelhas elétricas',
    'breve história do tempo',
    'o mundo assombrado pelos demônios',
]


def test_sanitize_string():
    for i, input_str in enumerate(inputs):
        assert sanitize_str(input_str) == expected_outputs[i]
