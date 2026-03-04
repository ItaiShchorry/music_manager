import api from './client'
import type { SubmitHubCampaign, SubmitHubSubmission } from '../types'

export interface SHCampaignCreate {
  song_id: number
  campaign_id?: number
  budget_allocated?: number
  curator_count?: number
  notes?: string
}

export interface SubmissionCreate {
  curator_name: string
  curator_genre_focus?: string[]
  curator_approval_rate?: number
  submission_date?: string
  cost?: number
}

export interface SubmissionUpdate {
  response_status?: 'pending' | 'approved' | 'declined'
  response_date?: string
  curator_feedback?: string
  playlist_added?: boolean
  playlist_url?: string
}

export const createSHCampaign = (payload: SHCampaignCreate): Promise<SubmitHubCampaign> =>
  api.post('/submithub-campaigns', payload).then((r) => r.data)

export const listSHCampaignsForSong = (songId: number): Promise<SubmitHubCampaign[]> =>
  api.get(`/songs/${songId}/submithub`).then((r) => r.data)

export const addSubmission = (shCampaignId: number, payload: SubmissionCreate): Promise<SubmitHubSubmission> =>
  api.post(`/submithub-campaigns/${shCampaignId}/submissions`, payload).then((r) => r.data)

export const listSubmissions = (shCampaignId: number): Promise<SubmitHubSubmission[]> =>
  api.get(`/submithub-campaigns/${shCampaignId}/submissions`).then((r) => r.data)

export const updateSubmission = (submissionId: number, patch: SubmissionUpdate): Promise<SubmitHubSubmission> =>
  api.patch(`/submithub-submissions/${submissionId}`, patch).then((r) => r.data)
