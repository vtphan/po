from sklearn.cluster import KMeans, DBSCAN, SpectralClustering, AgglomerativeClustering, MeanShift
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph
import pandas

def read_csv(filename, **kwargs):
   df = pandas.read_csv(filename, **kwargs)
   return Po(df)

class Po(pandas.core.frame.DataFrame):
   def __init__(self, df):
      super(Po, self).__init__(df)

   def query(self, expr, **kwargs):
      self.estimator = None
      df = super(Po,self).query(expr, **kwargs)
      return Po(df)

   def Cluster(self, columns, **argv):
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

      self.estimator = Estimator.get(method)(**option)

      ## Select data
      rows = self.get(columns)
      if argv.get('scaled') == True:
         rows = StandardScaler().fit_transform(rows)

      ## Cluster and store results
      labels = self.estimator.fit_predict(rows)
      self['_'+method+'_'] = labels
      print("\tClustering method: ", method, "\tNumber of clusters: ", len(set(labels)))
      return self

