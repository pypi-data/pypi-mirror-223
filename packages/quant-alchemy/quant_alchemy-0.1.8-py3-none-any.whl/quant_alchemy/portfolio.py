import pandas as pd
import numpy as np
from scipy.optimize import minimize

class Portfolio:
    """
    A class to perform financial calculations on a portfolio.
    """
    
    def __init__(self, weights, returns):
        """
        Constructs all the necessary attributes for the Portfolio object.

        Parameters
        ----------
        weights: numpy.array
            The weights of the assets in the portfolio.
        returns: numpy.array or pandas.Series or pandas.DataFrame
            The returns of the assets.
        """
        self.weights = weights
        self.returns = returns
        self.covmat = self.cov_matrix()

    def cov_matrix(self):
        """
        Computes the covariance matrix of the returns.

        Returns
        -------
        numpy.array or pandas.DataFrame
            The covariance matrix of the returns.
        """
        return self.returns.cov()
    
    def portfolio_return(self):
        """
        Computes the return on a portfolio from constituent returns and weights.

        Returns
        -------
        float: The return on the portfolio.
        """
        return self.weights.T @ self.returns

    def portfolio_vol(self):
        """
        Computes the vol of a portfolio from a covariance matrix and constituent weights.

        Returns
        -------
        float: The volatility of the portfolio.
        """
        return (self.weights.T @ self.covmat @ self.weights)**0.5

    @staticmethod
    def plot_ef2(n_points, er, cov):
        """
        Plots the 2-asset efficient frontier.

        Parameters
        ----------
        n_points: int
            The number of points to plot.
        er: numpy.array or pandas.Series
            The returns of the two assets.
        cov: numpy.array or pandas.DataFrame
            The covariance matrix of the returns of the two assets.

        Returns
        -------
        matplotlib.figure.Figure
            The plot of the 2-asset efficient frontier.
        """
        if er.shape[0] != 2 or er.shape[0] != 2:
            raise ValueError("plot_ef2 can only plot 2-asset frontiers")
        weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
        rets = [w.T @ er for w in weights]
        vols = [(w.T @ cov @ w)**0.5 for w in weights]
        ef = pd.DataFrame({
            "Returns": rets, 
            "Volatility": vols
        })
        return ef.plot.line(x="Volatility", y="Returns", style=".-")

    def minimize_vol(self, target_return, er, cov):
        """
        Returns the optimal weights that achieve the target return
        given a set of expected returns and a covariance matrix
        """
        n = er.shape[0]
        init_guess = np.repeat(1/n, n)
        bounds = ((0.0, 1.0),) * n # an N-tuple of 2-tuples!
        # construct the constraints
        weights_sum_to_1 = {'type': 'eq',
                            'fun': lambda weights: np.sum(weights) - 1
        }
        return_is_target = {'type': 'eq',
                            'args': (er,),
                            'fun': lambda weights, er: target_return - self.portfolio_return(weights,er)
        }
        weights = minimize(self.portfolio_vol, init_guess,
                        args=(cov,), method='SLSQP',
                        options={'disp': False},
                        constraints=(weights_sum_to_1,return_is_target),
                        bounds=bounds)
        return weights.x