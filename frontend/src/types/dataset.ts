export type QualityScoreBrief = {
  total: number | null;
  rank: string | null;
  evaluationStatus: string | null;
  measuredAt: string | null;
};

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
  qualityScore: QualityScoreBrief;
};

export type Pagination = {
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
};

export type DatasetListResponse = {
  items: Dataset[];
  pagination: Pagination;
};

export type DatasetResource = {
  resourceId: string;
  resourceType: string;
  format: string | null;
  resourceUrl: string | null;
  apiEndpoint: string | null;
  isMonitoringTarget: boolean;
  latestHttpStatus: number | null;
  latestResponseTimeMs: number | null;
  latestCheckedAt: string | null;
};

export type DatasetDetailResponse = {
  datasetId: string;
  organization: {
    organizationId: string;
    name: string;
  };
  sourceType: string;
  title: string | null;
  description: string | null;
  license: string | null;
  category: string | null;
  tags: string[] | null;
  lastUpdated: string | null;
  expectedUpdateCycle: string | null;
  monitoringEnabled: boolean;
  excludedFromScoring: boolean;
  createdAt: string | null;
  updatedAt: string | null;
  latestQualityScore: {
    completeness: number | null;
    freshness: number | null;
    accessibility: number | null;
    formatQuality: number | null;
    total: number | null;
    rank: string | null;
    evaluationStatus: string | null;
    measuredAt: string | null;
  };
  resources: DatasetResource[];
};

export type QualityScoreHistoryItem = {
  measuredDate: string;
  scores: {
    completeness: number | null;
    freshness: number | null;
    accessibility: number | null;
    formatQuality: number | null;
    total: number | null;
    rank: string | null;
    evaluationStatus: string | null;
  };
};

export type QualityScoreHistoryResponse = {
  datasetId: string;
  history: QualityScoreHistoryItem[];
};

export type QualityReason = {
  metricType: string;
  reasonCode: string;
  severity: string;
  message: string;
  detail: Record<string, unknown> | null;
};

export type QualityReasonListResponse = {
  datasetId: string;
  items: QualityReason[];
};
