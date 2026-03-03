import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { ProtectedRoute } from './components/ProtectedRoute'
import { DiscoverPage } from './pages/DiscoverPage'
import { LoginPage } from './pages/LoginPage'
import { SongDetailPage } from './pages/SongDetailPage'
import { SongNewPage } from './pages/SongNewPage'
import { SongsPage } from './pages/SongsPage'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/songs" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/songs"
            element={
              <ProtectedRoute>
                <SongsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/songs/new"
            element={
              <ProtectedRoute>
                <SongNewPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/songs/:id"
            element={
              <ProtectedRoute>
                <SongDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/discover"
            element={
              <ProtectedRoute>
                <DiscoverPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
