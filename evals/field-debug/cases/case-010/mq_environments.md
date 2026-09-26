# MQ environments reference (internal wiki excerpt)

`gl-dispatcher` can point at either queue manager depending on the
`GL_MQ_ENV` deploy variable. Queue name (`GL.POST.QUEUE`) and channel name
(`GL.POST.CHANNEL`) are identical across environments -- only the queue
manager and host differ, which is a common source of confusion when
someone says "the GL queue" without naming which one:

| Env  | Queue manager | Host              |
|------|----------------|-------------------|
| prod | `QM_PROD01`    | mq-prod-01.internal |
| qa   | `QM_QA01`      | mq-qa-01.internal   |

Production `gl-dispatcher` instances have run with `GL_MQ_ENV=prod` since
the service's original rollout.
