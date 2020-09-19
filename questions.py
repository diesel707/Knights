import nltk
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    f = dict()
    for i in os.listdir(directory):
        a = os.path.join(directory, i)
        with open(a,encoding = "utf-8") as j:
            f[i] = j.read()
    return f
    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    list1 = []
    alphabet = nltk.word_tokenize(document)

    for i in range(len(alphabet)):
        alphabet[i] = alphabet[i].lower()

        if alphabet in nltk.corpus.stopwords.words("english"):
            list1.append(i)
            continue
    for i in list1:
        del alphabet[i]

    return alphabet
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    alphabet = {}
    for i in documents:
        a = documents[i]
        for i in a:
            if i in alphabet:
                continue
            else:
                temp = 0
                tot = 0
                for j in documents:
                    if i in documents[j]:
                        temp += 1
                    tot += 1
                alphabet[i] = math.log(float(tot/temp))
    return alphabet
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    temp = {}
    for i in files:
        s = 0
        for j in query:
            t = idfs[j]
            s += files[i].count(j) * t
        temp[i] = s
    grade = sorted(temp.keys(), key=lambda x: temp[x], reverse = True)
    grade = list(grade)
    try:
        return grade[0:n+1]
    except:
        return grade
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    abc = {}
    for i in sentences:
        s = 0
        letters = sentences[i]
        temp = len(letters)
        letter = 0
        for j in query:
            letter = letters.count(j)
            if j in letters:
                s += idfs[j]
        abc[i] = (s,float(letter/temp))
    grade = sorted(abc.keys(), key=lambda x: abc[x], reverse = True)
    grade = list(grade)
    try:
        return grade[0:n+1]
    except:
        return grade
    # raise NotImplementedError


if __name__ == "__main__":
    main()
