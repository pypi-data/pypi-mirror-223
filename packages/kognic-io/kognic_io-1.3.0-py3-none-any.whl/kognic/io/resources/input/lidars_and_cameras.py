import logging
from typing import Optional, List

import kognic.io.model.input as input_model
import kognic.io.model.input.lidars_and_cameras as lc_model
from kognic.io.model.input.feature_flags import FeatureFlags
from kognic.io.resources.abstract import CreateableIOResource

log = logging.getLogger(__name__)


class LidarsAndCameras(CreateableIOResource):

    path = 'lidars-and-cameras'

    def create(
        self,
        lidars_and_cameras: lc_model.LidarsAndCameras,
        project: Optional[str] = None,
        batch: Optional[str] = None,
        annotation_types: Optional[List[str]] = None,
        dryrun: bool = False,
        feature_flags: Optional[FeatureFlags] = None
    ) -> Optional[input_model.CreateInputResponse]:
        """
        Upload files and create an input of type ``LidarsAndCameras``.

        :param lidars_and_cameras: class containing 2D and 3D resources that constitute the input
        :param project: project to add input to
        :param batch: batch, defaults to latest open batch
        :param annotation_types: annotation types for which to produce annotations for. Defaults to `None` (corresponds
         to all available annotation types). Passing an empty list will result in the same behaviour as passing `None`.
        :param dryrun: If True the files/metadata will be validated but no input job will be created.
        :param feature_flags Optional set of feature flags to control the input creation process.
        :returns InputJobCreated: Class containing id of the created input job, or `None` if dryrun.
        """
        if not isinstance(lidars_and_cameras, lc_model.LidarsAndCameras):
            raise ValueError(f"Cannot create a {type(lidars_and_cameras)} via this endpoint")

        response = self._post_input_request(
            self.path,
            lidars_and_cameras.to_dict(),
            project=project,
            batch=batch,
            annotation_types=annotation_types,
            imu_data=lidars_and_cameras.imu_data,
            resources=lidars_and_cameras.resources,
            dryrun=dryrun,
            feature_flags=feature_flags
        )

        if dryrun:
            return None

        log.info(f"Created inputs for files with uuid={response.input_uuid}")
        return input_model.CreateInputResponse.from_input_job_response(response)
