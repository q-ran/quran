# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# <img align="right" src="images/tf.png" width="128"/>
# <img align="right" src="images/uu-small.png" width="128"/>
# <img align="right" src="images/dans.png" width="128"/>
#
# # Tutorial
#
# This notebook gets you started with using
# [Text-Fabric](https://annotation.github.io/text-fabric/) for coding in the Quran.
#
# Familiarity with the underlying
# [data model](https://annotation.github.io/text-fabric/tf/about/datamodel.html)
# is recommended.

# ## Installing Text-Fabric
#
# ### Python
#
# You need to have Python on your system. Most systems have it out of the box,
# but alas, that is python2 and we need at least python **3.6**.
#
# Install it from [python.org](https://www.python.org) or from
# [Anaconda](https://www.anaconda.com/download).
#
# ### TF itself
#
# ```
# pip3 install text-fabric
# ```
#
# ### Jupyter notebook
#
# You need [Jupyter](http://jupyter.org).
#
# If it is not already installed:
#
# ```
# pip3 install jupyter
# ```

# ## Tip
# If you start computing with this tutorial, first copy its parent directory to somewhere else,
# outside your `syrnt` directory.
# If you pull changes from the `syrnt` repository later, your work will not be overwritten.
# Where you put your tutorial directory is up till you.
# It will work from any directory.

# %load_ext autoreload
# %autoreload 2

import os
import collections

from tf.app import use

# ## Quran data
#
# Text-Fabric will fetch a standard set of features for you from the newest github release binaries.
#
# The data will be stored in the `text-fabric-data` in your home directory.

# # Load Features
# The data of the corpus is organized in features.
# They are *columns* of data.
# Think of the text as a gigantic spreadsheet, where row 1 corresponds to the
# first word, row 2 to the second word, and so on, for all 100,000+ words.
#
# The letters of each word is a column `form` in that spreadsheet.
#
# The corpus contains ca. 30 columns, not only for the words, but also for
# textual objects, such as *suras*, *ayas*, and *word groups*.
#
# Instead of putting that information in one big table, the data is organized in separate columns.
# We call those columns **features**.

# For the very last version, use `hot`.
#
# For the latest release, use `latest`.
#
# If you have cloned the repos (TF app and data), use `clone`.
#
# If you do not want/need to upgrade, leave out the checkout specifiers.

A = use("quran:clone", checkout="clone", hoist=globals())
# A = use('quran:hot', checkout="hot", hoist=globals())
# A = use('quran:latest', checkout="latest", hoist=globals())
# A = use('quran', hoist=globals())

# ## API
#
# At this point it is helpful to throw a quick glance at the text-fabric API documentation
# (see the links under **API Members** above).
#
# The most essential thing for now is that we can use `F` to access the data in the features
# we've loaded.
# But there is more, such as `N`, which helps us to walk over the text, as we see in a minute.

# # Counting
#
# In order to get acquainted with the data, we start with the simple task of counting.
#
# ## Count all nodes
# We use the
# [`N.walk()` generator](https://annotation.github.io/text-fabric/tf/core/nodes.html#tf.core.nodes.Nodes.walk)
# to walk through the nodes.
#
# We compared corpus to a gigantic spreadsheet, where the rows correspond to the words.
# In Text-Fabric, we call the rows `slots`, because they are the textual positions that can be filled with words.
#
# We also mentioned that there are also more textual objects.
# They are the verses, chapters and books.
# They also correspond to rows in the big spreadsheet.
#
# In Text-Fabric we call all these rows *nodes*, and the `N()` generator
# carries us through those nodes in the textual order.
#
# Just one extra thing: the `info` statements generate timed messages.
# If you use them instead of `print` you'll get a sense of the amount of time that
# the various processing steps typically need.

# +
A.indent(reset=True)
A.info("Counting nodes ...")

i = 0
for n in N.walk():
    i += 1

A.info("{} nodes".format(i))
# -

# ## What are those nodes?
# Every node has a type, like word, or aya, or sura.
# We know that we have approximately 100,000 words and a few other nodes.
# But what exactly are they?
#
# Text-Fabric has two special features, `otype` and `oslots`, that must occur in every Text-Fabric data set.
# `otype` tells you for each node its type, and you can ask for the number of `slot`s in the text.
#
# Here we go!

