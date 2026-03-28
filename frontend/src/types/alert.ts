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

export type AlertDetail = {
  alertId: string;
  datasetId: string;
  alertType: string;
  severity: string;
  message: string;
  measuredAt: string | null;
  payload: Record<string, unknown> | null;
};
