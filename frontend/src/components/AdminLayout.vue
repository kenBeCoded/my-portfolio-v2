<script setup lang="ts">
import { ref, onMounted, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const props = defineProps<{ pageTitle: string }>()

const router = useRouter()
const route  = useRoute()

const sidebarOpen = ref(false)
const isDark = ref(true)

provide('isDark', isDark)


const navItems = [
  { label: 'Overview',  icon: 'dashboard',    to: '/admin'           },
  { label: 'Projects',  icon: 'account_tree', to: '/admin/projects'  },
  { label: 'TechStack', icon: 'analytics',    to: '/admin/techstack' },
  { label: 'Accounts',  icon: 'group',        to: '/admin/accounts'  },
]

function isActive(to: string) {
  return to === '/admin' ? route.path === '/admin' : route.path.startsWith(to)
}

function logout() {
  router.push('/admin/login')
}

function toggleTheme() {
  isDark.value = !isDark.value
  updateTheme()
}

function updateTheme() {
  if (isDark.value) {
    document.documentElement.classList.remove('light')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.add('light')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'light') {
    isDark.value = false
    updateTheme()
  }
})
</script>

<template>
  <div
    class="bg-[var(--background)] text-[var(--on-surface)] min-h-screen flex overflow-x-hidden transition-colors duration-300"
    style="font-family:'Geist',sans-serif;"
  >
    <!-- ─── Sidebar ─── -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 w-64 bg-[var(--surface)] border-r border-[var(--outline)] z-50 flex flex-col transition-transform duration-300',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <!-- Logo -->
      <div class="p-6 border-b border-[var(--outline)] flex items-center gap-3">
        <div class="w-8 h-8 bg-[var(--primary)] flex items-center justify-center">
          <span class="text-[var(--on-primary)] font-bold text-xs" style="font-family:'JetBrains Mono',monospace;">&gt;_</span>
        </div>
        <span class="font-bold text-lg tracking-tighter text-[var(--on-surface)]">&lt;BACKEND&gt;</span>
      </div>

      <!-- Nav -->
      <nav class="flex-grow p-4 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in navItems"
          :key="item.label"
          :to="item.to"
          @click="sidebarOpen = false"
          :class="[
            'flex items-center gap-3 px-4 py-3 transition-all',
            'font-semibold tracking-widest uppercase text-[11px]',
            isActive(item.to)
              ? 'bg-[var(--primary)]/10 text-[var(--primary-bright)] border-l-2 border-[var(--primary-bright)]'
              : 'text-[var(--on-surface-variant)] hover:bg-[var(--surface-variant)] hover:text-[var(--on-surface)]'
          ]"
          style="font-family:'JetBrains Mono',monospace;"
        >
          <span class="material-symbols-outlined text-[20px]">{{ item.icon }}</span>
          {{ item.label }}
        </router-link>
      </nav>

      <!-- Session / Logout -->
      <div class="p-6 border-t border-[var(--outline)]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-[var(--primary)] flex items-center justify-center text-[var(--on-primary)] font-bold text-sm" style="font-family:'JetBrains Mono',monospace;">AD</div>
          <div>
            <p class="text-[12px] font-semibold tracking-widest uppercase text-[var(--on-surface)]" style="font-family:'JetBrains Mono',monospace;">Admin_Root</p>
            <p class="text-[10px] tracking-widest uppercase text-[var(--on-surface-variant)]" style="font-family:'JetBrains Mono',monospace;">Session: Active</p>
          </div>
        </div>
        <button
          @click="logout"
          class="mt-4 w-full text-[10px] font-semibold tracking-widest uppercase text-[var(--on-surface-variant)] hover:text-[var(--tertiary)] transition-colors text-left"
          style="font-family:'JetBrains Mono',monospace;"
        >[ LOGOUT ]</button>
      </div>
    </aside>

    <!-- Mobile overlay -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black/60 z-40 lg:hidden" @click="sidebarOpen = false" />

    <!-- ─── Main Content ─── -->
    <div class="flex-grow lg:ml-64 flex flex-col min-h-screen">

      <!-- Top Bar -->
      <header class="sticky top-0 w-full z-40 flex justify-between items-center px-5 md:px-16 py-4 bg-[var(--background)]/90 backdrop-blur-md border-b border-[var(--outline)]">
        <div class="flex items-center gap-4">
          <button class="lg:hidden text-[var(--primary-bright)]" @click="sidebarOpen = !sidebarOpen">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <h1 class="text-base font-semibold text-[var(--on-surface)]">{{ pageTitle }}</h1>
        </div>
        <div class="flex items-center gap-4">
          <button class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">search</span></button>
          <button class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity"><span class="material-symbols-outlined">notifications</span></button>
          <button
            @click="toggleTheme"
            class="text-[var(--primary-bright)] hover:opacity-70 transition-opacity"
          >
            <span class="material-symbols-outlined">{{ isDark ? 'light_mode' : 'dark_mode' }}</span>
          </button>
        </div>
      </header>

      <!-- Blueprint overlay + slot -->
      <main class="relative flex-grow">
        <div class="absolute inset-0 pointer-events-none -z-10" style="background-image:linear-gradient(to right,var(--outline) 1px,transparent 1px),linear-gradient(to bottom,var(--outline) 1px,transparent 1px);background-size:40px 40px;opacity:0.07;"></div>
        <div class="max-w-[1200px] mx-auto px-5 md:px-16 py-8">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

