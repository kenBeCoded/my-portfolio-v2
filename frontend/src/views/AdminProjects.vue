<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '../components/AdminLayout.vue'
import { fetchTechStacks, type TechStackOut } from '../services/techStackService'
import {
  fetchProjects,
  createProject,
  updateProject,
  deleteProjectApi,
  type ProjectOut
} from '../services/projectService'

const statusStyle: Record<string, string> = {
  PRODUCTION: 'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  STAGING:    'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  DEPRECATED: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
}

// ── State (from API) ─────────────────────────────────────────
const availableTechstacks = ref<TechStackOut[]>([])
const isLoadingTechstacks = ref(false)

const projects = ref<ProjectOut[]>([])
const isLoadingProjects = ref(true)
const projectsApiError = ref('')

// ── Pagination ──────────────────────────────────────────────
const currentPage = ref(1)
const itemsPerPage = ref(10)

const totalPages = computed(() => Math.ceil(projects.value.length / itemsPerPage.value) || 1)

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return projects.value.slice(start, end)
})

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

onMounted(async () => {
  isLoadingTechstacks.value = true
  isLoadingProjects.value = true
  projectsApiError.value = ''
  try {
    const [techData, projData] = await Promise.all([
      fetchTechStacks(),
      fetchProjects(true)
    ])
    availableTechstacks.value = techData
    projects.value = projData
  } catch (err) {
    projectsApiError.value = err instanceof Error ? err.message : 'Failed to load data.'
    console.error('Data load error:', err)
  } finally {
    isLoadingTechstacks.value = false
    isLoadingProjects.value = false
  }
})

// ── Dialog state ─────────────────────────────────────────────
const showNewProjectDialog = ref(false)
const selectedTechstacks = ref<number[]>([])
const newProjectForm = ref({
  title: '',
  description: '',
  repo_url: '',
  live_url: '',
  project_img_url: '',
  status: 'pending',
  sort_order: 0,
  featured: false,
})

const newProjectLoading = ref(false)
const newProjectError = ref('')

function toggleTechstack(id: number) {
  const idx = selectedTechstacks.value.indexOf(id)
  if (idx === -1) selectedTechstacks.value.push(id)
  else selectedTechstacks.value.splice(idx, 1)
}

function openNewProjectDialog() {
  newProjectForm.value = { title: '', description: '', repo_url: '', live_url: '', project_img_url: '', status: 'pending', sort_order: 0, featured: false }
  selectedTechstacks.value = []
  newProjectError.value = ''
  showNewProjectDialog.value = true
}

function closeNewProjectDialog() {
  showNewProjectDialog.value = false
}

async function submitNewProject() {
  newProjectLoading.value = true
  newProjectError.value = ''
  try {
    const payload = {
      ...newProjectForm.value,
      description: newProjectForm.value.description || null,
      repo_url: newProjectForm.value.repo_url || null,
      live_url: newProjectForm.value.live_url || null,
      project_img_url: newProjectForm.value.project_img_url || null,
      techstack_ids: selectedTechstacks.value,
    }
    const created = await createProject(payload)
    projects.value.push(created)
    closeNewProjectDialog()
  } catch (err) {
    newProjectError.value = err instanceof Error ? err.message : 'Failed to create project.'
  } finally {
    newProjectLoading.value = false
  }
}

// ── Manage Project Dialog ────────────────────────────────────
const showManageProjectDialog = ref(false)
const manageSelectedTechstacks = ref<number[]>([])
const manageProjectForm = ref({
  title: '',
  description: '',
  repo_url: '',
  live_url: '',
  project_img_url: '',
  status: 'pending',
  sort_order: 0,
  featured: false,
})

const manageSelectedProjectId = ref<number | null>(null)
const manageLoading = ref(false)
const manageError = ref('')

function toggleManageTechstack(id: number) {
  const idx = manageSelectedTechstacks.value.indexOf(id)
  if (idx === -1) manageSelectedTechstacks.value.push(id)
  else manageSelectedTechstacks.value.splice(idx, 1)
}

function openManageProjectDialog(p: ProjectOut) {
  manageSelectedProjectId.value = p.id
  manageProjectForm.value = {
    title: p.title,
    description: p.description || '',
    repo_url: p.repo_url || '',
    live_url: p.live_url || '',
    project_img_url: p.project_img_url || '',
    status: p.status,
    sort_order: p.sort_order,
    featured: p.featured,
  }
  manageSelectedTechstacks.value = p.techstacks.map(t => t.id)
  manageError.value = ''
  showManageProjectDialog.value = true
}

