/**
 * userService.ts
 * Typed API service for user account CRUD — maps to /api/users endpoints.
 *
 * In development the Vite proxy rewrites /api/* → http://localhost:8000/api/*
 * In production set VITE_API_URL to your backend origin (e.g. https://api.example.com).
 */

const BASE_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

/** Shape returned by the backend (UserOut schema). */
export interface UserOut {
  id: number
  username: string
  fullname: string
  role: string
  created_at: string | null
  updated_at: string | null
}

/** Body for POST /api/users/ */
export interface UserCreatePayload {
  username: string
  password: string
  fullname: string
  role: string
}

/** Body for PUT /api/users/{id} */
export interface UserUpdatePayload {
  username?: string
  password?: string
  fullname?: string
  role?: string
}

// ── Helpers ────────────────────────────────────────────────────

function authHeaders(): HeadersInit {
  const token = localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body?.detail ?? `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

// ── CRUD ───────────────────────────────────────────────────────

/** GET /api/users/ — list all accounts */
export async function fetchUsers(): Promise<UserOut[]> {
  const res = await fetch(`${BASE_URL}/api/users/`, {
    headers: authHeaders(),
  })
  return handleResponse<UserOut[]>(res)
}

/** POST /api/users/ — create a new account */
export async function createUser(payload: UserCreatePayload): Promise<UserOut> {
  const res = await fetch(`${BASE_URL}/api/users/`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  return handleResponse<UserOut>(res)
}

/** PUT /api/users/{id} — update an existing account */
export async function updateUser(id: number, payload: UserUpdatePayload): Promise<UserOut> {
  const res = await fetch(`${BASE_URL}/api/users/${id}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  return handleResponse<UserOut>(res)
}

/** DELETE /api/users/{id} — remove an account */
export async function deleteUser(id: number): Promise<{ message: string }> {
  const res = await fetch(`${BASE_URL}/api/users/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
  })
  return handleResponse<{ message: string }>(res)
}