F.otype.slotType

F.otype.maxSlot

F.otype.maxNode

F.otype.all

C.levels.data

# This is interesting: above you see all the textual objects, with the average size of their objects,
# the node where they start, and the node where they end.

# ## Count individual object types
# This is an intuitive way to count the number of nodes in each type.
# Note in passing, how we use the `indent` in conjunction with `info` to produce neat timed
# and indented progress messages.

# +
A.indent(reset=True)
A.info("counting objects ...")

for otype in F.otype.all:
    i = 0
    A.indent(level=1, reset=True)

    for n in F.otype.s(otype):
        i += 1

    A.info("{:>7} {}s".format(i, otype))

A.indent(level=0)
A.info("Done")
# -

# # Viewing textual objects
#
# We use the A API (the extra power) to peek into the corpus.

# Let's inspect some words.

wordShow = (1000, 10000, 100000)
for word in wordShow:
    A.pretty(word)

# # Feature statistics
#
# `F`
# gives access to all features.
# Every feature has a method
# `freqList()`
# to generate a frequency list of its values, higher frequencies first.
# Here are the parts of speech:

F.pos.freqList()

# # Lexeme matters
#
# ## Top 10 frequent verbs
#
# If we count the frequency of words, we usually mean the frequency of their
# corresponding roots or lexemes.
#
# Let's start with roots.

# +
verbs = collections.Counter()
A.indent(reset=True)
A.info("Collecting data")

for w in F.otype.s("word"):
    if F.pos.v(w) != "verb":
        continue
    verbs[F.root.v(w)] += 1

A.info("Done")
print(
    "".join(
        "{}: {}\n".format(verb, cnt)
        for (verb, cnt) in sorted(verbs.items(), key=lambda x: (-x[1], x[0]))[0:10]
    )
)
# -

# Now the same with lexemes.
# There are several methods for working with lexemes.
#
# ### Method 1: counting words

# +
verbs = collections.Counter()
A.indent(reset=True)
A.info("Collecting data")

for w in F.otype.s("word"):
    if F.pos.v(w) != "verb":
        continue
    verbs[F.lemma.v(w)] += 1

A.info("Done")
print(
    "".join(
        "{}: {}\n".format(verb, cnt)
        for (verb, cnt) in sorted(verbs.items(), key=lambda x: (-x[1], x[0]))[0:10]
    )
)
# -

# ## Lexeme distribution
#
# Let's do a bit more fancy lexeme stuff.
#
# ### Hapaxes
#
# A hapax can be found by inspecting lexemes and see to how many word nodes they are linked.
# If that is number is one, we have a hapax.
#
# We print 10 hapaxes with their gloss.

# +
A.indent(reset=True)

hapax = []
lexIndex = collections.defaultdict(list)

for n in F.otype.s("word"):
    lexIndex[F.lemma.v(n)].append(n)

hapax = dict((lex, occs) for (lex, occs) in lexIndex.items() if len(occs) == 1)

A.info("{} hapaxes found".format(len(hapax)))

for h in sorted(hapax)[0:10]:
    print(f"\t{h}")
# -

# If we want more info on the hapaxes, we get that by means of its *node*.
# The lexIndex dictionary stores the occurrences of a lexeme as a list of nodes.
#
# Let's get the part of speech and the Arabic form of those 10 hapaxes.

for h in sorted(hapax)[0:10]:
    node = hapax[h][0]
    print(f"\t{F.pos.v(node):<12} {F.unicode.v(node)}")

# ### Small occurrence base
#
# The occurrence base of a lexeme are the suras in which it occurs.
# Let's look for lexemes that occur in a single sura.
#
# Oh yes, we have already found the hapaxes, we will skip them here.

# +
A.indent(reset=True)
A.info("Finding single sura lexemes")

lexSuraIndex = {}

for (lex, occs) in lexIndex.items():
    lexSuraIndex[lex] = set(L.u(n, otype="sura")[0] for n in occs)

singleSura = [
    (lex, occs)
    for (lex, occs) in lexIndex.items()
    if len(lexSuraIndex.get(lex, [])) == 1
]
singleSuraWithoutHapax = [(lex, occs) for (lex, occs) in singleSura if len(occs) != 1]

