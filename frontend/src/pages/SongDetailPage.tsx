import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getPitchesForSong, updatePitch } from '../api/pitches'
import { getSong, updateSong } from '../api/songs'
import { Nav } from '../components/Nav'
import { ContentPanel } from '../components/content/ContentPanel'
import type { PitchSubmission, Song } from '../types'

// ---------------------------------------------------------------------------
// Suggestions & story starters
// ---------------------------------------------------------------------------

const SUGGESTED_GENRES = [
  'mainstream Hebrew pop', 'indie pop', 'acoustic', 'R&B / soul',
  'folk', 'mizrahi', 'rock', 'hip hop', 'electronic', 'alternative',
]

const SUGGESTED_MOODS = [
  'upbeat', 'melancholic', 'romantic', 'energetic', 'dreamy',
  'nostalgic', 'hopeful', 'dark', 'playful', 'intense',
  'chill', 'bittersweet', 'empowering', 'spiritual',
]

const STORY_STARTERS = [
  {
    theme: 'Heartbreak',
    text: "This song was written the night after a relationship ended. I wanted to capture that specific feeling of sitting alone at 2am, replaying every moment and every word.",
  },
  {
    theme: 'Nostalgia',
    text: "I grew up in [neighborhood] and this song is a love letter to that time — the streets, the sounds, the people who shaped who I am.",
  },
  {
    theme: 'New love',
    text: "I wrote this during the early weeks of a relationship, when everything feels electric and uncertain. It's about the courage it takes to let someone in.",
  },
  {
    theme: 'Resilience',
    text: "After a really hard period in my life, I needed to write something that reminded me — and others — that you can come out the other side stronger.",
  },
  {
    theme: 'Longing',
    text: "This song is about missing someone who's physically close but emotionally distant — the kind of distance you can't measure in kilometers.",
  },
  {
    theme: 'Celebration',
    text: "Sometimes you just need a song about joy. This came from a specific night with people I love, and I wanted to bottle that feeling forever.",
  },
]

// ---------------------------------------------------------------------------
// Tag input component (comma-separated chips)
// ---------------------------------------------------------------------------
interface TagInputProps {
  value: string[]
  onChange: (tags: string[]) => void
  placeholder?: string
}

function TagInput({ value, onChange, placeholder }: TagInputProps) {
  const [input, setInput] = useState('')

  const commit = () => {
    const trimmed = input.trim()
    if (trimmed && !value.includes(trimmed)) {
      onChange([...value, trimmed])
    }
    setInput('')
  }

  const remove = (tag: string) => onChange(value.filter((t) => t !== tag))

  return (
    <div className="border border-gray-300 rounded-lg px-3 py-2 flex flex-wrap gap-2 focus-within:ring-2 focus-within:ring-indigo-500">
      {value.map((tag) => (
        <span
          key={tag}
          className="inline-flex items-center gap-1 bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full"
        >
          {tag}
          <button type="button" onClick={() => remove(tag)} className="hover:text-red-500">
            ×
          </button>
        </span>
      ))}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault()
            commit()
          }
          if (e.key === 'Backspace' && !input && value.length) {
            onChange(value.slice(0, -1))
          }
        }}
        onBlur={commit}
        placeholder={value.length === 0 ? placeholder : ''}
        className="flex-1 min-w-[120px] text-sm outline-none bg-transparent"
      />
    </div>
  )
}

// ---------------------------------------------------------------------------
// Suggested tags chip picker
// ---------------------------------------------------------------------------