function closeManageProjectDialog() {
  showManageProjectDialog.value = false
}

async function submitManageProject() {
  if (manageSelectedProjectId.value === null) return
  manageLoading.value = true
  manageError.value = ''
  try {
    const payload = {
      ...manageProjectForm.value,
      description: manageProjectForm.value.description || null,
      repo_url: manageProjectForm.value.repo_url || null,
      live_url: manageProjectForm.value.live_url || null,
      project_img_url: manageProjectForm.value.project_img_url || null,
      techstack_ids: manageSelectedTechstacks.value,
    }
    const updated = await updateProject(manageSelectedProjectId.value, payload)
    const idx = projects.value.findIndex(p => p.id === updated.id)
    if (idx !== -1) projects.value[idx] = updated
    closeManageProjectDialog()
  } catch (err) {
    manageError.value = err instanceof Error ? err.message : 'Failed to update project.'
  } finally {
    manageLoading.value = false
  }
}

async function deleteProject() {
  if (manageSelectedProjectId.value === null) return
  manageLoading.value = true
  manageError.value = ''
  try {
    await deleteProjectApi(manageSelectedProjectId.value)
    projects.value = projects.value.filter(p => p.id !== manageSelectedProjectId.value)
    closeManageProjectDialog()
  } catch (err) {
    manageError.value = err instanceof Error ? err.message : 'Failed to delete project.'
  } finally {
    manageLoading.value = false
  }
}
</script>

