import { useState } from 'react'
import type { YouTubeBrief } from '../../types'
import { updateBrief } from '../../api/youtube'

const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-600',
  planned: 'bg-blue-100 text-blue-700',
  filmed: 'bg-amber-100 text-amber-700',
  published: 'bg-green-100 text-green-700',
}

const CONCEPT_LABELS: Record<string, string> = {
  making_of: 'Making Of',
  acoustic_session: 'Acoustic Session',
  production_breakdown: 'Production Breakdown',
  song_explained: 'Song Explained',
  live_performance: 'Live Performance',
}

interface Props {
  brief: YouTubeBrief
  onUpdated: (updated: YouTubeBrief) => void
  onDeleted: (id: number) => void
}

export function YouTubeBriefCard({ brief, onUpdated, onDeleted }: Props) {
  const [expanded, setExpanded] = useState(false)
  const [publishUrl, setPublishUrl] = useState('')
  const [showPublish, setShowPublish] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const nextStatus: Record<string, string> = {
    draft: 'planned',
    planned: 'filmed',
    filmed: 'published',
  }

  async function advanceStatus() {
    if (brief.status === 'filmed') {
      setShowPublish(true)
      return
    }
    const next = nextStatus[brief.status]
    if (!next) return
    setLoading(true)
    try {
      const updated = await updateBrief(brief.id, { status: next })
      onUpdated(updated)
    } finally {
      setLoading(false)
    }
  }

  async function handlePublish() {
    setError('')
    setLoading(true)
    try {
      const updated = await updateBrief(brief.id, { status: 'published', youtube_url: publishUrl })
      onUpdated(updated)
      setShowPublish(false)
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } } }
      setError(err?.response?.data?.detail ?? 'Failed to publish')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 flex flex-col gap-3">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-medium bg-red-50 text-red-700 px-2 py-0.5 rounded-full">
            {CONCEPT_LABELS[brief.concept_type] ?? brief.concept_type}
          </span>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${STATUS_COLORS[brief.status]}`}>
            {brief.status}
          </span>
        </div>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-indigo-600 hover:underline"
        >
          {expanded ? 'Collapse' : 'View Brief'}
        </button>
      </div>

      {brief.seo_title && (
        <p className="text-sm font-semibold text-gray-900 leading-snug">{brief.seo_title}</p>
      )}

      {expanded && (
        <div className="space-y-3 text-sm text-gray-700">
          {brief.hook_paragraph && (
            <div>
              <p className="text-xs font-medium text-gray-500 mb-1">Hook Paragraph</p>
              <p className="text-sm text-gray-700 leading-relaxed">{brief.hook_paragraph}</p>
            </div>
          )}
          {brief.chapters && brief.chapters.length > 0 && (
            <div>
              <p className="text-xs font-medium text-gray-500 mb-1">Chapters</p>
              <ul className="space-y-1">
                {brief.chapters.map((ch, i) => (
                  <li key={i} className="text-xs text-gray-600">
                    <span className="font-mono text-gray-400 mr-2">{ch.timestamp}</span>
                    <span className="font-medium">{ch.title}</span>
                    <span className="text-gray-400"> — {ch.what_to_cover}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {brief.video_description && (
            <div>
              <p className="text-xs font-medium text-gray-500 mb-1">Description</p>
              <p className="text-xs text-gray-600">{brief.video_description}</p>
            </div>
          )}
          {brief.tags && brief.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {brief.tags.map((tag) => (
                <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {brief.youtube_url && (
        <a
          href={brief.youtube_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-red-600 hover:underline"
        >
          Watch on YouTube →
        </a>
      )}

      {showPublish && (
        <div className="space-y-2">
          <input
            type="url"
            value={publishUrl}
            onChange={(e) => setPublishUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            className="w-full text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          {error && <p className="text-xs text-red-600">{error}</p>}
          <div className="flex gap-2">
            <button
              onClick={handlePublish}
              disabled={loading || !publishUrl}
              className="flex-1 text-sm bg-green-600 text-white py-1.5 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              Confirm Publish
            </button>
            <button
              onClick={() => setShowPublish(false)}
              className="text-sm border border-gray-300 px-3 py-1.5 rounded-lg"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {!showPublish && brief.status !== 'published' && (
        <div className="flex gap-2">
          <button
            onClick={advanceStatus}
            disabled={loading}
            className="flex-1 text-sm bg-indigo-600 text-white py-1.5 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            {brief.status === 'draft' ? 'Mark Planned' : brief.status === 'planned' ? 'Mark Filmed' : 'Publish'}
          </button>
          <button
            onClick={() => onDeleted(brief.id)}
            className="text-sm border border-red-200 text-red-500 px-3 py-1.5 rounded-lg hover:bg-red-50 transition-colors"
          >
            Delete
          </button>
        </div>
      )}
    </div>
  )
}
