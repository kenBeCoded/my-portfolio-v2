<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { fetchTechStacks, type TechStackOut } from '../services/techStackService'

const activeSection = ref('home')
const mobileMenuOpen = ref(false)

const navLinks = [
  { label: 'Home',     id: 'home'     },
  { label: 'Projects', id: 'projects' },
  { label: 'About',    id: 'about'    },
  { label: 'Contact',  id: 'contact'  },
]

const projects = [
  {
    title: 'Hyperion Gateway', status: 'STABLE',
    desc: 'A distributed API gateway designed for sub-millisecond latency with dynamic rate limiting and automated schema validation.',
    stack: ['React', 'FastAPI', 'Docker', 'Redis'], icon: 'hub',
  },
  {
    title: 'NexusDB', status: 'BETA',
    desc: 'Custom time-series database engine optimized for telemetry data visualization and real-time processing.',
    stack: ['Go', 'gRPC', 'Redis'], icon: 'database',
  },
  {
    title: 'Sentinel Auth', status: 'PRODUCTION',
    desc: 'Zero-trust authentication provider with multi-region support and JWT/OAuth2 integration modules.',
    stack: ['Node.js', 'PostgreSQL', 'JWT'], icon: 'security',
  },
  {
    title: 'Vortex Crawler', status: 'ACTIVE',
    desc: 'High-velocity web scraping engine with proxy rotation and intelligent data extraction strategies.',
    stack: ['Python', 'Redis', 'K8s'], icon: 'travel_explore',
  },
]

const apiTechStacks = ref<TechStackOut[]>([])

const techStack = computed(() => {
  const filterByCategory = (...catPrefixes: string[]) => {
    return apiTechStacks.value
      .filter(t => catPrefixes.some(prefix => t.category.toUpperCase().includes(prefix.toUpperCase())))
      .sort((a, b) => a.sort_order - b.sort_order)
  }

  return [
    { category: 'Languages',        icon: 'code',              items: filterByCategory('LANGUAGE') },
    { category: 'Frontend',         icon: 'layers',            items: filterByCategory('FRONTEND') },
    { category: 'Backend',          icon: 'settings_ethernet', items: filterByCategory('BACKEND') },
    { category: 'Databases',        icon: 'database',          items: filterByCategory('DATABASE') },
    { category: 'Tools & Platforms',icon: 'build',             items: filterByCategory('TOOL'), wide: true },
    { category: 'Other & AI Tools', icon: 'bolt',              items: filterByCategory('OTHER', 'AI'), wide: true, accent: true },
  ]
})

