import type { Song } from '../types'
import client from './client'

export async function listSongs(): Promise<Song[]> {
  const { data } = await client.get<Song[]>('/songs')
  return data
}

export async function getSong(id: number): Promise<Song> {
  const { data } = await client.get<Song>(`/songs/${id}`)
  return data
}

export async function createSong(payload: { spotify_url: string }): Promise<Song> {
  const { data } = await client.post<Song>('/songs', payload)
  return data
}

export async function updateSong(
  id: number,
  patch: Partial<Pick<Song, 'story' | 'mood_tags' | 'themes' | 'comparable_artists'>>
): Promise<Song> {
  const { data } = await client.patch<Song>(`/songs/${id}`, patch)
  return data
}

export async function deleteSong(id: number): Promise<void> {
  await client.delete(`/songs/${id}`)
}
