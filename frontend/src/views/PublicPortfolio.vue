<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { 
  Github, 
  ExternalLink, 
  Code2, 
  Palette, 
  Zap, 
  Layers,
  ArrowRight
} from 'lucide-vue-next'

const projects = ref([
  {
    title: 'Modern Portfolio',
    description: 'A premium portfolio built with Vue 3, Vite, and Tailwind CSS v4.',
    tags: ['Vue 3', 'TypeScript', 'Tailwind'],
    link: '#'
  },
  {
    title: 'E-commerce API',
    description: 'High-performance backend services built with FastAPI and PostgreSQL.',
    tags: ['FastAPI', 'Python', 'SQL'],
    link: '#'
  }
])

const backendStatus = ref('Checking...')

onMounted(async () => {
  try {
    // This is just a placeholder to show axios works
    // In a real app, this would be your backend URL
    // const response = await axios.get('http://localhost:8000/health')
    // backendStatus.value = response.data.status
    backendStatus.value = 'Ready'
  } catch (err) {
    backendStatus.value = 'Disconnected'
  }
})
</script>

<template>
  <div class="min-h-screen bg-neutral-950 text-neutral-100 selection:bg-purple-500/30">
    <!-- Navbar -->
    <nav class="sticky top-0 z-50 border-b border-neutral-800/50 bg-neutral-950/80 backdrop-blur-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-gradient-to-tr from-purple-600 to-blue-500 rounded-lg flex items-center justify-center">
              <Code2 class="w-5 h-5 text-white" />
            </div>
            <span class="font-bold text-xl tracking-tight bg-gradient-to-r from-white to-neutral-400 bg-clip-text text-transparent">
              Portfolio
            </span>
          </div>
          <div class="hidden md:flex items-center gap-8 text-sm font-medium text-neutral-400">
            <a href="#" class="hover:text-white transition-colors">Projects</a>
            <a href="#" class="hover:text-white transition-colors">Tech Stack</a>
            <a href="#" class="hover:text-white transition-colors">About</a>
            <a href="https://github.com" target="_blank" class="flex items-center gap-2 px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-full transition-all border border-neutral-700">
              <Github class="w-4 h-4" />
              GitHub
            </a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
      <div class="relative">
        <div class="absolute -top-24 -left-24 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl opacity-50 animate-pulse"></div>
        <div class="absolute -bottom-24 -right-24 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl opacity-50 animate-pulse"></div>
        
        <div class="relative space-y-8 max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-neutral-900 border border-neutral-800 text-xs font-semibold text-purple-400">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
            </span>
            Available for new projects
          </div>
          
          <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight leading-tight">
            Building digital 
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-emerald-400">
              experiences
            </span> 
            that matter.
          </h1>
          
          <p class="text-lg md:text-xl text-neutral-400 leading-relaxed max-w-2xl">
            A full-stack developer specializing in modern web technologies. 
            Backend powered by Python, Frontend crafted with Vue 3.
          </p>

          <div class="flex flex-wrap gap-4 pt-4">
            <button class="px-8 py-4 bg-white text-black font-bold rounded-2xl hover:scale-105 transition-transform flex items-center gap-2">
              View Work
              <ArrowRight class="w-5 h-5" />
            </button>
            <button class="px-8 py-4 bg-neutral-900 text-white font-bold rounded-2xl border border-neutral-800 hover:bg-neutral-800 transition-colors flex items-center gap-2">
              Get in Touch
            </button>
          </div>
        </div>
      </div>

      <!-- Features Grid -->
      <section class="mt-32 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="p-8 rounded-3xl bg-neutral-900/50 border border-neutral-800 hover:border-purple-500/50 transition-colors group">
          <div class="w-12 h-12 bg-purple-500/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Zap class="w-6 h-6 text-purple-400" />
          </div>
          <h3 class="text-xl font-bold mb-3">High Performance</h3>
          <p class="text-neutral-400">Optimized for speed using Vite and modern build tools.</p>
        </div>
        
        <div class="p-8 rounded-3xl bg-neutral-900/50 border border-neutral-800 hover:border-blue-500/50 transition-colors group">
          <div class="w-12 h-12 bg-blue-500/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Layers class="w-6 h-6 text-blue-400" />
          </div>
          <h3 class="text-xl font-bold mb-3">Modular Design</h3>
          <p class="text-neutral-400">Clean architecture with reusable Vue components.</p>
        </div>
        
        <div class="p-8 rounded-3xl bg-neutral-900/50 border border-neutral-800 hover:border-emerald-500/50 transition-colors group">
          <div class="w-12 h-12 bg-emerald-500/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Palette class="w-6 h-6 text-emerald-400" />
          </div>
          <h3 class="text-xl font-bold mb-3">Premium UI</h3>
          <p class="text-neutral-400">Modern aesthetics with Tailwind CSS v4 and Lucide icons.</p>
        </div>
      </section>

      <!-- Projects Section -->
      <section class="mt-32 space-y-12">
        <div class="flex items-end justify-between">
          <div class="space-y-4">
            <h2 class="text-3xl md:text-4xl font-bold">Featured Projects</h2>
            <p class="text-neutral-400">Selected work from my professional journey.</p>
          </div>
          <a href="#" class="text-purple-400 hover:text-purple-300 font-semibold flex items-center gap-1 transition-colors">
            See all projects <ArrowRight class="w-4 h-4" />
          </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div v-for="project in projects" :key="project.title" class="group relative overflow-hidden rounded-3xl bg-neutral-900 border border-neutral-800">
            <div class="aspect-video bg-gradient-to-br from-neutral-800 to-neutral-900 p-8 flex items-center justify-center">
              <div class="w-20 h-20 bg-white/5 rounded-full blur-xl group-hover:scale-150 transition-transform duration-700"></div>
              <Code2 class="w-16 h-16 text-neutral-700 group-hover:text-neutral-500 transition-colors" />
            </div>
            <div class="p-8 space-y-4">
              <div class="flex gap-2">
                <span v-for="tag in project.tags" :key="tag" class="text-[10px] uppercase tracking-wider font-bold px-2 py-1 bg-neutral-800 text-neutral-400 rounded-md">
                  {{ tag }}
                </span>
              </div>
              <h3 class="text-2xl font-bold">{{ project.title }}</h3>
              <p class="text-neutral-400 leading-relaxed">{{ project.description }}</p>
              <a :href="project.link" class="inline-flex items-center gap-2 text-sm font-bold text-white group/link">
                View Project 
                <ExternalLink class="w-4 h-4 group-hover/link:translate-x-1 group-hover/link:-translate-y-1 transition-transform" />
              </a>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="mt-32 border-t border-neutral-900 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="text-sm text-neutral-500">
          © 2026 Portfolio. Built with Vue 3 & Tailwind v4.
        </div>
        <div class="flex items-center gap-6">
          <div class="flex items-center gap-2 text-xs">
            <span class="w-2 h-2 rounded-full" :class="backendStatus === 'Ready' ? 'bg-emerald-500' : 'bg-amber-500'"></span>
            <span class="text-neutral-400">Backend: {{ backendStatus }}</span>
          </div>
          <div class="flex gap-4">
            <a href="#" class="text-neutral-400 hover:text-white transition-colors"><Github class="w-5 h-5" /></a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
/* Custom animations if needed, but Tailwind v4 handles most */
@layer base {
  html {
    scroll-behavior: smooth;
  }
}
</style>
