<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import AdminLayout from "../components/AdminLayout.vue";
import { fetchProjects } from "../services/projectService";
import { fetchTechStacks } from "../services/techStackService";
import { fetchUsers } from "../services/userService";
import { fetchVisitorStats, type VisitorStatsOut } from "../services/visitorService";

// ── General stats ────────────────────────────────────────────
const projectsCount  = ref(0);
const accountsCount  = ref(0);
const techStackCount = ref(0);
const isLoading      = ref(true);

// ── Visitor analytics ────────────────────────────────────────
const visitorStats    = ref<VisitorStatsOut | null>(null);
const visitorLoading  = ref(true);
const visitorError    = ref(false);
const chartMode       = ref<'daily' | 'weekly'>('daily');

onMounted(async () => {
  try {
    const [projects, techStacks, users] = await Promise.all([
      fetchProjects(),
      fetchTechStacks(),
      fetchUsers(),
    ]);
    projectsCount.value  = projects.length;
    techStackCount.value = techStacks.length;
    accountsCount.value  = users.length;
  } catch (error) {
    console.error("Failed to fetch dashboard stats:", error);
  } finally {
    isLoading.value = false;
  }

  try {
    visitorStats.value = await fetchVisitorStats();
  } catch (error) {
    console.error("Failed to fetch visitor stats:", error);
    visitorError.value = true;
  } finally {
    visitorLoading.value = false;
  }
});

