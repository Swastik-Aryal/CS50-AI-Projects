import os
import random
import re
import sys
import copy

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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = list(corpus[page])
    all_pages = list()
    probability_distribution = dict()

    for page in corpus:
        all_pages.append(page)
        probability_distribution[page] = 0

    for page in linked_pages:
        probability_distribution[page] = damping_factor * (1 / len(linked_pages))

    for page in all_pages:

        probability_distribution[page] += (1 - damping_factor) * (1 / len(all_pages))

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimations = dict()
    all_pages = list(corpus)

    start_page = random.choice(all_pages)

    for page in all_pages:
        estimations[page] = 0

    estimations[start_page] = 1 / n

    for i in range(n - 1):

        probability_dict = transition_model(corpus, start_page, damping_factor)

        next_page = random.choices(
            list(probability_dict), weights=list(probability_dict.values())
        )[0]

        estimations[next_page] += 1 / n

        start_page = next_page

    return estimations


def summation(corpus, estimations, page):
    """
    Return the summation value based on the formula given in the bacground
    """
    sum = 0
    all_pages = list(corpus)

    for pg in all_pages:
        if page in corpus[pg]:
            sum += estimations[pg] / len(corpus[pg])
        if len(corpus[pg]) == 0:
            sum += (estimations[pg]) / len(corpus)

    return sum


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimations = dict()
    init_estimations = dict()
    all_pages = list(corpus)

    for page in all_pages:
        init_estimations[page] = 1 / len(all_pages)

    convergence = False

    while not convergence:
        for page in all_pages:
            estimations[page] = (1 - damping_factor) / len(all_pages) + (
                damping_factor * summation(corpus, init_estimations, page)
            )

        difference = max(
            [abs(estimations[i] - init_estimations[i]) for i in init_estimations]
        )
        if difference < 0.001:
            convergence = True
        else:
            init_estimations = copy.deepcopy(estimations)

    return init_estimations


if __name__ == "__main__":
    main()
