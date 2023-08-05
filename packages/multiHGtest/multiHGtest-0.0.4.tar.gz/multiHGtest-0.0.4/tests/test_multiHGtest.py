import numpy as np
from scipy.stats import poisson

import sys
sys.path.append("../src")
from multiHGtest import testHG_dashboard, HCHGtest, FisherHGtest


def sample_survival_poisson(T, N1, N2, lam0, eps, r):
    """
    Sample :T: times from two survival populations with
    initial sizes :N1: and :N2:
    In each time t and group j, the reduction `Oj` is a Poisson RV.
    Usually, the Poisson rates are identical although in :eps:
    fraction the times the Poisson rate of O2 are elevated by an
    amount controlled by :mu:.

    Args:
    -----
    :T:    number of events
    :N1:   total in group 1 at t=0
    :N2:   total in group 2 at t=0
    :eps:  fraction of non-null events
    :lam0: baseline Poisson rate
    :r:   intensity of non-null events

    Note that since we sample from two Poisson distributions
    in each 'event', there is some possibility that we draw (O1,O2) = (0,0),
    hence there is no change in that event. This situation is different
    from standard notation.

    """

    Nt1 = np.zeros(T + 1)
    Nt2 = np.zeros(T + 1)

    lam1 = lam0  # `base` Poisson rates (does not have to be fixed)
    theta = np.random.rand(T) < eps

    lam2 = lam1.copy()
    tt = np.arange(T)
    nt = 2 * N1 * N2 / (N1 + N2) * np.exp(-lam0 * tt)
    mu = r / 2 * np.log(T)
    lam2[theta] = (np.sqrt(mu / nt[theta]) + np.sqrt(lam1[theta])) ** 2  # perturbed Poisson rates

    Nt1[0] = N1
    Nt2[0] = N2

    for t in np.arange(T):
        O1 = poisson.rvs(Nt1[t] * lam1[t] * (Nt1[t] > 0))
        O2 = poisson.rvs(Nt2[t] * lam2[t] * (Nt2[t] > 0))

        Nt1[t + 1] = np.maximum(Nt1[t] - O1, 0)
        Nt2[t + 1] = np.maximum(Nt2[t] - O2, 0)
    return Nt1, Nt2



def sample_survival_poisson_rand(T, N1, N2, lam0, eps, r):
    """
    Sample :T: times from two survival populations with initial sizes :N1: and :N2:
    In each time t and group j, the reduction `Oj` is a Poisson RV. Usually, the Poisson
    rates are identical although in :eps: fraction the times the Poisson rate of O2 are
    elevated by an amount controlled by :mu:.

    The perturbation is proportional to actual group sizes in each time
    (which is random).

    Args:
    -----
    :T:    number of events
    :N1:   total in group 1 at t=0
    :N2:   total in group 2 at t=0
    :eps:  fraction of non-null events
    :lam0: baseline Poisson rate
    :r:   intensity of non-null events

    """

    Nt1 = np.zeros(T + 1)
    Nt2 = np.zeros(T + 1)

    lam1 = lam0  # baseline risk
    theta = np.random.rand(T) < eps

    Nt1[0] = N1
    Nt2[0] = N2

    for t in np.arange(T):
        Nt = 2 * Nt1[t] * Nt2[t] / (Nt1[t] + Nt2[t])
        if Nt > 0:
            lam2 = (np.sqrt(lam1[t]) + theta[t] * np.sqrt(r * np.log(T) / 2 / Nt)) ** 2
        else:
            lam2 = 0

        O1 = poisson.rvs(Nt1[t] * lam1[t] * (Nt1[t] > 0))
        O2 = poisson.rvs(Nt2[t] * lam2 * (Nt2[t] > 0))

        Nt1[t + 1] = np.maximum(Nt1[t] - O1, 0)
        Nt2[t + 1] = np.maximum(Nt2[t] - O2, 0)
    return Nt1, Nt2




def main():
    T = 1000
    N1 = 5000
    N2 = 5000

    beta = .6
    r = 2

    lam0 = 1

    eps = T ** (-beta)
    lam = lam0 * np.ones(T) / T

    # sample data

    Nt1, Nt2 = sample_survival_poisson(T, N1, N2, lam, eps, r)
    Ot1 = -np.diff(Nt1)
    Ot2 = -np.diff(Nt2)


    # evaluate test statistics
    df, test_stats = testHG_dashboard(Nt1[:-1], Nt2[:-1], Ot1, Ot2, randomize=False)

    print(df)
    print(test_stats)

    hc = HCHGtest(Nt1[:-1], Nt2[:-1], Ot1, Ot2, randomize=False)
    fisher = FisherHGtest(Nt1[:-1], Nt2[:-1], Ot1, Ot2, randomize=False)
    print(hc)
    print(fisher[0])


if __name__ == '__main__':
    main()
