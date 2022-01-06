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
# ---
#
# To get started: consult [start](start.ipynb)
#
# ---
#
# # Rings
#
# Rings are literary structures of text composition, typically at the sub-sura level.
# They are marked by certain formal characteristics and a semantic structure where elements at the start
# are mirrored semantically at the end.
# The resulting effect is that the crux of the narrative/exposition appears at its center.
#
# This is not an easy concept to deal with computationally, because our dataset has only limited semantic information,
# and the observed patterns are the result of sensitivity of the human mind to a literary and religious text.
#
# So, do not expect to a recipe to identify rokings, but just a scratching of their surface.
#
# Moreover, this notebook is written from the view-point of a non-expert in Islam and Arabic.
# It serves as a testimony of how much perception such a person can muster.
# If you, as an expert, read on, it will become clear how much room for improvement there is.
# The challenge for you is then to strengthen your computational skills, so that you
# can actually make those improvements.
#
# The notebook finishes off by showing how to save, export and share the data you create.

# %load_ext autoreload
# %autoreload 2

# +
import os
import collections
from IPython.display import Markdown, display

from tf.app import use

# -

A = use("quran:clone", checkout="clone", hoist=globals())
# A = use('quran', hoist=globals())

# + [markdown] toc-hr-collapsed=false
# # Exploration
#
# We follow an article by
# Raymond K. Farrin, [*Surat al-Baqara: A Structural Analysis*](https://www.academia.edu/8642515/Surat_al-Baqarah_A_Structural_Analysis)
# -

# ## Trival detail: names of suras
#
# The layman does not know what the Al-Baqara sura is. But there is data!
# Let's print the names of the suras.

for s in F.otype.s("sura"):
    print(f"{F.number.v(s)}: {F.nameTrans.v(s)} ({F.name.v(s)})")

# The article is about sura 2.

sura2 = F.otype.s("sura")[1]

# ## Sections
#
# The article speaks about sections in sura2.
# Those sections apparently form a level between the sura and the aya.
#
# > The sura, 286 verses, consists of nine sections.
#
# ```
# A    1 -  20
# B   21 -  39
# C   40 - 103
# D  104 - 141
# E  142 - 152
# D' 153 - 177
# C' 178 - 253
# B' 254 - 284
# A' 285 - 286
# ```
#
# Can we identify those sections in the data?

# +
sections = [
    (1, 20),
    (21, 39),
    (40, 103),
    (104, 141),
    (142, 152),
    (153, 177),
    (178, 253),
    (254, 284),
    (285, 286),
]

nSections = len(sections)
sectionStarts = {b for (b, e) in sections}
# -

# Apart from suras and ayas, there are other sectional objects in our data, see the
# feature documentation (one of the links after the incantation):
#
# * juz
# * hizb
# * manzil
# * ruku
# * page
# * sajda
#
# Let's see how our sura is divided into these units.
#
# Per unit type we list the how many of those units there are in this sura.

UTYPES = """
juz
hizb
manzil
ruku
page
sajda
""".strip().split()

for uType in UTYPES:
    units = L.d(sura2, otype=uType)
    print(f"{uType.upper():<6}: {len(units):>2} x")

# Now we want to now the exact aya intervals of the hizb, ruku and page units.

for uType in UTYPES:
    units = L.d(sura2, otype=uType)
    if not len(units):
        continue
    print(f"{uType.upper():<6}: {len(units):>2} x")
    for unit in units:
        unitNum = F.number.v(unit)
        ayas = L.d(unit, otype="aya")
        firstAya = F.number.v(ayas[0])
        lastAya = F.number.v(ayas[-1])
        print(f"\t{unitNum:>2}: aya {firstAya:>3}-{lastAya:>3}")

# It seems that the section boundaries all coincide with ruku boundaries.
#
# Let's check the degree in which the section boundaries respect the unit boundaries, for each unit type.
#
# We collect the start ayas for each unit.

# +
startAyas = collections.defaultdict(set)

for uType in UTYPES:
    units = L.d(sura2, otype=uType)
    if not len(units):
        continue
    for unit in units:
        unitNum = F.number.v(unit)
        ayas = L.d(unit, otype="aya")
        firstAya = F.number.v(ayas[0])
        startAyas[uType].add(firstAya)
