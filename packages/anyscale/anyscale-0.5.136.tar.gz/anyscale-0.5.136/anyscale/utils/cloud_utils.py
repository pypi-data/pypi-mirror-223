import contextlib
import sys
from typing import Optional, Tuple
import uuid

from click.exceptions import ClickException

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.client.openapi_client.models import (
    CloudAnalyticsEvent,
    CloudAnalyticsEventCommandName,
    CloudAnalyticsEventError,
    CloudAnalyticsEventName,
    CreateAnalyticsEvent,
)
from anyscale.cloud import get_cloud_id_and_name


def get_organization_default_cloud(api_client: DefaultApi) -> Optional[str]:
    """Return default cloud name for organization if it exists and
        if user has correct permissions for it.

        Returns:
            Name of default cloud name for organization if it exists and
            if user has correct permissions for it.
        """
    user = api_client.get_user_info_api_v2_userinfo_get().result
    organization = user.organizations[0]  # Each user only has one org
    if organization.default_cloud_id:
        try:
            # Check permissions
            _, cloud_name = get_cloud_id_and_name(
                api_client, cloud_id=organization.default_cloud_id
            )
            return str(cloud_name)
        except Exception:  # noqa: BLE001
            return None
    return None


def get_default_cloud(
    api_client: DefaultApi, cloud_name: Optional[str]
) -> Tuple[str, str]:
    """Returns the cloud id from cloud name.
    If cloud name is not provided, returns the default cloud name if exists in organization.
    If default cloud name does not exist returns last used cloud.
    """

    if cloud_name is None:
        default_cloud_name = get_organization_default_cloud(api_client)
        if default_cloud_name:
            cloud_name = default_cloud_name
    return get_cloud_id_and_name(api_client, cloud_name=cloud_name)


def verify_anyscale_access(
    api_client: DefaultApi, cloud_id: str, logger: BlockLogger
) -> bool:
    try:
        api_client.verify_access_api_v2_cloudsverify_access_cloud_id_get(cloud_id)
        return True
    except ClickException as e:
        logger.error(
            f"Anyscale's control plane is unable to access resources on your cloud provider.\n{e}"
        )
        return False


class CloudEventProducer:
    """
    Produce events during cloud setup/register/verify
    """

    def __init__(self, api_client: DefaultApi):
        self.api_client = api_client
        self.cloud_id: Optional[str] = None

    def init_trace_context(
        self,
        command_name: CloudAnalyticsEventCommandName,
        cloud_id: Optional[str] = None,
    ):
        self.trace_id = str(uuid.uuid4().hex)
        self.command_name = command_name
        self.raw_command_input = str(" ".join(sys.argv[1:]))
        self.cloud_id = cloud_id

    def set_cloud_id(self, cloud_id: str):
        self.cloud_id = cloud_id

    def produce(
        self,
        event_name: CloudAnalyticsEventName,
        succeeded: bool,
        internal_error: Optional[str] = None,
    ):
        with contextlib.suppress(Exception):
            # shouldn't block cloud setup even if cloud event generation fails
            error = None
            if not succeeded:
                # TODO (congding): cloud provider error
                error_message = internal_error if internal_error else ""
                error = CloudAnalyticsEventError(internal_error=error_message,)

            self.api_client.produce_analytics_event_api_v2_analytics_post(
                CreateAnalyticsEvent(
                    cloud_analytics_event=CloudAnalyticsEvent(
                        trace_id=self.trace_id,
                        cloud_id=self.cloud_id,
                        succeeded=succeeded,
                        command_name=self.command_name,
                        raw_command_input=self.raw_command_input,
                        event_name=event_name,
                        error=error,
                    )
                )
            )