A.info("{} single sura lexemes found".format(len(singleSura)))

for data in (singleSura, singleSuraWithoutHapax):
    print("=====================================")
    for (lex, occs) in sorted(data[0:10]):
        print(
            "{:<15} ({}x) first {:>5} last {:>5}".format(
                lex,
                len(occs),
                "{}:{}".format(*T.sectionFromNode(occs[0])),
                "{}:{}".format(*T.sectionFromNode(occs[-1])),
            )
        )
# -

# ### Confined to suras
#
# As a final exercise with lexemes, lets make a list of all suras, and show their total number of lexemes and
# the number of lexemes that occur exclusively in that sura.

# +
A.indent(reset=True)
A.info("Making sura-lexeme index")

allSura = collections.defaultdict(set)
allLex = set()

for s in F.otype.s("sura"):
    for w in L.d(s, "word"):
        ln = F.lemma.v(w)
        allSura[s].add(ln)
        allLex.add(ln)

A.info("Found {} lexemes".format(len(allLex)))

# +
A.indent(reset=True)
A.info("Finding single sura lexemes")

lexSuraIndex = {}

for (lex, occs) in lexIndex.items():
    lexSuraIndex[lex] = set(L.u(n, otype="sura")[0] for n in occs)

singleSuraLex = collections.defaultdict(set)
for (lex, suras) in lexSuraIndex.items():
    if len(suras) == 1:
        singleSuraLex[list(suras)[0]].add(lex)

singleSura = {sura: len(lexs) for (sura, lexs) in singleSuraLex.items()}

A.info("found {} single sura lexemes".format(sum(singleSura.values())))

# +
print(
    "{:<30} {:>4} {:>4} {:>4} {:>5}\n{}".format(
        "sura name",
        "sura",
        "#all",
        "#own",
        "%own",
        "-" * 51,
    )
)
suraList = []

for s in F.otype.s("sura"):
    suraName = Fs("name@en").v(s)
    sura = T.suraName(s)
    a = len(allSura[s])
    o = singleSura.get(s, 0)
    p = 100 * o / a
    suraList.append((suraName, sura, a, o, p))

for x in sorted(suraList, key=lambda e: (-e[4], -e[2], e[1])):
    print("{:<30} {:>4} {:>4} {:>4} {:>4.1f}%".format(*x))


# -

# ## For all section types
#
# What we did for suras, we can also do for the other section types.
#
# We generalize the task into a function, that accepts the kind of section as parameter.
# Then we can call that function for all our section types.


def lexBase(section):
    # make indices
    lexemesPerSection = {}
    sectionsPerLexeme = {}
    for s in F.otype.s(section):
        for w in L.d(s, otype="word"):
            lex = F.lemma.v(w)
            lexemesPerSection.setdefault(s, set()).add(lex)
            sectionsPerLexeme.setdefault(lex, set()).add(s)

    print(
        "{:<10} {:>4} {:>4} {:>5}\n{}".format(
            section,
            "#all",
            "#own",
            "%own",
            "-" * 26,
        )
    )
    sectionList = []

    for s in F.otype.s(section):
        n = F.number.v(s)
        myLexes = lexemesPerSection[s]
        a = len(myLexes)
        o = len([lex for lex in myLexes if len(sectionsPerLexeme[lex]) == 1])
        p = 100 * o / a
        sectionList.append((n, a, o, p))

    for x in sorted(sectionList, key=lambda e: (-e[3], -e[1], e[0])):
        print("{:<10} {:>4} {:>4} {:>4.1f}%".format(*x))
    print("=" * 26)


for section in (
    "manzil",
    #  'sajda',
    #  'juz',
    #  'ruku',
    #  'hizb',
    #  'page',
):
    lexBase(section)

