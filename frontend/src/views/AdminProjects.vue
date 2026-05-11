<script setup lang="ts">
import AdminLayout from '../components/AdminLayout.vue'

const projects = [
  { title: 'Quantum-Engine',      repo: 'github.com/org/q-engine',   live: 'q-engine.io',         status: 'PRODUCTION', featured: true  },
  { title: 'Neural-API-v2',       repo: 'github.com/org/neural-v2',  live: null,                  status: 'STAGING',    featured: false },
  { title: 'Data-Viz-Dashboard',  repo: 'github.com/org/dataviz',    live: 'analytics.main.net',  status: 'PRODUCTION', featured: true  },
  { title: 'Auth-Refactor',       repo: 'github.com/org/auth-ref',   live: null,                  status: 'DEPRECATED', featured: false },
]

const statusStyle: Record<string, string> = {
  PRODUCTION: 'text-[#4edea3] border-[#4edea3]/20 bg-[#4edea3]/10',
  STAGING:    'text-[#c2c4e3] border-[#c2c4e3]/20 bg-[#42455f]/30',
  DEPRECATED: 'text-[#ffb3af] border-[#ffb3af]/20 bg-[#fc7c78]/10',
}
</script>

<template>
  <AdminLayout page-title="Project Management">
    <div class="space-y-6">

      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface)]" style="font-family:'JetBrains Mono',monospace;">// REPOSITORY_INDEX</h2>
          <p class="text-[12px] text-[var(--on-surface-variant)] mt-1" style="font-family:'JetBrains Mono',monospace;">TOTAL_COUNT: 0{{ projects.length }}_PROJECTS</p>
        </div>
        <button class="flex items-center gap-2 bg-[var(--primary)] text-[var(--on-primary)] font-semibold tracking-widest uppercase text-[11px] px-4 py-2 hover:bg-[var(--primary-bright)] transition-colors" style="font-family:'JetBrains Mono',monospace;">
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
              <tr
                v-for="p in projects"
                :key="p.title"
                class="hover:bg-[var(--surface-variant)]/30 transition-colors border-b border-[var(--outline)]/30 text-[12px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;"
              >
                <td class="px-6 py-4 font-bold text-[var(--on-surface)]">{{ p.title }}</td>
                <td class="px-6 py-4">
                  <a href="#" class="text-[var(--primary-bright)] hover:underline flex items-center gap-1">
                    <span class="material-symbols-outlined text-[16px]">link</span>{{ p.repo }}
                  </a>
                </td>
                <td class="px-6 py-4">
                  <a v-if="p.live" href="#" class="text-[var(--primary-bright)] hover:underline flex items-center gap-1">
                    <span class="material-symbols-outlined text-[16px]">open_in_new</span>{{ p.live }}
                  </a>
                  <span v-else class="text-[var(--on-surface-variant)]">N/A</span>
                </td>
                <td class="px-6 py-4">
                  <span :class="['px-2 py-0.5 border text-[10px] font-semibold tracking-widest uppercase', statusStyle[p.status].replace(/text-\[#[0-9a-f]+\]/, 'text-[var(--primary-bright)]').replace(/border-\[#[0-9a-f\/]+\]/, 'border-[var(--primary-bright)]/30').replace(/bg-\[#[0-9a-f\/]+\]/, 'bg-[var(--primary-bright)]/10')]">{{ p.status }}</span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span v-if="p.featured" class="material-symbols-outlined text-[var(--primary-bright)] text-[20px]">check_circle</span>
                  <span v-else class="material-symbols-outlined text-[var(--on-surface-variant)]/40 text-[20px]">cancel</span>
                </td>
                <td class="px-6 py-4 text-right">
                  <button class="px-3 py-1 border border-[var(--on-surface-variant)] text-[var(--on-surface)] hover:bg-[var(--surface-variant)] transition-colors text-[10px] font-semibold tracking-widest uppercase" style="font-family:'JetBrains Mono',monospace;">MANAGE</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="p-4 border-t border-[var(--outline)] bg-[var(--surface-variant)]/10 flex justify-between items-center">
          <p class="text-[10px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">INDEX_PAGE_01_OF_02</p>
          <div class="flex gap-2">
            <button class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">chevron_left</span></button>
            <button class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">chevron_right</span></button>
          </div>
        </div>
      </div>

    </div>
  </AdminLayout>
</template>
