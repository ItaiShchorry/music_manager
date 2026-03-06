import { useQuery } from '@tanstack/react-query'
import { getProgress } from '../../api/progress'

const LEVEL_COLORS: Record<string, string> = {
  newcomer: 'bg-gray-100 text-gray-600',
  emerging: 'bg-blue-100 text-blue-700',
  pro: 'bg-indigo-100 text-indigo-700',
  expert: 'bg-amber-100 text-amber-700',
}

const LEVEL_NEXT: Record<string, { label: string; at: number }> = {
  newcomer: { label: 'Emerging', at: 5 },
  emerging: { label: 'Pro', at: 15 },
  pro: { label: 'Expert', at: 30 },
  expert: { label: 'Max Level', at: 30 },
}

const BADGE_EMOJIS: Record<string, string> = {
  first_spark: '✨',
  three_day_streak: '🔥',
  week_on_fire: '🚀',
  ten_creations: '🎯',
  publisher: '📢',
  youtube_debut: '🎬',
}

export function ProgressWidget() {
  const { data: progress, isLoading } = useQuery({
    queryKey: ['progress'],
    queryFn: getProgress,
    retry: false,
  })

  if (isLoading) {
    return <div className="h-20 bg-gray-100 rounded-xl animate-pulse" />
  }

  if (!progress) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-4 text-center">
        <p className="text-sm text-gray-400">Complete your first challenge to start tracking progress!</p>
      </div>
    )
  }

  const levelInfo = LEVEL_NEXT[progress.level] ?? LEVEL_NEXT.newcomer
  const progressToNext =
    progress.level !== 'expert'
      ? Math.min((progress.total_completed / levelInfo.at) * 100, 100)
      : 100

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full capitalize ${LEVEL_COLORS[progress.level]}`}>
          {progress.level}
        </span>
        {progress.streak_current > 0 && (
          <span className="text-sm font-medium text-amber-600">
            🔥 {progress.streak_current}-day streak
          </span>
        )}
      </div>

      {/* Progress bar */}
      {progress.level !== 'expert' && (
        <div className="space-y-1">
          <div className="w-full bg-gray-100 rounded-full h-1.5">
            <div
              className="bg-indigo-500 h-1.5 rounded-full transition-all duration-500"
              style={{ width: `${progressToNext}%` }}
            />
          </div>
          <p className="text-xs text-gray-400">
            {progress.total_completed}/{levelInfo.at} challenges → {levelInfo.label}
          </p>
        </div>
      )}

      {/* Recent badges */}
      {progress.badges.length > 0 && (
        <div className="flex gap-2 flex-wrap">
          {progress.badges.slice(-5).map((badge) => (
            <span
              key={badge.badge_type}
              title={badge.badge_type.replace(/_/g, ' ')}
              className="text-lg"
            >
              {BADGE_EMOJIS[badge.badge_type] ?? '🏅'}
            </span>
          ))}
        </div>
      )}

      <p className="text-xs text-gray-400">{progress.total_completed} total challenges completed</p>
    </div>
  )
}