# # Layer API
# We travel upwards and downwards, forwards and backwards through the nodes.
# The Layer-API (`L`) provides functions: `u()` for going up, and `d()` for going down,
# `n()` for going to next nodes and `p()` for going to previous nodes.
#
# These directions are indirect notions: nodes are just numbers, but by means of the
# `oslots` feature they are linked to slots. One node *contains* an other node, if the one is linked to a set of slots that contains the set of slots that the other is linked to.
# And one if next or previous to an other, if its slots follow of precede the slots of the other one.
#
# `L.u(node)` **Up** is going to nodes that embed `node`.
#
# `L.d(node)` **Down** is the opposite direction, to those that are contained in `node`.
#
# `L.n(node)` **Next** are the next *adjacent* nodes, i.e. nodes whose first slot comes immediately after the last slot of `node`.
#
# `L.p(node)` **Previous** are the previous *adjacent* nodes, i.e. nodes whose last slot comes immediately before the first slot of `node`.
#
# All these functions yield nodes of all possible otypes.
# By passing an optional parameter, you can restrict the results to nodes of that type.
#
# The result are ordered according to the order of things in the text.
#
# The functions return always a tuple, even if there is just one node in the result.
#
# ## Going up
# We go from the first word to the book it contains.
# Note the `[0]` at the end. You expect one book, yet `L` returns a tuple.
# To get the only element of that tuple, you need to do that `[0]`.
#
# If you are like me, you keep forgetting it, and that will lead to weird error messages later on.

firstSura = L.u(1, otype="sura")[0]
print(firstSura)

# And let's see all the containing objects of word 3:

w = 3
for otype in F.otype.all:
    if otype == F.otype.slotType:
        continue
    up = L.u(w, otype=otype)
    upNode = "x" if len(up) == 0 else up[0]
    print("word {} is contained in {} {}".format(w, otype, upNode))

# ## Going next
# Let's go to the next nodes of the first book.

afterFirstSura = L.n(firstSura)
for n in afterFirstSura:
    print(
        "{:>7}: {:<13} first slot={:<6}, last slot={:<6}".format(
            n,
            F.otype.v(n),
            E.oslots.s(n)[0],
            E.oslots.s(n)[-1],
        )
    )
secondSura = L.n(firstSura, otype="sura")[0]

# ## Going previous
#
# And let's see what is right before the second book.

for n in L.p(secondSura):
    print(
        "{:>7}: {:<13} first slot={:<6}, last slot={:<6}".format(
            n,
            F.otype.v(n),
            E.oslots.s(n)[0],
            E.oslots.s(n)[-1],
        )
    )

# ## Going down

# We go to the chapters of the second book, and just count them.

ayas = L.d(secondSura, otype="aya")
print(len(ayas))

# ## The first aya
# We pick the first aya and the first word, and explore what is above and below them.

for n in [1, L.u(1, otype="aya")[0]]:
    A.indent(level=0)
    A.info("Node {}".format(n), tm=False)
    A.indent(level=1)
    A.info("UP", tm=False)
    A.indent(level=2)
    A.info("\n".join(["{:<15} {}".format(u, F.otype.v(u)) for u in L.u(n)]), tm=False)
    A.indent(level=1)
    A.info("DOWN", tm=False)
    A.indent(level=2)
    A.info("\n".join(["{:<15} {}".format(u, F.otype.v(u)) for u in L.d(n)]), tm=False)
A.indent(level=0)
A.info("Done", tm=False)

# # Text API
#
# So far, we have mainly seen nodes and their numbers, and the names of node types.
# You would almost forget that we are dealing with text.
# So let's try to see some text.
#
# In the same way as `F` gives access to feature data,
# `T` gives access to the text.
# That is also feature data, but you can tell Text-Fabric which features are specifically
# carrying the text, and in return Text-Fabric offers you
# a Text API: `T`.
#
# ## Formats
# Arabic text can be represented in a number of ways:
#
# * in transliteration, or in Arabic characters,
# * showing the actual text or only the lexemes, or roots.
#
# If you wonder where the information about text formats is stored:
# not in the program text-fabric, but in the data set.
# It has a feature `otext`, which specifies the formats and which features
# must be used to produce them. `otext` is the third special feature in a TF data set,
# next to `otype` and `oslots`.
# It is an optional feature.
# If it is absent, there will be no `T` API.
#
# Here is a list of all available formats in this data set.

sorted(T.formats)

# ## Using the formats
#
# We can pretty display in other formats:

for word in wordShow:
    A.pretty(word, fmt="text-trans-full")

# Now let's use those formats to print out the first aya of the Quran.

# +
a1 = F.otype.s("aya")[0]

for fmt in sorted(T.formats):
    print("{}:\n\t{}".format(fmt, T.text(a1, fmt=fmt, descend=True)))
