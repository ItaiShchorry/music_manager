import { useState } from 'react'
import { createPitch } from '../../api/pitches'
import type { Playlist } from '../../types'

const METHOD_LABELS: Record<string, string> = {
  email: 'Email',
  instagram_dm: 'Instagram DM',
  spotify_for_artists: 'Spotify for Artists',
  submithub: 'SubmitHub',
}

interface Props {
  playlist: Playlist
  score: number
  reasons: string[]
  songId: number
  onPitched: () => void
}

export function PlaylistCard({ playlist, score, reasons, songId, onPitched }: Props) {
  const [showModal, setShowModal] = useState(false)
  const [method, setMethod] = useState(playlist.submission_method ?? 'email')
  const [loading, setLoading] = useState(false)

  const handlePitch = async () => {
    setLoading(true)
    try {
      await createPitch({
        song_id: songId,
        target_type: 'playlist',
        playlist_id: playlist.id,
        pitch_method: method,
      })
      setShowModal(false)
      onPitched()
    } finally {
      setLoading(false)
    }
  }

  const scoreColor =
    score >= 70 ? 'bg-green-100 text-green-800' :
    score >= 40 ? 'bg-yellow-100 text-yellow-800' :
    'bg-gray-100 text-gray-600'

  return (
    <>
      <div className="bg-white rounded-xl border border-gray-200 p-4 flex flex-col gap-3">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h4 className="font-semibold text-gray-900 truncate">{playlist.name}</h4>
            {playlist.curator_name && (
              <p className="text-xs text-gray-500 mt-0.5">by {playlist.curator_name}</p>
            )}
          </div>
          <span className={`flex-shrink-0 text-xs font-bold px-2 py-1 rounded-full ${scoreColor}`}>
            {score}%
          </span>
        </div>

        <div className="flex flex-wrap gap-1.5 text-xs">
          {playlist.follower_count != null && (
            <span className="bg-gray-50 border border-gray-200 px-2 py-0.5 rounded-full text-gray-600">
              {playlist.follower_count.toLocaleString()} followers
            </span>
          )}
          {playlist.genres?.slice(0, 3).map((g) => (
            <span key={g} className="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">{g}</span>
          ))}
        </div>

        {reasons.length > 0 && (
          <div className="flex flex-wrap gap-1 text-xs">
            {reasons.map((r) => (
              <span key={r} className="bg-green-50 text-green-700 px-2 py-0.5 rounded-full">✓ {r}</span>
            ))}
          </div>
        )}

        <div className="flex items-center justify-between mt-1">
          {playlist.submission_method ? (
            <span className="text-xs text-gray-500">
              via {METHOD_LABELS[playlist.submission_method] ?? playlist.submission_method}
            </span>
          ) : (
            <span className="text-xs text-gray-400 italic">No direct pitch</span>
          )}
          {playlist.submission_method && (
            <button
              onClick={() => setShowModal(true)}
              className="text-xs bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Mark Pitched
            </button>
          )}
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm space-y-4">
            <h3 className="font-semibold text-gray-900">Log pitch to "{playlist.name}"</h3>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pitch method</label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="email">Email</option>
                <option value="instagram_dm">Instagram DM</option>
                <option value="spotify_for_artists">Spotify for Artists</option>
                <option value="submithub">SubmitHub</option>
              </select>
            </div>
            <div className="flex gap-3 pt-1">
              <button
                onClick={handlePitch}
                disabled={loading}
                className="flex-1 bg-indigo-600 text-white py-2 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Logging…' : 'Confirm'}
              </button>
              <button
                onClick={() => setShowModal(false)}
                className="flex-1 border border-gray-300 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
