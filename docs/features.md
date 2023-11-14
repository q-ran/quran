# Feature documentation

## otype

There are the following node types

`otype` | description
--- | ---
*`word`* | logical word. It may be a prefix or suffix attached to a main word
*`lex`* | lexeme. These are nodes that are linked to all words with the same lexeme
*`group`* | word group. These are the pieces that are separated by spaces
*`aya`* | a line of text. This is also section level 2
*`sura`* | a book. This is section level 1
*`juz`* | a type of section
*`hizb`* | a type of section
*`manzil`* | a type of section
*`ruku`* | a type of section
*`page`* | a type of section
*`sajda`* | a type of section

## oslots

Links every non-word node to all the word nodes it "contains".
You do not need this feature directly.

## Generic features

name | node type | example values | description
--- | --- | --- | ---
*`number`* | all types except *lex*  | `1` `2` `3` | the number of the section or word group or word

## Section features

name | node type | example values | description
--- | --- | --- | ---
*`name`* | sura | `الفاتحة` `البقرة` `الناس` | name of sura in Arabic
*`nameTrans`* | sura | `Al-Faatiha` `Al-Baqara` `An-Naas` | name of sura in transcribed Arabic
*`nameAscii`* | sura | `AlfAtHp` `Albqrp` `AlnAs` | name of sura in transliterated Arabic
*`name@en`* | sura | `The Opening` `The Cow` `Mankind` | name of sura in English
*`type`* | sura  sajda | `Meccan` `Medinan` (suras); `recommended` `obligatory` (sajdas) | type of sura
*`order`* | sura | `5` `87` `21` | ordinal number of sura
*`translation@en`* | aya | `I serve not what you serve` | english translation of whole aya
*`translation@nl`* | aya | `Ik zal niet dienen wat jullie dienen.` | dutch translation of whole aya

## Word features: text

name | example values | description
--- | --- | ---
*`ascii`* | `bi` `somi` `n~aAsi` | transliterated text of word
*`unicode`* | `بِ` `سْمِ` `نَّاسِ` | arabic text of word (`uthmani`)
*`space`* | ` ` *empty*  | a single space if the word is followed by a space, else empty

## Word/lemma features: lemmatisation

name | node types | example values | description
--- | --- | --- | ---
*`lemma`* | word lex | *None* `{som` `n~aAs` | lemma of word; not all words have a lemma
*`root`* | word | *None* `smw` `nws` | root of word; not all words have a root
*`sp`* | word | *None* `<in~` `kaAn` | ??

## Word features: morphology

### features with part-of-speech tags

The morphological labels in the source have been converted to more
explicit names according to the documentation on 
[Quranic Arabic Corpus](http://corpus.quran.com/releasenotes.jsp),
especially
[part-of-speech tag set](http://corpus.quran.com/documentation/tagset.jsp)
and
[morphological features](http://corpus.quran.com/documentation/morphologicalfeatures.jsp)

There is a rich set of tags for part-of-speech. 
We have split the tags over two features, *`pos`* and *`posx`*, where
*`pos`* contains the primary classification, e.g. `noun`, `particle`, and
*`posx`* contains a subclassification, e.g. `proper`, `cause`, `certainty`.

For a precise division of the original labels into the TF features,
see the
[conversion program](https://github.com/q-ran/quran/blob/master/programs/tfFromMorph.py),
especially the `valTrans` dictionary.

Besides *`pos`*, there are a few other features that have pos tags as values,
they have been treated in the same way: *`a`* and *`ax`*, *`f`* and *`fx`*,
*`l`* and *`lx`*, *`w`* and *`wx`*, and *`n`*.

name | example values | description
--- | --- | ---
*`pos`* | `noun` `particle` `conjunction` | part of speech, main classification
*`posx`* | `proper` `negative` `coordinating` | part of speech, refined classification
*`a`* | *None* `particle` | ??
*`ax`* | *None* `equalization` `interrogative` | ??
*`f`* | *None* `particle` `conjunction` | ??
*`fx`* | *None* `resumption` `coordinating` | ??
*`l`* | *None* `preposition` `prefix` | ??
*`lx`* | *None* `emphatic` `purpose` `imperative` | ??
*`w`* | *None* `particle` `conjunction` | ??
*`wx`* | *None* `resumption` `coordinating` | ??
*`n`* | *None* `emphatic` | ??

### features with nominal morphology

name | example values | description
--- | --- | ---
*`case`* | `nominative` `accusative` `genitive` | grammatical case
*`gn`* | `m` `f` | grammatical gender (masculine, feminine)
*`nu`* | `s` `d` `p` | grammatical number (singular, dual, plural)
*`definite`* | *None* `1` | definiteness (the value is a number) 

### features for verb morphology

name | example values | description
--- | --- | ---
*`formation`* | `II` `V` `X` | stem formation of a verb
*`voice`* | `active` `passive` | voice of a verb
*`tense`* | `perfect` `participle` | tense(like) form of a verb
*`mood`* | `jussive` `subjunctive` | mood form of a verb
*`ps`* | `1` `2` `3` | grammatical person (1st, 2nd, 3rd) (the value is a string, not a number)

### features for other purposes

name | example values | description
--- | --- | ---
*`component`* | `prefix` `stem` `suffix` | role of the word in its word group
*`interjection`* | *None* `allahuma` | assumes the value 5 times only 