const contactLinks = [
  { label: 'Gmail',    icon: 'mail',     value: 'root@backend.dev',     href: 'mailto:root@backend.dev' },
  { label: 'LinkedIn', icon: 'lan',      value: 'in/technical-profile',  href: '#' },
  { label: 'Facebook', icon: 'public',   value: '/backend.dev',          href: '#' },
  { label: 'GitHub',   icon: 'terminal', value: '/backend_engineer',     href: '#' },
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
  try {
    apiTechStacks.value = await fetchTechStacks()
  } catch (error) {
    console.error('Failed to load tech stacks:', error)
  }
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <div class="bg-[#0b1326] text-[#dae2fd] min-h-screen overflow-x-hidden" style="font-family:'Geist',sans-serif;">

    <!-- Blueprint grid -->
    <div class="fixed inset-0 pointer-events-none z-0"
      style="background-image:linear-gradient(to right,#3c4a42 1px,transparent 1px),linear-gradient(to bottom,#3c4a42 1px,transparent 1px);background-size:40px 40px;opacity:0.07;"></div>

    <!-- ── NAVBAR ── -->
    <header class="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-5 md:px-16 py-4 bg-[#0b1326]/80 backdrop-blur-md border-b border-[#3c4a42]">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-[#10b981] flex items-center justify-center">
          <span class="text-[#003824] font-bold text-xs" style="font-family:'JetBrains Mono',monospace;">&gt;_</span>
        </div>
        <span class="font-bold text-lg tracking-tighter">&lt;BACKEND&gt;</span>
      </div>

      <nav class="hidden md:flex items-center gap-8">
        <button
          v-for="link in navLinks" :key="link.id"
          @click="scrollTo(link.id)"
          :class="[
            'text-[11px] font-semibold tracking-widest uppercase transition-colors',
            'font-[JetBrains_Mono,monospace]',
            activeSection === link.id
              ? 'text-[#4edea3] border-b border-[#4edea3] pb-0.5'
              : 'text-[#86948a] hover:text-[#4edea3]'
          ]"
          style="font-family:'JetBrains Mono',monospace;"
        >{{ link.label }}</button>
      </nav>

      <div class="flex items-center gap-3">
        <a href="/admin/login" class="hidden md:flex items-center gap-1 text-[10px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] transition-colors border border-[#3c4a42] hover:border-[#4edea3] px-3 py-1.5" style="font-family:'JetBrains Mono',monospace;">
          <span class="material-symbols-outlined text-[16px]">lock</span> ADMIN
        </a>
        <button class="md:hidden text-[#4edea3]" @click="mobileMenuOpen = !mobileMenuOpen">
          <span class="material-symbols-outlined">{{ mobileMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
    </header>

    <!-- Mobile Nav -->
    <div v-if="mobileMenuOpen" class="fixed inset-0 z-40 bg-[#0b1326]/95 flex flex-col items-center justify-center gap-8">
      <button v-for="link in navLinks" :key="link.id" @click="scrollTo(link.id)"
        class="text-2xl font-semibold tracking-widest uppercase text-[#dae2fd] hover:text-[#4edea3] transition-colors"
        style="font-family:'JetBrains Mono',monospace;">{{ link.label }}</button>
    </div>

    <main class="relative z-10">

      <!-- ── HERO SECTION ── -->
      <section id="home" class="max-w-[1200px] mx-auto px-5 md:px-16 pt-40 pb-32 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
        <div class="md:col-span-8 flex flex-col gap-8">
          <!-- Status badge -->
          <div class="inline-flex items-center gap-2 px-3 py-1 border border-[#4edea3] text-[#4edea3] w-fit" style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.1em;">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full bg-[#4edea3] opacity-75"></span>
              <span class="relative inline-flex h-2 w-2 bg-[#4edea3]"></span>
            </span>
            SYSTEM_READY // 2025.V1
          </div>

          <h1 class="text-4xl md:text-5xl font-bold tracking-tight leading-tight">
            Aspiring Fullstack Developer building
            <span class="text-[#10b981]"> robust backend systems.</span>
          </h1>

          <p class="text-lg text-[#86948a] max-w-xl leading-relaxed">
            Architecture-first development focused on scalability, data integrity, and the performance of complex logic-driven applications.
          </p>

          <div class="flex flex-wrap gap-4 pt-2">
            <button @click="scrollTo('contact')"
              class="bg-[#10b981] text-[#003824] px-8 py-3 font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3] transition-colors"
              style="font-family:'JetBrains Mono',monospace;">INITIALIZE_CONTACT</button>
            <button @click="scrollTo('projects')"
              class="border border-[#3c4a42] text-[#dae2fd] px-8 py-3 font-semibold tracking-widest uppercase text-[11px] hover:border-[#4edea3] transition-colors"
              style="font-family:'JetBrains Mono',monospace;">VIEW_PROJECTS</button>
          </div>
        </div>

        <!-- Code card -->
        <div class="md:col-span-4 hidden md:block">
          <div class="bg-[#171f33] border border-[#3c4a42] p-6 relative">
            <div class="absolute top-2 right-2 text-[10px] text-[#86948a] opacity-50" style="font-family:'JetBrains Mono',monospace;">SYS_LOG.TS</div>
            <div class="space-y-2 text-[13px]" style="font-family:'JetBrains Mono',monospace;line-height:1.6;">
              <div><span class="text-[#86948a]">01</span> <span class="text-[#4edea3]">interface</span> <span class="text-[#ffb3af]">Developer</span> <span class="text-[#dae2fd]">{</span></div>
              <div><span class="text-[#86948a]">02</span> <span class="text-[#dae2fd] ml-4">focus:</span> <span class="text-[#c2c4e3]">'Backend'</span><span class="text-[#dae2fd]">;</span></div>
              <div><span class="text-[#86948a]">03</span> <span class="text-[#dae2fd] ml-4">stack:</span> <span class="text-[#c2c4e3]">['Node', 'TS', 'Python']</span><span class="text-[#dae2fd]">;</span></div>
              <div><span class="text-[#86948a]">04</span> <span class="text-[#dae2fd] ml-4">status:</span> <span class="text-[#c2c4e3]">'Building'</span><span class="text-[#dae2fd]">;</span></div>
              <div><span class="text-[#86948a]">05</span> <span class="text-[#dae2fd]">}</span></div>
            </div>
            <div class="mt-6 pt-4 border-t border-[#3c4a42] flex justify-between items-center">
              <span class="text-[10px] text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">STABILITY: 99.9%</span>
              <div class="h-1 w-24 bg-[#2d3449] overflow-hidden">
                <div class="h-full bg-[#10b981]" style="width:80%;"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── TECHSTACK SECTION ── -->
      <section id="about" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-14">
          <div>
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-2" style="font-family:'JetBrains Mono',monospace;">// FULL_STACK_INVENTORY</p>
            <h2 class="text-2xl font-semibold text-[#dae2fd]">Engineered Infrastructure</h2>
          </div>
          <div class="text-[11px] text-[#86948a] text-right leading-relaxed" style="font-family:'JetBrains Mono',monospace;">VER_04.22.99<br/>STATUS: OPERATIONAL</div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="t in techStack" :key="t.category"
            :class="['flex flex-col gap-4 p-6 bg-[#171f33]/40 border border-[#3c4a42] hover:border-[#4edea3]/50 transition-colors', t.wide ? 'lg:col-span-2' : '', t.category === 'Other & AI Tools' ? 'lg:col-span-3' : '']"
          >
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined text-[#4edea3]">{{ t.icon }}</span>
              <h3 class="text-[11px] font-semibold tracking-widest uppercase text-[#dae2fd]" style="font-family:'JetBrains Mono',monospace;">{{ t.category }}</h3>
            </div>
            <div class="flex flex-wrap gap-4">
              <template v-for="item in t.items" :key="item.id">
                <div v-if="item.logo_url" class="relative group flex items-center justify-center">
                  <img :src="item.logo_url" :alt="item.name.toUpperCase()"
                    class="h-10 w-10 object-contain hover:scale-110 transition-transform filter brightness-90 hover:brightness-110" />
                  <span class="absolute -top-10 bg-[#171f33] border border-[#3c4a42] text-[#dae2fd] text-[10px] px-3 py-1 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10 shadow-lg" style="font-family:'JetBrains Mono',monospace; letter-spacing: 0.05em;">{{ item.name.toUpperCase() }}</span>
                </div>
                <span v-else
                  :class="[
                    'text-[12px] px-3 py-1 border flex items-center justify-center min-h-[40px]',
                    'font-[JetBrains_Mono,monospace]',
                    t.accent
                      ? 'bg-[#4edea3]/10 border-[#4edea3]/30 text-[#4edea3]'
                      : 'bg-[#171f33] border-[#3c4a42] text-[#86948a]'
                  ]"
                  style="font-family:'JetBrains Mono',monospace;"
                  :title="item.name.toUpperCase()"
                >{{ item.name.toUpperCase() }}</span>
              </template>
            </div>
          </div>
        </div>
      </section>

      <!-- ── PROJECTS SECTION ── -->
      <section id="projects" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="flex flex-col gap-4 max-w-2xl mb-14">
          <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3]" style="font-family:'JetBrains Mono',monospace;">// DEPLOYMENT_REGISTRY</p>
          <h2 class="text-4xl font-bold tracking-tight leading-none text-[#dae2fd]">Curated Production Artifacts</h2>
          <p class="text-lg text-[#86948a] mt-2">A collection of backend systems, distributed architectures, and API frameworks built with precision.</p>
        </div>
        <div class="h-px bg-[#3c4a42] mb-12"></div>

        <div class="flex flex-col gap-6">
          <div
            v-for="p in projects" :key="p.title"
            class="group bg-[#060e20] border border-[#3c4a42] hover:border-[#4edea3] transition-all duration-300 flex flex-col md:flex-row overflow-hidden min-h-[200px]"
          >
            <div class="flex-grow p-8 flex flex-col justify-between">
              <div class="flex flex-col gap-3">
                <div class="flex items-center gap-4">
                  <span class="text-[10px] font-semibold tracking-widest uppercase text-[#4edea3] border border-[#4edea3]/30 px-2 py-0.5" style="font-family:'JetBrains Mono',monospace;">STATUS: {{ p.status }}</span>
                  <h3 class="text-xl font-semibold text-[#dae2fd]">{{ p.title }}</h3>
                </div>
                <p class="text-[#86948a] max-w-2xl leading-relaxed">{{ p.desc }}</p>
              </div>
              <div class="mt-6 flex flex-wrap items-end justify-between gap-4">
                <div class="flex flex-wrap gap-2">
                  <span v-for="s in p.stack" :key="s"
                    class="text-[13px] px-3 py-1 bg-[#222a3d] border border-[#3c4a42] text-[#86948a]"
                    style="font-family:'JetBrains Mono',monospace;">--{{ s }}</span>
                </div>
                <div class="flex items-center gap-2 text-[#86948a] group-hover:text-[#4edea3] transition-colors cursor-pointer text-[11px] font-semibold tracking-widest uppercase" style="font-family:'JetBrains Mono',monospace;">
                  VIEW_DOCUMENTATION <span class="material-symbols-outlined text-lg">arrow_right_alt</span>
                </div>
              </div>
            </div>
            <div class="w-full md:w-56 h-40 md:h-auto shrink-0 flex items-center justify-center bg-[#171f33] border-t md:border-t-0 md:border-l border-[#3c4a42]">
              <span class="material-symbols-outlined text-[#4edea3]/30 text-6xl group-hover:text-[#4edea3]/60 group-hover:scale-110 transition-all duration-300">{{ p.icon }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ── CONTACT SECTION ── -->
      <section id="contact" class="max-w-[1200px] mx-auto px-5 md:px-16 py-24 border-t border-[#3c4a42]">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8">
          <!-- Left -->
          <div class="md:col-span-5">
            <p class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-4" style="font-family:'JetBrains Mono',monospace;">ESTABLISH_CONNECTION</p>
            <h2 class="text-4xl font-bold tracking-tight text-[#dae2fd] mb-8">Reach Out</h2>

            <div class="space-y-4">
              <a v-for="c in contactLinks" :key="c.label" :href="c.href"
                class="flex items-center gap-4 group border border-[#3c4a42] p-4 hover:border-[#4edea3] transition-colors">
                <span class="material-symbols-outlined text-[#4edea3]">{{ c.icon }}</span>
                <div>
                  <p class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a] opacity-60" style="font-family:'JetBrains Mono',monospace;">{{ c.label }}</p>
                  <p class="text-base font-semibold text-[#dae2fd] group-hover:text-[#4edea3] transition-colors">{{ c.value }}</p>
                </div>
              </a>
            </div>

            <button class="mt-8 w-full flex items-center justify-center gap-2 px-8 py-4 border border-[#4edea3] text-[#4edea3] font-semibold tracking-widest uppercase text-[11px] hover:bg-[#4edea3]/10 transition-all duration-300"
              style="font-family:'JetBrains Mono',monospace;">
              <span class="material-symbols-outlined">download</span> DOWNLOAD RESUME/CV
            </button>
          </div>

          <!-- Right: Contact Form -->
          <div class="md:col-span-7">
            <form class="space-y-6 border border-[#3c4a42] p-8 bg-[#060e20]" @submit.prevent>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">User_Identity</label>
                  <input v-model="form.name" type="text" placeholder="Name"
                    class="w-full bg-[#0b1326] border border-[#3c4a42] focus:border-[#4edea3] focus:outline-none text-[#dae2fd] px-4 py-3 placeholder-[#3c4a42]"
                    style="font-family:'JetBrains Mono',monospace;font-size:13px;" />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">Return_Address</label>
                  <input v-model="form.email" type="email" placeholder="Email"
                    class="w-full bg-[#0b1326] border border-[#3c4a42] focus:border-[#4edea3] focus:outline-none text-[#dae2fd] px-4 py-3 placeholder-[#3c4a42]"
                    style="font-family:'JetBrains Mono',monospace;font-size:13px;" />
                </div>
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-semibold tracking-widest uppercase text-[#86948a]" style="font-family:'JetBrains Mono',monospace;">Payload_Data</label>
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
    <footer class="max-w-[1200px] mx-auto px-5 md:px-16 py-12 border-t border-[#3c4a42] flex flex-col md:flex-row justify-between items-center gap-4 relative z-10">
      <div class="text-[11px] text-[#86948a] opacity-60" style="font-family:'JetBrains Mono',monospace;">
        SYS_STATUS: OPERATIONAL // LAST_UPDATED: 2025.05.11
      </div>
      <div class="flex gap-8">
        <a href="#" class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors" style="font-family:'JetBrains Mono',monospace;">GITHUB</a>
        <a href="#" class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors" style="font-family:'JetBrains Mono',monospace;">LINKEDIN</a>
        <a href="#" class="text-[11px] font-semibold tracking-widest uppercase text-[#86948a] hover:text-[#4edea3] underline transition-colors" style="font-family:'JetBrains Mono',monospace;">RSS</a>
      </div>
    </footer>

  </div>
</template>
