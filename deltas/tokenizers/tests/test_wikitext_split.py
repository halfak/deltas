from nose.tools import eq_

from ..wikitext_split import wikitext_split


def test_wikitext_split():

    input = "As a sentence, this 34 includes punctuation. \n" + \
            "\n" + \
            "==Header!==\n" + \
            "克·科伊尔 し〤。foobar!" + \
            "And then we have another sentence here!\n" + \
            "[//google.com foo] " + \
            "https://website.gov?param=value\n" + \
            "peoples' ain't d’encyclopédie\n" + \
            "[[foo|bar]]" + \
            "mailto:email@email.mail"

    expected = [('As', 'word'),
                (' ', 'whitespace'),
                ('a', 'word'),
                (' ', 'whitespace'),
                ('sentence', 'word'),
                (',', 'comma'),
                (' ', 'whitespace'),
                ('this', 'word'),
                (' ', 'whitespace'),
                ('34', 'number'),
                (' ', 'whitespace'),
                ('includes', 'word'),
                (' ', 'whitespace'),
                ('punctuation', 'word'),
                ('.', 'period'),
                (' ', 'whitespace'),
                ('\n\n', 'break'),
                ('==', 'equals'),
                ('Header', 'word'),
                ('!', 'epoint'),
                ('==', 'equals'),
                ('\n', 'whitespace'),
                ('克', 'cjk'),
                ('·', 'etc'),
                ('科', 'cjk'),
                ('伊', 'cjk'),
                ('尔', 'cjk'),
                (' ', 'whitespace'),
                ('し', 'cjk'),
                ('〤', 'japan_punct'),
                ('。', 'japan_punct'),
                ('foobar', 'word'),
                ('!', 'epoint'),
                ('And', 'word'),
                (' ', 'whitespace'),
                ('then', 'word'),
                (' ', 'whitespace'),
                ('we', 'word'),
                (' ', 'whitespace'),
                ('have', 'word'),
                (' ', 'whitespace'),
                ('another', 'word'),
                (' ', 'whitespace'),
                ('sentence', 'word'),
                (' ', 'whitespace'),
                ('here', 'word'),
                ('!', 'epoint'),
                ('\n', 'whitespace'),
                ('[', 'brack_open'),
                ('//google.com', 'url'),
                (' ', 'whitespace'),
                ('foo', 'word'),
                (']', 'brack_close'),
                (' ', 'whitespace'),
                ('https://website.gov?param=value', 'url'),
                ('\n', 'whitespace'),
                ('peoples\'', 'word'),
                (' ', 'whitespace'),
                ('ain\'t', 'word'),
                (' ', 'whitespace'),
                ('d’encyclopédie', 'word'),
                ('\n', 'whitespace'),
                ('[[', 'dbrack_open'),
                ('foo', 'word'),
                ('|', 'bar'),
                ('bar', 'word'),
                (']]', 'dbrack_close'),
                ('mailto:email@email.mail', 'url')]

    tokens = list(wikitext_split.tokenize(input))

    for token, (s, t) in zip(tokens, expected):
        print(repr(token), (s, t))
        eq_(token, s)
        eq_(token.type, t)
