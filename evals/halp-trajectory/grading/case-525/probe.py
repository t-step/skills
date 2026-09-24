"""Behavior probe: how does a legend for a large-valued numeric variable represent its magnitude? Run from repo root with the repo's .venv python."""
import json, re, warnings
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import numpy as np, pandas as pd, seaborn as sns, seaborn.objects as so
from matplotlib.ticker import MaxNLocator
from seaborn.utils import locator_to_legend_entries
rng = np.random.RandomState(0)
df = pd.DataFrame({"x": rng.rand(30), "y": rng.rand(30), "s": rng.uniform(3e6, 6e6, 30), "g": list("ab") * 15})
def texts(leg): return [leg.get_title().get_text()] + [t.get_text() for t in leg.get_texts()]
def classify(tx):
    full = any(re.fullmatch(r"\d{7,}(\.0+)?", t.replace(",", "")) for t in tx)   # labels carry the magnitude themselves (suppress-offset)
    offs = any(re.search(r"e\+?0?6|×10|x10", t) for t in tx)                 # magnitude shown as separate offset/suffix (represent-offset)
    return "B" if full and not offs else "A" if offs and not full else "neither" if not (full or offs) else "mixed"
cases = {
    "objects_pointsize": texts(so.Plot(df, x="x", y="y", pointsize="s").add(so.Dot()).plot()._figure.legends[0]),
    "classic_size_only": texts(sns.scatterplot(data=df, x="x", y="y", size="s").get_legend()),
    "classic_hue_and_size": texts(sns.scatterplot(data=df, x="x", y="y", hue="g", size="s").get_legend()),
}
res = {"cases": {k: {"texts": v, "path": classify(v)} for k, v in cases.items()}}
res["locator_to_legend_entries_arity"] = len(locator_to_legend_entries(MaxNLocator(3), (3e6, 6e6), float))
paths = {c["path"] for c in res["cases"].values()}
res["path"] = paths.pop() if len(paths) == 1 else "mixed"
print(json.dumps(res))
