import numpy as np 
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KernelDensity

def get_bandwidth(values):

    cv = GridSearchCV(KernelDensity(kernel="gaussian"),
                        {'bandwidth': np.linspace(0.01, 1.0, 50)},
                        cv=np.min((20,values.shape[0]))) 
    cv.fit(values)

    return cv.best_params_["bandwidth"]

def compute_cloud(df,x,y,bandwidth=.1):
    kde = KernelDensity(bandwidth=bandwidth, 
                        kernel='gaussian').fit(df)
    X,Y = np.meshgrid(x ,
                      y)
    grid = np.array([X.ravel(), Y.ravel()]).T
    Z = np.exp(kde.score_samples(grid))
    Z = Z.reshape(X.shape)
    Z /= Z.sum()
    return X,Y,Z,kde

def get_density_by_role(X,Y,Z):
    masks = { "R1":np.logical_and(Y<=2.5, X<.05),
              "R2":np.logical_and(Y<=2.5, np.logical_and(.05<=X, X<.625)),
              "R3":np.logical_and(Y<=2.5, np.logical_and(.625<=X,X<.8)),
              "R4":np.logical_and(Y<=2.5, .8<=X),
              "R5":np.logical_and(Y>2.5, X<.3),
              "R6":np.logical_and(Y>2.5, np.logical_and(.3<=X,X<.75)),
              "R7":np.logical_and(Y>2.5, .75<=X)}
    density = {}
    for role,m in masks.items():
        density[role] = Z[m].sum()
    return density
