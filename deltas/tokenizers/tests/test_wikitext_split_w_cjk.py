from nose.tools import eq_

from ..wikitext_split_w_cjk import wikitext_split_w_cjk


def test_chinese():
    input = "长岛三百周年半美元是美国铸币局1936年生产的50美分纪念币，" + \
            "旨在纪念欧洲移民定居长岛三百周年。"
    expected = [('长岛', 'cjk_word'),
                ('三百', 'cjk_word'),
                ('周年', 'cjk_word'),
                ('半', 'cjk_word'),
                ('美元', 'cjk_word'),
                ('是', 'cjk_word'),
                ('美国', 'cjk_word'),
                ('铸币', 'cjk_word'),
                ('局', 'cjk_word'),
                ('1936', 'number'),
                ('年', 'cjk_word'),
                ('生产', 'cjk_word'),
                ('的', 'cjk_word'),
                ('50', 'number'),
                ('美分', 'cjk_word'),
                ('纪念币', 'cjk_word'),
                ('，', 'etc'),
                ('旨在', 'cjk_word'),
                ('纪念', 'cjk_word'),
                ('欧洲', 'cjk_word'),
                ('移民', 'cjk_word'),
                ('定居', 'cjk_word'),
                ('长岛', 'cjk_word'),
                ('三百', 'cjk_word'),
                ('周年', 'cjk_word'),
                ('。', 'japan_punct')]

    tokens = list(wikitext_split_w_cjk.tokenize(input))

    for token, (s, t) in zip(tokens, expected):
        print(repr(token), (s, t))
        eq_(token, s)
        eq_(token.type, t)


