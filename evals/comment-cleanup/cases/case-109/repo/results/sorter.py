"""Result sorting utilities."""


def sort_results(results: list[dict]) -> list[dict]:
    # Originally this used a hand-rolled bubble sort, written back when
    # the team was avoiding stdlib dependencies for build-size reasons;
    # that constraint doesn't apply anymore, and it was swapped for
    # sorted() in 2021 for a large performance win.
    return sorted(results, key=lambda r: r["score"], reverse=True)
