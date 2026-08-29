from src.crawler import crawl


def test_crawl_empty_site_returns_no_broken_links():
    assert crawl("https://example.test/empty") == []
