<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login } from '../services/authService'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = 'ERR: All fields required.'
    return
  }
  loading.value = true
  try {
    await login(username.value, password.value)
    const redirect = (route.query.redirect as string) || '/admin'
    router.push(redirect)
  } catch (err: unknown) {
    error.value = err instanceof Error ? `ERR: ${err.message}` : 'ERR: Authentication failed.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#0b1326] flex items-center justify-center px-4 relative overflow-hidden"
    style="font-family:'Geist',sans-serif;">
    <!-- Blueprint grid -->
    <div class="absolute inset-0 pointer-events-none"
      style="background-image:linear-gradient(to right,#3c4a42 1px,transparent 1px),linear-gradient(to bottom,#3c4a42 1px,transparent 1px);background-size:40px 40px;opacity:0.07;">
    </div>

    <!-- Corner decorations -->
    <div class="absolute top-8 left-8 text-[#3c4a42] text-[10px] font-semibold tracking-widest"
      style="font-family:'JetBrains Mono',monospace;">// AUTH_GATEWAY</div>
    <div class="absolute top-8 right-8 text-[#3c4a42] text-[10px] font-semibold tracking-widest"
      style="font-family:'JetBrains Mono',monospace;">v2.4.1</div>
    <div class="absolute bottom-8 left-8 text-[#3c4a42] text-[10px] font-semibold tracking-widest"
      style="font-family:'JetBrains Mono',monospace;">SESSION: UNAUTH</div>
    <div class="absolute bottom-8 right-8 text-[#3c4a42] text-[10px] font-semibold tracking-widest"
      style="font-family:'JetBrains Mono',monospace;">SYS: ONLINE</div>

    <!-- Login Panel -->
    <div class="relative w-full max-w-sm bg-[#171f33] border border-[#3c4a42]">

      <!-- Header bar -->
      <div class="p-6 border-b border-[#3c4a42] flex items-center gap-3">
        <div class="w-8 h-8 bg-[#10b981] flex items-center justify-center">
          <span class="text-[#003824] font-bold text-xs" style="font-family:'JetBrains Mono',monospace;">&gt;_</span>
        </div>
        <div>
          <p class="text-base font-bold tracking-tighter text-[#dae2fd]">&lt;KEN_BE_CODED&gt;</p>
          <p class="text-[10px] tracking-widest uppercase text-[#86948a]"
            style="font-family:'JetBrains Mono',monospace;">Admin Portal</p>
        </div>
      </div>

      <!-- Form body -->
      <div class="p-8 space-y-6">
        <div>
          <h1 class="text-[11px] font-semibold tracking-widest uppercase text-[#4edea3] mb-1"
            style="font-family:'JetBrains Mono',monospace;">// AUTHENTICATE</h1>
          <p class="text-[13px] text-[#86948a]">Enter your credentials to access the admin system.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">

          <!-- Username -->
          <div class="space-y-1.5">
            <label for="username" class="block text-[10px] font-semibold tracking-widest uppercase text-[#86948a]"
              style="font-family:'JetBrains Mono',monospace;">USERNAME</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[#4edea3] text-[13px]"
                style="font-family:'JetBrains Mono',monospace;">$</span>
              <input id="username" v-model="username" type="text" autocomplete="username" placeholder="admin_root"
                class="w-full bg-[#0b1326] border border-[#3c4a42] text-[#dae2fd] pl-7 pr-4 py-3 text-[13px] focus:outline-none focus:border-[#4edea3] transition-colors placeholder-[#3c4a42] caret-[#4edea3]"
                style="font-family:'JetBrains Mono',monospace;" />
            </div>
          </div>

          <!-- Password -->
          <div class="space-y-1.5">
            <label for="password" class="block text-[10px] font-semibold tracking-widest uppercase text-[#86948a]"
              style="font-family:'JetBrains Mono',monospace;">PASSWORD</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[#4edea3] text-[13px]"
                style="font-family:'JetBrains Mono',monospace;">#</span>
              <input id="password" v-model="password" type="password" autocomplete="current-password"
                placeholder="••••••••••••"
                class="w-full bg-[#0b1326] border border-[#3c4a42] text-[#dae2fd] pl-7 pr-4 py-3 text-[13px] focus:outline-none focus:border-[#4edea3] transition-colors placeholder-[#3c4a42] caret-[#4edea3]"
                style="font-family:'JetBrains Mono',monospace;" />
            </div>
          </div>

          <!-- Error -->
          <p v-if="error" class="text-[11px] text-[#ffb4ab] font-semibold tracking-widest uppercase"
            style="font-family:'JetBrains Mono',monospace;">{{ error }}</p>

          <!-- Submit -->
          <button type="submit" :disabled="loading"
            class="w-full bg-[#10b981] text-[#003824] font-bold text-[11px] tracking-widest uppercase py-3.5 hover:bg-[#4edea3] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            style="font-family:'JetBrains Mono',monospace;">
            <span v-if="loading">[ AUTHENTICATING... ]</span>
            <span v-else>[ AUTHENTICATE ]</span>
          </button>
        </form>

        <!-- Code snippet decoration -->
        <div class="border-t border-[#3c4a42] pt-5 space-y-1 text-[11px] text-[#3c4a42]"
          style="font-family:'JetBrains Mono',monospace;">
          <div><span class="text-[#86948a]">// </span>Unauthorized access is prohibited.</div>
          <div><span class="text-[#86948a]">// </span>All sessions are logged and audited.</div>
        </div>
      </div>
    </div>
  </div>
</template>
