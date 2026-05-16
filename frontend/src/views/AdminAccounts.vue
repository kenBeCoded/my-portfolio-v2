<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '../components/AdminLayout.vue'
import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser as apiDeleteUser,
  type UserOut,
} from '../services/userService'

// ── State ─────────────────────────────────────────────────────
const search = ref('')
const accounts = ref<UserOut[]>([])
const isLoading = ref(false)
const apiError = ref('')

// ── Pagination ──────────────────────────────────────────────
const currentPage = ref(1)
const itemsPerPage = ref(10)

const totalPages = computed(() => Math.ceil(filtered.value.length / itemsPerPage.value) || 1)

const paginatedAccounts = computed(() => {
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



// ── Helpers ───────────────────────────────────────────────────
function formatDate(iso: string | null): string {
  if (!iso) return '—'
  return new Date(iso).toISOString().slice(0, 10)
}

const roleBadge: Record<string, string> = {
  ROOT_ADMIN: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  DEVELOPER: 'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  VIEWER: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  AUDITOR: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#ffb3af]/10',
  ADMIN: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  USER: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
}

function getBadgeClass(role: string) {
  const r = role.toUpperCase()
  const base = roleBadge[r] || 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30'
  return base
    .replace(/text-\[#[0-9a-f]+\]/, 'text-[var(--tertiary)]')
    .replace(/border-\[#[0-9a-f\/]+\]/, 'border-[var(--tertiary)]/30')
    .replace(/bg-\[#[0-9a-f\/]+\]/, 'bg-[var(--tertiary)]/10')
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return accounts.value.filter(a =>
    (a.username?.toLowerCase() || '').includes(q) ||
    (a.fullname?.toLowerCase() || '').includes(q)
  )
})

// ── Load users on mount ───────────────────────────────────────
async function loadUsers() {
  isLoading.value = true
  apiError.value = ''
  try {
    accounts.value = await fetchUsers()
  } catch (err: unknown) {
    apiError.value = err instanceof Error ? err.message : 'Failed to load users.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadUsers)

// ── Create dialog ─────────────────────────────────────────────
const showCreateDialog = ref(false)
const createLoading = ref(false)
const createError = ref('')
const createForm = ref({ username: '', password: '', fullname: '', role: 'user' })

function openCreateDialog() {
  createForm.value = { username: '', password: '', fullname: '', role: 'user' }
  createError.value = ''
  showCreateDialog.value = true
}

function closeCreateDialog() {
  showCreateDialog.value = false
}

async function submitCreateUser() {
  createLoading.value = true
  createError.value = ''
  try {
    const created = await createUser(createForm.value)
    accounts.value.push(created)
    closeCreateDialog()
  } catch (err: unknown) {
    createError.value = err instanceof Error ? err.message : 'Failed to create user.'
  } finally {
    createLoading.value = false
  }
}

// ── Manage dialog ─────────────────────────────────────────────
const showManageDialog = ref(false)
const manageLoading = ref(false)
const manageError = ref('')
const selectedUserId = ref<number | null>(null)
const manageForm = ref({ username: '', password: '', fullname: '', role: 'user' })

function openManageDialog(a: UserOut) {
  selectedUserId.value = a.id
  manageForm.value = { username: a.username, password: '', fullname: a.fullname, role: a.role.toLowerCase() }
  manageError.value = ''
  showManageDialog.value = true
}

function closeManageDialog() {
  showManageDialog.value = false
}

async function submitManageUser() {
  if (selectedUserId.value === null) return
  manageLoading.value = true
  manageError.value = ''
  try {
    const payload: Record<string, string> = {
      username: manageForm.value.username,
      fullname: manageForm.value.fullname,
      role: manageForm.value.role,
    }
    if (manageForm.value.password) {
      payload.password = manageForm.value.password
    }
    const updated = await updateUser(selectedUserId.value, payload)
    const idx = accounts.value.findIndex(a => a.id === selectedUserId.value)
    if (idx !== -1) accounts.value[idx] = updated
    closeManageDialog()
  } catch (err: unknown) {
    manageError.value = err instanceof Error ? err.message : 'Failed to update user.'
  } finally {
    manageLoading.value = false
  }
}

async function deleteUser() {
  if (selectedUserId.value === null) return
  manageLoading.value = true
  manageError.value = ''
  try {
    await apiDeleteUser(selectedUserId.value)
    accounts.value = accounts.value.filter(a => a.id !== selectedUserId.value)
    closeManageDialog()
  } catch (err: unknown) {
    manageError.value = err instanceof Error ? err.message : 'Failed to delete user.'
  } finally {
    manageLoading.value = false
  }
}
</script>

<template>
  <AdminLayout page-title="Account Management">
    <section class="bg-[var(--surface)] border border-[var(--outline)] overflow-hidden">

      <!-- Header -->
      <div
        class="p-6 border-b border-[var(--outline)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface)]"
            style="font-family:'JetBrains Mono',monospace;">// USER_DIRECTORY</h2>
          <p class="text-[10px] font-semibold tracking-widest text-[var(--on-surface-variant)] italic mt-0.5"
            style="font-family:'JetBrains Mono',monospace;">Listing all active system accounts and permissions</p>
        </div>
        <div class="flex items-center gap-3 w-full md:w-auto">
          <!-- Search -->
          <div class="relative flex-grow">
            <span
              class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[var(--on-surface-variant)] text-[18px]">search</span>
            <input v-model="search" type="text" placeholder="Filter users..."
              class="w-full md:w-64 bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] pl-9 pr-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
              style="font-family:'JetBrains Mono',monospace;" />
          </div>
          <!-- Create -->
          <button @click="openCreateDialog"
            class="flex items-center gap-2 bg-[var(--primary)] text-[var(--on-primary)] font-semibold tracking-widest uppercase text-[11px] px-4 py-2 hover:bg-[var(--primary-bright)] transition-colors whitespace-nowrap"
            style="font-family:'JetBrains Mono',monospace;">
            <span class="material-symbols-outlined text-[18px]">person_add</span> CREATE_NEW
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-[var(--surface-variant)]/40">
            <tr
              class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] border-b border-[var(--outline)]"
              style="font-family:'JetBrains Mono',monospace;">
              <th class="px-6 py-4">USERNAME</th>
              <th class="px-6 py-4">FULLNAME</th>
              <th class="px-6 py-4">ROLE</th>
              <th class="px-6 py-4">CREATED AT</th>
              <th class="px-6 py-4 text-right">ACTION</th>
            </tr>
          </thead>
          <tbody>
            <!-- Loading row -->
            <tr v-if="isLoading">
              <td colspan="5" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">LOADING...</td>
            </tr>
            <!-- Error row -->
            <tr v-else-if="apiError">
              <td colspan="5" class="px-6 py-8 text-center text-[12px] text-[#fc7c78]"
                style="font-family:'JetBrains Mono',monospace;">ERR: {{ apiError }}</td>
            </tr>
            <!-- Data rows — wrapped in template so v-else applies to a single element -->
            <template v-else>
              <tr v-for="a in paginatedAccounts" :key="a.id"
                class="hover:bg-[var(--surface-variant)]/30 transition-colors border-b border-[var(--outline)]/30 text-[12px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                <td class="px-6 py-4 font-semibold text-[var(--on-surface)]">{{ a.username }}</td>
                <td class="px-6 py-4">{{ a.fullname }}</td>
                <td class="px-6 py-4">
                  <span
                    :class="['px-2 py-0.5 border text-[10px] font-semibold tracking-widest uppercase', getBadgeClass(a.role)]">
                    {{ a.role }}
                  </span>
                </td>
                <td class="px-6 py-4">{{ formatDate(a.created_at) }}</td>
                <td class="px-6 py-4 text-right">
                  <button @click="openManageDialog(a)"
                    class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)] hover:underline underline-offset-4"
                    style="font-family:'JetBrains Mono',monospace;">MANAGE</button>
                </td>
              </tr>
              <!-- Empty state — only shows after load when no results match -->
              <tr v-if="filtered.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">NO_RESULTS_FOUND</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Pagination footer -->
      <div
        v-if="filtered.length > 0"
        class="p-4 border-t border-[var(--outline)] bg-[var(--surface-variant)]/10 flex justify-between items-center">
        <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
          style="font-family:'JetBrains Mono',monospace;">
          INDEX_PAGE_{{ currentPage.toString().padStart(2, '0') }}_OF_{{ totalPages.toString().padStart(2, '0') }}
        </p>
        <div class="flex gap-2">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="p-1 text-[var(--on-surface-variant)] hover:text-[var(--primary-bright)] transition-colors disabled:opacity-30 disabled:cursor-not-allowed">
            <span class="material-symbols-outlined">chevron_left</span>
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="p-1 text-[var(--on-surface-variant)] hover:text-[var(--primary-bright)] transition-colors disabled:opacity-30 disabled:cursor-not-allowed">
            <span class="material-symbols-outlined">chevron_right</span>
          </button>
        </div>
      </div>

    </section>

    <!-- ── Manage User Dialog ──────────────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div v-if="showManageDialog" class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeManageDialog">
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
          <div class="relative z-10 w-full max-w-md bg-[var(--surface)] border border-[var(--outline)] shadow-2xl">

            <!-- Dialog header -->
            <div
              class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]"
                  style="font-family:'JetBrains Mono',monospace;">// MANAGE_ACCOUNT</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5"
                  style="font-family:'JetBrains Mono',monospace;">{{ manageForm.username }}</h3>
              </div>
              <button @click="closeManageDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitManageUser" class="p-6 space-y-4">

              <!-- Username -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">USERNAME</label>
                <input v-model="manageForm.username" type="text" required
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Password -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">NEW PASSWORD <span
                    class="normal-case italic text-[var(--outline)]">(leave blank to keep)</span></label>
                <input v-model="manageForm.password" type="password" placeholder="••••••••"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Fullname -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">FULL NAME</label>
                <input v-model="manageForm.fullname" type="text" required
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Role -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">ROLE</label>
                <select v-model="manageForm.role"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;">
                  <option value="user">USER</option>
                  <option value="admin">ADMIN</option>
                </select>
              </div>

              <!-- Inline error -->
              <p v-if="manageError" class="text-[11px] text-[#fc7c78] font-semibold tracking-widest"
                style="font-family:'JetBrains Mono',monospace;">ERR: {{ manageError }}</p>

              <!-- Actions -->
              <div class="flex items-center justify-between pt-2">
                <!-- Delete -->
                <button type="button" :disabled="manageLoading" @click="deleteUser"
                  class="flex items-center gap-1.5 px-4 py-2 border border-[#fc7c78]/40 text-[#fc7c78] text-[11px] font-semibold tracking-widest uppercase hover:bg-[#fc7c78]/10 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  style="font-family:'JetBrains Mono',monospace;">
                  <span class="material-symbols-outlined text-[16px]">delete</span>DELETE
                </button>
                <div class="flex gap-3">
                  <button type="button" @click="closeManageDialog"
                    class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                    style="font-family:'JetBrains Mono',monospace;">CANCEL</button>
                  <button type="submit" :disabled="manageLoading"
                    class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                    style="font-family:'JetBrains Mono',monospace;">
                    {{ manageLoading ? 'SAVING...' : 'SAVE_CHANGES' }}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ── Create User Dialog ──────────────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div v-if="showCreateDialog" class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeCreateDialog">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

          <!-- Panel -->
          <div class="relative z-10 w-full max-w-md bg-[var(--surface)] border border-[var(--outline)] shadow-2xl">

            <!-- Dialog header -->
            <div
              class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]"
                  style="font-family:'JetBrains Mono',monospace;">// CREATE_NEW_ACCOUNT</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5"
                  style="font-family:'JetBrains Mono',monospace;">Register System User</h3>
              </div>
              <button @click="closeCreateDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitCreateUser" class="p-6 space-y-4">

              <!-- Username -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">USERNAME</label>
                <input v-model="createForm.username" type="text" required placeholder="e.g. dev_user_01"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Password -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">PASSWORD</label>
                <input v-model="createForm.password" type="password" required placeholder="••••••••"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Fullname -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">FULL NAME</label>
                <input v-model="createForm.fullname" type="text" required placeholder="e.g. John Doe"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;" />
              </div>

              <!-- Role -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">ROLE</label>
                <select v-model="createForm.role"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;">
                  <option value="user">USER</option>
                  <option value="admin">ADMIN</option>
                </select>
              </div>

              <!-- Inline error -->
              <p v-if="createError" class="text-[11px] text-[#fc7c78] font-semibold tracking-widest"
                style="font-family:'JetBrains Mono',monospace;">ERR: {{ createError }}</p>

              <!-- Actions -->
              <div class="flex justify-end gap-3 pt-2">
                <button type="button" @click="closeCreateDialog"
                  class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;">CANCEL</button>
                <button type="submit" :disabled="createLoading"
                  class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  style="font-family:'JetBrains Mono',monospace;">{{ createLoading ? 'CREATING...' : 'CREATE_USER'
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