def test_japanese():
    input = "日本語の俳句（はいく）とは、季語（有季）及び五・七・五（十七音）" + \
            "を主とした定型を基本とする定型詩である。江戸時代には十七文字と呼称され、" + \
            "現代では十七音とも表記される[1]。和歌や連句（俳諧連歌）の発句と同様に、" + \
            "俳句は発生の時点で無季（雑）の作品も存在しており、無季俳句といわれる。有季定型" + \
            "性を捨象する形で派生した自由律俳句もある。また、多くの外国語でも俳句は作られて" + \
            "いるが、外国語では季節感のある言葉でも季語の本意・本情が成立しがたく、しかも五" + \
            "・七・五では切れや季語が活きる短さにならない言語が多いため、日本で言うところの" + \
            "無季自由律俳句が多い。世界最短の定型詩のうちの一つとされる。俳句を詠む（作る）人を俳人と呼ぶ。 "

    expected = [('日本語', 'cjk_word'),
                ('の', 'cjk_word'),
                ('俳句', 'cjk_word'),
                ('（', 'etc'),
                ('は', 'cjk_word'),
                ('いく', 'cjk_word'),
                ('）', 'etc'),
                ('と', 'cjk_word'),
                ('は', 'cjk_word'),
                ('、', 'japan_punct'),
                ('季語', 'cjk_word'),
                ('（', 'etc'),
                ('有季', 'cjk_word'),
                ('）', 'etc'),
                ('及び', 'cjk_word'),
                ('五', 'cjk_word'),
                ('・', 'cjk_word'),
                ('七', 'cjk_word'),
                ('・', 'cjk_word'),
                ('五', 'cjk_word'),
                ('（', 'etc'),
                ('十七', 'cjk_word'),
                ('音', 'cjk_word'),
                ('）', 'etc'),
                ('を', 'cjk_word'),
                ('主', 'cjk_word'),
                ('と', 'cjk_word'),
                ('し', 'cjk_word'),
                ('た', 'cjk_word'),
                ('定型', 'cjk_word'),
                ('を', 'cjk_word'),
                ('基本', 'cjk_word'),
                ('と', 'cjk_word'),
                ('する', 'cjk_word'),
                ('定型詩', 'cjk_word'),
                ('で', 'cjk_word'),
                ('ある', 'cjk_word'),
                ('。', 'japan_punct'),
                ('江戸', 'cjk_word'),
                ('時代', 'cjk_word'),
                ('に', 'cjk_word'),
                ('は', 'cjk_word'),
                ('十七', 'cjk_word'),
                ('文字', 'cjk_word'),
                ('と', 'cjk_word'),
                ('呼称', 'cjk_word'),
                ('さ', 'cjk_word'),
                ('れ', 'cjk_word'),
                ('、', 'japan_punct'),
                ('現代', 'cjk_word'),
                ('で', 'cjk_word'),
                ('は', 'cjk_word'),
                ('十七', 'cjk_word'),
                ('音', 'cjk_word'),
                ('とも', 'cjk_word'),
                ('表記', 'cjk_word'),
                ('さ', 'cjk_word'),
                ('れる', 'cjk_word'),
                ('[', 'brack_open'),
                ('1', 'number'),
                (']', 'brack_close'),
                ('。', 'japan_punct'),
                ('和歌', 'cjk_word'),
                ('や', 'cjk_word'),
                ('連句', 'cjk_word'),
                ('（', 'etc'),
                ('俳諧', 'cjk_word'),
                ('連歌', 'cjk_word'),
                ('）', 'etc'),
                ('の', 'cjk_word'),
                ('発句', 'cjk_word'),
                ('と', 'cjk_word'),
                ('同様', 'cjk_word'),
                ('に', 'cjk_word'),
                ('、', 'japan_punct'),
                ('俳句', 'cjk_word'),
                ('は', 'cjk_word'),
                ('発生', 'cjk_word'),
                ('の', 'cjk_word'),
                ('時点', 'cjk_word'),
                ('で', 'cjk_word'),
                ('無季', 'cjk_word'),
                ('（', 'etc'),
                ('雑', 'cjk_word'),
                ('）', 'etc'),
                ('の', 'cjk_word'),
                ('作品', 'cjk_word'),
                ('も', 'cjk_word'),
                ('存在', 'cjk_word'),
                ('し', 'cjk_word'),
                ('て', 'cjk_word'),
                ('おり', 'cjk_word'),
                ('、', 'japan_punct'),
                ('無季', 'cjk_word'),
                ('俳句', 'cjk_word'),
                ('と', 'cjk_word'),
                ('いわ', 'cjk_word'),
                ('れる', 'cjk_word'),
                ('。', 'japan_punct'),
                ('有季', 'cjk_word'),
                ('定型', 'cjk_word'),
                ('性', 'cjk_word'),
                ('を', 'cjk_word'),
                ('捨象', 'cjk_word'),
                ('する', 'cjk_word'),
                ('形', 'cjk_word'),
                ('で', 'cjk_word'),
                ('派生', 'cjk_word'),
                ('し', 'cjk_word'),
                ('た', 'cjk_word'),
                ('自由', 'cjk_word'),
                ('律', 'cjk_word'),
                ('俳句', 'cjk_word'),
                ('も', 'cjk_word'),
                ('ある', 'cjk_word'),
                ('。', 'japan_punct'),
                ('また', 'cjk_word'),
                ('、', 'japan_punct'),
                ('多く', 'cjk_word'),
                ('の', 'cjk_word'),
                ('外国語', 'cjk_word'),
                ('で', 'cjk_word'),
                ('も', 'cjk_word'),
                ('俳句', 'cjk_word'),
                ('は', 'cjk_word'),
                ('作ら', 'cjk_word'),
                ('れ', 'cjk_word'),
                ('て', 'cjk_word'),
                ('いる', 'cjk_word'),
                ('が', 'cjk_word'),
                ('、', 'japan_punct'),
                ('外国語', 'cjk_word'),
                ('で', 'cjk_word'),
                ('は', 'cjk_word'),
                ('季節感', 'cjk_word'),
                ('の', 'cjk_word'),
                ('ある', 'cjk_word'),
                ('言葉', 'cjk_word'),
                ('で', 'cjk_word'),
                ('も', 'cjk_word'),
                ('季語', 'cjk_word'),
                ('の', 'cjk_word'),
                ('本意', 'cjk_word'),
                ('・', 'cjk_word'),
                ('本', 'cjk_word'),
                ('情', 'cjk_word'),
                ('が', 'cjk_word'),
                ('成立', 'cjk_word'),
                ('し', 'cjk_word'),
                ('がたく', 'cjk_word'),
                ('、', 'japan_punct'),
                ('しかも', 'cjk_word'),
                ('五', 'cjk_word'),
                ('・', 'cjk_word'),
                ('七', 'cjk_word'),
                ('・', 'cjk_word'),
                ('五', 'cjk_word'),
                ('で', 'cjk_word'),
                ('は', 'cjk_word'),
                ('切れ', 'cjk_word'),
                ('や', 'cjk_word'),
                ('季語', 'cjk_word'),
                ('が', 'cjk_word'),
                ('活きる', 'cjk_word'),
                ('短', 'cjk_word'),
                ('さ', 'cjk_word'),
                ('に', 'cjk_word'),
                ('なら', 'cjk_word'),
                ('ない', 'cjk_word'),
                ('言語', 'cjk_word'),
                ('が', 'cjk_word'),
                ('多い', 'cjk_word'),
                ('ため', 'cjk_word'),
                ('、', 'japan_punct'),
                ('日本', 'cjk_word'),
                ('で', 'cjk_word'),
                ('言う', 'cjk_word'),
                ('ところ', 'cjk_word'),
                ('の', 'cjk_word'),
                ('無季', 'cjk_word'),
                ('自由', 'cjk_word'),
                ('律', 'cjk_word'),
                ('俳句', 'cjk_word'),
                ('が', 'cjk_word'),
                ('多い', 'cjk_word'),
                ('。', 'japan_punct'),
                ('世界', 'cjk_word'),
                ('最短', 'cjk_word'),
                ('の', 'cjk_word'),
                ('定型詩', 'cjk_word'),
                ('の', 'cjk_word'),
                ('うち', 'cjk_word'),
                ('の', 'cjk_word'),
                ('一', 'cjk_word'),
                ('つ', 'cjk_word'),
                ('と', 'cjk_word'),
                ('さ', 'cjk_word'),
                ('れる', 'cjk_word'),
                ('。', 'japan_punct'),
                ('俳句', 'cjk_word'),
                ('を', 'cjk_word'),
                ('詠む', 'cjk_word'),
                ('（', 'etc'),
                ('作る', 'cjk_word'),
                ('）', 'etc'),
                ('人', 'cjk_word'),
                ('を', 'cjk_word'),
                ('俳人', 'cjk_word'),
                ('と', 'cjk_word'),
                ('呼ぶ', 'cjk_word'),
                ('。', 'japan_punct'),
                (' ', 'whitespace')]

    tokens = list(wikitext_split_w_cjk.tokenize(input))

    for token, (s, t) in zip(tokens, expected):
        print(repr(token), (s, t))
        eq_(token, s)
        eq_(token.type, t)


