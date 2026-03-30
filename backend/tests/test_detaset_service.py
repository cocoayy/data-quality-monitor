import pytest

from app.services.dataset_service import DatasetService


class DummyRepository:
    def patch_monitoring_settings(self, **kwargs):
        return kwargs


def test_patch_monitoring_settings_invalid_cycle():
    service = DatasetService(DummyRepository())

    with pytest.raises(ValueError):
        service.patch_monitoring_settings(
            dataset_id="dummy",
            monitoring_enabled=True,
            excluded_from_scoring=False,
            expected_update_cycle="everyday",
        )
