import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Nav } from '../components/Nav'
import { OpportunityCard } from '../components/opportunities/OpportunityCard'
import { ChallengeMode } from '../components/challenges/ChallengeMode'
import { ProgressWidget } from '../components/progress/ProgressWidget'
import { YouTubeQueueWidget } from '../components/youtube/YouTubeQueueWidget'
import { generateOpportunities, listOpportunities, updateOpportunity } from '../api/opportunities'
import { getHealthScore, listInsights, updateInsight } from '../api/dashboard'
import { listCampaigns } from '../api/campaigns'
import type { PostOpportunity } from '../types'

const INSIGHT_ICON: Record<string, string> = {
  momentum: '🎉',
  warning: '⚠️',
  opportunity: '🔥',
  tip: '💡',
  milestone: '🏆',
}

const SCORE_COLOR: Record<string, string> = {
  Excellent: 'text-green-600',
  Healthy: 'text-yellow-600',
  'Needs Work': 'text-orange-500',
  Critical: 'text-red-600',
}

export function ManagerPage() {
  const qc = useQueryClient()
  const [activeChallenge, setActiveChallenge] = useState<PostOpportunity | null>(null)

  // Data queries
  const { data: opportunities = [] } = useQuery({
    queryKey: ['opportunities'],
    queryFn: listOpportunities,
  })
  const { data: healthData } = useQuery({
    queryKey: ['health-score'],
    queryFn: getHealthScore,
    retry: false,
  })
  const { data: insights = [] } = useQuery({
    queryKey: ['insights'],
    queryFn: listInsights,
  })
  const { data: campaigns = [] } = useQuery({
    queryKey: ['campaigns'],
    queryFn: listCampaigns,
  })

  // Mutations
  const generateMutation = useMutation({
    mutationFn: () => generateOpportunities(),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['opportunities'] }),
  })

  const updateOppMutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: 'used' | 'dismissed' | 'remind_later' }) => updateOpportunity(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['opportunities'] })
      qc.invalidateQueries({ queryKey: ['progress'] })
    },
  })

  const dismissInsightMutation = useMutation({
    mutationFn: (id: number) => updateInsight(id, 'dismissed'),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['insights'] }),
  })

  // Split opportunities by category
  const creative = opportunities.filter((o) => o.category === 'creative' || o.category === 'youtube').slice(0, 3)
  const promotion = opportunities.filter((o) => o.category === 'promotion')
  const activeInsights = insights.filter((i) => i.status === 'active').slice(0, 3)
  const activeCampaigns = campaigns.filter((c) => c.status === 'active').slice(0, 3)

  function handleAccept(opp: PostOpportunity) {
    setActiveChallenge(opp)
  }

  function handleDismiss(id: number) {
    updateOppMutation.mutate({ id, status: 'dismissed' as const })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-10">

        {/* ------------------------------------------------------------------ */}
        {/* CREATE */}
        {/* ------------------------------------------------------------------ */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">CREATE</h2>
              <p className="text-sm text-gray-500">Your creative challenges for today</p>
            </div>
            <button
              onClick={() => generateMutation.mutate()}
              disabled={generateMutation.isPending}
              className="text-sm bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-xl font-medium disabled:opacity-50 transition-colors"
            >
              {generateMutation.isPending ? 'Generating…' : 'Generate Ideas ✨'}
            </button>
          </div>

          {creative.length === 0 ? (
            <div className="bg-white border border-dashed border-amber-300 rounded-xl p-6 text-center space-y-2">
              <p className="text-2xl">🎸</p>
              <p className="text-sm font-medium text-gray-700">No creative challenges yet</p>
              <p className="text-xs text-gray-400">Click "Generate Ideas ✨" to get your personalized challenges</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {creative.map((opp) => (
                <OpportunityCard
                  key={opp.id}
                  opportunity={opp}
                  onUse={() => handleAccept(opp)}
                  onDismiss={handleDismiss}
                  loading={updateOppMutation.isPending}
                />
              ))}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <YouTubeQueueWidget />
            <ProgressWidget />
          </div>
        </section>

        {/* ------------------------------------------------------------------ */}
        {/* SHARE */}
        {/* ------------------------------------------------------------------ */}
        <section className="space-y-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">SHARE</h2>
            <p className="text-sm text-gray-500">Promotional opportunities & active campaigns</p>
          </div>

          {promotion.length === 0 ? (
            <p className="text-sm text-gray-400 italic">No promotional ideas — generate new ideas above.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {promotion.slice(0, 4).map((opp) => (
                <OpportunityCard
                  key={opp.id}
                  opportunity={opp}
                  onUse={(id) => updateOppMutation.mutate({ id, status: 'used' as const })}
                  onDismiss={handleDismiss}
                  loading={updateOppMutation.isPending}
                />
              ))}
            </div>
          )}

          {activeCampaigns.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-gray-700">Active Campaigns</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {activeCampaigns.map((c) => (
                  <Link
                    key={c.id}
                    to={`/campaigns/${c.id}`}
                    className="bg-white border border-gray-200 rounded-xl p-3 hover:border-indigo-300 transition-colors"
                  >
                    <p className="text-sm font-medium text-gray-900">{c.name}</p>
                    <p className="text-xs text-gray-400 capitalize">{c.release_type} · {c.status}</p>
                    <div className="mt-2 w-full bg-gray-100 rounded-full h-1">
                      <div
                        className="bg-indigo-500 h-1 rounded-full"
                        style={{ width: `${c.budget_total > 0 ? Math.min((c.budget_spent / c.budget_total) * 100, 100) : 0}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-400 mt-1">
                      ${c.budget_spent} / ${c.budget_total} spent
                    </p>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* ------------------------------------------------------------------ */}
        {/* TRACK */}
        {/* ------------------------------------------------------------------ */}
        <section className="space-y-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">TRACK</h2>
            <p className="text-sm text-gray-500">Health score, insights & performance</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Health Score */}
            {healthData ? (
              <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-2">
                <p className="text-xs font-medium text-gray-500">Artist Health Score</p>
                <div className="flex items-baseline gap-2">
                  <span className={`text-4xl font-bold ${SCORE_COLOR[healthData.label] ?? 'text-gray-700'}`}>
                    {healthData.health_score}
                  </span>
                  <span className="text-sm text-gray-500">/ 100 — {healthData.label}</span>
                </div>
                <p className="text-xs text-gray-400">as of {healthData.snapshot_date}</p>
                <Link to="/dashboard" className="text-xs text-indigo-600 hover:underline">View full dashboard →</Link>
              </div>
            ) : (
              <div className="bg-white border border-dashed border-gray-200 rounded-xl p-4 text-center">
                <p className="text-sm text-gray-400">No stats synced yet</p>
                <Link to="/dashboard" className="text-xs text-indigo-600 hover:underline">Go to Dashboard →</Link>
              </div>
            )}

            {/* Quick stats */}
            <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
              <p className="text-xs font-medium text-gray-500">Quick Links</p>
              <div className="space-y-2">
                <Link to="/songs" className="flex items-center justify-between text-sm text-gray-700 hover:text-indigo-600 transition-colors">
                  <span>My Songs</span>
                  <span className="text-gray-400">→</span>
                </Link>
                <Link to="/discover" className="flex items-center justify-between text-sm text-gray-700 hover:text-indigo-600 transition-colors">
                  <span>Discover Playlists</span>
                  <span className="text-gray-400">→</span>
                </Link>
                <Link to="/campaigns" className="flex items-center justify-between text-sm text-gray-700 hover:text-indigo-600 transition-colors">
                  <span>Campaigns</span>
                  <span className="text-gray-400">→</span>
                </Link>
                <Link to="/dashboard" className="flex items-center justify-between text-sm text-gray-700 hover:text-indigo-600 transition-colors">
                  <span>Full Dashboard</span>
                  <span className="text-gray-400">→</span>
                </Link>
              </div>
            </div>
          </div>

          {/* AI Insights */}
          {activeInsights.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-gray-700">AI Insights</h3>
              {activeInsights.map((insight) => (
                <div key={insight.id} className="bg-white border border-gray-200 rounded-xl p-3 flex gap-3">
                  <span className="text-lg flex-shrink-0">{INSIGHT_ICON[insight.insight_type] ?? '💡'}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{insight.title}</p>
                    <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">{insight.description}</p>
                  </div>
                  <button
                    onClick={() => dismissInsightMutation.mutate(insight.id)}
                    className="text-gray-300 hover:text-gray-500 flex-shrink-0 text-sm"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      {/* Challenge mode overlay */}
      {activeChallenge && (
        <ChallengeMode
          opportunity={activeChallenge}
          onClose={() => setActiveChallenge(null)}
          onCompleted={() => {
            qc.invalidateQueries({ queryKey: ['opportunities'] })
            qc.invalidateQueries({ queryKey: ['progress'] })
          }}
        />
      )}
    </div>
  )
}