// ── Chart data ───────────────────────────────────────────────
const chartBars = computed(() => {
  if (!visitorStats.value) return [];

  if (chartMode.value === 'daily') {
    const rows = visitorStats.value.daily_stats;
    const max  = Math.max(...rows.map(r => r.unique_visitors), 1);
    return rows.map(r => ({
      label: new Date(r.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      value: r.unique_visitors,
      views: r.page_views,
      pct:   Math.round((r.unique_visitors / max) * 100),
    }));
  } else {
    const rows = visitorStats.value.weekly_stats;
    const max  = Math.max(...rows.map(r => r.unique_visitors), 1);
    return rows.map(r => ({
      label: new Date(r.week_start_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      value: r.unique_visitors,
      views: null,
      pct:   Math.round((r.unique_visitors / max) * 100),
    }));
  }
});

// ── Top pages ─────────────────────────────────────────────────
const topPagesMax = computed(() => {
  if (!visitorStats.value?.top_pages.length) return 1;
  return Math.max(...visitorStats.value.top_pages.map(p => p.page_views));
});

// ── Recent visits — parse browser from UA ────────────────────
function parseBrowser(ua: string | null): string {
  if (!ua) return 'Unknown';
  if (/Edg\//.test(ua))     return 'Edge';
  if (/OPR\//.test(ua))     return 'Opera';
  if (/Firefox\//.test(ua)) return 'Firefox';
  if (/Chrome\//.test(ua))  return 'Chrome';
  if (/Safari\//.test(ua))  return 'Safari';
  return 'Other';
}

function parseOS(ua: string | null): string {
  if (!ua) return '';
  if (/Windows/.test(ua))  return 'Windows';
  if (/Mac OS/.test(ua))   return 'macOS';
  if (/Linux/.test(ua))    return 'Linux';
  if (/Android/.test(ua))  return 'Android';
  if (/iPhone|iPad/.test(ua)) return 'iOS';
  return '';
}

function formatTime(ts: string): string {
  return new Date(ts).toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}
</script>

<template>
  <AdminLayout page-title="Dashboard Overview">
    <div class="space-y-10">

      <!-- ── Stats Grid ── -->
      <section class="grid grid-cols-1 gap-4 md:grid-cols-3">
        <!-- Created Projects -->
        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors h-full">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">rocket_launch</span>
            <span class="font-label-caps text-[10px] text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace">LIVE</span>
          </div>
          <p class="font-label-caps text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
            style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;font-weight:600;">
            Created Projects
          </p>
          <h3 class="font-headline-md text-3xl font-semibold text-[var(--on-surface)]">
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else>{{ projectsCount }}</span>
          </h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-label-caps text-[var(--on-surface-variant)]"
            style="font-family:'JetBrains Mono',monospace">
            <span class="text-[var(--primary-bright)]">+ Active</span>
          </div>
        </div>

        <!-- Total Accounts -->
        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors h-full">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">timer</span>
            <span class="font-label-caps text-[10px] text-[var(--primary-bright)]" style="font-family:'JetBrains Mono',monospace">System</span>
          </div>
          <p class="font-label-caps text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
            style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;font-weight:600;">
            Total Accounts
          </p>
          <h3 class="font-headline-md text-3xl font-semibold text-[var(--on-surface)]">
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else>{{ accountsCount }}</span>
          </h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-label-caps text-[var(--on-surface-variant)]"
            style="font-family:'JetBrains Mono',monospace">
            <span class="text-[var(--primary-bright)]">Registered</span>
          </div>
        </div>

        <!-- TechStack Registry -->
        <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors h-full">
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]">api</span>
            <span class="font-label-caps text-[10px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace">REQUESTS</span>
          </div>
          <p class="font-label-caps text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
            style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;font-weight:600;">
            TechStack Registry
          </p>
          <h3 class="font-headline-md text-3xl font-semibold text-[var(--on-surface)]">
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else>{{ techStackCount }}</span>
          </h3>
          <div class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-label-caps text-[var(--on-surface-variant)]"
            style="font-family:'JetBrains Mono',monospace">
            <span class="text-[var(--primary-bright)]">Verified</span>
          </div>
        </div>
      </section>


      <!-- ── Visitor Analytics Section ── -->
      <section class="space-y-6">

        <!-- Section header -->
        <div class="flex items-center gap-3 pb-2 border-b border-[var(--outline)]">
          <span class="material-symbols-outlined text-[var(--primary-bright)]">monitoring</span>
          <h2 class="text-[13px] font-semibold tracking-widest uppercase text-[var(--on-surface)]"
            style="font-family:'JetBrains Mono',monospace;">
            // PORTFOLIO_VISITOR_ANALYTICS
          </h2>
        </div>

        <!-- Error state -->
        <div v-if="visitorError" class="bg-[var(--surface)] border border-[var(--outline)] p-6 text-center">
          <span class="material-symbols-outlined text-[var(--error)] text-3xl mb-2 block">error_outline</span>
          <p class="text-[12px] text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">
            Failed to load visitor analytics. Check backend connection.
          </p>
        </div>

        <template v-else>
          <!-- Visitor metric cards -->
          <div class="grid grid-cols-1 gap-4 md:grid-cols-3">

            <!-- Weekly Unique Visitors -->
            <div class="bg-[var(--surface)] border border-[var(--primary-bright)]/30 p-6 hover:border-[var(--primary-bright)] transition-colors relative overflow-hidden">
              <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-[var(--primary-bright)] to-transparent"></div>
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[var(--primary-bright)]">group</span>
                <span class="text-[10px] px-2 py-0.5 border border-[var(--primary-bright)]/40 text-[var(--primary-bright)]"
                  style="font-family:'JetBrains Mono',monospace;">
                  LIVE · 7D
                </span>
              </div>
              <p class="text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
                style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;font-weight:600;">
                Weekly Visitors
              </p>
              <h3 class="text-3xl font-semibold text-[var(--on-surface)]">
                <span v-if="visitorLoading" class="animate-pulse text-[var(--on-surface-variant)]">···</span>
                <span v-else>{{ visitorStats?.weekly_unique_visitors ?? 0 }}</span>
              </h3>
              <div class="mt-4 pt-4 border-t border-[var(--outline)] text-[10px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                Unique devices · last 7 days
              </div>
            </div>

            <!-- Total Unique Visitors -->
            <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors">
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[var(--primary-bright)]">person_pin</span>
                <span class="text-[10px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">ALL TIME</span>
              </div>
              <p class="text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
                style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;font-weight:600;">
                Unique Visitors
              </p>
              <h3 class="text-3xl font-semibold text-[var(--on-surface)]">
                <span v-if="visitorLoading" class="animate-pulse text-[var(--on-surface-variant)]">···</span>
                <span v-else>{{ visitorStats?.total_unique_visitors ?? 0 }}</span>
              </h3>
              <div class="mt-4 pt-4 border-t border-[var(--outline)] text-[10px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                Distinct browser devices
              </div>
            </div>

            <!-- Total Page Views -->
            <div class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors">
              <div class="flex justify-between items-start mb-4">
                <span class="material-symbols-outlined text-[var(--primary-bright)]">bar_chart</span>
                <span class="text-[10px] text-[var(--on-surface-variant)]"
                  style="font-family:'JetBrains Mono',monospace;">ALL TIME</span>
              </div>
              <p class="text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
                style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;font-weight:600;">
                Total Page Views
              </p>
              <h3 class="text-3xl font-semibold text-[var(--on-surface)]">
                <span v-if="visitorLoading" class="animate-pulse text-[var(--on-surface-variant)]">···</span>
                <span v-else>{{ visitorStats?.total_page_views ?? 0 }}</span>
              </h3>
              <div class="mt-4 pt-4 border-t border-[var(--outline)] text-[10px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                Total recorded sessions
              </div>
            </div>
          </div>

          <!-- ── Bar Chart ── -->
          <div class="bg-[var(--surface)] border border-[var(--outline)] p-6">
            <!-- Chart header + toggle -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <p class="text-[11px] uppercase text-[var(--on-surface-variant)] mb-0.5"
                  style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;">
                  Unique Visitors Over Time
                </p>
                <p class="text-[10px] text-[var(--on-surface-variant)]/60"
                  style="font-family:'JetBrains Mono',monospace;">
                  {{ chartMode === 'daily' ? 'Last 14 days' : 'Last 8 weeks' }}
                </p>
              </div>
              <!-- Toggle tabs -->
              <div class="flex border border-[var(--outline)] overflow-hidden shrink-0">
                <button
                  @click="chartMode = 'daily'"
                  :class="[
                    'px-4 py-1.5 text-[10px] font-semibold tracking-widest uppercase transition-colors',
                    chartMode === 'daily'
                      ? 'bg-[var(--primary-bright)] text-[var(--on-primary)]'
                      : 'text-[var(--on-surface-variant)] hover:text-[var(--primary-bright)]'
                  ]"
                  style="font-family:'JetBrains Mono',monospace;">
                  Daily
                </button>
                <button
                  @click="chartMode = 'weekly'"
                  :class="[
                    'px-4 py-1.5 text-[10px] font-semibold tracking-widest uppercase transition-colors border-l border-[var(--outline)]',
                    chartMode === 'weekly'
                      ? 'bg-[var(--primary-bright)] text-[var(--on-primary)]'
                      : 'text-[var(--on-surface-variant)] hover:text-[var(--primary-bright)]'
                  ]"
                  style="font-family:'JetBrains Mono',monospace;">
                  Weekly
                </button>
              </div>
            </div>

            <!-- Chart loading -->
            <div v-if="visitorLoading" class="flex items-end gap-2 h-36">
              <div v-for="i in 10" :key="i"
                class="flex-1 bg-[var(--surface-variant)] animate-pulse rounded-sm"
                :style="`height:${20 + Math.random() * 80}%`">
              </div>
            </div>

            <!-- No data -->
            <div v-else-if="!chartBars.length" class="h-36 flex items-center justify-center text-[12px] text-[var(--on-surface-variant)]"
              style="font-family:'JetBrains Mono',monospace;">
              No visitor data yet. Visit the public portfolio to start tracking.
            </div>

            <!-- SVG Bar Chart -->
            <div v-else>
              <div class="flex items-end gap-1.5 h-36 mb-2">
                <div
                  v-for="(bar, i) in chartBars" :key="i"
                  class="group flex-1 flex flex-col items-center justify-end gap-1 h-full relative"
                >
                  <!-- Tooltip -->
                  <div class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-[var(--surface-variant)] border border-[var(--outline)] px-2 py-1 text-[10px] text-[var(--on-surface)] opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10"
                    style="font-family:'JetBrains Mono',monospace;">
                    {{ bar.value }} visitor{{ bar.value !== 1 ? 's' : '' }}
                    <span v-if="bar.views !== null" class="text-[var(--on-surface-variant)]">· {{ bar.views }} views</span>
                  </div>
                  <!-- Bar -->
                  <div
                    class="w-full bg-[var(--primary)] group-hover:bg-[var(--primary-bright)] transition-colors rounded-sm"
                    :style="`height:${Math.max(bar.pct, 2)}%`"
                  ></div>
                </div>
              </div>
              <!-- X-axis labels -->
              <div class="flex gap-1.5">
                <div
                  v-for="(bar, i) in chartBars" :key="i"
                  class="flex-1 text-center text-[8px] text-[var(--on-surface-variant)] truncate"
                  style="font-family:'JetBrains Mono',monospace;"
                >
                  {{ bar.label }}
                </div>
              </div>
            </div>
          </div>

          <!-- ── Bottom grid: Top Pages + Recent Activity ── -->
          <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">

            <!-- Top Pages -->
            <div class="bg-[var(--surface)] border border-[var(--outline)] p-6">
              <div class="flex items-center gap-2 mb-5">
                <span class="material-symbols-outlined text-[var(--primary-bright)] text-[18px]">leaderboard</span>
                <p class="text-[11px] font-semibold uppercase text-[var(--on-surface)]"
                  style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;">
                  Top Pages
                </p>
              </div>

              <div v-if="visitorLoading" class="space-y-3">
                <div v-for="i in 5" :key="i" class="h-8 bg-[var(--surface-variant)] animate-pulse rounded-sm"></div>
              </div>

              <div v-else-if="!visitorStats?.top_pages.length" class="text-[12px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                No page data yet.
              </div>

              <div v-else class="space-y-3">
                <div v-for="page in visitorStats.top_pages" :key="page.page_path" class="flex flex-col gap-1">
                  <div class="flex justify-between items-center">
                    <span class="text-[11px] text-[var(--on-surface)] truncate max-w-[70%]"
                      style="font-family:'JetBrains Mono',monospace;">
                      {{ page.page_path || '/' }}
                    </span>
                    <span class="text-[10px] text-[var(--primary-bright)] shrink-0"
                      style="font-family:'JetBrains Mono',monospace;">
                      {{ page.page_views }} views
                    </span>
                  </div>
                  <!-- Progress bar -->
                  <div class="h-1 w-full bg-[var(--surface-variant)] rounded-full overflow-hidden">
                    <div
                      class="h-full bg-[var(--primary)] rounded-full transition-all duration-700"
                      :style="`width:${Math.round((page.page_views / topPagesMax) * 100)}%`"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Activity -->
            <div class="bg-[var(--surface)] border border-[var(--outline)] p-6">
              <div class="flex items-center gap-2 mb-5">
                <span class="material-symbols-outlined text-[var(--primary-bright)] text-[18px]">history</span>
                <p class="text-[11px] font-semibold uppercase text-[var(--on-surface)]"
                  style="font-family:'JetBrains Mono',monospace;letter-spacing:0.1em;">
                  Recent Activity
                </p>
              </div>

              <div v-if="visitorLoading" class="space-y-3">
                <div v-for="i in 5" :key="i" class="h-10 bg-[var(--surface-variant)] animate-pulse rounded-sm"></div>
              </div>

              <div v-else-if="!visitorStats?.recent_visits.length" class="text-[12px] text-[var(--on-surface-variant)]"
                style="font-family:'JetBrains Mono',monospace;">
                No recent visits logged.
              </div>

              <div v-else class="space-y-2.5">
                <div v-for="visit in visitorStats.recent_visits" :key="visit.id"
                  class="flex items-start justify-between gap-3 pb-2.5 border-b border-[var(--outline)] last:border-0">
                  <div class="flex flex-col gap-0.5 min-w-0">
                    <span class="text-[11px] text-[var(--on-surface)] truncate"
                      style="font-family:'JetBrains Mono',monospace;">
                      {{ visit.page_path || '/' }}
                    </span>
                    <div class="flex items-center gap-1.5 flex-wrap">
                      <span class="text-[9px] px-1.5 py-0.5 bg-[var(--surface-variant)] text-[var(--primary-bright)] border border-[var(--outline)]"
                        style="font-family:'JetBrains Mono',monospace;">
                        {{ parseBrowser(visit.user_agent) }}
                      </span>
                      <span v-if="parseOS(visit.user_agent)"
                        class="text-[9px] px-1.5 py-0.5 bg-[var(--surface-variant)] text-[var(--on-surface-variant)] border border-[var(--outline)]"
                        style="font-family:'JetBrains Mono',monospace;">
                        {{ parseOS(visit.user_agent) }}
                      </span>
                    </div>
                  </div>
                  <span class="text-[9px] text-[var(--on-surface-variant)] shrink-0 mt-0.5"
                    style="font-family:'JetBrains Mono',monospace;">
                    {{ formatTime(visit.timestamp) }}
                  </span>
                </div>
              </div>
            </div>

          </div>
        </template>
      </section>

    </div>
  </AdminLayout>
</template>
