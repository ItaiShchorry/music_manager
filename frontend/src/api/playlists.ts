import type { MatchResponse, Playlist } from '../types'
import client from './client'

export async function listPlaylists(params?: { language?: string; genre?: string }): Promise<Playlist[]> {
  const { data } = await client.get<Playlist[]>('/playlists', { params })
  return data
}

export async function getMatchesForSong(songId: number): Promise<MatchResponse> {
  const { data } = await client.get<MatchResponse>(`/songs/${songId}/matches`)
  return data
}
