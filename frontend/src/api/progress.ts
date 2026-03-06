import type { UserProgress } from '../types'
import client from './client'

export async function getProgress(): Promise<UserProgress> {
  const resp = await client.get<UserProgress>('/me/progress')
  return resp.data
}