# -

# Now we count how many section starts are members of the startAyas for each unit type.

# +
agreement = {}

for uType in UTYPES:
    units = L.d(sura2, otype=uType)
    if not len(units):
        continue
    agreement[uType] = len(startAyas[uType] & sectionStarts)

for (uType, agreement) in agreement.items():
    print(
        f"{agreement} out of {nSections} section starts coincide with a {uType} start"
    )
# -

# The rukus are the best match, but two sections cross a ruku boundary:

sorted(sectionStarts - startAyas["ruku"])

# ## First and last lines
#
# We explore the first and last ayas of each section.
#
# We make a list of tuples of their nodes.
#
# Note that the number of an aya is not the same as the node number of the aya.
#
# Node numbers are like barcodes: they identify objects uniquely within the whole universe.
# Aya numbers only identify an aya within its sura.
# But no two ayas have the same node number.
#
# All functions of TF require node numbers, so every now and then we have to move from the
# identifications in front of our nose to the underlying node numbers.
#
# That is what the `T.nodeFromSection()` does: it takes a pair (sura number, aya number) and
# converts it into a unique aya node number.

# +
boundaryAyaNodes = []

for (beginAnum, endAnum) in sections:
    beginA = T.nodeFromSection((2, beginAnum))
    endA = T.nodeFromSection((2, endAnum))
    boundaryAyaNodes.append((beginA, endA))
# -

# Here is the tuple we constructed: an abstract ensemble of barcodes:

boundaryAyaNodes

# Now we ask TF to show them in a more insightful way:

A.table(boundaryAyaNodes)

# But I do not read Arabic, and I want to get a sense of what is going on.
#
# We display them more extensively by using `A.show()` instead.
# Before we make the call, we set up a
# [display parameter](https://annotation.github.io/text-fabric/tf/advanced/options.html)
# that calls up the `translation@en` feature for each aya.

A.displaySetup(extraFeatures="translation@en", prettyTypes=False)

# If we run `A.show()` now, we get a display of ayas and words with translations and morphological information.

A.show(boundaryAyaNodes, baseTypes="group")

# ## Vocative and resumption particles
#
# With my unaided eye I can already see that the start aya tends to start with a vocative particle and the end aya with a resumption particle.

# We now build a table of all ayas in this sura, where we highlight first words if they are a resumption or vocative particle.
# We also highlight the ayas that are the start and end ayas of the sections.

# ### Building a tuple of the objects of interest
#
# We proceed by building a list of aya nodes and their first words.
#
# We also make sets of the ayas where a section starts and where a section ends.

# +
sura2Ayas = L.d(sura2, otype="aya")

ayaTuples = [(a, L.d(a, otype="word")[0]) for a in sura2Ayas]

startAyaNodes = set()
endAyaNodes = set()

for (beginAnum, endAnum) in sections:
    beginA = T.nodeFromSection((2, beginAnum))
    endA = T.nodeFromSection((2, endAnum))
    startAyaNodes.add(beginA)
    endAyaNodes.add(endA)
# -

# ### Defining highlights
#
# We can make a dictionary of nodes and the colors we want to display their objects in.
#
# We can pass that dictionary as a
# [display parameter](https://annotation.github.io/text-fabric/tf/advanced/options.html)

# +
highlights = {}

for a in sura2Ayas:
    firstWord = L.d(a, otype="word")[0]
    isVoc = F.posx.v(firstWord) == "vocative"
    isRes = F.posx.v(firstWord) == "resumption"
    if isVoc or isRes:
        highlights[firstWord] = "lime" if isVoc else "fuchsia"
    if a in startAyaNodes:
        highlights[a] = "gold"
    elif a in endAyaNodes:
        highlights[a] = "lightcoral"
# -

# ### Color display of sections and particles
#
# Ayas that start a section are marked with a bar in *gold*, the ones that end a section have a *light coral* bar.
#
# Resumptive particles at the start of an aya are highlighted in *fuchsia*, the voactive ones in *lime*.

A.table(ayaTuples, start=240, end=260, highlights=highlights)


# ## Semantics
#
# The article says:
#
# > interior sections correspond to each other: the second section corresponds to the second-to-last, and so on concentrically.
#
# and
#
# > By means of concentric patterning, ring composition calls attention to the center. We are drawn to look here for the essential message.
#
# If you don't read Arabic, a translation is the next best way to access the semantics.

