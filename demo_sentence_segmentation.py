import mwparserfromhell as mwp
from deltas.segmenters import (MatchableSegment,
                               ParagraphsSentencesAndWhitespace)
from deltas.tokenizers import wikitext_split
from mwparserfromhell.nodes import Wikilink

text = """{{Redirect-distinguish|Biological science|life science}}
{{Other uses}}
{{pp-semi-indef}}
{{pp-move-indef}}

{| class="infobox" style="width: 280px;"
|-
|
{| cellpadding=0 cellspacing=0
|-
|[[File:EscherichiaColi NIAID.jpg|alt=microscopic view of E. Coli|135px]]
|[[File:Thompson's Gazelle.jpeg|alt=a Thompson's Gazelle in profile
 facing right|140px]]
|-
|[[File:Goliath beetle.jpg|alt=a Goliath beetle facing up with white
 stripes on carapace|135px]]
|[[File:Tree Fern.jpg|alt=A tree fern unrolling a new frond|140px]]
|}
|-
| Biology deals with the study of the many living [[organism]]s.
* top: ''[[E. coli]]'' bacteria and [[gazelle]]
* bottom: [[Goliathus|Goliath beetle]] and [[tree fern]]
|}

'''Biology''' is a [[natural science]] concerned with the study of
[[life]] and living [[organism]]s, including their structure, function,
growth, [[evolution]], distribution, identification and
[[Taxonomy (biology)|taxonomy]].<ref name=aquarenagloss>Based on definition
from: {{cite web
|url=http://www.bio.txstate.edu/~wetlands/Glossary/glossary.html
|archiveurl=https://web.archive.org/web/20040608113114/http://www.bio.txstate.edu/~wetlands/Glossary/glossary.html
|archivedate=2004-06-08 |title=Aquarena Wetlands Project glossary of terms
|author=<!--Staff writer(s); no by-line.-->
|publisher=Texas State University at San Marcos }}</ref>  Modern biology is a
vast and eclectic field, composed of many
[[#Branches|branches and subdisciplines]]. However, despite the broad scope of
biology, there are certain general and unifying concepts within it that govern
 all study and research, consolidating it into single, coherent field.
 In general, biology recognizes the [[Cell (biology)|cell]] as the basic unit
 of life, [[genes]] as the basic unit of [[heredity]], and [[evolution]] as
 the engine that propels the synthesis and creation of new [[species]]. It is
 also understood today that all the organisms survive by consuming and
 transforming [[energy]] and by [[homeostasis|regulating]] their internal
 environment to maintain a stable and vital condition known as [[homeostasis]].

Sub-disciplines of biology are defined by the scale at which organisms
 are studied, the kinds of organisms studied, and the methods used to
study them: [[biochemistry]] examines the rudimentary chemistry of
life; [[molecular biology]] studies the complex interactions among
biological [[molecule]]s; [[botany]] studies the biology of plants;
[[cellular biology]] examines the basic building-block of all life, the
[[cell (biology)|cell]]; [[physiology]] examines the physical and chemical
functions of [[tissue (biology)|tissues]], [[Organ (anatomy)|organs]],
and [[organ system]]s of an organism; [[evolutionary biology]] examine
s the processes that produced the diversity of life; and [[ecology]]
examines how organisms interact in their
[[environment (biophysical)|environment]].<ref>{{
cite web|
url=http://community.weber.edu/sciencemuseum/pages/life_main.asp
|title=Life Science, Weber State Museum of Natural Science
|publisher=Community.weber.edu |accessdate=2013-10-02}}</ref>

==History==
{{Main|History of biology}}
[[File:Hooke-bluefly.jpg|thumb|alt=A drawing of a fly from facing up, with
 wing detail|A Diagram of a fly from [[Robert Hooke|Robert Hooke's]]
  innovative [[Micrographia]], 1665]]
[[File:Tree of life by Haeckel.jpg|thumb|alt=Ernst Haeckel's pedigree of Man
 family tree from Evolution of Man|[[Ernst Haeckel]]'s Tree of Life (1879)]]
The term ''[[wikt:biology|biology]]'' is derived from the [[Greek Lang
uage|Greek]] word {{lang|grc|[[wikt:βίος|βίος]]}}, ''bios'', "[[life]]
" and the suffix {{lang|grc|[[wikt:-λογία|-λογία]]}}, ''-logia'',
"study of."<ref>{{cite web
|url=http://topics.info.com/Who-coined-the-term-biology_716
|title=Who coined the term biology? |work=Info.com|access
date=2012-06-03}}</ref><ref name=OnlineEtDict>{{cite web|title=biology
|url=http://www.etymonline.com/index.php?term=biology&allowed_in_frame=0
|publisher=[[Online Etymology Dictionary]]}}</ref> The
Latin-language form of the term first appeared in 1736 when Swedish scientist
[[Carl Linnaeus]] (Carl von Linné) used ''biologi'' in his
''Bibliotheca botanica''. It was used again in 1766 in a work entitled
''Philosophiaenaturalis sive physicae: tomus III, continens geologian,
biologian, phytologian generalis'', by
[[Michael Christoph Hanow|Michael Christoph Hanov]], a disciple of
[[Christian Wolff (philosopher)|Christian Wolff
]]. The first German use, ''Biologie'', was in a 1771 translation of
Linnaeus' work. In 1797, Theodor Georg August Roose used the term in
the preface of a book, ''Grundzüge der Lehre van der Lebenskraft''.
[[Karl Friedrich Burdach]] used the term in 1800 in a more restricted
sense of the study of human beings from a morphological, physiological and
 psychological perspective (''Propädeutik zum Studien der gesammten He
ilkunst''). The term came into its modern usage with the six-volume
treatise ''Biologie, oder Philosophie der lebenden Natur'' (1802–22) by
[[Gottfried Reinhold Treviranus]], who announced:<ref name=Richards>{{
cite book|last=Richards|first=Robert J.|title=The Romantic Conception
of Life: Science and Philosophy in the Age of Goethe|year=2002|publish
er=University of Chicago Press|isbn=0-226-71210-9|
url=https://books.google.com/?id=X7N4_i7vrTUC&printsec=frontcover#v=onepage&q&f=false
}}</ref>

:The objects of our research will be the different forms and manifestations
 of life, the conditions and laws under which these phenomena occur, and
  the causes through which they have been effected. The science that concerns
   itself with these objects we will indicate by the name biology [Biologie]
    or the doctrine of life [Lebenslehre].

"""


segmenter = ParagraphsSentencesAndWhitespace()


def process_sentences(segments):
    sentences = []
    for paragraph_or_whitespace in segments:
        if isinstance(paragraph_or_whitespace, MatchableSegment):
            paragraph = paragraph_or_whitespace  # We have a paragraph
            for sentence_or_whitespace in paragraph:
                if isinstance(sentence_or_whitespace, MatchableSegment):
                    sentence = sentence_or_whitespace  # We have a sentence
                    sentences.append(sentence)
    return sentences


def my_strip_code(wikicode):
    return "".join(_my_strip_code(wikicode))


def _my_strip_code(wikicode):

    for node in wikicode.nodes:
        stripped = node.__strip__(normalize=True, collapse=True)
        if isinstance(node, Wikilink):
            stripped = stripped.split("|")[-1]
        if stripped is not None:
            yield str(stripped)


tokens = wikitext_split.tokenize(text)
sentences = process_sentences(segmenter.segment(tokens))

for sentence in sentences:
    raw_sentence = my_strip_code(mwp.parse(str(sentence).replace("\n", "  ")))
    print("  *", raw_sentence)
