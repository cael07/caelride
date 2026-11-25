<template>
  <div class="passenger-layout">
    <!-- Fullscreen Map Background -->
    <div id="passenger-map" class="map-container"></div>

    <!-- Top Overlay Elements -->
    <div class="top-overlay">
      <!-- Routing Card -->
      <div class="route-card glass">
        <div class="route-header">
          <button class="back-btn-inline" @click="$router.push('/dashboard')">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
          </button>
          <div v-if="auth.user?.face_image_base64" class="header-avatar">
            <img :src="auth.user.face_image_base64" alt="Me" class="header-face-img" />
          </div>
          <h3>Choose route</h3>
        </div>
        
        <div class="route-inputs">
          <div class="input-row relative" :class="{'active-row': activeSearchType === 'pickup'}">
            <div class="dot pickup-dot"></div>
            <div class="input-content w-100">
              <span class="label">Pickup <span class="badge" v-if="isCurrentLocation">(Current)</span></span>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <input type="text" class="location-input" v-model="pickupText" @input="onInput('pickup')" @focus="activeSearchType = 'pickup'" placeholder="Enter Pickup Location" :disabled="rideStore.currentBooking" />
                <button v-if="!rideStore.currentBooking" class="gps-btn-inline" @click="centerOnUser" title="Current Location">
                   <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
                </button>
              </div>
              <ul class="suggestions-list" v-if="activeSearchType === 'pickup' && suggestions.length > 0">
                <li v-for="s in suggestions" :key="s.place_id" @click="selectSuggestion(s, 'pickup')">
                  {{ s.display_name }}
                </li>
              </ul>
            </div>
          </div>
          <div class="input-divider"></div>
          <div class="input-row relative" :class="{'active-row': activeSearchType === 'dropoff'}">
            <div class="dot dropoff-dot"></div>
            <div class="input-content w-100">
              <span class="label">Drop-off</span>
              <input type="text" class="location-input" v-model="dropoffText" @input="onInput('dropoff')" @focus="activeSearchType = 'dropoff'" placeholder="Tap map or search location" :disabled="rideStore.currentBooking" />
              <ul class="suggestions-list" v-if="activeSearchType === 'dropoff' && suggestions.length > 0">
                <li v-for="s in suggestions" :key="s.place_id" @click="selectSuggestion(s, 'dropoff')">
                  {{ s.display_name }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Sheet -->
    <div :class="['bottom-sheet', 'glass', { expanded: isSheetExpanded }]">
      <div class="sheet-header" @click="isSheetExpanded = !isSheetExpanded">
        <div class="drag-handle">
          <svg v-if="!isSheetExpanded" viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/></svg>
          <svg v-else viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6z"/></svg>
        </div>
        <h3 v-if="!rideStore.currentBooking" class="sheet-title">Choose your Ride</h3>
        <h3 v-else class="sheet-title">Status: <span :class="['status-badge', rideStore.currentBooking.status]">{{ rideStore.currentBooking.status }}</span></h3>
      </div>

      <div class="sheet-content-wrapper">
        <div v-if="!rideStore.currentBooking" class="h-100 flex-col">
          <div v-show="isSheetExpanded">
            <div class="ride-options">
              <div class="ride-option active">
                <div class="ride-icon">🛵</div>
                <div class="ride-details">
                  <h4>MC Taxi</h4>
                  <p>Beat the traffic</p>
                </div>
                <div class="ride-price">₱ {{ ridePrice }}</div>
              </div>

              <!-- Disabled Car Taxi Card -->
              <div class="ride-option disabled">
                <div class="ride-icon">🚗</div>
                <div class="ride-details">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <h4 style="margin: 0;">Car Taxi</h4>
                    <span style="font-size: 0.65rem; background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); padding: 1px 6px; border-radius: 10px; font-weight: 700; text-transform: uppercase;">Disabled</span>
                  </div>
                  <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #64748b;">4-Seater Premium Car (Unavailable)</p>
                </div>
                <div class="ride-price" style="opacity: 0.6; font-size: 0.88rem; color: #94a3b8;">Unavailable</div>
              </div>
            </div>

            <button 
              class="btn-primary btn-large book-btn" 
              @click="requestRide" 
              :disabled="!dropoff"
            >
              Book MC Taxi
            </button>
          </div>
        </div>

        <div v-else class="status-panel">
          <div class="status-content">
            <div v-if="rideStore.currentBooking.status === 'pending'" class="waiting">
              <div class="spinner"></div>
              <p>Finding you a driver...</p>
            </div>
            <div v-if="rideStore.currentBooking.status === 'accepted'" class="accepted">
              <div class="driver-info">
                <div v-if="rideStore.currentBooking.driver_image" class="driver-avatar">
                  <img :src="rideStore.currentBooking.driver_image" class="driver-face-img" />
                </div>
                <div v-else class="driver-avatar">👨‍✈️</div>
                <div>
                  <h4>{{ rideStore.currentBooking.driver_name || 'Driver' }} is on the way!</h4>
                  <p>Arriving shortly</p>
                </div>
              </div>
            </div>
            <div v-if="rideStore.currentBooking.status === 'arrived'" class="accepted arrived">
              <div class="driver-info highlight">
                <div v-if="rideStore.currentBooking.driver_image" class="driver-avatar blink-fast">
                   <img :src="rideStore.currentBooking.driver_image" class="driver-face-img" />
                </div>
                <div v-else class="driver-avatar blink-fast">🛵</div>
                <div>
                  <h4>{{ rideStore.currentBooking.driver_name || 'Driver' }} has arrived!</h4>
                  <p>Meet your driver at the pickup point</p>
                </div>
              </div>
            </div>
            <div v-if="rideStore.currentBooking.status === 'started'" class="accepted started">
              <div class="driver-info highlight">
                <div class="driver-avatar">🏁</div>
                <div>
                  <h4>On your way!</h4>
                  <p>Heading to destination</p>
                </div>
              </div>
            </div>

            <!-- From & To Route Card -->
            <div v-if="['accepted','arrived','started'].includes(rideStore.currentBooking.status)" class="route-details-card inline-route mb-3">
              <div class="route-point-inline">
                <span class="route-icon">👤</span>
                <div class="route-inline-text">
                  <span class="route-inline-label">From:</span>
                  <span class="route-inline-val">{{ rideStore.currentBooking.pickup_address || addressNames[rideStore.currentBooking.id]?.pickup || (rideStore.currentBooking.pickup_lat + ', ' + rideStore.currentBooking.pickup_lng) }}</span>
                </div>
              </div>

              <div class="route-point-inline">
                <span class="route-icon">📍</span>
                <div class="route-inline-text">
                  <span class="route-inline-label">To:</span>
                  <span class="route-inline-val">{{ rideStore.currentBooking.dropoff_address || addressNames[rideStore.currentBooking.id]?.dropoff || (rideStore.currentBooking.dropoff_lat + ', ' + rideStore.currentBooking.dropoff_lng) }}</span>
                </div>
              </div>
            </div>

            <!-- ── Chat & Call Action Buttons ── -->
            <div class="comm-actions">
              <button class="comm-btn chat-btn" @click="rideStore.chatOpen = !rideStore.chatOpen">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                Chat
                <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
              </button>
              <button
                v-if="!rideStore.callActive"
                class="comm-btn call-btn"
                @click="rideStore.initiateCall(rideStore.currentBooking.driver_id)"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
                Call Driver
              </button>
              <div v-else class="active-call-bar">
                <span class="call-live-dot"></span>
                <span>Call Live</span>
                <button class="mute-btn" @click="rideStore.toggleMute()">
                  {{ rideStore.callMuted ? '🔇' : '🎙️' }}
                </button>
                <button class="end-call-btn" @click="rideStore.endCall(rideStore.currentBooking.driver_id)">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
                  End
                </button>
              </div>
            </div>

            <button class="btn-secondary mt-3 w-100" @click="cancelRide">Cancel Ride</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Hidden audio element for WebRTC remote stream ── -->
  <audio id="remote-audio" autoplay playsinline style="display:none"></audio>

  <!-- ── Incoming Call Modal ── -->
  <Transition name="call-pop">
    <div v-if="rideStore.incomingCall" class="call-modal-overlay">
      <div class="call-modal glass">
        <div class="call-ring-icon">📞</div>
        <h3>Incoming Call</h3>
        <p>{{ rideStore.currentBooking?.driver_name || 'Driver' }} is calling you</p>
        <div class="call-modal-actions">
          <button class="accept-call-btn" @click="rideStore.acceptCall(rideStore.currentBooking?.driver_id)">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
            Accept
          </button>
          <button class="decline-call-btn" @click="rideStore.incomingCall = false; rideStore._pendingOffer = null">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
            Decline
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- ── Chat Drawer ── -->
  <Transition name="slide-up">
    <div v-if="rideStore.chatOpen" class="chat-drawer glass">
      <div class="chat-header">
        <span>💬 Chat with {{ rideStore.currentBooking?.driver_name || 'Driver' }}</span>
        <button class="chat-close-btn" @click="rideStore.chatOpen = false; unreadCount = 0">✕</button>
      </div>
      <div class="chat-messages" ref="chatBox">
        <div v-if="rideStore.chatMessages.length === 0" class="chat-empty">
          <p>No messages yet. Say hello! 👋</p>
        </div>
        <div
          v-for="(msg, i) in rideStore.chatMessages"
          :key="i"
          :class="['chat-bubble', msg.sender === 'me' ? 'bubble-me' : 'bubble-other']"
        >
          <span class="bubble-text">{{ msg.text }}</span>
          <span class="bubble-time">{{ msg.time }}</span>
        </div>
      </div>
      <div class="chat-input-row">
        <input
          v-model="chatInput"
          class="chat-input"
          placeholder="Type a message..."
          @keydown.enter.prevent="sendChat"
          maxlength="500"
        />
        <button class="chat-send-btn" @click="sendChat" :disabled="!chatInput.trim()">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'
import { useRideStore } from '../stores/ride'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const rideStore = useRideStore()
const auth = useAuthStore()
const router = useRouter()
let map = null
let pickupMarker = null
let dropoffMarker = null
let driverMarker = null
let watchId = null
let routeLine = null
let lastRouteFetch = 0

const pickup = ref({ lat: 14.5995, lng: 120.9842 }) // default fallback
const dropoff = ref(null)
const isCurrentLocation = ref(false)
const pickupText = ref('')
const dropoffText = ref('')
const activeSearchType = ref(null)
const suggestions = ref([])
let searchTimeout = null
const deviceLocation = ref(null)
const isSheetExpanded = ref(false)
const addressNames = ref({})

const resolveAddress = async (lat, lng) => {
  if (!lat || !lng) return ''
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
    const data = await res.json()
    return data.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`
  } catch (e) {
    return `${lat.toFixed(5)}, ${lng.toFixed(5)}`
  }
}

watch(() => rideStore.currentBooking, async (b) => {
  if (b) {
    const p = b.pickup_address || await resolveAddress(b.pickup_lat, b.pickup_lng)
    const d = b.dropoff_address || await resolveAddress(b.dropoff_lat, b.dropoff_lng)
    addressNames.value[b.id] = { pickup: p, dropoff: d }
  }
}, { immediate: true, deep: true })

// Chat & Call refs
const chatInput = ref('')
const unreadCount = ref(0)
const chatBox = ref(null)

function sendChat() {
  const text = chatInput.value.trim()
  if (!text || !rideStore.currentBooking?.driver_id) return
  rideStore.sendChatMessage(text, rideStore.currentBooking.driver_id)
  chatInput.value = ''
  // Scroll to bottom
  nextTick(() => {
    if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
  })
}

let lastGeocodeTime = { pickup: 0, dropoff: 0 }

const reverseGeocode = async (lat, lng, type) => {
  const now = Date.now()
  // Only throttle if it's not the first time
  if (lastGeocodeTime[type] > 0 && now - lastGeocodeTime[type] < 5000) return 
  lastGeocodeTime[type] = now

  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`, {
      headers: { 'User-Agent': 'JoyRide-App-PythonLogin-V1' }
    })
    
    if (res.status === 429) return

    const data = await res.json()
    if (data && data.display_name) {
      const parts = data.display_name.split(',')
      const shortAddress = parts.slice(0, 2).join(',')
      if (type === 'pickup') pickupText.value = shortAddress
      else dropoffText.value = shortAddress
    }
  } catch (err) {
    console.warn("Geocoding suppressed:", err)
  }
}

