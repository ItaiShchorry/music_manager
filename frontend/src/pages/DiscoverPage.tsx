import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useSearchParams } from 'react-router-dom'
import { getMatchesForSong } from '../api/playlists'
import { listSongs } from '../api/songs'
import { PlaylistCard } from '../components/discover/PlaylistCard'
import { RadioStationCard } from '../components/discover/RadioStationCard'
import { Nav } from '../components/Nav'

export function DiscoverPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const queryClient = useQueryClient()

  const selectedSongId = searchParams.get('song') ? Number(searchParams.get('song')) : null

  const { data: songs = [], isLoading: songsLoading } = useQuery({
    queryKey: ['songs'],
    queryFn: listSongs,
  })

  const {
    data: matches,
    isLoading: matchesLoading,
    error: matchesError,
  } = useQuery({
    queryKey: ['matches', selectedSongId],
    queryFn: () => getMatchesForSong(selectedSongId!),
    enabled: selectedSongId !== null,
  })

  const handleSongSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value
    if (val) {
      setSearchParams({ song: val })
    } else {
      setSearchParams({})
    }
  }

  const handlePitched = () => {
    if (selectedSongId !== null) {
      queryClient.invalidateQueries({ queryKey: ['pitches', selectedSongId] })
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />

      <main className="max-w-4xl mx-auto p-6 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">Discover</h1>
          <p className="text-sm text-gray-500">
            Select a song to see matching Israeli playlists and radio stations.
          </p>
        </div>

        {/* Song selector */}
        <div className="bg-white rounded-2xl shadow-sm p-5">
          <label className="block text-sm font-medium text-gray-700 mb-2">Select a song</label>
          {songsLoading ? (
            <p className="text-sm text-gray-400">Loading songs…</p>
          ) : (
            <select
              value={selectedSongId ?? ''}
              onChange={handleSongSelect}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">— choose a song —</option>
              {songs.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.title} — {s.artist_name}
                  {s.genre ? ` · ${s.genre}` : ''}
                </option>
              ))}
            </select>
          )}
          {selectedSongId && (() => {
            const song = songs.find((s) => s.id === selectedSongId)
            if (!song) return null
            const hasProfile = song.genre || song.language || (song.mood_tags?.length ?? 0) > 0
            if (!hasProfile) {
              return (
                <p className="mt-2 text-xs text-amber-600">
                  This song has no genre, language, or mood tags — scores will be 0.{' '}
                  <a href={`/songs/${song.id}`} className="underline hover:text-amber-800">
                    Add profile fields
                  </a>{' '}
                  for better matches.
                </p>
              )
            }
            return null
          })()}
        </div>

        {selectedSongId && (
          <>
            {matchesLoading && (
              <div className="flex items-center justify-center py-12">
                <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
              </div>
            )}

            {matchesError && (
              <p className="text-red-600 text-sm">Failed to load matches.</p>
            )}

            {matches && (
              <>
                {/* Playlists section */}
                <section className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-gray-900">
                      Playlists
                      <span className="ml-2 text-sm font-normal text-gray-400">
                        ({matches.playlists.length})
                      </span>
                    </h2>
                  </div>
                  {matches.playlists.length === 0 ? (
                    <p className="text-sm text-gray-400">No playlists found.</p>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {matches.playlists.map(({ playlist, score, reasons }) => (
                        <PlaylistCard
                          key={playlist.id}
                          playlist={playlist}
                          score={score}
                          reasons={reasons}
                          songId={selectedSongId}
                          onPitched={handlePitched}
                        />
                      ))}
                    </div>
                  )}
                </section>

                {/* Radio stations section */}
                <section className="space-y-4">
                  <h2 className="text-lg font-semibold text-gray-900">
                    Radio Stations
                    <span className="ml-2 text-sm font-normal text-gray-400">
                      ({matches.radio_stations.length})
                    </span>
                  </h2>
                  {matches.radio_stations.length === 0 ? (
                    <p className="text-sm text-gray-400">No radio stations found.</p>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {matches.radio_stations.map(({ station, recommended }) => (
                        <RadioStationCard
                          key={station.id}
                          station={station}
                          recommended={recommended}
                          songId={selectedSongId}
                          onPitched={handlePitched}
                        />
                      ))}
                    </div>
                  )}
                </section>
              </>
            )}
          </>
        )}
      </main>
    </div>
  )
}
