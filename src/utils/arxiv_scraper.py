import arxiv
import argparse
import PyPDF2
import os
import json
import nltk
from rake_nltk import Rake

nltk.download("stopwords")
nltk.download("punkt")


def refine_query(query):
    rake = Rake()
    rake.extract_keywords_from_text(query)
    keywords = rake.get_ranked_phrases()
    return " ".join(keywords)


def scrape_papers(args):
    refined_query = refine_query(args.query)
    results = []

    search = arxiv.Search(
        query=refined_query,
        max_results=args.numresults,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers = list(search.results())

    for i, p in enumerate(papers):
        text = ""
        file_path = f"src/data/data_{i}.pdf"
        p.download_pdf(filename=file_path)

        with open(f"src/data/data_{i}.pdf", "rb") as file:
            pdf = PyPDF2.PdfReader(file)

            for page in range(len(pdf.pages)):
                page_obj = pdf.pages[page]

                text += page_obj.extract_text() + " "

        os.unlink(file_path)
        paper_doc = {"url": p.pdf_url, "title": p.title, "text": text}
        results.append(paper_doc)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", help="the query to search for", type=str)
    parser.add_argument(
        "--numresults", help="the number of results to return", type=int
    )
    args = parser.parse_args()

    results = scrape_papers(args)
    for i, r in enumerate(results):
        with open(f"src/data/data_{i}.json", "w") as f:
            json.dump(r, f)
