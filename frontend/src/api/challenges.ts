import type { CreationEntry } from '../types'
import client from './client'

export interface CompleteRequest {
  content_type: string
  text_content?: string
  file_url?: string
  external_url?: string
  caption_draft?: string
}

export async function completeChallenge(opportunityId: number, data: CompleteRequest): Promise<CreationEntry> {
  const resp = await client.post<CreationEntry>(`/challenges/${opportunityId}/complete`, data)
  return resp.data
}

export async function listCreations(status?: string): Promise<CreationEntry[]> {
  const params = status ? { status_filter: status } : {}
  const resp = await client.get<CreationEntry[]>('/challenges', { params })
  return resp.data
}

export async function uploadFile(file: File): Promise<{ file_url: string; filename: string }> {
  const form = new FormData()
  form.append('file', file)
  const resp = await client.post<{ file_url: string; filename: string }>('/uploads', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resp.data
}