const onInput = (type) => {
  activeSearchType.value = type
  if (type === 'pickup') isCurrentLocation.value = false
  const query = type === 'pickup' ? pickupText.value : dropoffText.value
  
  clearTimeout(searchTimeout)
  if (!query || query.length < 3) {
    suggestions.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=ph`, {
        headers: { 'User-Agent': 'JoyRide-App-PythonLogin-V1' }
      })
      if (res.status === 429) return
      const data = await res.json()
      suggestions.value = data || []
    } catch (err) {
      console.warn("Search suppressed")
    }
  }, 500)
}

const selectSuggestion = (suggestion, type) => {
  const lat = parseFloat(suggestion.lat)
  const lon = parseFloat(suggestion.lon)
  const parts = suggestion.display_name.split(',')
  const shortAddress = parts.slice(0, 2).join(',')

  if (type === 'pickup') {
    pickupText.value = shortAddress
    pickup.value = { lat, lng: lon }
    isCurrentLocation.value = false
    updatePickupMarker()
    map.flyTo([lat, lon], 15)
  } else {
    dropoffText.value = shortAddress
    dropoff.value = { lat, lng: lon }
    if (dropoffMarker) {
      dropoffMarker.setLatLng([lat, lon])
    } else {
      dropoffMarker = L.marker([lat, lon], { icon: destIcon }).addTo(map)
    }
    map.flyTo([lat, lon], 15)
  }
  
  // Close suggestions
  suggestions.value = []
  activeSearchType.value = null
}

// Haversine distance calculation in km
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

const ridePrice = computed(() => {
  if (!pickup.value || !dropoff.value) return 50;
  const dist = calculateDistance(pickup.value.lat, pickup.value.lng, dropoff.value.lat, dropoff.value.lng);
  // Based on Northville to Monumento being ~152 PHP
  // Minimum fare 50 PHP
  return Math.max(50, Math.round(dist * 15.2));
})

// Custom modern icons
const userIcon = L.divIcon({
  className: 'custom-map-marker',
  html: `<div class="marker-pin pickup-pin"></div><div class="marker-pulse pickup-pulse"></div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 15]
})

