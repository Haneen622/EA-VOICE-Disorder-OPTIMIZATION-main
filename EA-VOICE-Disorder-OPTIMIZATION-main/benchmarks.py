# benchmarks.py
# Minimal benchmark functions for your optimizer code

def F2(x, alpha=None):
    """
    Objective function expected by PSO/WOA code: objf(x, alpha)

    Here we simply minimize the number of selected features.
    x: solution vector
       last two genes are (gamma, cost) and the rest is feature-mask
    alpha: not used here, kept for compatibility with PSO.py signature
    """
    features = x[:-2]  # exclude last two hyperparameter genes
    # Many optimizers keep these as continuous; treat >0.5 as "selected"
    return sum(1 for v in features if v > 0.5)


def getFunctionDetails(idx):
    """
    Must return: [function_name, lb, ub]
    Your optimizer selects F2 when idx=1
    """
    if idx == 1:  # F2
        return ["F2", 0, 1]

    raise ValueError("Benchmark function not defined for idx=%s" % idx)
