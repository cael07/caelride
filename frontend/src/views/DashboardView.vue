<template>
  <div class="app-shell">

    <!-- ===== PERMANENT ICON SIDEBAR ===== -->
    <aside class="sidebar">
      <!-- Hamburger toggle (opens full drawer) -->
      <button class="sb-hamburger" @click="mobileOpen = true" title="Open menu">
        <span></span><span></span><span></span>
      </button>

      <!-- Brand icon -->
      <div class="sidebar-top">
        <div class="brand-icon" title="JoyRide">
          <svg viewBox="0 0 24 24" fill="white" width="20" height="20">
            <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
          </svg>
        </div>

        <!-- User avatar -->
        <div class="sb-avatar" v-if="user?.face_image_base64" :title="user?.full_name">
          <img :src="user.face_image_base64" alt="face" />
        </div>
        <div class="sb-avatar sb-initials" v-else :title="user?.full_name">{{ initials }}</div>
      </div>

      <!-- Nav icons -->
      <nav class="sidebar-nav">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="nav-icon-btn"
          :class="{ active: activePage === item.key }"
          @click="activePage = item.key"
          :title="item.label"
          v-html="item.icon"
        ></button>
      </nav>

      <!-- Logout at bottom -->
      <div class="sidebar-bottom">
        <button class="nav-icon-btn nav-logout" @click="handleLogout" title="Logout">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- ===== MOBILE FLOATING DRAWER ===== -->
    <Transition name="overlay-fade">
      <div v-if="mobileOpen" class="mobile-overlay" @click="mobileOpen = false">
        <aside class="mobile-drawer" @click.stop>
          <!-- Brand + Close -->
          <div class="sidebar-brand">
            <div class="brand-icon">
              <svg viewBox="0 0 24 24" fill="white" width="20" height="20">
                <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
              </svg>
            </div>
            <span class="brand-name">JoyRide</span>
            <button class="close-btn" @click="mobileOpen = false">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          <!-- Profile row -->
          <div class="drawer-profile">
            <div class="sb-avatar" v-if="user?.face_image_base64"><img :src="user.face_image_base64" alt="face" /></div>
            <div class="sb-avatar sb-initials" v-else>{{ initials }}</div>
            <div class="sp-info">
              <span class="sp-name">{{ user?.full_name || 'Passenger' }}</span>
              <span class="sp-role">Passenger</span>
            </div>
          </div>
          <!-- Nav -->
          <nav class="drawer-nav">
            <button
              v-for="item in navItems" :key="item.key"
              class="drawer-nav-item"
              :class="{ active: activePage === item.key }"
              @click="activePage = item.key; mobileOpen = false"
            >
              <span class="nav-icon" v-html="item.icon"></span>
              <span class="nav-label">{{ item.label }}</span>
              <span v-if="activePage === item.key" class="nav-active-dot"></span>
            </button>
          </nav>
          <!-- Logout -->
          <div class="drawer-footer">
            <button class="drawer-nav-item nav-logout" @click="handleLogout">
              <span class="nav-icon"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg></span>
              <span class="nav-label">Logout</span>
            </button>
          </div>
        </aside>
      </div>
    </Transition>

    <!-- ===== CONTENT AREA ===== -->
    <main class="content-area">

      <!-- Mobile top bar (hidden on desktop) -->
      <div class="mobile-topbar">
        <button class="mobile-menu-btn" @click="mobileOpen = true">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
        </button>
        <span class="mobile-page-title">{{ currentPageLabel }}</span>
        <div class="sb-avatar sb-initials topbar-avatar" v-if="!user?.face_image_base64">{{ initials }}</div>
        <div class="sb-avatar topbar-avatar" v-else><img :src="user.face_image_base64" alt="face" /></div>
      </div>

      <Transition name="page-switch" mode="out-in">

        <!-- ====== HOME PAGE ====== -->
        <div v-if="activePage === 'home'" key="home" class="page-content">
          <div class="page-header">
            <h1 class="page-title">Home</h1>
            <p class="page-sub">Welcome back, {{ user?.full_name?.split(' ')[0] || 'Passenger' }}!</p>
          </div>

          <div class="home-grid">
            <!-- Book a Ride card -->
            <div class="ride-card glass">
              <h3 class="ride-title">
                <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
                  <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
                </svg>
                Book a Ride
              </h3>
              <p class="ride-sub">Choose your mode to continue:</p>

              <div class="mode-actions">
                <!-- Motorcycle -->
                <button class="action-tile" @click="handleAction('/passenger', $event)">
                  <div class="tile-wave-container">
                    <svg class="tile-waves" xmlns="http://www.w3.org/2000/svg" viewBox="0 24 150 28" preserveAspectRatio="none">
                      <defs><path id="tw-motor" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" /></defs>
                      <g class="tile-parallax">
                        <use href="#tw-motor" x="48" y="0" fill="rgba(59,130,246,0.10)" />
                        <use href="#tw-motor" x="48" y="3" fill="rgba(59,130,246,0.18)" />
                        <use href="#tw-motor" x="48" y="5" fill="rgba(59,130,246,0.32)" />
                      </g>
                    </svg>
                  </div>
                  <svg viewBox="0 0 512 396.904" class="tile-icon motor-svg">
                    <defs>
                      <linearGradient id="motor-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#93c5fd"/>
                        <stop offset="100%" stop-color="#2563eb"/>
                      </linearGradient>
                    </defs>
                    <path d="M374.602 185.165c2.929.208 5.81.437 8.631.684-3.21 5.724-6.795 10.786-10.662 15.239a236.047 236.047 0 002.031-15.923zm-81.809-81.974c-1.421-15.363 8.046-29.185 21.556-30.564 39.44-4.029 50.501 55.635 51.478 85.028.476 14.337-.539 29.146-3.177 44.385-6.077 20.951-22.561 26.459-49.788 25.096h-47.386l13.549 55.536c4.88 14.083 4.451 32.732-15.602 33.646-14.026.639-18.289-10.996-21.145-22.65l-17.25-71.531c-2.345-9.606-5.743-19.917.84-28.843 5.915-8.018 13.834-8.421 22.678-8.468l55.313.21-3.642-37.756c5.261-4.17 15.675-12.065 23.69-19.946 4.937-4.855 9.003-9.565 10.476-13.08 5.677-13.544-7.723-28.152-20.379-25.663-2.903.571-6.737 3.078-10.481 5.951-3.864 2.965-8.168 6.628-10.73 8.649zM274.344 0c20.996 0 38.016 17.02 38.016 38.016s-17.02 38.016-38.016 38.016c-20.995 0-38.016-17.02-38.016-38.016S253.349 0 274.344 0zm32.653 98.084c5.933-5.077 14.859-4.383 19.936 1.55s4.382 14.859-1.55 19.936l-58.659 50.276a14.103 14.103 0 01-10.797 3.303l-.002.02-62.022-7.182-4.12 2.859c-4.603 3.178-10.428 3.251-14.991.673-2.529 1.335-5.573 1.738-9.579 2.753l-4.809 1.217c-6.12 1.67-11.065 1.627-14.552.447l-4.342.899-7.068 15.744c17.093 4.183 32.801-2.463 47.462-17.3 17.485-2.738 34.484-1.82 50.86 3.769-5.482 1.714-10.431 4.837-14.653 10.56-8.721 11.823-5.801 23.415-3.023 34.451.492 1.959.027-.018.601 2.337l17.25 71.531c1.677 6.846 3.841 13.784 8.003 19.4 5.002 6.75 12.113 11.085 22.895 10.594 3.601-.164 6.823-.783 9.695-1.778 7.008-2.428 11.652-6.909 14.483-12.543 2.542-5.06 3.427-10.843 3.161-16.674-.227-5.006-1.311-10.137-2.891-14.838l-10.109-41.437c26.638 13.579 61.895 8.536 87.145-7.318 15.228-9.561 27.768-23.212 37.792-40.686 22.259-.078 44.249 1.173 65.813 4.57l6.4 14.626c-79.949 1.158-127.397 57.189-146.254 144.426H187.845c-8.498-49.454-30.93-83.491-62.871-107.006l-7.058 16.321c21.709 12.189 36.378 35.425 36.378 62.094 0 39.305-31.863 71.168-71.168 71.168-39.304 0-71.168-31.863-71.168-71.168 0-34.81 24.993-63.778 58.012-69.949-18.889 2.053-40.472 8.792-64.285 19.413L0 265.603c21.248-19.267 53.883-31.046 101.739-32.825-16.054-8.455-33.796-15.042-52.835-20.192 22.952-44.716 52.25-77.45 90.037-94.152l5.484 9.141c-12.649 14.416-22.92 32.006-30.621 53.017 3.33 2.382 6.608 4.364 9.839 5.969l8.662-19.171a5.741 5.741 0 014.473-3.273l4.003-.829c.184-.433.401-.871.65-1.312 3.966-6.993 12.094-8.764 19.891-10.372 2.691-.551 5.556-1.425 8.388-1.787a14.078 14.078 0 014.014-4.23l7.793-5.409a14.113 14.113 0 0110.349-2.931l61.162 7.082 53.969-46.245z" fill="url(#motor-grad)"/>
                  </svg>
                  <div class="tile-text">
                    <span class="tile-title">Motorcycle</span>
                    <span class="tile-desc">Fast bike ride</span>
                  </div>
                </button>

                <!-- Documents -->
                <button class="action-tile" @click="handleAction('modal', $event)">
                  <div class="tile-wave-container">
                    <svg class="tile-waves" xmlns="http://www.w3.org/2000/svg" viewBox="0 24 150 28" preserveAspectRatio="none">
                      <defs><path id="tw-doc" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" /></defs>
                      <g class="tile-parallax">
                        <use href="#tw-doc" x="48" y="0" fill="rgba(59,130,246,0.10)" />
                        <use href="#tw-doc" x="48" y="3" fill="rgba(59,130,246,0.18)" />
                        <use href="#tw-doc" x="48" y="5" fill="rgba(59,130,246,0.32)" />
                      </g>
                    </svg>
                  </div>
                  <svg viewBox="0 0 24 24" class="tile-icon doc-svg">
                    <defs>
                      <linearGradient id="doc-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#93c5fd"/>
                        <stop offset="100%" stop-color="#2563eb"/>
                      </linearGradient>
                    </defs>
                    <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z" fill="url(#doc-grad)"/>
                  </svg>
                  <div class="tile-text">
                    <span class="tile-title">Documents</span>
                    <span class="tile-desc">Credentials</span>
                  </div>
                </button>

                <!-- Car (disabled) -->
                <button class="action-tile disabled" disabled>
                  <span class="disabled-badge">Soon</span>
                  <svg viewBox="0 0 512 512" class="tile-icon car-svg">
                    <defs>
                      <linearGradient id="car-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#94a3b8"/>
                        <stop offset="100%" stop-color="#475569"/>
                      </linearGradient>
                    </defs>
                    <path d="M499.99 176h-59.87l-16.64-41.6C406.38 91.63 365.57 64 319.5 64h-127c-46.06 0-86.88 27.63-103.99 70.4L71.87 176H12.01C4.2 176-1.53 183.34.37 190.91l6 24C7.7 220.25 12.5 224 18.01 224h20.07C24.65 235.73 16 252.78 16 272v48c0 16.12 6.16 30.67 16 41.93V416c0 17.67 14.33 32 32 32h32c17.67 0 32-14.33 32-32v-32h256v32c0 17.67 14.33 32 32 32h32c17.67 0 32-14.33 32-32v-52.07c9.84-11.26 16-25.81 16-41.93v-48c0-19.22-8.65-36.27-22.07-48h20.07c.51 0 10.31-3.75 11.64-8.91l6-24c1.9-7.57-3.83-14.91-11.64-14.91z" fill="url(#car-grad)"/>
                  </svg>
                  <div class="tile-text">
                    <span class="tile-title">Car</span>
                    <span class="tile-desc">Sedan ride</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== PROFILE PAGE ====== -->
        <div v-else-if="activePage === 'profile'" key="profile" class="page-content">
          <div class="page-header">
            <h1 class="page-title">Profile</h1>
            <p class="page-sub">Your account information</p>
          </div>
          <div class="profile-card glass">
            <div class="profile-avatar-wrap">
              <div class="profile-avatar" v-if="user?.face_image_base64">
                <img :src="user.face_image_base64" alt="face" />
              </div>
              <div class="profile-avatar profile-initials" v-else>{{ initials }}</div>
            </div>
            <div class="profile-fields">
              <div class="pf-row"><span class="pf-lbl">Full Name</span><span class="pf-val">{{ user?.full_name || '—' }}</span></div>
              <div class="pf-row"><span class="pf-lbl">Username</span><span class="pf-val">@{{ user?.username || '—' }}</span></div>
              <div class="pf-row"><span class="pf-lbl">Email</span><span class="pf-val">{{ user?.email || '—' }}</span></div>
              <div class="pf-row">
                <span class="pf-lbl">Role</span>
                <span class="pf-val"><span class="role-badge">{{ (user?.role || 'PASSENGER').toUpperCase() }}</span></span>
              </div>
              <div class="pf-row"><span class="pf-lbl">Face Biometrics</span><span class="pf-val text-success">✓ Connected</span></div>
              <div class="pf-row"><span class="pf-lbl">Account Status</span><span class="pf-val text-success">✓ Verified</span></div>
            </div>
            <div class="fingerprint-section">
              <button v-if="biometricAvailable && !fingerprintEnabled" class="btn-fingerprint" @click="setupFingerprint">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.44-5.57 1.31-.28.14-.62.03-.76-.25-.14-.28-.03-.62.25-.76 1.88-.96 3.94-1.45 6.08-1.45 2.15 0 4.02.48 5.7 1.4.28.15.38.49.23.77-.09.16-.24.25-.43.25z"/></svg>
                Enable Fingerprint Login
              </button>
              <div v-else-if="fingerprintEnabled" class="fingerprint-linked">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                Fingerprint Login Linked
              </div>
            </div>
          </div>
        </div>

      </Transition>
    </main>

    <!-- Documents Modal -->
    <Transition name="modal-fade">
      <div v-if="showDocModal" class="modal-overlay" @click.self="showDocModal = false">
        <div class="modal-content glass">
          <div class="modal-wave-container">
            <svg class="modal-waves" xmlns="http://www.w3.org/2000/svg" viewBox="0 24 150 28" preserveAspectRatio="none">
              <defs><path id="gwave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" /></defs>
              <g class="mparallax">
                <use href="#gwave" x="48" y="0" fill="rgba(59,130,246,0.15)" />
                <use href="#gwave" x="48" y="3" fill="rgba(59,130,246,0.28)" />
                <use href="#gwave" x="48" y="5" fill="rgba(59,130,246,0.42)" />
                <use href="#gwave" x="48" y="7" fill="rgba(59,130,246,0.6)" />
              </g>
            </svg>
            <div class="modal-title-wrap"><h3 class="modal-title">📄 Verified Credentials</h3></div>
          </div>
          <p class="modal-desc">Your identity documents verified via OCR face-scanning:</p>
          <div class="doc-list">
            <div class="doc-item"><span class="d-lbl">Full Name</span><span class="d-val">{{ user?.full_name }}</span></div>
            <div class="doc-item"><span class="d-lbl">Auth Role</span><span class="d-val role-badge" style="text-transform:uppercase;">{{ user?.role }}</span></div>
            <div class="doc-item"><span class="d-lbl">Face Biometrics</span><span class="d-val text-success">CONNECTED ✓</span></div>
            <div class="doc-item"><span class="d-lbl">Account Status</span><span class="d-val text-success">VERIFIED ✓</span></div>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary" @click="showDocModal = false">Close</button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth   = useAuthStore()
const router = useRouter()
const user   = computed(() => auth.user)

const activePage         = ref('home')
const mobileOpen         = ref(false)
const showDocModal       = ref(false)
const biometricAvailable = ref(false)
const fingerprintEnabled = ref(false)

const currentPageLabel = computed(() => {
  const found = navItems.find(i => i.key === activePage.value)
  return found ? found.label : 'Dashboard'
})

const navItems = [
  {
    key: 'home',
    label: 'Home',
    icon: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>`
  },
  {
    key: 'profile',
    label: 'Profile',
    icon: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/></svg>`
  },
  {
    key: 'documents',
    label: 'Documents',
    icon: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>`
  },
]

const initials = computed(() => {
  if (!user.value?.full_name) return '?'
  return user.value.full_name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

onMounted(async () => {
  try {
    const isSecure = window.location.protocol === 'https:' || window.location.hostname === 'localhost'
    biometricAvailable.value = !!(window.PublicKeyCredential && isSecure)
    if (user.value?.username) {
      fingerprintEnabled.value = localStorage.getItem(`fp_${user.value.username}`) === 'true'
    }
  } catch (e) {}
})

async function setupFingerprint() {
  try {
    const challenge = new Uint8Array(32)
    window.crypto.getRandomValues(challenge)
    const userId = new Uint8Array(16)
    window.crypto.getRandomValues(userId)
    const credential = await navigator.credentials.create({
      publicKey: {
        challenge, rp: { name: 'JoyRide' },
        user: { id: userId, name: user.value.username, displayName: user.value.full_name },
        pubKeyCredParams: [{ alg: -7, type: 'public-key' }],
        timeout: 60000, attestation: 'direct', userVerification: 'required',
        authenticatorSelection: { authenticatorAttachment: 'platform', userVerification: 'required' }
      }
    })
    if (credential) {
      fingerprintEnabled.value = true
      localStorage.setItem(`fp_${user.value.username}`, 'true')
      alert('Fingerprint login has been enabled!')
    }
  } catch (e) { alert('Could not set up fingerprint. Make sure your device supports it.') }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

function handleAction(type, event) {
  if (type === 'modal') {
    // Quick ripple then open
    showDocModal.value = true
    return
  }
  const button = event.currentTarget
  const createRipple = (delay = 0) => {
    const circle = document.createElement('span')
    const sid = button.getAttributeNames().find(n => n.startsWith('data-v-'))
    if (sid) circle.setAttribute(sid, '')
    const d = Math.max(button.clientWidth, button.clientHeight)
    const rect = button.getBoundingClientRect()
    circle.style.width = circle.style.height = `${d}px`
    circle.style.left = `${event.clientX - rect.left - d / 2}px`
    circle.style.top  = `${event.clientY - rect.top - d / 2}px`
    circle.classList.add('ripple-wave')
    if (delay) circle.style.animationDelay = `${delay}ms`
    button.appendChild(circle)
    setTimeout(() => circle.remove(), 1000 + delay)
  }
  Array.from(button.getElementsByClassName('ripple-wave')).forEach(r => r.remove())
  createRipple(0); setTimeout(() => createRipple(120), 120)
  setTimeout(() => router.push(type), 500)
}
</script>

<style scoped>
/* ── Shell ─────────────────────────────────────────── */
.app-shell {
  display: flex;
  height: 100dvh;
  width: 100%;
  overflow: hidden;
  background: var(--bg);
}

/* ── Narrow Icon Sidebar ───────────────────────────── */
.sidebar {
  width: 60px;
  min-width: 60px;
  height: 100%;
  background: rgba(12, 9, 30, 0.98);
  border-right: 1px solid rgba(139, 92, 246, 0.12);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 0;
  gap: 0;
  flex-shrink: 0;
  z-index: 10;
}

/* Hamburger button at top of icon sidebar */
.sb-hamburger {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  width: 42px; height: 42px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  outline: none;
  flex-shrink: 0;
  border-radius: 10px;
  transition: background 0.18s ease;
}
.sb-hamburger span {
  display: block;
  width: 20px; height: 2px;
  background: var(--text-3);
  border-radius: 2px;
  transition: background 0.18s ease;
}
.sb-hamburger:hover { background: rgba(139,92,246,0.1); }
.sb-hamburger:hover span { background: #fff; }

.sidebar-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.65rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  width: 100%;
  padding-left: 0; padding-right: 0;
}

.brand-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(139,92,246,0.45);
  cursor: default;
}

.sb-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(139,92,246,0.35);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.sb-avatar img { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
.sb-initials {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  font-size: 0.72rem; font-weight: 700; color: #fff;
}

/* Nav icon buttons */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  padding: 0.65rem 0;
  width: 100%;
}

.nav-icon-btn {
  width: 42px; height: 42px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  background: none;
  border: none;
  color: var(--text-3);
  cursor: pointer;
  transition: background 0.18s ease, color 0.18s ease, transform 0.15s ease;
  outline: none;
  position: relative;
}
.nav-icon-btn:hover {
  background: rgba(139,92,246,0.1);
  color: var(--text-1);
  transform: scale(1.08);
}
.nav-icon-btn.active {
  background: rgba(139,92,246,0.18);
  color: var(--primary-light);
  box-shadow: 0 0 0 1.5px rgba(139,92,246,0.3);
}
/* Active left accent bar */
.nav-icon-btn.active::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 50%; transform: translateY(-50%);
  width: 3px; height: 20px;
  border-radius: 0 3px 3px 0;
  background: var(--primary-light);
}

.sidebar-bottom {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding-top: 0.65rem;
  width: 100%;
  display: flex; justify-content: center;
}

.nav-logout { color: #fca5a5 !important; }
.nav-logout:hover { background: rgba(239,68,68,0.12) !important; color: #f87171 !important; }
.nav-logout.active { background: none !important; box-shadow: none !important; }
.nav-logout.active::before { display: none; }

/* ── Content Area ──────────────────────────────────── */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  min-width: 0;
}

.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.75rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  height: 100%;
  box-sizing: border-box;
}

.page-header { flex-shrink: 0; }
.page-title { font-size: 1.5rem; font-weight: 700; color: var(--text-1); margin: 0; }
.page-sub { font-size: 0.85rem; color: var(--text-2); margin: 0.2rem 0 0; }

/* Page transition */
.page-switch-enter-active, .page-switch-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.page-switch-enter-from { opacity: 0; transform: translateX(12px); }
.page-switch-leave-to  { opacity: 0; transform: translateX(-12px); }

/* ── Home grid ─────────────────────────────────────── */
.home-grid { display: flex; flex-direction: column; gap: 1rem; flex: 1; min-height: 0; }

/* ── Ride Card ─────────────────────────────────────── */
.ride-card { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.ride-title {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.95rem; font-weight: 600; color: var(--text-1); margin: 0;
}
.ride-sub { font-size: 0.85rem; color: var(--text-2); margin: 0; }

.mode-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.85rem;
}

.action-tile {
  position: relative; overflow: hidden;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 1.25rem 0.75rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-align: center; gap: 0.5rem; outline: none;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  color: var(--text-2);
}
.action-tile:hover {
  background: rgba(255,255,255,0.06);
  border-color: rgba(59,130,246,0.45);
  color: var(--text-1);
  box-shadow: 0 8px 24px rgba(37,99,235,0.2);
  transform: translateY(-4px);
}
.action-tile:hover .motor-svg { transform: scale(1.15) rotate(-6deg); filter: drop-shadow(0 0 10px rgba(59,130,246,0.7)); }
.action-tile:hover .doc-svg   { transform: scale(1.15) rotate(6deg);  filter: drop-shadow(0 0 10px rgba(59,130,246,0.7)); }
.action-tile::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at center, rgba(255,255,255,0.08) 0%, transparent 70%);
  opacity: 0; transition: opacity 0.4s ease; pointer-events: none; z-index: 1;
}
.action-tile:hover::before { opacity: 1; animation: hoverPulse 1.8s infinite alternate ease-in-out; }
@keyframes hoverPulse {
  0%   { transform: scale(0.95); opacity: 0.4; }
  100% { transform: scale(1.05); opacity: 0.9; }
}

.tile-wave-container {
  position: absolute; bottom: 0; left: 0;
  width: 100%; height: 25px;
  overflow: hidden; pointer-events: none; z-index: 1;
  border-bottom-left-radius: var(--radius-sm); border-bottom-right-radius: var(--radius-sm);
}
.tile-waves { width: 100%; height: 100%; position: absolute; left: 0; bottom: -1px; }
.tile-parallax > use { animation: moveTileWave 12s cubic-bezier(.55,.5,.45,.5) infinite; }
.tile-parallax > use:nth-child(1) { animation-delay: -2s; animation-duration: 5s; }
.tile-parallax > use:nth-child(2) { animation-delay: -3s; animation-duration: 7s; }
.tile-parallax > use:nth-child(3) { animation-delay: -4s; animation-duration: 9s; }
@keyframes moveTileWave { 0% { transform: translate3d(-90px,0,0); } 100% { transform: translate3d(85px,0,0); } }

.tile-icon { width: 32px; height: 32px; transition: all 0.3s ease; position: relative; z-index: 2; }
.tile-text { display: flex; flex-direction: column; gap: 0.15rem; position: relative; z-index: 2; }
.tile-title { font-size: 0.85rem; font-weight: 700; letter-spacing: 0.3px; }
.tile-desc  { font-size: 0.68rem; color: var(--text-3); }

.action-tile.disabled {
  opacity: 0.4; cursor: not-allowed !important;
  background: rgba(255,255,255,0.01) !important;
  border-color: rgba(255,255,255,0.04) !important;
  pointer-events: none;
}
.disabled-badge {
  position: absolute; top: 6px; right: 6px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
  color: var(--text-3); font-size: 0.5rem; font-weight: 700;
  padding: 0.1rem 0.28rem; border-radius: 4px;
  letter-spacing: 0.3px; text-transform: uppercase;
}

/* ── Profile ───────────────────────────────────────── */
.profile-card { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.25rem; }
.profile-avatar-wrap { display: flex; justify-content: center; }
.profile-avatar {
  width: 80px; height: 80px; border-radius: 50%; overflow: hidden;
  border: 3px solid rgba(139,92,246,0.5);
  box-shadow: 0 0 24px rgba(139,92,246,0.3);
  display: flex; align-items: center; justify-content: center;
}
.profile-avatar img { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
.profile-initials { background: linear-gradient(135deg, var(--primary), #7c3aed); font-size: 1.6rem; font-weight: 700; color: #fff; }
.profile-fields { display: flex; flex-direction: column; }
.pf-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.65rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem;
}
.pf-lbl { color: var(--text-3); font-weight: 500; }
.pf-val { color: var(--text-1); font-weight: 600; text-align: right; }
.text-success { color: var(--success); }
.role-badge { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); color: #fbbf24; padding: 0.15rem 0.5rem; border-radius: 99px; font-size: 0.72rem; font-weight: 700; }
.fingerprint-section { display: flex; justify-content: center; padding-top: 0.25rem; }
.btn-fingerprint {
  display: flex; align-items: center; gap: 0.5rem;
  background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.4);
  color: var(--primary-light); padding: 0.55rem 1.25rem;
  border-radius: var(--radius-sm); cursor: pointer; font-size: 0.85rem; font-weight: 500;
  transition: all 0.2s ease;
}
.btn-fingerprint:hover { background: rgba(139,92,246,0.2); }
.fingerprint-linked { display: flex; align-items: center; gap: 0.4rem; color: var(--success); font-size: 0.85rem; font-weight: 600; }

/* ── Modal ─────────────────────────────────────────── */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.65); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
  width: 90%; max-width: 400px; padding: 2rem;
  border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: rgba(22,18,30,0.95);
  box-shadow: 0 20px 45px rgba(0,0,0,0.5), 0 0 35px rgba(139,92,246,0.15);
  display: flex; flex-direction: column; gap: 1.25rem; overflow: hidden;
}
.modal-wave-container {
  position: relative; width: calc(100% + 4rem); margin: -2rem -2rem 0 -2rem;
  height: 90px; background: linear-gradient(135deg, rgba(37,99,235,0.4), rgba(96,165,250,0.2));
  border-bottom: 1px solid rgba(59,130,246,0.2); overflow: hidden;
}
.modal-waves { position: absolute; bottom: -2px; width: 100%; height: 40px; }
.modal-title-wrap { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 10; padding-bottom: 12px; }
.modal-title { font-size: 1.2rem; font-weight: 800; margin: 0; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
.mparallax > use { animation: mWave 25s cubic-bezier(.55,.5,.45,.5) infinite; }
.mparallax > use:nth-child(1) { animation-delay: -2s; animation-duration: 7s; }
.mparallax > use:nth-child(2) { animation-delay: -3s; animation-duration: 10s; }
.mparallax > use:nth-child(3) { animation-delay: -4s; animation-duration: 13s; }
.mparallax > use:nth-child(4) { animation-delay: -5s; animation-duration: 20s; }
@keyframes mWave { 0% { transform: translate3d(-90px,0,0); } 100% { transform: translate3d(85px,0,0); } }
.modal-desc { font-size: 0.85rem; color: var(--text-2); margin: 0; }
.doc-list { display: flex; flex-direction: column; gap: 0.75rem; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 6px; padding: 1rem; }
.doc-item { display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; }
.d-lbl { color: var(--text-3); font-weight: 500; }
.d-val { color: var(--text-1); font-weight: 700; }
.modal-actions { display: flex; justify-content: flex-end; }
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-active .modal-content, .modal-fade-leave-active .modal-content { transition: all 0.28s cubic-bezier(0.34,1.56,0.64,1); }
.modal-fade-enter-from .modal-content { transform: scale(0.9) translateY(12px); }
.modal-fade-leave-to .modal-content { transform: scale(0.95); }

/* ── Mobile Top Bar ────────────────────────────────── */
.mobile-topbar {
  display: none;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  background: rgba(12, 9, 30, 0.97);
  border-bottom: 1px solid rgba(139, 92, 246, 0.12);
  flex-shrink: 0;
}
.mobile-menu-btn {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-1); cursor: pointer; flex-shrink: 0; outline: none;
}
.mobile-menu-btn:hover { background: rgba(255,255,255,0.12); }
.mobile-page-title { flex: 1; font-size: 0.95rem; font-weight: 600; color: var(--text-1); }
.topbar-avatar { width: 30px !important; height: 30px !important; font-size: 0.68rem !important; flex-shrink: 0; }

/* ── Mobile Floating Drawer ─────────────────────────── */
.mobile-overlay {
  position: fixed; inset: 0; z-index: 900;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
  display: flex;
}
.mobile-drawer {
  width: 260px; height: 100%;
  background: rgba(12, 9, 30, 0.98);
  border-right: 1px solid rgba(139,92,246,0.2);
  display: flex; flex-direction: column; overflow: hidden;
  box-shadow: 4px 0 40px rgba(0,0,0,0.5);
}
.sidebar-brand {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 1.1rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06); flex-shrink: 0;
}
.brand-name {
  font-family: 'Outfit', sans-serif; font-size: 1.05rem;
  font-weight: 700; color: #fff; flex: 1; white-space: nowrap;
}
.close-btn {
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px; width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-3); cursor: pointer; outline: none; flex-shrink: 0;
}
.close-btn:hover { background: rgba(255,255,255,0.12); color: #fff; }
.drawer-profile {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06); flex-shrink: 0;
}
.sp-info { display: flex; flex-direction: column; min-width: 0; overflow: hidden; }
.sp-name { font-size: 0.85rem; font-weight: 600; color: var(--text-1); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sp-role { font-size: 0.7rem; color: var(--primary-light); text-transform: uppercase; letter-spacing: 0.5px; }
.drawer-nav { flex: 1; display: flex; flex-direction: column; padding: 0.5rem 0; overflow-y: auto; }
.drawer-nav-item {
  display: flex; align-items: center; gap: 0.85rem;
  padding: 0.75rem 1rem;
  background: none; border: none; color: var(--text-2);
  cursor: pointer; text-align: left; width: 100%;
  white-space: nowrap; overflow: hidden; outline: none;
  transition: background 0.18s ease, color 0.18s ease;
}
.drawer-nav-item:hover { background: rgba(139,92,246,0.08); color: var(--text-1); }
.drawer-nav-item.active { background: rgba(139,92,246,0.15); color: #fff; border-right: 3px solid var(--primary); }
.nav-icon { display: flex; align-items: center; justify-content: center; flex-shrink: 0; width: 22px; }
.nav-label { font-size: 0.88rem; font-weight: 500; flex: 1; }
.nav-active-dot { margin-left: auto; width: 6px; height: 6px; border-radius: 50%; background: var(--primary-light); flex-shrink: 0; }
.drawer-footer { border-top: 1px solid rgba(255,255,255,0.06); flex-shrink: 0; }
.overlay-fade-enter-active, .overlay-fade-leave-active { transition: opacity 0.25s ease; }
.overlay-fade-enter-from, .overlay-fade-leave-to { opacity: 0; }

/* ── Responsive ────────────────────────────────────── */
@media (max-width: 768px) {
  /* Hide desktop icon sidebar, show mobile topbar */
  .sidebar { display: none; }
  .mobile-topbar { display: flex; }
  .page-content { padding: 1.25rem; }
  .mode-actions { grid-template-columns: 1fr 1fr; gap: 0.65rem; }
}
@media (max-width: 420px) {
  .mode-actions { grid-template-columns: 1fr; }
}
</style>

<style>
.action-tile .ripple-wave {
  position: absolute; border-radius: 50%;
  transform: scale(0); opacity: 1; pointer-events: none;
  z-index: 2000; box-sizing: border-box;
  animation: rippleAnim 0.9s cubic-bezier(0.1,0.8,0.2,1) forwards;
  background: radial-gradient(circle at center, rgba(96,165,250,0.55) 0%, rgba(37,99,235,0.2) 50%, transparent 70%);
  border: 1.5px solid rgba(96,165,250,0.5);
  box-shadow: 0 0 25px rgba(37,99,235,0.35);
}
@keyframes rippleAnim {
  0%   { transform: scale(0); opacity: 0.95; }
  50%  { opacity: 0.65; }
  100% { transform: scale(3.5); opacity: 0; }
}
</style>
