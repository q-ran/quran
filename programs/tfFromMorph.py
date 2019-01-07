import os
import re
from shutil import rmtree

from tf.fabric import Fabric
from tf.writing.transcription import Transcription as tr

# locations

GH_BASE = os.path.expanduser('~/github')
ORG = 'q-ran'
REPO = 'quran'
BASE = f'{GH_BASE}/{ORG}/{REPO}'
SOURCES = f'{BASE}/sources'
MORPH_FILE = 'quranic-corpus-morphology-0.4.txt'
MORPH_PATH = f'{SOURCES}/{MORPH_FILE}'
DATA_FILE = 'quran-data.xml'
DATA_PATH = f'{SOURCES}/{DATA_FILE}'
TF_PATH = f'{BASE}/tf'
VERSION = '0.2'

TRANSLATIONS = dict(
    en=f'{SOURCES}/en.arberry.xml',
    nl=f'{SOURCES}/nl.leemhuis.xml',
)

# config

keyTrans = {
    'LEM': 'lemma',
    '+n': 'n',
}
keySkip = {
    'POS',
}

keyOmit = {
    'PRON',
}

keyOther = {
    'STEM',
    'ROOT',
    'SP',
}

valTrans = {
    'n': {
        'EMPH': 'emphatic',
    },
    'f': {
        'CONJ+': ('conjunction', 'coordinating'),
        'CAUS+': ('particle', 'cause'),
        'REM+': ('particle', 'resumption'),
        'RSLT+': ('particle', 'result'),
        'SUP+': ('particle', 'supplemental'),
    },
    'a': {
        'EQ+': ('particle', 'equalization'),
        'INTG+': ('particle', 'interrogative'),
    },
    'w': {
        'CONJ+': ('conjunction', 'coordinating'),
        'P+': 'preposition',
        'CIRC+': ('particle', 'circumstantial'),
        'COM+': ('particle', 'comitative'),
        'REM+': ('particle', 'resumption'),
        'SUP+': ('particle', 'supplemental'),
    },
    'l': {
        'EMPH+': ('prefix', 'emphatic'),
        'IMPV+': ('prefix', 'imperative'),
        'PRP+': ('prefix', 'purpose'),
        'P+': 'preposition',
    },
    'mood': {
        'SUBJ': 'subjunctive',
        'JUS': 'jussive',
    },
    'pos': {
        'V': 'verb',

        'N': 'noun',
        'PN': ('noun', 'proper'),
        'IMPN': ('noun', 'imperative verbal'),

        'ADJ': 'adjective',

        'PRON': ('pronoun', 'personal'),
        'REL': ('pronoun', 'relative'),
        'DEM': ('pronoun', 'demonstrative'),

        'LOC': ('adverb', 'location'),
        'T': ('adverb', 'time'),

        'CONJ': ('conjunction', 'coordinating'),
        'SUB': ('conjunction', 'subordinating'),

        'DET': 'determiner',

        'P': 'preposition',

        'IMPV': ('prefix', 'imperative'),
        'EMPH': ('prefix', 'emphatic'),
        'PRP': ('prefix', 'purpose'),

        'INL': 'initials',

        'ACC': ('particle', 'accusative'),
        'AMD': ('particle', 'amendment'),
        'ANS': ('particle', 'answer'),
        'AVR': ('particle', 'aversion'),
        'CAUS': ('particle', 'cause'),
        'CERT': ('particle', 'certainty'),
        'CIRC': ('particle', 'circumstantial'),
        'COM': ('particle', 'comitative'),
        'COND': ('particle', 'conditional'),
        'EQ': ('particle', 'equalization'),
        'EXH': ('particle', 'exhortation'),
        'EXL': ('particle', 'explanation'),
        'EXP': ('particle', 'exceptive'),
        'FUT': ('particle', 'future'),
        'INC': ('particle', 'inceptive'),
        'INT': ('particle', 'interpretation'),
        'INTG': ('particle', 'interrogative'),
        'NEG': ('particle', 'negative'),
        'PREV': ('particle', 'preventive'),
        'PRO': ('particle', 'prohibition'),
        'REM': ('particle', 'resumption'),
        'RES': ('particle', 'restriction'),
        'RET': ('particle', 'retraction'),
        'RSLT': ('particle', 'result'),
        'SUP': ('particle', 'supplemental'),
        'SUR': ('particle', 'surprise'),
        'VOC': ('particle', 'vocative'),
    },
}

