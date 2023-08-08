#!/usr/bin/env python
"""
Class that uses Gaussian Process Regression to perform a fit of Thomson
scattering data found in provided .h5 files. Uses inference tools library
"""

import argparse
import h5py
from numpy import (
    ndarray,
    exp,
    abs,
    array,
    concatenate,
    linspace,
    max,
    mean,
    sqrt,
    where,
    argmin,
    argmax,
    gradient,
    diag,
    zeros,
    log,
    copy,
)
from scipy.linalg import block_diag
import matplotlib.pyplot as plt
from inference.covariance import CovarianceFunction
from inference.gp import ChangePoint, GpRegressor, SquaredExponential


class GPTSFit(object):
    """
    A class for performing Gaussian-process regression in one dimension for
    Thomson scattering profiles.  Gaussian-process regression (GPR) is a
    non-parametric regression technique, which can fit arbitrarily spaced data
    in any number of dimensions.
    """

    optmethod: str
    outliermethod: str
    plot: bool
    constrainAxisGradient: bool
    constrainEdgeGradient: bool

    def __init__(
        self,
        xx,
        yy,
        yerr,
        method="EmpBayes",
        outlierMethod="None",
        plot=False,
        constrainAxisGradient=True,
        constrainEdgeGradient=True,
        optimizer="bfgs",
    ):
        """
        Initialize the GPTSFit object
        :param method("EmpBayes): \
            The method to use for the fit. Options are: EmpBayes
        :param outlierMethod("None"): \
            The method for handling outliers. Options are: None, varyErrors
        :param plot(False): \
            Option to show plots. Options are True/False
        :param constrainAxisGradient(True): \
            Option to constraint fit gradient on axis to zero
        :param constraintEdgeGradient(True): \
            Option to constrain fit gradient at edge to zero
        :param optimizer("bfgs")
            Option for the optimizer to use during hyperparameter optimization
        """
        # store the input parameters
        self.optmethod = method
        self.outliermethod = outlierMethod
        self.plot = plot
        self.constrainAxisGradient = constrainAxisGradient
        self.constrainEdgeGradient = constrainEdgeGradient
        self.varyErrors = False
        self.optimizer = optimizer

        if self.optimizer not in ["bfgs", "diffev"]:
            raise ValueError(
                """
                [ GPFit Error ]
                >> Option optimizer must be "bfgs" (default) or "diffev"
                """
            )

        if outlierMethod == "varyErrors":
            self.varyErrors = True

        # read datafile to store data
        self.x = array(xx).flatten()
        self.y = array(yy).flatten()
        self.Ndata = len(self.x)
        self.dataerrors = True
        self.yerr = array(yerr).flatten()

        # normalize the data
        self.ydata = copy(self.y)
        self.yerrdata = copy(self.yerr)
        self.xdata = copy(self.x)
        self.y0 = max(self.y)
        self.y /= self.y0
        self.yerr /= self.y0
        self.m0 = mean(self.y)
        self.y -= self.m0

        # calculate covariance error matrix from yerr input
        self.ycov = diag(self.yerr**2)

        # constrain the gradient at the core to be zero
        if self.constrainAxisGradient:
            correlation = 1.0
            dx = 0.01
            error = 1.0
            self.Ndata += 2
            x_constraint = array([-dx, dx])
            y_constraint = array([1.0 - self.m0, 1.0 - self.m0])
            cov_constraint = error**2 * array(
                [[1.0, correlation], [correlation, 1.0]]
            )
            self.x = concatenate([x_constraint, self.x])
            self.y = concatenate([y_constraint, self.y])
            self.ycov = block_diag(cov_constraint, self.ycov)

        # constrain the gradient at the edge to be zero
        if self.constrainEdgeGradient:
            correlation = 1.0
            dx = 0.01
            error = 1.0
            self.Ndata += 2
            x_constraint = array([max(self.x) + dx, max(self.x) + 2 * dx])
            y_constraint = array([-self.m0, -self.m0])
            cov_constraint = error**2 * array(
                [[1.0, correlation], [correlation, 1.0]]
            )
            self.x = concatenate([self.x, x_constraint])
            self.y = concatenate([self.y, y_constraint])
            self.ycov = block_diag(self.ycov, cov_constraint)

        # allow errors to vary with minimum error set to experimental error
        if self.varyErrors:
            if not self.constrainAxisGradient:
                errors = HeteroskedasticUncertainties(
                    hyperpar_bounds=[(-10, 3) for _ in range(self.Ndata)]
                )
            else:
                hp_bounds = [(-10, 3) for _ in range(self.Ndata - 2)]
                con_bounds = [(-10, -9), (-10, -9)]
                hpbounds = [*con_bounds, *hp_bounds]
                errors = HeteroskedasticUncertainties(hyperpar_bounds=hpbounds)

        if plot:
            plt.errorbar(self.x, self.y, self.yerr)
            plt.show()

        # new axis for fit
        self.X = linspace(0.0, max(self.x), 200)
        dx = self.X[1] - self.X[0]

        # setup the kernel
        k1 = SquaredExponential()
        k2 = SquaredExponential()
        k3 = SquaredExponential()
        self.kernel = ChangePoint(
            [k1, k2, k3],
            location_bounds=[[0.85, 1.0], [1.0, 1.15]],
            width_bounds=[[dx, 1e-1], [dx, 1e-1]],
        )

        if self.varyErrors:
            self.kernel += errors
        # setup likelihood
        # if (self.outliermethod == "StudentT"):
        #     self.likelihood = MyStudentT(1.0,1.5)

        # setup the model
        if self.optmethod == "MCMC":
            raise ValueError(
                """
            [ GPFit Error ]
            >> Option method=MCMC is not avilable. Please choose EmpBayes.
            """
            )
        elif self.optmethod == "EmpBayes":
            if self.outliermethod == "StudentT":
                raise ValueError(
                    """
                    [ GPFit Error ]
                    >> Cannot use non-gaussian likelihood with emperical Bayes
                    """
                )
            self.model = GpRegressor(
                self.x,
                self.y,
                y_cov=self.ycov,
                kernel=self.kernel,
                n_starts=100,
                optimizer=self.optimizer,
            )

        else:
            print("Model choice not valid. Must be EmpBayes or MCMC.")
            return

        if self.outliermethod == "StudentT":
            raise ValueError(
                """
            [ GPFit Error ]
            >> Option for outliermethod=StudentT is not yet available.
            >> Please specify varyErrors or None.
            """
            )

    def __itfit(self) -> tuple:
        """
        Private method for doing the emperical Bayes fit
        """
        # optimize hyperparameters
        mean, sig = self.model(self.X)
        var = sig**2

        # unnormalize after fit
        mean += self.m0
        mean *= self.y0
        var *= self.y0 * self.y0

        return array(mean), array(var)

    def __itfitMCMC(self):
        """
        Private method for doing the MCMC fit
        """
        return

    def performfit(self, x=None) -> tuple:
        """
        Perform the fit once the GPTSFit object is setup. Returns a tuple of
        the mean and variance of the fit.
        """
        if x is not None:
            if x.ndim != 1:
                print("UNBAFFELD error: fit axis must be 1-dimensional.")
                return
            self.X = x
        if self.optmethod == "MCMC":
            self.mean, self.variance = self.__itfitMCMC()
        else:
            self.mean, self.variance = self.__itfit()
        self.err = sqrt(abs(self.variance))

        if self.plot:
            plt.plot(self.x, self.y, "o", label="data")
            plt.plot(self.X, self.mean, "r-", label="mean fit")
            plt.legend()
            plt.show()

            plt.plot(self.x, self.y0 * (self.y + self.m0), "o", label="data")
            plt.plot(self.X, self.mean, "r-", label="mean fit")
            plt.legend()
            plt.savefig("fit.png", dpi=300)
            plt.close()

        # fit the pedestal location and width
        xx = self.X.flatten()
        xwin = where((xx < 1.05) * (xx > 0.9))
        xx = xx[xwin]
        yp = gradient(self.mean.flatten()[xwin], xx)
        ypp = gradient(yp, xx)
        self.pedloc = xx[argmin(yp)]
        self.pedwid = abs(xx[argmax(ypp)] - xx[argmin(ypp)]) / 4.0

        return self.mean, self.variance

    def getSamples(self, N) -> ndarray:
        """
        Returns an array of sample fits
        :param N: \
            number of fits
        """
        # get the mean and covariance matrix
        means, covar = self.model.build_posterior(self.X)
        # draw samples from the distribution
        from numpy.random import multivariate_normal

        f_samples = multivariate_normal(means, covar, N)

        # unnormalize the samples
        f_samples += self.m0
        f_samples *= self.y0

        return array(f_samples).T

    def getPedestalInfo(self) -> tuple:
        """
        Returns a tuple of the pedestal information from the fit of the form
        (pedestal location, pedestal width).
        """
        return self.pedloc, self.pedwid

    def getHyperparameters(self) -> ndarray:
        """
        Returns an array of the hyperparameters of the model
        """
        return self.model.hyperpars

    def printHyperparameters(self, indent="") -> None:
        """
        Prints the hyperparameters of the model
        """
        k = indent + "kernel"
        c = indent + "change"
        print(k + "1 length scale: ", self.model.hyperpars[0])
        print(k + "1 scale: ", self.model.hyperpars[1])
        print(k + "2 length scale: ", self.model.hyperpars[2])
        print(k + "2 scale: ", self.model.hyperpars[3])
        print(k + "3 length scale: ", self.model.hyperpars[4])
        print(k + "3 scale: ", self.model.hyperpars[5])
        print(c + "point 1 location: ", self.model.hyperpars[7])
        print(c + "point 2 location: ", self.model.hyperpars[9])
        return

    def writeData(self, filename, time="", dataname="", postfix=None):
        """
        Writes the fit data to h5 file
        :param filename: \
            name of file to which the data are written
        :param time: \
            time of data slice - for writing to database files (default empty string)
        :param dataname: \
            name of the data/fit to be written to the h5 file (default None)
        """
        # Set up the names of all the things we are writing out
        fitlst = []
        datagrp = dataname + "_fit"
        if postfix is None:
            postfix = "_" + self.optmethod + "_" + self.outliermethod
        for nm in ["data", "variance", "rho_tor", "pedestal_height", "pedestal_width"]:
            fitlst.append(nm + postfix)

        # open file
        self.openh5file = h5py.File(filename, "a")

        # Structure of h5 file
        grpnm = "thomson_scattering/profiles/" + str(time) + "/" + datagrp
        if grpnm in self.openh5file:
            h5fit = self.openh5file[grpnm]
        else:
            h5fit = self.openh5file.create_group(grpnm)

        # Remove previous fits
        for fitname in fitlst:
            if fitname in h5fit:
                del h5fit[fitname]

        # write mean, variance, profile, and axis
        h5fit[fitlst[0]] = self.mean.T.flatten()
        h5fit[fitlst[1]] = self.err.T.flatten()
        h5fit[fitlst[2]] = self.X.T.flatten()
        h5fit[fitlst[3]] = self.pedwid
        h5fit[fitlst[4]] = self.pedloc
        self.openh5file.close()


