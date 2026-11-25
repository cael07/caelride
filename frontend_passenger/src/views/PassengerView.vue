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
          <h3 style="flex:1;">Choose route</h3>
          <button class="history-btn-inline" @click="openRideHistoryModal" title="Ride History">
            📜 History
          </button>
        </div>
        
        <div class="route-inputs">
          <div class="input-row relative" :class="{'active-row': activeSearchType === 'pickup'}">
            <div class="dot pickup-dot"></div>
            <div class="input-content w-100">
              <span class="label">Pickup <span class="badge" v-if="isCurrentLocation">(Current)</span></span>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <input 
                  type="text" 
                  class="location-input" 
                  v-model="pickupText" 
                  @input="onInput('pickup')" 
                  @focus="onFocusInput('pickup')" 
                  @blur="onBlurInput" 
                  placeholder="Enter Pickup Location" 
                  :disabled="rideStore.currentBooking" 
                />
                <button 
                  v-if="!rideStore.currentBooking && savedLocations.length > 0" 
                  type="button" 
                  class="history-btn-input" 
                  :class="{ active: activeSavedDropdown === 'pickup' }" 
                  @click.stop="toggleSavedDropdown('pickup')" 
                  title="Pickup History"
                >
                  ⭐ History
                </button>
                <button v-if="!rideStore.currentBooking" class="gps-btn-inline" @click="centerOnUser" title="Current Location">
                   <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
                </button>
              </div>
              <ul class="suggestions-list" v-if="activeSearchType === 'pickup' && suggestions.length > 0">
                <li v-for="s in suggestions" :key="s.place_id" @mousedown.prevent="selectSuggestion(s, 'pickup')">
                  {{ s.display_name }}
                </li>
              </ul>
              <!-- Saved Locations Inline Dropdown triggered by History button -->
              <ul class="suggestions-list saved-dropdown-list" v-else-if="activeSavedDropdown === 'pickup' && savedLocations.length > 0" @mousedown.prevent>
                <li class="saved-dropdown-header" @click.stop>
                  <span>⭐ Pickup History</span>
                  <button type="button" class="dropdown-close-btn" @click.stop="closeSavedDropdown" title="Close saved places">✕</button>
                </li>
                <li 
                  v-for="loc in savedLocations.slice(0, 15)" 
                  :key="loc.id" 
                  class="saved-dropdown-item" 
                  @mousedown.prevent="selectSavedLocation(loc, 'pickup')"
                  @click="selectSavedLocation(loc, 'pickup')"
                >
                  <div class="item-location-box">
                    <span class="location-icon">📍</span>
                    <span class="location-addr truncate">{{ loc.address }}</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <div class="input-divider"></div>
          <div class="input-row relative" :class="{'active-row': activeSearchType === 'dropoff'}">
            <div class="dot dropoff-dot"></div>
            <div class="input-content w-100">
              <span class="label">Drop-off</span>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <input 
                  type="text" 
                  class="location-input" 
                  v-model="dropoffText" 
                  @input="onInput('dropoff')" 
                  @focus="onFocusInput('dropoff')" 
                  @blur="onBlurInput" 
                  placeholder="Tap map or search location" 
                  :disabled="rideStore.currentBooking" 
                />
                <button 
                  v-if="!rideStore.currentBooking && savedLocations.length > 0" 
                  type="button" 
                  class="history-btn-input" 
                  :class="{ active: activeSavedDropdown === 'dropoff' }" 
                  @click.stop="toggleSavedDropdown('dropoff')" 
                  title="Drop-off History"
                >
                  ⭐ History
                </button>
                <button 
                  v-if="!rideStore.currentBooking" 
                  type="button" 
                  class="swap-btn-inline" 
                  @click="swapLocations" 
                  title="Swap Pickup and Drop-off locations"
                >
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M16 17.01V10h-2v7.01h-3L15 21l4-3.99h-3zM9 3L5 6.99h3V14h2V6.99h3L9 3z"/></svg>
                </button>
              </div>
              <ul class="suggestions-list" v-if="activeSearchType === 'dropoff' && suggestions.length > 0">
                <li v-for="s in suggestions" :key="s.place_id" @mousedown.prevent="selectSuggestion(s, 'dropoff')">
                  {{ s.display_name }}
                </li>
              </ul>
              <!-- Saved Locations Inline Dropdown triggered by History button -->
              <ul class="suggestions-list saved-dropdown-list" v-else-if="activeSavedDropdown === 'dropoff' && savedLocations.length > 0" @mousedown.prevent>
                <li class="saved-dropdown-header" @click.stop>
                  <span>⭐ Drop-off History</span>
                  <button type="button" class="dropdown-close-btn" @click.stop="closeSavedDropdown" title="Close saved places">✕</button>
                </li>
                <li 
                  v-for="loc in savedLocations.slice(0, 15)" 
                  :key="loc.id" 
                  class="saved-dropdown-item" 
                  @mousedown.prevent="selectSavedLocation(loc, 'dropoff')"
                  @click="selectSavedLocation(loc, 'dropoff')"
                >
                  <div class="item-location-box">
                    <span class="location-icon">📍</span>
                    <span class="location-addr truncate">{{ loc.address }}</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Sheet -->
    <div :class="['bottom-sheet', 'glass', { expanded: isSheetExpanded, 'active-booking': rideStore.currentBooking }]">
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

            <!-- Visual cue for document attached -->
            <div v-if="rideStore.documentCapture?.image" class="document-attached-pill glass">
              <span class="pill-icon">📄</span>
              <div class="pill-text">
                <span class="pill-title">Document Attached for Delivery</span>
                <span class="pill-desc">{{ rideStore.documentCapture.info }}</span>
              </div>
              <button class="pill-remove-btn" @click="clearAttachedDocument" title="Remove Document">✕</button>
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

            <!-- Driver Info Card — shown for accepted / arrived / started -->
            <div v-if="['accepted','arrived','started'].includes(rideStore.currentBooking.status)" class="driver-card">

              <!-- Status Stepper -->
              <div class="ride-stepper">
                <div class="step" :class="{ active: rideStore.currentBooking.status === 'accepted', done: ['arrived','started'].includes(rideStore.currentBooking.status) }">
                  <div class="step-icon">🛵</div>
                  <span class="step-label">On the way</span>
                </div>
                <div class="step-line" :class="{ done: ['arrived','started'].includes(rideStore.currentBooking.status) }"></div>
                <div class="step" :class="{ active: rideStore.currentBooking.status === 'arrived', done: rideStore.currentBooking.status === 'started' }">
                  <div class="step-icon">📍</div>
                  <span class="step-label">Arrived</span>
                </div>
                <div class="step-line" :class="{ done: rideStore.currentBooking.status === 'started' }"></div>
                <div class="step" :class="{ active: rideStore.currentBooking.status === 'started' }">
                  <div class="step-icon">🏁</div>
                  <span class="step-label">Started</span>
                </div>
              </div>

              <!-- Status message -->
              <p class="driver-status-msg">
                <span v-if="rideStore.currentBooking.status === 'accepted'">🛵 <strong>{{ rideStore.currentBooking.driver_name || 'Driver' }}</strong> is heading to your pickup!</span>
                <span v-else-if="rideStore.currentBooking.status === 'arrived'">📍 <strong>{{ rideStore.currentBooking.driver_name || 'Driver' }}</strong> has arrived at your location!</span>
                <span v-else-if="rideStore.currentBooking.status === 'started'">🏁 Ride in progress — heading to destination!</span>
              </p>

              <!-- Driver Profile -->
              <div class="driver-info-row">
                <div class="driver-avatar-wrap">
                  <img v-if="rideStore.currentBooking.driver_image" :src="rideStore.currentBooking.driver_image" class="driver-face-img" />
                  <div v-else class="driver-avatar-placeholder">👨‍✈️</div>
                  <span v-if="rideStore.currentBooking.status === 'arrived'" class="driver-arrived-dot blink-fast"></span>
                </div>
                <div class="driver-meta">
                  <span class="driver-meta-name">{{ rideStore.currentBooking.driver_name || 'Driver' }}</span>
                  <span class="inline-type-container">
                    <span v-if="rideStore.currentBooking.document_image" class="inline-type-badge doc-badge">📄 Document</span>
                    <span v-else class="inline-type-badge passenger-badge">👤 Person</span>
                  </span>
                </div>
              </div>

              <!-- Vehicle Details -->
              <div class="driver-vehicle-card">
                <div class="vehicle-detail-row">
                  <span class="vd-icon">🪪</span>
                  <span class="vd-label">License No.</span>
                  <span class="vd-value">{{ rideStore.currentBooking.driver_license_number || '—' }}</span>
                </div>
                <div class="vehicle-detail-row">
                  <span class="vd-icon">🏍️</span>
                  <span class="vd-label">Motorcycle</span>
                  <span class="vd-value">
                    {{ [rideStore.currentBooking.driver_moto_brand, rideStore.currentBooking.driver_moto_model].filter(Boolean).join(' ') || '—' }}
                  </span>
                </div>
                <div class="vehicle-detail-row">
                  <span class="vd-icon">🔖</span>
                  <span class="vd-label">Plate No.</span>
                  <span class="vd-value plate-badge">{{ rideStore.currentBooking.driver_plate_number || '—' }}</span>
                </div>
              </div>

              <!-- From & To Route Card -->
              <div class="route-details-card inline-route">
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

            </div>

            <!-- ── Chat & Call Action Buttons ── -->
            <div v-if="rideStore.currentBooking && rideStore.currentBooking.status !== 'pending'" class="comm-actions">
              <button class="comm-btn chat-btn" @click="rideStore.chatOpen = !rideStore.chatOpen">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                Chat
                <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
              </button>

              <button
                v-if="!rideStore.callActive"
                class="comm-btn call-btn"
                @click="rideStore.initiateCall(rideStore.currentBooking.driver_id)"
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
                App Call
              </button>
              <div v-else class="active-call-bar">
                <span class="call-live-dot"></span>
                <span>Call Live</span>
                <button class="mute-btn" @click="rideStore.toggleMute()">
                  {{ rideStore.callMuted ? '🔇' : '🎙️' }}
                </button>
                <button class="end-call-btn" @click="rideStore.endCall(rideStore.currentBooking.driver_id)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
                  End
                </button>
              </div>

              <!-- Direct Phone Call & SMS -->
              <a
                :href="'tel:' + (rideStore.currentBooking?.driver_phone || '09170000001')"
                class="comm-btn phone-call-btn"
                title="Phone Call"
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.053 15.053 0 0 1-6.59-6.59l2.2-2.21c.28-.26.36-.65.25-1A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>
                Phone Call
              </a>

              <a
                :href="'sms:' + (rideStore.currentBooking?.driver_phone || '09170000001')"
                class="comm-btn phone-sms-btn"
                title="Phone SMS"
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
                Phone SMS
              </a>
            </div>

            <button v-if="rideStore.currentBooking.status !== 'arrived' && rideStore.currentBooking.status !== 'started'" class="btn-secondary btn-cancel mt-3 w-100" @click="cancelRide">Cancel Ride</button>
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
          <button class="decline-call-btn" @click="rideStore.declineCall(rideStore.currentBooking?.driver_id)">
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
          :class="['chat-bubble', msg.sender === 'me' ? 'bubble-me' : 'bubble-other', { 'delivery-bubble': msg.is_delivery_confirm }]"
        >
          <!-- Delivery Confirmation Bubble -->
          <template v-if="msg.is_delivery_confirm">
            <div class="delivery-confirm-banner">
              <div class="delivery-banner-header">
                <span class="delivery-banner-icon">📦</span>
                <span class="delivery-banner-title">Delivery Confirmed</span>
              </div>
              <!-- Proof of delivery photo -->
              <div v-if="msg.image" class="delivery-proof-photo-wrap">
                <img :src="msg.image" class="delivery-proof-photo" alt="Proof of Delivery" />
                <span class="delivery-photo-label">📷 Proof of Delivery</span>
              </div>
              <!-- Receiver Signature -->
              <div v-if="msg.signature" class="delivery-sig-wrap">
                <img :src="msg.signature" class="delivery-sig-img" alt="Receiver Signature" />
                <span class="delivery-sig-label">✍️ Receiver's Signature</span>
              </div>
              <p class="delivery-confirm-text">{{ msg.text }}</p>
              <span class="bubble-time" style="align-self: flex-end; margin-top: 4px;">{{ msg.time }}</span>
            </div>
          </template>
          <!-- Regular chat bubble -->
          <template v-else>
            <span class="bubble-text">{{ msg.text }}</span>
            <span class="bubble-time">{{ msg.time }}</span>
          </template>
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

  <!-- Custom Glassmorphic Premium Popup Modal Alert / Confirm -->
  <div v-if="rideStore.customAlert.show" class="custom-alert-overlay">
    <div class="custom-alert-card glass animate-pop">
      <div class="alert-icon-container" :class="rideStore.customAlert.type">
        <span class="alert-emoji">{{ rideStore.customAlert.emoji }}</span>
      </div>
      <h3 class="alert-title">{{ rideStore.customAlert.title }}</h3>
      <p class="alert-message">{{ rideStore.customAlert.message }}</p>
      
      <div v-if="rideStore.customAlert.isConfirm" class="alert-action-row">
        <button class="alert-confirm-btn" @click="rideStore.customAlert.onConfirm()">Yes, Confirm</button>
        <button class="alert-cancel-btn" @click="rideStore.customAlert.onCancel()">Cancel</button>
      </div>
      <button v-else class="alert-dismiss-btn" @click="rideStore.closeAlert()">Got it</button>
    </div>
  </div>
  <!-- ── Ride History Modal ── -->
  <Transition name="lb-fade">
    <div v-if="showHistoryModal" class="ride-modal-overlay" @click.self="showHistoryModal = false">
      <div class="ride-details-modal glass" style="max-width: 560px;">
        <div class="ride-modal-header">
          <div class="ride-modal-title">
            <span class="ride-modal-icon">📜</span>
            <div>
              <h3 style="margin:0; font-size: 1.15rem; font-weight:700; color:#fff;">Ride History</h3>
              <span style="font-size: 0.75rem; color: rgba(255,255,255,0.6);">Your past rides & deliveries</span>
            </div>
          </div>
          <button class="ride-modal-close" @click="showHistoryModal = false">✕</button>
        </div>

        <div class="ride-modal-body">
          <div v-if="historyBookings.length === 0" style="text-align:center; padding: 2rem; color: rgba(255,255,255,0.6);">
            <span style="font-size: 2rem;">🚗</span>
            <p>No ride history found.</p>
          </div>
          <div v-else style="display:flex; flex-direction:column; gap:8px; max-height: 380px; overflow-y:auto;">
            <div 
              v-for="b in historyBookings" 
              :key="b.id" 
              class="audit-log-row glass clickable-ride-row"
              :class="b.document_image ? 'document' : 'ride'"
              @click="selectedRideHistory = b"
              style="padding: 10px 14px; border-radius: 12px; display:flex; justify-content:space-between; align-items:center; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);"
            >
              <div style="display:flex; align-items:center; gap: 10px;">
                <span style="font-size: 1.4rem;">{{ b.document_image ? '📄' : '🛵' }}</span>
                <div>
                  <span style="font-weight:700; color:#fff; font-size:0.9rem; display:block;">{{ b.document_image ? 'Document Delivery' : 'Passenger Ride' }}</span>
                  <span style="font-size:0.72rem; color:rgba(255,255,255,0.6);">{{ formatDate(b.date) }} {{ formatTime(b.date) }}</span>
                </div>
              </div>
              <div style="text-align:right;">
                <span style="font-weight:700; color:#38bdf8; font-size:0.95rem; display:block;">₱{{ (b.amount || 0).toFixed(2) }}</span>
                <span :class="['status-badge', b.status]" style="font-size: 0.6rem; padding: 0.1rem 0.35rem; border-radius: 4px; font-weight: 600; text-transform: uppercase;">{{ b.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>

  <!-- ── Ride Details Sub-Modal ── -->
  <Transition name="lb-fade">
    <div v-if="selectedRideHistory" class="ride-modal-overlay" style="z-index: 10000;" @click.self="selectedRideHistory = null">
      <div class="ride-details-modal glass">
        <div class="ride-modal-header">
          <div class="ride-modal-title">
            <span class="ride-modal-icon">{{ selectedRideHistory.document_image ? '📄' : '🛵' }}</span>
            <div>
              <h3 style="margin:0; font-size: 1.15rem; font-weight:700; color:#fff;">{{ selectedRideHistory.document_image ? 'Document Delivery' : 'Passenger Ride' }}</h3>
              <span style="font-size: 0.75rem; color: rgba(255,255,255,0.6);">Booking #{{ selectedRideHistory.id }} • {{ formatDate(selectedRideHistory.date) }} {{ formatTime(selectedRideHistory.date) }}</span>
            </div>
          </div>
          <button class="ride-modal-close" @click="selectedRideHistory = null">✕</button>
        </div>

        <div class="ride-modal-body">
          <div class="ride-summary-grid">
            <div class="summary-box">
              <span class="summary-lbl">Fare Amount</span>
              <span class="summary-val" style="color: #38bdf8;">₱{{ (selectedRideHistory.amount || 0).toFixed(2) }}</span>
            </div>
            <div v-if="selectedRideHistory.document_tip" class="summary-box">
              <span class="summary-lbl">Tip</span>
              <span class="summary-val" style="color: #fbbf24;">₱{{ selectedRideHistory.document_tip }}</span>
            </div>
            <div class="summary-box">
              <span class="summary-lbl">Status</span>
              <span :class="['status-badge', selectedRideHistory.status]" style="font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700; text-transform: uppercase; display: inline-block; text-align: center;">{{ selectedRideHistory.status }}</span>
            </div>
          </div>

          <div class="route-proof-box">
            <div class="route-row-item mb-2">
              <span style="color:#4ade80;">📍</span>
              <div>
                <span class="summary-lbl" style="display:block;">From (Pickup)</span>
                <span style="font-size:0.85rem; color:#fff; font-weight:500;">{{ selectedRideHistory.pickup }}</span>
              </div>
            </div>
            <div class="route-row-item">
              <span style="color:#f87171;">🏁</span>
              <div>
                <span class="summary-lbl" style="display:block;">To (Destination)</span>
                <span style="font-size:0.85rem; color:#fff; font-weight:500;">{{ selectedRideHistory.dropoff }}</span>
              </div>
            </div>
          </div>

          <div class="ride-summary-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 1rem;">
            <div class="summary-box">
              <span class="summary-lbl">Passenger</span>
              <span style="font-size:0.85rem; font-weight:600; color:#fff;">{{ selectedRideHistory.passenger || selectedRideHistory.passenger_username }}</span>
            </div>
            <div class="summary-box">
              <span class="summary-lbl">Driver</span>
              <span style="font-size:0.85rem; font-weight:600; color:#fff;">{{ selectedRideHistory.driver || selectedRideHistory.driver_username || 'Unassigned' }}</span>
            </div>
          </div>

          <div v-if="selectedRideHistory.document_image || selectedRideHistory.document_info || selectedRideHistory.received_image || selectedRideHistory.signature_image" class="doc-proof-section">
            <div class="doc-proof-title">
              <span>📦 Document & Delivery Details</span>
            </div>

            <p v-if="selectedRideHistory.document_info" style="font-size: 0.8rem; color: rgba(255,255,255,0.85); margin-bottom: 12px; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 8px;">
              <strong>Description:</strong> {{ selectedRideHistory.document_info }}
            </p>

            <div class="doc-gallery-grid">
              <div v-if="selectedRideHistory.document_image" class="gallery-card">
                <span class="gallery-tag">📄 Item Photo</span>
                <img :src="selectedRideHistory.document_image" class="gallery-img" @click="previewImage = selectedRideHistory.document_image" alt="Item Photo" />
              </div>

              <div v-if="selectedRideHistory.received_image" class="gallery-card">
                <span class="gallery-tag">📷 Received Photo</span>
                <img :src="selectedRideHistory.received_image" class="gallery-img" @click="previewImage = selectedRideHistory.received_image" alt="Received Photo" />
              </div>

              <div v-if="selectedRideHistory.signature_image" class="gallery-card">
                <span class="gallery-tag">✍️ Receiver Signature</span>
                <img :src="selectedRideHistory.signature_image" class="gallery-sig-img" @click="previewImage = selectedRideHistory.signature_image" alt="Receiver Signature" />
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </Transition>

  <!-- ── Fullscreen Image Lightbox Preview ── -->
  <Transition name="lb-fade">
    <div v-if="previewImage" class="lightbox-modal-overlay" style="z-index: 10001;" @click="previewImage = null">
      <div class="lightbox-card" @click.stop>
        <button class="lightbox-close" @click="previewImage = null">✕</button>
        <img :src="previewImage" class="lightbox-img" alt="Fullscreen Preview" />
      </div>
    </div>
  </Transition>

  <!-- ── Saved & Frequent Places Modal ── -->
  <Transition name="modal">
    <div v-if="showSavedLocationsModal" class="modal-overlay" style="z-index: 10000;" @click.self="showSavedLocationsModal = false">
      <div class="modal-card glass saved-routes-card">
        <div class="modal-header-bar">
          <div class="header-title-box">
            <span class="header-icon">⭐</span>
            <h3>Saved & Frequent Places</h3>
            <span class="route-count-badge">{{ savedLocations.length }}/20</span>
          </div>
          <button class="modal-close-btn" @click="showSavedLocationsModal = false">&times;</button>
        </div>

        <div class="modal-scroll-body">
          <p class="saved-desc-subtitle">
            Locations you use are automatically saved here (up to 20 unique places). Tap any place to set it in your focused input field.
          </p>

          <div v-if="savedLocations.length === 0" class="empty-saved-routes-box">
            <div class="empty-icon">📍</div>
            <div class="empty-title">No Saved Places Yet</div>
            <div class="empty-sub">Your booked locations will automatically be saved here without duplicates.</div>
          </div>

          <div v-else class="saved-routes-list">
            <div 
              v-for="loc in savedLocations" 
              :key="loc.id" 
              class="saved-location-tile"
              @click="selectSavedLocation(loc)"
            >
              <div class="tile-badge-icon">📍</div>
              <div class="tile-content">
                <span class="tile-addr">{{ loc.address }}</span>
              </div>
              <button 
                class="tile-delete-btn" 
                @click.stop="deleteSavedLocation(loc.id, $event)" 
                title="Remove location"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>

        <div v-if="savedLocations.length > 0" class="modal-footer-bar">
          <span class="footer-info">Auto-deduplicated (max 20 places)</span>
          <button class="clear-all-link" @click="clearAllSavedLocations">Clear History</button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- LIVE SUPPORT CHAT FLOATING WIDGET -->
  <SupportChatModal :user="auth.user" role="Passenger" />
</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'
import { useRideStore } from '../stores/ride'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { authApi } from '../api/auth'
import SupportChatModal from '../components/SupportChatModal.vue'

const rideStore = useRideStore()
const auth = useAuthStore()
const router = useRouter()

const historyBookings = ref([])
const showHistoryModal = ref(false)
const selectedRideHistory = ref(null)
const previewImage = ref(null)

async function openRideHistoryModal() {
  showHistoryModal.value = true
  try {
    const list = await authApi.getBookings()
    historyBookings.value = list || []
  } catch (err) {
    console.error("Failed to fetch ride history:", err)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { timeZone: 'Asia/Manila', month: 'short', day: 'numeric', year: 'numeric' })
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleTimeString('en-US', { timeZone: 'Asia/Manila', hour: '2-digit', minute: '2-digit' })
}
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

// ── Saved Locations History Management (Max 20, De-duplicated) ──
const SAVED_LOCATIONS_KEY = 'ridehailing_passenger_saved_locations_v1'
const savedLocations = ref([])
const showSavedLocationsModal = ref(false)
const activeSavedDropdown = ref(null)

const toggleSavedDropdown = (type) => {
  if (activeSavedDropdown.value === type) {
    activeSavedDropdown.value = null
  } else {
    activeSavedDropdown.value = type
  }
}

const normalizeAddr = (str) => {
  return (str || '').toLowerCase().replace(/[^a-z0-9]/g, '')
}

const isDuplicateLocation = (locA, locB) => {
  const normA = normalizeAddr(locA.address || locA.text)
  const normB = normalizeAddr(locB.address || locB.text)
  if (!normA || !normB) return false

  const stringMatch = normA === normB || (normA.length > 6 && normB.length > 6 && (normA.includes(normB) || normB.includes(normA)))
  const distMatch = Math.abs(locA.lat - locB.lat) < 0.0008 && Math.abs(locA.lng - locB.lng) < 0.0008
  return stringMatch || distMatch
}

const loadSavedLocations = async () => {
  try {
    const raw = localStorage.getItem(SAVED_LOCATIONS_KEY)
    if (raw) {
      savedLocations.value = JSON.parse(raw)
    }
  } catch (err) {
    console.error('Failed to load saved locations:', err)
  }

  // Seed from history if empty
  if (savedLocations.value.length === 0) {
    try {
      const list = await authApi.getBookings()
      if (list && list.length > 0) {
        list.forEach(b => {
          if (b.pickup_lat) {
            const pAddr = b.pickup_address || b.pickup || `${b.pickup_lat}, ${b.pickup_lng}`
            saveLocationToHistory({ lat: b.pickup_lat, lng: b.pickup_lng, address: pAddr })
          }
          if (b.dropoff_lat) {
            const dAddr = b.dropoff_address || b.dropoff || `${b.dropoff_lat}, ${b.dropoff_lng}`
            saveLocationToHistory({ lat: b.dropoff_lat, lng: b.dropoff_lng, address: dAddr })
          }
        })
      }
    } catch (e) {}
  }

  // Deduplicate loaded list
  const cleanList = []
  for (const loc of savedLocations.value) {
    if (!cleanList.some(item => isDuplicateLocation(item, loc))) {
      cleanList.push(loc)
    }
  }
  savedLocations.value = cleanList
}

const saveLocationToHistory = (item) => {
  if (!item?.lat || !item?.lng) return
  const addr = (item.address || item.text || '').trim()
  if (!addr) return

  const newLoc = {
    id: 'loc_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
    address: addr,
    lat: item.lat,
    lng: item.lng,
    timestamp: Date.now()
  }

  // De-duplication check: remove existing matching items
  savedLocations.value = savedLocations.value.filter(l => !isDuplicateLocation(l, newLoc))

  savedLocations.value.unshift(newLoc)

  // Max 15 locations limit (replacing oldest with latest)
  if (savedLocations.value.length > 15) {
    savedLocations.value = savedLocations.value.slice(0, 15)
  }

  try {
    localStorage.setItem(SAVED_LOCATIONS_KEY, JSON.stringify(savedLocations.value))
  } catch (err) {
    console.error('Failed to save location history:', err)
  }
}

const selectSavedLocation = (loc, targetField) => {
  if (!loc) return
  if (blurTimeout) clearTimeout(blurTimeout)

  const target = targetField || activeSavedDropdown.value || activeSearchType.value || 'dropoff'

  if (target === 'pickup') {
    pickupText.value = loc.address
    pickup.value = { lat: loc.lat, lng: loc.lng }
    isCurrentLocation.value = false
    updatePickupMarker()
    if (map) map.flyTo([loc.lat, loc.lng], 15)
  } else {
    dropoffText.value = loc.address
    dropoff.value = { lat: loc.lat, lng: loc.lng }
    if (map) {
      if (dropoffMarker) {
        dropoffMarker.setLatLng([loc.lat, loc.lng])
      } else {
        dropoffMarker = L.marker([loc.lat, loc.lng], { icon: destIcon }).addTo(map)
      }
      map.flyTo([loc.lat, loc.lng], 15)
    }
  }

  activeSavedDropdown.value = null
  activeSearchType.value = null
  showSavedLocationsModal.value = false

  // Blur active input text field
  if (document.activeElement && typeof document.activeElement.blur === 'function') {
    document.activeElement.blur()
  }
}

const deleteSavedLocation = (locId, event) => {
  if (event) event.stopPropagation()
  savedLocations.value = savedLocations.value.filter(l => l.id !== locId)
  try {
    localStorage.setItem(SAVED_LOCATIONS_KEY, JSON.stringify(savedLocations.value))
  } catch (err) {
    console.error('Failed to delete saved location:', err)
  }
}

const clearAllSavedLocations = () => {
  savedLocations.value = []
  try {
    localStorage.removeItem(SAVED_LOCATIONS_KEY)
  } catch (err) {
    console.error('Failed to clear saved locations:', err)
  }
}

const swapLocations = () => {
  if (rideStore.currentBooking) return

  // Swap coordinates
  const tempPickup = pickup.value ? { ...pickup.value } : null
  const tempDropoff = dropoff.value ? { ...dropoff.value } : null
  pickup.value = tempDropoff || { lat: 14.5995, lng: 120.9842 }
  dropoff.value = tempPickup

  // Swap address texts
  const tempPickupText = pickupText.value
  pickupText.value = dropoffText.value
  dropoffText.value = tempPickupText

  // Reset current location indicator
  isCurrentLocation.value = false

  // Update map markers
  updatePickupMarker()
  if (dropoff.value) {
    if (dropoffMarker) {
      dropoffMarker.setLatLng([dropoff.value.lat, dropoff.value.lng])
    } else if (map) {
      dropoffMarker = L.marker([dropoff.value.lat, dropoff.value.lng], { icon: destIcon }).addTo(map)
    }
  } else if (dropoffMarker && map) {
    map.removeLayer(dropoffMarker)
    dropoffMarker = null
  }

  // Adjust map view to show both or single marker
  if (map && pickup.value && dropoff.value) {
    const bounds = L.latLngBounds([pickup.value.lat, pickup.value.lng], [dropoff.value.lat, dropoff.value.lng])
    map.flyToBounds(bounds, { padding: [60, 60], animate: true })
  } else if (map && pickup.value) {
    map.flyTo([pickup.value.lat, pickup.value.lng], 15, { animate: true })
  }
}

let blurTimeout = null

const onFocusInput = (type) => {
  if (blurTimeout) clearTimeout(blurTimeout)
  activeSearchType.value = type
}

const onBlurInput = () => {
  blurTimeout = setTimeout(() => {
    if (!showSavedLocationsModal.value) {
      activeSearchType.value = null
    }
  }, 200)
}

const closeSavedDropdown = () => {
  if (blurTimeout) clearTimeout(blurTimeout)
  activeSavedDropdown.value = null
  activeSearchType.value = null
  if (document.activeElement && typeof document.activeElement.blur === 'function') {
    document.activeElement.blur()
  }
}

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

watch(() => rideStore.chatMessages, (newMessages) => {
  if (!rideStore.chatOpen) {
    unreadCount.value++
  }
}, { deep: true })

watch(() => rideStore.chatOpen, (isOpen) => {
  if (isOpen) {
    unreadCount.value = 0
  }
})

let lastGeocodeTime = { pickup: 0, dropoff: 0 }

const reverseGeocode = async (lat, lng, type) => {
  const now = Date.now()
  // Only throttle if it's not the first time
  if (lastGeocodeTime[type] > 0 && now - lastGeocodeTime[type] < 5000) return 
  lastGeocodeTime[type] = now

  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`, {
      headers: { 'User-Agent': 'CAEL-App-PythonLogin-V1' }
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

const fetchSuggestions = async (query) => {
  const cleanQuery = query.trim()
  if (cleanQuery.length < 3) return []

  let rawResults = []

  // 1. Primary: Photon (Komoot) API - optimized for fast typeahead & partial word matching
  try {
    const photonUrl = `https://photon.komoot.io/api/?q=${encodeURIComponent(cleanQuery)}&limit=8&lat=14.5995&lon=120.9842`
    const res = await fetch(photonUrl)
    if (res.ok) {
      const data = await res.json()
      if (data && data.features && data.features.length > 0) {
        rawResults = data.features.map(f => {
          const props = f.properties || {}
          const name = props.name || ''
          const street = props.street || ''
          const city = props.city || props.county || props.district || props.state || ''
          const fullAddr = [name, street, city].filter(Boolean).join(', ')
          return {
            place_id: props.osm_id || (Math.random() + '_' + Date.now()),
            display_name: fullAddr || name || cleanQuery,
            lat: f.geometry.coordinates[1],
            lon: f.geometry.coordinates[0]
          }
        })
      }
    }
  } catch (e) {
    console.warn("Photon search fallback:", e)
  }

  // 2. Fallback: Nominatim API if Photon has no results
  if (rawResults.length === 0) {
    try {
      const nomUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(cleanQuery)}&limit=8&countrycodes=ph`
      const res = await fetch(nomUrl, {
        headers: { 'User-Agent': 'CAEL-App-PythonLogin-V1' }
      })
      if (res.ok) {
        const data = await res.json()
        if (data && data.length > 0) rawResults = data
      }
    } catch (e) {
      console.warn("Nominatim search fallback:", e)
    }
  }

  // Deduplicate rawResults by normalized display_name & spatial proximity
  const uniqueResults = []
  for (const item of rawResults) {
    const norm = normalizeAddr(item.display_name)
    const isDup = uniqueResults.some(u => {
      const uNorm = normalizeAddr(u.display_name)
      const sameText = uNorm === norm || (norm.length > 6 && uNorm.length > 6 && (uNorm.includes(norm) || norm.includes(uNorm)))
      const sameCoord = Math.abs(u.lat - item.lat) < 0.0005 && Math.abs(u.lon - item.lon) < 0.0005
      return sameText || sameCoord
    })
    if (!isDup) {
      uniqueResults.push(item)
    }
  }

  return uniqueResults.slice(0, 5)
}

const onInput = (type) => {
  activeSearchType.value = type
  if (type === 'pickup') isCurrentLocation.value = false
  const query = type === 'pickup' ? pickupText.value : dropoffText.value
  
  clearTimeout(searchTimeout)
  if (!query || query.trim().length < 3) {
    suggestions.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    suggestions.value = await fetchSuggestions(query)
  }, 250)
}

const selectSuggestion = (suggestion, type) => {
  const lat = typeof suggestion.lat === 'number' ? suggestion.lat : parseFloat(suggestion.lat)
  const lon = typeof suggestion.lon === 'number' ? suggestion.lon : parseFloat(suggestion.lon)
  const parts = (suggestion.display_name || '').split(',')
  const shortAddress = parts.slice(0, 2).join(',') || suggestion.display_name

  if (type === 'pickup') {
    pickupText.value = shortAddress
    pickup.value = { lat, lng: lon }
    isCurrentLocation.value = false
    updatePickupMarker()
    if (map) map.flyTo([lat, lon], 15)
  } else {
    dropoffText.value = shortAddress
    dropoff.value = { lat, lng: lon }
    if (map) {
      if (dropoffMarker) {
        dropoffMarker.setLatLng([lat, lon])
      } else {
        dropoffMarker = L.marker([lat, lon], { icon: destIcon }).addTo(map)
      }
      map.flyTo([lat, lon], 15)
    }
  }
  
  // Close suggestions
  suggestions.value = []
  activeSearchType.value = null
  if (document.activeElement && typeof document.activeElement.blur === 'function') {
    document.activeElement.blur()
  }
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
  loadSavedLocations()
  rideStore.connectWebSocket()
  await rideStore.fetchActiveBooking()
  console.log("DEBUG: Current Booking ->", rideStore.currentBooking)

  // Initialize map fullscreen
  map = L.map('passenger-map', { zoomControl: false, tap: false }).setView([pickup.value.lat, pickup.value.lng], 15)
  
  L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    attribution: '&copy; Google Maps'
  }).addTo(map)

  // If there's an active booking, set the map and markers
  if (rideStore.currentBooking) {
    isSheetExpanded.value = true
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
        if (!map) return
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
    activeSavedDropdown.value = null

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
    }
  })
})

onUnmounted(() => {
  const tempMap = map
  map = null
  if (tempMap) {
    try {
      tempMap.remove()
    } catch (e) {
      console.warn("Leaflet map removal suppressed:", e)
    }
  }
  if (watchId && navigator.geolocation) {
    try {
      navigator.geolocation.clearWatch(watchId)
    } catch (e) {}
  }
})

const updatePickupMarker = () => {
  if (!map) return
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
    rideStore.triggerAlert({
      title: "Locating... 📍",
      message: "Still acquiring GPS coordinates. Please wait a moment.",
      type: "info",
      emoji: "📍"
    })
  }
}

const requestRide = async () => {
  if (!dropoff.value) return

  // Save booked locations to history (max 20 unique places, deduplicated)
  if (pickup.value?.lat && pickupText.value) {
    saveLocationToHistory({ lat: pickup.value.lat, lng: pickup.value.lng, address: pickupText.value })
  }
  if (dropoff.value?.lat && dropoffText.value) {
    saveLocationToHistory({ lat: dropoff.value.lat, lng: dropoff.value.lng, address: dropoffText.value })
  }

  const doc = rideStore.documentCapture || {}
  await rideStore.createBooking(
    pickup.value.lat,
    pickup.value.lng,
    dropoff.value.lat,
    dropoff.value.lng,
    pickupText.value || 'Current Location',
    dropoffText.value || 'Tap Map Dropoff',
    doc.image,
    doc.info,
    doc.tip
  )
  
  // Center map to show both markers
  const bounds = L.latLngBounds([pickup.value.lat, pickup.value.lng], [dropoff.value.lat, dropoff.value.lng])
  if (map) {
    map.flyToBounds(bounds, { padding: [50, 50], animate: true })
  }
}

const clearAttachedDocument = () => {
  rideStore.documentCapture = {
    image: null,
    info: '',
    tip: ''
  }
}

const cancelRide = async () => {
  if (rideStore.currentBooking) {
    await rideStore.cancelBooking(rideStore.currentBooking.id)
  }
}

watch(() => rideStore.currentBooking, (newVal, oldVal) => {
  if (newVal) {
    isSheetExpanded.value = true
  }
  if (!map) return
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
       rideStore.triggerAlert({
         title: "Ride Cancelled ⚠️",
         message: "The booking has been cancelled.",
         type: "warning",
         emoji: "⚠️"
       })
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
  if (!map) return
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
.document-attached-pill {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.25);
  border-radius: 12px;
  margin-bottom: 1rem;
  text-align: left;
}
.pill-icon {
  font-size: 1.5rem;
}
.pill-text {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}
.pill-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #3b82f6;
}
.pill-desc {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.pill-remove-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.18s ease;
}
.pill-remove-btn:hover {
  color: #ef4444;
}

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
  background: rgba(15, 23, 42, 0.95);
  border-radius: 16px;
  padding: 1rem 1.25rem;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #f8fafc;
  backdrop-filter: blur(16px);
}

.route-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.back-btn-inline {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #f8fafc;
  cursor: pointer;
  transition: background-color 0.2s;
}
.back-btn-inline:hover {
  background: rgba(255, 255, 255, 0.2);
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
  color: #fff;
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
  background-color: rgba(59, 130, 246, 0.15);
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
  background: rgba(255, 255, 255, 0.15);
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
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f8fafc;
}
.value.placeholder { color: #64748b; font-weight: 500; }
.badge { color: #38bdf8; font-size: 0.75rem; }

.location-input {
  border: none;
  background: transparent;
  font-size: 0.95rem;
  font-weight: 600;
  color: #f8fafc;
  flex: 1;
  padding: 0.25rem 0;
  outline: none;
  font-family: inherit;
}
.location-input::placeholder {
  color: #64748b;
  font-weight: 500;
}
.location-input:disabled {
  background: transparent;
  color: #475569;
}

.relative { position: relative; }
.w-100 { width: 100%; }

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(15, 23, 42, 0.98);
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.7);
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
  color: #ffffff;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.suggestions-list li:hover {
  background: rgba(59, 130, 246, 0.25);
  color: #ffffff;
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
  overflow: hidden; /* Prevent visual overflow outside sheet bounds */
  pointer-events: auto; /* Explicitly guarantee touch and click captures */
}
.bottom-sheet.active-booking {
  height: 65vh; /* Additional height to display active booking details and action items nicely */
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
  min-height: 0; /* Allow the wrapper to shrink within parent flex context to trigger scrollbar */
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
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
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
.ride-option.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #f8fafc;
  border-color: #e2e8f0;
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
  cursor: pointer;
  pointer-events: auto; /* Guarantee event captures */
  transition: all 0.2s ease;
}
.btn-secondary:hover {
  background: #e5e7eb;
}
.btn-secondary:active {
  transform: scale(0.98);
}
.btn-cancel {
  margin-bottom: 24px; /* Move up to prevent iOS/Android navigation gesture interception */
  margin-bottom: env(safe-area-inset-bottom, 24px);
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
  gap: 8px;
  margin-top: 14px;
  flex-wrap: wrap;
}
.comm-btn {
  flex: 1;
  min-width: 105px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 12px;
  border: none;
  border-radius: 14px;
  font-weight: 600;
  font-size: 0.82rem;
  cursor: pointer;
  position: relative;
  text-decoration: none;
  transition: transform 0.15s, box-shadow 0.15s;
}
.comm-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.15); }
.chat-btn { background: linear-gradient(135deg, #4f8ef7, #6c63ff); color: white; }
.call-btn { background: linear-gradient(135deg, #00c48c, #00a878); color: white; }
.phone-call-btn { background: linear-gradient(135deg, #10b981, #059669); color: white; }
.phone-sms-btn { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
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

/* ── Delivery Confirmation Bubble ───────────────────── */
.delivery-bubble {
  max-width: 92% !important;
  width: 100%;
}
.delivery-confirm-banner {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(5, 150, 105, 0.12));
  border: 1px solid rgba(16, 185, 129, 0.35);
  border-radius: 16px;
  padding: 14px;
  width: 100%;
}
.delivery-banner-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
.delivery-banner-icon { font-size: 1.3rem; }
.delivery-banner-title {
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #34d399;
}
.delivery-proof-photo-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.delivery-proof-photo {
  width: 100%;
  border-radius: 10px;
  border: 1px solid rgba(16, 185, 129, 0.3);
  max-height: 200px;
  object-fit: cover;
}
.delivery-photo-label, .delivery-sig-label {
  font-size: 0.68rem;
  color: rgba(255,255,255,0.45);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.delivery-sig-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.delivery-sig-img {
  width: 100%;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.2);
  background: #0f172a;
  max-height: 90px;
  object-fit: contain;
  padding: 4px;
}
.delivery-confirm-text {
  font-size: 0.83rem;
  color: rgba(255,255,255,0.85);
  line-height: 1.5;
  margin: 0;
}

.inline-type-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 0.82rem;
  color: #666;
  margin-top: 4px;
}
.inline-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 6px;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.inline-type-badge.doc-badge {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.2);
}
.inline-type-badge.passenger-badge {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}
.inline-sep {
  color: #ccc;
  font-weight: bold;
}

/* ── Slide-up Transition ─────────────────────────── */
.slide-up-enter-active { transition: transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s; }
.slide-up-leave-active { transition: transform 0.22s ease-in, opacity 0.2s; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); opacity: 0; }

/* ── Driver Card ─────────────────────────────────── */
.driver-card {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  padding: 0.5rem 0 0.25rem;
}

/* ── Ride Stepper ───────────────────────────────── */
.ride-stepper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  padding: 0.5rem 0.25rem;
  background: rgba(59,130,246,0.06);
  border-radius: 14px;
  border: 1px solid rgba(59,130,246,0.12);
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex: 0 0 auto;
  opacity: 0.38;
  transition: opacity 0.3s;
}
.step.active {
  opacity: 1;
}
.step.done {
  opacity: 0.75;
}
.step-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: background 0.3s, transform 0.3s;
}
.step.active .step-icon {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  box-shadow: 0 3px 10px rgba(59,130,246,0.4);
  transform: scale(1.15);
}
.step.done .step-icon {
  background: #10b981;
}
.step-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.step.active .step-label { color: #2563eb; }
.step.done .step-label  { color: #10b981; }
.step-line {
  flex: 1;
  height: 3px;
  background: #e5e7eb;
  border-radius: 2px;
  margin: 0 4px;
  min-width: 24px;
  margin-bottom: 18px;
  transition: background 0.4s;
}
.step-line.done { background: #10b981; }

/* ── Status Message ─────────────────────────────── */
.driver-status-msg {
  font-size: 0.88rem;
  font-weight: 600;
  color: #374151;
  text-align: center;
  margin: 0;
  line-height: 1.4;
}

/* ── Driver Info Row ────────────────────────────── */
.driver-info-row {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.65rem 0.85rem;
  background: rgba(255,255,255,0.7);
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.07);
}
.driver-avatar-wrap {
  position: relative;
  flex-shrink: 0;
}
.driver-avatar-wrap .driver-face-img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #3b82f6;
}
.driver-avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  border: 2px solid #bfdbfe;
}
.driver-arrived-dot {
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #10b981;
  border: 2px solid #fff;
}
.driver-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.driver-meta-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
}

/* ── Vehicle Details Card ───────────────────────── */
.driver-vehicle-card {
  background: rgba(248, 250, 252, 0.95);
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 12px;
  overflow: hidden;
}
.vehicle-detail-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.9rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
.vehicle-detail-row:last-child { border-bottom: none; }
.vd-icon { font-size: 1rem; width: 20px; text-align: center; }
.vd-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  min-width: 82px;
}
.vd-value {
  font-size: 0.85rem;
  font-weight: 700;
  color: #111827;
  flex: 1;
}
.plate-badge {
  background: #1e3a5f;
  color: #fff;
  padding: 2px 10px;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  letter-spacing: 1.5px;
  font-size: 0.82rem;
  display: inline-block;
}

/* ── Tip row ── */
.tip-highlight-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 10px;
  margin-top: 8px;
}
.tip-icon { font-size: 1rem; }
.tip-label { font-size: 0.8rem; color: var(--text-2); }
.tip-value { font-size: 0.9rem; font-weight: 700; color: #f59e0b; margin-left: auto; }

.history-btn-inline {
  background: rgba(59, 130, 246, 0.18);
  border: 1px solid rgba(59, 130, 246, 0.4);
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}
.history-btn-inline:hover {
  background: rgba(59, 130, 246, 0.35);
  transform: translateY(-1px);
}

.clickable-ride-row {
  cursor: pointer !important;
  transition: transform 0.2s, box-shadow 0.2s;
}
.clickable-ride-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  border-color: rgba(56, 189, 248, 0.4) !important;
}

/* ── Ride Details Modal Styles ── */
.ride-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
  backdrop-filter: blur(8px);
}
.ride-details-modal {
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  color: #fff;
  padding: 1.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
.ride-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}
.ride-modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}
.ride-modal-icon {
  font-size: 1.6rem;
  background: rgba(255, 255, 255, 0.1);
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ride-modal-close {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.1rem;
}
.ride-modal-close:hover { background: rgba(255, 255, 255, 0.2); }

.ride-summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 10px;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.04);
  padding: 12px;
  border-radius: 14px;
}
.summary-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.summary-lbl {
  font-size: 0.68rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  font-weight: 700;
}

.route-proof-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 12px;
  margin-bottom: 1rem;
}
.route-row-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.85rem;
}

.doc-proof-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 14px;
  margin-top: 1rem;
}
.doc-proof-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #fbbf24;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.doc-gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 12px;
  margin-top: 10px;
}
.gallery-card {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.gallery-tag {
  font-size: 0.72rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 6px;
}
.gallery-img {
  width: 100%;
  height: 110px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}
.gallery-img:hover { transform: scale(1.03); }
.gallery-sig-img {
  width: 100%;
  height: 80px;
  object-fit: contain;
  background: #0f172a;
  border-radius: 8px;
  padding: 4px;
  cursor: pointer;
}

/* ── Lightbox Modal Styles ── */
.lightbox-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.88);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1.5rem;
}
.lightbox-card {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}
.lightbox-img {
  max-width: 100%;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}
.lightbox-close {
  position: absolute;
  top: -16px;
  right: -16px;
  background: #ef4444;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}

/* ── Saved Routes Styles ── */
.saved-btn-inline {
  background: rgba(234, 179, 8, 0.18) !important;
  border: 1px solid rgba(234, 179, 8, 0.4) !important;
  color: #facc15 !important;
  padding: 4px 10px !important;
  border-radius: 8px !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.history-btn-input {
  background: rgba(234, 179, 8, 0.15);
  color: #facc15;
  border: 1px solid rgba(234, 179, 8, 0.3);
  padding: 5px 9px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
  line-height: 1.2;
}
.history-btn-input:hover, .history-btn-input.active {
  background: rgba(234, 179, 8, 0.3);
  border-color: #facc15;
  color: #fff;
}
.swap-btn-inline {
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 5px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25 ease;
  flex-shrink: 0;
}
.swap-btn-inline:hover {
  background: rgba(56, 189, 248, 0.3);
  border-color: #38bdf8;
  color: #fff;
  transform: rotate(180deg);
}

.saved-dropdown-list {
  background: rgba(15, 23, 42, 0.95) !important;
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 12px !important;
  padding: 6px !important;
  max-height: 280px;
  overflow-y: auto;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  margin-top: 4px;
}
.saved-dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  font-size: 0.76rem;
  font-weight: 700;
  color: #ffffff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 4px;
}
.dropdown-close-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  border: none;
  font-size: 0.75rem;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}
.dropdown-close-btn:hover {
  background: #ef4444;
  color: #fff;
}
.view-all-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  border: none;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.view-all-btn:hover {
  background: #3b82f6;
  color: #fff;
}
.saved-dropdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px !important;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s ease;
  margin-bottom: 4px;
}
.saved-dropdown-item:hover {
  background: rgba(59, 130, 246, 0.2) !important;
}
.item-route-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}
.item-line {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: #e2e8f0;
}
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}
.mini-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.mini-dot.green { background: #22c55e; }
.mini-dot.red { background: #ef4444; }
.select-badge {
  font-size: 0.7rem;
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 600;
  flex-shrink: 0;
  margin-left: 8px;
}

.saved-routes-card {
  width: 90%;
  max-width: 480px;
  max-height: 85vh;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
}
.modal-header-bar {
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.header-title-box {
  display: flex;
  align-items: center;
  gap: 8px;
}
.header-title-box h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
}
.route-count-badge {
  font-size: 0.75rem;
  background: rgba(234, 179, 8, 0.2);
  color: #facc15;
  border: 1px solid rgba(234, 179, 8, 0.3);
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 700;
}
.modal-close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}
.modal-close-btn:hover { color: #fff; }
.modal-scroll-body {
  padding: 16px 20px;
  overflow-y: auto;
  flex: 1;
}
.saved-desc-subtitle {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 14px;
  line-height: 1.4;
}
.empty-saved-routes-box {
  text-align: center;
  padding: 30px 15px;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 8px; }
.empty-title { font-size: 0.95rem; font-weight: 700; color: #f1f5f9; }
.empty-sub { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
.saved-routes-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.item-location-box {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}
.location-icon {
  font-size: 0.95rem;
  flex-shrink: 0;
}
.location-addr {
  font-size: 0.83rem;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.saved-location-tile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.saved-location-tile:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}
.saved-route-tile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.saved-route-tile:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}
.tile-badge-icon {
  font-size: 1.4rem;
  background: rgba(255, 255, 255, 0.06);
  padding: 8px;
  border-radius: 10px;
  flex-shrink: 0;
}
.tile-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.tile-row {
  display: flex;
  align-items: center;
  gap: 6px;
}
.tile-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.tile-dot.green { background: #22c55e; }
.tile-dot.red { background: #ef4444; }
.tile-connector {
  width: 1px;
  height: 8px;
  background: rgba(255, 255, 255, 0.15);
  margin-left: 3.5px;
}
.tile-addr {
  font-size: 0.83rem;
  font-weight: 500;
  color: #f8fafc;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tile-delete-btn {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  padding: 6px 8px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}
.tile-delete-btn:hover {
  background: #ef4444;
  color: #fff;
}
.modal-footer-bar {
  padding: 12px 20px;
  background: rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.footer-info {
  font-size: 0.75rem;
  color: #64748b;
}
.clear-all-link {
  background: none;
  border: none;
  color: #ef4444;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}
.clear-all-link:hover { text-decoration: underline; }
</style>
