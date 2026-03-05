import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { addExpense, applyLearnings, getBudgetRecommendation, getCampaign, listExpenses, updateCampaign } from '../api/campaigns'
import { Nav } from '../components/Nav'
import type { BudgetRecommendation, Campaign, CampaignLearnings, ChannelInsight } from '../types'
import type { ExpenseCreate } from '../api/campaigns'

const EXPENSE_CATEGORIES = [
  'playlist_pitching', 'social_ads', 'content', 'radio_promotion',
  'submithub', 'pr', 'other',
] as const

// Maps expense category names → budget recommendation channel keys
const CATEGORY_TO_CHANNEL: Record<string, string> = {
  playlist_pitching: 'playlist_pitching',
  submithub: 'submithub',
  social_ads: 'social_ads',
  content: 'content_creation',
  radio_promotion: 'radio_promotion',
  pr: 'other',
  other: 'other',
}

const STATUS_OPTIONS = ['planning', 'active', 'completed'] as const

// ---------------------------------------------------------------------------
// Budget Recommendation card
// ---------------------------------------------------------------------------

function BudgetCard({
  rec,
  actualByChannel,
}: {
  rec: BudgetRecommendation
  actualByChannel: Record<string, number>
}) {
  const channels = [
    { key: 'playlist_pitching' as const, label: 'Playlist Pitching' },
    { key: 'submithub' as const, label: 'SubmitHub' },
    { key: 'social_ads' as const, label: 'Social Ads' },
    { key: 'content_creation' as const, label: 'Content Creation' },
    { key: 'radio_promotion' as const, label: 'Radio Promotion' },
    { key: 'other' as const, label: 'Other' },
  ]

  return (
    <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-indigo-900">AI Budget Recommendation</h4>
        <span className="text-xs text-indigo-500">planned → actual</span>
      </div>
      {rec.top_tip && (
        <p className="text-xs text-indigo-700 italic">💡 {rec.top_tip}</p>
      )}
      <div className="space-y-4">
        {channels.map(({ key, label }) => {
          const ch = rec[key]
          if (!ch || ch.amount === 0) return null
          const actual = actualByChannel[key] ?? 0
          const isOver = actual > ch.amount
          const fillPct = ch.amount > 0 ? Math.min(Math.round((actual / ch.amount) * 100), 100) : 0
          return (
            <div key={key}>
              <div className="flex justify-between items-baseline text-xs mb-1">
                <span className="font-medium text-gray-700">
                  {label} <span className="text-gray-400 font-normal">({ch.pct}%)</span>
                </span>
                <span className={isOver ? 'text-red-600 font-medium' : actual > 0 ? 'text-indigo-700 font-medium' : 'text-gray-400'}>
                  ${actual.toFixed(0)} / ${ch.amount}
                  {isOver && (
                    <span className="ml-1 text-red-500 font-normal">
                      (+${(actual - ch.amount).toFixed(0)} over)
                    </span>
                  )}
                </span>
              </div>
              {/* Bar: background = recommended budget, fill = actual spent */}
              <div className="h-2 bg-white rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${isOver ? 'bg-red-400' : actual > 0 ? 'bg-indigo-500' : 'bg-indigo-200'}`}
                  style={{ width: `${fillPct || (actual === 0 ? 0 : 100)}%` }}
                />
              </div>
              <p className="text-xs text-gray-400 mt-0.5">{ch.rationale}</p>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Expense row
// ---------------------------------------------------------------------------

function ExpenseRow({ expense }: { expense: { expense_date: string; amount: number; category: string; subcategory: string | null; description: string | null } }) {
  return (
    <tr className="border-t border-gray-100">
      <td className="py-2 text-xs text-gray-500">{expense.expense_date}</td>
      <td className="py-2 text-sm text-gray-800">${expense.amount.toFixed(2)}</td>
      <td className="py-2 text-xs text-gray-600 capitalize">{expense.category.replace('_', ' ')}</td>
      <td className="py-2 text-xs text-gray-500">{expense.subcategory ?? '—'}</td>
      <td className="py-2 text-xs text-gray-400">{expense.description ?? ''}</td>
    </tr>
  )
}

// ---------------------------------------------------------------------------
// Add Expense form
// ---------------------------------------------------------------------------

function AddExpenseForm({ campaignId, onClose }: { campaignId: number; onClose: () => void }) {
  const queryClient = useQueryClient()
  const [form, setForm] = useState<ExpenseCreate>({
    expense_date: new Date().toISOString().slice(0, 10),
    amount: 0,
    category: 'playlist_pitching',
    subcategory: '',
    description: '',
  })

  const mutation = useMutation({
    mutationFn: () => addExpense(campaignId, {
      ...form,
      subcategory: form.subcategory || undefined,
      description: form.description || undefined,
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] })
      queryClient.invalidateQueries({ queryKey: ['expenses', campaignId] })
      onClose()
    },
  })

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 space-y-3">
      <h4 className="text-sm font-semibold text-gray-700">Add Expense</h4>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Date</label>
          <input
            type="date"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.expense_date}
            onChange={(e) => setForm({ ...form, expense_date: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Amount ($)</label>
          <input
            type="number"
            min={0.01}
            step={0.01}
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: Number(e.target.value) })}
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Category</label>
          <select
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value as ExpenseCreate['category'] })}
          >
            {EXPENSE_CATEGORIES.map((c) => (
              <option key={c} value={c}>{c.replace('_', ' ')}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Subcategory</label>
          <input
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.subcategory}
            onChange={(e) => setForm({ ...form, subcategory: e.target.value })}
            placeholder="e.g. Instagram Ads"
          />
        </div>
      </div>
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Description (optional)</label>
        <input
          className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          placeholder="e.g. SubmitHub 12 credits"
        />
      </div>
      <div className="flex gap-2 justify-end">
        <button onClick={onClose} className="text-sm text-gray-500 hover:text-gray-700">Cancel</button>
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending || form.amount <= 0}
          className="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {mutation.isPending ? 'Adding…' : 'Add Expense'}
        </button>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Learnings card
// ---------------------------------------------------------------------------

const VERDICT_STYLES: Record<string, string> = {
  on_track: 'bg-green-100 text-green-800',
  over_budget: 'bg-red-100 text-red-800',
  under_budget: 'bg-yellow-100 text-yellow-800',
  not_used: 'bg-gray-100 text-gray-500',
  unplanned: 'bg-orange-100 text-orange-800',
}

const VERDICT_LABELS: Record<string, string> = {
  on_track: 'On track',
  over_budget: 'Over budget',
  under_budget: 'Under budget',
  not_used: 'Not used',
  unplanned: 'Unplanned',
}

const CHANNEL_LABELS: Record<string, string> = {
  playlist_pitching: 'Playlist Pitching',
  submithub: 'SubmitHub',
  social_ads: 'Social Ads',
  content_creation: 'Content Creation',
  radio_promotion: 'Radio Promotion',
  other: 'Other',
}

function LearningsCard({ learnings }: { learnings: CampaignLearnings }) {
  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-700 leading-relaxed">{learnings.summary}</p>

      {learnings.channel_insights.length > 0 && (
        <div className="space-y-2">
          <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Channel breakdown</h5>
          {learnings.channel_insights.map((ci: ChannelInsight) => (
            <div key={ci.channel} className="bg-gray-50 rounded-lg p-3 space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-800">
                  {CHANNEL_LABELS[ci.channel] ?? ci.channel}
                </span>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${VERDICT_STYLES[ci.verdict] ?? 'bg-gray-100 text-gray-600'}`}>
                  {VERDICT_LABELS[ci.verdict] ?? ci.verdict}
                </span>
              </div>
              <div className="flex gap-4 text-xs text-gray-500">
                {ci.planned != null && <span>Planned: ${ci.planned.toFixed(0)}</span>}
                <span>Actual: ${ci.actual.toFixed(0)}</span>
              </div>
              <p className="text-xs text-gray-600 italic">{ci.recommendation}</p>
            </div>
          ))}
        </div>
      )}

      {learnings.next_campaign_suggestions.length > 0 && (
        <div className="space-y-1">
          <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Next campaign</h5>
          <ul className="space-y-1">
            {learnings.next_campaign_suggestions.map((s, i) => (
              <li key={i} className="text-sm text-gray-700 flex gap-2">
                <span className="text-indigo-400 flex-shrink-0">→</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export function CampaignDetailPage() {
  const { id } = useParams<{ id: string }>()
  const campaignId = Number(id)
  const queryClient = useQueryClient()

  const [showAddExpense, setShowAddExpense] = useState(false)
  const [learnings, setLearnings] = useState<CampaignLearnings | null>(null)

  const { data: campaign, isLoading } = useQuery<Campaign>({
    queryKey: ['campaign', campaignId],
    queryFn: () => getCampaign(campaignId),
  })

  const { data: expenses = [] } = useQuery({
    queryKey: ['expenses', campaignId],
    queryFn: () => listExpenses(campaignId),
    enabled: !!campaign,
  })

  const recMutation = useMutation({
    mutationFn: () => getBudgetRecommendation(campaignId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] }),
  })

  const statusMutation = useMutation({
    mutationFn: (status: Campaign['status']) => updateCampaign(campaignId, { status }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] }),
  })

  const learningsMutation = useMutation({
    mutationFn: () => applyLearnings(campaignId),
    onSuccess: (data) => setLearnings(data),
  })

  if (isLoading || !campaign) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Nav />
        <div className="max-w-3xl mx-auto px-6 py-8">
          <p className="text-sm text-gray-500">Loading…</p>
        </div>
      </div>
    )
  }

  const spentPct = campaign.budget_total > 0
    ? Math.min(Math.round((campaign.budget_spent / campaign.budget_total) * 100), 100)
    : 0

  const actualByChannel = expenses.reduce<Record<string, number>>((acc, e) => {
    const channel = CATEGORY_TO_CHANNEL[e.category] ?? 'other'
    acc[channel] = (acc[channel] ?? 0) + e.amount
    return acc
  }, {})

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />
      <div className="max-w-3xl mx-auto px-6 py-8 space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{campaign.name}</h1>
            <p className="text-sm text-gray-500 mt-1">
              {campaign.release_type.toUpperCase()} · {campaign.start_date} → {campaign.end_date}
            </p>
          </div>
          <select
            value={campaign.status}
            onChange={(e) => statusMutation.mutate(e.target.value as Campaign['status'])}
            className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Budget overview */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Budget</h3>
          <div className="flex justify-between text-sm mb-2">
            <span className="text-gray-500">${campaign.budget_spent.toFixed(2)} spent</span>
            <span className="font-medium text-gray-900">${campaign.budget_total.toFixed(2)} total</span>
          </div>
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden mb-1">
            <div
              className={`h-full rounded-full transition-all ${spentPct >= 80 ? 'bg-orange-400' : 'bg-indigo-500'}`}
              style={{ width: `${spentPct}%` }}
            />
          </div>
          <p className="text-xs text-gray-400">{spentPct}% of budget used</p>
        </div>

        {/* Songs */}
        {campaign.songs.length > 0 && (
          <div className="bg-white rounded-2xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Songs in Campaign</h3>
            <div className="flex flex-wrap gap-2">
              {campaign.songs.map((s) => (
                <span key={s.id} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">
                  {s.title}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Budget Recommendation */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-700">Budget Allocation</h3>
            <button
              onClick={() => recMutation.mutate()}
              disabled={recMutation.isPending}
              className="text-xs bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
            >
              {recMutation.isPending ? 'Generating…' : campaign.budget_recommendation ? 'Regenerate' : 'Get AI Recommendation'}
            </button>
          </div>
          {campaign.budget_recommendation ? (
            <BudgetCard rec={campaign.budget_recommendation} actualByChannel={actualByChannel} />
          ) : (
            <p className="text-sm text-gray-400">
              No recommendation yet. Click "Get AI Recommendation" to generate a channel split.
            </p>
          )}
        </div>

        {/* Expenses */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-700">Expenses</h3>
            <button
              onClick={() => setShowAddExpense((v) => !v)}
              className="text-xs bg-indigo-600 text-white px-3 py-1.5 rounded-lg hover:bg-indigo-700"
            >
              + Add Expense
            </button>
          </div>

          {showAddExpense && (
            <AddExpenseForm campaignId={campaignId} onClose={() => setShowAddExpense(false)} />
          )}

          {expenses.length === 0 ? (
            <p className="text-sm text-gray-400">No expenses logged yet.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-xs font-medium text-gray-500">
                    <th className="pb-2">Date</th>
                    <th className="pb-2">Amount</th>
                    <th className="pb-2">Category</th>
                    <th className="pb-2">Subcategory</th>
                    <th className="pb-2">Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {expenses.map((e) => (
                    <ExpenseRow key={e.id} expense={e} />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Apply Learnings */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-gray-700">Apply Learnings</h3>
              <p className="text-xs text-gray-400 mt-0.5">
                Analyze what worked, what didn't, and what to do next time.
              </p>
            </div>
            <button
              onClick={() => learningsMutation.mutate()}
              disabled={learningsMutation.isPending}
              className="text-xs bg-violet-600 text-white px-3 py-1.5 rounded-lg hover:bg-violet-700 disabled:opacity-50 transition-colors"
            >
              {learningsMutation.isPending ? 'Analyzing…' : learnings ? 'Re-analyze' : 'Analyze Campaign ✨'}
            </button>
          </div>
          {learningsMutation.isError && (
            <p className="text-xs text-red-500">Analysis failed. Please try again.</p>
          )}
          {learnings ? (
            <LearningsCard learnings={learnings} />
          ) : (
            <p className="text-sm text-gray-400">
              Click "Analyze Campaign" to get AI-powered insights on your channel spend and recommendations for next time.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