valIndex = {
    'NOM': (('case', 'nominative'),),
    'ACC': (('case', 'accusative'),),
    'GEN': (('case', 'genitive'),),
    '(II)': (('formation', 'II'),),
    '(III)': (('formation', 'III'),),
    '(IV)': (('formation', 'IV'),),
    '(IX)': (('formation', 'IX'),),
    '(V)': (('formation', 'V'),),
    '(VI)': (('formation', 'VI'),),
    '(VII)': (('formation', 'VII'),),
    '(VIII)': (('formation', 'VIII'),),
    '(X)': (('formation', 'X'),),
    '(XI)': (('formation', 'XI'),),
    '(XII)': (('formation', 'XII'),),
    '+VOC': (('interjection', 'allahuma'),),
    '1P': (('ps', '1'), ('nu', 'p')),
    '1S': (('ps', '1'), ('nu', 's')),
    '2D': (('ps', '2'), ('nu', 'd')),
    '2FD': (('ps', '2'), ('nu', 'd'), ('gn', 'f')),
    '2FP': (('ps', '2'), ('nu', 'p'), ('gn', 'f')),
    '2FS': (('ps', '2'), ('nu', 's'), ('gn', 'f')),
    '2MD': (('ps', '2'), ('nu', 'd'), ('gn', 'm')),
    '2MP': (('ps', '2'), ('nu', 'p'), ('gn', 'm')),
    '2MS': (('ps', '2'), ('nu', 's'), ('gn', 'm')),
    '3D': (('ps', '3'), ('nu', 'd')),
    '3FD': (('ps', '3'), ('nu', 'd'), ('gn', 'f')),
    '3FP': (('ps', '3'), ('nu', 'p'), ('gn', 'f')),
    '3FS': (('ps', '3'), ('nu', 's'), ('gn', 'f')),
    '3MD': (('ps', '3'), ('nu', 'd'), ('gn', 'm')),
    '3MP': (('ps', '3'), ('nu', 'p'), ('gn', 'm')),
    '3MS': (('ps', '3'), ('nu', 's'), ('gn', 'm')),
    'MD': (('nu', 'd'), ('gn', 'm')),
    'MP': (('nu', 'p'), ('gn', 'm')),
    'M': (('gn', 'm'),),
    'MS': (('gn', 'm'), ('nu', 's')),
    'FD': (('nu', 'd'), ('gn', 'f')),
    'FP': (('nu', 'p'), ('gn', 'f')),
    'FS': (('nu', 's'), ('gn', 'f')),
    'F': (('gn', 'f'),),
    'P': (('nu', 'p'),),
    'ACT': (('voice', 'active'),),
    'PASS': (('voice', 'passive'),),
    'IMPF': (('tense', 'imperfect'),),
    'IMPV': (('tense', 'imperative'),),
    'PERF': (('tense', 'perfect'),),
    'PCPL': (('tense', 'participle'),),
    'VN': (('tense', 'verbalNoun'),),
    'INDEF': (('definite', 1),),
    'PREFIX': (('component', 'prefix'),),
    'STEM': (('component', 'main'),),
    'SUFFIX': (('component', 'suffix'),),
    'Al+': (),
    'bi+': (),
    'ha+': (),
    'ka+': (),
    'sa+': (),
    'ta+': (),
    'ya+': (),
}

