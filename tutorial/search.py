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
# # Search Introduction
#
# *Search* in Text-Fabric is a template based way of looking for structural patterns in your dataset.
#
# Within Text-Fabric we have the unique possibility to combine the ease of formulating search templates for
# complicated syntactical patterns with the power of programmatically processing the results.
#
# This notebook will show you how to get up and running.
#
# ## Easy command
#
# Search is as simple as saying (just an example)
#
# ```python
# results = A.search(template)
# A.show(results)
# ```
#
# See all ins and outs in the
# [search template docs](https://annotation.github.io/text-fabric/tf/about/searchusage.html).

# %load_ext autoreload
# %autoreload 2

from tf.app import use

A = use("quran:clone", checkout="clone", hoist=globals())
# A = use('quran', hoist=globals())

# # Basic search command
#
# We start with the most simple form of issuing a query.
# Let's look for the words in sura 1.
#
# All work involved in searching takes place under the hood.

query = """
sura number=1|2|3
  aya number<4
    word
"""
results = A.search(query)
A.table(results, end=10)

# The hyperlinks take us to aya on Tanzil.
#
# Note that we can choose start and/or end points in the results list.

A.table(results, start=8, end=13)

# We can show the results more fully with `show()`.

A.displaySetup(queryFeatures=False)

A.show(results, start=1, end=3)

# We can show all results condensed by *aya*:

A.show(results, condensed=True)

# # Meaningful queries
#
# Let's turn to a bit more meaningful query:
#
# all ayas with a verb immediately followed by the word for Allah.

query = """
aya
  word pos=verb
  <: word pos=noun posx=proper root=Alh
"""

# We run it with `A.search()`:

results = A.search(query)

A.table(results, start=10, end=20)

# Here it comes: the `A.show()` function asks you for some limits (it will not show more than 100 at a time), and then it displays them.
#
# It lists the results as follows:
#
# * a heading showing which result in the sequence of all results this is
# * an overview of the nodes in the tuple of this result
# * a display of all verses that have result material, with the places highlighted that
#   correspond to a node in the result tuple

A.show(results, start=10, end=14, withNodes=True)

# We can also package the results tuples in other things than ayas, e.g. pages:

A.show(results, start=12, end=12, withNodes=True, condensed=True, condenseType="page")

# ---
#
# All chapters:
#
# * **[start](start.ipynb)** introduction to computing with your corpus
# * **[display](display.ipynb)** become an expert in creating pretty displays of your text structures
# * **search** turbo charge your hand-coding with search templates
# * **[exportExcel](exportExcel.ipynb)** make tailor-made spreadsheets out of your results
# * **[share](share.ipynb)** draw in other people's data and let them use yours
# * **[similarAyas](similarAyas.ipynb)** spot the similarities between lines
# * **[rings](rings.ipynb)** ring structures in sura 2
#
# CC-BY Dirk Roorda