const destIcon = L.divIcon({
  className: 'custom-map-marker',
  html: `<div class="marker-pin dropoff-pin"></div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 15]
})

const carIcon = L.divIcon({
  className: 'custom-map-marker',
  html: `<div class="marker-pin car-pin">🛵</div>`,
  iconSize: [44, 44],
  iconAnchor: [22, 22]
})

onMounted(async () => {
  rideStore.connectWebSocket()
  await rideStore.fetchActiveBooking()
  console.log("DEBUG: Current Booking ->", rideStore.currentBooking)

  // Initialize map fullscreen
  map = L.map('passenger-map', { zoomControl: false }).setView([pickup.value.lat, pickup.value.lng], 15)
  
  L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    attribution: '&copy; Google Maps'
  }).addTo(map)

  // If there's an active booking, set the map and markers
  if (rideStore.currentBooking) {
    pickup.value = { lat: rideStore.currentBooking.pickup_lat, lng: rideStore.currentBooking.pickup_lng }
    dropoff.value = { lat: rideStore.currentBooking.dropoff_lat, lng: rideStore.currentBooking.dropoff_lng }
    updatePickupMarker()
    
    if (rideStore.currentBooking.status === 'pending') {
      dropoffMarker = L.marker([dropoff.value.lat, dropoff.value.lng], { icon: destIcon }).addTo(map)
      map.fitBounds([
        [pickup.value.lat, pickup.value.lng],
        [dropoff.value.lat, dropoff.value.lng]
      ], { padding: [50, 50] })
    } else {
      // Accepted or Arrived: focus on pickup
      map.setView([pickup.value.lat, pickup.value.lng], 15)
      
      // If we already have driver location, show it
      if (rideStore.driverLocation) {
        if (driverMarker) map.removeLayer(driverMarker)
        driverMarker = L.marker([rideStore.driverLocation.lat, rideStore.driverLocation.lng], { icon: carIcon, zIndexOffset: 1000 }).addTo(map)
        
        const bounds = L.latLngBounds([pickup.value.lat, pickup.value.lng], [rideStore.driverLocation.lat, rideStore.driverLocation.lng])
        map.fitBounds(bounds, { padding: [100, 100] })
      }
    }
  }

  // Start Geolocating
  if ("geolocation" in navigator) {
    watchId = navigator.geolocation.watchPosition(
      (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        
        // Store the raw device location always
        deviceLocation.value = { lat, lng }
        
        // Only update text on first load or if user hasn't typed a custom one
        if (!pickupText.value || isCurrentLocation.value) {
           pickup.value = { lat, lng }
           isCurrentLocation.value = true
           reverseGeocode(lat, lng, 'pickup')
           updatePickupMarker()
           
           // Only auto-center once initially
           if (!map.userHasMoved) {
             map.setView([lat, lng], 15)
           }
        }
      },
      (error) => {
        console.error("Error getting location:", error)
        updatePickupMarker() // Use default
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    )
  } else {
    updatePickupMarker()
  }

  // Detect manual drag to stop auto-centering
  map.on('dragstart', () => {
    map.userHasMoved = true
  })

  // Map click for setting locations
  map.on('click', (e) => {
    if (rideStore.currentBooking) return // lock if already booking

    if (activeSearchType.value === 'pickup') {
      pickup.value = { lat: e.latlng.lat, lng: e.latlng.lng }
      isCurrentLocation.value = false
      updatePickupMarker()
      reverseGeocode(e.latlng.lat, e.latlng.lng, 'pickup')
    } else {
      // Default to dropoff if null or dropoff is focused
      dropoff.value = e.latlng
      if (dropoffMarker) {
        dropoffMarker.setLatLng(e.latlng)
      } else {
        dropoffMarker = L.marker(e.latlng, { icon: destIcon }).addTo(map)
      }
      reverseGeocode(e.latlng.lat, e.latlng.lng, 'dropoff')
      activeSearchType.value = 'dropoff'
    }
  })
})

onUnmounted(() => {
  if (map) map.remove()
  if (watchId && navigator.geolocation) navigator.geolocation.clearWatch(watchId)
})

const updatePickupMarker = () => {
  if (pickupMarker) {
    pickupMarker.setLatLng([pickup.value.lat, pickup.value.lng])
  } else {
    pickupMarker = L.marker([pickup.value.lat, pickup.value.lng], { icon: userIcon }).addTo(map)
  }
}

const centerOnUser = () => {
  if (deviceLocation.value) {
    const lat = deviceLocation.value.lat;
    const lng = deviceLocation.value.lng;
    pickup.value = { lat, lng }
    isCurrentLocation.value = true
    map.flyTo([lat, lng], 16, { animate: true, duration: 0.8 })
    map.userHasMoved = false
    updatePickupMarker()
    reverseGeocode(lat, lng, 'pickup')
  } else {
    alert("Still getting your location...")
  }
}

const requestRide = async () => {
  if (!dropoff.value) return
  await rideStore.createBooking(
    pickup.value.lat,
    pickup.value.lng,
    dropoff.value.lat,
    dropoff.value.lng,
    pickupText.value || 'Current Location',
    dropoffText.value || 'Tap Map Dropoff'
  )
  
  // Center map to show both markers
  const bounds = L.latLngBounds([pickup.value.lat, pickup.value.lng], [dropoff.value.lat, dropoff.value.lng])
  map.flyToBounds(bounds, { padding: [50, 50], animate: true })
}

const cancelRide = async () => {
  if (rideStore.currentBooking) {
    await rideStore.cancelBooking(rideStore.currentBooking.id)
  }
}

// Watch for ride status changes
watch(() => rideStore.currentBooking, (newVal, oldVal) => {
  if (!newVal && oldVal) {
    // Ride was cancelled or ended
    if (driverMarker) {
      map.removeLayer(driverMarker)
      driverMarker = null
    }
    if (routeLine) {
      map.removeLayer(routeLine)
      routeLine = null
    }
    
    // Restore dropoff marker if it was removed during the ride
    if (dropoff.value && !dropoffMarker) {
      dropoffMarker = L.marker([dropoff.value.lat, dropoff.value.lng], { icon: destIcon }).addTo(map)
    }

    // If it was cancelled by someone else, notify
    if (oldVal.status !== 'completed' && oldVal.status !== 'cancelled') {
       alert("Ride has been cancelled.")
    }

    // Clean up chat & call state
    rideStore._cleanupCall()
    rideStore.chatMessages = []
    rideStore.chatOpen = false
  } else if (newVal && oldVal && newVal.status !== oldVal.status) {
    // Status changed
    if (newVal.status === 'accepted' || newVal.status === 'arrived') {
      // Remove destination marker when driver is coming
      if (dropoffMarker) {
        map.removeLayer(dropoffMarker)
        dropoffMarker = null
      }
      // If we have driver location, zoom to show both
      if (rideStore.driverLocation) {
        const bounds = L.latLngBounds([pickup.value.lat, pickup.value.lng], [rideStore.driverLocation.lat, rideStore.driverLocation.lng])
        map.flyToBounds(bounds, { padding: [100, 100], animate: true })
      } else {
        // Just focus on pickup for now
        map.flyTo([pickup.value.lat, pickup.value.lng], 15)
      }
    } else if (newVal.status === 'started') {
      // Re-add destination marker when trip starts
      if (dropoffMarker) map.removeLayer(dropoffMarker)
      dropoffMarker = L.marker([newVal.dropoff_lat, newVal.dropoff_lng], { icon: destIcon }).addTo(map)
      
      // Zoom to show both
      if (rideStore.driverLocation) {
        const bounds = L.latLngBounds([newVal.dropoff_lat, newVal.dropoff_lng], [rideStore.driverLocation.lat, rideStore.driverLocation.lng])
        map.flyToBounds(bounds, { padding: [100, 100], animate: true })
      }
    }
  }
}, { deep: true })

const fetchRoute = async (start, end) => {
  try {
    const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`)
    const data = await res.json()
    if (data.code === 'Ok' && data.routes.length > 0) {
      return data.routes[0].geometry.coordinates.map(c => ({ lat: c[1], lng: c[0] }))
    }
  } catch (err) {
    console.warn("Routing error")
  }
  return null
}

