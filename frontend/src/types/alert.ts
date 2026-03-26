export type AlertSummary = {
  alertId: string;
  datasetId: string;
  datasetTitle: string;
  organizationId: string;
  alertType: string;
  severity: string;
  message: string;
  measuredAt: string | null;
};

export type AlertListResponse = {
  items: AlertSummary[];
};