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
# # Sharing data features
#
# ## Explore additional data
#
# Once you analyse a corpus, it is likely that you produce data that others can reuse.
# Maybe you have defined a set of proper name occurrences, or you have computed sentiments.
#
# It is possible to turn these insights into *new features*, i.e. new `.tf` files with values assigned to specific nodes.
#
# ## Make your own data
#
# New data is a product of your own methods and computations in the first place.
# But how do you turn that data into new TF features?
# It turns out that the last step is not that difficult.
#
# If you can shape your data as a mapping (dictionary) from node numbers (integers) to values
# (strings or integers), then TF can turn that data into a feature file for you with one command.
#
# ## Share your new data
# You can then easily share your new features on GitHub, so that your colleagues everywhere
# can try it out for themselves.
#
# You can add such data on the fly, by passing a `mod={org}/{repo}/{path}` parameter,
# or a bunch of them separated by commas.
#
# If the data is there, it will be auto-downloaded and stored on your machine.
#
# Let's do it.

# %load_ext autoreload
# %autoreload 2

# +
import collections
import os

from tf.app import use

# -

A = use("quran:clone", checkout="clone", hoist=globals())
# A = use('quran', hoist=globals())

# # Making data
#
# We illustrate the data creation part by creating a new feature, `sentiment`.
#
# It is not very sensical, but it serves to illustrate the workflow.
#
# We consider ayas that start with a vocative particle as a positive context,
# and ayas that start with a resumptive particle as a negative context.
#
# For each lemma of a noun, verb, or adjective in the corpus,
# we count how often it occurs in a positive context,
# and subtract how many times it occurs in a negative context.
#
# The resulting number is the sentiment.
#
# We use a query to fetch the postive contexts and the negative contexts.

contentTypes = set("verb noun adjective".split())
contentTypeCrit = "|".join(contentTypes)

# +
queryP = f"""
aya
  =: word posx=vocative
  word pos={contentTypeCrit}
"""

queryN = f"""
aya
  =: word posx=resumption
  word pos={contentTypeCrit}
"""
# -

resultsP = A.search(queryP)
resultsN = A.search(queryN)

# Here are the first few results of both:

A.displaySetup(extraFeatures="translation@en")

A.show(resultsP, end=2, condensed=True)

A.show(resultsN, end=2, condensed=True)

# Observe how the positive results indeed have a positive sentiment, and the negative ones are indeed negative.
#
# However, we do not attempt at all to weed out the positive words under negation from the negative contexts.
#
# So our sentiments have to work against a massive "pollution", and are probably not useful.

# +
sentiment = collections.Counter()

for (results, kind) in ((resultsP, 1), (resultsN, -1)):
    for (aya, particle, word) in results:
        sentiment[F.lemma.v(word)] += kind
# -

# Let's check what we found: how many lemma's per sentiment.

# +
sentimentDist = collections.Counter()

for (lemma, sent) in sentiment.items():
    sentimentDist[sent] += 1

for (sent, amount) in sorted(
    sentimentDist.items(),
    key=lambda x: (-x[1], x[0]),
):
    print(f"sentiment {sent:>3} is assigned to {amount:>4} lemmas")
# -

# We show the most negative and most positive sentiments in context.

# +
negaThreshold = -100
posiThreshold = 4

xPlemmas = {lemma for lemma in sentiment if sentiment[lemma] >= posiThreshold}
xNlemmas = {lemma for lemma in sentiment if sentiment[lemma] <= negaThreshold}

xPwords = [
    w
    for w in F.otype.s("word")
    if F.lemma.v(w) in xPlemmas and F.pos.v(w) in contentTypes
]
xNwords = [
    w
    for w in F.otype.s("word")
    if F.lemma.v(w) in xNlemmas and F.pos.v(w) in contentTypes
]

print(f"{len(xPwords)} extremely positive word occurrences")
print(f"{len(xNwords)} extremely negative word occurrences")
# -

# We put the words in their ayas, and show a few.

# +
xPayas = collections.defaultdict(list)
xNayas = collections.defaultdict(list)

for w in xPwords:
    a = L.u(w, otype="aya")[0]
    xPayas[a].append(w)

for w in xNwords:
    a = L.u(w, otype="aya")[0]
    xNayas[a].append(w)

print(f"{len(xPayas)} ayas with extremely positive word occurrences")
print(f"{len(xNayas)} ayas with extremely negative word occurrences")

xPtuples = [(a, *words) for (a, words) in sorted(xPayas.items())]
xNtuples = [(a, *words) for (a, words) in sorted(xNayas.items())]
# -

# We show three ayas of each category

A.show(xPtuples, end=3)

A.show(xNtuples, end=3)

