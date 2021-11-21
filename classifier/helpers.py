from keras.models import load_model
import pandas as pd
import re
import numpy as np
import string
from nltk.corpus import wordnet
from keras.preprocessing import text, sequence
import json


def summarize(comments):
    new_comments = []
    for comment in comments:
        auto_abstractor = AutoAbstractor()
        auto_abstractor.tokenizable_doc = SimpleTokenizer()
        auto_abstractor.delimiter_list = [".", "\n"]
        abstractable_doc = TopNRankAbstractor()
        result_dict = auto_abstractor.summarize(comment, abstractable_doc)
        para=""
        for sentence in result_dict["summarize_result"]:
            para += sentence
        new_comments.append(para)


modelPath = "C:/Users/Rajeswar Sharma/Documents/minor project 2/comment-sentiment-analyzer/classifier/tweet_sentiment_extraction.h5"
model = load_model(modelPath)

def limit_text(comment_list):
    new_list = []
    for comment in comment_list:
        if len(comment)<=32:
            new_list.append(comment)
    return new_list

def dropNa(data):
    data['text'].replace('', np.nan, inplace=True)
    data.dropna(subset=["text"], inplace=True)
    return data


def load_dict_contractions():
    return {
        "cant": "can not",
        "dont": "do not",
        "wont": "will not",
        "ain't": "is not",
        "amn't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "'cause": "because",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "could've": "could have",
        "daren't": "dare not",
        "daresn't": "dare not",
        "dasn't": "dare not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "e'er": "ever",
        "em": "them",
        "everyone's": "everyone is",
        "finna": "fixing to",
        "gimme": "give me",
        "gonna": "going to",
        "gon't": "go not",
        "gotta": "got to",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "he've": "he have",
        "how'd": "how would",
        "how'll": "how will",
        "how're": "how are",
        "how's": "how is",
        "I'd": "I would",
        "I'll": "I will",
        "I'm": "I am",
        "I'm'a": "I am about to",
        "I'm'o": "I am going to",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
        "I've": "I have",
        "kinda": "kind of",
        "let's": "let us",
        "mayn't": "may not",
        "may've": "may have",
        "mightn't": "might not",
        "might've": "might have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "must've": "must have",
        "needn't": "need not",
        "ne'er": "never",
        "o'": "of",
        "o'er": "over",
        "ol'": "old",
        "oughtn't": "ought not",
        "shalln't": "shall not",
        "shan't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "should've": "should have",
        "somebody's": "somebody is",
        "someone's": "someone is",
        "something's": "something is",
        "that'd": "that would",
        "that'll": "that will",
        "that're": "that are",
        "that's": "that is",
        "there'd": "there would",
        "there'll": "there will",
        "there're": "there are",
        "there's": "there is",
        "these're": "these are",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "this's": "this is",
        "those're": "those are",
        "'tis": "it is",
        "'twas": "it was",
        "wanna": "want to",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we're": "we are",
        "weren't": "were not",
        "we've": "we have",
        "what'd": "what did",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "where'd": "where did",
        "where're": "where are",
        "where's": "where is",
        "where've": "where have",
        "which's": "which is",
        "who'd": "who would",
        "who'd've": "who would have",
        "who'll": "who will",
        "who're": "who are",
        "who's": "who is",
        "who've": "who have",
        "why'd": "why did",
        "why're": "why are",
        "why's": "why is",
        "won't": "will not",
        "wouldn't": "would not",
        "would've": "would have",
        "y'all": "you all",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have",
        "Whatcha": "What are you",
        "luv": "love",
        "sux": "sucks",
        "couldn't": "could not",
        "wouldn't": "would not",
        "shouldn't": "should not",
        "im": "i am"
    }


def replaceElongated(word):
    """ Replaces an elongated word with its basic form, unless the word exists in the lexicon """
    repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
    repl = r'\1\2\3'
    if wordnet.synsets(word):
        return word
    repl_word = repeat_regexp.sub(repl, word)
    if repl_word != word:
        return replaceElongated(repl_word)
    else:
        return repl_word


def normalization(text):
    text = str(text).lower()

    # Unicodes
    text = re.sub(r'(\\u[0-9A-Fa-f]+)', r'', text)
    text = re.sub(r'[^\x00-\x7f]', r'', text)

    # URL
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)

    # User Tag
    text = re.sub('@[^\s]+', ' ', text)

    # Hash Tag
    text = re.sub(r'#([^\s]+)', r' ', text)

    # Number
    text = ''.join([i for i in text if not i.isdigit()])

    # Punctuation
    #text = ' '.join([char for char in text if char not in string.punctuation])
    for sym in string.punctuation:
        text = text.replace(sym, " ")

    # Elongated Words
    for word in text.split():
        text = text.replace(word, replaceElongated(word))

    # Contraction
    CONTRACTIONS = load_dict_contractions()
    text = text.replace("’", "'")
    words = text.split()
    reformed = [CONTRACTIONS[word]
                if word in CONTRACTIONS else word for word in words]
    text = " ".join(reformed)
    text = ' '.join([w for w in text.split() if len(w)
                     > 1 and w != 'a' and w != 'i'])

    return text


def word_count(sentence):
    return len(str(sentence).split())


def mapper(x):
    sentiment = {0: "negative", 1: "neutral", 2: "positive"}
    return sentiment[x]

path = "C:/Users/Rajeswar Sharma/Documents/minor project 2/comment-sentiment-analyzer/classifier/raw.json"
with open(path, encoding="utf-8") as json_file:
    data = json.load(json_file)
data = limit_text(list(data))

df = pd.DataFrame(data, columns=["text"])


# df["text"] = df["text"].apply(normalization)
# df['word_count'] = df['text'].apply(word_count)
# df.text = df.text.astype(str)
tk = text.Tokenizer(num_words=200000)
# tk.fit_on_texts(list(df.text.values))
# X_text_indices = tk.texts_to_sequences(df.text.values)

# X_text_indices = sequence.pad_sequences(X_text_indices, maxlen=31)
# result = model.predict(X_text_indices)
# for i in range(len(result)):
#     result[i] = np.argmax(result[i])
# res = result[1:, 0]
# output = np.array(list(map(mapper, res)))
# output
