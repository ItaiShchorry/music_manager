import type { PostOpportunity } from '../../types'

const PLATFORM_LABELS: Record<string, string> = {
  instagram: 'Instagram',
  facebook: 'Facebook',
  tiktok: 'TikTok',
  youtube: 'YouTube',
  all: 'All platforms',
}

const SIGNAL_COLORS: Record<string, string> = {
  // promotion signals
  milestone: 'bg-yellow-100 text-yellow-800',
  playlist_add: 'bg-green-100 text-green-800',
  inactivity: 'bg-orange-100 text-orange-800',
  recent_release: 'bg-blue-100 text-blue-800',
  calendar: 'bg-purple-100 text-purple-800',
  trend: 'bg-pink-100 text-pink-800',
  // creative signals
  lyric_prompt: 'bg-amber-100 text-amber-800',
  catalog_gap: 'bg-amber-100 text-amber-800',
  song_experiment: 'bg-amber-100 text-amber-800',
  style_exploration: 'bg-amber-100 text-amber-800',
  instrumental_challenge: 'bg-amber-100 text-amber-800',
  cover_idea: 'bg-amber-100 text-amber-800',
  // youtube signals
  story_ready: 'bg-red-100 text-red-700',
  no_video: 'bg-red-100 text-red-700',
  brief_filmed_unpublished: 'bg-red-100 text-red-700',
  youtube_milestone: 'bg-red-100 text-red-700',
}

const CATEGORY_STYLES: Record<string, { border: string; button: string; buttonLabel: string }> = {
  creative: {
    border: 'border-amber-200',
    button: 'bg-amber-500 hover:bg-amber-600 text-white',
    buttonLabel: 'Accept Challenge',
  },
  youtube: {
    border: 'border-red-200',
    button: 'bg-red-600 hover:bg-red-700 text-white',
    buttonLabel: 'Plan Video',
  },
  promotion: {
    border: 'border-gray-200',
    button: 'bg-indigo-600 hover:bg-indigo-700 text-white',
    buttonLabel: 'Use This',
  },
}

interface Props {
  opportunity: PostOpportunity
  onUse: (id: number) => void
  onDismiss: (id: number) => void
  loading?: boolean
}

export function OpportunityCard({ opportunity: opp, onUse, onDismiss, loading }: Props) {
  const signalColor = SIGNAL_COLORS[opp.signal_type] ?? 'bg-gray-100 text-gray-600'
  const category = opp.category ?? 'promotion'
  const catStyle = CATEGORY_STYLES[category] ?? CATEGORY_STYLES.promotion

  return (
    <div className={`bg-white rounded-xl border ${catStyle.border} p-4 flex flex-col gap-3`}>
      {/* Header row */}
      <div className="flex items-start justify-between gap-3">
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${signalColor}`}>
          {opp.signal_type.replace(/_/g, ' ')}
        </span>
        {opp.suggested_platform && (
          <span className="text-xs text-gray-400">
            {PLATFORM_LABELS[opp.suggested_platform] ?? opp.suggested_platform}
          </span>
        )}
      </div>

      {/* Hook */}
      <p className="text-sm font-medium text-gray-900 leading-snug">{opp.hook}</p>

      {/* Why now */}
      <p className="text-xs text-gray-500">{opp.why_now}</p>

      {/* Hashtags */}
      {opp.hashtag_suggestions && opp.hashtag_suggestions.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {opp.hashtag_suggestions.map((tag) => (
            <span key={tag} className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full">
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Timing note */}
      {opp.timing_note && (
        <p className="text-xs text-amber-700 bg-amber-50 px-2 py-1 rounded-lg">
          ⏰ {opp.timing_note}
        </p>
      )}

      {/* Actions */}
      <div className="flex gap-2 pt-1">
        <button
          onClick={() => onUse(opp.id)}
          disabled={loading}
          className={`flex-1 text-sm py-1.5 rounded-lg disabled:opacity-50 transition-colors font-medium ${catStyle.button}`}
        >
          {catStyle.buttonLabel}
        </button>
        <button
          onClick={() => onDismiss(opp.id)}
          disabled={loading}
          className="text-sm border border-gray-300 text-gray-500 px-3 py-1.5 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
        >
          Dismiss
        </button>
      </div>
    </div>
  )
}
