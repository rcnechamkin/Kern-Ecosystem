from nltk.corpus import wordnet as wn

try:
    wn.ensure_loaded()
except:
    import nltk
    nltk.download("wordnet")

def expand_with_wordnet(tag):
    synonyms = set()
    for syn in wn.synsets(tag):
        for lemma in syn.lemmas():
            name = lemma.name().lower().replace("_", " ")
            if name != tag:
                synonyms.add(name)
    return list(synonyms)

def expand_tags(tag_list):
    expanded = set(tag_list)
    for tag in tag_list:
        expanded.update(expand_with_wordnet(tag))
    return sorted(expanded)