# ### Shuffled ayas
#
# For each section, we will list the first three ayas (b1, b2, b3), the middle three (m1, m2, m3) and the last three (e1, e2, e3).
#
# We produce them in the order b1 - e3 - b2 - e2 - b3 - e1 - m1 - m3 - m2.
#
# We also put the first words, if they are particles of the vocative or resumption kind in the table.
#
# Everything will be formatted in a markdown table.


def dm(markdownString):
    display(Markdown(markdownString))


# ### Construction of the table
#
# We walk through the sections and grab all the information we need, and wrap it into a big
# markdown table.

# +
markdown = """
section | aya | position | kind | particle | translation
--- | --- | --- | --- | --- | ---
""".lstrip()

for (i, (beginAnum, endAnum)) in enumerate(sections):
    ayas = {}
    ayas["b1"] = T.nodeFromSection((2, beginAnum))
    ayas["e3"] = T.nodeFromSection((2, endAnum))
    ayas["m2"] = (ayas["b1"] + ayas["e3"]) // 2
    ayas["b2"] = ayas["b1"] + 1
    ayas["b3"] = ayas["b1"] + 2
    ayas["m1"] = ayas["m2"] - 1
    ayas["m3"] = ayas["m2"] + 1
    ayas["e1"] = ayas["e3"] - 2
    ayas["e2"] = ayas["e3"] - 1
    for aName in "b1 e3 b2 e2 b3 e1 m1 m3 m2".split():
        a = ayas[aName]
        w = L.d(a, otype="word")[0]
        posx = F.posx.v(w)
        kind = posx if posx in {"vocative", "resumption"} else None
        particle = None if kind is None else F.ascii.v(w)
        markdown += f"""
{i + 1} | {F.number.v(a)} | {aName} | {kind or '&nbsp;'} | {particle or '&nbsp;'} | {Fs('translation@en').v(a)}
""".lstrip()
# -

# ### Shuffled table display

dm(markdown)

# # Sentiment Mining (primitive)
#
# As the article points out, sections often start by speaking to *good* people or actions, and end with condemning *bad*
# people or actions. Can we base sentiment mining on this idea?

# ## Positivity located in the rings
#
# If a verb, noun or adjective occurs in an e1, e2, or e3 aya, its positivity is deccreased by 1, if it occurs in a b1, b2, b3 it is increased by 1.
#
# This is very crude, because we have taken the ring structure very rigidly.
# In the actual text, there might be ayas that are less pertinent to the ring structure, and the middle of the ring
# does not have to coincide with the exact middle aya of the section.
#
# It is up to the expert to devise additional heuristics that help to identify the rings in a more precise mannner.

# ## Calculating positivity
#
# Now we are going to assign a positivity to all lemmas (verb, noun or adjective) of the sura.

# +
positivity = collections.Counter()
contentCats = {"verb", "noun", "word"}

for (i, (beginAnum, endAnum)) in enumerate(sections):
    ayas = {}
    ayas["b1"] = T.nodeFromSection((2, beginAnum))
    ayas["e3"] = T.nodeFromSection((2, endAnum))
    ayas["m2"] = (ayas["b1"] + ayas["e3"]) // 2
    ayas["b2"] = ayas["b1"] + 1
    ayas["b3"] = ayas["b1"] + 2
    ayas["m1"] = ayas["m2"] - 1
    ayas["m3"] = ayas["m2"] + 1
    ayas["e1"] = ayas["e3"] - 2
    ayas["e2"] = ayas["e3"] - 1
    for aName in "b1 e3 b2 e2 b3 e1 m1 m3 m2".split():
        a = ayas[aName]
        pos = 1 if aName.startswith("b") else -1 if aName.startswith("e") else 0
        for w in L.d(a, otype="word"):
            if F.pos.v(w) in contentCats:
                positivity[F.lemma.v(w)] += pos
# -

# ## Table of lemmas and their positivity
#
# We show the positivity of the lemmas of this sura.

for (lemma, pos) in sorted(
    positivity.items(),
    key=lambda x: (-x[1], x[0]),
)[0:30]:
    print(f"{lemma:<20} has positivity {pos:>2}")

