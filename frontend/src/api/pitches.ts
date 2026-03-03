import type { PitchSubmission } from '../types'
import client from './client'

export interface CreatePitchPayload {
  song_id: number
  target_type: 'playlist' | 'radio'
  playlist_id?: number | null
  radio_station_id?: number | null
  pitch_method: string
  response_notes?: string | null
}

export async function createPitch(payload: CreatePitchPayload): Promise<PitchSubmission> {
  const { data } = await client.post<PitchSubmission>('/pitches', payload)
  return data
}

export async function getPitchesForSong(songId: number): Promise<PitchSubmission[]> {
  const { data } = await client.get<PitchSubmission[]>(`/songs/${songId}/pitches`)
  return data
}

export async function updatePitch(
  pitchId: number,
  patch: Partial<Pick<PitchSubmission, 'status' | 'response_notes' | 'response_date'>>
): Promise<PitchSubmission> {
  const { data } = await client.patch<PitchSubmission>(`/pitches/${pitchId}`, patch)
  return data
}
