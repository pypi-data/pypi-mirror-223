from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PIDDeletedError
from invenio_pidstore.models import (
    PersistentIdentifier,
    PIDStatus
)
import pytest

def test_create(published_service, sample_record, search_clear):
    created = published_service.create(system_identity, sample_record)

    assert PersistentIdentifier.query.filter(PersistentIdentifier.pid_value == created.id).first() is not None
    assert created["metadata"] == sample_record["metadata"]

def test_delete(published_service, sample_record, search_clear):
    created = published_service.create(system_identity, sample_record)
    
    is_deleted = published_service.delete(system_identity, created.id)
    
    assert is_deleted
    assert PersistentIdentifier.query.filter(PersistentIdentifier.pid_value == created.id).first().status == PIDStatus.DELETED
    with pytest.raises(PIDDeletedError):
        published_service.read(system_identity, created.id)

def test_read(published_service, sample_record, search_clear):
    created = published_service.create(system_identity, sample_record)
    
    read = published_service.read(system_identity, created.id)
    
    assert created.id == read.id
    assert created["metadata"] == read["metadata"]
    
def test_update(published_service, sample_record, search_clear):
    created = published_service.create(system_identity, sample_record)
    modified_record = sample_record
    modified_record["metadata"]["title"] = "Novy nazov"
    
    updated = published_service.update(system_identity, created.id, modified_record)
    
    assert updated["metadata"] == sample_record["metadata"]

def test_search(published_service, sample_record, search_clear):
    published_service.create(system_identity, sample_record)
    
    search_params = { "title": sample_record["metadata"]["title"] }
    search_result = published_service.search(system_identity, params=search_params)
    
    assert search_result is not None


