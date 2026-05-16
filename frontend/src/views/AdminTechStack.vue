<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '../components/AdminLayout.vue'
import {
  fetchTechStacks,
  createTechStack,
  updateTechStack,
  deleteTechStack as apiDeleteTechStack,
  type TechStackOut,
} from '../services/techStackService'

// ── State ─────────────────────────────────────────────────────
const search = ref('')
const category = ref('ALL_CATEGORIES')
const techStacks = ref<TechStackOut[]>([])
const isLoading = ref(false)
const apiError = ref('')

// ── Pagination ──────────────────────────────────────────────
const currentPage = ref(1)
const itemsPerPage = ref(10)

const totalPages = computed(() => Math.ceil(filtered.value.length / itemsPerPage.value) || 1)

const paginatedTech = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filtered.value.slice(start, end)
})

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

function goToPage(p: number) {
  currentPage.value = p
}

// ── Helpers ───────────────────────────────────────────────────
function formatDate(iso: string | null): string {
  if (!iso) return '—'
  return new Date(iso).toISOString().slice(0, 10)
}

const categoryBadge: Record<string, string> = {
  RUNTIME: 'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  DATABASE: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  CACHE: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  ORCHESTRATION: 'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  FRAMEWORK: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  STYLING: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  INFRASTRUCTURE: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  LANGUAGE: 'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  DEVOPS: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
}

