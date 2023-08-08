from invenio_records_resources.services import RecordService
from invenio_records_resources.services.uow import (
    RecordCommitOp,
    unit_of_work
)

from oarepo_published_service.services import PublishedServiceConfig

class PublishedService(RecordService):
    def __init__(self, config: PublishedServiceConfig):
        self.config = config
    
    @unit_of_work()
    def _create(
        self, record_cls, identity, data, raise_errors=True, uow=None, expand=False
    ):
        """Create a record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param bool raise_errors: raise schema ValidationError or not.
        """
        self.require_permission(identity, "create")
        
        # Validate data and create record with pid
        data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=raise_errors  # if False, flow is continued with data
            # only containing valid data, but errors
            # are reported (as warnings)
        )

        parent = record_cls.parent_record_cls.create({})
        parent.commit()

        # It's the components who saves the actual data in the record.
        record = record_cls.create(
            {},
            parent=parent,
        )

        # Run components
        self.run_components(
            "create",
            identity,
            data=data,
            record=record,
            errors=errors,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(record, self.indexer))

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            errors=errors,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )