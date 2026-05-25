<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { logVisit, getOrCreateVisitorId } from '../services/visitorService'
import { fetchProjects, type ProjectOut } from '../services/projectService'

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
  { label: 'Experience', id: 'about' },
  { label: 'Projects', id: 'projects' },
  { label: 'Contact', id: 'contact' },
]

const projects = ref<ProjectOut[]>([])

interface ExperienceDetail {
  title: string
  period: string
  location: string
  role: string
  description: string
  achievements: { type: string; desc: string }[]
  techStack: string[]
}

const experienceData: Record<string, { companyName: string; folderName: string; files: Record<string, ExperienceDetail> }> = {
  nexGen_systems: {
    companyName: 'NexGen Systems',
    folderName: 'nexGen_systems',
    files: {
      'Lead_Architect.md': {
        title: 'NexGen Systems',
        period: '2021 - Present',
        location: 'Remote/Global',
        role: 'Lead Solution Architect',
        description: 'Spearheaded the migration of legacy monolithic architecture to a high-availability microservices mesh, reducing system latency by 42% and operational overhead by $1.2M annually.',
        achievements: [
          { type: 'PROCESSED', desc: 'Engineered a real-time data pipeline handling 4.5M events/sec using Kafka and Rust.' },
          { type: 'SCALED', desc: 'Automated CI/CD workflows for 120+ microservices using Kubernetes and custom Go operators.' },
          { type: 'SECURED', desc: 'Implemented Zero-Trust security protocols across all internal API gateways.' }
        ],
        techStack: ['RUST', 'GO', 'KUBERNETES', 'AWS']
      },
      'Senior_Dev.md': {
        title: 'NexGen Systems',
        period: '2018 - 2021',
        location: 'On-site / Tech City',
        role: 'Senior Backend Developer',
        description: 'Designed and optimized high-performance database schemas and REST/gRPC APIs, handling peak traffic spikes during major system operations.',
        achievements: [
          { type: 'OPTIMIZED', desc: 'Reduced database query response times by 60% through query refactoring and Redis caching.' },
          { type: 'BUILT', desc: 'Developed a distributed event logging service processing 10k messages per second.' },
          { type: 'MIGRATED', desc: 'Successfully phased out 3 legacy subsystems into modular internal packages.' }
        ],
        techStack: ['NODE.JS', 'TYPESCRIPT', 'POSTGRESQL', 'REDIS']
      }
    }
  },
  cloud_core_labs: {
    companyName: 'Cloud Core Labs',
    folderName: 'cloud_core_labs',
    files: {
      'Infrastructure_Lead.md': {
        title: 'Cloud Core Labs',
        period: '2016 - 2018',
        location: 'Hybrid / Headquarters',
        role: 'Infrastructure & DevOps Lead',
        description: 'Managed cloud infrastructure reliability, multi-region failovers, and DevOps tooling pipelines.',
        achievements: [
          { type: 'AUTOMATED', desc: 'Wrote custom Terraform scripts reducing cloud deployment time from hours to 8 minutes.' },
          { type: 'MONITORED', desc: 'Configured Prometheus and Grafana stacks for detailed container metrics and alert systems.' },
          { type: 'SCALED', desc: 'Scaled AWS ECS clusters to handle over 150 million API requests daily.' }
        ],
        techStack: ['TERRAFORM', 'AWS', 'DOCKER', 'PROMETHEUS']
      }
    }
  },
  stealth_startup: {
    companyName: 'Stealth Startup',
    folderName: 'stealth_startup',
    files: {
      'Backend_Engineer.md': {
        title: 'Stealth Startup',
        period: '2015 - 2016',
        location: 'On-site / Startup Lab',
        role: 'Founding Backend Engineer',
        description: 'Core contributor to early-stage MVP product development, backend architecture, and third-party integrations.',
        achievements: [
          { type: 'LAUNCHED', desc: 'Built and shipped the version 1.0 API in 3 months using Python and FastAPI.' },
          { type: 'INTEGRATED', desc: 'Connected Stripe payments, SendGrid email, and Twilio alerts natively.' },
          { type: 'SECURED', desc: 'Implemented OAuth2 and JWT-based authentication system from scratch.' }
        ],
        techStack: ['PYTHON', 'FASTAPI', 'POSTGRESQL', 'STRIPE']
      }
    }
  },
  root_files: {
    companyName: 'Root',
    folderName: '',
    files: {
      'README.sh': {
        title: 'Career Summary Overview',
        period: '2015 - Present',
        location: 'Global',
        role: 'Fullstack / Systems Engineer',
        description: 'Welcome to the career logs explorer. Click on the company folders or specific role files in the tree hierarchy to view standard markdown outputs detailing structural roles, system accomplishments, and tech stacks.',
        achievements: [
          { type: 'EXPERIENCED', desc: 'Over 8+ years architecting scalable backends, database schemas, and microservice meshes.' },
          { type: 'VERSATILE', desc: 'Proficient in systems languages (Rust, Go), web development (TypeScript, Node), and infrastructure (AWS, K8s).' }
        ],
        techStack: ['RUST', 'GO', 'TYPESCRIPT', 'PYTHON', 'AWS', 'KUBERNETES']
      }
    }
  }
}

