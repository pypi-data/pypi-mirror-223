"""
Client module for cox regression
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
import pandas as pd

from tno.fl.protocols.logistic_regression.client import Client as LogRegClient

from tno.fl.protocols.cox_regression import msg_ids, survival_stacking
from tno.fl.protocols.cox_regression.config import Config


class Client(LogRegClient):
    """
    The client class, representing data owning clients in the learning process.
    Based on logistic regression client.
    """

    def __init__(self, config: Config, client_name: str) -> None:
        """
        Initializes the client

        :param config: The configuration for the experiment
        """
        self.config: Config
        super().__init__(config, client_name)

    def load_data(self) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.bool_]]:
        """
        Load the data as in logistic regression, but add the time column to the data.
        The time column is the last column in the data and can hence be used in further analysis.

        :return: A data set containing covariates and time column and an array containing failure
            data.
        :raises FileNotFoundError: if the training data file does not exist.
        """
        path = self.client.train_data_path
        if not path.exists():
            raise FileNotFoundError("The training data does not exist: ", path)
        csv_data: pd.DataFrame = pd.read_csv(path)
        return (
            csv_data[self.config.data_columns + [self.config.time_column]].to_numpy(),
            csv_data[self.config.target_column].to_numpy(),
        )

    async def get_global_max_time(self) -> int:
        """
        Get the global maximum event time.

        :return: The global maximum event time
        """
        # Share local max time with server
        local_max_time = self.data[:, -1].max()
        await self.pool.send(
            self.SERVER_ID, local_max_time, msg_id=msg_ids.LOCAL_MAX_TIME
        )
        # Receive global max event time from server
        return (
            int(await self.pool.recv(self.SERVER_ID, msg_id=msg_ids.GLOBAL_MAX_TIME))
            + 1
        )

    def compute_time_bins(self, global_max_time: int) -> npt.NDArray[np.float_]:
        """
        Compute time bins given a max event time

        :param global_max_time: The global max event time
        :return: The time bins
        """
        return np.linspace(0, global_max_time, self.config.n_bins)

    async def preprocessing(self) -> None:
        """
        Preprocess the data: create time bins and stack the data
        """
        global_max_time = await self.get_global_max_time()
        time_bins = self.compute_time_bins(global_max_time)
        self.data, self.target = survival_stacking.stack(
            covariates=self.data[:, :-1],
            times=self.data[:, -1],
            failed=self.target,
            time_bins=time_bins,
        )
