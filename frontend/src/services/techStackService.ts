/**
 * techStackService.ts
 * Typed API service for TechStack CRUD — maps to /api/techstacks endpoints.
 *
 * GET  /api/techstacks/       — public (no auth required)
 * POST /api/techstacks/       — protected
 * PUT  /api/techstacks/{id}   — protected
 * DELETE /api/techstacks/{id} — protected
 */

const BASE_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

/** Shape returned by the backend (TechStackOut schema). */
export interface TechStackOut {
  id: number
  name: string
  category: string
  logo_url: string | null
  sort_order: number
  created_at: string | null
  updated_at: string | null
}

/** Body for POST /api/techstacks/ */
export interface TechStackCreatePayload {
  name: string
  category: string
  logo_url?: string | null
  sort_order?: number
}

/** Body for PUT /api/techstacks/{id} */
export interface TechStackUpdatePayload {
  name?: string
  category?: string
  logo_url?: string | null
  sort_order?: number
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
    let msg = body?.detail ?? `HTTP ${res.status}`

    // FastAPI returns 422 validation errors as a list of objects
    if (Array.isArray(msg)) {
      msg = msg.map((err: any) => {
        const loc = err.loc ? err.loc.slice(1).join('.') : 'error'
        return `${loc}: ${err.msg}`
      }).join(', ')
    }

    throw new Error(msg)
  }
  return res.json() as Promise<T>
}

// ── CRUD ───────────────────────────────────────────────────────

/** GET /api/techstacks/ — list all entries (public) */
export async function fetchTechStacks(): Promise<TechStackOut[]> {
  const res = await fetch(`${BASE_URL}/api/techstacks/`, {
    headers: authHeaders(),
  })
  return handleResponse<TechStackOut[]>(res)
}

/** POST /api/techstacks/ — create a new entry (protected) */
export async function createTechStack(payload: TechStackCreatePayload): Promise<TechStackOut> {
  const res = await fetch(`${BASE_URL}/api/techstacks/`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  return handleResponse<TechStackOut>(res)
}

/** PUT /api/techstacks/{id} — update an existing entry (protected) */
export async function updateTechStack(id: number, payload: TechStackUpdatePayload): Promise<TechStackOut> {
  const res = await fetch(`${BASE_URL}/api/techstacks/${id}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  return handleResponse<TechStackOut>(res)
}

/** DELETE /api/techstacks/{id} — remove an entry (protected) */
export async function deleteTechStack(id: number): Promise<unknown> {
  const res = await fetch(`${BASE_URL}/api/techstacks/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
  })
  return handleResponse<unknown>(res)
}
