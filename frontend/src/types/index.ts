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

export interface GeneratedContent {
  id: number
  song_id: number
  post_type: string
  platform: string
  tone: string
  caption_hebrew: string | null
  caption_english: string | null
  hashtags: string[] | null
  character_count: number | null
  created_at: string
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

export interface SongBrief {
  id: number
  title: string
  artist_name: string
}

export interface BudgetChannel {
  amount: number
  pct: number
  rationale: string
}

export interface BudgetRecommendation {
  playlist_pitching: BudgetChannel
  submithub: BudgetChannel
  social_ads: BudgetChannel
  content_creation: BudgetChannel
  radio_promotion: BudgetChannel
  other: BudgetChannel
  top_tip: string
}

export interface Campaign {
  id: number
  name: string
  release_type: 'single' | 'ep' | 'album'
  start_date: string
  end_date: string
  budget_total: number
  budget_spent: number
  primary_goal: 'awareness' | 'growth' | 'monetization' | null
  status: 'planning' | 'active' | 'completed'
  budget_recommendation: BudgetRecommendation | null
  notes: string | null
  songs: SongBrief[]
  created_at: string
}

export interface Expense {
  id: number
  campaign_id: number
  expense_date: string
  amount: number
  category: string
  subcategory: string | null
  description: string | null
  created_at: string
}

export interface SubmitHubCampaign {
  id: number
  song_id: number
  campaign_id: number | null
  campaign_code: string
  budget_allocated: number | null
  curator_count: number | null
  status: 'active' | 'completed'
  notes: string | null
  created_at: string
}

export interface SubmitHubSubmission {
  id: number
  submithub_campaign_id: number
  curator_name: string
  curator_genre_focus: string[] | null
  curator_approval_rate: number | null
  submission_date: string | null
  cost: number
  response_status: 'pending' | 'approved' | 'declined'
  response_date: string | null
  curator_feedback: string | null
  playlist_added: boolean
  playlist_url: string | null
  created_at: string
}

export interface DashboardSnapshot {
  id: number
  snapshot_date: string
  total_streams: number
  total_monthly_listeners: number
  total_followers: number
  total_saves: number
  total_playlist_adds: number
  save_rate: number | null
  follower_conversion_rate: number | null
  cost_per_stream: number | null
  streams_vs_last_week_pct: number | null
  listeners_vs_last_week_pct: number | null
  followers_vs_last_week_pct: number | null
  health_score: number | null
}

export interface HealthScoreResponse {
  health_score: number
  label: string
  snapshot_date: string
  metrics: {
    total_streams: number
    total_monthly_listeners: number
    total_followers: number
    total_saves: number
    total_playlist_adds: number
    save_rate: number | null
    follower_conversion_rate: number | null
    cost_per_stream: number | null
    streams_vs_last_week_pct: number | null
    listeners_vs_last_week_pct: number | null
    followers_vs_last_week_pct: number | null
  }
}

export interface Insight {
  id: number
  insight_type: 'momentum' | 'warning' | 'opportunity' | 'tip' | 'milestone'
  priority: 'high' | 'medium' | 'low'
  title: string
  description: string
  action_text: string | null
  action_link: string | null
  related_song_id: number | null
  related_campaign_id: number | null
  status: 'active' | 'dismissed' | 'actioned'
  created_at: string
}

export interface PostOpportunity {
  id: number
  song_id: number | null
  hook: string
  why_now: string
  signal_type: string
  suggested_platform: string | null
  hashtag_suggestions: string[] | null
  timing_note: string | null
  status: 'active' | 'used' | 'dismissed' | 'remind_later'
  used_at: string | null
  created_at: string
}

export interface ChannelInsight {
  channel: string
  planned: number | null
  actual: number
  verdict: 'on_track' | 'over_budget' | 'under_budget' | 'not_used' | 'unplanned'
  recommendation: string
}

export interface CampaignLearnings {
  summary: string
  channel_insights: ChannelInsight[]
  next_campaign_suggestions: string[]
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
