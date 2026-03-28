class DatasetService:
    VALID_CYCLES = {"daily", "weekly", "monthly", "quarterly", "yearly", "unknown"}

    def __init__(self, repository) -> None:
        self.repository = repository

    def list_datasets(self, **kwargs):
        return self.repository.list_datasets(**kwargs)

    def get_dataset_by_id(self, dataset_id: str):
        return self.repository.get_dataset_by_id(dataset_id)

    def patch_monitoring_settings(
        self,
        dataset_id: str,
        monitoring_enabled: bool | None,
        excluded_from_scoring: bool | None,
        expected_update_cycle: str | None,
    ):
        if (
            expected_update_cycle is not None
            and expected_update_cycle not in self.VALID_CYCLES
        ):
            raise ValueError("invalid expectedUpdateCycle")

        return self.repository.patch_monitoring_settings(
            dataset_id=dataset_id,
            monitoring_enabled=monitoring_enabled,
            excluded_from_scoring=excluded_from_scoring,
            expected_update_cycle=expected_update_cycle,
        )
