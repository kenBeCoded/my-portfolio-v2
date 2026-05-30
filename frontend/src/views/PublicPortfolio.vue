<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { fetchTechStacks, type TechStackOut } from '../services/techStackService'
import { logVisit, getOrCreateVisitorId } from '../services/visitorService'
import { fetchProjects, type ProjectOut } from '../services/projectService'
import { experienceData, type ExperienceDetail } from '../data/experienceData'

const activeSection = ref('home')
const mobileMenuOpen = ref(false)
const isDarkMode = ref(true)

function toggleTheme() {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.remove('light')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.add('light')
    localStorage.setItem('theme', 'light')
  }
}

const navLinks = [
  { label: 'Home', id: 'home' },
  { label: 'Experience', id: 'experience' },
  { label: 'Projects', id: 'projects' },
  { label: 'Contact', id: 'contact' },
]

const projects = ref<ProjectOut[]>([])

const selectedFolder = ref('linfra_corp')
const selectedFile = ref('ERP_Controller.md')
const isFlatView = ref(false)
const viewMode = ref<'explorer' | 'timeline'>('explorer')

const expandedFolders = ref<Record<string, boolean>>({
  linfra_corp: true,
  richwell_phils: true
})

function toggleFolder(folderKey: string) {
  expandedFolders.value[folderKey] = !expandedFolders.value[folderKey]
}

function selectFile(folder: string, filename: string) {
  selectedFolder.value = folder
  selectedFile.value = filename
}

const currentFileContent = computed(() => {
  return experienceData[selectedFolder.value]?.files[selectedFile.value] || experienceData.root_files.files['README.sh']
})

const flatFiles = computed(() => {
  const list: { folder: string; filename: string; detail: ExperienceDetail }[] = []
  for (const [folderKey, folderData] of Object.entries(experienceData)) {
    for (const [filename, fileDetail] of Object.entries(folderData.files)) {
      list.push({
        folder: folderKey,
        filename,
        detail: fileDetail
      })
    }
  }
  return list
})

function getFallbackIcon(p: ProjectOut) {
  const title = (p.title || '').toLowerCase()
  if (title.includes('gateway') || title.includes('network') || title.includes('api')) return 'hub'
  if (title.includes('db') || title.includes('database') || title.includes('data')) return 'database'
  if (title.includes('auth') || title.includes('security') || title.includes('login')) return 'security'
  if (title.includes('crawler') || title.includes('scraper') || title.includes('search')) return 'travel_explore'
  return 'deployed_code'
}

const apiTechStacks = ref<TechStackOut[]>([])
const isLoadingTechStacks = ref(true)
const isLoadingProjects = ref(true)

const techStack = computed(() => {
  const filterByCategory = (...catPrefixes: string[]) => {
    return apiTechStacks.value
      .filter(t => catPrefixes.some(prefix => t.category.toUpperCase().includes(prefix.toUpperCase())))
      .sort((a, b) => a.sort_order - b.sort_order)
  }

  return [
    { category: 'Languages', icon: 'code', items: filterByCategory('LANGUAGE') },
    { category: 'Frontend', icon: 'layers', items: filterByCategory('FRONTEND') },
    { category: 'Backend', icon: 'settings_ethernet', items: filterByCategory('BACKEND') },
    { category: 'Databases', icon: 'database', items: filterByCategory('DATABASE') },
    { category: 'Tools & Platforms', icon: 'build', items: filterByCategory('TOOL'), wide: true },
    { category: 'Other & AI Tools', icon: 'bolt', items: filterByCategory('OTHER', 'AI'), wide: true, accent: true },
  ]
})

const contactLinks = [
  { label: 'LinkedIn', icon: 'lan', value: 'linkedin.com/in/johnkennethgregorio', href: 'https://www.linkedin.com/in/johnkennethgregorio' },
  { label: 'Gmail', icon: 'mail', value: 'johnkennethgregorio.wom@gmail.com', href: 'mailto:johnkennethgregorio.wom@gmail.com' },
  { label: 'Contact Number (PH) Viber/WhatsApp', icon: 'call', value: '+63 946 328 7756 / +63 963 684 9388', href: '#' },
  { label: 'GitHub', icon: 'terminal', value: 'github.com/kenBeCoded', href: 'https://github.com/kenBeCoded' },
]

// Copy notification states for copy-to-clipboard contact
const showCopyNotification = ref(false)
const copyNotificationText = ref('')

// Lightbox
const lightboxImage = ref<string | null>(null)
function openLightbox(url: string) { lightboxImage.value = url }
function closeLightbox() { lightboxImage.value = null }

