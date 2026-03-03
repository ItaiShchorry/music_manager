import { NavLink } from 'react-router-dom'

export function Nav() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-medium px-3 py-1 rounded-lg transition-colors ${
      isActive
        ? 'bg-indigo-100 text-indigo-700'
        : 'text-gray-600 hover:text-indigo-600 hover:bg-gray-100'
    }`

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-4">
      <span className="text-sm font-semibold text-gray-900 mr-4">Music Manager</span>
      <NavLink to="/songs" className={linkClass}>Songs</NavLink>
      <NavLink to="/discover" className={linkClass}>Discover</NavLink>
    </nav>
  )
}