function getBadgeClass(cat: string): string {
  const c = cat.toUpperCase()
  const base = categoryBadge[c] || 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30'
  return base
    .replace(/text-\[#[0-9a-f]+\]/, 'text-[var(--primary-bright)]')
    .replace(/border-\[#[0-9a-f\/]+\]/, 'border-[var(--primary-bright)]/30')
    .replace(/bg-\[#[0-9a-f\/]+\]/, 'bg-[var(--primary-bright)]/10')
}

// Derive unique categories from live data for the filter dropdown
const categories = computed(() => {
  const cats = new Set(techStacks.value.map(t => t.category.toUpperCase()))
  return ['ALL_CATEGORIES', ...Array.from(cats).sort()]
})

const filtered = computed(() =>
  techStacks.value.filter(t => {
    const matchCat = category.value === 'ALL_CATEGORIES' || t.category.toUpperCase() === category.value
    const q = search.value.toLowerCase()
    const matchSearch = (t.name?.toLowerCase() || '').includes(q) ||
      (t.category?.toLowerCase() || '').includes(q)
    return matchCat && matchSearch
  })
)

// ── Load on mount ─────────────────────────────────────────────
async function loadTechStacks() {
  isLoading.value = true
  apiError.value = ''
  try {
    techStacks.value = await fetchTechStacks()
  } catch (err: unknown) {
    apiError.value = err instanceof Error ? err.message : 'Failed to load tech stacks.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadTechStacks)

// ── Register dialog ───────────────────────────────────────────
const showRegisterDialog = ref(false)
const registerLoading = ref(false)
const registerError = ref('')
const registerForm = ref({ name: '', category: '', logo_url: '', sort_order: 0 })

function openRegisterDialog() {
  registerForm.value = { name: '', category: '', logo_url: '', sort_order: 0 }
  registerError.value = ''
  showRegisterDialog.value = true
}

function closeRegisterDialog() {
  showRegisterDialog.value = false
}

async function submitRegister() {
  registerLoading.value = true
  registerError.value = ''
  try {
    const payload = {
      name: registerForm.value.name,
      category: registerForm.value.category.toUpperCase(),
      logo_url: registerForm.value.logo_url || null,
      sort_order: registerForm.value.sort_order,
    }
    const created = await createTechStack(payload)
    techStacks.value.push(created)
    closeRegisterDialog()
  } catch (err: unknown) {
    registerError.value = err instanceof Error ? err.message : 'Failed to register tech stack.'
  } finally {
    registerLoading.value = false
  }
}

// ── Manage dialog ─────────────────────────────────────────────
const showManageTechDialog = ref(false)
const manageLoading = ref(false)
const manageError = ref('')
const selectedTechId = ref<number | null>(null)
const manageTechForm = ref({ name: '', category: '', logo_url: '', sort_order: 0 })

function openManageTechDialog(t: TechStackOut) {
  selectedTechId.value = t.id
  manageTechForm.value = {
    name: t.name,
    category: t.category,
    logo_url: t.logo_url || '',
    sort_order: t.sort_order,
  }
  manageError.value = ''
  showManageTechDialog.value = true
}

function closeManageTechDialog() {
  showManageTechDialog.value = false
}

async function submitManageTech() {
  if (selectedTechId.value === null) return
  manageLoading.value = true
  manageError.value = ''
  try {
    const payload = {
      name: manageTechForm.value.name,
      category: manageTechForm.value.category.toUpperCase(),
      logo_url: manageTechForm.value.logo_url || null,
      sort_order: manageTechForm.value.sort_order,
    }
    const updated = await updateTechStack(selectedTechId.value, payload)
    const idx = techStacks.value.findIndex(t => t.id === selectedTechId.value)
    if (idx !== -1) techStacks.value[idx] = updated
    closeManageTechDialog()
  } catch (err: unknown) {
    manageError.value = err instanceof Error ? err.message : 'Failed to update tech stack.'
  } finally {
    manageLoading.value = false
  }
}

async function deleteTech() {
  if (selectedTechId.value === null) return
  manageLoading.value = true
  manageError.value = ''
  try {
    await apiDeleteTechStack(selectedTechId.value)
    techStacks.value = techStacks.value.filter(t => t.id !== selectedTechId.value)
    closeManageTechDialog()
  } catch (err: unknown) {
    manageError.value = err instanceof Error ? err.message : 'Failed to delete tech stack.'
  } finally {
    manageLoading.value = false
  }
}
</script>

<template>
  <AdminLayout page-title="TechStack Registry">
    <div class="space-y-8">

      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div class="space-y-1">
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]"
            style="font-family:'JetBrains Mono',monospace;">// INVENTORY_INDEX</p>
          <h2 class="text-3xl font-bold tracking-tight text-[var(--on-surface)]">Registry Overview</h2>
          <p class="text-[var(--on-surface-variant)] text-sm max-w-xl">Centrally managed library of all technologies,
            frameworks, and infrastructure components currently deployed across the system architecture.</p>
        </div>
        <div class="flex gap-2 shrink-0">
          <button
            class="flex items-center gap-2 bg-[var(--surface)] border border-[var(--outline)] text-[var(--on-surface)] text-[11px] font-semibold tracking-widest uppercase px-4 py-2 hover:bg-[var(--surface-variant)] transition-colors"
            style="font-family:'JetBrains Mono',monospace;">
            <span class="material-symbols-outlined text-[18px]">download</span> EXPORT_CSV
          </button>
          <button @click="openRegisterDialog"
            class="flex items-center gap-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase px-4 py-2 hover:bg-[var(--primary-bright)] transition-colors"
            style="font-family:'JetBrains Mono',monospace;">
            <span class="material-symbols-outlined text-[18px]">add</span> REGISTER_NEW
          </button>
        </div>
      </div>

      <!-- Table -->
      <section class="bg-[var(--surface)] border border-[var(--outline)] overflow-hidden">

        <!-- Filter bar -->
        <div
          class="p-4 border-b border-[var(--outline)] flex flex-wrap items-center justify-between gap-4 bg-[var(--surface-low)]">
          <div class="flex gap-3">
            <!-- Category filter -->
            <div class="relative">
              <span
                class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-[var(--on-surface-variant)] text-[18px]">filter_list</span>
              <select v-model="category"
                class="bg-[var(--surface-variant)]/50 border border-[var(--outline)] text-[var(--on-surface)] text-[11px] pl-9 pr-6 py-1.5 focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                style="font-family:'JetBrains Mono',monospace;">
                <option v-for="cat in categories" :key="cat">{{ cat }}</option>
              </select>
            </div>
            <!-- Search -->
            <div class="relative">
              <span
                class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-[var(--on-surface-variant)] text-[18px]">search</span>
              <input v-model="search" type="text" placeholder="SEARCH_REGISTRY..."
                class="bg-[var(--surface-variant)]/50 border border-[var(--outline)] text-[var(--on-surface)] text-[11px] pl-9 pr-4 py-1.5 focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                style="font-family:'JetBrains Mono',monospace;" />
            </div>
          </div>
          <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
            style="font-family:'JetBrains Mono',monospace;">SHOWING {{ filtered.length }}-OF-{{ techStacks.length }}
            ENTRIES</p>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-[var(--surface-variant)]/40 border-b border-[var(--outline)]">
              <tr class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                <th class="px-6 py-4">ID</th>
                <th class="px-6 py-4">NAME</th>
                <th class="px-6 py-4">CATEGORY</th>
                <th class="px-6 py-4">ICON</th>
                <th class="px-6 py-4">CREATED_AT</th>
                <th class="px-6 py-4">UPDATED_AT</th>
                <th class="px-6 py-4 text-right">ACTION</th>
              </tr>
            </thead>
            <tbody>
              <!-- Loading row -->
              <tr v-if="isLoading">
                <td colspan="6" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">LOADING...</td>
              </tr>
              <!-- Error row -->
              <tr v-else-if="apiError">
                <td colspan="6" class="px-6 py-8 text-center text-[12px] text-[#fc7c78]"
                  style="font-family:'JetBrains Mono',monospace;">ERR: {{ apiError }}</td>
              </tr>
              <!-- Data rows -->
              <template v-else>
                <tr v-for="t in paginatedTech" :key="t.id"
                  class="hover:bg-[var(--surface-variant)]/30 transition-colors border-b border-[var(--outline)]/30 text-[12px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">
                  <td class="px-6 py-4 text-[var(--on-surface-variant)]">#TS-{{ String(t.id).padStart(3, '0') }}</td>
                  <td class="px-6 py-4 font-semibold text-[var(--on-surface)]">{{ t.name }}</td>
                  <td class="px-6 py-4">
                    <span
                      :class="['px-2 py-0.5 border text-[10px] font-semibold tracking-widest uppercase', getBadgeClass(t.category)]">{{
                        t.category }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <img v-if="t.logo_url" :src="t.logo_url || undefined" alt="" class="h-8 w-8 object-contain">
                    <span v-else
                      class="material-symbols-outlined text-[20px] text-[var(--on-surface-variant)]">code</span>
                  </td>
                  <td class="px-6 py-4">{{ formatDate(t.created_at) }}</td>
                  <td class="px-6 py-4">{{ formatDate(t.updated_at) }}</td>
                  <td class="px-6 py-4 text-right">
                    <button @click="openManageTechDialog(t)"
                      class="text-[var(--primary-bright)] hover:underline font-semibold tracking-widest uppercase text-[10px]"
                      style="font-family:'JetBrains Mono',monospace;">MANAGE</button>
                  </td>
                </tr>
                <!-- Empty state -->
                <tr v-if="filtered.length === 0">
                  <td colspan="6" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]"
                    style="font-family:'JetBrains Mono',monospace;">NO_RESULTS_FOUND</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="filtered.length > 0" class="p-4 border-t border-[var(--outline)] flex items-center gap-2">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] text-[10px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] disabled:opacity-30 transition-colors"
            style="font-family:'JetBrains Mono',monospace;">PREV</button>
          
          <button
            v-for="p in totalPages"
            :key="p"
            @click="goToPage(p)"
            :class="[
              'px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] text-[10px] font-semibold tracking-widest uppercase transition-colors',
              currentPage === p ? 'bg-[var(--primary-bright)]/20 border-[var(--primary-bright)]' : 'hover:bg-[var(--surface-variant)]'
            ]"
            style="font-family:'JetBrains Mono',monospace;">{{ p }}</button>

          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] text-[10px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] disabled:opacity-30 transition-colors"
            style="font-family:'JetBrains Mono',monospace;">NEXT</button>
        </div>
      </section>

    </div>

    <!-- ── Manage TechStack Dialog ─────────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div v-if="showManageTechDialog" class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeManageTechDialog">
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
          <div class="relative z-10 w-full max-w-md bg-[var(--surface)] border border-[var(--outline)] shadow-2xl">

            <!-- Dialog header -->
            <div
              class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]"
                  style="font-family:'JetBrains Mono',monospace;">// MANAGE_TECH_ENTRY</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5"
                  style="font-family:'JetBrains Mono',monospace;">#TS-{{ String(selectedTechId || 0).padStart(3, '0') }}
                  —
                  {{ manageTechForm.name }}</h3>
              </div>
              <button @click="closeManageTechDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitManageTech" class="p-6 space-y-4">

              <!-- Name -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">NAME</label>
                <input v-model="manageTechForm.name" type="text" required
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Category -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">CATEGORY</label>
                <input v-model="manageTechForm.category" type="text" required placeholder="e.g. FRAMEWORK"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Logo URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">LOGO URL</label>
                <input v-model="manageTechForm.logo_url" type="url" placeholder="https://cdn.example.com/logo.svg"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Sort Order -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">SORT ORDER</label>
                <input v-model.number="manageTechForm.sort_order" type="number" min="0"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Inline error -->
              <p v-if="manageError" class="text-[11px] text-[#fc7c78] font-semibold tracking-widest"
                style="font-family:'JetBrains Mono',monospace;">ERR: {{ manageError }}</p>

              <!-- Actions -->
              <div class="flex items-center justify-between pt-2">
                <!-- Delete -->
                <button type="button" @click="deleteTech" :disabled="manageLoading"
                  class="flex items-center gap-1.5 px-4 py-2 border border-[#fc7c78]/40 text-[#fc7c78] text-[11px] font-semibold tracking-widest uppercase hover:bg-[#fc7c78]/10 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  style="font-family:'JetBrains Mono',monospace;">
                  <span class="material-symbols-outlined text-[16px]">delete</span>{{ manageLoading ? 'DELETING...' :
                    'DELETE' }}
                </button>
                <div class="flex gap-3">
                  <button type="button" @click="closeManageTechDialog"
                    class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;">CANCEL</button>
                  <button type="submit" :disabled="manageLoading"
                    class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                    style="font-family:'JetBrains Mono',monospace;">{{ manageLoading ? 'SAVING...' : 'SAVE_CHANGES'
                    }}</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ── Register TechStack Dialog ───────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div v-if="showRegisterDialog" class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeRegisterDialog">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

          <!-- Panel -->
          <div class="relative z-10 w-full max-w-md bg-[var(--surface)] border border-[var(--outline)] shadow-2xl">

            <!-- Dialog header -->
            <div
              class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]"
                  style="font-family:'JetBrains Mono',monospace;">// REGISTER_NEW_TECH</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5"
                  style="font-family:'JetBrains Mono',monospace;">Add to Registry</h3>
              </div>
              <button @click="closeRegisterDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitRegister" class="p-6 space-y-4">

              <!-- Name -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">NAME</label>
                <input v-model="registerForm.name" type="text" required placeholder="e.g. FastAPI"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Category -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">CATEGORY</label>
                <input v-model="registerForm.category" type="text" required placeholder="e.g. FRAMEWORK"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Logo URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">LOGO URL</label>
                <input v-model="registerForm.logo_url" type="url" placeholder="https://cdn.example.com/logo.svg"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Sort Order -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">SORT ORDER</label>
                <input v-model.number="registerForm.sort_order" type="number" min="0"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Actions -->
              <div class="flex justify-end gap-3 pt-2">
                <!-- Inline error -->
                <p v-if="registerError" class="text-[11px] text-[#fc7c78] font-semibold tracking-widest mr-auto"
                  style="font-family:'JetBrains Mono',monospace;">ERR: {{ registerError }}</p>
                <button type="button" @click="closeRegisterDialog"
                  class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;">CANCEL</button>
                <button type="submit" :disabled="registerLoading"
                  class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  style="font-family:'JetBrains Mono',monospace;">{{ registerLoading ? 'REGISTERING...' : 'REGISTER'
                  }}</button>
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
