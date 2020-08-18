import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pd = {}
    p = round(float((1-damping_factor)/len(corpus.keys())), 5)
    for k in corpus.keys():
        pd[k] = p

    links = corpus[page]

    if len(links) == 0:
        for k in pd.keys():
            pd[k] += damping_factor/len(corpus.keys())
        return pd
    for link in links:
        pd[link] += damping_factor/len(links)
        return pd

    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    page = random.choice(list(corpus.keys()))

    for k in corpus.keys():
        result[k] = 0
    while n:
        n -= 1
        result[page] += 1
        r = random.random()
        pd = transition_model(corpus, page, damping_factor)
        for k in pd:
            if pd[k] < r:
                r -= pd[k]
            else:
                page = k
                break
    norm = sum(result.values())
    for k in result.keys():
        result[k] = round(result[k]/norm, 5)
    return result


    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = {}
    for k in corpus.keys():
        pr[k] = float(1/len(corpus.keys()))
    a = 1
    while a:
        b = {}
        for k in pr.keys():
            t = pr[k]

            b[k] = float((1 - damping_factor)/len(corpus.keys()))

            for i, j in corpus.items():
                if k in j:
                    b[k] += float(damping_factor*(pr[i]/len(j)))
            if abs(t - b[k]) < 0.001:
                a = 0
        pr.update(b)
    return pr

    # raise NotImplementedError


if __name__ == "__main__":
    main()