metaData = {
    '': dict(
        acronym='quran',
        createdBy='Kais Dukes',
        createdDate='2011',
        convertedBy='Dirk Roorda and Cornelis van Lit',
        source1='Morphology: Quranic Arabic Corpus 0.4 (2011) by Kais Dukes',
        source1Url='http://corpus.quran.com',
        license1='Open Source, unspecified, see http://corpus.quran.com/releasenotes.jsp',
        source2='Text: Tanzil Quran Text (Uthmani, version 1.0.2)',
        source2Url='http://tanzil.net/docs/home',
        license2='Creative Commons BY-ND 3.0 Unported',
        description='Quran: plain text plus morphological annotations at the word level',
    ),
    'otext': {
        'sectionFeatures': 'number,number',
        'sectionTypes': 'sura,aya',
        'fmt:text-orig-full': f'{{unicode}}{{space}}',
        'fmt:text-trans-full': f'{{ascii}}{{space}}',
        'fmt:lex-trans-full': f'{{lemma}}{{space}}',
        'fmt:root-trans-full': f'{{root}}{{space}}',
    },
    'otype': {
        'valueType': 'str',
    },
    'oslots': {
        'valueType': 'str',
    },
    'number': {
        'valueType': 'int',
        'description': 'Number of sura, aya, word group, or word',
    },
    'name@en': {
        'valueType': 'str',
        'language': 'english',
        'languageCode': 'en',
        'languageEnglish': 'English',
        'description': 'Name of sura in English',
    },
    'name': {
        'valueType': 'str',
        'language': 'arabic',
        'description': 'Name of sura in Arabic',
    },
    'nameTrans': {
        'valueType': 'str',
        'language': 'arabic',
        'description': 'Name of sura in Arabic, transcribed',
    },
    'nameAscii': {
        'valueType': 'str',
        'language': 'arabic',
        'description': 'Name of sura in Arabic, transliterated',
    },
    'type': {
        'valueType': 'str',
        'description': 'type of sura',
    },
    'order': {
        'valueType': 'int',
        'description': 'ordinal number of sura',
    },
    'ascii': {
        'valueType': 'str',
        'description': 'transliterated text of word',
    },
    'unicode': {
        'valueType': 'str',
        'description': 'unicode arabic text of word',
    },
    'space': {
        'valueType': 'str',
        'description': 'material between this word and the next',
    },
    'lemma': {
        'valueType': 'str',
        'description': 'lemma of word',
    },
    'root': {
        'valueType': 'str',
        'description': 'root of word',
    },
    'case': {
        'valueType': 'str',
        'description': 'case of word',
    },
    'pos': {
        'valueType': 'str',
        'description': 'part-of-speech of word, main class',
        'documentation': 'http://corpus.quran.com/documentation/tagset.jsp',
    },
    'posx': {
        'valueType': 'str',
        'description': 'part-of-speech of word, refined class',
        'documentation': 'http://corpus.quran.com/documentation/tagset.jsp',
    },
    'formation': {
        'valueType': 'str',
        'description': 'stem formation of verb',
    },
    'interjection': {
        'valueType': 'str',
        'description': 'kind of interjection',
    },
    'gn': {
        'valueType': 'str',
        'description': 'gender of word (masculine, feminine)',
    },
    'nu': {
        'valueType': 'str',
        'description': 'number of word (singular, dual, plural)',
    },
    'ps': {
        'valueType': 'str',
        'description': 'person of word (1st, 2nd, 3rd)',
    },
    'voice': {
        'valueType': 'str',
        'description': 'voice of a verb (active, passive)',
    },
    'tense': {
        'valueType': 'str',
        'description': 'tense of a verb (perfect, imperfect, ...)',
    },
    'mood': {
        'valueType': 'str',
        'description': 'mood of a verb (subj, jus, ...)',
    },
    'definite': {
        'valueType': 'int',
        'description': 'whether the word is definite',
    },
    'component': {
        'valueType': 'str',
        'description': 'role of the word in its word group (prefix, main, or suffix)',
    },
    'a': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'ax': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'f': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'fx': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'l': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'lx': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'n': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'w': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'wx': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'sp': {
        'valueType': 'str',
        'description': 'not yet understood',
    },
    'translation@en': {
        'valueType': 'str',
        'description': 'english translation of whole aya',
        'translator': 'Arthur Arberry (1955), https://en.wikipedia.org/wiki/Arthur_John_Arberry',
    },
    'translation@nl': {
        'valueType': 'str',
        'description': 'english translation of whole aya',
        'translator': 'Fred Leemhuis (1989), https://rug.academia.edu/FrederikLeemhuis',
    },
}

# data holders

morphDb = {}
wordFeatures = {}
suraFeatures = {}
sectionFeatures = {}

translations = {}

unknowns = set()
unknownFeatures = set()
unknownPerFeat = {}

posIndex = {}

nodeFeatures = {}
edgeFeatures = {}

attPat = r' ([a-z]+)="([^"]*)"'
attRe = re.compile(attPat)


