# This is demo code for implementation of Procrustes cross-validation method in Python
# It requires "pcv" and "matplotlib" packages.
#
# The code creates plots similar to what you can see on Figures with Corn example
# in this paper:
#

import numpy as np
from scipy.linalg import svd
from pcv import pcvpca, pcvpcr, pcvpls

# 0. Simple helper functions necessary to run the examples below

def pca_fit(X:np.ndarray, ncomp:int, center:bool = True, scale:bool = False) -> dict:
    """ Fits PCA model """

    nrows, ncols = X.shape

    # autoscale data and save vectors for centring and scaling
    mX = X.mean(axis = 0) if center else np.zeros(ncols)
    sX = X.std(axis = 0, ddof = 1) if scale else np.ones(ncols)
    X = (X - mX) / sX

    # get and return PCA outcomes by using SVD
    U, s, V = svd(X, full_matrices=False)
    return {
        'P': V[:ncomp, ...].T,
        'eigenvals': (s[:ncomp] * s[:ncomp]) / (nrows - 1),
        'mX': mX,
        'sX': sX,
        'ncomp': ncomp
    }


def pca_predict(X:np.ndarray, m:dict) -> dict:
    """ Project data to PCA model and return main PCA outcomes (scores, distances, variances). """

    nrows, ncols = X.shape
    ncomp = m['ncomp']

    # autoscale data and save vectors for centring and scaling
    X = (X - m['mX']) / m['sX']

    # get and return PCA outcomes by using SVD
    T = np.dot(T, m['P'])
    U = T / np.sqrt(m['eigenvals'])

    H = np.zeros((nrows, ncomp))
    Q = np.zeros((nrows, ncomp))
    expvar = np.zeros((1, ncomp))
    totvar = (X * X).sum()

    for a in range(1, m['ncomp'] + 1):
        Pa = m['P'][..., :a]
        Ta = T[..., :a]
        Ua = U[..., :a]
        Ea = X - np.dot(Ta, Pa.T)
        Q[..., a - 1] = (Ea * Ea).sum(axis = 1)
        H[..., a - 1] = (Ua * Ua).sum(axis = 1)
        expvar = 1 - Q[..., a - 1].sum() / totvar

    return {
        'T': T,
        'H': H,
        'Q': Q,
        'expvar': expvar
    }


# load original spectra and response values for Corn dataset
D = np.genfromtxt('corn.csv', delimiter=',')
X = D[:, 1:]
Y = D[:, :1]

# 1. PCA based examples

## create pseudo-validation set
Xpv = pcvpca(X, ncomp = 30, cv = {'type': 'ven', 'nseg': 4})

## show plot with original and generated spectra
#par(mfrow = c(2, 2))
#mdaplot(X, type = "l", cgroup = as.numeric(Y), main = "Original")
#mdaplot(Xpv, type = "l", cgroup = as.numeric(Y), main = "Pseudo-validation")
#mdaplot(prep.autoscale(X), type = "l", cgroup = as.numeric(Y), main = "Original (mean centered)")
#mdaplot(prep.autoscale(Xpv), type = "l", cgroup = as.numeric(Y), main = "Pseudo-validation (mean centered)")

## make PCA model for calibration set
m = pca_fit(X, 20)

## project calibration and pseudo-validation set to the model
res_cal = pca_predict(m, X)
res_pv = pca_predict(m, Xpv)

## show Distance plot for A = 2 and A = 20
plotResiduals(m, {'cal': res_cal, 'pv': res_pv}, ncomp = 2, main = "Distance plot (A = 2)")
plotResiduals(m, {'cal': res_cal, 'pv': res_pv}, ncomp = 20, main = "Distance plot (A = 20)")


# # 2. PLS based examples

# ## create pseudo-validation set for PLS model
# Xpv <- pcvpls(X, Y, ncomp = 30, cv = list("ven", 4))

# ## create PLS model using xpv as validation set
# m <- pls(X, Y, ncomp = 20, x.test = Xpv, y.test = Y)

# ## show the main plots
# par(mfrow = c(2, 2))
# plotXCumVariance(m)
# plotYCumVariance(m)
# plotRMSE(m)
# plotPredictions(m, 10)

# ## show heatmap for elements of D - it is returned as attribute of PC-set
# ## this plot must be identical to the first plot in the figure with heatmaps shown in the manuscript

# D <- attr(Xpv, "D")

# colmap <- mdaplot.getColors(256, colmap = c("blue", "white", "red"))
# par(mfrow = c(2, 1))
# plotD(Xpv)

# boxplot(D, range = 100, col = "gray", border = "gray", ylim = c(0, 2), xlab = "Components", ylab = expression(c[k]/c))
# abline(h = 1, col = "black", lty = 2)
# par(mar = c(5, 4, 2, 2))
