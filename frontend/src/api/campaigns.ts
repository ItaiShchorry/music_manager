import api from './client'
import type { Campaign, BudgetRecommendation, CampaignLearnings, Expense } from '../types'

export interface CampaignCreate {
  name: string
  release_type: 'single' | 'ep' | 'album'
  start_date: string
  end_date: string
  budget_total: number
  primary_goal?: 'awareness' | 'growth' | 'monetization'
  notes?: string
  song_ids?: number[]
}

export interface ExpenseCreate {
  expense_date: string
  amount: number
  category: 'playlist_pitching' | 'social_ads' | 'content' | 'radio_promotion' | 'submithub' | 'pr' | 'other'
  subcategory?: string
  description?: string
}

export const listCampaigns = (): Promise<Campaign[]> =>
  api.get('/campaigns').then((r) => r.data)

export const getCampaign = (id: number): Promise<Campaign> =>
  api.get(`/campaigns/${id}`).then((r) => r.data)

export const createCampaign = (payload: CampaignCreate): Promise<Campaign> =>
  api.post('/campaigns', payload).then((r) => r.data)

export const updateCampaign = (id: number, patch: Partial<Pick<Campaign, 'name' | 'status' | 'notes' | 'primary_goal'>>): Promise<Campaign> =>
  api.patch(`/campaigns/${id}`, patch).then((r) => r.data)

export const deleteCampaign = (id: number): Promise<void> =>
  api.delete(`/campaigns/${id}`)

export const getBudgetRecommendation = (campaignId: number): Promise<BudgetRecommendation> =>
  api.post(`/campaigns/${campaignId}/budget-recommendation`).then((r) => r.data)

export const listExpenses = (campaignId: number): Promise<Expense[]> =>
  api.get(`/campaigns/${campaignId}/expenses`).then((r) => r.data)

export const addExpense = (campaignId: number, payload: ExpenseCreate): Promise<Expense> =>
  api.post(`/campaigns/${campaignId}/expenses`, payload).then((r) => r.data)

export const applyLearnings = (campaignId: number): Promise<CampaignLearnings> =>
  api.post(`/campaigns/${campaignId}/apply-learnings`).then((r) => r.data)
