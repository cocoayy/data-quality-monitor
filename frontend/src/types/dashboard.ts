export type Organization = {
  organizationId: string;
  name: string;
  displayName: string | null;
  sourceType: string;
  isActive: boolean;
  createdAt: string | null;
  updatedAt: string | null;
};

export type OrganizationListResponse = {
  items: Organization[];
};

export type DashboardSummaryResponse = {
  measuredDate: string | null;
  summary: {
    totalDatasets: number;
    evaluatedDatasets: number;
    unevaluableDatasets: number;
    averageTotalScore: number;
    rankDistribution: {
      A: number;
      B: number;
      C: number;
      D: number;
      E: number;
    };
    criticalAlerts: number;
    warningAlerts: number;
  };
};

export type DashboardHistoryItem = {
  measuredDate: string;
  averageTotalScore: number;
  rankDistribution: {
    A: number;
    B: number;
    C: number;
    D: number;
    E: number;
  };
};

export type DashboardHistoryResponse = {
  items: DashboardHistoryItem[];
};