function SuggestedTags({
  tags,
  isActive,
  onToggle,
}: {
  tags: string[]
  isActive: (tag: string) => boolean
  onToggle: (tag: string) => void
}) {
  return (
    <div className="flex flex-wrap gap-1.5 mt-2">
      {tags.map((tag) => (
        <button
          key={tag}
          type="button"
          onClick={() => onToggle(tag)}
          className={`text-xs px-2.5 py-1 rounded-full border transition-colors ${
            isActive(tag)
              ? 'bg-indigo-100 text-indigo-800 border-indigo-300 font-medium'
              : 'bg-white text-gray-500 border-gray-200 hover:border-indigo-300 hover:text-indigo-700'
          }`}
        >
          {tag}
        </button>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Story starters panel
// ---------------------------------------------------------------------------

function StoryStarters({ onSelect }: { onSelect: (text: string) => void }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-2">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="text-xs text-indigo-600 hover:underline"
      >
        {open ? '▲ Hide story starters' : '▼ Need inspiration? Browse story starters'}
      </button>
      {open && (
        <div className="mt-3 grid gap-2">
          {STORY_STARTERS.map(({ theme, text }) => (
            <div key={theme} className="border border-gray-100 rounded-lg p-3 bg-gray-50">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <span className="text-xs font-semibold text-gray-600 block mb-1">{theme}</span>
                  <p className="text-xs text-gray-500 leading-relaxed">{text}</p>
                </div>
                <button
                  type="button"
                  onClick={() => { onSelect(text); setOpen(false) }}
                  className="flex-shrink-0 text-xs text-indigo-600 hover:text-indigo-800 font-medium whitespace-nowrap"
                >
                  Use this
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Status badge
// ---------------------------------------------------------------------------
const STATUS_COLORS: Record<string, string> = {
  sent: 'bg-blue-100 text-blue-800',
  responded: 'bg-yellow-100 text-yellow-800',
  added: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
  no_response: 'bg-gray-100 text-gray-600',
}

// ---------------------------------------------------------------------------
// Pitch row
// ---------------------------------------------------------------------------
interface PitchRowProps {
  pitch: PitchSubmission
  onStatusChange: (id: number, status: string) => void
}

function PitchRow({ pitch, onStatusChange }: PitchRowProps) {
  const date = new Date(pitch.pitched_date).toLocaleDateString()
  const target = pitch.target_name ?? (pitch.target_type === 'playlist'
    ? `Playlist #${pitch.playlist_id}`
    : `Radio #${pitch.radio_station_id}`)

  return (
    <tr className="border-t border-gray-100">
      <td className="py-2 pr-4 text-sm text-gray-700">{target}</td>
      <td className="py-2 pr-4 text-sm text-gray-500">{date}</td>
      <td className="py-2 pr-4 text-sm text-gray-500">{pitch.pitch_method}</td>
      <td className="py-2">
        <select
          value={pitch.status}
          onChange={(e) => onStatusChange(pitch.id, e.target.value)}
          className={`text-xs font-medium px-2 py-1 rounded-full border-0 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer ${STATUS_COLORS[pitch.status] ?? 'bg-gray-100 text-gray-600'}`}
        >
          {['sent', 'responded', 'added', 'rejected', 'no_response'].map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </td>
    </tr>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
export function SongDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: song, isLoading, error } = useQuery({
    queryKey: ['song', Number(id)],
    queryFn: () => getSong(Number(id)),
  })

  const { data: pitches = [] } = useQuery({
    queryKey: ['pitches', Number(id)],
    queryFn: () => getPitchesForSong(Number(id)),
  })

  const [story, setStory] = useState<string>('')
  const [moodTags, setMoodTags] = useState<string[]>([])
  const [themes, setThemes] = useState<string[]>([])
  const [comparableArtists, setComparableArtists] = useState<string[]>([])
  const [genre, setGenre] = useState<string>('')
  const [language, setLanguage] = useState<string>('')

  useEffect(() => {
    if (song) {
      setStory(song.story ?? '')
      setMoodTags(song.mood_tags ?? [])
      setThemes(song.themes ?? [])
      setComparableArtists(song.comparable_artists ?? [])
      setGenre(song.genre ?? '')
      setLanguage(song.language ?? '')
    }
  }, [song?.id])

  const mutation = useMutation({
    mutationFn: (patch: Partial<Pick<Song, 'story' | 'mood_tags' | 'themes' | 'comparable_artists' | 'genre' | 'language'>>) =>
      updateSong(Number(id), patch),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['song', Number(id)] })
    },
  })

  const pitchMutation = useMutation({
    mutationFn: ({ pitchId, status }: { pitchId: number; status: string }) =>
      updatePitch(pitchId, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pitches', Number(id)] })
    },
  })

  const handleSave = () => {
    mutation.mutate({
      story: story || null,
      mood_tags: moodTags.length ? moodTags : null,
      themes: themes.length ? themes : null,
      comparable_artists: comparableArtists.length ? comparableArtists : null,
      genre: genre || null,
      language: language || null,
    })
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (error || !song) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-red-600">Song not found.</p>
      </div>
    )
  }

  const releaseYear = song.release_date ? song.release_date.slice(0, 4) : '—'
  const durationMin = song.duration_ms
    ? `${Math.floor(song.duration_ms / 60000)}:${String(Math.floor((song.duration_ms % 60000) / 1000)).padStart(2, '0')}`
    : '—'

  return (
    <div className="min-h-screen bg-gray-50">
      <Nav />

      <main className="max-w-3xl mx-auto p-6 space-y-8">
        {/* Back link */}
        <button
          onClick={() => navigate('/songs')}
          className="text-sm text-indigo-600 hover:underline"
        >
          ← Back to songs
        </button>

        {/* Spotify metadata (read-only) */}
        <section className="bg-white rounded-2xl shadow-sm p-6 flex gap-6">
          {song.album_image_url ? (
            <img
              src={song.album_image_url}
              alt={song.album_name ?? song.title}
              className="w-32 h-32 rounded-xl object-cover flex-shrink-0"
            />
          ) : (
            <div className="w-32 h-32 rounded-xl bg-gray-100 flex items-center justify-center text-4xl flex-shrink-0">
              🎵
            </div>
          )}
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold text-gray-900 truncate">{song.title}</h2>
            <p className="text-gray-600 mt-1">{song.artist_name}</p>
            {song.album_name && (
              <p className="text-sm text-gray-400 mt-1">{song.album_name}</p>
            )}
            <div className="mt-3 flex gap-4 text-sm text-gray-500">
              <span>📅 {releaseYear}</span>
              <span>⏱ {durationMin}</span>
              {song.popularity !== null && <span>🔥 {song.popularity}/100</span>}
            </div>
            {song.spotify_url && (
              <a
                href={song.spotify_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-3 text-xs text-green-600 hover:underline"
              >
                Open in Spotify ↗
              </a>
            )}
          </div>
        </section>

        {/* Manual fields (editable) */}
        <section className="bg-white rounded-2xl shadow-sm p-6 space-y-5">
          <h3 className="text-lg font-semibold text-gray-900">Song Profile</h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Genre</label>
              <input
                type="text"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                placeholder="e.g. mainstream Hebrew pop"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <SuggestedTags
                tags={SUGGESTED_GENRES}
                isActive={(t) => genre === t}
                onToggle={(t) => setGenre(genre === t ? '' : t)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">— select —</option>
                <option value="hebrew">Hebrew</option>
                <option value="english">English</option>
                <option value="both">Both</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Story</label>
            <textarea
              value={story}
              onChange={(e) => setStory(e.target.value)}
              rows={4}
              placeholder="What's the story behind this song?"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
            />
            <StoryStarters onSelect={setStory} />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mood Tags</label>
            <TagInput
              value={moodTags}
              onChange={setMoodTags}
              placeholder="e.g. melancholic, upbeat — press Enter or comma"
            />
            <SuggestedTags
              tags={SUGGESTED_MOODS}
              isActive={(t) => moodTags.includes(t)}
              onToggle={(t) =>
                setMoodTags(moodTags.includes(t) ? moodTags.filter((m) => m !== t) : [...moodTags, t])
              }
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Themes</label>
            <TagInput
              value={themes}
              onChange={setThemes}
              placeholder="e.g. love, nostalgia, freedom"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Comparable Artists</label>
            <TagInput
              value={comparableArtists}
              onChange={setComparableArtists}
              placeholder="e.g. Idan Raichel, Dudu Tassa"
            />
          </div>

          <div className="flex items-center gap-3 pt-2">
            <button
              onClick={handleSave}
              disabled={mutation.isPending}
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
            >
              {mutation.isPending ? 'Saving…' : 'Save'}
            </button>
            {mutation.isSuccess && (
              <span className="text-sm text-green-600">Saved!</span>
            )}
            {mutation.isError && (
              <span className="text-sm text-red-600">Save failed. Please try again.</span>
            )}
          </div>
        </section>

        {/* Content generation */}
        <ContentPanel songId={Number(id)} />

        {/* SubmitHub campaigns */}
        <section className="bg-white rounded-2xl shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">SubmitHub Campaigns</h3>
              <p className="text-sm text-gray-400 mt-0.5">
                Plan curator submissions and track outcomes for this song.
              </p>
            </div>
            <Link
              to={`/songs/${id}/submithub`}
              className="text-sm bg-indigo-50 text-indigo-700 px-4 py-2 rounded-lg hover:bg-indigo-100 font-medium transition-colors"
            >
              Manage →
            </Link>
          </div>
        </section>

        {/* Pitch history */}
        <section className="bg-white rounded-2xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Pitch History
              {pitches.length > 0 && (
                <span className="ml-2 text-sm font-normal text-gray-400">({pitches.length})</span>
              )}
            </h3>
            <Link
              to={`/discover?song=${id}`}
              className="text-xs text-indigo-600 hover:underline"
            >
              + Discover & pitch →
            </Link>
          </div>

          {pitches.length === 0 ? (
            <p className="text-sm text-gray-400">No pitches logged yet.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-xs text-gray-400 uppercase tracking-wide">
                    <th className="pb-2 pr-4 font-medium">Target</th>
                    <th className="pb-2 pr-4 font-medium">Date</th>
                    <th className="pb-2 pr-4 font-medium">Method</th>
                    <th className="pb-2 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {pitches.map((pitch) => (
                    <PitchRow
                      key={pitch.id}
                      pitch={pitch}
                      onStatusChange={(pitchId, status) =>
                        pitchMutation.mutate({ pitchId, status })
                      }
                    />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
