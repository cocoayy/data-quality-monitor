import {
  DatasetDetailResponse,
  DatasetListResponse,
  QualityReasonListResponse,
  QualityScoreHistoryResponse,
} from "@/types/dataset";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function fetchDatasets(): Promise<DatasetListResponse> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/datasets`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch datasets");
  }

  return response.json();
}

export async function fetchDatasetById(
  datasetId: string,
): Promise<DatasetDetailResponse> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/datasets/${datasetId}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch dataset detail");
  }

  return response.json();
}

export async function fetchDatasetScoreHistory(
  datasetId: string,
): Promise<QualityScoreHistoryResponse> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const response = await fetch(
    `${API_BASE_URL}/api/v1/datasets/${datasetId}/quality-score/history`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error("Failed to fetch dataset score history");
  }

  return response.json();
}

export async function fetchDatasetScoreReasons(
  datasetId: string,
): Promise<QualityReasonListResponse> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const response = await fetch(
    `${API_BASE_URL}/api/v1/datasets/${datasetId}/quality-score/reasons`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error("Failed to fetch dataset score reasons");
  }

  return response.json();
}