class HeteroskedasticUncertainties(CovarianceFunction):
    def __init__(self, hyperpar_bounds=None):
        self.bounds = hyperpar_bounds

    def pass_spatial_data(self, x: ndarray):
        """
        Pre-calculates hyperparameter-independent part of the data covariance
        matrix as an optimisation.
        """
        n_params = x.shape[0]
        self.n_params = n_params
        self.dK = []
        for i in range(n_params):
            A = zeros([n_params, n_params])
            A[i, i] = 2.0
            self.dK.append(A)
        self.hyperpar_labels = [f"log_sigma_{i+1}" for i in range(n_params)]

    def estimate_hyperpar_bounds(self, y: ndarray):
        """
        Estimates bounds on the hyper-parameters to be
        used during optimisation.
        """
        # construct sensible bounds on the hyperparameter values
        s = log(y.ptp())
        self.bounds = [(s - 8, s + 2) for _ in range(self.n_params)]

    def __call__(self, u, v, theta):
        return zeros([u.size, v.size])

    def build_covariance(self, theta):
        """
        Optimized version of self.matrix() specifically for the data
        covariance matrix where the vectors v1 & v2 are both self.x.
        """
        sigma_sq = exp(2 * theta)
        return diag(sigma_sq)

    def covariance_and_gradients(self, theta):
        sigma_sq = exp(2 * theta)
        K = diag(sigma_sq)
        grads = [s * dk for s, dk in zip(sigma_sq, self.dK)]
        return K, grads

    def get_bounds(self):
        return self.bounds


