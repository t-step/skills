# Context

Excerpts from two services: `ingestion/import_job.py` (Data Platform team)
and `catalog/dataset_version.py` (Catalog team). Neither team's full
codebase is included; treat anything not shown here as not available.

An excerpt from `#data-platform`, forwarded for context:

> **alex.p:** anyone know why import job 88213 shows COMPLETED but I don't
> see a published dataset version for it in Catalog yet?
>
> **jordan.k:** completed just means the raw ingest finished -- Catalog
> makes a draft version off of that, but publishing is a separate manual
> step a curator does later, could be minutes or days later
>
> **alex.p:** ok but doesn't that mean the two systems are out of sync?
> should we add a `sync_status` field on ImportJob that mirrors whatever
> DatasetVersion's state is, so people stop asking this in the channel?
>
> **jordan.k:** not sure, maybe worth asking the review for an opinion
> before we build anything
