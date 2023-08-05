import numpy as np
from scipy.stats import hypergeom, uniform
from multitest import MultiTest
import pandas as pd


def hypergeom_test(k, M, n, N, alternative='two-sided', randomize=False):
    """
    Exact hypergeometric test

    Args:
    -----
        k:    number of observed Type I objects
        M:    total number of object
        n:    total number of Type I objects
        N:    number of draws
        randomize:   whether to do a randomized test
        alternative: type of alternative to consider. Options are:
                  'greater', 'less', 'two-sided'

        NOTE: For 'two-sided', the function only returns approximated P-values what is accurate for extreme values
        but less accurate for typical values.

    Returns:
        Test's P-value
    """

    if randomize:
        U1, U2 = uniform.rvs(size=(2, len(k)))
    else:
        U1 = U2 = 0

    if alternative == 'greater':
        return hypergeom.sf(k - 1, M, n, N) - U1 * hypergeom.pmf(k, M, n, N)  # sf is 1-cdf+Pk, so Pr(X >= k) = Pr(X>k-1)

    if alternative == 'less':
        return hypergeom.cdf(k, M, n, N) - U1 * hypergeom.pmf(k, M, n, N)

    if alternative == 'two-sided':
        l1 = hypergeom.cdf(k, M, n, N)
        l2 = hypergeom.cdf(N - k, M, n, N)

        r1 = hypergeom.sf(k - 1, M, n, N)
        r2 = hypergeom.sf(N - k + 1, M, n, N)
        l = np.minimum(l1, l2) - U1 * ((l1 < l2) * hypergeom.pmf(k, M, n, N) + (l1 > l2) * hypergeom.pmf(N - k, M, n, N)) / 2
        r = np.minimum(r1, r2) - U2 * ((r1 < r2) * hypergeom.pmf(k, M, n, N) + (r1 > r2) * hypergeom.pmf(N - k, M, n, N)) / 2
        return l + r

    raise ValueError("'alternative' must be one of 'grater', 'less', or 'two-sided'")


def _MultiTest(Nt1: list, Nt2: list, Ot1: list = None, Ot2: list = None, **kwargs):
    """

       Args:
           Nt1:  number of at-risk subjects in group 1 per time
           Nt2:  number of at-risk subjects in group 2 per time
           Ot1:  number failure events in group 1 per time
           Ot2:  number of failure events in group 1 per time
           **kwargs:

       Returns:
           MultiTest object
       """

    assert (len(Nt1) == len(Nt2))
    assert (len(Ot1) == len(Ot2))
    assert (len(Nt1) == len(Ot2))

    randomize = kwargs.get('randomize', False)
    alternative = kwargs.get('alternative', 'two-sided')

    pvals = hypergeom_test(Ot2, Nt2 + Nt1, Nt2, Ot1 + Ot2,
                           randomize=randomize, alternative=alternative)
    return MultiTest(pvals)


def HCHGtest(Nt1: np.ndarray, Nt2: np.ndarray, Ot1=None, Ot2=None, **kwargs):
    """
    higher criticism test of hypergeometric P-values for comparing survival data as
    described in: [1] Galili, Kipnis, Yakhini. 2023. Survival Analysis with Sensitivity to Rare and Weak Temporal
    Differences.

    Args:
        Nt1:  number of at-risk subjects in group 1 per time
        Nt2:  number of at-risk subjects in group 2 per time
        Ot1:  number failure events in group 1 per time; if Ot1 = None, then assume
              Ot1[i] = Nt1[i-1] - Nt1[i] (no censorship)
        Ot2:  number of failure events in group 1 per time; if Ot2 = None, then assume
              Ot2[i] = Nt2[i-1] - Nt2[i] (no censorship)
        **kwargs:

    Returns:
        HC test statistic

    """

    if Ot1 is None:
        Ot1 = -Nt1.diff()
        Nt1 = Nt1[:-1]
    if Ot2 is None:
        Ot2 = -Nt2.diff()
        Nt2 = Nt2[:-1]

    mtest = _MultiTest(Nt1, Nt2, Ot1, Ot2, **kwargs)
    gamma = kwargs.get('gamma', 0.2)
    return mtest.hc(gamma)[0]


def FisherHGtest(Nt1: np.ndarray, Nt2: np.ndarray, Ot1=[], Ot2=[], **kwargs):
    """
    Fisher combination test of hypergeometric P-values

    Args:
        Nt1:  number of at-risk subjects in group 1 per time
        Nt2:  number of at-risk subjects in group 2 per time
        Ot1:  number failure events in group 1 per time; if Ot1 = None, then assume
              Ot1[i] = Nt1[i-1] - Nt1[i] (no censorship)
        Ot2:  number of failure events in group 1 per time; if Ot2 = None, then assume
              Ot2[i] = Nt2[i-1] - Nt2[i] (no censorship)
        **kwargs:

    Returns:
        test statistic
        P-value of corresponding chi-squared test

    """

    if Ot1 == []:
        Ot1 = -Nt1.diff()
        Nt1 = Nt1[:-1]
    if Ot2 == []:
        Ot2 = -Nt2.diff()
        Nt2 = Nt2[:-1]

    mtest = _MultiTest(Nt1, Nt2, Ot1, Ot2, **kwargs)
    return mtest.fisher()


def testHG_dashboard(Nt1: np.ndarray, Nt2: np.ndarray, Ot1=[], Ot2=[], **kwargs):
    """

    Args:
        Nt1:  number of at-risk subjects in group 1 per time
        Nt2:  number of at-risk subjects in group 2 per time
        Ot1:  number failure events in group 1 per time; if Ot1 = None, then assume
              Ot1[i] = Nt1[i-1] - Nt1[i] (no censorship)
        Ot2:  number of failure events in group 1 per time; if Ot2 = None, then assume
              Ot2[i] = Nt2[i-1] - Nt2[i] (no censorship)
        **kwargs:

    Returns:
        test statistic
        P-value of corresponding chi-squared test

    """

    if Ot1 == []:
        Ot1 = -Nt1.diff()
        Nt1 = Nt1[:-1]
    if Ot2 == []:
        Ot2 = -Nt2.diff()
        Nt2 = Nt2[:-1]

    assert (len(Nt1) == len(Nt2))
    assert (len(Ot1) == len(Ot2))
    assert (len(Nt1) == len(Ot2))

    df = pd.DataFrame()
    df['at-risk1'] = Nt1
    df['at-risk2'] = Nt2
    df['events1'] = Ot1
    df['events2'] = Ot2

    df['at-risk1'] = df['at-risk1'].astype(int)
    df['at-risk2'] = df['at-risk2'].astype(int)
    df['events1'] = df['events1'].astype(int)
    df['events2'] = df['events2'].astype(int)

    randomize = kwargs.get('randomize', False)
    alternative = kwargs.get('alternative', 'two-sided')
    gamma = kwargs.get('gamma', 0.4)
    pvals = hypergeom_test(Ot2, Nt2 + Nt1, Nt2, Ot1 + Ot2,
                           randomize=randomize, alternative=alternative)
    df['pvalue'] = pvals

    stbl = kwargs.get('stbl', True)
    mtest = MultiTest(pvals, stbl=stbl)

    fisher, fisher_pval = mtest.fisher()
    hc, hct = mtest.hc(gamma=gamma)
    minP = np.exp(-mtest.minp())

    df['HCT'] = pvals <= hct

    return df, {'hc': hc,
                'fisher': fisher,
                'fisher_pval': fisher_pval,
                'minP': minP}