<template>
  <AdminLayout page-title="Project Management">
    <div class="space-y-6">

      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface)]" style="font-family:'JetBrains Mono',monospace;">// REPOSITORY_INDEX</h2>
          <p class="text-[12px] text-[var(--on-surface-variant)] mt-1" style="font-family:'JetBrains Mono',monospace;">TOTAL_COUNT: {{ projects.length < 10 ? '0' + projects.length : projects.length }}_PROJECTS</p>
        </div>
        <button
          @click="openNewProjectDialog"
          class="flex items-center gap-2 bg-[var(--primary)] text-[var(--on-primary)] font-semibold tracking-widest uppercase text-[11px] px-4 py-2 hover:bg-[var(--primary-bright)] transition-colors"
          style="font-family:'JetBrains Mono',monospace;"
        >
          <span class="material-symbols-outlined text-[18px]">add</span>
          NEW_PROJECT
        </button>
      </div>

      <!-- Table -->
      <div class="bg-[var(--surface)] border border-[var(--outline)] overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-[var(--surface-variant)]/40">
              <tr class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] border-b border-[var(--outline)]" style="font-family:'JetBrains Mono',monospace;">
                <th class="px-6 py-3">TITLE</th>
                <th class="px-6 py-3">REPO URL</th>
                <th class="px-6 py-3">LIVE URL</th>
                <th class="px-6 py-3">STATUS</th>
                <th class="px-6 py-3 text-center">FEATURED</th>
                <th class="px-6 py-3 text-right">ACTION</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="isLoadingProjects">
                <td colspan="6" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">LOADING...</td>
              </tr>
              <tr v-else-if="projectsApiError">
                <td colspan="6" class="px-6 py-8 text-center text-[12px] text-[#fc7c78]" style="font-family:'JetBrains Mono',monospace;">ERR: {{ projectsApiError }}</td>
              </tr>
              <template v-else>
                <tr
                  v-for="p in paginatedProjects"
                  :key="p.id"
                  class="hover:bg-[var(--surface-variant)]/30 transition-colors border-b border-[var(--outline)]/30 text-[12px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;"
                >
                  <td class="px-6 py-4 font-bold text-[var(--on-surface)]">{{ p.title }}</td>
                  <td class="px-6 py-4">
                    <a v-if="p.repo_url" :href="p.repo_url" class="text-[var(--primary-bright)] hover:underline flex items-center gap-1" target="_blank">
                      <span class="material-symbols-outlined text-[16px]">link</span>{{ p.repo_url.replace(/^https?:\/\//, '') }}
                    </a>
                    <span v-else class="text-[var(--on-surface-variant)]">N/A</span>
                  </td>
                  <td class="px-6 py-4">
                    <a v-if="p.live_url" :href="p.live_url" class="text-[var(--primary-bright)] hover:underline flex items-center gap-1" target="_blank">
                      <span class="material-symbols-outlined text-[16px]">open_in_new</span>{{ p.live_url.replace(/^https?:\/\//, '') }}
                    </a>
                    <span v-else class="text-[var(--on-surface-variant)]">N/A</span>
                  </td>
                  <td class="px-6 py-4">
                    <span :class="['px-2 py-0.5 border text-[10px] font-semibold tracking-widest uppercase', (statusStyle[p.status.toUpperCase()] || statusStyle.STAGING).replace(/text-\[#[0-9a-f]+\]/, 'text-[var(--primary-bright)]').replace(/border-\[#[0-9a-f\/]+\]/, 'border-[var(--primary-bright)]/30').replace(/bg-\[#[0-9a-f\/]+\]/, 'bg-[var(--primary-bright)]/10')]">{{ p.status }}</span>
                  </td>
                  <td class="px-6 py-4 text-center">
                    <span v-if="p.featured" class="material-symbols-outlined text-[var(--primary-bright)] text-[20px]">check_circle</span>
                    <span v-else class="material-symbols-outlined text-[var(--on-surface-variant)]/40 text-[20px]">cancel</span>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <button @click="openManageProjectDialog(p)" class="px-3 py-1 border border-[var(--on-surface-variant)] text-[var(--on-surface)] hover:bg-[var(--surface-variant)] transition-colors text-[10px] font-semibold tracking-widest uppercase" style="font-family:'JetBrains Mono',monospace;">MANAGE</button>
                  </td>
                </tr>
                <tr v-if="projects.length === 0">
                  <td colspan="6" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">NO_PROJECTS_FOUND</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="projects.length > 0" class="p-4 border-t border-[var(--outline)] bg-[var(--surface-variant)]/10 flex justify-between items-center">
          <p class="text-[10px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
            INDEX_PAGE_{{ currentPage.toString().padStart(2, '0') }}_OF_{{ totalPages.toString().padStart(2, '0') }}
          </p>
          <div class="flex gap-2">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity disabled:opacity-20 disabled:cursor-not-allowed"
            >
              <span class="material-symbols-outlined">chevron_left</span>
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity disabled:opacity-20 disabled:cursor-not-allowed"
            >
              <span class="material-symbols-outlined">chevron_right</span>
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- ── New Project Dialog ──────────────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div
          v-if="showNewProjectDialog"
          class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeNewProjectDialog"
        >
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

          <!-- Panel -->
          <div class="relative z-10 w-full max-w-lg bg-[var(--surface)] border border-[var(--outline)] shadow-2xl max-h-[90vh] flex flex-col">

            <!-- Dialog header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30 shrink-0">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">// NEW_PROJECT</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5" style="font-family:'JetBrains Mono',monospace;">Register New Project</h3>
              </div>
              <button
                @click="closeNewProjectDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors"
              >
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitNewProject" class="p-6 space-y-4 overflow-y-auto">

              <!-- Title -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">TITLE</label>
                <input
                  v-model="newProjectForm.title"
                  type="text"
                  required
                  placeholder="e.g. My Awesome Project"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Description -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">DESCRIPTION</label>
                <textarea
                  v-model="newProjectForm.description"
                  rows="3"
                  placeholder="Brief project description..."
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)] resize-none"
                  style="font-family:'JetBrains Mono',monospace;"
                ></textarea>
              </div>

              <!-- Repo URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">REPO URL</label>
                <input
                  v-model="newProjectForm.repo_url"
                  type="url"
                  placeholder="https://github.com/..."
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Live URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">LIVE URL</label>
                <input
                  v-model="newProjectForm.live_url"
                  type="url"
                  placeholder="https://myproject.io"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Image URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">IMAGE URL</label>
                <input
                  v-model="newProjectForm.project_img_url"
                  type="url"
                  placeholder="https://example.com/image.png"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Status + Sort Order (row) -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">STATUS</label>
                  <select
                    v-model="newProjectForm.status"
                    class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;"
                  >
                    <option value="pending">PENDING</option>
                    <option value="in-progress">IN_PROGRESS</option>
                    <option value="done">DONE</option>
                  </select>
                </div>
                <div class="space-y-1">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">SORT ORDER</label>
                  <input
                    v-model.number="newProjectForm.sort_order"
                    type="number"
                    min="0"
                    class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;"
                  />
                </div>
              </div>

              <!-- Featured checkbox -->
              <div class="flex items-center gap-3 pt-1">
                <div
                  @click="newProjectForm.featured = !newProjectForm.featured"
                  :class="[
                    'w-5 h-5 border flex items-center justify-center cursor-pointer transition-colors shrink-0',
                    newProjectForm.featured
                      ? 'bg-[var(--primary)] border-[var(--primary)]'
                      : 'bg-[var(--background)] border-[var(--outline)]'
                  ]"
                >
                  <span v-if="newProjectForm.featured" class="material-symbols-outlined text-[var(--on-primary)] text-[14px]">check</span>
                </div>
                <label
                  @click="newProjectForm.featured = !newProjectForm.featured"
                  class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] cursor-pointer select-none"
                  style="font-family:'JetBrains Mono',monospace;"
                >MARK AS FEATURED</label>
              </div>

              <!-- TechStack multi-select -->
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">TECH STACK</label>
                  <span class="text-[10px] tracking-widest text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">{{ selectedTechstacks.length }}_SELECTED</span>
                </div>
                <div class="border border-[var(--outline)] bg-[var(--background)] p-3 flex flex-wrap gap-2 min-h-[56px]">
                  <p v-if="isLoadingTechstacks" class="text-[10px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">LOADING...</p>
                  <button
                    v-else
                    v-for="tech in availableTechstacks"
                    :key="tech.id"
                    type="button"
                    @click="toggleTechstack(tech.id)"
                    :class="[
                      'flex items-center gap-1.5 px-2.5 py-1 border text-[10px] font-semibold tracking-widest uppercase transition-all select-none',
                      selectedTechstacks.includes(tech.id)
                        ? 'bg-[var(--primary)] border-[var(--primary)] text-[var(--on-primary)]'
                        : 'bg-transparent border-[var(--outline)] text-[var(--on-surface-variant)] hover:border-[var(--primary-bright)] hover:text-[var(--primary-bright)]'
                    ]"
                    style="font-family:'JetBrains Mono',monospace;"
                  >
                    <span v-if="selectedTechstacks.includes(tech.id)" class="material-symbols-outlined text-[12px]">check</span>
                    {{ tech.name }}
                  </button>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex justify-end gap-3 pt-2">
                <p v-if="newProjectError" class="text-[11px] text-[#fc7c78] font-semibold tracking-widest mr-auto" style="font-family:'JetBrains Mono',monospace;">ERR: {{ newProjectError }}</p>
                <button
                  type="button"
                  @click="closeNewProjectDialog"
                  class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;"
                >CANCEL</button>
                <button
                  type="submit"
                  :disabled="newProjectLoading"
                  class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  style="font-family:'JetBrains Mono',monospace;"
                >{{ newProjectLoading ? 'CREATING...' : 'CREATE_PROJECT' }}</button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ── Manage Project Dialog ────────────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div
          v-if="showManageProjectDialog"
          class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeManageProjectDialog"
        >
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

          <!-- Panel -->
          <div class="relative z-10 w-full max-w-lg bg-[var(--surface)] border border-[var(--outline)] shadow-2xl max-h-[90vh] flex flex-col">

            <!-- Dialog header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30 shrink-0">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">// MANAGE_PROJECT</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5" style="font-family:'JetBrains Mono',monospace;">{{ manageProjectForm.title }}</h3>
              </div>
              <button
                @click="closeManageProjectDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors"
              >
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitManageProject" class="p-6 space-y-4 overflow-y-auto">

              <!-- Title -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">TITLE</label>
                <input
                  v-model="manageProjectForm.title"
                  type="text"
                  required
                  placeholder="e.g. My Awesome Project"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Description -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">DESCRIPTION</label>
                <textarea
                  v-model="manageProjectForm.description"
                  rows="3"
                  placeholder="Brief project description..."
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)] resize-none"
                  style="font-family:'JetBrains Mono',monospace;"
                ></textarea>
              </div>

              <!-- Repo URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">REPO URL</label>
                <input
                  v-model="manageProjectForm.repo_url"
                  type="url"
                  placeholder="https://github.com/..."
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Live URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">LIVE URL</label>
                <input
                  v-model="manageProjectForm.live_url"
                  type="url"
                  placeholder="https://myproject.io"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Image URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">IMAGE URL</label>
                <input
                  v-model="manageProjectForm.project_img_url"
                  type="url"
                  placeholder="https://example.com/image.png"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Status + Sort Order (row) -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">STATUS</label>
                  <select
                    v-model="manageProjectForm.status"
                    class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;"
                  >
                    <option value="pending">PENDING</option>
                    <option value="in-progress">IN_PROGRESS</option>
                    <option value="done">DONE</option>
                    <option value="production">PRODUCTION</option>
                    <option value="staging">STAGING</option>
                    <option value="deprecated">DEPRECATED</option>
                  </select>
                </div>
                <div class="space-y-1">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">SORT ORDER</label>
                  <input
                    v-model.number="manageProjectForm.sort_order"
                    type="number"
                    min="0"
                    class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;"
                  />
                </div>
              </div>

              <!-- Featured checkbox -->
              <div class="flex items-center gap-3 pt-1">
                <div
                  @click="manageProjectForm.featured = !manageProjectForm.featured"
                  :class="[
                    'w-5 h-5 border flex items-center justify-center cursor-pointer transition-colors shrink-0',
                    manageProjectForm.featured
                      ? 'bg-[var(--primary)] border-[var(--primary)]'
                      : 'bg-[var(--background)] border-[var(--outline)]'
                  ]"
                >
                  <span v-if="manageProjectForm.featured" class="material-symbols-outlined text-[var(--on-primary)] text-[14px]">check</span>
                </div>
                <label
                  @click="manageProjectForm.featured = !manageProjectForm.featured"
                  class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] cursor-pointer select-none"
                  style="font-family:'JetBrains Mono',monospace;"
                >MARK AS FEATURED</label>
              </div>

              <!-- TechStack multi-select -->
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">TECH STACK</label>
                  <span class="text-[10px] tracking-widest text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">{{ manageSelectedTechstacks.length }}_SELECTED</span>
                </div>
                <div class="border border-[var(--outline)] bg-[var(--background)] p-3 flex flex-wrap gap-2 min-h-[56px]">
                  <p v-if="isLoadingTechstacks" class="text-[10px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">LOADING...</p>
                  <button
                    v-else
                    v-for="tech in availableTechstacks"
                    :key="tech.id"
                    type="button"
                    @click="toggleManageTechstack(tech.id)"
                    :class="[
                      'flex items-center gap-1.5 px-2.5 py-1 border text-[10px] font-semibold tracking-widest uppercase transition-all select-none',
                      manageSelectedTechstacks.includes(tech.id)
                        ? 'bg-[var(--primary)] border-[var(--primary)] text-[var(--on-primary)]'
                        : 'bg-transparent border-[var(--outline)] text-[var(--on-surface-variant)] hover:border-[var(--primary-bright)] hover:text-[var(--primary-bright)]'
                    ]"
                    style="font-family:'JetBrains Mono',monospace;"
                  >
                    <span v-if="manageSelectedTechstacks.includes(tech.id)" class="material-symbols-outlined text-[12px]">check</span>
                    {{ tech.name }}
                  </button>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex items-center justify-between pt-2">
                <!-- Delete -->
                <button
                  type="button"
                  @click="deleteProject"
                  :disabled="manageLoading"
                  class="flex items-center gap-1.5 px-4 py-2 border border-[#fc7c78]/40 text-[#fc7c78] text-[11px] font-semibold tracking-widest uppercase hover:bg-[#fc7c78]/10 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  style="font-family:'JetBrains Mono',monospace;"
                >
                  <span class="material-symbols-outlined text-[16px]">delete</span>{{ manageLoading ? 'DELETING...' : 'DELETE' }}
                </button>
                <div class="flex gap-3 items-center">
                  <p v-if="manageError" class="text-[11px] text-[#fc7c78] font-semibold tracking-widest" style="font-family:'JetBrains Mono',monospace;">ERR: {{ manageError }}</p>
                  <button
                    type="button"
                    @click="closeManageProjectDialog"
                    class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;"
                  >CANCEL</button>
                  <button
                    type="submit"
                    :disabled="manageLoading"
                    class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                    style="font-family:'JetBrains Mono',monospace;"
                  >{{ manageLoading ? 'SAVING...' : 'SAVE_CHANGES' }}</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

  </AdminLayout>
</template>

<style scoped>
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.2s ease;
}
.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}
.dialog-fade-enter-active .relative,
.dialog-fade-leave-active .relative {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.dialog-fade-enter-from .relative,
.dialog-fade-leave-to .relative {
  transform: translateY(-12px);
  opacity: 0;
}
</style>
