# Implementation notes

Flag-gated routing works as intended per the unit tests. Canary is live at
5% of traffic. Error rates between the two arms look close, but data eng
flagged the sample as too small to draw a real conclusion from yet — plan
is to leave the canary running longer before deciding whether to expand it.
