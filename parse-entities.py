import sys
from collections import Counter, defaultdict
import pprint
from pyparsing import *

vowel = Char("அஆஇஈஉஊஎஏஐஒஓஔஃ")
consonant = Literal("ஸ்ர") | Literal("க்ஷ") | Char("கசடதபறயரலவழளஞஙனநமணஸஷஹஜ")

#This following is written as multiline string to not to appease vim.
mark = Char("""
்ாிீுூெேைொோௌ
""".strip())


optionally_marked_consonant = Combine(consonant + Optional(mark))

entity = vowel | optionally_marked_consonant
entities = OneOrMore(entity)

#phonetic
ph_kuril = Char("aeiou")
ph_nedil = Char("AEIOU") | Combine(ph_kuril * (1, 2))

ph_vowel = ph_nedil | ph_kuril #in this order to avoid 'oo' parsed as 'o' 'o'

ph_consonant = Literal("sh") | Literal("dh") | Literal("th") | Literal("ch") | Literal("zh") | Char("bcdfghjklmnpqrstvwxyzLN")

ph_optionally_marked_consonant = Combine(ph_consonant + Optional(ph_vowel))

ph_entity = ph_vowel | ph_optionally_marked_consonant
ph_entities = OneOrMore(ph_entity)

def unigram_auto(word, rules):
    ents = entities.parseString(word)
    res = []
    for e in ents:
        if e not in rules:
            return None
        res += [rules[e]]
    return ''.join(res)



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
        f_ents = entities.parseString(frm)
        t_ents = ph_entities.parseString(to)
        f_len, t_len = len(f_ents), len(t_ents)

        if f_len != t_len:
            print(frm, to)
            print(entities.parseString(frm))
            print(ph_entities.parseString(to))
            print(f_len, "--", t_len)
        else:

            for uni, ph  in zip(f_ents, t_ents):
                count_unic_ents[uni] += 1
                count_phon_ents[ph] += 1
                uni2phon[uni][ph] += 1
                phon2uni[ph][uni] += 1

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
    auto_transf = auto_transf.most_common(17)
    auto_transf = [x for x,_ in auto_transf]
    auto_transf = {u: ph for (u, ph) in auto_transf}
    print(auto_transf)

    print(unigram_auto("வயல்", auto_transf))
    print(unigram_auto("விறல் ", auto_transf))
    print(unigram_auto("விறல் -வயல்", auto_transf))

    for word in open('/home/guru/tamil-words/tamil_words_without_hyphen', 'r'):
        transformed = unigram_auto(word.rstrip(), auto_transf)
        if transformed:
            print("%s->%s" % (word.rstrip(), transformed))

    # print(ph_entities.parseString("gurukandhamoorthi"))
