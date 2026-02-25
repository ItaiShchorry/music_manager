import type { LoginRequest, TokenResponse, User } from '../types'
import client from './client'

export async function login(credentials: LoginRequest): Promise<TokenResponse> {
  const params = new URLSearchParams()
  params.append('username', credentials.email)
  params.append('password', credentials.password)

  const { data } = await client.post<TokenResponse>('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export async function getMe(): Promise<User> {
  const { data } = await client.get<User>('/auth/me')
  return data
}
