import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { generateContent, getGeneratedContent } from '../../api/content'
import type { Platform, PostType, Tone } from '../../api/content'
import type { GeneratedContent } from '../../types'

const POST_TYPE_LABELS: Record<PostType, string> = {
  release: 'New Release Announcement',
  bts: 'Behind-the-Scenes / Studio',
  story: 'Story Behind the Song',
  engagement: 'Engagement (Question / Poll)',
  thank_you: 'Thank You / Milestone',
}

const TONE_LABELS: Record<Tone, string> = {
  emotional: 'Emotional / Vulnerable',
  excited: 'Excited / Energetic',
  casual: 'Conversational / Casual',
}

const PLATFORM_LABELS: Record<Platform, string> = {
  instagram: 'Instagram',
  facebook: 'Facebook',
  tiktok: 'TikTok',
}

const PLATFORM_COLORS: Record<Platform, string> = {
  instagram: 'bg-pink-100 text-pink-800',
  facebook: 'bg-blue-100 text-blue-700',
  tiktok: 'bg-gray-900 text-white',
}

const TONE_COLORS: Record<Tone, string> = {
  emotional: 'bg-purple-100 text-purple-800',
  excited: 'bg-orange-100 text-orange-800',
  casual: 'bg-teal-100 text-teal-800',
}

// ---------------------------------------------------------------------------
// Generated content card
// ---------------------------------------------------------------------------

function ContentCard({ item }: { item: GeneratedContent }) {
  const [copied, setCopied] = useState<'he' | 'en' | null>(null)

  const copy = (text: string, which: 'he' | 'en') => {
    navigator.clipboard.writeText(text)
    setCopied(which)
    setTimeout(() => setCopied(null), 1500)
  }

  const platform = item.platform as Platform
  const tone = item.tone as Tone

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
      <div className="flex items-center gap-2 flex-wrap">
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${PLATFORM_COLORS[platform] ?? 'bg-gray-100 text-gray-700'}`}>
          {PLATFORM_LABELS[platform] ?? platform}
        </span>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${TONE_COLORS[tone] ?? 'bg-gray-100 text-gray-600'}`}>
          {TONE_LABELS[tone] ?? tone}
        </span>
        {item.character_count !== null && (
          <span className="text-xs text-gray-400 ml-auto">{item.character_count} chars</span>
        )}
      </div>

      {item.caption_hebrew && (
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-medium text-gray-500">Hebrew</span>
            <button
              onClick={() => copy(item.caption_hebrew!, 'he')}
              className="text-xs text-indigo-600 hover:underline"
            >
              {copied === 'he' ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <p dir="rtl" lang="he" className="text-sm text-gray-800 bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">
            {item.caption_hebrew}
          </p>
        </div>
      )}

      {item.caption_english && (
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-medium text-gray-500">English</span>
            <button
              onClick={() => copy(item.caption_english!, 'en')}
              className="text-xs text-indigo-600 hover:underline"
            >
              {copied === 'en' ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <p className="text-sm text-gray-800 bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">
            {item.caption_english}
          </p>
        </div>
      )}

      {item.hashtags && item.hashtags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {item.hashtags.map((tag) => (
            <span key={tag} className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full">
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main panel
// ---------------------------------------------------------------------------

interface Props {
  songId: number
}

const ALL_TONES: Tone[] = ['emotional', 'excited', 'casual']
const ALL_PLATFORMS: Platform[] = ['instagram', 'facebook', 'tiktok']

export function ContentPanel({ songId }: Props) {
  const queryClient = useQueryClient()

  // Form state
  const [postType, setPostType] = useState<PostType>('release')
  const [keyMessage, setKeyMessage] = useState('')
  const [context, setContext] = useState('')
  const [selectedTones, setSelectedTones] = useState<Tone[]>(['emotional', 'excited', 'casual'])
  const [selectedPlatforms, setSelectedPlatforms] = useState<Platform[]>(['instagram', 'facebook', 'tiktok'])

  // Previously generated content
  const { data: history = [] } = useQuery({
    queryKey: ['content', songId],
    queryFn: () => getGeneratedContent(songId),
  })

  const mutation = useMutation({
    mutationFn: () =>
      generateContent(songId, {
        post_type: postType,
        key_message: keyMessage || undefined,
        context: context || undefined,
        tones: selectedTones,
        platforms: selectedPlatforms,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['content', songId] })
    },
  })

  const toggleTone = (tone: Tone) =>
    setSelectedTones((prev) =>
      prev.includes(tone) ? prev.filter((t) => t !== tone) : [...prev, tone],
    )

  const togglePlatform = (platform: Platform) =>
    setSelectedPlatforms((prev) =>
      prev.includes(platform) ? prev.filter((p) => p !== platform) : [...prev, platform],
    )

  return (
    <section className="bg-white rounded-2xl shadow-sm p-6 space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Generate Social Content</h3>

      {/* Post type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Post type</label>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {(Object.keys(POST_TYPE_LABELS) as PostType[]).map((type) => (
            <label key={type} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="postType"
                value={type}
                checked={postType === type}
                onChange={() => setPostType(type)}
                className="text-indigo-600"
              />
              <span className="text-sm text-gray-700">{POST_TYPE_LABELS[type]}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Key message + context */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Key message <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <input
            type="text"
            value={keyMessage}
            onChange={(e) => setKeyMessage(e.target.value)}
            placeholder="e.g. Out now on Spotify"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Context <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <input
            type="text"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="e.g. Recorded in one take"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Tones + platforms */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Tones</label>
          <div className="space-y-1.5">
            {ALL_TONES.map((tone) => (
              <label key={tone} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedTones.includes(tone)}
                  onChange={() => toggleTone(tone)}
                  className="text-indigo-600"
                />
                <span className="text-sm text-gray-700">{TONE_LABELS[tone]}</span>
              </label>
            ))}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Platforms</label>
          <div className="space-y-1.5">
            {ALL_PLATFORMS.map((platform) => (
              <label key={platform} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedPlatforms.includes(platform)}
                  onChange={() => togglePlatform(platform)}
                  className="text-indigo-600"
                />
                <span className="text-sm text-gray-700">{PLATFORM_LABELS[platform]}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Generate button */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending || selectedTones.length === 0 || selectedPlatforms.length === 0}
          className="bg-indigo-600 text-white px-5 py-2 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          {mutation.isPending ? 'Generating…' : 'Generate Content'}
        </button>
        {mutation.isError && (
          <span className="text-sm text-red-600">
            {(mutation.error as any)?.response?.data?.detail ?? 'Generation failed. Please try again.'}
          </span>
        )}
      </div>

      {/* Newly generated results */}
      {mutation.data && mutation.data.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Generated ({mutation.data.length} variants)
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mutation.data.map((item) => (
              <ContentCard key={item.id} item={item} />
            ))}
          </div>
        </div>
      )}

      {/* History */}
      {history.length > 0 && !mutation.data && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Previous generations ({history.length})
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {history.slice(0, 6).map((item) => (
              <ContentCard key={item.id} item={item} />
            ))}
          </div>
          {history.length > 6 && (
            <p className="text-xs text-gray-400 mt-3">
              Showing 6 of {history.length} — generate new content to refresh.
            </p>
          )}
        </div>
      )}
    </section>
  )
}
