export interface User {
  id: number
  email: string
  name: string
}

export interface Song {
  id: number
  spotify_track_id: string
  title: string
  artist_name: string
  album_name: string | null
  release_date: string | null
  duration_ms: number | null
  spotify_url: string | null
  album_image_url: string | null
  popularity: number | null
  story: string | null
  mood_tags: string[] | null
  themes: string[] | null
  comparable_artists: string[] | null
  genre: string | null
  language: string | null
}

export interface Playlist {
  id: number
  name: string
  spotify_id: string | null
  curator_name: string | null
  curator_contact: string | null
  follower_count: number | null
  genres: string[] | null
  languages: string[] | null
  mood_tags: string[] | null
  submission_method: string | null
  submission_guidelines: string | null
  is_active: boolean
  notes: string | null
}

export interface RadioStation {
  id: number
  name: string
  name_hebrew: string | null
  station_type: string
  contact_email: string | null
  contact_phone: string | null
  website: string | null
  genres_focus: string[] | null
  best_for: string[] | null
  submission_guidelines: string | null
  response_time: string | null
  reach_description: string | null
  notes: string | null
}

export interface PlaylistMatchEntry {
  playlist: Playlist
  score: number
  reasons: string[]
}

export interface RadioStationMatchEntry {
  station: RadioStation
  recommended: boolean
}

export interface MatchResponse {
  playlists: PlaylistMatchEntry[]
  radio_stations: RadioStationMatchEntry[]
}

export interface PitchSubmission {
  id: number
  song_id: number
  target_type: 'playlist' | 'radio'
  target_name: string | null
  playlist_id: number | null
  radio_station_id: number | null
  pitched_date: string
  pitch_method: string
  status: string
  response_date: string | null
  response_notes: string | null
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