def print_gpfit_options(args):
    """Routine for pretty print the key options used in GPR
    Return as string to either print or log
    """
    msg = ""
    msg += "GPR Fit options used are:\n"
    mopts = " [EmpBayes]"
    msg += "\tHyperparameter choice method: " + args.method + mopts + "\n"
    oopts = " [None varyErrors]"
    msg += "\tOutlier Method: " + str(args.outliermethod) + oopts + "\n"
    aeopts = " [True False]" + "\n"
    msg += "\tAxis Constraint: " + str(args.constrainAxisGradient) + aeopts
    msg += "\tEdge Constraint: " + str(args.constrainEdgeGradient) + aeopts
    aeopts = " [bfgs diffev]"
    msg += "\tOptimizer: " + str(args.optimizer) + aeopts
    return msg


def parse_gpfit(desc=None):
    """Set up parsing the arguments and return the parser.
    This enables other files to use the same parser
    """
    if not desc:
        desc = "Perform GPR on x and y data"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "files", type=str, nargs="+", help="h5 data file containing Thomson profile"
    )

    parser.add_argument(
        "-m",
        "--method",
        dest="method",
        default="EmpBayes",
        help="method to choose hyperparameter values: MCMC or EmpBayes",
    )
    parser.add_argument(
        "-o",
        "--outliers",
        dest="outliermethod",
        default=None,
        help="method for handling outliers: None, StudentT, or Detect",
    )
    parser.add_argument(
        "-a",
        "--axis_gradient_constraint",
        dest="constrainAxisGradient",
        help="Whether to constrain the axis gradient or not",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--edge_gradient_constraint",
        dest="constrainEdgeGradient",
        help="Whether to constrain the edge gradient or not",
        action="store_true",
    )
    parser.add_argument(
        "-z",
        "--optimizer",
        dest="optimizer",
        help="optimization method to use for hyperparameters",
        default="bfgs",
    )
    parser.add_argument(
        "-p", "--plot", dest="plot", help="Plot the data", action="store_true"
    )
    parser.add_argument(
        "-S", "--save", dest="save", help="Save plots as figures", action="store_true"
    )
    return parser


def main():
    """
    Read profile from provided .h5 file and fit.
    """
    parser = parse_gpfit()
    args = parser.parse_args()

    # TODO:  This doesn't match the class
    # args.input_data_file, args.method, args.kernel, args.outliermethod, True
    GPRfit = GPTSFit(args)
    _, _ = GPRfit.performfit()  # EmpBayes


if __name__ == "__main__":
    main()
