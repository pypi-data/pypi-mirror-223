from __future__ import annotations

import asyncio
from pathlib import Path

import numpy as np
import pytest

from tno.mpc.communication import Pool

from tno.fl.protocols.cox_regression.client import Client
from tno.fl.protocols.cox_regression.config import Config
from tno.fl.protocols.cox_regression.server import Server

CONFIG_TEXT = """
[Experiment]
data_columns=age,grade,nodes,pgr,er,meno,hormon
time_column=dtime
target_column=death
n_epochs=25
n_bins=25
learning_rate=hessian

[Parties]
clients=local1,local2
server=Server

[Server]
address=localhost
port=8000

[local1]
address=localhost
port=8001
train_data=examples/rotterdam/data_alice.csv

[local2]
address=localhost
port=8002
train_data=examples/rotterdam/data_bob.csv
"""


@pytest.mark.asyncio
async def test_protocol(
    tmp_path: Path, http_pool_trio: tuple[Pool, Pool, Pool]
) -> None:
    """
    Run the Cox regression with the Rotterdam example

    :param tmp_path: temporary path fixture
    :param http_pool_trio: communication pool fixture for 3 parties
    """
    # Set up the config file
    config_filename = tmp_path / "config.ini"
    with open(config_filename, "w", encoding="UTF-8") as text_file:
        text_file.write(CONFIG_TEXT)

    # Run the protocol
    config = Config.from_file(config_filename)
    server = Server(config)
    client1 = Client(config, "local1")
    client2 = Client(config, "local2")

    server.pool = http_pool_trio[0]
    client1.pool = http_pool_trio[1]
    client2.pool = http_pool_trio[2]
    client1.SERVER_ID = "local0"
    client2.SERVER_ID = "local0"

    models = await asyncio.gather(server.run(), client1.run(), client2.run())
    assert (models[0] == models[1]).all()
    assert (models[0] == models[2]).all()
    assert np.isclose(
        models[0],
        np.expand_dims(
            [
                1.86449847e-02,
                3.89188321e-01,
                9.82261632e-02,
                -4.17423605e-04,
                -4.65078085e-05,
                -2.56380564e-02,
                -9.38696967e-02,
                -6.86025374e00,
                -5.63603967e00,
                -5.26000426e00,
                -4.99814596e00,
                -5.17402824e00,
                -5.22295515e00,
                -5.15305936e00,
                -5.26649996e00,
                -5.19298631e00,
                -5.40067082e00,
                -5.66413637e00,
                -5.32790654e00,
                -4.91227922e00,
                -4.84025114e00,
                -5.49584117e00,
                -5.33377527e00,
                -4.94023371e00,
                -5.58201662e00,
                -6.01541961e00,
                -3.79886969e00,
                -4.95485433e00,
                -4.09474962e00,
                -2.81158475e01,
                -2.81444680e01,
            ],
            -1,
        ),
        rtol=1e-05,
        atol=1e-08,
        equal_nan=False,
    ).all()
