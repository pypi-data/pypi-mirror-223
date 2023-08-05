from pathlib import Path

from tno.fl.protocols.logistic_regression.config import Party

from tno.fl.protocols.cox_regression.config import Config

CONFIG_TEXT = """
[Experiment]
data_columns=age,grade,nodes,pgr,er,meno,hormon
time_column=dtime
target_column=death
n_epochs=25
n_bins=25
learning_rate=hessian

[Parties]
clients=Alice,Bob
server=Server

[Server]
address=localhost
port=8000

[Alice]
address=localhost
port=8001
train_data=data_alice.csv

[Bob]
address=localhost
port=8002
train_data=data_bob.csv
"""


def test_config_parse(tmp_path: Path) -> None:
    """
    Test parsing a configuration file

    :param tmp_path: temporary path fixture
    """

    # Set up the config file
    config_filename = tmp_path / "config.ini"
    with open(config_filename, "w", encoding="UTF-8") as text_file:
        text_file.write(CONFIG_TEXT)

    # Parse it
    config = Config.from_file(config_filename)

    # Test correctness
    correct_config = Config(
        clients=[
            Party(
                name="Alice",
                address="localhost",
                port=8001,
                train_data_path=Path("data_alice.csv"),
            ),
            Party(
                name="Bob",
                address="localhost",
                port=8002,
                train_data_path=Path("data_bob.csv"),
            ),
        ],
        server=Party(
            name="Server",
            address="localhost",
            port=8000,
            train_data_path=Path("."),
        ),
        data_columns=["age", "grade", "nodes", "pgr", "er", "meno", "hormon"],
        target_column="death",
        intercept=False,
        n_epochs=25,
        learning_rate=None,
        hessian=True,
        time_column="dtime",
        n_bins=25,
    )
    assert config == correct_config
