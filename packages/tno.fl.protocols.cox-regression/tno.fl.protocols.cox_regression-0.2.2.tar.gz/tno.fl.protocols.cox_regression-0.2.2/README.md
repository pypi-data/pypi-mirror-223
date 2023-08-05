# TNO PET Lab - Federated Learning (FL) - Protocols - Cox Regression

The TNO PET Lab consists of generic software components, procedures, and
functionalities developed and maintained on a regular basis to facilitate and
aid in the development of PET solutions. The lab is a cross-project initiative
allowing us to integrate and reuse previously developed PET functionalities to
boost the development of new protocols and solutions.

The package `tno.fl.protocols.cox_regression` is part of the TNO Python Toolbox.

Implementation of a Federated Learning scheme for Cox Regression. It is based on
the library for Logistic Regression in the TNO PET lab. This library was
designed to facilitate both developers that are new to federated learning and
developers that are more familiar the technique.

Supports:

- Any number of clients and one server.
- Horizontal fragmentation
- Both fixed learning rate or second-order methods (Hessian)

This software implementation was financed via EUREKA ITEA labeling under Project
reference number 20050.

_Limitations in (end-)use: the content of this software package may solely be
used for applications that comply with international export control laws.  
This implementation of cryptographic software has not been audited. Use at your
own risk._

## Documentation

