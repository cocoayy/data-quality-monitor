import { AlertListResponse } from "@/types/alert";
import { DashboardSummaryResponse, OrganizationListResponse } from "@/types/dashboard";
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

export async function fetchDatasets(): Promise<DatasetListResponse> {
  return fetchJson<DatasetListResponse>("/api/v1/datasets");
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

export async function fetchDashboardSummary(): Promise<DashboardSummaryResponse> {
  return fetchJson<DashboardSummaryResponse>("/api/v1/dashboard/summary");
}

export async function fetchAlerts(): Promise<AlertListResponse> {
  return fetchJson<AlertListResponse>("/api/v1/alerts");
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