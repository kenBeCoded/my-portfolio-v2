<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import AdminLayout from '../components/AdminLayout.vue'

const isDark = inject('isDark', ref(true))


const search = ref('')
const category = ref('ALL_CATEGORIES')

const techStack = [
  { id: '#TS-001', name: 'Node.js',      category: 'RUNTIME',        icon: 'javascript', iconColor: '#4edea3',  created: '2023-11-04', updated: '2024-05-12' },
  { id: '#TS-002', name: 'PostgreSQL',   category: 'DATABASE',       icon: 'database',   iconColor: '#c2c4e3',  created: '2023-11-04', updated: '2024-05-20' },
  { id: '#TS-003', name: 'Redis',        category: 'CACHE',          icon: 'memory',     iconColor: '#ffb3af',  created: '2023-11-15', updated: '2024-04-01' },
  { id: '#TS-004', name: 'Kubernetes',   category: 'ORCHESTRATION',  icon: 'hub',        iconColor: '#4edea3',  created: '2023-12-01', updated: '2024-05-22' },
  { id: '#TS-005', name: 'Vue 3',        category: 'FRAMEWORK',      icon: 'token',      iconColor: '#c2c4e3',  created: '2023-11-04', updated: '2024-05-15' },
  { id: '#TS-006', name: 'Tailwind CSS', category: 'STYLING',        icon: 'palette',    iconColor: '#ffb3af',  created: '2023-11-04', updated: '2024-05-10' },
  { id: '#TS-007', name: 'FastAPI',      category: 'FRAMEWORK',      icon: 'bolt',       iconColor: '#4edea3',  created: '2024-01-10', updated: '2024-05-18' },
  { id: '#TS-008', name: 'Docker',       category: 'INFRASTRUCTURE', icon: 'inventory_2',iconColor: '#c2c4e3',  created: '2023-11-20', updated: '2024-05-05' },
]

const categories = ['ALL_CATEGORIES', 'RUNTIME', 'DATABASE', 'CACHE', 'ORCHESTRATION', 'FRAMEWORK', 'STYLING', 'INFRASTRUCTURE']

const categoryBadge: Record<string, string> = {
  RUNTIME:        'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  DATABASE:       'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  CACHE:          'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  ORCHESTRATION:  'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  FRAMEWORK:      'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  STYLING:        'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  INFRASTRUCTURE: 'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
}

const filtered = computed(() =>
  techStack.filter(t => {
    const matchCat = category.value === 'ALL_CATEGORIES' || t.category === category.value
    const matchSearch = t.name.toLowerCase().includes(search.value.toLowerCase()) || t.id.includes(search.value)
    return matchCat && matchSearch
  })
)

// ── Dialog state ─────────────────────────────────────────────
const showRegisterDialog = ref(false)
const registerForm = ref({ name: '', category: '', logo_url: '', sort_order: 0 })

function openRegisterDialog() {
  registerForm.value = { name: '', category: '', logo_url: '', sort_order: 0 }
  showRegisterDialog.value = true
}

function closeRegisterDialog() {
  showRegisterDialog.value = false
}

function submitRegister() {
  // TODO: wire up to API
  console.log('Register tech:', registerForm.value)
  closeRegisterDialog()
}
</script>

