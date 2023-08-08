from invenio_drafts_resources.services.records import RecordServiceConfig
from oarepo_runtime.config.permissions_presets import OaiHarvesterPermissionPolicy

from oarepo_published_service.services.records.components.pid_register import PidRegisterComponent

class PublishedServiceConfig:
    permission_policy_cls = OaiHarvesterPermissionPolicy
    
    @property
    def components(self):
        return [
            *self._proxied_drafts_config.components,
            PidRegisterComponent
        ]

    def __init__(self, proxied_drafts_config: RecordServiceConfig):
        self._proxied_drafts_config = proxied_drafts_config

    def __getattr__(self, name: str) -> None:
        if name in self.__dict__:
            return getattr(self, name)
        else:
            return getattr(self._proxied_drafts_config, name)