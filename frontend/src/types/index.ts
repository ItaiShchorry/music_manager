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
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