# -

# If we do not specify a format, the **default** format is used (`text-orig-full`).

print(T.text(a1))

# ## Whole text in all formats in about a second
# Part of the pleasure of working with computers is that they can crunch massive amounts of data.
# The text of the Quran Bible is a piece of cake.
#
# It takes less than a second to have that cake and eat it.
# In nearly a handful formats.

# +
A.indent(reset=True)
A.info("writing plain text of whole Quran in all formats")

text = collections.defaultdict(list)

for a in F.otype.s("aya"):
    words = L.d(a, "word")
    for fmt in sorted(T.formats):
        text[fmt].append(T.text(words, fmt=fmt))

A.info("done {} formats".format(len(text)))

for fmt in sorted(text):
    print("{}\n{}\n".format(fmt, "\n".join(text[fmt][0:5])))
# -

# ### The full plain text
# We write a few formats to file, in your `Downloads` folder.

orig = "text-orig-full"
trans = "text-trans-full"
for fmt in (orig, trans):
    with open(os.path.expanduser(f"~/Downloads/Quran-{fmt}.txt"), "w") as f:
        f.write("\n".join(text[fmt]))

# !head -n 20 ~/Downloads/Quran-{orig}.txt

# !head -n 20 ~/Downloads/Quran-{trans}.txt

# ## Sections
#
# A section is a sura, and an aya.
# Knowledge of sections is not baked into Text-Fabric.
# The config feature `otext.tf` may specify two or three section levels, and tell
# what the corresponding node types and features are.
#
# From that knowledge it can construct mappings from nodes to sections, e.g. from aya
# nodes to tuples of the form:
#
#     (sura number, aya number)
#
# Here are examples of getting the section that corresponds to a node and vice versa.
#
# **NB:** `sectionFromNode` always delivers a verse specification, either from the
# first slot belonging to that node, or, if `lastSlot`, from the last slot
# belonging to that node.
#

for x in (
    ("sura, aya of first word", T.sectionFromNode(1)),
    ("node of 1:1", T.nodeFromSection((1, 1))),
    ("node of 2:1", T.nodeFromSection((2, 1))),
    ("node of sura 1", T.nodeFromSection((1,))),
    ("section of sura node", T.sectionFromNode(211890)),
    ("section of aya node", T.sectionFromNode(210000)),
    ("section of juz node", T.sectionFromNode(216850)),
    ("idem, now last word", T.sectionFromNode(216850, lastSlot=True)),
):
    print("{:<30} {}".format(*x))

# The other sectional units in the quran, `manzil`, `sajda`, `juz`, `ruku`, `hizb`, `page`
# are not associated with special Text-Fabric functions in this data set, although we could have
# chosen to use two or three of them instead of sura and aya.
#
# But, TF also offers the possibility to define your own sections, independent from and more flexible than
# the sections defined above.
#
# For a bit more on sections, consult the [sections recipe in the cookbook](cookbook/sections.ipynb).

# # Translations
#
# This data source contains English (by Arberry) and Dutch (by Leemhuis) translations of the Quran.
# They are stored in the features `translation@en` and `translation@nl` for aya nodes.
#
# Let's get the translations of sura 107, together with the arabic original.
#
# The translation features are not loaded by default, we load them first.

# +
TF.load("translation@en translation@nl", add=True)

sura = 107

suraNode = T.suraNode(sura)
print(F.name.v(suraNode))

for ayaNode in L.d(suraNode, otype="aya"):
    print(f"{F.number.v(ayaNode)}")
    print(T.text(ayaNode))
    print(Fs("translation@en").v(ayaNode))
    print(Fs("translation@nl").v(ayaNode))
# -

# # Next steps
#
# * **[display](display.ipynb)** become an expert in creating pretty displays of your text structures
# * **[search](search.ipynb)** turbo charge your hand-coding with search templates
# * **[exportExcel](exportExcel.ipynb)** make tailor-made spreadsheets out of your results
# * **[share](share.ipynb)** draw in other people's data and let them use yours
# * **[similarAyas](similarAyas.ipynb)** spot the similarities between lines
# * **[rings](rings.ipynb)** ring structures in sura 2
#
# CC-BY Dirk Roorda
