import { useNavigate } from 'react-router-dom'
import type { Song } from '../../types'

interface Props {
  song: Song
}

export function SongCard({ song }: Props) {
  const navigate = useNavigate()
  const year = song.release_date ? song.release_date.slice(0, 4) : '—'

  return (
    <div
      onClick={() => navigate(`/songs/${song.id}`)}
      className="cursor-pointer rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-shadow overflow-hidden"
    >
      {song.album_image_url ? (
        <img
          src={song.album_image_url}
          alt={song.album_name ?? song.title}
          className="w-full aspect-square object-cover"
        />
      ) : (
        <div className="w-full aspect-square bg-gray-100 flex items-center justify-center text-gray-400 text-4xl">
          🎵
        </div>
      )}
      <div className="p-3">
        <p className="font-semibold text-gray-900 truncate">{song.title}</p>
        <p className="text-sm text-gray-500 truncate">{song.artist_name}</p>
        <p className="text-xs text-gray-400 mt-1">{year}</p>
      </div>
    </div>
  )
}