def readTranslations():
  suraPat = r'<sura(.*?)>(.*?)</sura>'
  suraRe = re.compile(suraPat, re.S)
  ayaPat = r'<aya(.*?)/>'
  ayaRe = re.compile(ayaPat)
  for (lang, source) in sorted(TRANSLATIONS.items()):
    print(f'Read @{lang} translation from {os.path.basename(source)}')
    with open(source) as fh:
      data = fh.read()
    suras = suraRe.findall(data)
    for (suraAttStr, content) in suras:
      suraAtts = dict(attRe.findall(suraAttStr))
      sI = int(suraAtts.get('index', 0))
      ayas = ayaRe.findall(content)
      for aya in ayas:
        ayaAtts = dict(attRe.findall(aya))
        aI = int(ayaAtts.get('index', 0))
        text = (
            ayaAtts.get('text', '')
            .replace('&quot;', '"')
            .replace('&apos;', "'")
            .replace('&lt;', '<')
            .replace('&gt;', '>')
        )
        translations.setdefault(lang, {})[(sI, aI)] = text


def readData():
  print('Reading sura metadata')

  suraPat = r'<sura(.*?)/>'
  suraRe = re.compile(suraPat)
  juzPat = r'<juz(.*?)/>'
  juzRe = re.compile(juzPat)
  hizbPat = r'<quarter(.*?)/>'
  hizbRe = re.compile(hizbPat)
  manzilPat = r'<manzil(.*?)/>'
  manzilRe = re.compile(manzilPat)
  rukuPat = r'<ruku(.*?)/>'
  rukuRe = re.compile(rukuPat)
  pagePat = r'<page(.*?)/>'
  pageRe = re.compile(pagePat)
  sajdaPat = r'<sajda(.*?)/>'
  sajdaRe = re.compile(sajdaPat)

  with open(DATA_PATH) as fh:
    data = fh.read()

  suras = suraRe.findall(data)
  for sura in suras:
    atts = dict(attRe.findall(sura))
    sI = int(atts.get('index', 0))
    suraFeatures[sI] = {
        'name': atts.get('name', ''),
        'nameAscii': tr.from_arabic(atts.get('name', '')),
        'nameTrans': atts.get('tname', ''),
        'name@en': atts.get('ename', ''),
        'type': atts.get('type', ''),
    }
    if 'order' in atts:
      suraFeatures[sI]['order'] = int(atts['order'])
  print(f'Read features for {len(suras)} suras')

  for (sectionName, sectionRe, info) in (
      ('juz', juzRe, ()),
      ('hizb', hizbRe, ()),
      ('manzil', manzilRe, ()),
      ('ruku', rukuRe, ()),
      ('page', pageRe, ()),
      ('sajda', sajdaRe, ('type',)),
  ):
    dest = sectionFeatures.setdefault(sectionName, {})
    sections = sectionRe.findall(data)
    for section in sections:
      atts = dict(attRe.findall(section))
      sI = int(atts.get('index', 0))
      sura = int(atts.get('sura', 0))
      aya = int(atts.get('aya', 0))
      dest[sI] = {'start': (sura, aya)}
      for k in info:
        dest[sI][k] = atts[k]


def readMorph():

  print('Reading morphologically annotated text of the Quran')
  print(f'\t{MORPH_PATH}')

  with open(MORPH_PATH) as fh:
    inPrefix = True
    dataLines = 0
    for (i, line) in enumerate(fh):
      if inPrefix:
        if line.startswith('LOCATION\t'):
          inPrefix = False
          continue
      else:
        dataLines += 1
        (locationRep, form, tag, features) = line.rstrip('\n').split('\t')
        (suraIndex, ayaIndex, groupIndex, wordIndex) = (
            int(x) for x in locationRep[1:-1].split(':')
        )
        morphDb\
            .setdefault(suraIndex, {})\
            .setdefault(ayaIndex, {})\
            .setdefault(groupIndex, {})[wordIndex] = (form, tag, features)

    print(f'Done: {dataLines:>6} data lines')


def doValue(value, features):
  keyValues = valIndex.get(value, None)
  if keyValues is None:
    unknowns.add(value)
  else:
    for (k, v) in keyValues:
      features[k] = v


def adjust(key, value):
  if key in valTrans:
    if value in valTrans[key]:
      return valTrans[key][value]
    unknownPerFeat.setdefault(key, set()).add(value)
    return value
  return value


