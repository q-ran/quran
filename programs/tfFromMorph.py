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
VERSION = '0.1'

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
}

# data holders

morphDb = {}
wordFeatures = {}
suraFeatures = {}
unknowns = set()
unknownFeatures = set()
unknownPerFeat = {}

nodeFeatures = {}
edgeFeatures = {}


def readData():
  print('Reading sura metadata')

  suraPat = r'<sura(.*?)/>'
  suraRe = re.compile(suraPat)
  attPat = r' ([a-z]+)="([^"]*)"'
  attRe = re.compile(attPat)

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
  (curS, curA, curG, curW) = (None, None, None, None)

  for (thisS, thisA, thisG, thisW) in sorted(wordFeatures):
    offsetW += 1
    if (thisS, thisA, thisG) != (curS, curA, curG):
      offsetG += 1
    if (thisS, thisA) != (curS, curA):
      offsetA += 1
    if thisS != curS:
      offsetS += 1
    (curS, curA, curG, curW) = (thisS, thisA, thisG, thisW)

  print(f'''
  {offsetS:>6} suras
  {offsetA:>6} ayas
  {offsetG:>6} word groups
  {offsetW:>6} words
''')

  (curS, curA, curG, curW) = (None, None, None, None)
  (nodeS, nodeA, nodeG, nodeW) = (0, 0, 0, 0)

  for (thisS, thisA, thisG, thisW) in sorted(wordFeatures):
    nodeW += 1
    otype[nodeW] = 'word'
    if curW is not None:
      space = (
          ' '
          if thisS == curS and thisA == curA and thisG != curG
          else ''
      )
      nodeFeatures.setdefault('space', {})[curW] = space

    nodeFeatures.setdefault('number', {})[nodeW] = thisW
    for (k, v) in wordFeatures.get((thisS, thisA, thisG, thisW), {}).items():
      nodeFeatures.setdefault(k, {})[nodeW] = v

    if (thisS, thisA, thisG) != (curS, curA, curG):
      nodeG += 1
      otype[offsetW + nodeG] = 'group'
      nodeFeatures.setdefault('number', {})[offsetW + nodeG] = thisG
    oslots.setdefault(offsetW + nodeG, set()).add(nodeW)

    if (thisS, thisA) != (curS, curA):
      nodeA += 1
      otype[offsetW + offsetG + nodeA] = 'aya'
      nodeFeatures.setdefault('number', {})[offsetW + offsetG + nodeA] = thisA
    oslots.setdefault(offsetW + offsetG + nodeA, set()).add(nodeW)

    if thisS != curS:
      nodeS += 1
      otype[offsetW + offsetG + offsetA + nodeS] = 'sura'
      nodeFeatures.setdefault('number', {})[offsetW + offsetG + offsetA + nodeW] = thisS
      for (k, v) in suraFeatures.get(thisS, {}).items():
        nodeFeatures.setdefault(k, {})[offsetW + offsetG + offsetA + nodeW] = v
    oslots.setdefault(offsetW + offsetG + offsetA + nodeS, set()).add(nodeW)

    (curS, curA, curG, curW) = (thisS, thisA, thisG, thisW)

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
''')

  fvs = (
      sum(len(nodeFeatures[f]) for f in nodeFeatures)
      +
      sum(len(edgeFeatures[f]) for f in edgeFeatures)
  )
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
    print(api.F.root.freqList()[0:20])


def main():
  readData()
  readMorph()
  parseMorph()
  makeTfData()
  makeTf()
  loadTf()


main()
