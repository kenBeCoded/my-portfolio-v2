/**
 * authService.ts
 * Handles authentication against POST /api/auth/login (OAuth2PasswordRequestForm).
 * Stores the JWT access token in localStorage under the key 'access_token'.
 */

const BASE_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')
const TOKEN_KEY = 'access_token'

// ── Token helpers ──────────────────────────────────────────────

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function isAuthenticated(): boolean {
  return !!getToken()
}

// ── Schemas ────────────────────────────────────────────────────

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface MeResponse {
  id: number
  username: string
  fullname: string
  role: string
  created_at: string | null
  updated_at: string | null
}

// ── API calls ──────────────────────────────────────────────────

/**
 * POST /api/auth/login
 * Sends username + password as application/x-www-form-urlencoded
 * (required by OAuth2PasswordRequestForm on the backend).
 * Stores the returned JWT in localStorage on success.
 */
export async function login(username: string, password: string): Promise<MeResponse> {
  const body = new URLSearchParams({ username, password })

  const res = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  })

  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new Error(data?.detail ?? `HTTP ${res.status}: Authentication failed.`)
  }

  const token: TokenResponse = await res.json()
  setToken(token.access_token)

  // Fetch and return the current user profile
  return getMe()
}

/**
 * GET /api/auth/me
 * Validates the stored token and returns the current user.
 * Throws if the token is missing or invalid (clears it automatically).
 */
export async function getMe(): Promise<MeResponse> {
  const token = getToken()
  if (!token) throw new Error('Not authenticated.')

  const res = await fetch(`${BASE_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (!res.ok) {
    clearToken()
    throw new Error('Session expired. Please log in again.')
  }

  return res.json() as Promise<MeResponse>
}

/**
 * POST /api/auth/logout
 * Notifies the backend and clears the local token.
 */
export async function logout(): Promise<void> {
  const token = getToken()
  if (token) {
    await fetch(`${BASE_URL}/api/auth/logout`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    }).catch(() => {/* ignore network errors on logout */})
  }
  clearToken()
}
