import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

np.random.seed(42)
crearr = np.random.rand(100,2)

KMeans = KMeans(n_clusters=5, random_state=42)
KMeans.fit(crearr)

centrides = KMeans.cluster_centers_
print(centrides)