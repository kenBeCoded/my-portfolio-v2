/**
 * projectService.ts
 * Typed API service for Project CRUD — maps to /api/projects endpoints.
 */

import type { TechStackOut } from './techStackService'

const BASE_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

/** Shape returned by the backend (ProjectOut schema). */
export interface ProjectOut {
  id: number
  title: string
  description: string | null
  repo_url: string | null
  live_url: string | null
  status: string
  sort_order: number
  featured: boolean
  is_deleted: boolean
  techstacks: TechStackOut[]
  updated_at: string | null
  created_at: string | null
}

export interface ProjectCreatePayload {
  title: string
  description?: string | null
  repo_url?: string | null
  live_url?: string | null
  status?: string
  sort_order?: number
  featured?: boolean
  techstack_ids?: number[]
}

export interface ProjectUpdatePayload {
  title?: string
  description?: string | null
  repo_url?: string | null
  live_url?: string | null
  status?: string
  sort_order?: number
  featured?: boolean
  techstack_ids?: number[]
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

/** GET /api/projects/ — list all entries */
export async function fetchProjects(includeAll = false): Promise<ProjectOut[]> {
  const url = new URL(`${BASE_URL}/api/projects/`)
  if (includeAll) {
    url.searchParams.append('include_all', 'true')
  }
  const res = await fetch(url.toString(), {
    headers: authHeaders(),
  })
  return handleResponse<ProjectOut[]>(res)
}

/** POST /api/projects/ — create a new project */
export async function createProject(payload: ProjectCreatePayload): Promise<ProjectOut> {
  const res = await fetch(`${BASE_URL}/api/projects/`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  return handleResponse<ProjectOut>(res)
}

/** PUT /api/projects/{id} — update an existing project */
export async function updateProject(id: number, payload: ProjectUpdatePayload): Promise<ProjectOut> {
  const res = await fetch(`${BASE_URL}/api/projects/${id}`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  return handleResponse<ProjectOut>(res)
}

/** DELETE /api/projects/{id} — remove a project */
export async function deleteProjectApi(id: number): Promise<unknown> {
  const res = await fetch(`${BASE_URL}/api/projects/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
  })
  return handleResponse<unknown>(res)
}
