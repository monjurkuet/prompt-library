"""arXiv integration for research monitoring."""

import datetime

import arxiv


class ArxivIntegrator:
    """arXiv API wrapper for research integration."""

    def __init__(self):
        self.client = arxiv.Client()

    def search_by_keywords(
        self, keywords: list[str], max_results: int = 10, days_back: int = 7
    ) -> list[dict]:
        """Search arXiv for recent papers by keywords."""
        query = " AND ".join(f"all:{kw}" for kw in keywords)
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        results = []
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            days=days_back
        )

        for result in self.client.results(search):
            if result.published < cutoff_date:
                continue

            results.append(
                {
                    "title": result.title,
                    "authors": [str(author) for author in result.authors],
                    "published": result.published.isoformat(),
                    "summary": result.summary,
                    "pdf_url": result.pdf_url,
                    "entry_id": result.entry_id,
                    "categories": result.categories,
                }
            )

        return results

    def search_by_category(
        self, category: str, max_results: int = 10, days_back: int = 7
    ) -> list[dict]:
        """Search arXiv by category (e.g., cs.AI, stat.ML)."""
        query = f"cat:{category}"
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        results = []
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            days=days_back
        )

        for result in self.client.results(search):
            if result.published < cutoff_date:
                continue

            results.append(
                {
                    "title": result.title,
                    "authors": [str(author) for author in result.authors],
                    "published": result.published.isoformat(),
                    "summary": result.summary,
                    "pdf_url": result.pdf_url,
                    "entry_id": result.entry_id,
                    "categories": result.categories,
                }
            )

        return results

    def get_paper_details(self, paper_id: str) -> dict | None:
        """Get detailed information about a specific paper."""
        search = arxiv.Search(id_list=[paper_id])

        try:
            result = next(self.client.results(search))
            return {
                "title": result.title,
                "authors": [str(author) for author in result.authors],
                "published": result.published.isoformat(),
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "entry_id": result.entry_id,
                "categories": result.categories,
            }
        except StopIteration:
            return None
