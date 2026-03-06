import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { YouTubeBrief } from '../../types'
import { generateBrief, listBriefsForSong, deleteBrief } from '../../api/youtube'
import { YouTubeBriefCard } from './YouTubeBriefCard'

const CONCEPT_TYPES = [
  { value: 'making_of', label: 'Making Of' },
  { value: 'acoustic_session', label: 'Acoustic Session' },
  { value: 'production_breakdown', label: 'Production Breakdown' },
  { value: 'song_explained', label: 'Song Explained' },
  { value: 'live_performance', label: 'Live Performance' },
]

interface Props {
  songId: number
}

export function YouTubeBriefPanel({ songId }: Props) {
  const qc = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [conceptType, setConceptType] = useState('making_of')
  const [keyMessage, setKeyMessage] = useState('')
  const [context, setContext] = useState('')

  const { data: briefs = [], isLoading } = useQuery({
    queryKey: ['youtube-briefs', songId],
    queryFn: () => listBriefsForSong(songId),
  })

  const generateMutation = useMutation({
    mutationFn: () =>
      generateBrief(songId, {
        concept_type: conceptType,
        key_message: keyMessage || undefined,
        context: context || undefined,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['youtube-briefs', songId] })
      setShowForm(false)
      setKeyMessage('')
      setContext('')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteBrief,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['youtube-briefs', songId] }),
  })

  function handleUpdated(updated: YouTubeBrief) {
    qc.setQueryData<YouTubeBrief[]>(['youtube-briefs', songId], (prev) =>
      prev ? prev.map((b) => (b.id === updated.id ? updated : b)) : [updated]
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900">YouTube Briefs</h3>
        <button
          onClick={() => setShowForm(!showForm)}
          className="text-xs bg-red-600 text-white px-3 py-1.5 rounded-lg hover:bg-red-700 transition-colors"
        >
          + Generate Brief
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-50 rounded-xl p-4 space-y-3 border border-gray-200">
          <div>
            <label className="text-xs font-medium text-gray-700 block mb-1">Video Concept</label>
            <select
              value={conceptType}
              onChange={(e) => setConceptType(e.target.value)}
              className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              {CONCEPT_TYPES.map((ct) => (
                <option key={ct.value} value={ct.value}>{ct.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-medium text-gray-700 block mb-1">Key Message (optional)</label>
            <input
              type="text"
              value={keyMessage}
              onChange={(e) => setKeyMessage(e.target.value)}
              placeholder="What's the main thing you want viewers to take away?"
              maxLength={200}
              className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-gray-700 block mb-1">Context (optional)</label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Any background info that would help (e.g., where you filmed, what gear you used)"
              rows={2}
              maxLength={300}
              className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 resize-none"
            />
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => generateMutation.mutate()}
              disabled={generateMutation.isPending}
              className="flex-1 text-sm bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors font-medium"
            >
              {generateMutation.isPending ? 'Generating…' : 'Generate with AI ✨'}
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="text-sm border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {isLoading ? (
        <p className="text-sm text-gray-400">Loading briefs…</p>
      ) : briefs.length === 0 ? (
        <p className="text-sm text-gray-400 italic">No briefs yet — generate your first one above.</p>
      ) : (
        <div className="space-y-3">
          {briefs.map((brief) => (
            <YouTubeBriefCard
              key={brief.id}
              brief={brief}
              onUpdated={handleUpdated}
              onDeleted={deleteMutation.mutate}
            />
          ))}
        </div>
      )}
    </div>
  )
}
