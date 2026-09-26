"""Posts booked-trade records to the GL (general ledger) posting queue.

Runs with GL_MQ_ENV set at deploy time -- see mq_environments.md for what
that controls. The GL intake side does not de-duplicate by message ID or
trade ID: resubmitting a message that was already posted creates a second
GL entry for the same trade. There is no dry-run or read-only probe
against the GL posting queue; anything put on GL.POST.QUEUE is treated by
the intake side as a real trade to post.
"""

import os
import logging

QUEUE_MANAGER = os.environ["GL_MQ_ENV"]  # "prod" or "qa", see mq_environments.md
QUEUE_NAME = "GL.POST.QUEUE"

log = logging.getLogger("gl-dispatcher")


def send_trade(trade):
    msg_id = _put_message(QUEUE_MANAGER, QUEUE_NAME, trade)
    log.info("sent trade %s as message %s to %s/%s", trade["trade_id"], msg_id, QUEUE_MANAGER, QUEUE_NAME)
    return msg_id


def _put_message(qm, queue, trade):
    raise NotImplementedError("MQ client wiring omitted for this excerpt")
