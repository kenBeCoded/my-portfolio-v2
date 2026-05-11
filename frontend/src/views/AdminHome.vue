<script setup lang="ts">
import AdminLayout from '../components/AdminLayout.vue'

const deployments = [
  { ts: '2024-05-23 14:22', service: 'auth-microservice', action: 'Deploy: v2.4.1',       status: 'SUCCESS' },
  { ts: '2024-05-23 12:05', service: 'api-gateway',       action: 'Patch: SSL Renewal',   status: 'SUCCESS' },
  { ts: '2024-05-23 09:45', service: 'db-backup-job',     action: 'Backup: pg_prod_01',   status: 'FAILED'  },
  { ts: '2024-05-22 23:12', service: 'analytics-worker',  action: 'Scale Up: +2 Replicas', status: 'SUCCESS' },
]
</script>

<template>
  <AdminLayout page-title="Dashboard Overview">
    <div class="space-y-10">

      <!-- ── Stats Grid ── -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">rocket_launch</span>
            <span class="text-[10px] font-semibold tracking-widest text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">LIVE</span>
          </div>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] mb-1" style="font-family:'JetBrains Mono',monospace;">Active Projects</p>
          <h3 class="text-2xl font-semibold text-[var(--on-surface)]">12</h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
            <span class="text-[var(--primary-bright)]">+2</span> this month
          </div>
        </div>

        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">timer</span>
            <span class="text-[10px] font-semibold tracking-widest text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">99.9%</span>
          </div>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] mb-1" style="font-family:'JetBrains Mono',monospace;">System Uptime</p>
          <h3 class="text-2xl font-semibold text-[var(--on-surface)]">724h 12m</h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)] text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace;">Operational</div>
        </div>

        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">api</span>
            <span class="text-[10px] font-semibold tracking-widest text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">REQUESTS</span>
          </div>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] mb-1" style="font-family:'JetBrains Mono',monospace;">Total API Calls</p>
          <h3 class="text-2xl font-semibold text-[var(--on-surface)]">1.2M</h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
            <span class="text-[var(--primary-bright)]">↑ 12%</span> vs last week
          </div>
        </div>

        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">memory</span>
            <span class="text-[10px] font-semibold tracking-widest text-[var(--tertiary)]" style="font-family:'JetBrains Mono',monospace;">STRESS_LOW</span>
          </div>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] mb-1" style="font-family:'JetBrains Mono',monospace;">Server Load</p>
          <h3 class="text-2xl font-semibold text-[var(--on-surface)]">34%</h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)]">
            <div class="h-1 w-full bg-[var(--surface-variant)] overflow-hidden">
              <div class="h-full bg-[var(--primary)]" style="width:34%;"></div>
            </div>
          </div>
        </div>

      </section>

      <!-- ── Main Panels ── -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

        <!-- Recent Deployments -->
        <section class="lg:col-span-8 bg-[var(--surface)] border border-[var(--outline)] overflow-hidden">
          <div class="p-6 border-b border-[var(--outline)] flex justify-between items-center">
            <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface)]" style="font-family:'JetBrains Mono',monospace;">// RECENT_DEPLOYMENTS</h2>
            <button class="text-[10px] font-semibold tracking-widest uppercase text-[var(--primary-bright)] hover:underline" style="font-family:'JetBrains Mono',monospace;">VIEW_ALL_LOGS</button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead class="bg-[var(--surface-variant)]/40">
                <tr class="text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
                  <th class="px-6 py-3 border-b border-[var(--outline)]">TIMESTAMP</th>
                  <th class="px-6 py-3 border-b border-[var(--outline)]">SERVICE</th>
                  <th class="px-6 py-3 border-b border-[var(--outline)]">ACTION</th>
                  <th class="px-6 py-3 border-b border-[var(--outline)] text-right">STATUS</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="d in deployments"
                  :key="d.ts"
                  class="hover:bg-[var(--surface-variant)]/30 transition-colors text-[12px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;"
                >
                  <td class="px-6 py-4 border-b border-[var(--outline)]/30">{{ d.ts }}</td>
                  <td class="px-6 py-4 border-b border-[var(--outline)]/30 text-[var(--on-surface)]">{{ d.service }}</td>
                  <td class="px-6 py-4 border-b border-[var(--outline)]/30">{{ d.action }}</td>
                  <td class="px-6 py-4 border-b border-[var(--outline)]/30 text-right">
                    <span
                      :class="d.status === 'SUCCESS'
                        ? 'px-2 py-0.5 border text-[var(--primary-bright)] border-[var(--primary-bright)]/30 bg-[var(--primary-bright)]/10'
                        : 'px-2 py-0.5 border text-[var(--error)] border-[var(--error)]/30 bg-[var(--error)]/20'"
                      class="text-[10px] font-semibold tracking-widest uppercase"
                    >{{ d.status }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Right Column -->
        <section class="lg:col-span-4 flex flex-col gap-8">

          <!-- System Health -->
          <div class="bg-[var(--surface)] border border-[var(--outline)] p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[var(--on-surface)]" style="font-family:'JetBrains Mono',monospace;">// SYSTEM_HEALTH</h2>
              <span class="material-symbols-outlined text-[var(--primary-bright)] text-sm">monitor_heart</span>
            </div>
            <div class="space-y-5">
              <div class="space-y-2">
                <div class="flex justify-between text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
                  <span>DATABASE_LATENCY</span><span class="text-[var(--primary-bright)]">12ms</span>
                </div>
                <div class="h-1.5 w-full bg-[var(--surface-variant)] overflow-hidden">
                  <div class="h-full bg-[var(--primary)]" style="width:12%;"></div>
                </div>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
                  <span>CACHE_HIT_RATE</span><span class="text-[var(--primary-bright)]">94%</span>
                </div>
                <div class="h-1.5 w-full bg-[var(--surface-variant)] overflow-hidden">
                  <div class="h-full bg-[var(--primary)]" style="width:94%;"></div>
                </div>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
                  <span>ERROR_RATE</span><span class="text-[var(--tertiary)]">0.02%</span>
                </div>
                <div class="h-1.5 w-full bg-[var(--surface-variant)] overflow-hidden">
                  <div class="h-full bg-[var(--tertiary)]" style="width:2%;"></div>
                </div>
              </div>
            </div>
            <div class="mt-8 pt-5 border-t border-[var(--outline)] flex justify-between items-center">
              <div class="text-[10px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">NODE_JS V20.12.2</div>
              <div class="flex gap-1">
                <div class="w-1.5 h-1.5 bg-[var(--primary-bright)] animate-pulse"></div>
                <div class="w-1.5 h-1.5 bg-[var(--primary-bright)] animate-pulse" style="animation-delay:0.2s"></div>
                <div class="w-1.5 h-1.5 bg-[var(--primary-bright)] animate-pulse" style="animation-delay:0.4s"></div>
              </div>
            </div>
          </div>

          <!-- Code Snippet -->
          <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 relative overflow-hidden">
            <div class="absolute top-2 right-2 text-[10px] text-[var(--on-surface-variant)] opacity-50" style="font-family:'JetBrains Mono',monospace;">SYS_LOG.TS</div>
            <div class="space-y-2 text-[13px]" style="font-family:'JetBrains Mono',monospace; line-height:1.5;">
              <div class="flex gap-4"><span class="text-[var(--on-surface-variant)]">01</span> <span class="text-[var(--primary-bright)]">const</span> <span class="text-[var(--tertiary)]">health</span> <span class="text-[var(--on-surface)]">= {</span></div>
              <div class="flex gap-4"><span class="text-[var(--on-surface-variant)]">02</span> <span class="text-[var(--on-surface)] ml-4">uptime:</span> <span class="text-[var(--secondary)]">'99.9%'</span><span class="text-[var(--on-surface)]">;</span></div>
              <div class="flex gap-4"><span class="text-[var(--on-surface-variant)]">03</span> <span class="text-[var(--on-surface)] ml-4">load:</span> <span class="text-[var(--secondary)]">'Low'</span><span class="text-[var(--on-surface)]">;</span></div>
              <div class="flex gap-4"><span class="text-[var(--on-surface-variant)]">04</span> <span class="text-[var(--on-surface)] ml-4">status:</span> <span class="text-[var(--secondary)]">'Stable'</span><span class="text-[var(--on-surface)]">;</span></div>
              <div class="flex gap-4"><span class="text-[var(--on-surface-variant)]">05</span> <span class="text-[var(--on-surface)]">}</span></div>
            </div>
          </div>

        </section>
      </div>

    </div>
  </AdminLayout>
</template>
