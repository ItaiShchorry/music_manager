import { useState } from 'react'
import type { PostOpportunity } from '../../types'
import { completeChallenge } from '../../api/challenges'
import { CelebrationScreen } from './CelebrationScreen'

interface Props {
  opportunity: PostOpportunity
  onClose: () => void
  onCompleted: () => void
}

const TEXT_SIGNAL_TYPES = new Set([
  'lyric_prompt', 'catalog_gap', 'style_exploration',
  'milestone', 'playlist_add', 'inactivity', 'calendar', 'recent_release',
  'story_ready',
])

export function ChallengeMode({ opportunity: opp, onClose, onCompleted }: Props) {
  const [textContent, setTextContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [completed, setCompleted] = useState(false)

  const isTextMode = TEXT_SIGNAL_TYPES.has(opp.signal_type)
  const label = opp.category === 'creative' ? 'Submit Challenge' : 'Use This'

  async function handleSubmit() {
    if (!textContent.trim()) return
    setLoading(true)
    try {
      await completeChallenge(opp.id, {
        content_type: isTextMode ? 'text' : 'link',
        text_content: textContent,
      })
      setCompleted(true)
    } finally {
      setLoading(false)
    }
  }

  if (completed) {
    return (
      <CelebrationScreen
        textContent={textContent}
        onNext={() => { onCompleted(); onClose() }}
      />
    )
  }

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        <div className="p-6 space-y-5">
          {/* Header */}
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-medium bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full">
                {opp.signal_type.replace(/_/g, ' ')}
              </span>
              <h2 className="text-lg font-bold text-gray-900 leading-snug">{opp.hook}</h2>
              <p className="text-sm text-gray-500">{opp.why_now}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-xl flex-shrink-0"
            >
              ✕
            </button>
          </div>

          {/* Creation area */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700 block">
              {opp.category === 'creative' ? 'Write your response' : 'Add a note (optional)'}
            </label>
            <textarea
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              placeholder={
                opp.signal_type === 'lyric_prompt'
                  ? 'Write your verse here…'
                  : opp.signal_type.includes('challenge') || opp.signal_type === 'catalog_gap'
                  ? 'Describe your idea or paste your lyrics…'
                  : 'Add a note about how you used this…'
              }
              rows={8}
              className="w-full text-sm border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-amber-400 resize-none font-mono"
              dir={opp.category === 'creative' ? 'auto' : 'ltr'}
            />
            <p className="text-xs text-gray-400 text-right">{textContent.length} characters</p>
          </div>

          {/* Hashtags */}
          {opp.hashtag_suggestions && opp.hashtag_suggestions.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {opp.hashtag_suggestions.map((tag) => (
                <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-2">
            <button
              onClick={handleSubmit}
              disabled={loading || !textContent.trim()}
              className="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2.5 rounded-xl disabled:opacity-50 transition-colors"
            >
              {loading ? 'Submitting…' : `${label} ✓`}
            </button>
            <button
              onClick={onClose}
              className="border border-gray-300 text-gray-500 px-5 py-2.5 rounded-xl hover:bg-gray-50 transition-colors"
            >
              Back
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
