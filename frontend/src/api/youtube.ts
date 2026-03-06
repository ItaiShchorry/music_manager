import type { YouTubeBrief, YouTubeBriefStat } from '../types'
import client from './client'

export interface CreateBriefRequest {
  concept_type: string
  key_message?: string
  context?: string
}

export interface UpdateBriefRequest {
  status?: string
  youtube_url?: string
  seo_title?: string
  key_message?: string
}

export interface LogStatsRequest {
  snapshot_date: string
  views?: number
  likes?: number
  comments?: number
  subscribers_gained?: number
}

export async function generateBrief(songId: number, data: CreateBriefRequest): Promise<YouTubeBrief> {
  const resp = await client.post<YouTubeBrief>(`/songs/${songId}/youtube-briefs`, data)
  return resp.data
}

export async function listBriefsForSong(songId: number): Promise<YouTubeBrief[]> {
  const resp = await client.get<YouTubeBrief[]>(`/songs/${songId}/youtube-briefs`)
  return resp.data
}

export async function listAllBriefs(status?: string): Promise<YouTubeBrief[]> {
  const params = status ? { status } : {}
  const resp = await client.get<YouTubeBrief[]>('/youtube-briefs', { params })
  return resp.data
}

export async function getBrief(id: number): Promise<YouTubeBrief> {
  const resp = await client.get<YouTubeBrief>(`/youtube-briefs/${id}`)
  return resp.data
}

export async function updateBrief(id: number, data: UpdateBriefRequest): Promise<YouTubeBrief> {
  const resp = await client.patch<YouTubeBrief>(`/youtube-briefs/${id}`, data)
  return resp.data
}

export async function deleteBrief(id: number): Promise<void> {
  await client.delete(`/youtube-briefs/${id}`)
}

export async function logStats(briefId: number, data: LogStatsRequest): Promise<YouTubeBriefStat> {
  const resp = await client.post<YouTubeBriefStat>(`/youtube-briefs/${briefId}/stats`, data)
  return resp.data
}
