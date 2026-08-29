# EXPERIMENTAL -- prototype for RFC-42 (predictive scheduling).
#
# Not wired into main.py or anything else that runs. No tests. No feature
# flag even routes to this yet -- it's a standalone prototype module that
# a load-testing script imports directly, on demand, for offline
# evaluation only. Last touched two days ago; scheduler.py above hasn't
# changed in eight months.


def next_job_ml(queue, model):
    scores = model.score(queue)
    return max(queue, key=lambda j: scores[j.id])
