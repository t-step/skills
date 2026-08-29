Great, that paging issue is fixed. Now that we're thinking about the HTTP
layer — it really bugs me that we've got requests, httpx, and urllib3 all
mixed together across the codebase. Can we use this as the moment to unify
all of that into one consistent client wrapper?

Materials: evals/next-best-slice/cases/case-104/: review.md, retro.md,
backlog.md.