async function handleContactClick(c: typeof contactLinks[number], event: Event) {
  if (c.label.includes('Contact Number')) {
    event.preventDefault()
    try {
      await navigator.clipboard.writeText(c.value)
      copyNotificationText.value = 'Copied contact numbers to clipboard!'
      showCopyNotification.value = true
      setTimeout(() => {
        showCopyNotification.value = false
      }, 3000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }
}

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
  mobileMenuOpen.value = false
}

async function downloadResume() {
  const url = import.meta.env.VITE_RESUME_URL || 'https://pmgwsuuyhwtvlzltzjwq.supabase.co/storage/v1/object/public/App-File-Storage/documents/Resume.pdf'
  try {
    const response = await fetch(url)
    const blob = await response.blob()
    const blobUrl = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = blobUrl
    a.download = 'JohnKenneth_Gregorio_Resume.pdf'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(blobUrl)
  } catch {
    // Fallback: open in new tab if fetch fails
    window.open(url, '_blank')
  }
}

let isScrolling = false
function onScroll() {
  if (!isScrolling) {
    window.requestAnimationFrame(() => {
      for (const link of [...navLinks].reverse()) {
        const el = document.getElementById(link.id)
        if (el && window.scrollY >= el.offsetTop - 120) {
          activeSection.value = link.id
          break
        }
      }
      isScrolling = false
    })
    isScrolling = true
  }
}

// Mobile Menu Focus Trap & Accessibility
const lastActiveElement = ref<HTMLElement | null>(null)
const mobileMenuContainer = ref<HTMLElement | null>(null)

function handleKeyDown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    if (lightboxImage.value) { closeLightbox(); return }
    if (mobileMenuOpen.value) mobileMenuOpen.value = false
  }
}

watch(mobileMenuOpen, async (isOpen) => {
  if (isOpen) {
    lastActiveElement.value = document.activeElement as HTMLElement
    window.addEventListener('keydown', handleKeyDown)
    await nextTick()
    // Focus the first button in mobile menu
    const focusable = mobileMenuContainer.value?.querySelectorAll('button, a')
    if (focusable && focusable.length > 0) {
      (focusable[0] as HTMLElement).focus()
    }
  } else {
    window.removeEventListener('keydown', handleKeyDown)
    if (lastActiveElement.value) {
      lastActiveElement.value.focus()
    }
  }
})

// Dynamic last updated (calculating dynamic year/month)
const computedLastUpdated = computed(() => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  return `${year}.${month}.01`
})