Documentation of the tno.fl.protocols.cox_regression package can be found
[here](https://docs.pet.tno.nl/fl/protocols/cox_regression/0.2.2).

## Install

Easily install the tno.fl.protocols.cox_regression package using pip:

```console
$ python -m pip install tno.fl.protocols.cox_regression
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.fl.protocols.cox_regression[tests]'
```

## Usage

In Federated Cox, several clients, each with their own data, wish to fit a Cox
model on their combined data. Each client computes a local update on their model
and sends this update to a central server. This server combines these updates,
updates the global model from this aggregated update and sends this new model
back to the clients. Then the process repeats: the clients compute the local
updates on this new model, send this to the server, which combines it and so on.
This is done until the server notices that the model has converged.

This package uses a combination of data preprocessing and federated logistic
regression to perform this federated Cox modelling. For each client, the input
data must be a .csv file in the usual format for survival data (specifics
below). Next, the package performs a procedure called survival stacking. This
procedure modifies the data in such a way that if we fit logistic regression on
the new data set, we obtain the coefficients of a Cox model. Therefore, the next
steps performs federated logistic regression and returns its coefficients. Each
of the steps will now be discussed in more detail.

#### Input data

Each row represents a subject, which has a number of covariates, a
failure/censoring time and a binary indicator whether the subject experienced
failure or was censored.  
Which column contains which information is specified in the configuration file
(see below).

_Note: At this moment, only csv-files are supported as input. Users can use
other file types or databases by overriding the `load_data()` method on the
clients._

#### Survival Stacking

As mentioned above, we use a method to transform fitting a cox model to fitting
a logistic regression model. This method is called 'Survival Stacking' and
described in [this paper](https://arxiv.org/abs/2107.13480). Basically, it
transforms the data such a way that we can obtain the Cox model parameters by
performing logistic regression. See the paper for more details. Note that best
results are achieved for large risk sets and will err the most for events that
occur near the end of the time period.

#### Federated Logistic Regression

For the implementation, we rely on
[this logistic regression package](https://github.com/TNO-FL/protocols.logistic_regression).

### Implementation

The implementation of federated cox consist of two classes with the suggestive
names `Client` and `Server`. Each client is an instance of `Client` and the
orchestrating server is an instance of the `Server` class. These classes are
passed a configuration object and a name (unique identifier for the client).
Calling the `.run()` method on the objects, will perform the federated learning
and returns the resulting logistic regression model (numpy array).

All settings are defined in a configuration file. This file is a `.ini` file and
a template is given in the `config.ini` (in the repository). An example is also
shown below in the minimal example. Here is an overview of what must be in the
configuration.

The files contains a Parties section in which the names of all clients and the
name of the server are listed. Next we have a separate section for each client
and server, containing the IP-address and port on which it can be reached. The
clients also have a link to the location of the `.csv`-file containing the
data.  
The 'Experiment' section contains the experiment configuration. Most of the
fields are self-explanatory:

- **data_columns**: the columns in the csv which should be used for training.
- **time_column**: The header of column containing event/censoring times.
- **target_column**: the target column in the csv (which should be predicted).
- **n_epochs**: maximum number of epochs
- **learning_rate**: the learning rate (float) or 'hessian'. If this value is
  'hessian', a second-order derivative is used as learning rate (Newton's
  method).
- **n_bins**: If discrete Cox should be used, put here the number of bins.

#### Communication

This package relies on the `tno.mpc.communication` package, which is also part
of the PET lab. It is used for the communication amongst the server and the
clients. Since this package uses `asyncio` for asynchronous handling, this
federated learning package depends on it as well. For more information about
this, we refer to the
[tno.mpc.communication documentation](https://docs.pet.tno.nl/mpc/communication)

### Example code

Below is a very minimal example of how to use the library. It consists of two
clients, Alice and Bob, who want to fit a cox model. Below are their two small
data sets. Note that in practice these would be way too small to fit a reliable
model.

`data_alice.csv`

```csv
var1,var2,var3,time,failure
0.104104,0.923302,1.22007,12.7973318626,1
0.781452,1.229076,0.069747,14.4093766173,1
1.613324,0.125566,1.921325,7.63949212526,1
0.068177,0.193788,2.693533,7.95449616061,1
0.406167,0.747936,1.240233,11.9701980352,1
1.602836,1.217881,0.350837,8.46420655566,1
0.401754,1.526443,0.449621,6.95252897093,0
0.305141,0.858988,3.883753,12.3573764607,1
0.620956,0.021884,3.20576,5.29165212342,1
2.193825,0.621184,0.466925,5.81874836313,1
```

`data_bob.csv`

```csv
var1,var2,var3,time,failure
0.621968,0.684428,0.135933,13.2176584654,1
0.323597,0.165159,0.97204,11.5169357575,0
0.647954,3.243631,0.034075,8.34491489657,1
0.106552,0.121843,0.257878,5.66506177628,1
1.239718,1.869215,0.020202,7.74300832502,1
0.000757,1.216615,0.861069,20.9813809356,1
1.01825,2.119666,0.716002,12.3366190173,1
0.853077,0.221376,1.635539,9.78044985255,1
1.806666,3.535072,2.176759,5.81052910695,1
1.389882,0.143133,0.821257,5.16269524116,0
```

Next, we create a configuration file for this experiment.

`config.ini`

```text
[Experiment]
data_columns=var1,var2,var3
time_column=time
target_column=failure
n_epochs=25
n_bins=10
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
```

Finally, we create the code to run the federated learning algorithm:

`main.py`

```python
import asyncio
import sys
from pathlib import Path

from tno.fl.protocols.cox_regression.client import Client
from tno.fl.protocols.cox_regression.config import Config
from tno.fl.protocols.cox_regression.server import Server


async def async_main() -> None:
    config = Config.from_file(Path("rotterdam.ini"))
    if sys.argv[1].lower() == "server":
        server = Server(config)
        print(await server.run())
    elif sys.argv[1].lower() == "alice":
        client = Client(config, "Alice")
        print(await client.run())
    elif sys.argv[1].lower() == "bob":
        client = Client(config, "Bob")
        print(await client.run())
    else:
        raise ValueError(
            "This player has not been implemented. Possible values are: server, alice, bob"
        )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_main())
```

To run this script, call `main.py` from the folder where the data files and the
config file are located. As command line argument, pass it the name of the party
running the app: 'Alice', 'Bob', or 'Server'. To run in on a single computer,
run the following three commands, each in a different terminal. Note that if a
client is started prior to the server, it will throw a ClientConnectorError.
Namely, the client tries to send a message to port the server, which has not
been opened yet. After starting the server, the error disappears.

```console
python main.py alice
python main.py bob
python main.py server
```

The output for the clients will be something similar to:

```console
>>> python main.py alice
2023-08-01 16:11:28,676 - tno.mpc.communication.httphandlers - INFO - Serving on localhost:8002
2023-08-01 16:11:28,691 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,691 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,707 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,707 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,722 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,722 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,734 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,734 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,734 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,750 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
2023-08-01 16:11:28,750 - tno.mpc.communication.httphandlers - INFO - Received message from 127.0.0.1:8000
[[2.1214126172776138], [0.039035037697618985], [0.5290931397920531], [-14.355284784838087], [-14.355284784838084], [-4.23172027479176], [-2.778626425074195], [-3.987265977480467], [-0.6026127569743797], [-1.1564113663049098], [-11.707555424183523], [10.698190979128784]]
```

We first see the client setting up the connection with the server. Then we have
ten rounds of training, as indicated in the configuration file. Finally, we
print the resulting model. We obtain the following coefficients for the
covariates. The other values represent the coefficients of the risk set
indicators respectively.

| Parameter | Coefficient          |
| --------- | -------------------- |
| var1      | 2.1214126172776138   |
| var2      | 0.039035037697618985 |
| var3      | 0.5290931397920531   |
