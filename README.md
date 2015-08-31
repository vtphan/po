
po - analysis of column-formatted data.

installation:
	Anaconda Python 3.

Examples:

```

import po
snp = po.read_csv('snp_known.csv')        # Read into a new data.
a = snp.query('var_prob < 0.6')     # Query a subset into a new data frame.
b = a[["tp-fp", "var_prob"]]        # Select a subset into a new data frame.
res = b.query('tp_fp == "fp"')            # Further query.


iris = po.read_csv('iris.csv')

# cluster using meanshift, a non-parametric method, by default.
iris.Cluster(["SepalLength", "SepalWidth"])

# cluster on a subset using hierarchical clustering
res = iris.query('SepalLength > 6 and PetalWidth > 2').Cluster(["SepalLength", "SepalWidth"], method="hierarchical", clusters=3)

```
Further information on how to select and query Pandas data frames: http://pandas.pydata.org/pandas-docs/stable/indexing.html
