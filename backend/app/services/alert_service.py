class AlertService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_alerts(self, **kwargs):
        return self.repository.list_alerts(**kwargs)

    def get_alert_by_id(self, alert_id: str):
        return self.repository.get_alert_by_id(alert_id)
