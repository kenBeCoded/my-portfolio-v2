<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const navItems = [
  { label: 'Overview',   icon: 'dashboard',    active: true  },
  { label: 'Projects',   icon: 'account_tree', active: false },
  { label: 'TechStack',  icon: 'analytics',    active: false },
  { label: 'Accounts',   icon: 'group',        active: false },
]

const deployments = [
  { ts: '2024-05-23 14:22', service: 'auth-microservice', action: 'Deploy: v2.4.1',      status: 'SUCCESS' },
  { ts: '2024-05-23 12:05', service: 'api-gateway',       action: 'Patch: SSL Renewal',  status: 'SUCCESS' },
  { ts: '2024-05-23 09:45', service: 'db-backup-job',     action: 'Backup: pg_prod_01',  status: 'FAILED'  },
  { ts: '2024-05-22 23:12', service: 'analytics-worker',  action: 'Scale Up: +2 Replicas', status: 'SUCCESS' },
]

const sidebarOpen = ref(false)

function logout() {
  router.push('/admin/login')
}
</script>

<template>
  <div
    class="bg-[#0b1326] text-[#dae2fd] min-h-screen flex overflow-x-hidden"
    style="font-family: 'Geist', sans-serif;"
  >
    <!-- ─── Sidebar ─── -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 w-64 bg-[#171f33] border-r border-[#3c4a42] z-50 flex flex-col transition-transform duration-300',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <!-- Logo -->
      <div class="p-6 border-b border-[#3c4a42] flex items-center gap-3">
        <div class="w-8 h-8 bg-[#10b981] flex items-center justify-center">
          <span class="text-[#003824] font-bold text-xs" style="font-family:'JetBrains Mono',monospace;">&gt;_</span>
        </div>
        <span class="font-bold text-lg tracking-tighter text-[#dae2fd]" style="font-family:'Geist',sans-serif;">&lt;BACKEND&gt;</span>
      </div>

      <!-- Nav -->
      <nav class="flex-grow p-4 space-y-1 overflow-y-auto">
        <a
          v-for="item in navItems"
          :key="item.label"
          href="#"
          :class="[
            'flex items-center gap-3 px-4 py-3 transition-all',
            'font-semibold tracking-widest uppercase text-[11px]',
            item.active
              ? 'bg-[#10b981]/10 text-[#4edea3] border-l-2 border-[#4edea3]'
              : 'text-[#86948a] hover:bg-[#222a3d] hover:text-[#dae2fd]'
          ]"
          style="font-family:'JetBrains Mono',monospace;"
        >
          <span class="material-symbols-outlined text-[20px]">{{ item.icon }}</span>
          {{ item.label }}
        </a>
      </nav>

      <!-- Session Info -->
      <div class="p-6 border-t border-[#3c4a42]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-[#10b981] flex items-center justify-center text-[#003824] font-bold text-sm" style="font-family:'JetBrains Mono',monospace;">
            AD
          </div>
          <div>
            <p class="text-[12px] font-semibold tracking-widest uppercase text-[#dae2fd]" style="font-family:'JetBrains Mono',monospace;">Admin_Root</p>
            <p class="text-[10px] tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">Session: Active</p>
          </div>
        </div>
        <button
          @click="logout"
          class="mt-4 w-full text-[10px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#ffb3af] transition-colors text-left px-0"
          style="font-family:'JetBrains Mono',monospace;"
        >
          [ LOGOUT ]
        </button>
      </div>
    </aside>

    <!-- Overlay for mobile -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/60 z-40 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- ─── Main Content ─── -->
    <div class="flex-grow lg:ml-64 flex flex-col min-h-screen">

      <!-- Top Bar -->
      <header class="sticky top-0 w-full z-40 flex justify-between items-center px-5 md:px-16 py-4 bg-[#0b1326]/90 backdrop-blur-md border-b border-[#3c4a42]">
        <div class="flex items-center gap-4">
          <!-- Hamburger (mobile) -->
          <button class="lg:hidden text-[#4edea3]" @click="sidebarOpen = !sidebarOpen">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <h1 class="text-base font-semibold text-[#dae2fd]" style="font-family:'Geist',sans-serif;">Dashboard Overview</h1>
        </div>
        <div class="flex items-center gap-4">
          <button class="text-[#4edea3] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">search</span></button>
          <button class="text-[#4edea3] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">notifications</span></button>
          <button class="text-[#4edea3] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">dark_mode</span></button>
        </div>
      </header>

      <!-- Page Body -->
      <main class="relative flex-grow">
        <!-- Blueprint grid overlay -->
        <div class="absolute inset-0 pointer-events-none -z-10" style="background-image:linear-gradient(to right,#3c4a42 1px,transparent 1px),linear-gradient(to bottom,#3c4a42 1px,transparent 1px);background-size:40px 40px;opacity:0.07;"></div>

        <div class="max-w-[1200px] mx-auto px-5 md:px-16 py-8 space-y-10">

          <!-- ── Stats Grid ── -->
          <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

            <div class="bg-[#171f33] border border-[#3c4a42] p-6 hover:border-[#4edea3] transition-colors group">
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[#4edea3]">rocket_launch</span>
                <span class="text-[10px] font-semibold tracking-widest text-[#4edea3]" style="font-family:'JetBrains Mono',monospace;">LIVE</span>
              </div>
              <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] mb-1" style="font-family:'JetBrains Mono',monospace;">Active Projects</p>
              <h3 class="text-2xl font-semibold text-[#dae2fd]">12</h3>
              <div class="mt-4 pt-4 border-t border-[#3c4a42] flex items-center gap-2 text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">
                <span class="text-[#4edea3]">+2</span> this month
              </div>
            </div>

            <div class="bg-[#171f33] border border-[#3c4a42] p-6 hover:border-[#4edea3] transition-colors">
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[#4edea3]">timer</span>
                <span class="text-[10px] font-semibold tracking-widest text-[#4edea3]" style="font-family:'JetBrains Mono',monospace;">99.9%</span>
              </div>
              <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] mb-1" style="font-family:'JetBrains Mono',monospace;">System Uptime</p>
              <h3 class="text-2xl font-semibold text-[#dae2fd]">724h 12m</h3>
              <div class="mt-4 pt-4 border-t border-[#3c4a42] text-[10px] font-semibold tracking-widest uppercase text-[#4edea3]" style="font-family:'JetBrains Mono',monospace;">Operational</div>
            </div>

            <div class="bg-[#171f33] border border-[#3c4a42] p-6 hover:border-[#4edea3] transition-colors">
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[#4edea3]">api</span>
                <span class="text-[10px] font-semibold tracking-widest text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">REQUESTS</span>
              </div>
              <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] mb-1" style="font-family:'JetBrains Mono',monospace;">Total API Calls</p>
              <h3 class="text-2xl font-semibold text-[#dae2fd]">1.2M</h3>
              <div class="mt-4 pt-4 border-t border-[#3c4a42] flex items-center gap-2 text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">
                <span class="text-[#4edea3]">↑ 12%</span> vs last week
              </div>
            </div>

            <div class="bg-[#171f33] border border-[#3c4a42] p-6 hover:border-[#4edea3] transition-colors">
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[#4edea3]">memory</span>
                <span class="text-[10px] font-semibold tracking-widest text-[#ffb3af]" style="font-family:'JetBrains Mono',monospace;">STRESS_LOW</span>
              </div>
              <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] mb-1" style="font-family:'JetBrains Mono',monospace;">Server Load</p>
              <h3 class="text-2xl font-semibold text-[#dae2fd]">34%</h3>
              <div class="mt-4 pt-4 border-t border-[#3c4a42]">
                <div class="h-1 w-full bg-[#2d3449] overflow-hidden">
                  <div class="h-full bg-[#10b981]" style="width:34%;"></div>
                </div>
              </div>
            </div>
          </section>

          <!-- ── Main Panels ── -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

            <!-- Recent Deployments -->
            <section class="lg:col-span-8 bg-[#171f33] border border-[#3c4a42] overflow-hidden">
              <div class="p-6 border-b border-[#3c4a42] flex justify-between items-center">
                <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[#dae2fd]" style="font-family:'JetBrains Mono',monospace;">// RECENT_DEPLOYMENTS</h2>
                <button class="text-[10px] font-semibold tracking-widest uppercase text-[#4edea3] hover:underline" style="font-family:'JetBrains Mono',monospace;">VIEW_ALL_LOGS</button>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-left">
                  <thead class="bg-[#222a3d]/40">
                    <tr class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">
                      <th class="px-6 py-3 border-b border-[#3c4a42]">TIMESTAMP</th>
                      <th class="px-6 py-3 border-b border-[#3c4a42]">SERVICE</th>
                      <th class="px-6 py-3 border-b border-[#3c4a42]">ACTION</th>
                      <th class="px-6 py-3 border-b border-[#3c4a42] text-right">STATUS</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="d in deployments"
                      :key="d.ts"
                      class="hover:bg-[#222a3d]/30 transition-colors text-[12px] text-[#86948a]"
                      style="font-family:'JetBrains Mono',monospace;"
                    >
                      <td class="px-6 py-4 border-b border-[#3c4a42]/30">{{ d.ts }}</td>
                      <td class="px-6 py-4 border-b border-[#3c4a42]/30 text-[#dae2fd]">{{ d.service }}</td>
                      <td class="px-6 py-4 border-b border-[#3c4a42]/30">{{ d.action }}</td>
                      <td class="px-6 py-4 border-b border-[#3c4a42]/30 text-right">
                        <span
                          :class="d.status === 'SUCCESS'
                            ? 'px-2 py-0.5 border text-[#4edea3] border-[#4edea3]/30 bg-[#4edea3]/10'
                            : 'px-2 py-0.5 border text-[#ffb4ab] border-[#ffb4ab]/30 bg-[#93000a]/40'"
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
              <div class="bg-[#171f33] border border-[#3c4a42] p-6">
                <div class="flex justify-between items-center mb-6">
                  <h2 class="text-[11px] font-semibold tracking-widest uppercase text-[#dae2fd]" style="font-family:'JetBrains Mono',monospace;">// SYSTEM_HEALTH</h2>
                  <span class="material-symbols-outlined text-[#4edea3] text-sm">monitor_heart</span>
                </div>
                <div class="space-y-5">
                  <div class="space-y-2">
                    <div class="flex justify-between text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">
                      <span>DATABASE_LATENCY</span><span class="text-[#4edea3]">12ms</span>
                    </div>
                    <div class="h-1.5 w-full bg-[#2d3449] overflow-hidden">
                      <div class="h-full bg-[#10b981]" style="width:12%;"></div>
                    </div>
                  </div>
                  <div class="space-y-2">
                    <div class="flex justify-between text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">
                      <span>CACHE_HIT_RATE</span><span class="text-[#4edea3]">94%</span>
                    </div>
                    <div class="h-1.5 w-full bg-[#2d3449] overflow-hidden">
                      <div class="h-full bg-[#10b981]" style="width:94%;"></div>
                    </div>
                  </div>
                  <div class="space-y-2">
                    <div class="flex justify-between text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">
                      <span>ERROR_RATE</span><span class="text-[#ffb3af]">0.02%</span>
                    </div>
                    <div class="h-1.5 w-full bg-[#2d3449] overflow-hidden">
                      <div class="h-full bg-[#fc7c78]" style="width:2%;"></div>
                    </div>
                  </div>
                </div>
                <div class="mt-8 pt-5 border-t border-[#3c4a42] flex justify-between items-center">
                  <div class="text-[10px] text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">NODE_JS V20.12.2</div>
                  <div class="flex gap-1">
                    <div class="w-1.5 h-1.5 bg-[#4edea3] animate-pulse"></div>
                    <div class="w-1.5 h-1.5 bg-[#4edea3] animate-pulse" style="animation-delay:0.2s"></div>
                    <div class="w-1.5 h-1.5 bg-[#4edea3] animate-pulse" style="animation-delay:0.4s"></div>
                  </div>
                </div>
              </div>

              <!-- Code Snippet -->
              <div class="bg-[#171f33] border border-[#3c4a42] p-6 relative overflow-hidden">
                <div class="absolute top-2 right-2 text-[10px] text-[#86948a] opacity-50" style="font-family:'JetBrains Mono',monospace;">SYS_LOG.TS</div>
                <div class="space-y-2 text-[13px]" style="font-family:'JetBrains Mono',monospace; line-height:1.5;">
                  <div class="flex gap-4"><span class="text-[#86948a]">01</span> <span class="text-[#4edea3]">const</span> <span class="text-[#ffb3af]">health</span> <span class="text-[#dae2fd]">= {</span></div>
                  <div class="flex gap-4"><span class="text-[#86948a]">02</span> <span class="text-[#dae2fd] ml-4">uptime:</span> <span class="text-[#c2c4e3]">'99.9%'</span><span class="text-[#dae2fd]">;</span></div>
                  <div class="flex gap-4"><span class="text-[#86948a]">03</span> <span class="text-[#dae2fd] ml-4">load:</span> <span class="text-[#c2c4e3]">'Low'</span><span class="text-[#dae2fd]">;</span></div>
                  <div class="flex gap-4"><span class="text-[#86948a]">04</span> <span class="text-[#dae2fd] ml-4">status:</span> <span class="text-[#c2c4e3]">'Stable'</span><span class="text-[#dae2fd]">;</span></div>
                  <div class="flex gap-4"><span class="text-[#86948a]">05</span> <span class="text-[#dae2fd]">}</span></div>
                </div>
              </div>

            </section>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
