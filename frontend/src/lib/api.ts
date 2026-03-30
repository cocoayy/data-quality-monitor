import { AlertDetail, AlertListResponse } from "@/types/alert";
import {
  DashboardHistoryResponse,
  DashboardSummaryResponse,
  OrganizationListResponse,
} from "@/types/dashboard";
import {
  DatasetDetailResponse,
  DatasetListResponse,
  QualityReasonListResponse,
  QualityScoreHistoryResponse,
} from "@/types/dataset";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${path}`);
  }

  return response.json();
}

export async function fetchDatasets(params?: {
  page?: number;
  pageSize?: number;
  organizationId?: string;
  sourceType?: string;
  monitoringEnabled?: boolean;
  evaluationStatus?: string;
  rank?: string;
  minTotalScore?: number;
  maxTotalScore?: number;
  keyword?: string;
  sortBy?: string;
  sortOrder?: string;
}): Promise<DatasetListResponse> {
  const searchParams = new URLSearchParams();

  if (params?.page) searchParams.set("page", String(params.page));
  if (params?.pageSize) searchParams.set("page_size", String(params.pageSize));
  if (params?.organizationId) searchParams.set("organization_id", params.organizationId);
  if (params?.sourceType) searchParams.set("source_type", params.sourceType);
  if (params?.monitoringEnabled !== undefined) {
    searchParams.set("monitoring_enabled", String(params.monitoringEnabled));
  }
  if (params?.evaluationStatus) searchParams.set("evaluation_status", params.evaluationStatus);
  if (params?.rank) searchParams.set("rank", params.rank);
  if (params?.minTotalScore !== undefined) {
    searchParams.set("min_total_score", String(params.minTotalScore));
  }
  if (params?.maxTotalScore !== undefined) {
    searchParams.set("max_total_score", String(params.maxTotalScore));
  }
  if (params?.keyword) searchParams.set("keyword", params.keyword);
  if (params?.sortBy) searchParams.set("sort_by", params.sortBy);
  if (params?.sortOrder) searchParams.set("sort_order", params.sortOrder);

  const query = searchParams.toString();
  return fetchJson<DatasetListResponse>(
    `/api/v1/datasets${query ? `?${query}` : ""}`,
  );
}

export async function fetchDatasetById(
  datasetId: string,
): Promise<DatasetDetailResponse> {
  return fetchJson<DatasetDetailResponse>(`/api/v1/datasets/${datasetId}`);
}

export async function fetchDatasetScoreHistory(
  datasetId: string,
): Promise<QualityScoreHistoryResponse> {
  return fetchJson<QualityScoreHistoryResponse>(
    `/api/v1/datasets/${datasetId}/quality-score/history`,
  );
}

export async function fetchDatasetScoreReasons(
  datasetId: string,
): Promise<QualityReasonListResponse> {
  return fetchJson<QualityReasonListResponse>(
    `/api/v1/datasets/${datasetId}/quality-score/reasons`,
  );
}

export async function fetchOrganizations(): Promise<OrganizationListResponse> {
  return fetchJson<OrganizationListResponse>("/api/v1/organizations");
}

export async function fetchDashboardSummary(
  organizationId?: string,
): Promise<DashboardSummaryResponse> {
  const query = organizationId
    ? `?organization_id=${encodeURIComponent(organizationId)}`
    : "";
  return fetchJson<DashboardSummaryResponse>(`/api/v1/dashboard/summary${query}`);
}

export async function fetchDashboardHistory(
  organizationId?: string,
): Promise<DashboardHistoryResponse> {
  const query = organizationId
    ? `?organization_id=${encodeURIComponent(organizationId)}`
    : "";
  return fetchJson<DashboardHistoryResponse>(`/api/v1/dashboard/history${query}`);
}

export async function fetchAlerts(params?: {
  datasetId?: string;
  organizationId?: string;
  alertType?: string;
  severity?: string;
  keyword?: string;
}): Promise<AlertListResponse> {
  const searchParams = new URLSearchParams();

  if (params?.datasetId) searchParams.set("dataset_id", params.datasetId);
  if (params?.organizationId) searchParams.set("organization_id", params.organizationId);
  if (params?.alertType) searchParams.set("alert_type", params.alertType);
  if (params?.severity) searchParams.set("severity", params.severity);
  if (params?.keyword) searchParams.set("keyword", params.keyword);

  const query = searchParams.toString();
  return fetchJson<AlertListResponse>(`/api/v1/alerts${query ? `?${query}` : ""}`);
}

export async function fetchAlertById(alertId: string): Promise<AlertDetail> {
  return fetchJson<AlertDetail>(`/api/v1/alerts/${alertId}`);
}

export async function patchMonitoringSettings(
  datasetId: string,
  body: {
    monitoringEnabled?: boolean;
    excludedFromScoring?: boolean;
    expectedUpdateCycle?: string;
  },
): Promise<{
  datasetId: string;
  monitoringEnabled: boolean;
  excludedFromScoring: boolean;
  expectedUpdateCycle: string | null;
  updatedAt: string | null;
}> {
  return fetchJson(`/api/v1/datasets/${datasetId}/monitoring-settings`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
}
