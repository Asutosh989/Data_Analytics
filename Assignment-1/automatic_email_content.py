
import pandas as pd
import re

# the document is '$' separated
df = pd.read_csv('Automatic email content store.csv', sep='$')

# To get all the unique email
email = df['to '].unique()
print(f'The list of unique Email ID are {email}')


# To remove the rows having timestamp in different format other than 'dd/mm/yy'
for i in range(len(df.index)):
    if not (bool(re.compile(r'(\d{2}\/\d{2}\/\d{2})').match(df['Date'][i]))):
        df.drop(df.index[i], inplace=True)

df.reset_index(drop=True, inplace=True)


# To find common words
# to store the list if matching words from dummy_words and raw column
remark = []

# user defined set of dummy words
dummy_words = set(['deadline', 'tell', 'me'])

# clean function to remove '?' from words in a list and retrurns a final list of cleaned words
def clean(a):
    x = []
    for j in a:
        if '?' in j:
            j = ''.join(j.split('?'))
        x.append(j)
    return x


# to find out the matching words in sentences of raw data and dummy data 
# And storing the final list of words in remark list
for j in range(len(df.index)):
    words = clean(df['raw'][j].split())
    word_set = set(words)
    result = ','.join(list(dummy_words.intersection(word_set)))
    if (len(result) == 0):
        remark.append('NO MATCHING WORDS')
    else:
        remark.append(result)


# adding a new column to existing dataframe to store common words
# it writes 'Nothing' if no common words is present
df['Same_words'] = remark


# Time delta in days
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# creating a final CSV out of the Dataframe
df.to_csv('final.csv', index=False)

# Here user can give their dates of their own
user_date = '2017-12-30'


# Stores the differenc in days between user provided sate and the last date
diff = abs(df.iloc[len(df.index)-1]['Date'] - pd.to_datetime(user_date)).days
print(f'The difference in days is {diff} days')


