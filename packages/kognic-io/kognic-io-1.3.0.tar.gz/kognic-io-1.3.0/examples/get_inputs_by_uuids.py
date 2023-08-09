from typing import List, Optional
from kognic.io import model as IAM
import kognic.io.client as IOC


def run(client: IOC.KognicIOClient, input_uuids: List[str]) -> List[IAM.Input]:

    print("Listing inputs...")
    return client.input.get_inputs_by_uuids(input_uuids=input_uuids)


if __name__ == '__main__':
    client = IOC.KognicIOClient()

    input_uuids = ["input-identifier"]
    run(client, input_uuids)
