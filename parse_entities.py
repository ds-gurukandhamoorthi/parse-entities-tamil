import sys
from collections import Counter, defaultdict
import re
import pprint
from pyparsing import *

vowel = Char("அஆஇஈஉஊஎஏஐஒஓஔஃ")
consonant = Literal("க்ஷ") | Char("கசடதபறயரலவழளஞஙனநமணஸஷஹஜ")
sri =  Literal("ஸ்ரீ")

#This following is written as multiline string to not to appease vim.
mark = Char("""
்ாிீுூெேைொோௌ
""".strip())


optionally_marked_consonant = Combine(consonant + Optional(mark))

entity = sri | vowel | optionally_marked_consonant
entities = OneOrMore(entity)

#phonetic
ph_kuril = Char("aeiou")
ph_nedil = Char("AEIOU") | Combine(ph_kuril * (1, 2))

ph_vowel = ph_nedil | ph_kuril #in this order to avoid 'oo' parsed as 'o' 'o'

ph_consonant = Literal("jh") | Literal("tr") | Literal("dr") | Literal("sh") | Literal("dh") | Literal("th") | Literal("ch") | Literal("zh") | Char("bcdfghjklmnpqrstvwxyzLN")

ph_optionally_marked_consonant = Combine(ph_consonant + Optional(ph_vowel))

ph_entity = ph_vowel | ph_optionally_marked_consonant
ph_entities = OneOrMore(ph_entity)

def unigram_auto(word, rules):
    ents = entities.parseString(word, parseAll=True)
    res = []
    for e in ents:
        if e not in rules:
            return None
        res += [rules[e]]
    return ''.join(res)

def nb_tamil_entities(word):
    try:
        ents = entities.parseString(word, parseAll=True)
        return len(ents)
    except:
        return 0 #we want to avoid erroneously encoded words

STRESSED_CONSONANT = "([கசடதபறயரலவழளஞஙனநமணஸஷஹஜ])[்]\\1"

def nb_stressed_consonants(word):
    return len(re.findall(STRESSED_CONSONANT, word))



if __name__ == "__main__":
    # print(entities.parseString("ஸ்ரீகுருகந்தமூர்த்தி"))
    # print(entities.parseString("பக்ஷி"))
    # print(entities.parseString("ஸகலம்"))
    # print(entities.parseString("புஷ்பம்"))
    # print(entities.parseString("பாகம்"))
    # print(entities.parseString("யோகத்திற்கு"))
    filename = sys.argv[1]
    # abc -> def

    #Unicode entities are transformed into... what... their count
    uni2phon = defaultdict(Counter)
    phon2uni = defaultdict(Counter)

    #count of unicode entities
    count_unic_ents = Counter()
    count_phon_ents = Counter()

    for transfrm in open(filename, 'r'):
        frm, to = transfrm.rstrip().split('->')
        # print(frm, to)
        try:
            f_ents = entities.parseString(frm, parseAll=True)
            t_ents = ph_entities.parseString(to, parseAll=True)
            f_len, t_len = len(f_ents), len(t_ents)
            nb_strssed = nb_stressed_consonants(frm)

            if f_len != t_len:
                if nb_stressed_consonants(frm) == 0: #we would deal with stressed consonants later.
                    njh, ndh, ngh = "ஞ்", "ந்", "ங்"
                    if not (njh in frm or ndh in frm or ngh in frm):
                        print(frm, to)
                        print(entities.parseString(frm, parseAll = True))
                        print(ph_entities.parseString(to, parseAll = True))
                        print(f_len, "--", t_len)
            else:
                for uni, ph  in zip(f_ents, t_ents):
                    count_unic_ents[uni] += 1
                    count_phon_ents[ph] += 1
                    uni2phon[uni][ph] += 1
                    phon2uni[ph][uni] += 1
        except:
            pass #avoid words with erroneous encodings

    for x in count_unic_ents.most_common(20):
        print(x)
    for x in count_phon_ents.most_common(20):
        print(x)
    pprint.pprint(uni2phon)
    pprint.pprint(phon2uni)

    auto_transf = Counter()
    for u in uni2phon:
        if len(uni2phon[u]) == 1:
            for ph, cnt in uni2phon[u].most_common(1):
                auto_transf[(u, ph)] += cnt
    # pprint.pprint(auto_transf.most_common())
    # auto_transf = auto_transf.most_common(17)
    auto_transf = auto_transf.most_common() #we don't want to focus on words that could be transcoded even approximatively (incorrectly). The disambiguation process can be done using bigrams later... 'kai' at start becomes kai, 'kai' at end becomes gai sometimes as in mutrugai
    auto_transf = [x for x,_ in auto_transf]
    auto_transf = {u: ph for (u, ph) in auto_transf}
    print(auto_transf)

    print(unigram_auto("வயல்", auto_transf))
    print(unigram_auto("விறல் ", auto_transf))
    # print(unigram_auto("விறல் -வயல்", auto_transf))

    for word in open('/tmp/important5000', 'r'):
        transformed = unigram_auto(word.rstrip(), auto_transf)
        if not transformed:
            print(word.rstrip())
            # print("%s->%s" % (word.rstrip(), transformed))

    # print(ph_entities.parseString("gurukandhamoorthi"))
