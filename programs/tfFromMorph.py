import os
import sys
import re
from shutil import rmtree

from tf.fabric import Fabric
from tf.writing.transcription import Transcription as tr
from tf.convert.walker import CV

# LOCATIONS

GH_BASE = os.path.expanduser('~/github')
ORG = 'q-ran'
REPO = 'quran'
BASE = f'{GH_BASE}/{ORG}/{REPO}'
VERSION_SRC = '1.0'
SOURCES = f'{BASE}/sources/{VERSION_SRC}'
MORPH_FILE = 'quranic-corpus-morphology-0.4.txt'
MORPH_PATH = f'{SOURCES}/{MORPH_FILE}'
DATA_FILE = 'quran-data.xml'
DATA_PATH = f'{SOURCES}/{DATA_FILE}'
TF_PATH = f'{BASE}/tf'
VERSION_TF = '0.4'
OUT_DIR = f'{TF_PATH}/{VERSION_TF}'

TRANSLATIONS = dict(
    en=f'{SOURCES}/en.arberry.xml',
    nl=f'{SOURCES}/nl.leemhuis.xml',
)

# SOURCE DECODING

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

# TF CONFIGURATION

slotType = 'word'

generic = dict(
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
)

otext = {
    'sectionFeatures': 'number,number',
    'sectionTypes': 'sura,aya',
    'structureFeatures': 'number,number,number',
    'structureTypes': 'sura,ruku,aya',
    'fmt:text-orig-full': f'{{unicode}}{{space}}',
    'fmt:text-trans-full': f'{{ascii}}{{space}}',
    'fmt:lex-trans-full': f'{{lemma}}{{space}}',
    'fmt:root-trans-full': f'{{root}}{{space}}',
}

intFeatures = set('''
    number
    order
    definite
'''.strip().split())

featureMeta = {
    'number': {
        'description': 'Number of sura, aya, word group, or word',
    },
    'name@en': {
        'language': 'english',
        'languageCode': 'en',
        'languageEnglish': 'English',
        'description': 'Name of sura in English',
    },
    'name': {
        'language': 'arabic',
        'description': 'Name of sura in Arabic',
    },
    'nameTrans': {
        'language': 'arabic',
        'description': 'Name of sura in Arabic, transcribed',
    },
    'nameAscii': {
        'language': 'arabic',
        'description': 'Name of sura in Arabic, transliterated',
    },
    'type': {
        'description': 'type of sura',
    },
    'order': {
        'description': 'ordinal number of sura',
    },
    'ascii': {
        'description': 'transliterated text of word',
    },
    'unicode': {
        'description': 'unicode arabic text of word',
    },
    'space': {
        'description': 'material between this word and the next',
    },
    'lemma': {
        'description': 'lemma of word',
    },
    'root': {
        'description': 'root of word',
    },
    'case': {
        'description': 'case of word',
    },
    'pos': {
        'description': 'part-of-speech of word, main class',
        'documentation': 'http://corpus.quran.com/documentation/tagset.jsp',
    },
    'posx': {
        'description': 'part-of-speech of word, refined class',
        'documentation': 'http://corpus.quran.com/documentation/tagset.jsp',
    },
    'formation': {
        'description': 'stem formation of verb',
    },
    'interjection': {
        'description': 'kind of interjection',
    },
    'gn': {
        'description': 'gender of word (masculine, feminine)',
    },
    'nu': {
        'description': 'number of word (singular, dual, plural)',
    },
    'ps': {
        'description': 'person of word (1st, 2nd, 3rd)',
    },
    'voice': {
        'description': 'voice of a verb (active, passive)',
    },
    'tense': {
        'description': 'tense of a verb (perfect, imperfect, ...)',
    },
    'mood': {
        'description': 'mood of a verb (subj, jus, ...)',
    },
    'definite': {
        'description': 'whether the word is definite',
    },
    'component': {
        'description': 'role of the word in its word group (prefix, main, or suffix)',
    },
    'a': {
        'description': 'not yet understood',
    },
    'ax': {
        'description': 'not yet understood',
    },
    'f': {
        'description': 'not yet understood',
    },
    'fx': {
        'description': 'not yet understood',
    },
    'l': {
        'description': 'not yet understood',
    },
    'lx': {
        'description': 'not yet understood',
    },
    'n': {
        'description': 'not yet understood',
    },
    'w': {
        'description': 'not yet understood',
    },
    'wx': {
        'description': 'not yet understood',
    },
    'sp': {
        'description': 'not yet understood',
    },
    'translation@en': {
        'description': 'english translation of whole aya',
        'translator': 'Arthur Arberry (1955), https://en.wikipedia.org/wiki/Arthur_John_Arberry',
    },
    'translation@nl': {
        'description': 'english translation of whole aya',
        'translator': 'Fred Leemhuis (1989), https://rug.academia.edu/FrederikLeemhuis',
    },
}

