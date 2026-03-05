import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import {
  addSubmission,
  createSHCampaign,
  listSHCampaignsForSong,
  listSubmissions,
  updateSubmission,
  type SHCampaignCreate,
  type SubmissionCreate,
  type SubmissionUpdate,
} from '../api/submithub'
import { getSong } from '../api/songs'
import { Nav } from '../components/Nav'
import type { SubmitHubCampaign, SubmitHubSubmission } from '../types'

const STATUS_COLORS: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-800',
  approved: 'bg-green-100 text-green-800',
  declined: 'bg-red-100 text-red-800',
}

// ---------------------------------------------------------------------------
// New Campaign Form
// ---------------------------------------------------------------------------

function NewCampaignForm({ songId, onClose }: { songId: number; onClose: () => void }) {
  const queryClient = useQueryClient()
  const [form, setForm] = useState<Omit<SHCampaignCreate, 'song_id'>>({
    budget_allocated: undefined,
    curator_count: undefined,
    notes: '',
  })

  const mutation = useMutation({
    mutationFn: () => createSHCampaign({ song_id: songId, ...form }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sh-campaigns', songId] })
      onClose()
    },
  })

  return (
    <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 space-y-3">
      <h4 className="text-sm font-semibold text-indigo-900">New SubmitHub Campaign</h4>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Budget ($)</label>
          <input
            type="number"
            min={0}
            step={3}
            placeholder="e.g. 36"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.budget_allocated ?? ''}
            onChange={(e) =>
              setForm({ ...form, budget_allocated: e.target.value ? Number(e.target.value) : undefined })
            }
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Target Curator Count</label>
          <input
            type="number"
            min={1}
            placeholder="e.g. 12"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.curator_count ?? ''}
            onChange={(e) =>
              setForm({ ...form, curator_count: e.target.value ? Number(e.target.value) : undefined })
            }
          />
        </div>
      </div>
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Notes (optional)</label>
        <input
          className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="e.g. Focus on indie pop curators"
          value={form.notes ?? ''}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
        />
      </div>
      <div className="flex gap-2 justify-end">
        <button onClick={onClose} className="text-sm text-gray-500 hover:text-gray-700">
          Cancel
        </button>
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending}
          className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {mutation.isPending ? 'Creating…' : 'Create Campaign'}
        </button>
      </div>
      {mutation.isError && <p className="text-xs text-red-600">Failed to create campaign.</p>}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Add Submission Form
// ---------------------------------------------------------------------------

