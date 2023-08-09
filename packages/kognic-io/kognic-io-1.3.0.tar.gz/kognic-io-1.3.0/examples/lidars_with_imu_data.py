from __future__ import absolute_import

import os.path
from uuid import uuid4

import kognic.io.client as IOC
import kognic.io.model.input as InputModel
import kognic.io.model.input.resources as ResourceModel
import kognic.io.model.input.lidars as lidar_model
from kognic.io.logger import setup_logging
from kognic.io.model.input.metadata.metadata import MetaData
from examples.imu_data.create_imu_data import create_dummy_imu_data


def run(client: IOC.KognicIOClient, project: str, dryrun: bool = True) -> InputModel.CreateInputResponse:
    print("Creating Lidars Input...")

    lidar_sensor1 = "lidar"
    metadata = MetaData.parse_obj({"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"})

    imu_data = create_dummy_imu_data(1557539923, 1557539925, 1e9)
    examples_path = os.path.dirname(__file__)
    lidars = lidar_model.Lidars(
        external_id=f"lidars-with-imu-data-example-{uuid4()}",
        frame=lidar_model.Frame(
            point_clouds=[ResourceModel.PointCloud(filename=examples_path + "/resources/point_cloud_RFL01.las", sensor_name=lidar_sensor1)],
            unix_timestamp=1644223851 * 1e9
        ),
        metadata=metadata,
        imu_data=imu_data
    )

    # Add input
    return client.lidars.create(lidars, project=project, dryrun=dryrun)


if __name__ == '__main__':
    setup_logging(level="INFO")
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"
    run(client, project)
