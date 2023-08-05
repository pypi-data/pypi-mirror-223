"""
Server module for cox regression
"""

import numpy as np
import numpy.typing as npt

from tno.fl.protocols.logistic_regression.server import Server as LogRegServer

from tno.fl.protocols.cox_regression import msg_ids
from tno.fl.protocols.cox_regression.config import Config


class Server(LogRegServer):
    """
    The Server class. Responsible for aggregating results of the clients.
    Based on logistic regression server.
    """

    def __init__(self, config: Config) -> None:
        """
        Initializes the server

        :param config: The configuration for the experiment
        """
        self.config: Config
        super().__init__(config)

    async def preprocessing(self) -> None:
        """
        Receive local maximum event times and distribute global maximum event time.
        """
        local_max_times = await self.pool.recv_all(msg_id=msg_ids.LOCAL_MAX_TIME)
        global_max_time = max(max_time for _, max_time in local_max_times)
        await self.pool.broadcast(global_max_time, msg_ids.GLOBAL_MAX_TIME)

    def initial_model(self) -> npt.NDArray[np.float64]:
        """
        Returns an initial model with zeros.
        Number of coefficients is based on number of covariates and number of time bins

        :return: An initialized model for cox regression
        """
        return np.zeros((len(self.config.data_columns) + self.config.n_bins - 1, 1))
