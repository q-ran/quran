# Provenance

This repository contains text and annotations of the Quran.

The source materials are obtained from these files:

1. file `quranic-corpus-morphology-0.4.txt`,
   obtained from
   [Quranic Arabic Corpus 0.4 (2011) by Kais Dukes](http://corpus.quran.com).
   under license: **Open Source**, see further its
   [release notes](http://corpus.quran.com/releasenotes.jsp).
2. file `quran-data.xml`,
   obtained from
   [tanzil](http://tanzil.net/docs/quran_metadata)
   under license: **Open Source**, see further its
   [project info](http://tanzil.net/docs/tanzil_project).
3. file `quran-uthmani.xml`,
   obtained from
   [tanzil](http://tanzil.net/download/)
   under license: **CC-BY-ND**

4. file `en.arberry.xml`,
   obtained from
   [tanzil](http://tanzil.net/download/)
   under license: **CC-BY-ND**

5. file `nl.leemhuis.xml`,
   obtained from
   [tanzil](http://tanzil.net/download/)
   under license: **CC-BY-ND**

Out of these sources we created a corpus in
[Text-Fabric](https://github.com/annotation/text-fabric)
format.
This corpus contains the unaltered plain unicode text and transliterated texts
as 1. and 2.
It contains all morphological data of 1. but in a column oriented organization,
as prescribed by the
[TF format](https://annotation.github.io/text-fabric/tf/about/fileformats.html).

We used 1. to obtain the full text in transliteration plus the morphological
annotations.

We used 2. to obtain metadata about the individual suras and other sectional
units, such as `juz` and `ruku`.

We used 3. to derive the transliteration mapping. It turned out there is a 1-1
correspondence between the plain arabic text in 3. and the transliterated text in 1.

We used 4. to add an English translation to each aya.

We used 5. to add a Dutch translation to each aya.

# License

We license the resulting corpus as
[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).

You may redistribute modified TF versions of the corpus, as long as you
respect the licenses on the sources.

Here is a more precise statement of the licenses as contained in the sources:

## 1.

```
#  Quranic Arabic Corpus (morphology, version 0.4)
#  Copyright (C) 2011 Kais Dukes
#  License: GNU General Public License
#
#  The Quranic Arabic Corpus includes syntactic and morphological
#  annotation of the Quran, and builds on the verified Arabic text
#  distributed by the Tanzil project.
#
#  TERMS OF USE:
#
#  - Permission is granted to copy and distribute verbatim copies
#    of this file, but CHANGING IT IS NOT ALLOWED.
#
#  - This annotation can be used in any website or application,
#    provided its source (the Quranic Arabic Corpus) is clearly
#    indicated, and a link is made to http://corpus.quran.com to enable
#    users to keep track of changes.
#
#  - This copyright notice shall be included in all verbatim copies
#    of the text, and shall be reproduced appropriately in all works
#    derived from or containing substantial portion of this file.
#
#  Please check updates at: http://corpus.quran.com/download
```

```
#
#  Tanzil Quran Text (Uthmani, version 1.0.2)
#  Copyright (C) 2008-2009 Tanzil.info
#  License: Creative Commons BY-ND 3.0 Unported
#
#  This copy of quran text is carefully produced, highly
#  verified and continuously monitored by a group of specialists
#  at Tanzil project.
#
#  TERMS OF USE:
#
#  - Permission is granted to copy and distribute verbatim copies
#    of this text, but CHANGING IT IS NOT ALLOWED.
#
#  - This quran text can be used in any website or application,
#    provided its source (Tanzil.info) is clearly indicated, and
#    a link is made to http://tanzil.info to enable users to keep
#    track of changes.
#
#  - This copyright notice shall be included in all verbatim copies
#    of the text, and shall be reproduced appropriately in all files
#    derived from or containing substantial portion of this text.
#
#  Please check updates at: http://tanzil.info/updates/
```

## 3.

```
#  Tanzil Quran Text (Uthmani, version 1.0.2)
#  Copyright (C) 2008-2010 Tanzil.net
#  License: Creative Commons Attribution 3.0
#
#  This copy of quran text is carefully produced, highly 
#  verified and continuously monitored by a group of specialists 
#  at Tanzil project.
#
#  TERMS OF USE:
#
#  - Permission is granted to copy and distribute verbatim copies 
#    of this text, but CHANGING IT IS NOT ALLOWED.
#
#  - This quran text can be used in any website or application, 
#    provided its source (Tanzil.net) is clearly indicated, and 
#    a link is made to http://tanzil.net to enable users to keep
#    track of changes.
#
#  - This copyright notice shall be included in all verbatim copies 
#    of the text, and shall be reproduced appropriately in all files 
#    derived from or containing substantial portion of this text.
#
#  Please check updates at: http://tanzil.net/updates/
```

## 4.

```
#=====================================================================
#
#  Quran Translation
#  Name: Arberry
#  Translator: A. J. Arberry
#  Language: English
#  ID: en.arberry
#  Last Update: July 31, 2011
#  Source: Tanzil.net
#
#=====================================================================

```

## 5.

```
#=====================================================================
#
#  Quran Translation
#  Name: Leemhuis
#  Translator: Fred Leemhuis
#  Language: Dutch
#  ID: nl.leemhuis
#  Last Update: August 5, 2012
#  Source: Tanzil.net
#
#=====================================================================
```
