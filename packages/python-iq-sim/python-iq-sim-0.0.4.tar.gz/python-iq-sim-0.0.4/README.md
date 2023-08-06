# Python-IQ-Sim

This repo is a python library for controlling starting stopping and managing simulations running in the Intelligent Quads Cloud.

## Installation

```bash
pip install python-iq-sim
```

## Generate Docs

```bash
pydoc-markdown -I iq_sim -m iq_sim --render-toc > docs/iq_sim.md
```

## Documentation Available 

https://intelligent-quads.gitbook.io/python-iq-sim-documentation/

## Example

```python
import iq_sim
import os
from pymavlink import mavutil


token = os.getenv("IQ_SIM_TOKEN")

api = iq_sim.iq_sim(token)
sim_id = api.start_sim()
api.wait_for_sim_ready(sim_id)

connection_info = api.get_connection(sim_id)
print(connection_info)
conn_str = f"tcp:{connection_info['ip']}:{connection_info['port']}"

mavlink_conn = mavutil.mavlink_connection(conn_str)
mavlink_conn.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (mavlink_conn.target_system, mavlink_conn.target_system))

# add pymavlink script here

api.stop_sim(sim_id)
```

## Customize Simulation Configuration

Simulation Configuration is in the form of:
```json
{
    "sim_config": [
        {
            "sim_type": "default-sitl",
            "vehicle_type": "ArduCopter",
            "vehicle_model": "X",
            "instances": "1",
            "flight_controls": "Ardupilot",
            "fc_version": "Copter-4.2.3",
            "latlonaltheading": [
                "-35.363261",
                "149.16523",
                "584",
                "353"
            ]
        }
    ]
}
```
the default config is available by accessing `iq_sim().sim_config`. This can be modified and passed to the `start_sim` method as shown below:


```python
import iq_sim
import os
from pymavlink import mavutil


token = os.getenv("IQ_SIM_TOKEN")

api = iq_sim.iq_sim(token)
config = api.sim_config
config["sim_config"][0]["instances"] = "2"
sim_id = api.start_sim(config)
api.wait_for_sim_ready(sim_id)

connection_info = api.get_connection(sim_id)
print(connection_info)
conn_str = f"tcp:{connection_info['ip']}:{connection_info['port']}"

mavlink_conn = mavutil.mavlink_connection(conn_str)
mavlink_conn.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (mavlink_conn.target_system, mavlink_conn.target_system))

# add pymavlink script here

api.stop_sim(sim_id)

```
