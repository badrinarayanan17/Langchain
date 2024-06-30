# Using profanity library to censor prohibited words

from profanity_filter import ProfanityFilter

pf = ProfanityFilter()

sencensor = pf.censor("This is fuckin crazy")
print(sencensor)