onMounted(async () => {
  window.addEventListener('scroll', onScroll)

  // ── Visitor tracking (once per browser session) ──────────────────────────
  try {
    if (!sessionStorage.getItem('portfolio_visited')) {
      const visitorId = getOrCreateVisitorId()
      await logVisit(visitorId, window.location.pathname, document.referrer)
      sessionStorage.setItem('portfolio_visited', 'true')
    }
  } catch {
    // Intentionally silent
  }

  // Concurrently load tech stacks and projects to optimize performance
  isLoadingTechStacks.value = true
  isLoadingProjects.value = true

  const [techStacksRes, projectsRes] = await Promise.allSettled([
    fetchTechStacks(),
    fetchProjects()
  ])

  if (techStacksRes.status === 'fulfilled') {
    apiTechStacks.value = techStacksRes.value
  } else {
    console.error('Failed to load tech stacks:', techStacksRes.reason)
  }
  isLoadingTechStacks.value = false

  if (projectsRes.status === 'fulfilled') {
    projects.value = projectsRes.value
  } else {
    console.error('Failed to load projects:', projectsRes.reason)
  }
  isLoadingProjects.value = false

  // Sync theme status with index.html initialized state
  isDarkMode.value = !document.documentElement.classList.contains('light')
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<template>
  <div class="bg-[#0b1326] text-[#dae2fd] min-h-screen overflow-x-hidden" style="font-family:'Geist',sans-serif;">

    <!-- Blueprint grid -->
    <div class="fixed inset-0 pointer-events-none z-0"
      style="background-image:linear-gradient(to right,var(--outline) 1px,transparent 1px),linear-gradient(to bottom,var(--outline) 1px,transparent 1px);background-size:40px 40px;opacity:0.07;">
    </div>

    <!-- ── NAVBAR ── -->
    <header
      class="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-5 md:px-16 py-4 bg-[#0b1326]/80 backdrop-blur-md border-b border-[#3c4a42]">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-[#10b981] flex items-center justify-center">
          <span class="text-[#003824] font-bold text-xs font-mono-jb">&gt;_</span>
        </div>
        <span class="font-bold text-lg tracking-tighter">&lt;KEN_BE_CODED&gt;</span>
      </div>

      <nav class="hidden md:flex items-center gap-8">
        <button v-for="link in navLinks" :key="link.id" @click="scrollTo(link.id)" :class="[
          'text-[11px] font-semibold tracking-widest uppercase transition-colors',
          'font-mono-jb',
          activeSection === link.id
            ? 'text-[#4edea3] border-b border-[#4edea3] pb-0.5'
            : 'text-[#86948a] hover:text-[#4edea3]'
        ]" :aria-current="activeSection === link.id ? 'page' : undefined">{{ link.label }}</button>
      </nav>

      <div class="flex items-center gap-3">
        <!-- Theme Toggle Button -->
        <button @click="toggleTheme"
          class="flex items-center justify-center text-[#86948a] hover:text-[#4edea3] transition-colors p-1.5 border border-[#3c4a42] hover:border-[#4edea3] cursor-pointer"
          title="Toggle Dark/Light Mode" aria-label="Toggle dark and light mode">
          <span class="material-symbols-outlined text-[18px]">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>

        <a href="#" @click.prevent="downloadResume"
          class="hidden md:flex items-center gap-1.5 text-[10px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] transition-colors border border-[#3c4a42] hover:border-[#4edea3] px-3 py-1.5 font-mono-jb"
          aria-label="Download resume or CV">
          <span class="material-symbols-outlined text-[16px]">download</span> DOWNLOAD RESUME/CV
        </a>
        <button class="md:hidden text-[#4edea3]" @click="mobileMenuOpen = !mobileMenuOpen"
          aria-label="Toggle mobile menu">
          <span class="material-symbols-outlined">{{ mobileMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
    </header>

    <!-- Mobile Nav -->
    <div v-if="mobileMenuOpen" ref="mobileMenuContainer" role="dialog" aria-modal="true"
      aria-label="Mobile Navigation Menu"
      class="fixed inset-0 z-40 bg-[#0b1326]/95 flex flex-col items-center justify-center gap-8">
      <button v-for="link in navLinks" :key="link.id" @click="scrollTo(link.id)"
        class="text-2xl font-semibold tracking-widest uppercase text-[#dae2fd] hover:text-[#4edea3] transition-colors font-mono-jb"
        :aria-current="activeSection === link.id ? 'page' : undefined">{{ link.label }}</button>
    </div>

    <main class="relative z-10">

      <!-- ── HERO SECTION ── -->
      <section id="home" class="max-w-[1200px] mx-auto px-5 md:px-16 pt-40 pb-32">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center pb-24">
          <div class="md:col-span-8 flex flex-col gap-6">
            <div class="space-y-2">
              <h1 class="text-5xl md:text-6xl font-bold tracking-tight text-[#dae2fd]">
                John Kenneth Gregorio
              </h1>
              <p class="text-xl md:text-2xl font-bold text-[#4edea3] font-mono-jb">
                Fullstack Developer
              </p>
            </div>

            <p class="text-lg text-[#dae2fd] max-w-2xl leading-relaxed">
              I am a <strong class="text-[#4edea3] font-bold">Fullstack Developer</strong> architecting the future
              of robust backend systems. My journey is defined by a relentless pursuit of
              engineering excellence, moving beyond simple features into the realm of distributed scalability and
              high-availability infrastructures.
            </p>

            <div class="flex flex-wrap gap-4 pt-2">
              <button @click="scrollTo('contact')"
                class="bg-[#10b981] text-[#003824] px-8 py-3 font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3] transition-colors font-mono-jb">INITIALIZE_CONTACT</button>
              <button @click="scrollTo('projects')"
                class="border border-[#3c4a42] text-[#dae2fd] px-8 py-3 font-semibold tracking-widest uppercase text-[11px] hover:border-[#4edea3] transition-colors font-mono-jb">VIEW_REPOSITORY</button>
            </div>
          </div>

          <!-- Code card -->
          <div class="md:col-span-4 hidden md:block">
            <div class="bg-[#171f33] border border-[#3c4a42] p-6 relative">
              <div class="absolute top-2 right-2 text-[10px] text-[#86948a] opacity-50 font-mono-jb">SYS_LOG.TS</div>
              <div class="space-y-2 text-[13px] font-mono-jb" style="line-height:1.6;">
                <div><span class="text-[#86948a]">01</span> <span class="text-[#4edea3]">interface</span> <span
                    class="text-[#ffb3af]">Developer</span> <span class="text-[#dae2fd]">{</span></div>
                <div><span class="text-[#86948a]">02</span> <span class="text-[#dae2fd] ml-4">focus:</span> <span
                    class="text-[#c2c4e3]">'Backend'</span><span class="text-[#dae2fd]">;</span></div>
                <div><span class="text-[#86948a]">03</span> <span class="text-[#dae2fd] ml-4">stack:</span> <span
                    class="text-[#c2c4e3]">['Node', 'TS', 'Python']</span><span class="text-[#dae2fd]">;</span></div>
                <div><span class="text-[#86948a]">04</span> <span class="text-[#dae2fd] ml-4">status:</span> <span
                    class="text-[#c2c4e3]">'Continuous Learning'</span><span class="text-[#dae2fd]">;</span></div>
                <div><span class="text-[#86948a]">05</span> <span class="text-[#dae2fd]">}</span></div>
              </div>
              <div class="mt-6 pt-4 border-t border-[#3c4a42] flex justify-between items-center">
                <span class="text-[10px] text-[#86948a] font-mono-jb">STABILITY: 99.9%</span>
                <div class="h-1 w-24 bg-[#2d3449] overflow-hidden">
                  <div class="h-full bg-[#10b981]" style="width:99.9%;"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tech stack cards -->
        <div class="border-t border-[#3c4a42]/30 pt-20">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-14">
            <div>
              <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-2 font-mono-jb">//
                FULL_STACK_INVENTORY</p>
              <h2 class="text-3xl font-bold tracking-tight text-[#dae2fd]">Technology Stack</h2>
            </div>
            <!-- <div class="text-[11px] text-[#86948a] text-right leading-relaxed font-mono-jb">VER_04.22.99<br />STATUS:
              OPERATIONAL</div> -->
          </div>

          <div v-if="isLoadingTechStacks"
            class="flex flex-col items-center justify-center py-20 border border-[#3c4a42]/30 bg-[#060e20]">
            <span class="material-symbols-outlined text-4xl text-[#4edea3] animate-spin mb-4">progress_activity</span>
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] font-mono-jb">//
              SYNCING_TECH_STACKS...</p>
          </div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="t in techStack" :key="t.category"
              :class="['flex flex-col gap-4 p-6 bg-[#171f33]/40 border border-[#3c4a42] hover:border-[#4edea3]/50 transition-colors', t.wide ? 'lg:col-span-2' : '', t.category === 'Other & AI Tools' ? 'lg:col-span-3' : '']">
              <div class="flex items-center gap-3">
                <span class="material-symbols-outlined text-[#4edea3]">{{ t.icon }}</span>
                <h3 class="text-[11px] font-semibold tracking-widest uppercase text-[#dae2fd] font-mono-jb">{{
                  t.category }}</h3>
              </div>
              <div class="flex flex-wrap gap-4">
                <template v-for="item in t.items" :key="item.id">
                  <div v-if="item.logo_url" class="relative group flex items-center justify-center">
                    <img :src="item.logo_url" :alt="item.name.toUpperCase()"
                      class="h-10 w-10 object-contain hover:scale-110 transition-transform filter brightness-90 hover:brightness-110" />
                    <span
                      class="absolute -top-10 bg-[#171f33] border border-[#3c4a42] text-[#dae2fd] text-[10px] px-3 py-1 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10 shadow-lg font-mono-jb"
                      style="letter-spacing: 0.05em;">{{ item.name.toUpperCase()
                      }}</span>
                  </div>
                  <span v-else :class="[
                    'text-[12px] px-3 py-1 border flex items-center justify-center min-h-[40px]',
                    'font-mono-jb',
                    t.accent
                      ? 'bg-[#4edea3]/10 border-[#4edea3]/30 text-[#4edea3]'
                      : 'bg-[#171f33] border-[#3c4a42] text-[#86948a]'
                  ]" :title="item.name.toUpperCase()">{{
                    item.name.toUpperCase() }}</span>
                </template>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── EXPERIENCE SECTION ── -->
      <section id="experience" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
          <div>
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-2 font-mono-jb">//
              WORK_HISTORY_LOGS</p>
            <h2 class="text-3xl font-bold tracking-tight text-[#dae2fd]">Professional Experience</h2>
          </div>

          <!-- Layout View Switcher -->
          <div class="flex items-center border border-[#3c4a42] p-1 bg-[#171f33]/40 font-mono-jb">
            <button @click="viewMode = 'explorer'"
              class="px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider transition-colors cursor-pointer"
              :class="viewMode === 'explorer' ? 'bg-[#10b981] text-[#003824]' : 'text-[#86948a] hover:text-[#dae2fd]'"
              aria-label="Switch to explorer view">
              Explorer View
            </button>
            <button @click="viewMode = 'timeline'"
              class="px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider transition-colors cursor-pointer"
              :class="viewMode === 'timeline' ? 'bg-[#10b981] text-[#003824]' : 'text-[#86948a] hover:text-[#dae2fd]'"
              aria-label="Switch to timeline view">
              Timeline View
            </button>
          </div>
        </div>

        <!-- 1. EXPLORER / IDE VIEW -->
        <div v-if="viewMode === 'explorer'"
          class="grid grid-cols-1 lg:grid-cols-12 border border-[#3c4a42] bg-[#0b1326] min-h-[500px]">

          <!-- Left Panel (Sidebar Explorer) -->
          <div class="lg:col-span-4 border-r border-[#3c4a42] flex flex-col bg-[#060e20]/60">
            <!-- Sidebar Header -->
            <div class="px-4 py-3 border-b border-[#3c4a42] flex items-center justify-between">
              <div class="flex items-center gap-2">
                <!-- MacOS style close/min/max window controls -->
                <div class="flex gap-1.5">
                  <span class="w-3 h-3 rounded-full bg-[#ff5f56]"></span>
                  <span class="w-3 h-3 rounded-full bg-[#ffbd2e]"></span>
                  <span class="w-3 h-3 rounded-full bg-[#27c93f]"></span>
                </div>
                <span
                  class="text-[11px] font-semibold tracking-wider text-[#86948a] uppercase ml-2 font-mono-jb">Explorer</span>
              </div>

              <!-- Folder Structure Design Toggle Button -->
              <button @click="isFlatView = !isFlatView"
                class="text-[#86948a] hover:text-[#4edea3] transition-colors p-1 cursor-pointer flex items-center gap-1 text-[10px] border border-[#3c4a42] px-2 font-mono-jb"
                title="Toggle Tree / Flat Folder Structure" aria-label="Toggle explorer tree or flat folder structure">
                <span class="material-symbols-outlined text-[14px]">{{ isFlatView ? 'account_tree' :
                  'format_list_bulleted' }}</span>
                <span>{{ isFlatView ? 'Tree' : 'Flat' }}</span>
              </button>
            </div>

            <!-- Directory path indicator -->
            <div
              class="px-4 py-2 text-[11px] font-semibold text-[#4edea3] bg-[#0b1326]/40 border-b border-[#3c4a42]/30 font-mono-jb">
              /career/
            </div>

            <!-- Folder list -->
            <div class="flex-grow overflow-y-auto p-2 space-y-1 select-none font-mono-jb" style="font-size: 13px;">

              <!-- TREE VIEW -->
              <template v-if="!isFlatView">
                <div v-for="(folderData, folderKey) in experienceData" :key="folderKey" class="space-y-1">
                  <!-- Folders (Skip root_files representing parent files) -->
                  <template v-if="folderKey !== 'root_files'">
                    <div @click="toggleFolder(folderKey)"
                      class="flex items-center gap-1.5 py-1 px-2 hover:bg-[#171f33]/40 text-[#dae2fd] cursor-pointer transition-colors rounded">
                      <span class="material-symbols-outlined text-[16px] text-[#86948a]">
                        {{ expandedFolders[folderKey] ? 'keyboard_arrow_down' : 'chevron_right' }}
                      </span>
                      <span class="material-symbols-outlined text-[18px] text-[#4edea3]/80">
                        {{ expandedFolders[folderKey] ? 'folder_open' : 'folder' }}
                      </span>
                      <span class="truncate">{{ folderData.folderName }}</span>
                    </div>

                    <!-- Indented files under folder -->
                    <div v-show="expandedFolders[folderKey]" class="pl-6 space-y-1">
                      <div v-for="(_, filename) in folderData.files" :key="filename"
                        @click="selectFile(folderKey, filename)" :class="[
                          'flex items-center gap-2 py-1 px-2 cursor-pointer transition-colors rounded border-l-2',
                          selectedFolder === folderKey && selectedFile === filename
                            ? 'bg-[#171f33] border-[#4edea3] text-[#4edea3]'
                            : 'border-transparent text-[#86948a] hover:text-[#dae2fd] hover:bg-[#171f33]/20'
                        ]">
                        <span class="material-symbols-outlined text-[16px] text-sky-400">description</span>
                        <span class="truncate">{{ filename }}</span>
                      </div>
                    </div>
                  </template>
                </div>

                <!-- Standalone/Root Files (like README.sh) -->
                <div v-for="(_, filename) in experienceData.root_files.files" :key="filename"
                  @click="selectFile('root_files', filename)" :class="[
                    'flex items-center gap-2 py-1 px-2 cursor-pointer transition-colors rounded border-l-2 ml-4',
                    selectedFolder === 'root_files' && selectedFile === filename
                      ? 'bg-[#171f33] border-[#4edea3] text-[#4edea3]'
                      : 'border-transparent text-[#86948a] hover:text-[#dae2fd] hover:bg-[#171f33]/20'
                  ]">
                  <span class="material-symbols-outlined text-[16px] text-amber-500">terminal</span>
                  <span class="truncate">{{ filename }}</span>
                </div>
              </template>

              <!-- FLAT VIEW -->
              <template v-else>
                <div v-for="item in flatFiles" :key="item.folder + '/' + item.filename"
                  @click="selectFile(item.folder, item.filename)" :class="[
                    'flex items-center gap-2 py-1.5 px-2 cursor-pointer transition-colors rounded border-l-2',
                    selectedFolder === item.folder && selectedFile === item.filename
                      ? 'bg-[#171f33] border-[#4edea3] text-[#4edea3]'
                      : 'border-transparent text-[#86948a] hover:text-[#dae2fd] hover:bg-[#171f33]/20'
                  ]">
                  <span class="material-symbols-outlined text-[16px]"
                    :class="item.folder === 'root_files' ? 'text-amber-500' : 'text-sky-400'">
                    {{ item.folder === 'root_files' ? 'terminal' : 'description' }}
                  </span>
                  <span class="truncate text-[12px]">
                    <span class="opacity-50" v-if="item.folder !== 'root_files'">{{ item.folder }}/</span>{{
                      item.filename }}
                  </span>
                </div>
              </template>

            </div>
          </div>

          <!-- Right Panel (File Editor/Viewer) -->
          <div class="lg:col-span-8 flex flex-col bg-[#0b1326]">
            <!-- Tab bar -->
            <div class="flex bg-[#060e20]/80 border-b border-[#3c4a42] text-[12px] font-mono-jb">
              <div
                class="flex items-center gap-2 px-4 py-2 bg-[#0b1326] border-t-2 border-[#4edea3] border-r border-[#3c4a42] text-[#dae2fd]">
                <span class="material-symbols-outlined text-[16px]"
                  :class="selectedFolder === 'root_files' ? 'text-amber-500' : 'text-sky-400'">
                  {{ selectedFolder === 'root_files' ? 'terminal' : 'description' }}
                </span>
                <span>{{ selectedFile }}</span>
                <span @click="selectFile('root_files', 'README.sh')"
                  class="material-symbols-outlined text-[12px] hover:text-[#ff5f56] ml-2 cursor-pointer">close</span>
              </div>
            </div>

            <!-- Editor Body -->
            <div class="flex-grow p-6 md:p-10 text-[#dae2fd] overflow-y-auto space-y-6">
              <!-- Document Title -->
              <div>
                <h1 class="text-3xl font-bold tracking-tight text-[#dae2fd]"># {{ currentFileContent.title }}</h1>
                <p class="text-[12px] text-[#86948a] mt-2 italic font-mono-jb">
                  // Period: {{ currentFileContent.period }} | Location: {{ currentFileContent.location }}
                </p>
              </div>

              <!-- Role -->
              <div v-if="currentFileContent.role" class="pt-2">
                <h2 class="text-lg font-semibold text-[#4edea3] font-mono-jb">
                  ## ROLE: {{ currentFileContent.role }}
                </h2>
                <p class="text-sm text-[#86948a] leading-relaxed mt-2">
                  {{ currentFileContent.description }}
                </p>
              </div>

              <!-- Achievements -->
              <div v-if="currentFileContent.achievements && currentFileContent.achievements.length > 0"
                class="space-y-3">
                <h2 class="text-[13px] font-bold text-[#dae2fd] uppercase tracking-wider font-mono-jb">
                  ## ACHIEVEMENTS
                </h2>
                <ul class="space-y-2">
                  <li v-for="(ach, i) in currentFileContent.achievements" :key="i"
                    class="text-sm text-[#dae2fd] leading-relaxed flex items-start gap-2">
                    <span class="text-[#4edea3] font-bold shrink-0 font-mono-jb">
                      - {{ ach.type }}:
                    </span>
                    <span>{{ ach.desc }}</span>
                  </li>
                </ul>
              </div>

              <!-- Tech Stack -->
              <div v-if="currentFileContent.techStack && currentFileContent.techStack.length > 0"
                class="pt-4 border-t border-[#3c4a42]/30">
                <h2 class="text-[13px] font-bold text-[#dae2fd] uppercase tracking-wider mb-3 font-mono-jb">
                  ## TECH_STACK
                </h2>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tech in currentFileContent.techStack" :key="tech"
                    class="px-3 py-1 border border-[#3c4a42] text-[#86948a] text-[10px] tracking-wider font-semibold rounded hover:border-[#4edea3] hover:text-[#4edea3] transition-colors font-mono-jb">
                    {{ tech }}
                  </span>
                </div>
              </div>

            </div>

            <!-- Editor Footer / Status Bar -->
            <div
              class="px-4 py-1.5 bg-[#060e20] border-t border-[#3c4a42] flex items-center justify-between text-[11px] text-[#86948a] font-mono-jb">
              <div>UTF-8 &nbsp;&nbsp; Line: 1, Col: 1</div>
              <div class="flex items-center gap-3">
                <span class="flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-[#10b981]"></span>
                  SYSTEM_READY
                </span>
                <span>Markdown</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. TIMELINE VIEW -->
        <div v-else class="space-y-8 max-w-3xl mx-auto">
          <div v-for="(folderData, folderKey) in experienceData" :key="folderKey">
            <template v-if="folderKey !== 'root_files'">
              <div v-for="(fileDetail, filename) in folderData.files" :key="filename"
                class="relative pl-8 pb-8 border-l border-[#3c4a42] last:pb-0">
                <!-- Timeline dot -->
                <span
                  class="absolute left-[-5px] top-1.5 w-[10px] h-[10px] rounded-full bg-[#10b981] border border-[#0b1326] shadow-glow"></span>

                <!-- Content card -->
                <div
                  class="bg-[#171f33]/40 border border-[#3c4a42] p-6 hover:border-[#4edea3]/50 transition-all rounded">
                  <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-4">
                    <div>
                      <h3 class="text-xl font-bold text-[#dae2fd]">{{ fileDetail.title }}</h3>
                      <p class="text-xs text-[#4edea3] font-semibold mt-1 font-mono-jb">{{ fileDetail.role }}</p>
                    </div>
                    <div class="text-right">
                      <span class="text-[11px] text-[#86948a] font-mono-jb">{{ fileDetail.period }}</span>
                      <p class="text-[10px] text-[#86948a] opacity-60 font-mono-jb">{{ fileDetail.location }}</p>
                    </div>
                  </div>

                  <p class="text-sm text-[#86948a] leading-relaxed mb-4">
                    {{ fileDetail.description }}
                  </p>

                  <!-- Key Achievements list -->
                  <div class="space-y-2 mb-4">
                    <div v-for="(ach, idx) in fileDetail.achievements" :key="idx"
                      class="text-xs text-[#dae2fd] flex items-start gap-2">
                      <span class="text-[#4edea3] font-bold font-mono-jb">// {{ ach.type }}:</span>
                      <span>{{ ach.desc }}</span>
                    </div>
                  </div>

                  <!-- Tech stack -->
                  <div class="flex flex-wrap gap-1.5 pt-2">
                    <span v-for="tech in fileDetail.techStack" :key="tech"
                      class="px-2 py-0.5 border border-[#3c4a42]/60 text-[#86948a] text-[9px] font-semibold rounded font-mono-jb">
                      {{ tech }}
                    </span>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>

      </section>

      <!-- ── PROJECTS SECTION ── -->
      <section id="projects" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="flex flex-col gap-4 max-w-2xl mb-14">
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] font-mono-jb">//
            PROJECT_REGISTRY
          </p>
          <h2 class="text-4xl font-bold tracking-tight leading-none text-[#dae2fd]">Featured Projects</h2>
          <p class="text-lg text-[#86948a] mt-2">A showcase of full-stack applications, system integrations, and
            developer
            utilities built with precision.</p>
        </div>
        <div class="h-px bg-[#3c4a42] mb-12"></div>

        <div v-if="isLoadingProjects"
          class="flex flex-col items-center justify-center py-20 border border-[#3c4a42]/30 bg-[#060e20]">
          <span class="material-symbols-outlined text-4xl text-[#4edea3] animate-spin mb-4">progress_activity</span>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] font-mono-jb">//
            SYNCING_DEPLOYMENT_REGISTRY...</p>
        </div>
        <div v-else-if="projects.filter(p => p.featured).length === 0"
          class="flex flex-col items-center justify-center py-16 border border-[#3c4a42]/30 bg-[#060e20]">
          <span class="material-symbols-outlined text-4xl text-[#86948a]/40 mb-4">info</span>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] font-mono-jb">//
            NO_ACTIVE_DEPLOYMENTS_FOUND</p>
        </div>
        <div v-else class="flex flex-col gap-6">
          <div v-for="p in projects.filter(p => p.featured)" :key="p.id"
            class="group bg-[#060e20] border border-[#3c4a42] hover:border-[#4edea3] transition-all duration-300 flex flex-col md:flex-row overflow-hidden min-h-[200px]">
            <div class="flex-grow p-8 flex flex-col justify-between">
              <div class="flex flex-col gap-3">
                <div class="flex items-center gap-4">
                  <span
                    class="text-[10px] font-semibold tracking-widest uppercase text-[#4edea3] border border-[#4edea3]/30 px-2 py-0.5 font-mono-jb">STATUS:
                    {{ p.status.toUpperCase() }}</span>
                  <h3 class="text-xl font-semibold text-[#dae2fd]">{{ p.title }}</h3>
                </div>
                <p class="text-[#86948a] max-w-2xl leading-relaxed">{{ p.description }}</p>
              </div>
              <div class="mt-6 flex flex-wrap items-end justify-between gap-4">
                <!-- Techstack rendered as icons -->
                <div class="flex flex-wrap gap-3 items-center">
                  <span
                    class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a] mr-1 font-mono-jb">STACK:</span>
                  <div v-for="tech in p.techstacks" :key="tech.id"
                    class="relative group/stackicon flex items-center justify-center">
                    <img v-if="tech.logo_url" :src="tech.logo_url" :alt="tech.name" loading="lazy"
                      class="h-7 w-7 object-contain hover:scale-110 transition-transform filter brightness-90 hover:brightness-110" />
                    <span v-else
                      class="text-[11px] px-2 py-0.5 bg-[#222a3d] border border-[#3c4a42] text-[#86948a] font-mono-jb">
                      {{ tech.name }}
                    </span>
                    <!-- Tooltip for image logo -->
                    <span
                      class="absolute -top-8 bg-[#171f33] border border-[#3c4a42] text-[#dae2fd] text-[9px] px-2 py-0.5 opacity-0 group-hover/stackicon:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10 shadow-lg font-mono-jb">{{
                        tech.name.toUpperCase() }}</span>
                  </div>
                </div>
                <!-- Break -->
                <div class="w-full"></div>
                <!-- Links -->
                <div class="flex gap-4">
                  <a v-if="p.repo_url" :href="p.repo_url" target="_blank"
                    class="flex items-center gap-1 text-[#86948a] hover:text-[#4edea3] transition-colors text-[11px] font-semibold tracking-widest uppercase font-mono-jb">
                    REPOSITORY <span class="material-symbols-outlined text-base">terminal</span>
                  </a>
                  <a v-if="p.live_url" :href="p.live_url" target="_blank"
                    class="flex items-center gap-1 text-[#86948a] hover:text-[#4edea3] transition-colors text-[11px] font-semibold tracking-widest uppercase font-mono-jb">
                    LIVE_DEMO <span class="material-symbols-outlined text-base">open_in_new</span>
                  </a>
                </div>
              </div>
            </div>
            <!-- Project Image or Fallback Icon -->
            <div
              class="w-full md:w-96 h-52 md:h-auto shrink-0 flex items-center justify-center bg-[#171f33] border-t md:border-t-0 md:border-l border-[#3c4a42] overflow-hidden">
              <img v-if="p.project_img_url" :src="p.project_img_url" :alt="p.title" loading="lazy"
                class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 cursor-zoom-in"
                @click.stop="openLightbox(p.project_img_url!)" />
              <span v-else
                class="material-symbols-outlined text-[#4edea3]/30 text-6xl group-hover:text-[#4edea3]/60 group-hover:scale-110 transition-all duration-300">
                {{ getFallbackIcon(p) }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- ── CONTACT SECTION ── -->
      <section id="contact" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8">
          <div class="md:col-span-8 md:col-start-3">
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-4 font-mono-jb">
              ESTABLISH_CONNECTION</p>
            <h2 class="text-4xl font-bold tracking-tight text-[#dae2fd] mb-8">Reach Out</h2>

            <div class="space-y-6">
              <a v-for="c in contactLinks" :key="c.label" :href="c.href" @click="handleContactClick(c, $event)"
                class="flex items-center gap-4 group border border-[#3c4a42] p-4 hover:border-[#4edea3] transition-colors">
                <span class="material-symbols-outlined text-[#4edea3]">{{ c.icon }}</span>
                <div>
                  <p class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a] opacity-60 font-mono-jb">
                    {{
                      c.label }}</p>
                  <p class="text-base font-semibold text-[#dae2fd] group-hover:text-[#4edea3] transition-colors">{{
                    c.value }}
                  </p>
                </div>
              </a>
            </div>

            <div class="mt-8">
              <button @click="downloadResume"
                class="w-full flex items-center justify-center gap-2 px-8 py-4 border border-[#4edea3] text-[#4edea3] font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3]/10 transition-all duration-300 font-mono-jb">
                <span class="material-symbols-outlined">download</span> DOWNLOAD RESUME/CV
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- ── FOOTER ── -->
    <footer
      class="max-w-[1200px] mx-auto px-5 md:px-16 py-12 border-t border-[#3c4a42] flex flex-col md:flex-row justify-between items-center gap-4 relative z-10">
      <div class="text-[11px] text-[#86948a] opacity-60 font-mono-jb">
        SYS_STATUS: OPERATIONAL // LAST_UPDATED: {{ computedLastUpdated }}
      </div>
      <div class="flex gap-8">
        <a href="https://github.com/kenBeCoded" target="_blank"
          class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors font-mono-jb">GITHUB</a>
        <a href="https://www.linkedin.com/in/johnkennethgregorio" target="_blank"
          class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors font-mono-jb">LINKEDIN</a>
        <a href="mailto:johnkennethgregorio.wom@gmail.com"
          class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors font-mono-jb">GMAIL</a>
      </div>
    </footer>

    <!-- Copy Notification Toast -->
    <Transition enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-y-4 opacity-0" enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in" leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-4 opacity-0">
      <div v-if="showCopyNotification"
        class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 bg-[#171f33] border border-[#4edea3] px-6 py-3 text-sm font-mono-jb text-[#4edea3] flex items-center gap-2">
        <span class="material-symbols-outlined text-[18px]">check_circle</span>
        {{ copyNotificationText }}
      </div>
    </Transition>

    <!-- Image Lightbox -->
    <Transition enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0" enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100"
      leave-to-class="opacity-0">
      <div v-if="lightboxImage"
        class="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 cursor-zoom-out"
        @click="closeLightbox">
        <button @click.stop="closeLightbox"
          class="absolute top-4 right-4 text-white/70 hover:text-white transition-colors"
          aria-label="Close image viewer">
          <span class="material-symbols-outlined text-4xl">close</span>
        </button>
        <img :src="lightboxImage" alt="Project image preview"
          class="max-w-full max-h-[90vh] object-contain shadow-2xl rounded"
          @click.stop />
      </div>
    </Transition>

  </div>
</template>

<style>
/* Color overrides for theme toggling */
.bg-\[\#0b1326\] {
  background-color: var(--background) !important;
}

.bg-\[\#0b1326\]\/80 {
  background-color: color-mix(in srgb, var(--background) 80%, transparent) !important;
}

.bg-\[\#0b1326\]\/95 {
  background-color: color-mix(in srgb, var(--background) 95%, transparent) !important;
}

.text-\[\#dae2fd\] {
  color: var(--on-surface) !important;
}

.bg-\[\#171f33\] {
  background-color: var(--surface) !important;
}

.bg-\[\#171f33\]\/40 {
  background-color: color-mix(in srgb, var(--surface) 40%, transparent) !important;
}

.bg-\[\#171f33\]\/20 {
  background-color: color-mix(in srgb, var(--surface) 20%, transparent) !important;
}

.border-\[\#3c4a42\] {
  border-color: var(--outline) !important;
}

.border-\[\#3c4a42\]\/30 {
  border-color: color-mix(in srgb, var(--outline) 30%, transparent) !important;
}

.text-\[\#86948a\] {
  color: var(--on-surface-variant) !important;
}

.text-\[\#86948a\]\/60 {
  color: color-mix(in srgb, var(--on-surface-variant) 60%, transparent) !important;
}

.text-\[\#86948a\]\/40 {
  color: color-mix(in srgb, var(--on-surface-variant) 40%, transparent) !important;
}

.bg-\[\#060e20\] {
  background-color: var(--surface-low) !important;
}

.bg-\[\#222a3d\] {
  background-color: var(--surface-variant) !important;
}

.text-\[\#4edea3\] {
  color: var(--primary-bright) !important;
}

.border-\[\#4edea3\] {
  border-color: var(--primary-bright) !important;
}

.border-\[\#4edea3\]\/30 {
  border-color: color-mix(in srgb, var(--primary-bright) 30%, transparent) !important;
}

.text-\[\#10b981\] {
  color: var(--primary) !important;
}

.bg-\[\#10b981\] {
  background-color: var(--primary) !important;
}

.bg-\[\#10b981\]\/10 {
  background-color: color-mix(in srgb, var(--primary) 10%, transparent) !important;
}
</style>