for (lemma, pos) in sorted(
    positivity.items(),
    key=lambda x: (-x[1], x[0]),
)[-30:]:
    print(f"{lemma:<20} has positivity {pos:>2}")


# ## Coloring the sura
#
# Finally, we display the whole sura with words colored according to their positivity or negativity.
#
#

# ### Color gradients
#
# Negative words marked red, and postive ones marked green.
# The farther from zero, the darker the color.
#
# The
# [HSL scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#HSL_colors)
# of color specification is very convenient here.


def posColor(p):
    if p <= -20:
        return "hsl(0, 100%, 50%)"
    if p <= -5:
        return "hsl(0, 90%, 60%)"
    if p <= -3:
        return "hsl(0, 80%, 70%)"
    if p == -2:
        return "hsl(30, 80%, 70%)"
    if p == -1:
        return "hsl(60, 80%, 70%)"
    if p == 0:
        return "hsl(90, 70%, 80%)"
    if p == 1:
        return "hsl(120, 80%, 70%)"
    if p == 2:
        return "hsl(120, 90%, 80%)"
    if p == 3:
        return "hsl(120, 100%, 90%)"
    if p == 4:
        return "hsl(120, 100%, 100%)"
    if p >= 4:
        return "hsl(150, 100%, 100%)"


# ### Computing highlights
#
# We just compute a highlight mapping, much like we did before, but now we are going to highlight
# all words in the sura that have a positivity or negativity.

# +
startAyaNodes = set()
endAyaNodes = set()

for (beginAnum, endAnum) in sections:
    beginA = T.nodeFromSection((2, beginAnum))
    endA = T.nodeFromSection((2, endAnum))
    startAyaNodes.add(beginA)
    endAyaNodes.add(endA)
highlights = {}

for a in sura2Ayas:
    words = L.d(a, otype="word")
    firstWord = words[0]
    isVoc = F.posx.v(firstWord) == "vocative"
    isRes = F.posx.v(firstWord) == "resumption"
    for w in words:
        if w == firstWord:
            if isVoc or isRes:
                highlights[firstWord] = "lime" if isVoc else "fuchsia"
        if F.lemma.v(w) in positivity:
            pos = positivity[F.lemma.v(w)]
            highlights[w] = posColor(pos)
    if a in startAyaNodes:
        highlights[a] = "gold"
    elif a in endAyaNodes:
        highlights[a] = "lightcoral"
# -

# ### Colored sentiment display

A.table(ayaTuples, start=240, end=260, highlights=highlights)

# # Saving data
#
# The real power of TF comes now: we can save the sentiments as a new feature and use it as if it were given with the data set.
#
# We save it to a temporary location, in your downloads folder, and load it from there.
#
# We use
# [TF.save()](https://annotation.github.io/text-fabric/tf/core/fabric.html#tf.core.fabric.FabricCore.save) to save the feature.

# ## Gathering the parameters
#
# We set up all data that `TF.save()` needs.

# +
metaData = {
    "sentiment": {
        "valueType": "int",
        "description": "crude sentiment values for some words in sura 2",
    },
}

edgeFeatures = {}
nodeFeatures = {
    "sentiment": {
        w: positivity[F.lemma.v(w)]
        for w in L.d(sura2, otype="word")
        if F.lemma.v(w) in positivity
    },
}

location = os.path.expanduser("~/Downloads/q-ran/quran/tf")
module = A.version
# -

# ## Performing the save
#
# Now we do the save action:

TF.save(
    metaData=metaData,
    edgeFeatures=edgeFeatures,
    nodeFeatures=nodeFeatures,
    location=location,
    module=module,
)

# ## Checking
#
# Let's check (maybe this does not work on Windows. Open the file explorer and locate the file yourself.

# + language="sh"
# ls -lR ~/Downloads/q-ran/quran/tf
# -

# # Using new data
#
# We are going to load the Quran data again plus the sentiment data

# ## Loading the sentiment data
#
# We use roughly the same statement as when we first loaded the data,
# but now we ask TF also to look into the directory where we saved the sentiments.
#
# We do that by supplying the `locations` and `modules` parameters.
#
# See also
# [A.use()](https://annotation.github.io/text-fabric/tf/advanced/app.html#tf.advanced.app.App)

