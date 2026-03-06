import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { listAllBriefs } from '../../api/youtube'

const STATUS_DOT: Record<string, string> = {
  draft: 'bg-gray-400',
  planned: 'bg-blue-500',
  filmed: 'bg-amber-500',
  published: 'bg-green-500',
}

export function YouTubeQueueWidget() {
  const { data: briefs = [] } = useQuery({
    queryKey: ['youtube-briefs-all'],
    queryFn: () => listAllBriefs(),
  })

  const active = briefs.filter((b) => b.status !== 'published').slice(0, 4)

  if (active.length === 0) return null

  return (
    <div className="bg-white border border-red-100 rounded-xl p-4 space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-sm font-semibold text-gray-900">YouTube Queue</span>
        <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">{active.length}</span>
      </div>
      <ul className="space-y-2">
        {active.map((brief) => (
          <li key={brief.id} className="flex items-center gap-3">
            <span className={`w-2 h-2 rounded-full flex-shrink-0 ${STATUS_DOT[brief.status]}`} />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-800 truncate">{brief.seo_title ?? '(no title)'}</p>
              <p className="text-xs text-gray-400 capitalize">{brief.status}</p>
            </div>
            <Link
              to={`/songs/${brief.song_id}`}
              className="text-xs text-indigo-600 hover:underline flex-shrink-0"
            >
              Edit
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
