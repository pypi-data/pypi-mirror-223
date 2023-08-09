from typing import List, Optional
from kognic.io import model as IAM
import kognic.io.client as IOC


def run(client: IOC.KognicIOClient, project: str, include_invalidated: bool = False) -> List[IAM.Input]:

    print("Listing inputs...")
    return client.input.get_inputs(project=project, include_invalidated=include_invalidated)


if __name__ == '__main__':
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "Project-identifier"
    run(client, project)
