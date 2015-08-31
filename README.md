
po - analysis of column-formatted data.

installation:
	Anaconda Python 3.

Examples:

```

import po
snp = po.Po('snp_known.csv')
a = snp.query('var_prob < 0.6')
b = a[["tp-fp", "var_prob"]]
b.query('tp_fp == "fp"')
len(b.query('tp_fp == "fp"')

```
