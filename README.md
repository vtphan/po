
po - analysis of column-formatted data.

installation:
	Anaconda Python 3.

Examples:

```

import po
snp = po.read_csv('snp_known.csv')        # Read into a new data.
a = snp.query('var_prob < 0.6')           # Query a subset into a new data frame.
b = a[["tp-fp", "var_prob"]]              # Select a subset into a new data frame.
res = b.query('tp_fp == "fp"')            # Further query.


iris = po.read_csv('iris.csv')

# Cluster using meanshift, a non-parametric method, by default (when "clusters" is not specified).
iris.Cluster(["SepalLength", "SepalWidth"])

# Cluster on a subset using hierarchical clustering
res = iris.query('SepalLength > 6 and PetalWidth > 2').Cluster(["SepalLength", "SepalWidth"], method="hierarchical", clusters=3)

# Plot distribution
import matplotlib.pyplot as plt

iris.Plot("SepalLength")
plt.show()

# Plot numerical versus numerical variables
iris.Plot("SepalLength", "SepalWidth")
plt.show()

iris.Plot("SepalLength", "SepalWidth", hue="Species")
plt.show()

iris.Plot("SepalLength", "SepalWidth", col="Species")
plt.show()

iris.Plot("SepalLength", "SepalWidth", row="Species")
plt.show()

# Plot categorical versus numerical variables
iris.Plot("Species", "SepalLength")
plt.show()

iris.Plot("Species", "SepalLength", kind="box")
plt.show()

iris.Plot("Species", "SepalLength", kind="violin")
plt.show()

```
Further information on how to select and query Pandas data frames: http://pandas.pydata.org/pandas-docs/stable/indexing.html