function AddSubmissionForm({
  shCampaignId,
  onClose,
}: {
  shCampaignId: number
  onClose: () => void
}) {
  const queryClient = useQueryClient()
  const [form, setForm] = useState<SubmissionCreate>({
    curator_name: '',
    cost: 3,
    submission_date: new Date().toISOString().slice(0, 10),
  })
  const [genreInput, setGenreInput] = useState('')

  const mutation = useMutation({
    mutationFn: () =>
      addSubmission(shCampaignId, {
        ...form,
        curator_genre_focus: genreInput
          ? genreInput.split(',').map((s) => s.trim()).filter(Boolean)
          : undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sh-submissions', shCampaignId] })
      onClose()
    },
  })

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 space-y-3 mt-3">
      <h5 className="text-sm font-semibold text-gray-700">Add Curator Submission</h5>
      <div className="grid grid-cols-2 gap-3">
        <div className="col-span-2">
          <label className="block text-xs font-medium text-gray-600 mb-1">Curator Name *</label>
          <input
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="e.g. IndieVibesPlaylist"
            value={form.curator_name}
            onChange={(e) => setForm({ ...form, curator_name: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Cost ($)</label>
          <input
            type="number"
            min={0}
            step={1}
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.cost}
            onChange={(e) => setForm({ ...form, cost: Number(e.target.value) })}
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Approval Rate (%)</label>
          <input
            type="number"
            min={0}
            max={100}
            placeholder="e.g. 20"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.curator_approval_rate ?? ''}
            onChange={(e) =>
              setForm({
                ...form,
                curator_approval_rate: e.target.value ? Number(e.target.value) : undefined,
              })
            }
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Submission Date</label>
          <input
            type="date"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.submission_date ?? ''}
            onChange={(e) => setForm({ ...form, submission_date: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Genre Focus</label>
          <input
            placeholder="indie, pop (comma-separated)"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={genreInput}
            onChange={(e) => setGenreInput(e.target.value)}
          />
        </div>
      </div>
      <div className="flex gap-2 justify-end">
        <button onClick={onClose} className="text-sm text-gray-500 hover:text-gray-700">
          Cancel
        </button>
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending || !form.curator_name.trim()}
          className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {mutation.isPending ? 'Adding…' : 'Add Submission'}
        </button>
      </div>
      {mutation.isError && <p className="text-xs text-red-600">Failed to add submission.</p>}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Outcome form — shown inline for pending submissions
// ---------------------------------------------------------------------------

function OutcomeForm({
  sub,
  onClose,
}: {
  sub: SubmitHubSubmission
  onClose: () => void
}) {
  const queryClient = useQueryClient()
  const [outcome, setOutcome] = useState<SubmissionUpdate>({})

  const mutation = useMutation({
    mutationFn: () => updateSubmission(sub.id, outcome),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sh-submissions', sub.submithub_campaign_id] })
      onClose()
    },
  })

  return (
    <tr>
      <td colSpan={6} className="pb-3 pt-1 px-0">
        <div className="bg-gray-50 rounded-lg p-3 space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Outcome</label>
              <select
                className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={outcome.response_status ?? ''}
                onChange={(e) =>
                  setOutcome({
                    ...outcome,
                    response_status: e.target.value as 'approved' | 'declined',
                    playlist_added: undefined,
                    playlist_url: undefined,
                    curator_feedback: undefined,
                  })
                }
              >
                <option value="">— select —</option>
                <option value="approved">Approved</option>
                <option value="declined">Declined</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Response Date</label>
              <input
                type="date"
                className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={outcome.response_date ?? ''}
                onChange={(e) => setOutcome({ ...outcome, response_date: e.target.value })}
              />
            </div>
          </div>

          {outcome.response_status === 'approved' && (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id={`pl-${sub.id}`}
                  checked={outcome.playlist_added ?? false}
                  onChange={(e) =>
                    setOutcome({ ...outcome, playlist_added: e.target.checked, playlist_url: undefined })
                  }
                  className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor={`pl-${sub.id}`} className="text-xs text-gray-700">
                  Added to a playlist
                </label>
              </div>
              {outcome.playlist_added && (
                <input
                  placeholder="Playlist URL (optional)"
                  className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  value={outcome.playlist_url ?? ''}
                  onChange={(e) => setOutcome({ ...outcome, playlist_url: e.target.value })}
                />
              )}
            </div>
          )}

          {outcome.response_status === 'declined' && (
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Curator Feedback (optional)
              </label>
              <input
                placeholder="e.g. Doesn't fit our current playlist direction"
                className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={outcome.curator_feedback ?? ''}
                onChange={(e) => setOutcome({ ...outcome, curator_feedback: e.target.value })}
              />
            </div>
          )}

          <div className="flex gap-2 justify-end">
            <button onClick={onClose} className="text-sm text-gray-500 hover:text-gray-700">
              Cancel
            </button>
            <button
              onClick={() => mutation.mutate()}
              disabled={!outcome.response_status || mutation.isPending}
              className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {mutation.isPending ? 'Saving…' : 'Save Outcome'}
            </button>
          </div>
        </div>
      </td>
    </tr>
  )
}

// ---------------------------------------------------------------------------
// Submission row
// ---------------------------------------------------------------------------

function SubmissionRow({ sub }: { sub: SubmitHubSubmission }) {
  const [showOutcome, setShowOutcome] = useState(false)

  return (
    <>
      <tr className="border-t border-gray-100">
        <td className="py-2 pr-3 text-sm text-gray-800">{sub.curator_name}</td>
        <td className="py-2 pr-3 text-xs text-gray-500">
          {sub.curator_genre_focus?.join(', ') ?? '—'}
        </td>
        <td className="py-2 pr-3 text-xs text-gray-500">
          {sub.curator_approval_rate != null ? `${sub.curator_approval_rate}%` : '—'}
        </td>
        <td className="py-2 pr-3 text-xs text-gray-500">${sub.cost.toFixed(0)}</td>
        <td className="py-2 pr-3">
          <span
            className={`text-xs font-medium px-2 py-0.5 rounded-full ${STATUS_COLORS[sub.response_status]}`}
          >
            {sub.response_status}
          </span>
        </td>
        <td className="py-2 text-right">
          {sub.response_status === 'pending' && (
            <button
              onClick={() => setShowOutcome((v) => !v)}
              className="text-xs text-indigo-600 hover:underline"
            >
              {showOutcome ? 'Cancel' : 'Record outcome'}
            </button>
          )}
          {sub.playlist_added && sub.playlist_url && (
            <a
              href={sub.playlist_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-green-600 hover:underline"
            >
              Playlist ↗
            </a>
          )}
          {sub.playlist_added && !sub.playlist_url && (
            <span className="text-xs text-green-600">In playlist</span>
          )}
        </td>
      </tr>
      {showOutcome && <OutcomeForm sub={sub} onClose={() => setShowOutcome(false)} />}
    </>
  )
}

// ---------------------------------------------------------------------------
// Campaign card — collapsible
// ---------------------------------------------------------------------------

function CampaignCard({ campaign }: { campaign: SubmitHubCampaign }) {
  const [expanded, setExpanded] = useState(false)
  const [showAddSub, setShowAddSub] = useState(false)

  const { data: submissions = [], isLoading } = useQuery({
    queryKey: ['sh-submissions', campaign.id],
    queryFn: () => listSubmissions(campaign.id),
    enabled: expanded,
  })

  const approved = submissions.filter((s) => s.response_status === 'approved').length
  const declined = submissions.filter((s) => s.response_status === 'declined').length
  const pending = submissions.filter((s) => s.response_status === 'pending').length
  const totalCost = submissions.reduce((sum, s) => sum + s.cost, 0)

  // Progress: how many submissions logged vs. target
  const targetCount = campaign.curator_count ?? 0
  const loggedCount = submissions.length
  const progressPct = targetCount > 0 ? Math.min(Math.round((loggedCount / targetCount) * 100), 100) : 0

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden bg-white">
      {/* Header row — click to expand */}
      <button
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-gray-50 transition-colors text-left"
        onClick={() => setExpanded((v) => !v)}
      >
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-xs font-mono bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
            {campaign.campaign_code}
          </span>
          {campaign.budget_allocated != null && (
            <span className="text-xs text-gray-700">
              ${campaign.budget_allocated} budget
            </span>
          )}
          {campaign.curator_count != null && (
            <span className="text-xs text-gray-500">
              {campaign.curator_count} curators target
            </span>
          )}
          {loggedCount > 0 && (
            <span className="text-xs text-indigo-600 font-medium">
              {loggedCount} submitted
            </span>
          )}
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <span className="text-xs text-gray-400">
            {new Date(campaign.created_at).toLocaleDateString('en-GB', {
              day: 'numeric',
              month: 'short',
              year: 'numeric',
            })}
          </span>
          <span className="text-xs text-gray-400">{expanded ? '▲' : '▼'}</span>
        </div>
      </button>

      {/* Expanded body */}
      {expanded && (
        <div className="px-4 pb-4 border-t border-gray-100 space-y-3">

          {/* Stats + progress */}
          {(submissions.length > 0 || targetCount > 0) && (
            <div className="pt-3 space-y-2">
              {submissions.length > 0 && (
                <div className="flex gap-4">
                  <span className="text-xs font-medium text-green-700">{approved} approved</span>
                  <span className="text-xs font-medium text-red-600">{declined} declined</span>
                  <span className="text-xs font-medium text-yellow-700">{pending} pending</span>
                  <span className="text-xs text-gray-500 ml-auto">${totalCost.toFixed(0)} spent</span>
                </div>
              )}
              {targetCount > 0 && (
                <div>
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Submissions logged</span>
                    <span>{loggedCount} / {targetCount}</span>
                  </div>
                  <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-indigo-400 rounded-full transition-all"
                      style={{ width: `${progressPct}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Submissions table */}
          {isLoading ? (
            <p className="text-xs text-gray-400 pt-2">Loading submissions…</p>
          ) : submissions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-xs text-gray-400">
                    <th className="pb-2 pr-3 font-medium">Curator</th>
                    <th className="pb-2 pr-3 font-medium">Genre Focus</th>
                    <th className="pb-2 pr-3 font-medium">Approval Rate</th>
                    <th className="pb-2 pr-3 font-medium">Cost</th>
                    <th className="pb-2 pr-3 font-medium">Status</th>
                    <th className="pb-2 font-medium"></th>
                  </tr>
                </thead>
                <tbody>
                  {submissions.map((sub) => (
                    <SubmissionRow key={sub.id} sub={sub} />
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-sm text-gray-400 pt-2">No submissions logged yet.</p>
          )}

          {/* Add submission */}
          {showAddSub ? (
            <AddSubmissionForm
              shCampaignId={campaign.id}
              onClose={() => setShowAddSub(false)}
            />
          ) : (
            <button
              onClick={(e) => { e.stopPropagation(); setShowAddSub(true) }}
              className="text-xs text-indigo-600 hover:underline"
            >
              + Add curator submission
            </button>
          )}

          {campaign.notes && (
            <p className="text-xs text-gray-400 italic border-t border-gray-100 pt-2">{campaign.notes}</p>
          )}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

export function SubmitHubPage() {
  const { id } = useParams<{ id: string }>()
  const songId = Number(id)
  const [showNewCampaign, setShowNewCampaign] = useState(false)

  const { data: song } = useQuery({
    queryKey: ['song', songId],
    queryFn: () => getSong(songId),
  })

  const { data: campaigns = [], isLoading } = useQuery({
    queryKey: ['sh-campaigns', songId],
    queryFn: () => listSHCampaignsForSong(songId),
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />
      <div className="max-w-3xl mx-auto px-6 py-8 space-y-6">

        {/* Header */}
        <div>
          <Link to={`/songs/${songId}`} className="text-sm text-indigo-600 hover:underline">
            ← {song?.title ?? 'Song'}
          </Link>
          <div className="flex items-start justify-between mt-2">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">SubmitHub Campaigns</h1>
              {song && <p className="text-sm text-gray-500 mt-0.5">{song.artist_name}</p>}
            </div>
            <button
              onClick={() => setShowNewCampaign((v) => !v)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
            >
              {showNewCampaign ? 'Cancel' : '+ New Campaign'}
            </button>
          </div>
        </div>

        {/* New campaign form */}
        {showNewCampaign && (
          <NewCampaignForm songId={songId} onClose={() => setShowNewCampaign(false)} />
        )}

        {/* Campaign list */}
        {isLoading ? (
          <p className="text-sm text-gray-500">Loading…</p>
        ) : campaigns.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center">
            <p className="text-gray-700 font-medium mb-1">No SubmitHub campaigns yet</p>
            <p className="text-sm text-gray-400 mb-4">
              Create a campaign to start tracking curator submissions for this song.
            </p>
            <button
              onClick={() => setShowNewCampaign(true)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
            >
              Create First Campaign
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {campaigns.map((c) => (
              <CampaignCard key={c.id} campaign={c} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
