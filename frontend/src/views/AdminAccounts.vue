<script setup lang="ts">
import { ref, computed } from 'vue'
import AdminLayout from '../components/AdminLayout.vue'

const search = ref('')

const accounts = [
  { username: 'admin_root',    fullname: 'System Administrator', role: 'ROOT_ADMIN', created: '2023-11-12' },
  { username: 'dev_lead_01',   fullname: 'Marcus Sterling',      role: 'DEVELOPER',  created: '2024-01-05' },
  { username: 'analyst_beta',  fullname: 'Elena Rodriguez',      role: 'VIEWER',     created: '2024-03-20' },
  { username: 'sec_ops_audit', fullname: 'Sarah Jenkins',        role: 'AUDITOR',    created: '2024-05-15' },
]

const roleBadge: Record<string, string> = {
  ROOT_ADMIN: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
  DEVELOPER:  'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  VIEWER:     'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  AUDITOR:    'text-[#ffb3af] border-[#ffb3af]/20 bg-[#ffb3af]/10',
}

const filtered = computed(() =>
  accounts.filter(a =>
    a.username.includes(search.value.toLowerCase()) ||
    a.fullname.toLowerCase().includes(search.value.toLowerCase())
  )
)
</script>

<template>
  <AdminLayout page-title="Account Management">
    <section class="bg-[var(--surface)] border border-[var(--outline)] overflow-hidden">

      <!-- Header -->
      <div class="p-6 border-b border-[var(--outline)] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface)]" style="font-family:'JetBrains Mono',monospace;">// USER_DIRECTORY</h2>
          <p class="text-[10px] font-semibold tracking-widest text-[var(--on-surface-variant)] italic mt-0.5" style="font-family:'JetBrains Mono',monospace;">Listing all active system accounts and permissions</p>
        </div>
        <div class="flex items-center gap-3 w-full md:w-auto">
          <!-- Search -->
          <div class="relative flex-grow">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[var(--on-surface-variant)] text-[18px]">search</span>
            <input
              v-model="search"
              type="text"
              placeholder="Filter users..."
              class="w-full md:w-64 bg-[var(--background)] border border-[var(--outline)] text-[var(--on-surface)] pl-9 pr-4 py-2 text-[12px] focus:outline-none focus:border-[var(--primary-bright)] transition-colors placeholder-[var(--outline)]"
              style="font-family:'JetBrains Mono',monospace;"
            />
          </div>
          <!-- Create -->
          <button class="flex items-center gap-2 bg-[var(--primary)] text-[var(--on-primary)] font-semibold tracking-widest uppercase text-[11px] px-4 py-2 hover:bg-[var(--primary-bright)] transition-colors whitespace-nowrap" style="font-family:'JetBrains Mono',monospace;">
            <span class="material-symbols-outlined text-[18px]">person_add</span> CREATE_NEW
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-[var(--surface-variant)]/40">
            <tr class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] border-b border-[var(--outline)]" style="font-family:'JetBrains Mono',monospace;">
              <th class="px-6 py-4">USERNAME</th>
              <th class="px-6 py-4">FULLNAME</th>
              <th class="px-6 py-4">ROLE</th>
              <th class="px-6 py-4">CREATED AT</th>
              <th class="px-6 py-4 text-right">ACTION</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="a in filtered"
              :key="a.username"
              class="hover:bg-[var(--surface-variant)]/30 transition-colors border-b border-[var(--outline)]/30 text-[12px] text-[var(--on-surface-variant)]"
              style="font-family:'JetBrains Mono',monospace;"
            >
              <td class="px-6 py-4 font-semibold text-[var(--on-surface)]">{{ a.username }}</td>
              <td class="px-6 py-4">{{ a.fullname }}</td>
              <td class="px-6 py-4">
                <span :class="['px-2 py-0.5 border text-[10px] font-semibold tracking-widest uppercase', roleBadge[a.role].replace(/text-\[#[0-9a-f]+\]/, 'text-[var(--tertiary)]').replace(/border-\[#[0-9a-f\/]+\]/, 'border-[var(--tertiary)]/30').replace(/bg-\[#[0-9a-f\/]+\]/, 'bg-[var(--tertiary)]/10')]">{{ a.role }}</span>
              </td>
              <td class="px-6 py-4">{{ a.created }}</td>
              <td class="px-6 py-4 text-right">
                <button class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)] hover:underline underline-offset-4" style="font-family:'JetBrains Mono',monospace;">MANAGE</button>
              </td>
            </tr>
            <tr v-if="filtered.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-[12px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">NO_RESULTS_FOUND</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination footer -->
      <div class="p-4 border-t border-[var(--outline)] bg-[var(--surface-variant)]/10 flex justify-between items-center">
        <p class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">SHOWING 1-{{ filtered.length }} OF 42 USERS</p>
        <div class="flex gap-2">
          <button class="p-1 text-[var(--on-surface-variant)] hover:text-[var(--primary-bright)] transition-colors disabled:opacity-30" disabled>
            <span class="material-symbols-outlined">chevron_left</span>
          </button>
          <button class="p-1 text-[var(--on-surface-variant)] hover:text-[var(--primary-bright)] transition-colors">
            <span class="material-symbols-outlined">chevron_right</span>
          </button>
        </div>
      </div>

    </section>
  </AdminLayout>
</template>
