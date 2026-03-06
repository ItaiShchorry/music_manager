import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getProgress } from '../../api/progress'

interface Props {
  textContent: string
  onNext: () => void
}

const BADGE_EMOJIS: Record<string, string> = {
  first_spark: '✨',
  three_day_streak: '🔥',
  week_on_fire: '🚀',
  ten_creations: '🎯',
  publisher: '📢',
  youtube_debut: '🎬',
}

export function CelebrationScreen({ textContent, onNext }: Props) {
  const [copied, setCopied] = useState(false)
  const caption = textContent
    ? `Just completed a creative challenge! ✨\n\n"${textContent.slice(0, 120)}${textContent.length > 120 ? '…' : ''}"\n\n#מוזיקה_ישראלית #songwriter #creative`
    : ''

  const { data: progress, refetch } = useQuery({
    queryKey: ['progress'],
    queryFn: getProgress,
    retry: false,
  })

  useEffect(() => {
    // Refresh progress to see new badges/level
    refetch()
  }, [refetch])

  function handleCopy() {
    navigator.clipboard.writeText(caption)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const newBadges = progress?.badges?.slice(-2) ?? []

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4">
      {/* Celebration animation */}
      <div className="text-center space-y-6 max-w-md w-full bg-white rounded-2xl p-8 shadow-2xl">
        {/* Confetti emoji burst */}
        <div className="text-6xl animate-bounce">🎉</div>

        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-gray-900">Challenge Complete!</h2>
          {progress && (
            <p className="text-sm text-gray-500">
              Level: <span className="font-semibold capitalize text-indigo-600">{progress.level}</span>
              {' · '}
              {progress.streak_current > 1 && (
                <span className="text-amber-600">🔥 {progress.streak_current}-day streak!</span>
              )}
              {progress.streak_current === 1 && <span>Keep going tomorrow for a streak!</span>}
            </p>
          )}
        </div>

        {/* New badges */}
        {newBadges.length > 0 && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 space-y-1">
            <p className="text-xs font-semibold text-amber-700">Badge{newBadges.length > 1 ? 's' : ''} Earned!</p>
            {newBadges.map((badge) => (
              <p key={badge.badge_type} className="text-sm font-medium text-gray-800">
                {BADGE_EMOJIS[badge.badge_type] ?? '🏅'}{' '}
                {badge.badge_type.replace(/_/g, ' ')}
              </p>
            ))}
          </div>
        )}

        {/* Share draft */}
        {caption && (
          <div className="text-left space-y-2">
            <p className="text-xs font-medium text-gray-500">Share your work</p>
            <div className="bg-gray-50 rounded-xl p-3 text-sm text-gray-700 whitespace-pre-wrap leading-relaxed max-h-32 overflow-y-auto">
              {caption}
            </div>
            <button
              onClick={handleCopy}
              className="w-full text-sm border border-gray-300 py-2 rounded-lg hover:bg-gray-50 transition-colors"
            >
              {copied ? 'Copied! ✓' : 'Copy Caption'}
            </button>
          </div>
        )}

        <button
          onClick={onNext}
          className="w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold py-3 rounded-xl transition-colors"
        >
          Next Challenge →
        </button>
      </div>
    </div>
  )
}
