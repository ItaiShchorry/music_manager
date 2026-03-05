import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { createCampaign, listCampaigns } from '../api/campaigns'
import { listSongs } from '../api/songs'
import { Nav } from '../components/Nav'
import type { CampaignCreate } from '../api/campaigns'

const STATUS_COLORS: Record<string, string> = {
  planning: 'bg-gray-100 text-gray-700',
  active: 'bg-green-100 text-green-700',
  completed: 'bg-blue-100 text-blue-700',
}

const GOAL_LABELS: Record<string, string> = {
  awareness: 'Build Awareness',
  growth: 'Grow Fanbase',
  monetization: 'Monetize',
}

function NewCampaignModal({ onClose }: { onClose: () => void }) {
  const queryClient = useQueryClient()
  const { data: songs = [] } = useQuery({ queryKey: ['songs'], queryFn: listSongs })

  const [form, setForm] = useState<CampaignCreate>({
    name: '',
    release_type: 'single',
    start_date: '',
    end_date: '',
    budget_total: 200,
    primary_goal: 'awareness',
    song_ids: [],
  })

  const mutation = useMutation({
    mutationFn: () => createCampaign(form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
      onClose()
    },
  })

  const toggleSong = (id: number) =>
    setForm((f) => ({
      ...f,
      song_ids: f.song_ids?.includes(id)
        ? f.song_ids.filter((s) => s !== id)
        : [...(f.song_ids ?? []), id],
    }))

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 space-y-4">
        <h2 className="text-lg font-semibold text-gray-900">New Campaign</h2>

        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Campaign name</label>
            <input
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="e.g. Spring Single Push"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Release type</label>
              <select
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={form.release_type}
                onChange={(e) => setForm({ ...form, release_type: e.target.value as CampaignCreate['release_type'] })}
              >
                <option value="single">Single</option>
                <option value="ep">EP</option>
                <option value="album">Album</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Primary goal</label>
              <select
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={form.primary_goal}
                onChange={(e) => setForm({ ...form, primary_goal: e.target.value as CampaignCreate['primary_goal'] })}
              >
                <option value="awareness">Build Awareness</option>
                <option value="growth">Grow Fanbase</option>
                <option value="monetization">Monetize</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start date</label>
              <input
                type="date"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={form.start_date}
                onChange={(e) => setForm({ ...form, start_date: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End date</label>
              <input
                type="date"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={form.end_date}
                onChange={(e) => setForm({ ...form, end_date: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Total budget ($)</label>
            <input
              type="number"
              min={1}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={form.budget_total}
              onChange={(e) => setForm({ ...form, budget_total: Number(e.target.value) })}
            />
          </div>

          {songs.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Attach songs (optional)</label>
              <div className="space-y-1 max-h-40 overflow-y-auto border border-gray-200 rounded-lg p-2">
                {songs.map((s) => (
                  <label key={s.id} className="flex items-center gap-2 cursor-pointer text-sm text-gray-700">
                    <input
                      type="checkbox"
                      checked={form.song_ids?.includes(s.id) ?? false}
                      onChange={() => toggleSong(s.id)}
                      className="text-indigo-600"
                    />
                    {s.title}
                  </label>
                ))}
              </div>
            </div>
          )}
        </div>

        {mutation.isError && (
          <p className="text-sm text-red-600">
            {(mutation.error as any)?.response?.data?.detail ?? 'Failed to create campaign.'}
          </p>
        )}

        <div className="flex gap-3 justify-end pt-2">
          <button onClick={onClose} className="text-sm text-gray-500 hover:text-gray-700">
            Cancel
          </button>
          <button
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending || !form.name || !form.start_date || !form.end_date}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            {mutation.isPending ? 'Creating…' : 'Create Campaign'}
          </button>
        </div>
      </div>
    </div>
  )
}

export function CampaignsPage() {
  const [showNew, setShowNew] = useState(false)
  const { data: campaigns = [], isLoading } = useQuery({
    queryKey: ['campaigns'],
    queryFn: listCampaigns,
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Campaigns</h1>
            <p className="text-sm text-gray-500 mt-1">Organize your promotion efforts with budgets and tracking</p>
          </div>
          <button
            onClick={() => setShowNew(true)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            + New Campaign
          </button>
        </div>

        {isLoading && <p className="text-sm text-gray-500">Loading…</p>}

        {!isLoading && campaigns.length === 0 && (
          <div className="bg-white rounded-2xl border border-gray-200 p-12 text-center">
            <p className="text-gray-500 mb-4">No campaigns yet.</p>
            <button
              onClick={() => setShowNew(true)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
            >
              Create your first campaign
            </button>
          </div>
        )}

        <div className="space-y-4">
          {campaigns.map((c) => {
            const pct = c.budget_total > 0 ? Math.round((c.budget_spent / c.budget_total) * 100) : 0
            return (
              <Link
                key={c.id}
                to={`/campaigns/${c.id}`}
                className="block bg-white rounded-2xl border border-gray-200 p-5 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h2 className="font-semibold text-gray-900">{c.name}</h2>
                    <p className="text-xs text-gray-500 mt-0.5">
                      {c.release_type.toUpperCase()} · {c.start_date} → {c.end_date}
                      {c.primary_goal && ` · ${GOAL_LABELS[c.primary_goal]}`}
                    </p>
                  </div>
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${STATUS_COLORS[c.status]}`}>
                    {c.status}
                  </span>
                </div>

                {/* Budget bar */}
                <div className="mb-2">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>${c.budget_spent.toFixed(2)} spent</span>
                    <span>${c.budget_total.toFixed(2)} total</span>
                  </div>
                  <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${pct >= 80 ? 'bg-orange-400' : 'bg-indigo-500'}`}
                      style={{ width: `${Math.min(pct, 100)}%` }}
                    />
                  </div>
                </div>

                {c.songs.length > 0 && (
                  <p className="text-xs text-gray-400">
                    Songs: {c.songs.map((s) => s.title).join(', ')}
                  </p>
                )}
              </Link>
            )
          })}
        </div>
      </div>

      {showNew && <NewCampaignModal onClose={() => setShowNew(false)} />}
    </div>
  )
}
