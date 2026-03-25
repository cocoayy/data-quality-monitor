export type Dataset = {
  datasetId: string;
  organizationId: string;
  title: string | null;
  sourceType: string;
  lastUpdated: string | null;
  monitoringEnabled: boolean;
  excludedFromScoring: boolean;
  createdAt: string | null;
  updatedAt: string | null;
};

export type DatasetListResponse = {
  items: Dataset[];
};