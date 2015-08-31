
po - analysis of column-formatted data.

installation:
	Anaconda Python 3.

Examples:

```

import po
snp = po.read_csv('snp_known.csv')        # Read into a new data.
a = snp.query('var_prob < 0.6')     # Query a subset into a new data frame.
b = a[["tp-fp", "var_prob"]]        # Select a subset into a new data frame.
b.query('tp_fp == "fp"')            # Further query.
len(b.query('tp_fp == "fp"'))


iris = po.read_csv('iris.csv')
iris.query('SepalLength > 6 and PetalWidth > 2')                                  # Query a subset.
iris.Cluster(["SepalLength", "SepalWidth"], method="hierarchical", clusters=3)    # Cluster based on two columns.


```
Further information on how to select and query Pandas data frames: http://pandas.pydata.org/pandas-docs/stable/indexing.html
