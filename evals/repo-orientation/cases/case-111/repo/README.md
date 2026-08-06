# digest-service

A small internal service that runs a daily digest job and emails a summary
to the ops distribution list. Started as a couple of scheduled scripts;
`src/app.py` is the entry point that runs them.

## Setup

```
pip install -r requirements.txt
```

## Running

```
python -m src.app
```
