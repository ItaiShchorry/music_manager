import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getSong, updateSong } from '../api/songs'
import type { Song } from '../types'

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

  const [story, setStory] = useState<string>('')
  const [moodTags, setMoodTags] = useState<string[]>([])
  const [themes, setThemes] = useState<string[]>([])
  const [comparableArtists, setComparableArtists] = useState<string[]>([])
  const [formInitialised, setFormInitialised] = useState(false)

  // Initialise form from query data once
  if (song && !formInitialised) {
    setStory(song.story ?? '')
    setMoodTags(song.mood_tags ?? [])
    setThemes(song.themes ?? [])
    setComparableArtists(song.comparable_artists ?? [])
    setFormInitialised(true)
  }

  const mutation = useMutation({
    mutationFn: (patch: Partial<Pick<Song, 'story' | 'mood_tags' | 'themes' | 'comparable_artists'>>) =>
      updateSong(Number(id), patch),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['song', Number(id)] })
    },
  })

  const handleSave = () => {
    mutation.mutate({
      story: story || null,
      mood_tags: moodTags.length ? moodTags : null,
      themes: themes.length ? themes : null,
      comparable_artists: comparableArtists.length ? comparableArtists : null,
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
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <button
          onClick={() => navigate('/songs')}
          className="text-sm text-indigo-600 hover:underline"
        >
          ← Back to songs
        </button>
      </header>

      <main className="max-w-3xl mx-auto p-6 space-y-8">
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

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Story</label>
            <textarea
              value={story}
              onChange={(e) => setStory(e.target.value)}
              rows={4}
              placeholder="What's the story behind this song?"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mood Tags</label>
            <TagInput
              value={moodTags}
              onChange={setMoodTags}
              placeholder="e.g. melancholic, upbeat — press Enter or comma"
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
      </main>
    </div>
  )
}