const drawRouteLine = (points) => {
  if (routeLine) map.removeLayer(routeLine)
  const latLngs = points.map(p => [p.lat, p.lng])
  routeLine = L.polyline(latLngs, {
    color: '#3498db',
    weight: 6,
    opacity: 0.6,
    lineJoin: 'round',
    dashArray: '1, 10'
  }).addTo(map)
}

// Watch for driver location updates
watch(() => rideStore.driverLocation, async (newLoc) => {
  if (!newLoc || !map) return
  
  if (!driverMarker) {
    driverMarker = L.marker([newLoc.lat, newLoc.lng], { icon: carIcon, zIndexOffset: 1000 }).addTo(map)
  } else {
    driverMarker.setLatLng([newLoc.lat, newLoc.lng])
  }

  // Update path periodically
  const now = Date.now()
  const target = (rideStore.currentBooking?.status === 'started') ? dropoff.value : pickup.value

  if (now - lastRouteFetch > 5000 && target) {
    lastRouteFetch = now
    const points = await fetchRoute(newLoc, target)
    if (points) drawRouteLine(points)
  }

  if (target && newLoc) {
    const bounds = L.latLngBounds([target.lat, target.lng], [newLoc.lat, newLoc.lng])
    map.flyToBounds(bounds, { padding: [100, 100], animate: true, duration: 1 })
  }
}, { deep: true })

