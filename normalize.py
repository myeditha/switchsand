# -*- coding: utf-8 -*-
"""
Usage:
    main.py --source-file=<file> --lang-set=<string>


Options:
    -h --help                               show this screen.

    --source-file=<file>                    source file to cleanse
                                            [default:  'file.txt']
    --lang-set=<string>                     list of languages in the corpus
                                            [default: ['eng','hin']]
    --lang-file=<file>                      language annotated file
                                            [default:  'file.txt']
    --aggressiveness=<float>                aggressiveness of cleaning
                                            [default: 1.0]
"""

from DataManagement import indicLangIdentifier, polyglot_SpellChecker
from DataManagement import dumbFilterCollection
from spellcheck import Spellchecker
import codecs
# from docopt import docopt
import os
from os import path
import argparse


def normalize_codemixed_text(source_file, lang_list):
    '''
    :param source_file: file containing tweets
    :param lang_list: list of languages with which to condition the language identifier
    :return: text cleaned from #tags, RT, transliterated and spell-corrrected
    '''
    dumbFilter = dumbFilterCollection()

    # loads a language identifier
    lid = indicLangIdentifier(lang_list)

    head, inpFileName = os.path.split(source_file)
    fileName, ext = inpFileName.split(".")
    outFile = fileName + "_filtered"
    outFile = os.path.join(head, outFile + "." + ext)
    # TODO: MEHERESH, Invoke the Spellchecker constructor from here
    spellChecker = Spellchecker()

    # if the lines within this file are already language annotated
    isLangTagged = True

    with codecs.open(source_file, 'r', encoding='utf-8') as fr:
        with codecs.open(outFile, 'w', encoding='utf-8') as fw:
            for line in fr.readlines():
                # 1. Apply basic filtering
                line = dumbFilter.filterLine(line)
                # 2. Language Tag the line
                lid_tags = []
                words = []
                lang_tagged_line = ""
                for token in line.split():
                    if isLangTagged:
                        word,lang = token.split('\\')
                        words.append(word)
                        lid_tags.append(lang)
                        lang_tagged_line +=token
                    else:
                        words.append(token)
                        lang = lid.detectLanguageInWord(token)
                        lang_tagged_line += token + "\\" + lang
                        lid_tags.append(lang)

                # spell_corrected_line = " ".join(words)
                spell_corrected_line = spellChecker.correctSentence(lang_tagged_line)
                fw.write(spell_corrected_line)
                # # 3. Transliterate each word to their language specific script
                # translit_words = []
                #
                # for word, lang in zip(spell_corrected_line.split(" "), lid_tags):
                #     translit_words.append(indic_transliterator(word, "english", lang))
                #
                # fw.write(" ".join(translit_words))

    return outFile

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Code-mixed spellchecking')
    parser.add_argument('source_file',type=str, help='file with code-mixed content, separated by newlines.')
    parser.add_argument('lang_set', type=str, help='comma separated languages in the file')
    args = parser.parse_args()

    source_file = args.source_file
    lang_list=args.lang_set.strip().split(",")

    normalize_codemixed_text(source_file, lang_list)