import PyPDF2
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


filename = 'JavaBasics-notes.pdf'

# opening the pdf in read mode
pdfFileObj = open(filename,'rb')

#Pypdf2 creates a read object of the whole file
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# stores the total number of pages in the pdf
num_pages = pdfReader.numPages

print(f'The total number of pages in the pdf is {num_pages}')

# Storing all the text of the pdf in `text` variable
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    text += pageObj.extractText()


# converting the whole text to lower case
text = text.lower()

# to create a list of sentences from the final text
sentences = text.split('.')

# The bullet points are replaced by exclamation mark while reading the pdf
# So the sengtences are further splitted on the basis of Exclamation mark
sen = [list(filter(None, s.split('!'))) for s in sentences]


# this function flattens to list of lists into one single list
def flatten(l):
    d = []
    for i in l:
        d.extend(i) 
    return d

# sen now contains all the possible sentences
sentences = flatten(sen)

# here the sentences containing single words are removed
for s in sentences:
    if (len(s.strip().split()) == 1):
        sentences.remove(s)


# creating a dataframe for the sentences
df = pd.DataFrame({
    'Sentence': sentences
})


# importing the list of stopwords from NLTK
stop_words = stopwords.words('english')

# all digits are removed as there are some examples like "19962003", "-1java"
# this function preprocess a sentence by removing all the digits, punctuations and stopwords
# the words in the final list of tokens produced are checked if it exists in english dictionary
# this function will act as an analyzer for the tokens
def preprocess(x):
    x = x.strip()
    y = [g for g in x if not g.isdigit()]
    no_punc = [c for c in y if c not in string.punctuation]
    no_punc = ''.join(no_punc)
    tokens = [c for c in no_punc.split() if c.lower() not in stop_words]
    keyword = [word for word in tokens if wordnet.synsets(word)]
    
    return keyword


# the vectoriser is initiated  with the above defined `preprocess` function
vectorizer = CountVectorizer(analyzer=preprocess)


# It returns a vector (bag of words)
bow = vectorizer.fit(df['Sentence'])


# applying the transform on all the sentences
bow_transform =  bow.transform(df['Sentence'])


# Tfidf Transformer is used the find the weighted average of the keywords passed by Count Vectoriser
tfidf = TfidfTransformer().fit(bow_transform)


# It finds the weighted average of particuaar words in the particular sentence
tfdif_transform = tfidf.transform(bow_transform)


# to create a dictionary of words with its mean weighted average
meta = {}
for i, val in enumerate(bow.get_feature_names()):
    # to exclude the single letter words
    if (len(val)!=1):
        meta[val] = tfdif_transform.getcol(i).mean() * 10


# converting the dictionary to a Dataframe 
new = pd.DataFrame.from_dict(meta, orient="index")
new.columns = ['Weighted_average']

new.to_csv('keywords.csv')

