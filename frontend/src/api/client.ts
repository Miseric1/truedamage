/**
 * All backend calls funnel through this file rather than components calling
 * `fetch` directly. That means: one place to add auth headers later, one
 * place to change the base URL, and components stay focused on rendering
 * instead of knowing HTTP details.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export interface HealthResponse {
  status: string
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`)
  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`)
  }
  return response.json() as Promise<HealthResponse>
}
