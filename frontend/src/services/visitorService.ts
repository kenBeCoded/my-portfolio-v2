/**
 * visitorService.ts
 * Handles public portfolio visitor logging and admin analytics fetching.
 *
 * logVisit()       — POST /api/visitors/log  (public, no auth)
 * fetchVisitorStats() — GET /api/visitors/stats (admin, requires JWT)
 */

import { getToken } from './authService'

const BASE_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

// ── Types ──────────────────────────────────────────────────────────────────

export interface DailyVisitorStats {
  date: string
  page_views: number
  unique_visitors: number
}

export interface WeeklyVisitorStats {
  week_start_date: string
  unique_visitors: number
}

export interface TopPageStats {
  page_path: string
  page_views: number
}

export interface RecentVisitorStats {
  id: number
  timestamp: string
  page_path: string
  user_agent: string | null
}

export interface VisitorStatsOut {
  total_page_views: number
  total_unique_visitors: number
  weekly_unique_visitors: number
  daily_stats: DailyVisitorStats[]
  weekly_stats: WeeklyVisitorStats[]
  top_pages: TopPageStats[]
  recent_visits: RecentVisitorStats[]
}

// ── Helpers ────────────────────────────────────────────────────────────────

/**
 * Generate or retrieve a persistent visitor ID for this browser/device.
 * Uses crypto.randomUUID() with a Math.random() fallback.
 */
export function getOrCreateVisitorId(): string {
  const KEY = 'visitor_id'
  let id = localStorage.getItem(KEY)
  if (!id) {
    id = typeof crypto?.randomUUID === 'function'
      ? crypto.randomUUID()
      : 'visitor_' + Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2)
    localStorage.setItem(KEY, id)
  }
  return id
}

// ── API calls ──────────────────────────────────────────────────────────────

/**
 * POST /api/visitors/log
 * Log a single portfolio page visit. Errors are silently swallowed so
 * tracking failures never affect the user experience.
 */
export async function logVisit(
  visitorId: string,
  pagePath: string,
  referer: string,
): Promise<void> {
  try {
    await fetch(`${BASE_URL}/api/visitors/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        visitor_id: visitorId,
        page_path: pagePath,
        user_agent: navigator.userAgent,
        referer: referer || null,
      }),
    })
  } catch {
    // Intentionally silent — tracking errors must never surface to the user
  }
}

/**
 * GET /api/visitors/stats
 * Fetch aggregated analytics (admin-only, requires JWT in localStorage).
 */
export async function fetchVisitorStats(): Promise<VisitorStatsOut> {
  const token = getToken()
  const res = await fetch(`${BASE_URL}/api/visitors/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error(`Failed to fetch visitor stats: ${res.status}`)
  return res.json() as Promise<VisitorStatsOut>
}