def test_korean():
    input = "국어사 자료에서 ‘김치’가 소급하는 최초의 형태는 16세기의 " + \
            "‘딤치’이다. 이 단어는 한자어 ‘침채(沈菜)’에서 온 말인데, ‘딤치’는 " + \
            "16세기보는 훨씬 이전의 한자음을 반영한 것이다. 17세기에 나타나는 " + \
            "‘짐치’는 이례적인데, 아마 경상 방언형이 아닌가 한다. 왜냐하면 서울 말에서 " + \
            "‘디’가 ‘지’로 바뀐 구개음화는 17세기 말에서 18세기초에 일반적으로 일어났기 때문이다. "

    expected = [('국어', 'cjk_word'),
                ('사', 'cjk_word'),
                (' ', 'whitespace'),
                ('자료', 'cjk_word'),
                ('에서', 'cjk_word'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('김치', 'cjk_word'),
                ('’', 'cjk_word'),
                ('가', 'cjk_word'),
                (' ', 'whitespace'),
                ('소급', 'cjk_word'),
                ('하는', 'cjk_word'),
                (' ', 'whitespace'),
                ('최초', 'cjk_word'),
                ('의', 'cjk_word'),
                (' ', 'whitespace'),
                ('형태', 'cjk_word'),
                ('는', 'cjk_word'),
                (' ', 'whitespace'),
                ('16', 'number'),
                ('세기', 'cjk_word'),
                ('의', 'cjk_word'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('딤치', 'cjk_word'),
                ('’', 'cjk_word'),
                ('이다', 'cjk_word'),
                ('.', 'period'),
                (' ', 'whitespace'),
                ('이', 'cjk_word'),
                (' ', 'whitespace'),
                ('단어', 'cjk_word'),
                ('는', 'cjk_word'),
                (' ', 'whitespace'),
                ('한자어', 'cjk_word'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('침채', 'cjk_word'),
                ('(', 'paren_open'),
                ('沈菜', 'cjk_word'),
                (')', 'paren_close'),
                ('’', 'etc'),
                ('에서', 'cjk_word'),
                (' ', 'whitespace'),
                ('온', 'cjk_word'),
                (' ', 'whitespace'),
                ('말', 'cjk_word'),
                ('인데', 'cjk_word'),
                (',', 'comma'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('딤치', 'cjk_word'),
                ('’', 'cjk_word'),
                ('는', 'cjk_word'),
                (' ', 'whitespace'),
                ('16', 'number'),
                ('세', 'cjk_word'),
                ('기보', 'cjk_word'),
                ('는', 'cjk_word'),
                (' ', 'whitespace'),
                ('훨씬', 'cjk_word'),
                (' ', 'whitespace'),
                ('이전', 'cjk_word'),
                ('의', 'cjk_word'),
                (' ', 'whitespace'),
                ('한', 'cjk_word'),
                ('자음', 'cjk_word'),
                ('을', 'cjk_word'),
                (' ', 'whitespace'),
                ('반영', 'cjk_word'),
                ('한', 'cjk_word'),
                (' ', 'whitespace'),
                ('것', 'cjk_word'),
                ('이다', 'cjk_word'),
                ('.', 'period'),
                (' ', 'whitespace'),
                ('17', 'number'),
                ('세기', 'cjk_word'),
                ('에', 'cjk_word'),
                (' ', 'whitespace'),
                ('나타나는', 'cjk_word'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('짐치', 'cjk_word'),
                ('’', 'cjk_word'),
                ('는', 'cjk_word'),
                (' ', 'whitespace'),
                ('이례', 'cjk_word'),
                ('적', 'cjk_word'),
                ('인데', 'cjk_word'),
                (',', 'comma'),
                (' ', 'whitespace'),
                ('아마', 'cjk_word'),
                (' ', 'whitespace'),
                ('경상', 'cjk_word'),
                (' ', 'whitespace'),
                ('방언', 'cjk_word'),
                ('형', 'cjk_word'),
                ('이', 'cjk_word'),
                (' ', 'whitespace'),
                ('아닌가', 'cjk_word'),
                (' ', 'whitespace'),
                ('한다', 'cjk_word'),
                ('.', 'period'),
                (' ', 'whitespace'),
                ('왜냐하면', 'cjk_word'),
                (' ', 'whitespace'),
                ('서울', 'cjk_word'),
                (' ', 'whitespace'),
                ('말', 'cjk_word'),
                ('에서', 'cjk_word'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('디', 'cjk_word'),
                ('’', 'cjk_word'),
                ('가', 'cjk_word'),
                (' ', 'whitespace'),
                ('‘', 'etc'),
                ('지', 'cjk_word'),
                ('’', 'cjk_word'),
                ('로', 'cjk_word'),
                (' ', 'whitespace'),
                ('바뀐', 'cjk_word'),
                (' ', 'whitespace'),
                ('구개음화', 'cjk_word'),
                ('는', 'cjk_word'),
                (' ', 'whitespace'),
                ('17', 'number'),
                ('세기', 'cjk_word'),
                (' ', 'whitespace'),
                ('말', 'cjk_word'),
                ('에서', 'cjk_word'),
                (' ', 'whitespace'),
                ('18', 'number'),
                ('세', 'cjk_word'),
                ('기초', 'cjk_word'),
                ('에', 'cjk_word'),
                (' ', 'whitespace'),
                ('일반', 'cjk_word'),
                ('적', 'cjk_word'),
                ('으로', 'cjk_word'),
                (' ', 'whitespace'),
                ('일어났기', 'cjk_word'),
                (' ', 'whitespace'),
                ('때문', 'cjk_word'),
                ('이다', 'cjk_word'),
                ('.', 'period'),
                (' ', 'whitespace')]

    tokens = list(wikitext_split_w_cjk.tokenize(input))

    for token, (s, t) in zip(tokens, expected):
        print(repr(token), (s, t))
        eq_(token, s)
        eq_(token.type, t)
