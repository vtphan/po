
Po is a Python module facilitates analysis of tabular data.  Po is built on top of pandas, scikit-learn, and seaborn.

### Installation

- Anaconda Python 3.
- seaborn (conda install seaborn)

### Read data

```
import po
iris = po.read_csv("data/iris.csv")
indels = po.read_csv("data/indels.txt", sep="\t")
```

*iris* is a po instance, which is a glorified pandas data frame.

### Data selection

po instances have a *query* method, which wraps around pandas data frame's query method.  Po.query returns a po instance.

```
a = iris.query('Species == "setosa" and PetalWidth > 0.1')
```

Selecting columns:
```
iris[["Species", "PetalLength"]]
```

Further information on how to select and query Pandas data frames: http://pandas.pydata.org/pandas-docs/stable/indexing.html

### Cluster rows based on columns

Cluster rows into 3 clusters based on petal widths and lengths.  Clustering is done using k-means.  Cluster labels are placed in a new column called *_kmeans_*.

```
iris.Cluster(["PetalWidth", "PetalLength"], clusters=3)
```

In case the number of clusters is not specified, clustering is done using meanshift.  Cluster labels are placed in a new column called *_meanshift_*.

```
iris.Cluster(["PetalWidth", "PetalLength"])
```

Other clusterting methods include hierarchical, spectral, and dbscan.

```
Cluster(["PetalWidth", "PetalLength"], method="hierarchical", clusters=3)
```

### Visualizing data

When one variable (defined by column name) is given, it must be a numerical variable.  The plot is a distribution plot.

```
iris.Plot("SepalLength")
```

When a numerical variable is compared against another numerical variable, the plot is a scatter plot.

```
iris.Plot("SepalLength", "SepalWidth")
```

Colors can be added to differentiate rows with values belonging to a categorical variable.

```
iris.Plot("SepalLength", "SepalWidth", hue="Species")
```

Scatter plot separated into different columns and rows.
```
iris.Plot("SepalLength", "SepalWidth", col="Species")
iris.Plot("SepalLength", "SepalWidth", row="Species")
```

When a categorical variable is plot against a numerical variable, the plot can be either a simple point plot, or a boxplot, or a violin plot.

```
iris.Plot("Species", "SepalLength")
iris.Plot("Species", "SepalLength", kind="box")
iris.Plot("Species", "SepalLength", kind="violin")
```

