import type { GeneratedContent } from '../types'
import client from './client'

export type PostType = 'release' | 'bts' | 'story' | 'engagement' | 'thank_you'
export type Tone = 'emotional' | 'excited' | 'casual'
export type Platform = 'instagram' | 'facebook' | 'tiktok'

export interface ContentRequest {
  post_type: PostType
  key_message?: string
  context?: string
  tones?: Tone[]
  platforms?: Platform[]
}

export async function generateContent(
  songId: number,
  request: ContentRequest,
): Promise<GeneratedContent[]> {
  const { data } = await client.post<GeneratedContent[]>(
    `/songs/${songId}/content`,
    request,
  )
  return data
}

export async function getGeneratedContent(songId: number): Promise<GeneratedContent[]> {
  const { data } = await client.get<GeneratedContent[]>(`/songs/${songId}/content`)
  return data
}