A = use(
    "quran:clone", checkout="clone", hoist=globals(), locations=location, modules=module
)
# A = use('quran', hoist=globals(), locations=location, modules=module)

# See: the feature `sentiment` got loaded.

# ## Inspecting the sentiment data
#
# Let's inspect it.

F.sentiment.freqList()

# or, a bit more pleasing

for (sent, amount) in F.sentiment.freqList():
    print(f"sentiment {sent:>3} occurs {amount:>3} times")

# ## Displaying sentiment data
#
# Remember the display where we showed the morphology and the translations?
#
# We can make the same display, but now with sentiments shown.
#
# We show only some of the ayas.
#
# We have to add the feature `sentiment` to the features to be displayed.

A.displaySetup(extraFeatures="translation@en sentiment")
A.show(ayaTuples, start=10, end=20)

# ## Searching for sentiment data
#
# We can use the sentiment feature in searches.
#
# Let's look for negative words in ayas starting with a vocative particle.

query = """
sura number=2
  aya
    =: word posx=vocative
    word sentiment<0
"""

results = A.search(query)

# Before we show the results, lets furnish an uncluttered
# [display](https://annotation.github.io/text-fabric/tf/advanced/display.html#tf.advanced.display.displaySetup)
# by suppressing a number of features.

A.displaySetup(extraFeatures="translation@en", suppress="number posx")

# We want to see multiple negative words of an aya highlighted in the same aya, instead of displaying the aya over and over again for each
# negative word. Hence we'll pass `condensed=True`.

A.show(results, start=1, end=5, condensed=True)

# # Export to Excel
#
# It is convenient to export this to Excel, for more intense inspection, aided by all the tools that Excel has to offer for sorting, filtering and making charts.
#
# We use the function
# [A.export()]()
# to do this.
#
# This function takes a list of node tuples, retrieves data about those nodes, and writes it to a .tsv file (tab-separated), that
# can be opened by Excel (even with Arabic characters).

A.export(results)

# The result is now in your Downloads folder, with name `results.tsv`

# + language="sh"
# ls -l ~/Downloads/results.tsv
# head -n 10 ~/Downloads/results.tsv
# -

# Not very pretty, because the file is in utf16 and the terminal does not handle that well.
# But this is the encoding that Excel can use, and there it looks allright:
#
# ![nega](images/negativeExcel.png)

# # Share your data
#
# You can share the new `sentiment` feature in such a way that others can use it easily, even more easy than we just did.
#
# The thing to do is:
#
# * use text-fabric to store your features in a zip file
# * make or use a github repository
# * create a new release and add the zip file to it
#
# These steps are explained in the [share](share.ipynb) tutorial.
# There we made an even cruder feature `sentiment`, with words in all suras, and stored it on GitHub
# in
# [q-ran/exercises/mining/tf](https://github.com/q-ran/exercises/tree/master/mining/tf/0.3).

# # Re-use your data
#
# That means that we can call up that data alongside the Quran data by passing an extra argument to `use()`:

A = use(
    "quran:clone",
    checkout="clone",
    hoist=globals(),
    mod="q-ran/exercises/mining/tf:clone",
)
# A = use('quran', hoist=globals(), mod='q-ran/exercises/mining/tf')

# Note that you can now click on the `sentiment` feature above, which will bring you to
# the repository where it is stored.
# If the creator of the data did a good job, you'll find documentation about `sentiment` in its readme file
# or docs directory.
#
# We check the feature itself for its distribution.

F.sentiment.freqList()

# Note that you can load as many extra modules as you want. If one researcher adds semantic domains, another sentiments, yet another named
# entities, then everybody can use semantics, sentiments and entities in one go.

# ---
#
# All chapters:
#
# * **[start](start.ipynb)** introduction to computing with your corpus
# * **[display](display.ipynb)** become an expert in creating pretty displays of your text structures
# * **[search](search.ipynb)** turbo charge your hand-coding with search templates
# * **[exportExcel](exportExcel.ipynb)** make tailor-made spreadsheets out of your results
# * **[share](share.ipynb)** draw in other people's data and let them use yours
# * **[similarAyas](similarAyas.ipynb)** spot the similarities between lines
# * **rings** ring structures in sura 2
#
# CC-BY Dirk Roorda
