import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  generateInsights,
  getHealthScore,
  listInsights,
  syncSnapshot,
  updateInsight,
  type SnapshotCreate,
} from '../api/dashboard'
import { listCampaigns } from '../api/campaigns'
import { Nav } from '../components/Nav'
import type { Insight } from '../types'

// ---------------------------------------------------------------------------
// Health score helpers
// ---------------------------------------------------------------------------

const SCORE_COLOR: Record<string, string> = {
  Excellent: 'text-green-600',
  Healthy: 'text-yellow-600',
  'Needs Work': 'text-orange-500',
  Critical: 'text-red-600',
}

const SCORE_BG: Record<string, string> = {
  Excellent: 'bg-green-50 border-green-200',
  Healthy: 'bg-yellow-50 border-yellow-200',
  'Needs Work': 'bg-orange-50 border-orange-200',
  Critical: 'bg-red-50 border-red-200',
}

const INSIGHT_ICON: Record<string, string> = {
  momentum: '🎉',
  warning: '⚠️',
  opportunity: '🔥',
  tip: '💡',
  milestone: '🏆',
}

const PRIORITY_BADGE: Record<string, string> = {
  high: 'bg-red-100 text-red-700',
  medium: 'bg-yellow-100 text-yellow-700',
  low: 'bg-gray-100 text-gray-600',
}

// ---------------------------------------------------------------------------
// Trend badge
// ---------------------------------------------------------------------------

function TrendBadge({ value }: { value: number | null }) {
  if (value === null) return <span className="text-xs text-gray-400">—</span>
  const positive = value >= 0
  return (
    <span className={`text-xs font-medium ${positive ? 'text-green-600' : 'text-red-600'}`}>
      {positive ? '↑' : '↓'} {Math.abs(value).toFixed(1)}%
    </span>
  )
}

// ---------------------------------------------------------------------------
// Sync Modal
// ---------------------------------------------------------------------------

function SyncModal({ onClose }: { onClose: () => void }) {
  const queryClient = useQueryClient()
  const [form, setForm] = useState<SnapshotCreate>({
    total_streams: 0,
    total_monthly_listeners: 0,
    total_followers: 0,
    total_saves: 0,
    total_playlist_adds: 0,
    streams_vs_last_week_pct: null,
    listeners_vs_last_week_pct: null,
    followers_vs_last_week_pct: null,
  })

  const mutation = useMutation({
    mutationFn: () => syncSnapshot(form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['healthScore'] })
      onClose()
    },
  })

  const field = (
    label: string,
    key: keyof SnapshotCreate,
    opts?: { step?: number; min?: number; placeholder?: string }
  ) => (
    <div>
      <label className="block text-xs font-medium text-gray-600 mb-1">{label}</label>
      <input
        type="number"
        step={opts?.step ?? 1}
        min={opts?.min ?? 0}
        placeholder={opts?.placeholder}
        className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        value={form[key] ?? ''}
        onChange={(e) =>
          setForm({ ...form, [key]: e.target.value === '' ? null : Number(e.target.value) })
        }
      />
    </div>
  )

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 space-y-4">
        <h2 className="text-lg font-semibold text-gray-900">Sync Spotify Data</h2>
        <p className="text-sm text-gray-500">
          Copy these numbers from your Spotify for Artists dashboard.
        </p>

        <div className="grid grid-cols-2 gap-3">
          {field('Total Streams (28 days)', 'total_streams')}
          {field('Monthly Listeners', 'total_monthly_listeners')}
          {field('Followers', 'total_followers')}
          {field('Saves (28 days)', 'total_saves')}
          {field('Playlist Adds (this week)', 'total_playlist_adds')}
        </div>

        <p className="text-xs font-medium text-gray-500 mt-1">
          Week-over-week trends (optional — enter as %, e.g. 25 for +25%, -10 for -10%)
        </p>
        <div className="grid grid-cols-3 gap-3">
          {field('Streams %', 'streams_vs_last_week_pct', { step: 0.1, placeholder: 'e.g. 25' })}
          {field('Listeners %', 'listeners_vs_last_week_pct', { step: 0.1, placeholder: 'e.g. 10' })}
          {field('Followers %', 'followers_vs_last_week_pct', { step: 0.1, placeholder: 'e.g. 5' })}
        </div>

        {mutation.isError && (
          <p className="text-sm text-red-600">Failed to save data. Please try again.</p>
        )}

        <div className="flex gap-3 justify-end pt-2">
          <button onClick={onClose} className="text-sm text-gray-500 hover:text-gray-700">
            Cancel
          </button>
          <button
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            {mutation.isPending ? 'Saving…' : 'Save Data'}
          </button>
        </div>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Insight card