def parseMorphItem(tag, featureStr):
  features = dict()
  pos = adjust('pos', tag)
  if type(pos) is str:
    features['pos'] = pos
  elif type(pos) is tuple:
    features['pos'] = pos[0]
    features['posx'] = pos[1]
  unknowns = set()
  fItems = featureStr.split('|')
  for fItem in fItems:
    if ':' in fItem:
      (key, value) = fItem.split(':', 1)
      if key in keySkip:
        continue
      if key in keyOmit:
        doValue(value, features)
        continue
      if key not in keyOther and key not in keyTrans and key.lower() not in valTrans:
        unknownFeatures.add(key)
        continue
      keyRep = keyTrans.get(key, key.lower())
      val = adjust(keyRep, value)
      if type(val) is str:
        features[keyRep] = val
      elif type(val) is tuple:
        features[keyRep] = val[0]
        features[f'{keyRep}x'] = val[1]
    else:
      doValue(fItem, features)
  return (features, unknowns)


def parseMorph():
  print('Parsing morphological data')

  global unknowns

  for (sura, suraData) in morphDb.items():
    for (aya, ayaData) in suraData.items():
      for (group, groupData) in ayaData.items():
        for (word, (form, tag, featureStr)) in groupData.items():
          wordFeatures.setdefault((sura, aya, group, word), {})['ascii'] = form
          wordFeatures.setdefault((sura, aya, group, word), {})['unicode'] = tr.to_arabic(form)
          (theseFeatures, theseUnknowns) = parseMorphItem(tag, featureStr)
          for (k, v) in theseFeatures.items():
            wordFeatures.setdefault((sura, aya, group, word), {})[k] = v
          unknowns |= theseUnknowns

  if unknownFeatures:
    feats = ' '.join(unknownFeatures)
    print(f'\tUnknown features: {feats}')
  else:
    print(f'\tAll features known')
  if (unknownPerFeat):
    for feat in sorted(unknownPerFeat):
      vals = ' '.join(sorted(unknownPerFeat[feat]))
      print(f'\tUnknown: {feat}: {vals}')
  if unknowns:
    vals = ' '.join(sorted(unknowns))
    print(f'\tUnknown labels: {vals}')
  if not unknownPerFeat and not unknowns:
    print(f'\tAll feature values known')
  print(f'Done')


