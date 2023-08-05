"""
Configuration parsing and storage for logistic regression
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tno.fl.protocols.logistic_regression.config import Config as LogRegConfig
from tno.fl.protocols.logistic_regression.config import (
    ConfigParser as LogRegConfigParser,
)
from tno.fl.protocols.logistic_regression.config import Party


class ConfigParser(LogRegConfigParser):
    """
    Parser for cox regression config file.

    :param EXPERIMENT_TIME_COLUMN_KEY: Key for which column contains event/censoring times
    :param EXPERIMENT_N_BINS_KEY: Key for number of bins
    """

    EXPERIMENT_TIME_COLUMN_KEY = "time_column"
    EXPERIMENT_N_BINS_COLUMN_KEY = "n_bins"

    def __init__(self, config_file_path: Path):
        """
        Load the config file and parse the objects variables from the file.

        :param config_file_path: The path to the config file
        """
        super().__init__(config_file_path)

        self.time_column = self.parse_time_column()
        self.n_bins = self.parse_n_bins()

    def parse_time_column(self) -> str:
        """
        Parse the column containing event/censoring times.

        :return: The column containing event/censoring times
        """
        return self.config.get(self.EXPERIMENT_SECTION, self.EXPERIMENT_TIME_COLUMN_KEY)

    def parse_n_bins(self) -> int:
        """
        Parse the number of bins to use in stacking.

        :return: the number of bins
        :raises ValueError: if the number of bins is nonpositive
        """
        n_bins = self.config.getint(
            self.EXPERIMENT_SECTION, self.EXPERIMENT_N_BINS_COLUMN_KEY
        )
        if n_bins < 1:
            raise ValueError("Number of bins must a strictly positive integer.")
        return n_bins

    def parse_intercept(self) -> bool:
        """
        In cox regression, an intercept is never used.

        :return: False, indicating no intercept is used.
        """
        return False

    def to_config(self) -> Config:
        """
        Convert the parse to an actual config object.

        :return: the config object containing the data from the parsed config file
        """
        return Config(
            clients=self.clients,
            server=self.server,
            data_columns=self.data_columns,
            target_column=self.target_column,
            intercept=self.intercept,
            n_epochs=self.n_epochs,
            time_column=self.time_column,
            n_bins=self.n_bins,
            learning_rate=self.learning_rate,
            hessian=self.hessian,
        )


@dataclass
class Config(LogRegConfig):
    """
    The configuration of the experiment.
    Contains all attributes of the logistic regression config together with:

    :param time_column: The column containing event/censoring times
    :param n_bins: The number of bins to use in stacking
    """

    time_column: str
    n_bins: int

    def __init__(
        self,
        clients: list[Party],
        server: Party,
        data_columns: list[str],
        target_column: str,
        intercept: bool,
        n_epochs: int,
        learning_rate: float | None,
        hessian: bool,
        time_column: str,
        n_bins: int,
    ):
        """
        Forwards initialization arguments to parent class.
        """
        super().__init__(
            clients=clients,
            server=server,
            data_columns=data_columns,
            target_column=target_column,
            intercept=intercept,
            n_epochs=n_epochs,
            learning_rate=learning_rate,
            hessian=hessian,
        )
        self.time_column = time_column
        self.n_bins = n_bins

    @staticmethod
    def from_file(config_path: Path) -> Config:
        """
        Create config from config file

        :param config_path: The path to the file
        :return: The configuration according to config file
        """
        return ConfigParser(config_path).to_config()