<template>
  <AdminLayout page-title="TechStack Registry">
    <div class="space-y-8">

      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div class="space-y-1">
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">// INVENTORY_INDEX</p>
          <h2 class="text-3xl font-bold tracking-tight text-[var(--on-surface)]">Registry Overview</h2>
          <p class="text-[var(--on-surface-variant)] text-sm max-w-xl">Centrally managed library of all technologies, frameworks, and infrastructure components currently deployed across the system architecture.</p>
        </div>
        <div class="flex gap-2 shrink-0">
          <button class="flex items-center gap-2 bg-[var(--surface)] border border-[var(--outline)] text-[var(--on-surface)] text-[11px] font-semibold tracking-widest uppercase px-4 py-2 hover:bg-[var(--surface-variant)] transition-colors" style="font-family:'JetBrains Mono',monospace;">
            <span class="material-symbols-outlined text-[18px]">download</span> EXPORT_CSV
          </button>
          <button
            @click="openRegisterDialog"
            class="flex items-center gap-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase px-4 py-2 hover:bg-[var(--primary-bright)] transition-colors"
            style="font-family:'JetBrains Mono',monospace;"
          >
            <span class="material-symbols-outlined text-[18px]">add</span> REGISTER_NEW
          </button>
        </div>
      </div>

      <!-- Table -->
      <section class="bg-[var(--surface)] border border-[var(--outline)] overflow-hidden">

        <!-- Filter bar -->
        <div class="p-4 border-b border-[var(--outline)] flex flex-wrap items-center justify-between gap-4 bg-[var(--surface-low)]">
          <div class="flex gap-3">
            <!-- Category filter -->
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-[var(--on-surface-variant)] text-[18px]">filter_list</span>
              <select
                v-model="category"
                class="bg-[var(--surface-variant)]/50 border border-[var(--outline)] text-[var(--on-surface)] text-[11px] pl-9 pr-6 py-1.5 focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                style="font-family:'JetBrains Mono',monospace;"
              >
                <option v-for="cat in categories" :key="cat">{{ cat }}</option>
              </select>
            </div>
            <!-- Search -->
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-[var(--on-surface-variant)] text-[18px]">search</span>
              <input
                v-model="search"
                type="text"
                placeholder="SEARCH_REGISTRY..."
                class="bg-[var(--surface-variant)]/50 border border-[var(--outline)] text-[var(--on-surface)] text-[11px] pl-9 pr-4 py-1.5 focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                style="font-family:'JetBrains Mono',monospace;"
              />
            </div>
          </div>
          <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">SHOWING {{ filtered.length }}-OF-{{ techStack.length }} ENTRIES</p>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-[var(--surface-variant)]/40 border-b border-[var(--outline)]">
              <tr class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
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
              <tr
                v-for="t in filtered"
                :key="t.id"
                class="hover:bg-[var(--surface-variant)]/30 transition-colors border-b border-[var(--outline)]/30 text-[12px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;"
              >
                <td class="px-6 py-4">{{ t.id }}</td>
                <td class="px-6 py-4 font-semibold text-[var(--on-surface)]">{{ t.name }}</td>
                <td class="px-6 py-4">
                  <span :class="['px-2 py-0.5 border text-[10px] font-semibold tracking-widest uppercase', categoryBadge[t.category].replace(/text-\[#[0-9a-f]+\]/, 'text-[var(--primary-bright)]').replace(/border-\[#[0-9a-f\/]+\]/, 'border-[var(--primary-bright)]/30').replace(/bg-\[#[0-9a-f\/]+\]/, 'bg-[var(--primary-bright)]/10')]">{{ t.category }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="material-symbols-outlined text-[20px]" :style="{ color: isDark ? t.iconColor : 'var(--primary-bright)' }">{{ t.icon }}</span>
                </td>
                <td class="px-6 py-4">{{ t.created }}</td>
                <td class="px-6 py-4">{{ t.updated }}</td>
                <td class="px-6 py-4 text-right">
                  <button class="text-[var(--primary-bright)] hover:underline font-semibold tracking-widest uppercase text-[10px]" style="font-family:'JetBrains Mono',monospace;">MANAGE</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="p-4 border-t border-[var(--outline)] flex items-center gap-2">
          <button class="px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] text-[10px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] disabled:opacity-30 transition-colors" disabled style="font-family:'JetBrains Mono',monospace;">PREV</button>
          <button class="px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] bg-[var(--primary-bright)]/20 text-[10px] font-semibold tracking-widest uppercase" style="font-family:'JetBrains Mono',monospace;">1</button>
          <button class="px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] text-[10px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors" style="font-family:'JetBrains Mono',monospace;">2</button>
          <button class="px-3 py-1 border border-[var(--outline)] text-[var(--on-surface)] text-[10px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors" style="font-family:'JetBrains Mono',monospace;">NEXT</button>
        </div>
      </section>

    </div>

    <!-- ── Register TechStack Dialog ───────────────────────── -->
    <Teleport to="body">
      <Transition name="dialog-fade">
        <div
          v-if="showRegisterDialog"
          class="fixed inset-0 z-50 flex items-center justify-center"
          @click.self="closeRegisterDialog"
        >
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

          <!-- Panel -->
          <div class="relative z-10 w-full max-w-md bg-[var(--surface)] border border-[var(--outline)] shadow-2xl">

            <!-- Dialog header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--outline)] bg-[var(--surface-variant)]/30">
              <div>
                <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">// REGISTER_NEW_TECH</p>
                <h3 class="text-[var(--on-surface)] font-bold text-sm mt-0.5" style="font-family:'JetBrains Mono',monospace;">Add to Registry</h3>
              </div>
              <button
                @click="closeRegisterDialog"
                class="text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors"
              >
                <span class="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <!-- Dialog body -->
            <form @submit.prevent="submitRegister" class="p-6 space-y-4">

              <!-- Name -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">NAME</label>
                <input
                  v-model="registerForm.name"
                  type="text"
                  required
                  placeholder="e.g. FastAPI"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Category -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">CATEGORY</label>
                <input
                  v-model="registerForm.category"
                  type="text"
                  required
                  placeholder="e.g. FRAMEWORK"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Logo URL -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">LOGO URL</label>
                <input
                  v-model="registerForm.logo_url"
                  type="url"
                  placeholder="https://cdn.example.com/logo.svg"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Sort Order -->
              <div class="space-y-1">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">SORT ORDER</label>
                <input
                  v-model.number="registerForm.sort_order"
                  type="number"
                  min="0"
                  class="w-full bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] px-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;"
                />
              </div>

              <!-- Actions -->
              <div class="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  @click="closeRegisterDialog"
                  class="px-4 py-2 border border-[var(--outline)] text-[var(--on-surface-variant)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--surface-variant)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;"
                >CANCEL</button>
                <button
                  type="submit"
                  class="px-4 py-2 bg-[var(--primary)] text-[var(--on-primary)] text-[11px] font-semibold tracking-widest uppercase hover:bg-[var(--primary-bright)] transition-colors"
                  style="font-family:'JetBrains Mono',monospace;"
                >REGISTER</button>
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