# DATA READING

morphDb = {}
wordFeatures = {}
suraFeatures = {}
sectionStart = {}
sectionEnd = {}

translations = {}

unknowns = set()
unknownFeatures = set()
unknownPerFeat = {}

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
    sections = sectionRe.findall(data)
    for section in sections:
      atts = dict(attRe.findall(section))
      sI = int(atts.get('index', 0))
      sura = int(atts.get('sura', 0))
      aya = int(atts.get('aya', 0))
      features = {k: atts[k] for k in info}
      if sI > 1:
        sectionEnd.setdefault((sura, aya), []).append((sectionName, sI - 1))
      sectionStart.setdefault((sura, aya), []).append((sectionName, sI, features))


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


# SET UP CONVERSION

def getConverter():
  if os.path.exists(OUT_DIR):
    rmtree(OUT_DIR)
  TF = Fabric(locations=[OUT_DIR])
  return CV(TF)


def convert():
  readTranslations()
  readData()
  readMorph()
  cv = getConverter()

  return cv.walk(
      director,
      slotType,
      otext=otext,
      generic=generic,
      intFeatures=intFeatures,
      featureMeta=featureMeta,
      generateTf=generateTf,
  )


# DIRECTOR

def director(cv):
  print('Parsing morphological data')

  global unknowns

  lemmaIndex = {}
  sectionIndex = {}

  for (sura, suraData) in morphDb.items():
    curSura = cv.node('sura')
    cv.feature(curSura, number=sura)
    theseSuraFeatures = suraFeatures.get(sura, None)
    if theseSuraFeatures:
      cv.feature(curSura, **theseSuraFeatures)
    for (aya, ayaData) in suraData.items():
      curAya = cv.node('aya')
      cv.feature(curAya, number=aya)
      transFeatures = {
          f'translation@{lang}': trans[(sura, aya)]
          for (lang, trans) in translations.items()
      }
      cv.feature(curAya, **transFeatures)
      for s in sectionEnd.get((sura, aya), []):
        curSection = sectionIndex[s]
        cv.terminate(curSection)
        del sectionIndex[s]
      for (sName, sI, sFeatures) in sectionStart.get((sura, aya), []):
        curSection = cv.node(sName)
        cv.feature(curSection, number=sI, **sFeatures)
        sectionIndex[(sName, sI)] = curSection
      nAya = len(ayaData)
      for (ig, (group, groupData)) in enumerate(ayaData.items()):
        curGroup = cv.node('group')
        cv.feature(curGroup, number=group)
        nGroup = len(groupData)
        for (iw, (word, (form, tag, featureStr))) in enumerate(groupData.items()):
          (theseFeatures, theseUnknowns) = parseMorphItem(tag, featureStr)
          lemma = theseFeatures.get('lemma', None)
          if lemma:
            thisLemma = lemmaIndex.get(lemma, None)
            if thisLemma:
              cv.resume(thisLemma)
            else:
              thisLemma = cv.node('lex')
              lemmaIndex[lemma] = thisLemma
            cv.feature(thisLemma, lemma=lemma)
          curWord = cv.slot()
          if lemma:
            cv.terminate(thisLemma)
          cv.feature(
              curWord,
              ascii=form,
              unicode=tr.to_arabic(form),
              space=' ' if iw == nGroup - 1 and ig != nAya - 1 else '',
              number=word,
          )
          cv.feature(curWord, **theseFeatures)
          unknowns |= theseUnknowns
        cv.terminate(curGroup)
      cv.terminate(curAya)
    cv.terminate(curSura)
  for curSection in sectionIndex.values():
    cv.terminate(curSection)

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


# TF LOADING (to test the generated TF)

def loadTf():
  TF = Fabric(locations=[OUT_DIR])
  allFeatures = TF.explore(silent=True, show=True)
  loadableFeatures = allFeatures['nodes'] + allFeatures['edges']
  api = TF.load(loadableFeatures, silent=False)
  if api:
    print(f'max node = {api.F.otype.maxNode}')
    print(api.F.root.freqList()[0:20])


# MAIN

generateTf = len(sys.argv) == 1 or sys.argv[1] != '-notf'

print(f'QURAN-MORPH to TF converter for {REPO}')
print(f'QURAN source version = {VERSION_SRC}')
print(f'TF  target version = {VERSION_TF}')
good = convert()

if generateTf and good:
  loadTf()
