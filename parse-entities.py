from pyparsing import *

vowel = Char("அஆஇஈஉஊஎஏஐஒஓஔஃ")
consonant = Literal("ஸ்ர") | Literal("க்ஷ") | Char("கசடதபறயரலவழளஞஙனநமணஸஷஹஜ")
mark = Char("்ாிீுூெேைொோௌ")
            

optionally_marked_consonant = Combine(consonant + Optional(mark))

entity = vowel | optionally_marked_consonant
entities = OneOrMore(entity)

if __name__ == "__main__":
    print(entities.parseString("ஸ்ரீகுருகந்தமூர்த்தி"))
    print(entities.parseString("பக்ஷி"))
    print(entities.parseString("ஸகலம்"))
    print(entities.parseString("புஷ்பம்"))
    print(entities.parseString("பாகம்"))
