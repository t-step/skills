"""Background worker process. Runs independently of any browser session --
picks jobs up off the queue whenever it gets to them, which can be minutes
to hours after they were enqueued."""

import reporting_service_client  # holds the worker's own service credential
import job_queue


def process_next_job():
    job = job_queue.dequeue("generate_report")
    if job is None:
        return

    project_ids = job.payload["project_ids"]
    requested_by_user_id = job.payload["requested_by_user_id"]  # label only

    # The worker authenticates to the data warehouse as itself, using a
    # broad internal service credential scoped to "generate any report" --
    # not as the requesting user, and not re-checking the requesting
    # user's current access. project_ids was fixed at enqueue time and is
    # trusted as still-valid here.
    rows = reporting_service_client.fetch_project_data(project_ids)
    pdf = render_report(rows, requested_by_label=requested_by_user_id)
    store_report_for_download(job.id, pdf)


def render_report(rows, requested_by_label):
    ...  # not relevant to this audit


def store_report_for_download(job_id, pdf):
    ...  # not relevant to this audit
