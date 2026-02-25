import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { createSong } from '../api/songs'

const schema = z.object({
  spotify_url: z.string().min(1, 'Paste a Spotify track URL'),
})

type FormValues = z.infer<typeof schema>

export function SongNewPage() {
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) })

  const mutation = useMutation({
    mutationFn: (values: FormValues) => createSong(values),
    onSuccess: (song) => navigate(`/songs/${song.id}`, { replace: true }),
    onError: (err: unknown) => {
      const message =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        'Failed to add song'
      setError('spotify_url', { message })
    },
  })

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
        <button
          onClick={() => navigate('/songs')}
          className="text-sm text-indigo-600 hover:underline mb-6 block"
        >
          ← Back to songs
        </button>

        <h1 className="text-2xl font-bold text-gray-900 mb-2">Add a Song</h1>
        <p className="text-sm text-gray-500 mb-6">
          Paste a Spotify track URL to import metadata automatically.
        </p>

        <form onSubmit={handleSubmit((v) => mutation.mutate(v))} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Spotify URL</label>
            <input
              {...register('spotify_url')}
              type="text"
              placeholder="https://open.spotify.com/track/..."
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            {errors.spotify_url && (
              <p className="text-xs text-red-600 mt-1">{errors.spotify_url.message}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={mutation.isPending}
            className="w-full bg-indigo-600 text-white py-2 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            {mutation.isPending ? 'Importing from Spotify…' : 'Import Song'}
          </button>
        </form>
      </div>
    </div>
  )
}