// ---------------------------------------------------------------------------

function InsightCard({ insight }: { insight: Insight }) {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (status: 'dismissed' | 'actioned') => updateInsight(insight.id, status),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['insights'] }),
  })

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-2">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-lg">{INSIGHT_ICON[insight.insight_type] ?? '📌'}</span>
          <span className="text-sm font-semibold text-gray-900">{insight.title}</span>
        </div>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${PRIORITY_BADGE[insight.priority]}`}>
          {insight.priority}
        </span>
      </div>
      <p className="text-sm text-gray-600">{insight.description}</p>
      {insight.action_text && (
        <p className="text-xs text-indigo-700 font-medium">→ {insight.action_text}</p>
      )}
      <div className="flex gap-2 pt-1">
        <button
          onClick={() => mutation.mutate('actioned')}
          disabled={mutation.isPending}
          className="text-xs bg-indigo-600 text-white px-2 py-1 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
        >
          Done
        </button>
        <button
          onClick={() => mutation.mutate('dismissed')}
          disabled={mutation.isPending}
          className="text-xs text-gray-500 hover:text-gray-700 disabled:opacity-50"
        >
          Dismiss
        </button>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export function DashboardPage() {
  const queryClient = useQueryClient()
  const [showSync, setShowSync] = useState(false)

  const { data: health, isLoading: healthLoading, isError: healthError } = useQuery({
    queryKey: ['healthScore'],
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

  const genMutation = useMutation({
    mutationFn: generateInsights,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['insights'] }),
  })

  const activeCampaigns = campaigns.filter((c) => c.status === 'active')

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />
      <div className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-sm text-gray-500 mt-1">Your music health at a glance</p>
          </div>
          <button
            onClick={() => setShowSync(true)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            Sync Spotify Data
          </button>
        </div>

        {/* Health Score */}
        {healthLoading && (
          <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center">
            <p className="text-sm text-gray-500">Loading…</p>
          </div>
        )}
        {!healthLoading && (healthError || !health) && (
          <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center">
            <p className="text-gray-500 mb-3">No data yet.</p>
            <p className="text-sm text-gray-400 mb-4">
              Sync your Spotify data to see your health score and insights.
            </p>
            <button
              onClick={() => setShowSync(true)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
            >
              Sync Now
            </button>
          </div>
        )}
        {health && (
          <div className={`rounded-2xl border p-6 ${SCORE_BG[health.label] ?? 'bg-white border-gray-200'}`}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-gray-700">Music Health Score</h2>
              <span className="text-xs text-gray-400">{health.metrics.streams_vs_last_week_pct !== null ? 'Updated today' : ''}</span>
            </div>
            <div className="flex items-baseline gap-3 mb-1">
              <span className={`text-5xl font-bold ${SCORE_COLOR[health.label] ?? 'text-gray-900'}`}>
                {health.health_score}
              </span>
              <span className={`text-lg font-semibold ${SCORE_COLOR[health.label] ?? 'text-gray-700'}`}>
                {health.label}
              </span>
            </div>
            <div className="w-full bg-white/60 rounded-full h-2 mt-3 mb-4 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${
                  health.health_score >= 85 ? 'bg-green-500' :
                  health.health_score >= 70 ? 'bg-yellow-400' :
                  health.health_score >= 50 ? 'bg-orange-400' : 'bg-red-500'
                }`}
                style={{ width: `${health.health_score}%` }}
              />
            </div>

            {/* Metrics grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {[
                { label: 'Streams', value: health.metrics.total_streams.toLocaleString(), trend: health.metrics.streams_vs_last_week_pct },
                { label: 'Monthly Listeners', value: health.metrics.total_monthly_listeners.toLocaleString(), trend: health.metrics.listeners_vs_last_week_pct },
                { label: 'Followers', value: health.metrics.total_followers.toLocaleString(), trend: health.metrics.followers_vs_last_week_pct },
                { label: 'Save Rate', value: health.metrics.save_rate !== null ? `${health.metrics.save_rate.toFixed(1)}%` : '—', trend: null },
                { label: 'Follower Conv.', value: health.metrics.follower_conversion_rate !== null ? `${health.metrics.follower_conversion_rate.toFixed(1)}%` : '—', trend: null },
                { label: 'Playlist Adds', value: String(health.metrics.total_playlist_adds), trend: null },
              ].map(({ label, value, trend }) => (
                <div key={label} className="bg-white/70 rounded-xl p-3">
                  <p className="text-xs text-gray-500 mb-0.5">{label}</p>
                  <p className="text-lg font-semibold text-gray-900">{value}</p>
                  <TrendBadge value={trend} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Active Campaigns */}
        {activeCampaigns.length > 0 && (
          <div className="bg-white rounded-2xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Active Campaigns</h3>
            <div className="space-y-3">
              {activeCampaigns.map((c) => {
                const pct = c.budget_total > 0 ? Math.round((c.budget_spent / c.budget_total) * 100) : 0
                return (
                  <Link
                    key={c.id}
                    to={`/campaigns/${c.id}`}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
                  >
                    <div>
                      <p className="text-sm font-medium text-gray-900">{c.name}</p>
                      <p className="text-xs text-gray-500">${c.budget_spent.toFixed(0)} / ${c.budget_total.toFixed(0)} spent</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-500">{pct}% used</p>
                      <div className="w-24 h-1.5 bg-gray-200 rounded-full mt-1">
                        <div
                          className={`h-full rounded-full ${pct >= 80 ? 'bg-orange-400' : 'bg-indigo-500'}`}
                          style={{ width: `${Math.min(pct, 100)}%` }}
                        />
                      </div>
                    </div>
                  </Link>
                )
              })}
            </div>
          </div>
        )}

        {/* Insights */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-700">
              Insights {insights.length > 0 && <span className="ml-1 text-xs bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded-full">{insights.length}</span>}
            </h3>
            <button
              onClick={() => genMutation.mutate()}
              disabled={genMutation.isPending || !health}
              className="text-xs bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              title={!health ? 'Sync Spotify data first' : undefined}
            >
              {genMutation.isPending ? 'Generating…' : 'Generate Insights'}
            </button>
          </div>

          {insights.length === 0 ? (
            <p className="text-sm text-gray-400">
              {health ? 'Click "Generate Insights" to get AI-powered recommendations.' : 'Sync Spotify data first, then generate insights.'}
            </p>
          ) : (
            <div className="space-y-3">
              {insights.map((insight) => (
                <InsightCard key={insight.id} insight={insight} />
              ))}
            </div>
          )}
        </div>

        {/* Quick Links */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Quick Links</h3>
          <div className="flex flex-wrap gap-2">
            <Link to="/songs/new" className="text-sm bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700">
              + Add Song
            </Link>
            <Link to="/campaigns" className="text-sm bg-white border border-indigo-300 text-indigo-700 px-3 py-1.5 rounded-lg hover:bg-indigo-50">
              Campaigns
            </Link>
            <Link to="/discover" className="text-sm bg-white border border-indigo-300 text-indigo-700 px-3 py-1.5 rounded-lg hover:bg-indigo-50">
              Find Playlists
            </Link>
            <Link to="/songs" className="text-sm bg-white border border-gray-300 text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-50">
              My Songs
            </Link>
          </div>
        </div>
      </div>

      {showSync && <SyncModal onClose={() => setShowSync(false)} />}
    </div>
  )
}
