import numpy as np

import tno.fl.protocols.cox_regression.survival_stacking as stacking

# Set up test dataset for stacking

# PID,    cov1,   time,   fail
# 1,      0.3,    1,     0     --> censored patient
# 2,      0.4,    3,     1     --> patient that died
# 3,      0.6,    21,    0
# 3,      0.7,    33,    1     --> patient for which we have two events, time-dependency
#
# 0         10         20         30          40
# ---O       |          |          |
# -----X     |          |          |
# -----------|----------|-O--------|--X

IDS = np.array([1, 2, 3, 3])
COVARIATES = np.array([[0.3], [0.4], [0.6], [0.7]])
TIMES = np.array([1, 3, 21, 33])
FAILS = np.array([0, 1, 0, 1])
TIME_BINS = np.array([0, 10, 20, 30, 40])


def test_stacking_with_ids() -> None:
    """
    Tests the survival stacking with ids
    """
    stacked_input_with_ids, stacked_target_with_ids = stacking.stack(
        covariates=COVARIATES,
        times=TIMES,
        failed=FAILS,
        ids=IDS,
        time_bins=TIME_BINS,
    )
    assert np.isclose(
        stacked_input_with_ids,
        np.array(
            [
                [0.3, 1, 0, 0, 0],
                [0.4, 1, 0, 0, 0],
                [0.6, 1, 0, 0, 0],
                [0.6, 0, 1, 0, 0],
                [0.6, 0, 0, 1, 0],
                [0.7, 0, 0, 0, 1],
            ]
        ),
    ).all()
    assert np.isclose(stacked_target_with_ids, [0, 1, 0, 0, 0, 1]).all()


def test_stacking_without_ids() -> None:
    """
    Tests the survival stacking without ids
    """
    stacked_input_without_ids, stacked_target_without_ids = stacking.stack(
        covariates=COVARIATES,
        times=TIMES,
        failed=FAILS,
        ids=None,
        time_bins=TIME_BINS,
    )

    assert np.isclose(
        stacked_input_without_ids,
        np.array(
            [
                [0.3, 1, 0, 0, 0],
                [0.4, 1, 0, 0, 0],
                [0.6, 1, 0, 0, 0],
                [0.7, 1, 0, 0, 0],
                [0.6, 0, 1, 0, 0],
                [0.7, 0, 1, 0, 0],
                [0.6, 0, 0, 1, 0],
                [0.7, 0, 0, 1, 0],
                [0.7, 0, 0, 0, 1],
            ]
        ),
    ).all()
    assert np.isclose(stacked_target_without_ids, [0, 1, 0, 0, 0, 0, 0, 0, 1]).all()
