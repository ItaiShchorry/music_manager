import api from './client'
import type { DashboardSnapshot, HealthScoreResponse, Insight } from '../types'

export interface SnapshotCreate {
  total_streams: number
  total_monthly_listeners: number
  total_followers: number
  total_saves: number
  total_playlist_adds?: number
  streams_vs_last_week_pct?: number | null
  listeners_vs_last_week_pct?: number | null
  followers_vs_last_week_pct?: number | null
  cost_per_stream?: number | null
}

export const syncSnapshot = (payload: SnapshotCreate): Promise<DashboardSnapshot> =>
  api.post('/dashboard/snapshots', payload).then((r) => r.data)

export const getHealthScore = (): Promise<HealthScoreResponse> =>
  api.get('/dashboard/health-score').then((r) => r.data)

export const generateInsights = (): Promise<Insight[]> =>
  api.post('/dashboard/insights/generate').then((r) => r.data)

export const listInsights = (): Promise<Insight[]> =>
  api.get('/dashboard/insights').then((r) => r.data)

export const updateInsight = (id: number, status: 'dismissed' | 'actioned'): Promise<Insight> =>
  api.patch(`/dashboard/insights/${id}`, { status }).then((r) => r.data)
