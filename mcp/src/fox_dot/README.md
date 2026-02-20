install SuperCollider
uv add FoxDot

in SuperCollider:
Quarks.install("FoxDot")
After installing the Quark, go to Language → Recompile Class Library

then,
FoxDot.start

back to terminal:

```
from FoxDot import *

p1 >> pads([0, 1, 2, 3])
d1 >> play("x-o-")
Go()

```

uv run script.py