</script>

<style scoped>
/* Mobile First Layout */
.passenger-layout {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #f0f0f0;
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* Global Map Marker Styles (Leaflet generates these dynamically) */
:deep(.custom-map-marker) {
  background: transparent;
  border: none;
}
:deep(.marker-pin) {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
:deep(.pickup-pin) { background: #3498db; }
:deep(.dropoff-pin) { background: #9b59b6; }
:deep(.car-pin) { background: #2ecc71; border: 2px solid #fff; color: #fff; }

:deep(.marker-pulse) {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: rgba(52, 152, 219, 0.4);
  border-radius: 50%;
  animation: pulse 2s infinite ease-out;
  z-index: 1;
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

/* UI Overlays */
.top-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  z-index: 1000;
  pointer-events: none; /* Let clicks pass through to map where transparent */
}

.back-btn {
  pointer-events: auto;
  background: #fff;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-bottom: 1rem;
  color: #333;
  cursor: pointer;
}

.route-card {
  pointer-events: auto;
  background: #fff;
  border-radius: 16px;
  padding: 1rem 1.25rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  border: 1px solid rgba(0,0,0,0.05);
  color: #333;
  backdrop-filter: none; /* solid background for better readability over map */
}

.route-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.back-btn-inline {
  background: #f3f4f6;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}
.back-btn-inline:hover {
  background: #e5e7eb;
}

.header-avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  flex-shrink: 0;
}
.header-face-img, .driver-face-img {
  width: 100%; height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
}

.route-header h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
}

.route-inputs {
  display: flex;
  flex-direction: column;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem;
  margin: -0.5rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.input-row.active-row {
  background-color: rgba(46, 49, 146, 0.05); /* subtle blue tint */
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 0 0 1px #ddd;
}
.pickup-dot { background: #3498db; }
.dropoff-dot { background: #9b59b6; }

.input-divider {
  width: 2px;
  height: 16px;
  background: #eee;
  margin-left: 5px;
  margin-top: 4px;
  margin-bottom: 4px;
}

.input-content {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #222;
}
.value.placeholder { color: #aaa; font-weight: 500; }
.badge { color: #3498db; font-size: 0.75rem; }

.location-input {
  border: none;
  background: transparent;
  font-size: 0.95rem;
  font-weight: 600;
  color: #222;
  flex: 1;
  padding: 0.25rem 0;
  outline: none;
  font-family: inherit;
}
.location-input::placeholder {
  color: #aaa;
  font-weight: 500;
}
.location-input:disabled {
  background: transparent;
  color: #666;
}

.relative { position: relative; }
.w-100 { width: 100%; }

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-top: 5px;
  padding: 0;
  list-style: none;
  max-height: 200px;
  overflow-y: auto;
  z-index: 2000;
  border: 1px solid #eee;
}

.suggestions-list li {
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  color: #333;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.suggestions-list li:hover {
  background: #f8f9fa;
  color: #2e3192;
}

.suggestions-list li:last-child {
  border-bottom: none;
}

.blink { animation: textBlink 1.5s infinite; }
@keyframes textBlink { 50% { opacity: 0.5; } }

.gps-btn-inline {
  background: transparent;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3498db;
  cursor: pointer;
  transition: background-color 0.2s;
  flex-shrink: 0;
}
.gps-btn-inline:hover {
  background: rgba(52, 152, 219, 0.1);
}
.gps-btn-inline:active { transform: scale(0.9); }

/* Bottom Sheet */
.bottom-sheet {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  border-radius: 24px 24px 0 0;
  padding: 0;
  z-index: 1000;
  box-shadow: 0 -8px 24px rgba(0,0,0,0.1);
  color: #333;
  height: 55vh;
  display: flex; flex-direction: column;
  transform: translateY(calc(100% - 90px));
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.bottom-sheet.expanded {
  transform: translateY(0);
}

.sheet-header {
  padding: 1rem 1.5rem 0.75rem 1.5rem;
  cursor: pointer;
  flex-shrink: 0;
  border-bottom: 1px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bottom-sheet.expanded .sheet-header {
  border-bottom: 1px solid #f0f0f0;
}

.sheet-content-wrapper {
  padding: 0 1.5rem 1.5rem 1.5rem;
  overflow-y: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.bottom-sheet.expanded .sheet-content-wrapper {
  overflow-y: auto;
}
.h-100 { height: 100%; }
.flex-col { display: flex; flex-direction: column; }

.drag-handle {
  width: 100%;
  height: 24px;
  color: #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.25rem;
  flex-shrink: 0;
}

.sheet-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0;
  text-align: center;
  flex-shrink: 0;
  color: #2e3192;
}

.ride-options {
  margin-bottom: 1.5rem;
}

.ride-option {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  transition: all 0.2s;
}
.ride-option.active {
  border-color: #2e3192; /* JoyRide Blue */
  background: rgba(46, 49, 146, 0.05);
}

.ride-icon { font-size: 2rem; margin-right: 1rem; }
.ride-details h4 { font-weight: 700; margin-bottom: 0.25rem; }
.ride-details p { font-size: 0.8rem; color: #666; }
.ride-price { margin-left: auto; font-weight: 700; font-size: 1.1rem; color: #2e3192; }

.btn-large {
  padding: 1rem;
  font-size: 1.1rem;
  border-radius: 12px;
  background: #2e3192; /* JoyRide Blue */
  width: 100%;
}
.btn-large:disabled { background: #ccc; }

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
}
.mt-3 { margin-top: 0.75rem; }

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.status-badge.pending { background: #fef08a; color: #854d0e; }
.status-badge.accepted { background: #bbf7d0; color: #166534; }
.status-badge.arrived { background: #3498db; color: #fff; }

.status-content { margin-top: 1.5rem; text-align: center; }
.waiting {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #666;
}
.driver-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 12px;
}
.driver-info.highlight {
  background: #ebf8ff;
  border: 2px solid #3498db;
}
.driver-avatar {
  font-size: 2.5rem;
  background: #fff;
  width: 60px; height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.blink-fast { animation: blink 1s infinite; }
@keyframes blink { 50% { opacity: 0.6; } }

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2e3192;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

/* ── Comm Action Buttons ─────────────────────────── */
.comm-actions {
  display: flex;
  gap: 10px;
  margin-top: 14px;
}
.comm-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 11px 14px;
  border: none;
  border-radius: 14px;
  font-weight: 600;
  font-size: 0.88rem;
  cursor: pointer;
  position: relative;
  transition: transform 0.15s, box-shadow 0.15s;
}
.comm-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.15); }
.chat-btn {
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  color: white;
}
.call-btn {
  background: linear-gradient(135deg, #00c48c, #00a878);
  color: white;
}
.unread-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

/* ── Active Call Bar ─────────────────────────────── */
.active-call-bar {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #ff4757, #c0392b);
  color: white;
  border-radius: 14px;
  padding: 10px 14px;
  font-weight: 600;
  font-size: 0.85rem;
}
.call-live-dot {
  width: 9px;
  height: 9px;
  background: #fff;
  border-radius: 50%;
  animation: live-pulse 1.2s infinite;
  flex-shrink: 0;
}
@keyframes live-pulse { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.4); } }
.mute-btn, .end-call-btn {
  background: rgba(255,255,255,0.25);
  border: none;
  border-radius: 8px;
  color: white;
  padding: 5px 9px;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: auto;
  font-weight: 600;
}
.mute-btn { margin-left: auto; }
.end-call-btn { background: rgba(0,0,0,0.3); }

/* ── From & To Inline Route Card ── */
.route-details-card.inline-route {
  background: rgba(15, 23, 42, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 14px;
  padding: 10px 14px;
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: left;
}
.route-point-inline {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}
.route-icon {
  font-size: 1.05rem;
  flex-shrink: 0;
  line-height: 1.3;
}
.route-inline-text {
  display: flex;
  align-items: baseline;
  gap: 5px;
  flex-wrap: wrap;
  font-size: 0.84rem;
}
.route-inline-label {
  font-weight: 700;
  color: #64748b;
  font-size: 0.8rem;
  flex-shrink: 0;
}
.route-inline-val {
  font-weight: 600;
  color: #1e293b;
  word-break: break-word;
}

/* ── Call Modal Overlay ──────────────────────────── */
.call-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(6px);
}
.call-modal {
  background: linear-gradient(145deg, #1a1a2e, #16213e);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 28px;
  padding: 40px 32px 32px;
  text-align: center;
  color: white;
  width: 300px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.5);
}
.call-ring-icon {
  font-size: 3.5rem;
  animation: ring-shake 0.6s infinite alternate;
  margin-bottom: 16px;
}
@keyframes ring-shake { 0% { transform: rotate(-12deg); } 100% { transform: rotate(12deg); } }
.call-modal h3 { font-size: 1.3rem; margin: 0 0 6px; }
.call-modal p { font-size: 0.9rem; opacity: 0.75; margin: 0 0 24px; }
.call-modal-actions { display: flex; gap: 14px; }
.accept-call-btn, .decline-call-btn {
  flex: 1;
  border: none;
  border-radius: 14px;
  padding: 14px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  transition: transform 0.15s;
}
.accept-call-btn:hover, .decline-call-btn:hover { transform: scale(1.04); }
.accept-call-btn { background: linear-gradient(135deg, #00c48c, #00a878); color: white; }
.decline-call-btn { background: linear-gradient(135deg, #ff4757, #c0392b); color: white; }

/* ── Call-pop Transition ─────────────────────────── */
.call-pop-enter-active { animation: pop-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.call-pop-leave-active { animation: pop-out 0.2s ease-in; }
@keyframes pop-in { from { opacity: 0; transform: scale(0.7); } to { opacity: 1; transform: scale(1); } }
@keyframes pop-out { from { opacity: 1; transform: scale(1); } to { opacity: 0; transform: scale(0.7); } }

/* ── Chat Drawer ─────────────────────────────────── */
.chat-drawer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 68vh;
  background: linear-gradient(160deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 24px 24px 0 0;
  display: flex;
  flex-direction: column;
  z-index: 8888;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.45);
  border-top: 1px solid rgba(255,255,255,0.08);
}
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
}
.chat-close-btn {
  background: rgba(255,255,255,0.1);
  border: none;
  color: white;
  border-radius: 8px;
  width: 32px;
  height: 32px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.chat-close-btn:hover { background: rgba(255,255,255,0.2); }
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  scroll-behavior: smooth;
}
.chat-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: rgba(255,255,255,0.4);
  font-size: 0.9rem;
}
.chat-bubble {
  display: flex;
  flex-direction: column;
  max-width: 78%;
}
.bubble-me {
  align-self: flex-end;
  align-items: flex-end;
}
.bubble-other {
  align-self: flex-start;
  align-items: flex-start;
}
.bubble-text {
  background: rgba(255,255,255,0.1);
  border-radius: 16px 16px 4px 16px;
  padding: 10px 14px;
  color: white;
  font-size: 0.9rem;
  line-height: 1.45;
  word-break: break-word;
}
.bubble-me .bubble-text {
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  border-radius: 16px 16px 4px 16px;
}
.bubble-time {
  font-size: 0.68rem;
  color: rgba(255,255,255,0.35);
  margin-top: 3px;
  padding: 0 4px;
}
.chat-input-row {
  display: flex;
  gap: 10px;
  padding: 12px 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.chat-input {
  flex: 1;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  padding: 11px 16px;
  color: white;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}
.chat-input::placeholder { color: rgba(255,255,255,0.35); }
.chat-input:focus { border-color: rgba(79,142,247,0.7); }
.chat-send-btn {
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  border: none;
  border-radius: 14px;
  width: 46px;
  height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: transform 0.15s;
  flex-shrink: 0;
}
.chat-send-btn:hover { transform: scale(1.08); }
.chat-send-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

/* ── Slide-up Transition ─────────────────────────── */
.slide-up-enter-active { transition: transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s; }
.slide-up-leave-active { transition: transform 0.22s ease-in, opacity 0.2s; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); opacity: 0; }
</style>
