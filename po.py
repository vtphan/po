from sklearn.cluster import KMeans, DBSCAN, SpectralClustering, AgglomerativeClustering, MeanShift
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph, KNeighborsClassifier
from sklearn import cross_validation, svm, tree
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import seaborn as sns
import pandas
import matplotlib.pyplot as plt
import math
import numpy as np
import statsmodels.formula.api as smf

def read_csv(filename, **kwargs):
   return Po(pandas.read_csv(filename, **kwargs))

class Po(pandas.core.frame.DataFrame):
   def __init__(self, df):
      super(Po, self).__init__(df)
      self.model = None

   def __getitem__(self, key):
      a = super(Po, self).__getitem__(key)
      return Po(a) if isinstance(a, pandas.core.frame.DataFrame) else a

   def query(self, expr, **kwargs):
      return Po(super(Po,self).query(expr, **kwargs))

   def check_columns(self, cols):
      if type(cols) == str:
         if cols not in self.keys():
            raise Exception("Invalid column: " + cols)
      else:
         unknown_columns = set(cols)-set(self.keys())
         if unknown_columns != set([]):
            raise Exception("Invalid columns: " + str(unknown_columns))

   def Regress(self, *cols):
      columns = list(cols); self.check_columns(columns)
      y = columns[-1]
      x = columns[0:-1]
      self.model = smf.ols(formula='%s ~ %s' % (y, '+'.join(x)), data=self)
      self.result = self.model.fit()
      print(self.result.summary())

   def Classify(self, *cols, method='logit', **argv):
      columns = list(cols); self.check_columns(columns)
      y = columns[-1]
      x = columns[0:-1]
      Y = self.get(y)
      X = self.get(x)
      Classifier = dict(
      	logit=LogisticRegression,
      	svm=svm.LinearSVC,
      	decision_tree=tree.DecisionTreeClassifier,
      	random_forest=RandomForestClassifier,
      	naive_bayes=GaussianNB,
      	gradient_descent=SGDClassifier,
      	knn=KNeighborsClassifier,
      	)
      self.model = Classifier.get(method)(**argv)
      self.model.fit(X,Y)

   def Cluster(self, *cols, **argv):
      columns = list(cols); self.check_columns(columns)
      option = {}
      Estimator = dict(kmeans=KMeans, meanshift=MeanShift, dbscan=DBSCAN, hierarchical=AgglomerativeClustering, spectral=SpectralClustering)

      if argv.get('method') is None:
         method = 'meanshift' if argv.get('clusters') is None else 'kmeans'
      else:
         if argv.get('method') not in Estimator:
            raise Exception("Unknown clustering method: " + argv.get('method'))
         method = argv.get('method', 'meanshift')

      if method == 'meanshift':
         pass
      elif method == 'dbscan':
         option['eps'] = argv.get('spacing', 0.3)
      else:
         if argv.get('clusters') is None:
            raise Exception("Must specify 'clusters', which is a number greater than 1.")
         option['n_clusters'] = argv.get('clusters')
         if argv.get('method') == 'hierarchical':
            option['linkage'] = argv.get('linkage', 'average')
            option['affinity'] = argv.get('affinity', 'euclidean')
         elif argv.get('method') == 'spectral':
            option['affinity'] = argv.get('affinity', 'rbf')

      self.model = Estimator.get(method)(**option)

      ## Select data
      rows = self.get(columns)
      if argv.get('scaled') == True:
         rows = StandardScaler().fit_transform(rows)

      ## Cluster and store results
      labels = self.model.fit_predict(rows)
      self['_'+method+'_'] = labels

      if method == 'kmeans':
         p = [ self.get(c) for c in columns ]
         self['_certainty_'] = [ self.point_entropy(p, i) for i in range(len(p[0])) ]

      print("\tClustering method: ", method, "\tNumber of clusters: ", len(set(labels)))


   def point_entropy(self, points, i):
      d = []

      for c in self.model.cluster_centers_:
         d.append(math.sqrt(sum((points[j][i]-c[j])**2 for j in range(len(points)))))
      d.sort()
      if d[0] == 0:
         entropy = 1 if d[1] != 0 else 0
      else:
         p1, p2 = float(d[0])/float(d[0]+d[1]), float(d[1])/float(d[0]+d[1])
         entropy = - (p1 * math.log(p1) + p2 * math.log(p2)) / math.log(2)

      return 1 - entropy


   def Plot(self, x, y=None, **kwargs):
      if x not in self.dtypes:
         raise Exception("Unknown column: " + x)
      if y is not None and y not in self.dtypes:
         raise Exception("Unknown column: " + y)

      if y is not None:
         if self.dtypes[x] in [int, float] and self.dtypes[y] in [int, float]:
            kwargs.setdefault("fit_reg", False)
            sns.lmplot(x=x, y=y, data=self, **kwargs)
         elif self.dtypes[x] in [object] and self.dtypes[y] in [int, float]:
            sns.factorplot(x=x, y=y, data=self, **kwargs)
         elif self.dtypes[y] in [object] and self.dtypes[x] in [int, float]:
            kwargs['orient'] = 'h'
            sns.factorplot(x=x, y=y, data=self, **kwargs)

      else:
         if self.dtypes[x] in [int, float]:
            sns.distplot(self[x], **kwargs)

      plt.show()


