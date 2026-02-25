import { useCallback, useEffect, useState } from 'react'
import { getMe, login as apiLogin } from '../api/auth'
import type { LoginRequest, User } from '../types'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      setLoading(false)
      return
    }
    getMe()
      .then(setUser)
      .catch(() => localStorage.removeItem('token'))
      .finally(() => setLoading(false))
  }, [])

  const login = useCallback(async (credentials: LoginRequest) => {
    const tokenResponse = await apiLogin(credentials)
    localStorage.setItem('token', tokenResponse.access_token)
    const me = await getMe()
    setUser(me)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    setUser(null)
  }, [])

  return {
    user,
    loading,
    login,
    logout,
    isAuthenticated: user !== null,
  }
}
