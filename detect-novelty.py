import sys
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.svm import OneClassSVM
from parse_entities import entities

def split_tam_entities(word):
    ents = entities.parseString(word, parseAll=True)
    return list(ents)

if __name__ == "__main__":
    word_stat_file = pd.read_csv(sys.argv[1])

    word_stat_file = word_stat_file.set_index('word')

    lengthy_words = word_stat_file['entities_len'] >= 3
    word_stat_file = word_stat_file[lengthy_words]

    known_words_files = sys.argv[2:]
    for knwn_wrd_fle in known_words_files:
        # print(knwn_wrd_fle)
        knwn = pd.read_csv(knwn_wrd_fle, sep='->', names=['word', knwn_wrd_fle])
        knwn = knwn.set_index('word')
        word_stat_file = pd.concat([word_stat_file, knwn], axis=1)
        # print(word_stat_file.columns)
        auto_poss = word_stat_file['auto_translit_poss']
        entered_manually = ~word_stat_file[knwn_wrd_fle].isna()
        word_stat_file['auto_translit_poss'] =  auto_poss| entered_manually


    word_stat_file.index.name = 'word'
    word_stat_file = word_stat_file.reset_index()
     
    can_be_automated = word_stat_file['auto_translit_poss']
    # print(sum(can_be_automated))

    # transliteration is typed (known) or guessable (known)
    known_words = word_stat_file[can_be_automated]

    # pipe = make_pipeline(
    #     CountVectorizer(analyzer='char', ngram_range=(2, 2), preprocessor=lambda s: f' {s} ', binary=True),
    #     OneClassSVM(gamma='auto'),
    # )

    pipe = make_pipeline(
        CountVectorizer(tokenizer=split_tam_entities, ngram_range=(4, 4), binary=True),
        OneClassSVM(gamma='auto'),
    )

    X = known_words['word']
    pipe.fit(X)

    sample_words = word_stat_file[~ can_be_automated].head(10000)['word']

    res = pipe.predict(sample_words)

    for novel_word in sample_words[res == -1]:
        print(novel_word)