def makeTfData():
  print('Making TF data')

  otype = {}
  oslots = {}

  (offsetS, offsetA, offsetG, offsetW) = (0, 0, 0, 0)
  (curS, curA, curG) = (None, None, None)

  for (thisS, thisA, thisG, thisW) in sorted(wordFeatures):
    offsetW += 1
    if (thisS, thisA, thisG) != (curS, curA, curG):
      offsetG += 1
    if (thisS, thisA) != (curS, curA):
      offsetA += 1
    if thisS != curS:
      offsetS += 1
    (curS, curA, curG) = (thisS, thisA, thisG)

  print(f'''
  {offsetS:>6} suras
  {offsetA:>6} ayas
  {offsetG:>6} word groups
  {offsetW:>6} words
''')

  (curS, curA, curG) = (None, None, None)
  (nodeS, nodeA, nodeG, nodeW, nodeL, nodeP) = (0, 0, 0, 0, 0, 0)
  seenL = {}

  for (thisS, thisA, thisG, thisW) in sorted(wordFeatures):
    if nodeW:
      space = (
          ' '
          if thisS == curS and thisA == curA and thisG != curG
          else ''
      )
      nodeFeatures.setdefault('space', {})[nodeW] = space

    nodeW += 1
    otype[nodeW] = 'word'

    nodeFeatures.setdefault('number', {})[nodeW] = thisW
    for (k, v) in wordFeatures.get((thisS, thisA, thisG, thisW), {}).items():
      nodeFeatures.setdefault(k, {})[nodeW] = v
      if k == 'lemma' and v is not None:
        if v not in seenL:
          nodeL += 1
          seenL[v] = nodeL
          otype[offsetW + offsetG + offsetA + offsetS + nodeL] = 'lex'
          nodeFeatures.setdefault(k, {})[offsetW + offsetG + offsetA + offsetS + nodeL] = v
        lex = seenL[v]
        oslots.setdefault(offsetW + offsetG + offsetA + offsetS + lex, set()).add(nodeW)

    if (thisS, thisA, thisG) != (curS, curA, curG):
      nodeG += 1
      otype[offsetW + nodeG] = 'group'
      nodeFeatures.setdefault('number', {})[offsetW + nodeG] = thisG
    oslots.setdefault(offsetW + nodeG, set()).add(nodeW)

    if (thisS, thisA) != (curS, curA):
      posIndex[(thisS, thisA)] = nodeW
      nodeA += 1
      otype[offsetW + offsetG + nodeA] = 'aya'
      nodeFeatures.setdefault('number', {})[offsetW + offsetG + nodeA] = thisA
      for lang in translations:
        nodeFeatures.setdefault(f'translation@{lang}', {})[offsetW + offsetG + nodeA] = (
            translations[lang][(thisS, thisA)]
        )
    oslots.setdefault(offsetW + offsetG + nodeA, set()).add(nodeW)

    if thisS != curS:
      nodeS += 1
      otype[offsetW + offsetG + offsetA + nodeS] = 'sura'
      nodeFeatures.setdefault('number', {})[offsetW + offsetG + offsetA + nodeS] = thisS
      for (k, v) in suraFeatures.get(thisS, {}).items():
        nodeFeatures.setdefault(k, {})[offsetW + offsetG + offsetA + nodeS] = v
    oslots.setdefault(offsetW + offsetG + offsetA + nodeS, set()).add(nodeW)

    (curS, curA, curG) = (thisS, thisA, thisG)

  offsetP = nodeW + nodeG + nodeA + nodeS + nodeL

  for (sectionName, sectionData) in sectionFeatures.items():
    for (sI, data) in sorted(sectionData.items()):
      nodeP += 1
      otype[offsetP + nodeP] = sectionName
      nodeFeatures.setdefault('number', {})[offsetP + nodeP] = sI
      (sura, aya) = data['start']
      startW = posIndex[(sura, aya)]
      endW = (
          posIndex[sectionData[sI + 1]['start']] - 1
          if sI + 1 in sectionData else
          nodeW
      )
      oslots[offsetP + nodeP] = set(range(startW, endW + 1))
      for k in data:
        if k == 'start':
          continue
        nodeFeatures.setdefault(k, {})[offsetP + nodeP] = data[k]

  nodeFeatures['otype'] = otype
  edgeFeatures['oslots'] = oslots

  for f in sorted(nodeFeatures) + sorted(edgeFeatures):
    if f not in metaData:
      print(f'\t!! {f}: no metadata')
    else:
      print(f'\t{f}: type {metaData[f]["valueType"]}')

  for f in metaData:
    if f in {'oslots', 'otype', 'otext', ''}:
      continue
    if f not in nodeFeatures and f not in edgeFeatures:
      print(f'\t!! {f} does not occur in the data')

  print(f'''
  {nodeS:>6} sura nodes
  {nodeA:>6} aya nodes
  {nodeG:>6} word group nodes
  {nodeW:>6} word nodes
  {nodeL:>6} lexeme nodes
  {nodeP:>6} section nodes
''')
  for (sectionName, sectionData) in sectionFeatures.items():
    print(f'  {len(sectionData):>6} {sectionName} nodes')

  fvs = (
      sum(len(nodeFeatures[f]) for f in nodeFeatures)
      +
      sum(len(edgeFeatures[f]) for f in edgeFeatures)
  )
  print(f'Nodes: {nodeW + nodeG + nodeA + nodeS + nodeL + nodeP}')
  print(f'Feature values: {fvs}')


def makeTf():
  if os.path.exists(TF_PATH):
    rmtree(TF_PATH)
  TF = Fabric(locations=[f'{TF_PATH}/{VERSION}'])
  TF.save(nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData)


def loadTf():
  TF = Fabric(locations=[f'{TF_PATH}/{VERSION}'])
  allFeatures = TF.explore(silent=True, show=True)
  loadableFeatures = allFeatures['nodes'] + allFeatures['edges']
  api = TF.load(loadableFeatures)
  if api:
    print(f'max node = {api.F.otype.maxNode}')
    print(api.F.root.freqList()[0:20])


def main():
  readTranslations()
  readData()
  readMorph()
  parseMorph()
  makeTfData()
  makeTf()
  loadTf()


main()
