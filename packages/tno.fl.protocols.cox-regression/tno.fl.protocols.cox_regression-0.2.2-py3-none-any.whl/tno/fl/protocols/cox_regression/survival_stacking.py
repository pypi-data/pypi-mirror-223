"""
Implementation of survival stacking as described in https://arxiv.org/pdf/2107.13480.pdf.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def stack(
    covariates: npt.NDArray[np.int_ | np.float_],
    times: npt.NDArray[np.int_ | np.float_],
    failed: npt.NDArray[np.bool_],
    ids: npt.NDArray[np.int_] | None = None,
    time_bins: npt.NDArray[np.float_] | None = None,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.bool_]]:
    """
    This function stacks a dataset as described in https://arxiv.org/pdf/2107.13480.pdf.
    The input is in the form of separate numpy arrays. So for patient 1, we have its covariates
    in covariates[1], its failure time in times[1], and its event indicator in failed[1]. All the
    arrays should have the same length. Based on the input, the function takes into consideration
    time-dependency and/or discretization. When using discretization, we always use the situation
    at the beginning of a time interval. E.g. if a covariate changes within a time interval, this
    is recorded at the start of the next interval. Hence, if a covariate changes twice during an
    interval, the intermediate value will be lost. Patients censored within an interval will be
    recorded as having survived the interval.

    :param covariates: The covariates of the patients. Can have multiple columns.
    :param times: The failure/censoring times.
    :param failed: The event indicators. Should contain boolean values.
    :param ids: The patient ids. Can be used to specify time-varying covariates. The id is unique
        per patient and a patient can have multiple rows. However, a patient id can have only one
        failure.
    :param time_bins: If provided, a discrete stacker is used. The parameter should contain the
        starting times of each time interval. E.g. [0, 200, 400, 600] denotes time intervals 0-200,
        200-400, and 400-600. It's first value must be zero, and its largest value must be bigger
        than the biggest failure/censoring time value.
    :returns: The stacked data set in the form a multidimensional array containing the input data
        and a vector containing the target data.
    :raises ValueError: if the parameter values are inconsistent or not as specified above.
    """
    # Set default value for optional parameter ids. If not set, set unique id per row.
    ids_ = ids if ids is not None else np.arange(len(covariates))

    # Validate the input
    n_samples = covariates.shape[0]
    if (
        times.shape != (n_samples,)
        or failed.shape != (n_samples,)
        or (ids is not None and ids.shape != (n_samples,))
    ):
        raise ValueError("Not all parameters have the same lengths.")

    if time_bins is not None:
        if any(time_bins[i] >= time_bins[i + 1] for i in range(len(time_bins[:-1]))):
            raise ValueError("Time bins must be a strictly increasing sequence.")
        if time_bins[0] != 0:
            raise ValueError("First time bin should start at 0.")
        if time_bins[-1] < np.max(times):
            raise ValueError("The maximum time value is larger than the last time bin.")

    # Sort the data by time
    permutation = times.argsort()
    covariates = covariates[permutation]
    times = times[permutation]
    failed = failed[permutation]
    ids = ids_[permutation]

    # Set defaults for optional parameter time bins.
    # If not set, set time bins at the failure times in the data.
    time_bins = (
        time_bins
        if time_bins is not None
        else np.append(times[np.where(failed > 0)], times[-1] + 1)
    )

    # Useful variables
    bin_start_indices = np.array(
        [np.searchsorted(times, bin_start) for bin_start in time_bins]
    )
    risk_sets_size = np.array(
        [
            len(np.unique(ids_[start_idx:], return_index=True)[1])
            for start_idx in bin_start_indices
        ]
    )
    n_covariates = covariates.shape[1]
    n_time_bins = len(bin_start_indices) - 1

    # Allocate memory for stacked dataset
    size_of_stacked_dataset = np.sum(risk_sets_size)
    stacked = np.zeros((size_of_stacked_dataset, n_covariates + n_time_bins))
    target = np.zeros(size_of_stacked_dataset, dtype=np.bool_)

    # Fill the matrix time bin after time bin
    offset = 0
    for bin_idx, bin_start_idx in enumerate(bin_start_indices[:-1]):
        # Compute risk set
        risk_set_ids, risk_set_indices = np.unique(
            ids_[bin_start_idx:], return_index=True
        )
        risk_set_size = risk_sets_size[bin_idx]
        # Fill in the covariates
        stacked[offset : offset + risk_set_size, :n_covariates] = covariates[
            risk_set_indices + bin_start_idx
        ]
        # Fill in the risk set indicators
        stacked[
            offset : offset + risk_set_size, n_covariates + bin_idx
        ] = 1  # times[bin_start_idx]
        # Update the target matrix (failed for events in time bin, leave 0 for all others)
        bin_end_idx = bin_start_indices[bin_idx + 1]
        failed_ids = ids_[
            np.where(failed[bin_start_idx:bin_end_idx])[0] + bin_start_idx
        ]
        failed_in_bin_indices = np.where(np.isin(risk_set_ids, failed_ids))[0] + offset
        target[failed_in_bin_indices] = 1
        # Keep track of where we are in updating the stacked matrix and target vector
        offset = offset + risk_set_size
    return stacked, target