# Probably Allah has a negative sentiment because He occurs in many negative contexts as a punisher.
#
# Anyway, we do not try to be sophisticated here.
#
# We move on to export this sentiment feature.

# # Saving data
#
# The [documentation](https://annotation.github.io/text-fabric/tf/core/fabric.html#tf.core.fabric.FabricCore.save) explains how to save this data into a text-fabric
# data file.
#
# We choose a location where to save it, the `exercises` repository in the `q-ran` organization, in the folder `mining`.
#
# In order to do this, we restart the TF api, but now with the desired output location in the `locations` parameter.

GITHUB = os.path.expanduser("~/github")
ORG = "q-ran"
REPO = "exercises"
PATH = "mining"
VERSION = A.version

# Note the version: we have built the version against a specific version of the data:

A.version

# Later on, we pass this version on, so that users of our data will get the shared data in exactly the same version as their core data.

# We have to specify a bit of metadata for this feature:

# +
metaData = {
    "sentiment": dict(
        valueType="int",
        description="crude sentiments in the Quran",
        creator="Dirk Roorda",
    ),
}

sentimentData = {
    w: sentiment[F.lemma.v(w)]
    for w in F.otype.s("word")
    if F.lemma.v(w) in sentiment and F.pos.v(w) in contentTypes
}
# -

# Now we can give the save command:

TF.save(
    nodeFeatures=dict(sentiment=sentimentData),
    metaData=metaData,
    location=f"{GITHUB}/{ORG}/{REPO}/{PATH}/tf",
    module=VERSION,
)

# # Sharing data
#
# How to share your own data is explained in the
# [documentation](https://annotation.github.io/text-fabric/tf/about/datasharing.html).
#
# Here we show it step by step for the `sentiment` feature.

# ## Zip the data
#
# We need to zip the data in exactly the right directory structure. Text-Fabric can do that for us:

# + language="sh"
#
# text-fabric-zip q-ran/exercises/mining/tf
# -

# Now you have the file in the desired structure in your Downloads folder.
#
# ## Put the data on Github
#
# The next thing is: make a new release in your Github directory, in this case Nino-cunei/exercises, and attach
# the zip file as a binary.
#
# You have to do this in your web browser, on the Github website.
#
# Here is the result for our case:
#
# ![release](images/release.png)

# # Use the data
#
# We can use the data by calling it up when we say `use('quran', ...)`.
#
# Here is how:

A = use(
    "quran:clone",
    checkout="clone",
    hoist=globals(),
    mod="q-ran/exercises/mining/tf:clone",
)
# A = use('quran', hoist=globals(), mod='q-ran/exercises/mining/tf')

# Above you see a new section in the feature list: **q-ran/exercises/mining/tf** with our foreign feature in it: `sentiment`.
#
# Now, suppose did not know much about this feature, then we would like to do a few basic checks:

F.sentiment.freqList()

# Which nodes have a sentiment feature?

{F.otype.v(n) for n in N.walk() if F.sentiment.v(n)}

# Only words have the feature.
#
# Which part of speech do these words have?

{F.pos.v(n) for n in F.otype.s("word") if F.sentiment.v(n)}

# Let's have a look at a table of some words with positive sentiments.

results = A.search(
    """
word sentiment>0
"""
)

A.table(results, start=1, end=5)

results = A.search(
    """
word sentiment<0
"""
)

A.table(results, start=1, end=5)

# Let's get lines with both positive and negative signs:

results = A.search(
    """
aya
  word sentiment>0
  word sentiment<0
"""
)

A.table(results, start=1, end=2, condensed=True)

# With highlights:

# +
highlights = {}

for w in F.otype.s("word"):
    sent = F.sentiment.v(w)
    if sent:
        color = "lightsalmon" if sent < 0 else "mediumaquamarine"
        highlights[w] = color
# -

A.table(results, start=1, end=10, condensed=True, highlights=highlights)

# If we do a pretty display, the `sentiment` feature shows up.

A.show(results, start=1, end=3, condensed=True, withNodes=True, highlights=highlights)

# # All together!
#
# If more researchers have shared data modules, you can draw them all in.
#
# Then you can design queries that use features from all these different sources.
#
# In that way, you build your own research on top of the work of others.

# ---
#
# All chapters:
#
# * **[start](start.ipynb)** introduction to computing with your corpus
# * **[display](display.ipynb)** become an expert in creating pretty displays of your text structures
# * **[search](search.ipynb)** turbo charge your hand-coding with search templates
# * **[exportExcel](exportExcel.ipynb)** make tailor-made spreadsheets out of your results
# * **share** draw in other people's data and let them use yours
# * **[similarAyas](similarAyas.ipynb)** spot the similarities between lines
# * **[rings](rings.ipynb)** ring structures in sura 2
#
# CC-BY Dirk Roorda
