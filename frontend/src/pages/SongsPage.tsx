import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { listSongs } from '../api/songs'
import { SongCard } from '../components/songs/SongCard'

export function SongsPage() {
  const navigate = useNavigate()
  const { data: songs, isLoading, error } = useQuery({
    queryKey: ['songs'],
    queryFn: listSongs,
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">My Songs</h1>
        <button
          onClick={() => navigate('/songs/new')}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
        >
          + Add Song
        </button>
      </header>

      <main className="p-6">
        {isLoading && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-gray-200 animate-pulse aspect-square" />
            ))}
          </div>
        )}

        {error && (
          <p className="text-center text-red-600 mt-10">Failed to load songs. Please try again.</p>
        )}

        {songs && songs.length === 0 && (
          <div className="text-center mt-20 text-gray-400">
            <p className="text-5xl mb-4">🎵</p>
            <p className="text-lg font-medium">No songs yet</p>
            <p className="text-sm mt-1">Click "Add Song" to import from Spotify</p>
          </div>
        )}

        {songs && songs.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {songs.map((song) => (
              <SongCard key={song.id} song={song} />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
