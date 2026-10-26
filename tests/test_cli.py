"""scripts/quettamin.py: the command line reads the built data."""
import contextlib
import io
import unittest

from tests.support import ROOT  # noqa: F401  (puts the project on sys.path)
from scripts import quettamin


def call(*argv) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        quettamin.main(list(argv))
    return out.getvalue()


class CommandLine(unittest.TestCase):
    def test_word(self):
        self.assertIn('id 3983103205', call('word', 'ereb'))

    def test_reconstruct(self):
        out = call('reconstruct', 'erinqua', '--to', 'sindarin/late/3')
        self.assertIn('ereb', out.split('→')[1].splitlines()[1])

    def test_affix_as_argument(self):
        out = call('compose', 'cen-', '-ima', '--n', '2')
        self.assertIn('kēnima', out)
        self.assertIn('производных', call('affix', '-ima'))

    def test_bad_period(self):
        with self.assertRaises(SystemExit):
            call('reconstruct', 'lindë', '--to', 'quenya/late/9')


if __name__ == '__main__':
    unittest.main()
