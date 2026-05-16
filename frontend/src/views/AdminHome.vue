<script setup lang="ts">
import { ref, onMounted } from "vue";
import AdminLayout from "../components/AdminLayout.vue";
import { fetchProjects } from "../services/projectService";
import { fetchTechStacks } from "../services/techStackService";
import { fetchUsers } from "../services/userService";

const projectsCount = ref(0);
const accountsCount = ref(0);
const techStackCount = ref(0);
const isLoading = ref(true);

onMounted(async () => {
  try {
    const [projects, techStacks, users] = await Promise.all([
      fetchProjects(),
      fetchTechStacks(),
      fetchUsers(),
    ]);
    projectsCount.value = projects.length;
    techStackCount.value = techStacks.length;
    accountsCount.value = users.length;
  } catch (error) {
    console.error("Failed to fetch dashboard stats:", error);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <AdminLayout page-title="Dashboard Overview">
    <div class="space-y-10">
      <!-- ── Stats Grid ── -->
      <section class="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div
          class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors h-full"
        >
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]"
              >rocket_launch</span
            >
            <span
              class="font-label-caps text-[10px] text-[var(--primary-bright)]"
              style="font-family: 'JetBrains Mono', monospace"
              >LIVE</span
            >
          </div>
          <p
            class="font-label-caps text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
            style="
              font-family: 'JetBrains Mono', monospace;
              letter-spacing: 0.1em;
              font-weight: 600;
            "
          >
            Created Projects
          </p>
          <h3
            class="font-headline-md text-3xl font-semibold text-[var(--on-surface)]"
          >
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else>{{ projectsCount }}</span>
          </h3>
          <div
            class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-label-caps text-[var(--on-surface-variant)]"
            style="font-family: 'JetBrains Mono', monospace"
          >
            <span class="text-[var(--primary-bright)]">+ Active</span>
          </div>
        </div>

        <div
          class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors h-full"
        >
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]"
              >timer</span
            >
            <span
              class="font-label-caps text-[10px] text-[var(--primary-bright)]"
              style="font-family: 'JetBrains Mono', monospace"
              >System</span
            >
          </div>
          <p
            class="font-label-caps text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
            style="
              font-family: 'JetBrains Mono', monospace;
              letter-spacing: 0.1em;
              font-weight: 600;
            "
          >
            Total Accounts
          </p>
          <h3
            class="font-headline-md text-3xl font-semibold text-[var(--on-surface)]"
          >
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else>{{ accountsCount }}</span>
          </h3>
          <div
            class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-label-caps text-[var(--on-surface-variant)]"
            style="font-family: 'JetBrains Mono', monospace"
          >
            <span class="text-[var(--primary-bright)]">Registered</span>
          </div>
        </div>

        <div
          class="bg-[var(--surface)] border border-[var(--outline)] p-6 hover:border-[var(--primary-bright)] transition-colors h-full"
        >
          <div class="flex justify-between items-start mb-4">
            <span class="material-symbols-outlined text-[var(--primary-bright)]"
              >api</span
            >
            <span
              class="font-label-caps text-[10px] text-[var(--on-surface-variant)]"
              style="font-family: 'JetBrains Mono', monospace"
              >REQUESTS</span
            >
          </div>
          <p
            class="font-label-caps text-[12px] uppercase text-[var(--on-surface-variant)] mb-1"
            style="
              font-family: 'JetBrains Mono', monospace;
              letter-spacing: 0.1em;
              font-weight: 600;
            "
          >
            TechStack Registry
          </p>
          <h3
            class="font-headline-md text-3xl font-semibold text-[var(--on-surface)]"
          >
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else>{{ techStackCount }}</span>
          </h3>
          <div
            class="mt-4 pt-4 border-t border-[var(--outline)] flex items-center gap-2 text-[10px] font-label-caps text-[var(--on-surface-variant)]"
            style="font-family: 'JetBrains Mono', monospace"
          >
            <span class="text-[var(--primary-bright)]">Verified</span>
          </div>
        </div>
      </section>


    </div>
  </AdminLayout>
</template>
