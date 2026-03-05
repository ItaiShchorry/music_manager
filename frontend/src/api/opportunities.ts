import type { PostOpportunity } from '../types'
import client from './client'

export async function listOpportunities(): Promise<PostOpportunity[]> {
  const res = await client.get<PostOpportunity[]>('/api/v1/opportunities')
  return res.data
}

export async function generateOpportunities(songId?: number): Promise<PostOpportunity[]> {
  const res = await client.post<PostOpportunity[]>('/api/v1/opportunities/generate', {
    song_id: songId ?? null,
  })
  return res.data
}

export async function updateOpportunity(
  id: number,
  status: 'used' | 'dismissed' | 'remind_later',
): Promise<PostOpportunity> {
  const res = await client.patch<PostOpportunity>(`/api/v1/opportunities/${id}`, { status })
  return res.data
}
