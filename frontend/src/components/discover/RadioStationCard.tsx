import { useState } from 'react'
import { createPitch } from '../../api/pitches'
import type { RadioStation } from '../../types'

interface Props {
  station: RadioStation
  recommended: boolean
  songId: number
  onPitched: () => void
}

export function RadioStationCard({ station, recommended, songId, onPitched }: Props) {
  const [showModal, setShowModal] = useState(false)
  const [method, setMethod] = useState('email')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handlePitch = async () => {
    setLoading(true)
    setError(null)
    try {
      await createPitch({
        song_id: songId,
        target_type: 'radio',
        radio_station_id: station.id,
        pitch_method: method,
      })
      setShowModal(false)
      onPitched()
    } catch {
      setError('Failed to log pitch. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="bg-white rounded-xl border border-gray-200 p-4 flex flex-col gap-3">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h4 className="font-semibold text-gray-900 truncate">{station.name}</h4>
              {station.name_hebrew && (
                <span className="text-sm text-gray-500" dir="rtl">{station.name_hebrew}</span>
              )}
            </div>
            <p className="text-xs text-gray-500 capitalize mt-0.5">{station.station_type}</p>
          </div>
          <span className={`flex-shrink-0 text-xs font-bold px-2 py-1 rounded-full ${
            recommended ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            {recommended ? 'Recommended' : 'Secondary'}
          </span>
        </div>

        <div className="flex flex-wrap gap-1.5 text-xs">
          {station.genres_focus?.slice(0, 3).map((g) => (
            <span key={g} className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full">{g}</span>
          ))}
        </div>

        {station.reach_description && (
          <p className="text-xs text-gray-500">{station.reach_description}</p>
        )}

        {station.response_time && (
          <p className="text-xs text-gray-400">Response time: {station.response_time}</p>
        )}

        <div className="flex items-center justify-between mt-1">
          {station.contact_email ? (
            <span className="text-xs text-gray-500">{station.contact_email}</span>
          ) : (
            <span className="text-xs text-gray-400">See website for contact</span>
          )}
          <button
            onClick={() => setShowModal(true)}
            className="text-xs bg-purple-600 text-white px-3 py-1.5 rounded-lg hover:bg-purple-700 transition-colors"
          >
            Mark Pitched
          </button>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm space-y-4">
            <h3 className="font-semibold text-gray-900">Log pitch to "{station.name}"</h3>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pitch method</label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="email">Email</option>
                <option value="instagram_dm">Instagram DM</option>
                <option value="spotify_for_artists">Spotify for Artists</option>
                <option value="submithub">SubmitHub</option>
              </select>
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <div className="flex gap-3 pt-1">
              <button
                onClick={handlePitch}
                disabled={loading}
                className="flex-1 bg-purple-600 text-white py-2 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Logging…' : 'Confirm'}
              </button>
              <button
                onClick={() => { setShowModal(false); setError(null) }}
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