const selectedFolder = ref('nexGen_systems')
const selectedFile = ref('Lead_Architect.md')
const isFlatView = ref(false)
const viewMode = ref<'explorer' | 'timeline'>('explorer')

const expandedFolders = ref<Record<string, boolean>>({
  nexGen_systems: true,
  cloud_core_labs: true,
  stealth_startup: true
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

const isLoadingProjects = ref(true)

const contactLinks = [
  { label: 'Gmail', icon: 'mail', value: 'root@backend.dev', href: 'mailto:root@backend.dev' },
  { label: 'LinkedIn', icon: 'lan', value: 'in/technical-profile', href: '#' },
  { label: 'Facebook', icon: 'public', value: '/backend.dev', href: '#' },
  { label: 'GitHub', icon: 'terminal', value: '/backend_engineer', href: '#' },
]

const form = ref({ name: '', email: '', message: '' })

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
  mobileMenuOpen.value = false
}

function onScroll() {
  for (const link of [...navLinks].reverse()) {
    const el = document.getElementById(link.id)
    if (el && window.scrollY >= el.offsetTop - 100) {
      activeSection.value = link.id
      break
    }
  }
}

onMounted(async () => {
  window.addEventListener('scroll', onScroll)

  // ── Visitor tracking (once per browser session) ──────────────────────────
  // Uses sessionStorage flag to prevent duplicate logs on refresh/navigation.
  // All errors are silently swallowed to guarantee no UX impact.
  try {
    if (!sessionStorage.getItem('portfolio_visited')) {
      const visitorId = getOrCreateVisitorId()
      await logVisit(visitorId, window.location.pathname, document.referrer)
      sessionStorage.setItem('portfolio_visited', 'true')
    }
  } catch {
    // Intentionally silent
  }

  // ── Projects data ─────────────────────────────────────────────────────────
  isLoadingProjects.value = true
  try {
    projects.value = await fetchProjects()
  } catch (error) {
    console.error('Failed to load projects:', error)
  } finally {
    isLoadingProjects.value = false
  }
  // ── Theme initialization ─────────────────────────────────────────────────
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'light') {
    isDarkMode.value = false
    document.documentElement.classList.add('light')
  } else if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.documentElement.classList.remove('light')
  } else {
    isDarkMode.value = !document.documentElement.classList.contains('light')
  }
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
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
          <span class="text-[#003824] font-bold text-xs" style="font-family:'JetBrains Mono',monospace;">&gt;_</span>
        </div>
        <span class="font-bold text-lg tracking-tighter">&lt;BACKEND&gt;</span>
      </div>

      <nav class="hidden md:flex items-center gap-8">
        <button v-for="link in navLinks" :key="link.id" @click="scrollTo(link.id)" :class="[
          'text-[11px] font-semibold tracking-widest uppercase transition-colors',
          'font-[JetBrains_Mono,monospace]',
          activeSection === link.id
            ? 'text-[#4edea3] border-b border-[#4edea3] pb-0.5'
            : 'text-[#86948a] hover:text-[#4edea3]'
        ]" style="font-family:'JetBrains Mono',monospace;">{{ link.label }}</button>
      </nav>

      <div class="flex items-center gap-3">
        <!-- Theme Toggle Button -->
        <button @click="toggleTheme"
          class="flex items-center justify-center text-[#86948a] hover:text-[#4edea3] transition-colors p-1.5 border border-[#3c4a42] hover:border-[#4edea3] cursor-pointer"
          title="Toggle Dark/Light Mode">
          <span class="material-symbols-outlined text-[18px]">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>

        <a href="#"
          class="hidden md:flex items-center gap-1.5 text-[10px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] transition-colors border border-[#3c4a42] hover:border-[#4edea3] px-3 py-1.5"
          style="font-family:'JetBrains Mono',monospace;">
          <span class="material-symbols-outlined text-[16px]">download</span> DOWNLOAD RESUME/CV
        </a>
        <button class="md:hidden text-[#4edea3]" @click="mobileMenuOpen = !mobileMenuOpen">
          <span class="material-symbols-outlined">{{ mobileMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
    </header>

    <!-- Mobile Nav -->
    <div v-if="mobileMenuOpen"
      class="fixed inset-0 z-40 bg-[#0b1326]/95 flex flex-col items-center justify-center gap-8">
      <button v-for="link in navLinks" :key="link.id" @click="scrollTo(link.id)"
        class="text-2xl font-semibold tracking-widest uppercase text-[#dae2fd] hover:text-[#4edea3] transition-colors"
        style="font-family:'JetBrains Mono',monospace;">{{ link.label }}</button>
    </div>

    <main class="relative z-10">

      <!-- ── HERO SECTION ── -->
      <section id="home"
        class="max-w-[1200px] mx-auto px-5 md:px-16 pt-40 pb-32 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
        <div class="md:col-span-8 flex flex-col gap-8">
          <h1 class="text-4xl md:text-5xl font-bold tracking-wider text-[#4edea3]"
            style="font-family:'JetBrains Mono',monospace;">
            // WHO_AM_I
          </h1>

          <p class="text-lg text-[#dae2fd] max-w-2xl leading-relaxed" style="font-family:'JetBrains Mono',monospace;">
            I am an aspiring <span class="text-[#4edea3]">Fullstack Developer</span> architecting the future
            of robust backend systems. My journey is defined by a relentless pursuit of
            engineering excellence, moving beyond simple features into the realm of distributed scalability and
            high-availability infrastructures.
          </p>

          <div class="flex flex-wrap gap-4 pt-2">
            <button @click="scrollTo('contact')"
              class="bg-[#10b981] text-[#003824] px-8 py-3 font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3] transition-colors"
              style="font-family:'JetBrains Mono',monospace;">INITIALIZE_CONTACT</button>
            <button @click="scrollTo('projects')"
              class="border border-[#3c4a42] text-[#dae2fd] px-8 py-3 font-semibold tracking-widest uppercase text-[11px] hover:border-[#4edea3] transition-colors"
              style="font-family:'JetBrains Mono',monospace;">VIEW_REPOSITORY</button>
          </div>
        </div>

        <!-- Code card -->
        <div class="md:col-span-4 hidden md:block">
          <div class="bg-[#171f33] border border-[#3c4a42] p-6 relative">
            <div class="absolute top-2 right-2 text-[10px] text-[#86948a] opacity-50"
              style="font-family:'JetBrains Mono',monospace;">SYS_LOG.TS</div>
            <div class="space-y-2 text-[13px]" style="font-family:'JetBrains Mono',monospace;line-height:1.6;">
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
              <span class="text-[10px] text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">STABILITY:
                99.9%</span>
              <div class="h-1 w-24 bg-[#2d3449] overflow-hidden">
                <div class="h-full bg-[#10b981]" style="width:80%;"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── EXPERIENCE SECTION ── -->
      <section id="about" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
          <div>
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-2"
              style="font-family:'JetBrains Mono',monospace;">// WORK_HISTORY_LOGS</p>
            <h2 class="text-3xl font-bold tracking-tight text-[#dae2fd]">Professional Experience</h2>
          </div>

          <!-- Layout View Switcher -->
          <div class="flex items-center border border-[#3c4a42] p-1 bg-[#171f33]/40"
            style="font-family:'JetBrains Mono',monospace;">
            <button @click="viewMode = 'explorer'"
              :class="['px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider transition-colors cursor-pointer', viewMode === 'explorer' ? 'bg-[#10b981] text-[#003824]' : 'text-[#86948a] hover:text-[#dae2fd]']">
              Explorer View
            </button>
            <button @click="viewMode = 'timeline'"
              :class="['px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider transition-colors cursor-pointer', viewMode === 'timeline' ? 'bg-[#10b981] text-[#003824]' : 'text-[#86948a] hover:text-[#dae2fd]']">
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
                <span class="text-[11px] font-semibold tracking-wider text-[#86948a] uppercase ml-2"
                  style="font-family:'JetBrains Mono',monospace;">Explorer</span>
              </div>

              <!-- Folder Structure Design Toggle Button -->
              <button @click="isFlatView = !isFlatView"
                class="text-[#86948a] hover:text-[#4edea3] transition-colors p-1 cursor-pointer flex items-center gap-1 text-[10px] border border-[#3c4a42] px-2"
                style="font-family:'JetBrains Mono',monospace;" title="Toggle Tree / Flat Folder Structure">
                <span class="material-symbols-outlined text-[14px]">{{ isFlatView ? 'account_tree' :
                  'format_list_bulleted' }}</span>
                <span>{{ isFlatView ? 'Tree' : 'Flat' }}</span>
              </button>
            </div>

            <!-- Directory path indicator -->
            <div class="px-4 py-2 text-[11px] font-semibold text-[#4edea3] bg-[#0b1326]/40 border-b border-[#3c4a42]/30"
              style="font-family:'JetBrains Mono',monospace;">
              /career/
            </div>

            <!-- Folder list -->
            <div class="flex-grow overflow-y-auto p-2 space-y-1 select-none font-[JetBrains_Mono,monospace]"
              style="font-family:'JetBrains Mono',monospace; font-size: 13px;">

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
            <div class="flex bg-[#060e20]/80 border-b border-[#3c4a42] text-[12px]"
              style="font-family:'JetBrains Mono',monospace;">
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
                <p class="text-[12px] text-[#86948a] mt-2 italic font-[JetBrains_Mono,monospace]"
                  style="font-family:'JetBrains Mono',monospace;">
                  // Period: {{ currentFileContent.period }} | Location: {{ currentFileContent.location }}
                </p>
              </div>

              <!-- Role -->
              <div v-if="currentFileContent.role" class="pt-2">
                <h2 class="text-lg font-semibold text-[#4edea3] font-[JetBrains_Mono,monospace]"
                  style="font-family:'JetBrains Mono',monospace;">
                  ## ROLE: {{ currentFileContent.role }}
                </h2>
                <p class="text-sm text-[#86948a] leading-relaxed mt-2">
                  {{ currentFileContent.description }}
                </p>
              </div>

              <!-- Achievements -->
              <div v-if="currentFileContent.achievements && currentFileContent.achievements.length > 0"
                class="space-y-3">
                <h2
                  class="text-[13px] font-bold text-[#dae2fd] uppercase tracking-wider font-[JetBrains_Mono,monospace]"
                  style="font-family:'JetBrains Mono',monospace;">
                  ## ACHIEVEMENTS
                </h2>
                <ul class="space-y-2">
                  <li v-for="(ach, i) in currentFileContent.achievements" :key="i"
                    class="text-sm text-[#dae2fd] leading-relaxed flex items-start gap-2">
                    <span class="text-[#4edea3] font-bold shrink-0 font-[JetBrains_Mono,monospace]"
                      style="font-family:'JetBrains Mono',monospace;">
                      - {{ ach.type }}:
                    </span>
                    <span>{{ ach.desc }}</span>
                  </li>
                </ul>
              </div>

              <!-- Tech Stack -->
              <div v-if="currentFileContent.techStack && currentFileContent.techStack.length > 0"
                class="pt-4 border-t border-[#3c4a42]/30">
                <h2
                  class="text-[13px] font-bold text-[#dae2fd] uppercase tracking-wider mb-3 font-[JetBrains_Mono,monospace]"
                  style="font-family:'JetBrains Mono',monospace;">
                  ## TECH_STACK
                </h2>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tech in currentFileContent.techStack" :key="tech"
                    class="px-3 py-1 border border-[#3c4a42] text-[#86948a] text-[10px] tracking-wider font-semibold rounded hover:border-[#4edea3] hover:text-[#4edea3] transition-colors font-[JetBrains_Mono,monospace]"
                    style="font-family:'JetBrains Mono',monospace;">
                    {{ tech }}
                  </span>
                </div>
              </div>

            </div>

            <!-- Editor Footer / Status Bar -->
            <div
              class="px-4 py-1.5 bg-[#060e20] border-t border-[#3c4a42] flex items-center justify-between text-[11px] text-[#86948a] font-[JetBrains_Mono,monospace]"
              style="font-family:'JetBrains Mono',monospace;">
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
                      <p class="text-xs text-[#4edea3] font-semibold mt-1 font-[JetBrains_Mono,monospace]"
                        style="font-family:'JetBrains Mono',monospace;">{{ fileDetail.role }}</p>
                    </div>
                    <div class="text-right">
                      <span class="text-[11px] text-[#86948a] font-[JetBrains_Mono,monospace]"
                        style="font-family:'JetBrains Mono',monospace;">{{ fileDetail.period }}</span>
                      <p class="text-[10px] text-[#86948a] opacity-60 font-[JetBrains_Mono,monospace]"
                        style="font-family:'JetBrains Mono',monospace;">{{ fileDetail.location }}</p>
                    </div>
                  </div>

                  <p class="text-sm text-[#86948a] leading-relaxed mb-4">
                    {{ fileDetail.description }}
                  </p>

                  <!-- Key Achievements list -->
                  <div class="space-y-2 mb-4">
                    <div v-for="(ach, idx) in fileDetail.achievements" :key="idx"
                      class="text-xs text-[#dae2fd] flex items-start gap-2">
                      <span class="text-[#4edea3] font-bold font-[JetBrains_Mono,monospace]"
                        style="font-family:'JetBrains Mono',monospace;">// {{ ach.type }}:</span>
                      <span>{{ ach.desc }}</span>
                    </div>
                  </div>

                  <!-- Tech stack -->
                  <div class="flex flex-wrap gap-1.5 pt-2">
                    <span v-for="tech in fileDetail.techStack" :key="tech"
                      class="px-2 py-0.5 border border-[#3c4a42]/60 text-[#86948a] text-[9px] font-semibold rounded font-[JetBrains_Mono,monospace]"
                      style="font-family:'JetBrains Mono',monospace;">
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
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3]"
            style="font-family:'JetBrains Mono',monospace;">// DEPLOYMENT_REGISTRY</p>
          <h2 class="text-4xl font-bold tracking-tight leading-none text-[#dae2fd]">Curated Production Artifacts</h2>
          <p class="text-lg text-[#86948a] mt-2">A collection of backend systems, distributed architectures, and API
            frameworks built with precision.</p>
        </div>
        <div class="h-px bg-[#3c4a42] mb-12"></div>

        <div v-if="isLoadingProjects"
          class="flex flex-col items-center justify-center py-20 border border-[#3c4a42]/30 bg-[#060e20]">
          <span class="material-symbols-outlined text-4xl text-[#4edea3] animate-spin mb-4">progress_activity</span>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a]"
            style="font-family:'JetBrains Mono',monospace;">// SYNCING_DEPLOYMENT_REGISTRY...</p>
        </div>
        <div v-else-if="projects.length === 0"
          class="flex flex-col items-center justify-center py-16 border border-[#3c4a42]/30 bg-[#060e20]">
          <span class="material-symbols-outlined text-4xl text-[#86948a]/40 mb-4">info</span>
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a]"
            style="font-family:'JetBrains Mono',monospace;">// NO_ACTIVE_DEPLOYMENTS_FOUND</p>
        </div>
        <div v-else class="flex flex-col gap-6">
          <div v-for="p in projects" :key="p.id"
            class="group bg-[#060e20] border border-[#3c4a42] hover:border-[#4edea3] transition-all duration-300 flex flex-col md:flex-row overflow-hidden min-h-[200px]">
            <div class="flex-grow p-8 flex flex-col justify-between">
              <div class="flex flex-col gap-3">
                <div class="flex items-center gap-4">
                  <span
                    class="text-[10px] font-semibold tracking-widest uppercase text-[#4edea3] border border-[#4edea3]/30 px-2 py-0.5"
                    style="font-family:'JetBrains Mono',monospace;">STATUS: {{ p.status.toUpperCase() }}</span>
                  <h3 class="text-xl font-semibold text-[#dae2fd]">{{ p.title }}</h3>
                </div>
                <p class="text-[#86948a] max-w-2xl leading-relaxed">{{ p.description }}</p>
              </div>
              <div class="mt-6 flex flex-wrap items-end justify-between gap-4">
                <!-- Techstack rendered as icons -->
                <div class="flex flex-wrap gap-3 items-center">
                  <span class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a] mr-1"
                    style="font-family:'JetBrains Mono',monospace;">STACK:</span>
                  <div v-for="tech in p.techstacks" :key="tech.id"
                    class="relative group/stackicon flex items-center justify-center">
                    <img v-if="tech.logo_url" :src="tech.logo_url" :alt="tech.name"
                      class="h-7 w-7 object-contain hover:scale-110 transition-transform filter brightness-90 hover:brightness-110" />
                    <span v-else
                      class="text-[11px] px-2 py-0.5 bg-[#222a3d] border border-[#3c4a42] text-[#86948a] font-[JetBrains_Mono,monospace]"
                      style="font-family:'JetBrains Mono',monospace;">
                      {{ tech.name }}
                    </span>
                    <!-- Tooltip for image logo -->
                    <span
                      class="absolute -top-8 bg-[#171f33] border border-[#3c4a42] text-[#dae2fd] text-[9px] px-2 py-0.5 opacity-0 group-hover/stackicon:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10 shadow-lg font-[JetBrains_Mono,monospace]"
                      style="font-family:'JetBrains Mono',monospace;">{{ tech.name.toUpperCase() }}</span>
                  </div>
                </div>
                <!-- Break -->
                <div class="w-full"></div>
                <!-- Links -->
                <div class="flex gap-4">
                  <a v-if="p.repo_url" :href="p.repo_url" target="_blank"
                    class="flex items-center gap-1 text-[#86948a] hover:text-[#4edea3] transition-colors text-[11px] font-semibold tracking-widest uppercase"
                    style="font-family:'JetBrains Mono',monospace;">
                    REPOSITORY <span class="material-symbols-outlined text-base">terminal</span>
                  </a>
                  <a v-if="p.live_url" :href="p.live_url" target="_blank"
                    class="flex items-center gap-1 text-[#86948a] hover:text-[#4edea3] transition-colors text-[11px] font-semibold tracking-widest uppercase"
                    style="font-family:'JetBrains Mono',monospace;">
                    LIVE_DEMO <span class="material-symbols-outlined text-base">open_in_new</span>
                  </a>
                </div>
              </div>
            </div>
            <!-- Project Image or Fallback Icon -->
            <div
              class="w-full md:w-56 h-40 md:h-auto shrink-0 flex items-center justify-center bg-[#171f33] border-t md:border-t-0 md:border-l border-[#3c4a42] overflow-hidden">
              <img v-if="p.project_img_url" :src="p.project_img_url" :alt="p.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
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
          <!-- Left -->
          <div class="md:col-span-5">
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-4"
              style="font-family:'JetBrains Mono',monospace;">ESTABLISH_CONNECTION</p>
            <h2 class="text-4xl font-bold tracking-tight text-[#dae2fd] mb-8">Reach Out</h2>

            <div class="space-y-4">
              <a v-for="c in contactLinks" :key="c.label" :href="c.href"
                class="flex items-center gap-4 group border border-[#3c4a42] p-4 hover:border-[#4edea3] transition-colors">
                <span class="material-symbols-outlined text-[#4edea3]">{{ c.icon }}</span>
                <div>
                  <p class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a] opacity-60"
                    style="font-family:'JetBrains Mono',monospace;">{{ c.label }}</p>
                  <p class="text-base font-semibold text-[#dae2fd] group-hover:text-[#4edea3] transition-colors">{{
                    c.value }}
                  </p>
                </div>
              </a>
            </div>

            <button
              class="mt-8 w-full flex items-center justify-center gap-2 px-8 py-4 border border-[#4edea3] text-[#4edea3] font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3]/10 transition-all duration-300"
              style="font-family:'JetBrains Mono',monospace;">
              <span class="material-symbols-outlined">download</span> DOWNLOAD RESUME/CV
            </button>
          </div>

          <!-- Right: Contact Form -->
          <div class="md:col-span-7">
            <form class="space-y-6 border border-[#3c4a42] p-8 bg-[#060e20]" @submit.prevent>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]"
                    style="font-family:'JetBrains Mono',monospace;">User_Identity</label>
                  <input v-model="form.name" type="text" placeholder="Name"
                    class="w-full bg-[#0b1326] border border-[#3c4a42] focus:border-[#4edea3] focus:outline-none text-[#dae2fd] px-4 py-3 placeholder-[#3c4a42]"
                    style="font-family:'JetBrains Mono',monospace;font-size:13px;" />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]"
                    style="font-family:'JetBrains Mono',monospace;">Return_Address</label>
                  <input v-model="form.email" type="email" placeholder="Email"
                    class="w-full bg-[#0b1326] border border-[#3c4a42] focus:border-[#4edea3] focus:outline-none text-[#dae2fd] px-4 py-3 placeholder-[#3c4a42]"
                    style="font-family:'JetBrains Mono',monospace;font-size:13px;" />
                </div>
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]"
                  style="font-family:'JetBrains Mono',monospace;">Payload_Data</label>
                <textarea v-model="form.message" rows="6" placeholder="Your message here..."
                  class="w-full bg-[#0b1326] border border-[#3c4a42] focus:border-[#4edea3] focus:outline-none text-[#dae2fd] px-4 py-3 placeholder-[#3c4a42] resize-none"
                  style="font-family:'JetBrains Mono',monospace;font-size:13px;"></textarea>
              </div>
              <button type="submit"
                class="flex items-center gap-2 px-10 py-4 bg-[#10b981] text-[#003824] font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3] transition-colors"
                style="font-family:'JetBrains Mono',monospace;">
                POST /SEND_MESSAGE <span class="material-symbols-outlined">send</span>
              </button>
            </form>
          </div>
        </div>
      </section>
    </main>

    <!-- ── FOOTER ── -->
    <footer
      class="max-w-[1200px] mx-auto px-5 md:px-16 py-12 border-t border-[#3c4a42] flex flex-col md:flex-row justify-between items-center gap-4 relative z-10">
      <div class="text-[11px] text-[#86948a] opacity-60" style="font-family:'JetBrains Mono',monospace;">
        SYS_STATUS: OPERATIONAL // LAST_UPDATED: 2025.05.11
      </div>
      <div class="flex gap-8">
        <a href="#"
          class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors"
          style="font-family:'JetBrains Mono',monospace;">GITHUB</a>
        <a href="#"
          class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors"
          style="font-family:'JetBrains Mono',monospace;">LINKEDIN</a>
        <a href="#"
          class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors"
          style="font-family:'JetBrains Mono',monospace;">RSS</a>
      </div>
    </footer>

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
