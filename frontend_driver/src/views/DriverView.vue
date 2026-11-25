<template>
  <div class="driver-layout">
    <!-- Fullscreen Map Background -->
    <div id="driver-map" class="map-container"></div>

    <!-- Top Overlay Elements -->
    <div class="top-overlay">
      <!-- Status Card -->
      <div class="route-card glass">
        <div class="route-header">
          <button class="back-btn-inline" @click="$router.push('/dashboard')">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
          </button>
          <div v-if="authStore.user?.face_image_base64" class="header-avatar">
            <img :src="authStore.user.face_image_base64" alt="Me" class="header-face-img" />
          </div>
          <h3 class="flex-1">Driver Mode</h3>
          <button @click="rideStore.fetchBookings()" class="refresh-btn">
             <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
          </button>
        </div>
        <!-- Auto Accept Toggle in Driver Header -->
        <div v-if="!rideStore.currentBooking" class="auto-accept-header-row">
          <span class="aa-lbl">Auto Accept Rides</span>
          <label class="toggle-switch">
            <input type="checkbox" v-model="autoAccept" @change="toggleAutoAccept" />
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>
    </div>

    <!-- Floating Map Controls -->
    <div class="map-controls">
      <button 
        class="control-btn recenter-btn" 
        @click="recenterMap"
        title="Recenter"
      >
        <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>
      </button>
    </div>

    <!-- Bottom Sheet -->
    <div :class="['bottom-sheet', 'glass', { expanded: isSheetExpanded, 'active-booking': rideStore.currentBooking }]">
      <div class="sheet-header" @click="isSheetExpanded = !isSheetExpanded">
        <div class="drag-handle">
          <svg v-if="!isSheetExpanded" viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/></svg>
          <svg v-else viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6z"/></svg>
        </div>
        <h3 v-if="!rideStore.currentBooking" class="sheet-title">Incoming Requests ({{ rideStore.bookings.length }})</h3>
        <h3 v-else class="sheet-title">Active Ride</h3>
      </div>

      <div class="sheet-content-wrapper">
        <div v-if="!rideStore.currentBooking" class="h-100 flex-col">
          <div v-if="rideStore.bookings.length === 0" class="empty-state">
            <div class="radar-pulse">📡</div>
            <p>Looking for passengers...</p>
          </div>
          
          <div class="requests-list">
            <div v-for="booking in rideStore.bookings" :key="booking.id" class="booking-card">
              <div class="passenger-preview">
                <div v-if="booking.passenger_image" class="passenger-avatar-small">
                  <img :src="booking.passenger_image" class="passenger-face-img" />
                </div>
                <div v-else class="passenger-avatar-small">👤</div>
                <span class="passenger-name-small">{{ booking.passenger_name || 'Passenger' }}</span>
              </div>
              <!-- Document Delivery Tag -->
              <div v-if="booking.document_image" class="doc-delivery-request-tag interactive" @click="openDocPreview(booking)">
                <div class="tag-header-row">
                  <span class="tag-badge">📄 Document Delivery</span>
                  <span class="tag-click-prompt">[Click to view details]</span>
                </div>
                <span class="tag-info-preview">{{ booking.document_info }}</span>
                <span v-if="booking.document_tip" class="tag-tip-pill">💰 Tip: ₱{{ booking.document_tip }}</span>
              </div>
              <div class="route-preview">
                <div class="loc-row">
                  <span class="dot pickup-dot"></span>
                  <span class="text-truncate">Pickup: {{ addressNames[booking.id]?.pickup || `${booking.pickup_lat.toFixed(4)}, ${booking.pickup_lng.toFixed(4)}` }}</span>
                </div>
                <div class="loc-row">
                  <span class="dot dropoff-dot"></span>
                  <span class="text-truncate">Dropoff: {{ addressNames[booking.id]?.dropoff || `${booking.dropoff_lat.toFixed(4)}, ${booking.dropoff_lng.toFixed(4)}` }}</span>
                </div>
              </div>
              <div class="d-flex gap-2 mt-2">
                <button @click="acceptRide(booking)" class="btn-primary flex-1">Accept</button>
                <button @click="rideStore.dismissBooking(booking.id)" class="btn-secondary flex-1">Dismiss</button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="status-panel">
          <div class="status-content">
            <div v-if="rideStore.currentBooking.status === 'accepted'" class="accepted">
              <div class="driver-info">
                <div v-if="rideStore.currentBooking.passenger_image" class="driver-avatar blink-fast">
                   <img :src="rideStore.currentBooking.passenger_image" class="passenger-face-img" />
                </div>
                <div v-else class="driver-avatar blink-fast">🚗</div>
                <div>
                  <h4>Driving to {{ rideStore.currentBooking.passenger_name || 'Passenger' }}</h4>
                  <p class="inline-type-container">
                    <span v-if="rideStore.currentBooking.document_image" class="inline-type-badge doc-badge" title="Document Delivery">📄 Document</span>
                    <span v-else class="inline-type-badge passenger-badge" title="Passenger Transport">👤 Person</span>
                    <span class="inline-sep">•</span>
                    <span>Heading to pickup</span>
                  </p>
                  
                  <div class="active-route-details mt-2">
                    <div class="loc-row">
                      <span class="dot pickup-dot"></span>
                      <span class="text-truncate">From: {{ rideStore.currentBooking.pickup_address || addressNames[rideStore.currentBooking.id]?.pickup || 'Resolving...' }}</span>
                    </div>
                    <div class="loc-row">
                      <span class="dot dropoff-dot"></span>
                      <span class="text-truncate">To: {{ rideStore.currentBooking.dropoff_address || addressNames[rideStore.currentBooking.id]?.dropoff || 'Resolving...' }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Waze Navigation to Pickup -->
              <button 
                type="button"
                @click="openWazeToPickup"
                class="btn-waze w-100 mt-3"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" style="display:inline-block; vertical-align:middle; margin-right:8px;"><path d="M12.002 2C6.479 2 2 6.479 2 12.002c0 2.213.722 4.256 1.939 5.922-.191.704-.492 1.815-.658 2.428-.158.583.332 1.111.905.939.615-.184 1.636-.492 2.378-.711a9.932 9.932 0 0 0 5.438 1.422c5.523 0 10.002-4.479 10.002-10.002C22.004 6.479 17.525 2 12.002 2zm-3.668 12.87a1.67 1.67 0 1 1 .001-3.339 1.67 1.67 0 0 1-.001 3.339zm7.336 0a1.67 1.67 0 1 1 0-3.339 1.67 1.67 0 0 1 0 3.339zm-1.834-3.136c.264 0 .478.214.478.478 0 .869-.707 1.576-1.576 1.576s-1.576-.707-1.576-1.576c0-.264.214-.478.478-.478s.478.214.478.478c0 .344.28.62.62.62s.62-.276.62-.62c0-.264.214-.478.478-.478z" fill="#ffffff"/></svg>
                Navigate to Pickup (Waze)
              </button>

              <!-- Google Maps Free Navigation to Pickup -->
              <button 
                type="button"
                @click="openGoogleMapsToPickup"
                class="btn-google-maps w-100 mt-2"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" style="display:inline-block; vertical-align:middle; margin-right:8px;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                Start Navigation (Google Maps)
              </button>
            </div>

            <div v-if="rideStore.currentBooking.status === 'arrived'" class="accepted arrived">
              <div class="driver-info highlight">
                <div v-if="rideStore.currentBooking.passenger_image" class="driver-avatar">
                   <img :src="rideStore.currentBooking.passenger_image" class="passenger-face-img" />
                </div>
                <div v-else class="driver-avatar">👤</div>
                <div>
                  <h4>Arrived for {{ rideStore.currentBooking.passenger_name || 'Passenger' }}</h4>
                  <p class="inline-type-container">
                    <span v-if="rideStore.currentBooking.document_image" class="inline-type-badge doc-badge" title="Document Delivery">📄 Document</span>
                    <span v-else class="inline-type-badge passenger-badge" title="Passenger Transport">👤 Person</span>
                    <span class="inline-sep">•</span>
                    <span>Waiting for pickup</span>
                  </p>
                  
                  <div class="active-route-details mt-2">
                    <div class="loc-row">
                      <span class="dot pickup-dot"></span>
                      <span class="text-truncate">From: {{ rideStore.currentBooking.pickup_address || addressNames[rideStore.currentBooking.id]?.pickup || 'Resolving...' }}</span>
                    </div>
                    <div class="loc-row">
                      <span class="dot dropoff-dot"></span>
                      <span class="text-truncate">To: {{ rideStore.currentBooking.dropoff_address || addressNames[rideStore.currentBooking.id]?.dropoff || 'Resolving...' }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="rideStore.currentBooking.status === 'started'" class="accepted in-progress">
              <div class="driver-info highlight">
                <div class="driver-avatar">
                  <svg viewBox="0 0 24 24" width="28" height="28" style="display: block;">
                    <defs>
                      <linearGradient id="driver-motor-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ff4757"/>
                        <stop offset="100%" stop-color="#ff6b81"/>
                      </linearGradient>
                    </defs>
                    <path d="M19.5 9.5H12V11H19.5V9.5ZM10.5 11.5H3.5V13H10.5V11.5ZM19.5 13.5C21.433 13.5 23 15.067 23 17C23 18.933 21.433 20.5 19.5 20.5C17.567 20.5 16 18.933 16 17C16 15.067 17.567 13.5 19.5 13.5ZM19.5 15C18.395 15 17.5 15.895 17.5 17C17.5 18.105 18.395 19 19.5 19C20.605 19 21.5 18.105 21.5 17C21.5 15.895 20.605 15 19.5 15ZM4.5 13.5C6.433 13.5 8 15.067 8 17C8 18.933 6.433 20.5 4.5 20.5C2.567 20.5 1 18.933 1 17C1 15.067 2.567 13.5 4.5 13.5ZM4.5 15C3.395 15 2.5 15.895 2.5 17C2.5 18.105 3.395 19 4.5 19C5.605 19 6.5 18.105 6.5 17C6.5 15.895 5.605 15 4.5 15ZM12.5 5.5C13.88 5.5 15 6.62 15 8C15 9.38 13.88 10.5 12.5 10.5C11.12 10.5 10 9.38 10 8C10 6.62 11.12 5.5 12.5 5.5ZM12.5 7C11.95 7 11.5 7.45 11.5 8C11.5 8.55 11.95 9 12.5 9C13.05 9 13.5 8.55 13.5 8C13.5 7.45 13.05 7 12.5 7ZM12.5 13.5C11.12 13.5 10 14.62 10 16C10 17.38 11.12 18.5 12.5 18.5C13.88 18.5 15 17.38 15 16C15 14.62 13.88 13.5 12.5 13.5Z" fill="url(#driver-motor-grad)"/>
                  </svg>
                </div>
                <div>
                  <h4>Ride in Progress</h4>
                  <p class="inline-type-container">
                    <span v-if="rideStore.currentBooking.document_image" class="inline-type-badge doc-badge" title="Document Delivery">📄 Document</span>
                    <span v-else class="inline-type-badge passenger-badge" title="Passenger Transport">👤 Person</span>
                    <span class="inline-sep">•</span>
                    <span>Heading to destination</span>
                  </p>
                  
                  <div class="active-route-details mt-2">
                    <div class="loc-row">
                      <span class="dot pickup-dot"></span>
                      <span class="text-truncate">From: {{ rideStore.currentBooking.pickup_address || addressNames[rideStore.currentBooking.id]?.pickup || 'Resolving...' }}</span>
                    </div>
                    <div class="loc-row">
                      <span class="dot dropoff-dot"></span>
                      <span class="text-truncate">To: {{ rideStore.currentBooking.dropoff_address || addressNames[rideStore.currentBooking.id]?.dropoff || 'Resolving...' }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Waze Navigation Integration -->
              <button 
                type="button"
                @click="openWazeToDropoff"
                class="btn-waze w-100 mt-3"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" style="display:inline-block; vertical-align:middle; margin-right:8px;"><path d="M12.002 2C6.479 2 2 6.479 2 12.002c0 2.213.722 4.256 1.939 5.922-.191.704-.492 1.815-.658 2.428-.158.583.332 1.111.905.939.615-.184 1.636-.492 2.378-.711a9.932 9.932 0 0 0 5.438 1.422c5.523 0 10.002-4.479 10.002-10.002C22.004 6.479 17.525 2 12.002 2zm-3.668 12.87a1.67 1.67 0 1 1 .001-3.339 1.67 1.67 0 0 1-.001 3.339zm7.336 0a1.67 1.67 0 1 1 0-3.339 1.67 1.67 0 0 1 0 3.339zm-1.834-3.136c.264 0 .478.214.478.478 0 .869-.707 1.576-1.576 1.576s-1.576-.707-1.576-1.576c0-.264.214-.478.478-.478s.478.214.478.478c0 .344.28.62.62.62s.62-.276.62-.62c0-.264.214-.478.478-.478z" fill="#ffffff"/></svg>
                Navigate in Waze
              </button>

              <!-- Google Maps Free Navigation to Destination -->
              <button 
                type="button"
                @click="openGoogleMapsToDropoff"
                class="btn-google-maps w-100 mt-2"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" style="display:inline-block; vertical-align:middle; margin-right:8px;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                Start Navigation (Google Maps)
              </button>
            </div>

            <!-- Tip Highlight (Document Delivery) -->
            <div v-if="rideStore.currentBooking.document_tip" class="tip-highlight-row mt-2">
              <span class="tip-icon">💰</span>
              <span class="tip-label">Tip from Passenger:</span>
              <span class="tip-value">₱{{ rideStore.currentBooking.document_tip }}</span>
            </div>

            <!-- Manual Arrival Button (Only shown while en route) -->
            <button 
              v-if="rideStore.currentBooking.status === 'accepted'"
              class="btn-primary w-100 mt-3" 
              @click="rideStore.notifyArrived(rideStore.currentBooking.id)"
            >
              I Have Arrived
            </button>

            <!-- Start Ride Button -->
            <button 
              v-if="rideStore.currentBooking.status === 'arrived'"
              class="btn-primary w-100 mt-3" 
              @click="onStartRide"
            >
              Start Ride
            </button>

            <!-- Complete Ride Button -->
            <button 
              v-if="rideStore.currentBooking.status === 'started'"
              class="btn-success w-100 mt-3" 
              @click="onCompleteRide"
            >
              Complete Ride
            </button>

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
                @click="rideStore.initiateCall(rideStore.currentBooking.passenger_id)"
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
                <button class="end-call-btn" @click="rideStore.endCall(rideStore.currentBooking.passenger_id)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
                  End
                </button>
              </div>

              <!-- Direct Phone Call & SMS -->
              <a
                :href="'tel:' + (rideStore.currentBooking?.passenger_phone || '09170000000')"
                class="comm-btn phone-call-btn"
                title="Phone Call"
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.053 15.053 0 0 1-6.59-6.59l2.2-2.21c.28-.26.36-.65.25-1A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>
                Phone Call
              </a>

              <a
                :href="'sms:' + (rideStore.currentBooking?.passenger_phone || '09170000000')"
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
      <div class="call-modal">
        <div class="call-ring-icon">📞</div>
        <h3>Incoming Call</h3>
        <p>{{ rideStore.currentBooking?.passenger_name || 'Passenger' }} is calling you</p>
        <div class="call-modal-actions">
          <button class="accept-call-btn" @click="rideStore.acceptCall(rideStore.currentBooking?.passenger_id)">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
            Accept
          </button>
          <button class="decline-call-btn" @click="rideStore.declineCall(rideStore.currentBooking?.passenger_id)">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
            Decline
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- ── Chat Drawer ── -->
  <Transition name="slide-up">
    <div v-if="rideStore.chatOpen" class="chat-drawer">
      <div class="chat-header">
        <span>💬 Chat with {{ rideStore.currentBooking?.passenger_name || 'Passenger' }}</span>
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
              <div v-if="msg.image" class="delivery-proof-photo-wrap">
                <img :src="msg.image" class="delivery-proof-photo" alt="Proof of Delivery" />
                <span class="delivery-photo-label">📷 Proof of Delivery</span>
              </div>
              <div v-if="msg.signature" class="delivery-sig-wrap">
                <img :src="msg.signature" class="delivery-sig-img" alt="Receiver Signature" />
                <span class="delivery-sig-label">✍️ Receiver's Signature</span>
              </div>
              <p class="delivery-confirm-text">{{ msg.text }}</p>
              <span class="bubble-time" style="align-self: flex-end; margin-top: 4px;">{{ msg.time }}</span>
            </div>
          </template>
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

  <!-- Document Fullscreen Modal -->
  <Transition name="modal-fade">
    <div v-if="showDocModal && selectedPreviewBooking?.document_image" class="modal-overlay" @click.self="showDocModal = false">
      <div class="modal-content glass">
        <div class="modal-wave-container">
          <svg class="modal-waves" xmlns="http://www.w3.org/2000/svg" viewBox="0 24 150 28" preserveAspectRatio="none">
            <defs><path id="gwave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" /></defs>
            <g class="mparallax">
              <use href="#gwave" x="48" y="0" fill="rgba(239,68,68,0.15)" />
              <use href="#gwave" x="48" y="3" fill="rgba(239,68,68,0.28)" />
              <use href="#gwave" x="48" y="5" fill="rgba(239,68,68,0.42)" />
              <use href="#gwave" x="48" y="7" fill="rgba(239,68,68,0.6)" />
            </g>
          </svg>
          <div class="modal-title-wrap"><h3 class="modal-title">📄 Delivery Document</h3></div>
        </div>
        
        <div class="modal-body-scroll">
          <!-- Captured Photo -->
          <div class="modal-img-container">
            <img :src="selectedPreviewBooking.document_image" class="modal-doc-img" alt="Delivery Document" />
          </div>
          
          <div class="modal-doc-details mt-3">
            <div class="mdd-group">
              <label class="mdd-lbl">Cargo Description</label>
              <div class="mdd-val">{{ selectedPreviewBooking.document_info }}</div>
            </div>
            <div v-if="selectedPreviewBooking.document_tip" class="mdd-group mt-2">
              <label class="mdd-lbl">{{ isNaN(selectedPreviewBooking.document_tip) ? 'Instruction / Tip' : 'Rider Tip' }}</label>
              <div class="mdd-val text-warning">
                {{ isNaN(selectedPreviewBooking.document_tip) ? '' : '₱' }}{{ selectedPreviewBooking.document_tip }}
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn-primary w-100" @click="showDocModal = false">Close Preview</button>
        </div>
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

  <!-- ── Document Delivery Confirmation Modal ── -->
  <Transition name="delivery-modal-pop">
    <div v-if="showDeliveryModal" class="delivery-modal-overlay" @click.self="closeDeliveryModal">
      <div class="delivery-modal-card glass">
        <!-- Header -->
        <div class="delivery-modal-header">
          <span class="delivery-modal-icon">📦</span>
          <div>
            <h3 class="delivery-modal-title">Confirm Delivery</h3>
            <p class="delivery-modal-sub">Take a photo & collect signature to complete</p>
          </div>
          <button class="delivery-modal-close" @click="closeDeliveryModal">✕</button>
        </div>

        <!-- Step 1: Camera / Photo -->
        <div class="delivery-step">
          <div class="delivery-step-label">
            <span class="step-badge">1</span>
            <span>Snap proof-of-delivery photo</span>
          </div>

          <!-- Camera preview (shown before snapping) -->
          <div v-if="!deliveryPhoto" class="delivery-cam-box">
            <video ref="deliveryVideoRef" class="delivery-cam-feed" autoplay playsinline muted></video>
            <button class="delivery-snap-btn" @click="snapDeliveryPhoto">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4z"/><path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>
              Snap Photo
            </button>
          </div>

          <!-- Photo preview (shown after snapping) -->
          <div v-else class="delivery-photo-taken-wrap">
            <img :src="deliveryPhoto" class="delivery-photo-taken" alt="Delivery Proof" />
            <button class="delivery-retake-btn" @click="retakeDeliveryPhoto">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
              Retake
            </button>
          </div>
        </div>

        <!-- Step 2: Signature Pad -->
        <div class="delivery-step">
          <div class="delivery-step-label">
            <span class="step-badge">2</span>
            <span>Receiver's signature</span>
          </div>
          <div class="delivery-sig-pad-wrap">
            <canvas
              ref="deliverySigRef"
              class="delivery-sig-pad"
              @mousedown="startSig"
              @mousemove="drawSig"
              @mouseup="endSig"
              @mouseleave="endSig"
              @touchstart.prevent="startSigTouch"
              @touchmove.prevent="drawSigTouch"
              @touchend="endSig"
            ></canvas>
            <div class="sig-pad-actions">
              <span class="sig-pad-hint">Draw signature above</span>
              <button class="delivery-clear-sig-btn" @click="clearSignature">Clear</button>
            </div>
          </div>
        </div>

        <!-- Confirmation Message (auto-filled) -->
        <div class="delivery-confirm-msg-box">
          <span class="delivery-confirm-msg-label">💬 Auto message to passenger</span>
          <p class="delivery-confirm-msg-text">Item have been successfully delivered and received, please inform your receiver.</p>
        </div>

        <!-- Actions -->
        <div class="delivery-modal-actions">
          <button class="delivery-cancel-btn" @click="closeDeliveryModal">Cancel</button>
          <button
            class="delivery-complete-btn"
            :disabled="!deliveryPhoto || !deliverySigData"
            @click="onDeliveryComplete"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>
            Complete &amp; Deliver
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- LIVE DRIVER SUPPORT CHAT FLOATING WIDGET -->
  <SupportChatModal :user="authStore.user" role="Driver" />
</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'
import { useRideStore } from '../stores/ride'
import { useAuthStore } from '../stores/auth'
import SupportChatModal from '../components/SupportChatModal.vue'

const rideStore = useRideStore()
const authStore = useAuthStore()
let map = null
let driverMarker = null
let passengerMarker = null
let heartbeatInterval = null
let watchId = null
let routeLayer = null
const routePoints = ref([])
let lastBearing = 0
let autoFollowTimeout = null

const isSheetExpanded = ref(false)
const addressNames = ref({})
const showDocModal = ref(false)
const selectedPreviewBooking = ref(null)

// ── Delivery Confirmation Modal refs ─────────────────
const showDeliveryModal = ref(false)
const deliveryPhoto = ref(null)        // base64 captured photo
const deliverySigData = ref(null)      // base64 signature
const deliveryVideoRef = ref(null)     // <video> template ref
const deliverySigRef = ref(null)       // <canvas> template ref
let   deliveryCamStream = null         // MediaStream
let   sigIsDrawing = false             // signature pad draw state

const openDocPreview = (booking) => {
  selectedPreviewBooking.value = booking
  showDocModal.value = true
}

// Chat & Call refs
const chatInput = ref('')
const unreadCount = ref(0)
const chatBox = ref(null)

function sendChat() {
  const text = chatInput.value.trim()
  if (!text || !rideStore.currentBooking?.passenger_id) return
  rideStore.sendChatMessage(text, rideStore.currentBooking.passenger_id)
  chatInput.value = ''
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

const autoAccept = ref(localStorage.getItem('auto_accept') === 'true')
const alertedBookings = ref(new Set())

function toggleAutoAccept() {
  localStorage.setItem('auto_accept', autoAccept.value ? 'true' : 'false')
  if (autoAccept.value) {
    checkAndAutoAccept()
  }
}

const resolveAddress = async (lat, lng) => {
  try {
    // Nominatim policy: 1 request per second max.
    await new Promise(r => setTimeout(r, 1100)) 
    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`, {
      headers: { 'User-Agent': 'CAEL-App-PythonLogin-V1' }
    })
    
    if (res.status === 429) return `${lat.toFixed(4)}, ${lng.toFixed(4)}`

    const data = await res.json()
    if (data && data.display_name) {
      const parts = data.display_name.split(',')
      return parts.slice(0, 3).join(',')
    }
  } catch (err) {
    console.warn("Reverse geocoding suppressed")
  }
  return `${lat.toFixed(4)}, ${lng.toFixed(4)}`
}

const getBearing = (startLat, startLng, destLat, destLng) => {
  const toRad = (v) => v * Math.PI / 180
  const toDeg = (v) => v * 180 / Math.PI
  
  const y = Math.sin(toRad(destLng - startLng)) * Math.cos(toRad(destLat))
  const x = Math.cos(toRad(startLat)) * Math.sin(toRad(destLat)) -
            Math.sin(toRad(startLat)) * Math.cos(toRad(destLat)) * Math.cos(toRad(destLng - startLng))
  const brng = toDeg(Math.atan2(y, x))
  return (brng + 360) % 360
}

watch(() => rideStore.bookings, async (newBookings) => {
  for (const b of newBookings) {
    if (!addressNames.value[b.id]) {
      // Prevents multiple fetches for the same ID
      addressNames.value[b.id] = { pickup: 'Resolving...', dropoff: 'Resolving...' }
      const pickup = await resolveAddress(b.pickup_lat, b.pickup_lng)
      const dropoff = await resolveAddress(b.dropoff_lat, b.dropoff_lng)
      addressNames.value[b.id] = { pickup, dropoff }
    }
  }
}, { deep: true, immediate: true })

watch(() => rideStore.currentBooking, async (b) => {
  if (b && !addressNames.value[b.id]) {
    addressNames.value[b.id] = { pickup: 'Resolving...', dropoff: 'Resolving...' }
    const pickup = await resolveAddress(b.pickup_lat, b.pickup_lng)
    const dropoff = await resolveAddress(b.dropoff_lat, b.dropoff_lng)
    addressNames.value[b.id] = { pickup, dropoff }
  }
}, { deep: true, immediate: true })

// Real or fallback driver location
const driverLocation = ref({ lat: 14.5800, lng: 120.9700 })

function openGoogleMapsToPickup() {
  const b = rideStore.currentBooking
  if (!b) return
  const fromLat = driverLocation.value?.lat || 14.5800
  const fromLng = driverLocation.value?.lng || 120.9700
  const toLat = b.pickup_lat
  const toLng = b.pickup_lng
  
  const url = `https://www.google.com/maps/dir/?api=1&origin=${fromLat},${fromLng}&destination=${toLat},${toLng}&travelmode=driving&dir_action=navigate`
  window.open(url, '_blank')
}

function openGoogleMapsToDropoff() {
  const b = rideStore.currentBooking
  if (!b) return
  const fromLat = b.pickup_lat
  const fromLng = b.pickup_lng
  const toLat = b.dropoff_lat
  const toLng = b.dropoff_lng
  
  const url = `https://www.google.com/maps/dir/?api=1&origin=${fromLat},${fromLng}&destination=${toLat},${toLng}&travelmode=driving&dir_action=navigate`
  window.open(url, '_blank')
}

function openWazeToPickup() {
  const b = rideStore.currentBooking
  if (!b) return
  const fromLat = driverLocation.value?.lat || 14.5800
  const fromLng = driverLocation.value?.lng || 120.9700
  const toLat = b.pickup_lat
  const toLng = b.pickup_lng
  const url = `https://www.waze.com/live-map/directions?navigate=yes&from=ll.${fromLat}%2C${fromLng}&to=ll.${toLat}%2C${toLng}`
  window.open(url, '_blank')
}

function openWazeToDropoff() {
  const b = rideStore.currentBooking
  if (!b) return
  const fromLat = b.pickup_lat
  const fromLng = b.pickup_lng
  const toLat = b.dropoff_lat
  const toLng = b.dropoff_lng
  const url = `https://www.waze.com/live-map/directions?navigate=yes&from=ll.${fromLat}%2C${fromLng}&to=ll.${toLat}%2C${toLng}`
  window.open(url, '_blank')
}

const carIcon = L.divIcon({
  className: 'custom-map-marker',
  html: `
    <div class="marker-pin nav-arrow-pin">
      <svg viewBox="0 0 24 24" width="36" height="36" fill="#fff">
        <path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/>
      </svg>
    </div>
  `,
  iconSize: [40, 40],
  iconAnchor: [20, 20]
})

const userIcon = L.divIcon({
  className: 'custom-map-marker',
  html: `<div class="marker-pin pickup-pin">👤</div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 15]
})

onMounted(async () => {
  rideStore.connectWebSocket()
  await rideStore.fetchActiveBooking() // Fetch if already in a ride
  if (rideStore.currentBooking) {
    isSheetExpanded.value = true
  }
  await rideStore.fetchBookings()      // Fetch new requests

  map = L.map('driver-map', { zoomControl: false, tap: false }).setView([driverLocation.value.lat, driverLocation.value.lng], 15)
  
  L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    attribution: '&copy; Google Maps'
  }).addTo(map)

  // Try Geolocating the driver
  if ("geolocation" in navigator) {
    watchId = navigator.geolocation.watchPosition(
      (position) => {
        if (!map) return
        const newLoc = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
        
        // Calculate bearing for rotation
        if (driverLocation.value) {
          const bearing = getBearing(driverLocation.value.lat, driverLocation.value.lng, newLoc.lat, newLoc.lng)
          if (getDistance(driverLocation.value.lat, driverLocation.value.lng, newLoc.lat, newLoc.lng) > 2) {
             lastBearing = bearing
          }
        }

        driverLocation.value = newLoc
        updateDriverMarker()
        
        // Auto-follow / Navigation Logic
        if (map && !map.userHasMoved) {
          if (rideStore.currentBooking) {
            const mapEl = document.querySelector('.map-container')
            if (mapEl) {
              mapEl.style.setProperty('--map-rotation', `${-lastBearing}deg`)
            }
            
            // Zoom in for nav
            const zoom = map.getZoom()
            if (zoom < 17) map.setZoom(18)
            
            // Forward-looking offset to keep icon at bottom-center
            const offset = 0.0012 
            const angleRad = (lastBearing * Math.PI) / 180
            const targetLat = newLoc.lat + offset * Math.cos(angleRad)
            const targetLng = newLoc.lng + offset * Math.sin(angleRad)
            
            map.panTo([targetLat, targetLng], { animate: true, duration: 0.5 })
          } else {
             map.panTo([newLoc.lat, newLoc.lng], { animate: true })
          }
        }

        // Send live GPS update if in a ride
        if (rideStore.currentBooking) {
          rideStore.updateLocation(rideStore.currentBooking.id, newLoc.lat, newLoc.lng)
          
          // Rerouting check
          checkReroute()

          // Auto-arrival check based on real GPS
          if (rideStore.currentBooking.status === 'accepted') {
            const dist = getDistance(
              driverLocation.value.lat, 
              driverLocation.value.lng, 
              rideStore.currentBooking.pickup_lat, 
              rideStore.currentBooking.pickup_lng
            )
            if (dist < 50) { // Within 50 meters
              rideStore.notifyArrived(rideStore.currentBooking.id)
            }
          }
        }
      },
      (error) => {
        console.error("Driver Geolocation Error:", error)
        updateDriverMarker()
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    )
  } else {
    updateDriverMarker()
  }

  map.on('dragstart', () => { 
    map.userHasMoved = true 
    if (autoFollowTimeout) clearTimeout(autoFollowTimeout)
    // Snap back to driver after 5 seconds of no interaction
    autoFollowTimeout = setTimeout(() => {
      map.userHasMoved = false
    }, 5000)
  })

  // Heartbeat to keep driver icon visible even when stationary
  heartbeatInterval = setInterval(() => {
    if (rideStore.currentBooking && driverLocation.value) {
      rideStore.updateLocation(rideStore.currentBooking.id, driverLocation.value.lat, driverLocation.value.lng)
    }
  }, 10000) // Every 10 seconds

  // Fetch the latest profile data for accurate balance validation
  try {
    await authStore.fetchCurrentUser()
  } catch (err) {
    console.error("Failed to fetch fresh user details:", err)
  }

  // Draw initial active booking route if there is one on load/refresh
  if (rideStore.currentBooking) {
    await syncMapWithBooking(rideStore.currentBooking)
  }
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
  if (heartbeatInterval) clearInterval(heartbeatInterval)
  if (watchId && navigator.geolocation) {
    try {
      navigator.geolocation.clearWatch(watchId)
    } catch (e) {}
  }
  stopDeliveryCam()
  rideStore._cleanupCall()
})

// Clean up chat & call when a ride ends
watch(() => rideStore.currentBooking, (newVal, oldVal) => {
  if (!newVal && oldVal) {
    rideStore._cleanupCall()
    rideStore.chatMessages = []
    rideStore.chatOpen = false
  }
})

const updateDriverMarker = () => {
  if (!map) return
  if (!driverMarker) {
    driverMarker = L.marker([driverLocation.value.lat, driverLocation.value.lng], { icon: carIcon }).addTo(map)
  } else {
    driverMarker.setLatLng([driverLocation.value.lat, driverLocation.value.lng])
  }
  
  const el = driverMarker.getElement()
  if (el) {
    const pin = el.querySelector('.marker-pin')
    if (pin) {
      // Icon stays straight (pointing UP) while map rotates around it
      pin.style.transform = `rotate(${lastBearing}deg)`
    }
  }
}

const recenterMap = () => {
  if (map && driverLocation.value) {
    map.userHasMoved = false
    map.setZoom(18)
    map.panTo([driverLocation.value.lat, driverLocation.value.lng], { animate: true })
  }
}

const fetchRoute = async (start, end) => {
  try {
    const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`)
    const data = await res.json()
    if (data.code === 'Ok' && data.routes.length > 0) {
      return data.routes[0].geometry.coordinates.map(c => ({ lat: c[1], lng: c[0] }))
    }
  } catch (err) {
    console.error("Routing error:", err)
  }
  return null
}

const drawRouteLine = (points) => {
  if (!map) return
  if (routeLayer) map.removeLayer(routeLayer)
  routePoints.value = points
  const latLngs = points.map(p => [p.lat, p.lng])
  
  routeLayer = L.layerGroup().addTo(map)
  
  // Base thick line
  L.polyline(latLngs, {
    color: '#2e3192',
    weight: 10,
    opacity: 0.9,
    lineJoin: 'round',
    lineCap: 'round'
  }).addTo(routeLayer)
  
  // Center highlight line
  L.polyline(latLngs, {
    color: '#4f46e5',
    weight: 4,
    opacity: 1,
    lineJoin: 'round',
    lineCap: 'round'
  }).addTo(routeLayer)
}

const syncMapWithBooking = async (booking) => {
  if (!map || !booking) return

  // Clean up existing route/marker
  if (passengerMarker) {
    map.removeLayer(passengerMarker)
    passengerMarker = null
  }
  if (routeLayer) {
    map.removeLayer(routeLayer)
    routeLayer = null
  }

  if (booking.status === 'accepted' || booking.status === 'arrived') {
    // Send initial location immediately so passenger sees icon right away
    rideStore.updateLocation(booking.id, driverLocation.value.lat, driverLocation.value.lng)

    // Show passenger pickup
    passengerMarker = L.marker([booking.pickup_lat, booking.pickup_lng], { icon: userIcon }).addTo(map)
      
    // Fetch road route
    const points = await fetchRoute(driverLocation.value, { lat: booking.pickup_lat, lng: booking.pickup_lng })
    
    if (points && map) {
      drawRouteLine(points)
      // Re-center map to show the whole route
      const bounds = L.latLngBounds(points.map(p => [p.lat, p.lng]))
      map.flyToBounds(bounds, { padding: [50, 50], animate: true })
    } else if (map) {
      // Fallback to straight line
      const bounds = L.latLngBounds([driverLocation.value.lat, driverLocation.value.lng], [booking.pickup_lat, booking.pickup_lng])
      map.flyToBounds(bounds, { padding: [50, 50], animate: true })
    }
  } else if (booking.status === 'started') {
    // Fetch route to destination
    const points = await fetchRoute(driverLocation.value, { lat: booking.dropoff_lat, lng: booking.dropoff_lng })
    if (points && map) {
      drawRouteLine(points)
      
      // Initial zoom for navigation
      map.setZoom(18)
      
      // Set initial bearing toward first point
      if (points.length > 1) {
        lastBearing = getBearing(driverLocation.value.lat, driverLocation.value.lng, points[1].lat, points[1].lng)
      }

      const bounds = L.latLngBounds(points.map(p => [p.lat, p.lng]))
      map.flyToBounds(bounds, { padding: [50, 50], animate: true })
    } else if (map) {
      const bounds = L.latLngBounds([driverLocation.value.lat, driverLocation.value.lng], [booking.dropoff_lat, booking.dropoff_lng])
      map.flyToBounds(bounds, { padding: [50, 50], animate: true })
    }
  }
}

const checkAndAutoAccept = async () => {
  if (!autoAccept.value) return
  if (rideStore.currentBooking) return
  if (rideStore.bookings.length === 0) return

  // Find the first pending booking
  const booking = rideStore.bookings[0]
  
  // Follow the 30% condition
  const requiredBalance = Math.round((booking.amount || 0) * 0.3 * 100) / 100
  const driverBalance = authStore.user?.balance || 0
  
  if (driverBalance < requiredBalance) {
    console.warn(`Auto-accept skipped: Insufficient balance (₱${driverBalance.toFixed(2)} < required ₱${requiredBalance.toFixed(2)})`)
    if (!alertedBookings.value.has(booking.id)) {
      alertedBookings.value.add(booking.id)
      rideStore.triggerAlert({
        title: "Auto-Accept Failed 💰",
        message: `Insufficient balance. You need at least ₱${requiredBalance.toFixed(2)} (30% of fare ₱${(booking.amount || 0).toFixed(2)}) to accept this booking. Current balance: ₱${driverBalance.toFixed(2)}.`,
        type: "warning",
        emoji: "💰"
      })
    }
    return
  }

  console.log("AUTO ACCEPT: Automatically accepting booking", booking.id)
  await acceptRide(booking)
}

const acceptRide = async (booking) => {
  await rideStore.acceptBooking(booking.id)
}

const cancelRide = async () => {
  if (rideStore.currentBooking) {
    await rideStore.cancelBooking(rideStore.currentBooking.id)
  }
}

const onStartRide = async () => {
  await rideStore.startRide(rideStore.currentBooking.id)
}

// ── Delivery confirmation modal logic ─────────────────────────
const openDeliveryModal = async () => {
  deliveryPhoto.value = null
  deliverySigData.value = null
  showDeliveryModal.value = true
  await nextTick()
  // Start back camera
  try {
    deliveryCamStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' } }
    })
    if (deliveryVideoRef.value) {
      deliveryVideoRef.value.srcObject = deliveryCamStream
    }
  } catch (err) {
    console.warn('Delivery camera failed:', err)
  }
  // Initialize signature canvas
  await nextTick()
  initSigCanvas()
}

const initSigCanvas = () => {
  const canvas = deliverySigRef.value
  if (!canvas) return
  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  const ctx = canvas.getContext('2d')
  ctx.scale(dpr, dpr)
  ctx.strokeStyle = '#ffffff'
  ctx.fillStyle = '#ffffff'
  ctx.lineWidth = 3.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
}

const stopDeliveryCam = () => {
  if (deliveryVideoRef.value) {
    deliveryVideoRef.value.srcObject = null
  }
  if (deliveryCamStream) {
    try {
      deliveryCamStream.getTracks().forEach(t => {
        t.stop()
        t.enabled = false
      })
    } catch (e) {
      console.warn('Error stopping camera tracks:', e)
    }
    deliveryCamStream = null
  }
}

const closeDeliveryModal = () => {
  stopDeliveryCam()
  showDeliveryModal.value = false
  deliveryPhoto.value = null
  deliverySigData.value = null
}

const snapDeliveryPhoto = () => {
  const video = deliveryVideoRef.value
  if (!video) return
  const offCanvas = document.createElement('canvas')
  offCanvas.width = video.videoWidth || 640
  offCanvas.height = video.videoHeight || 480
  const ctx = offCanvas.getContext('2d')
  ctx.drawImage(video, 0, 0)
  deliveryPhoto.value = offCanvas.toDataURL('image/jpeg', 0.82)
  stopDeliveryCam()
}

const retakeDeliveryPhoto = async () => {
  deliveryPhoto.value = null
  await nextTick()
  try {
    deliveryCamStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' } }
    })
    if (deliveryVideoRef.value) {
      deliveryVideoRef.value.srcObject = deliveryCamStream
    }
  } catch (err) {
    console.warn('Retake camera failed:', err)
  }
}

// ── Signature pad ───────────────────────────────────
const getPos = (canvas, e) => {
  const rect = canvas.getBoundingClientRect()
  return { x: e.clientX - rect.left, y: e.clientY - rect.top }
}
const startSig = (e) => {
  sigIsDrawing = true
  const canvas = deliverySigRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.strokeStyle = '#ffffff'
  ctx.fillStyle = '#ffffff'
  ctx.lineWidth = 3.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  const pos = getPos(canvas, e)
  ctx.beginPath()
  ctx.moveTo(pos.x, pos.y)
}
const drawSig = (e) => {
  if (!sigIsDrawing) return
  const canvas = deliverySigRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.strokeStyle = '#ffffff'
  ctx.fillStyle = '#ffffff'
  ctx.lineWidth = 3.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  const pos = getPos(canvas, e)
  ctx.lineTo(pos.x, pos.y)
  ctx.stroke()
}
const endSig = () => {
  if (!sigIsDrawing) return
  sigIsDrawing = false
  // Capture signature as base64
  const canvas = deliverySigRef.value
  if (canvas) deliverySigData.value = canvas.toDataURL('image/png')
}

// Touch variants
const getTouchPos = (canvas, touch) => {
  const rect = canvas.getBoundingClientRect()
  return { x: touch.clientX - rect.left, y: touch.clientY - rect.top }
}
const startSigTouch = (e) => {
  sigIsDrawing = true
  const canvas = deliverySigRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.strokeStyle = '#ffffff'
  ctx.fillStyle = '#ffffff'
  ctx.lineWidth = 3.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  const pos = getTouchPos(canvas, e.touches[0])
  ctx.beginPath()
  ctx.moveTo(pos.x, pos.y)
}
const drawSigTouch = (e) => {
  if (!sigIsDrawing) return
  const canvas = deliverySigRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.strokeStyle = '#ffffff'
  ctx.fillStyle = '#ffffff'
  ctx.lineWidth = 3.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  const pos = getTouchPos(canvas, e.touches[0])
  ctx.lineTo(pos.x, pos.y)
  ctx.stroke()
}
const clearSignature = () => {
  const canvas = deliverySigRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.strokeStyle = '#ffffff'
  ctx.fillStyle = '#ffffff'
  ctx.lineWidth = 3.5
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  deliverySigData.value = null
}

const onDeliveryComplete = async () => {
  const booking = rideStore.currentBooking
  if (!booking) return
  
  const photo = deliveryPhoto.value
  const sig = deliverySigData.value

  // Instantly turn off camera stream hardware and close modal
  stopDeliveryCam()
  showDeliveryModal.value = false
  deliveryPhoto.value = null
  deliverySigData.value = null

  // Send delivery confirmation message to passenger
  rideStore.sendDeliveryConfirmation(booking.passenger_id, photo, sig)

  // Complete the ride
  const success = await rideStore.completeRide(booking.id, photo, sig)
  if (success) {
    routePoints.value = []
  }
}

const onCompleteRide = async () => {
  // For document delivery bookings → open delivery confirmation modal
  if (rideStore.currentBooking?.document_image) {
    openDeliveryModal()
    return
  }
  // For regular rides → standard confirm dialog
  rideStore.triggerConfirm({
    title: "Complete Ride? 🏁",
    message: "Have you safely reached the passenger's destination?",
    type: "info",
    emoji: "🏁",
    onConfirm: async () => {
      const success = await rideStore.completeRide(rideStore.currentBooking.id)
      if (success) {
        routePoints.value = []
      }
    }
  })
}

const checkReroute = async () => {
  if (!rideStore.currentBooking || !routePoints.value || routePoints.value.length < 2) return
  
  let minDist = Infinity
  for (const p of routePoints.value) {
    const d = getDistance(driverLocation.value.lat, driverLocation.value.lng, p.lat, p.lng)
    if (d < minDist) minDist = d
  }
  
  // If driver is more than 150m away from the route, recalculate
  if (minDist > 150) {
    console.log("Rerouting...")
    const target = (rideStore.currentBooking.status === 'started') 
      ? { lat: rideStore.currentBooking.dropoff_lat, lng: rideStore.currentBooking.dropoff_lng }
      : { lat: rideStore.currentBooking.pickup_lat, lng: rideStore.currentBooking.pickup_lng }
      
    const points = await fetchRoute(driverLocation.value, target)
    if (points) {
      drawRouteLine(points)
    }
  }
}

watch(() => rideStore.currentBooking, async (newVal, oldVal) => {
  if (newVal) {
    isSheetExpanded.value = true
  }
  if (!map) return
  if (!newVal && oldVal) {
    // Ride was cancelled or ended
    if (passengerMarker) {
      map.removeLayer(passengerMarker)
      passengerMarker = null
    }
    if (routeLayer) {
      map.removeLayer(routeLayer)
      routeLayer = null
    }
    // Reset map perspective for next ride
    if (map) {
      map.setZoom(15)
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
  } else if (newVal && (!oldVal || oldVal.id !== newVal.id || oldVal.status !== newVal.status)) {
    // Ride was accepted, started or status changed
    await syncMapWithBooking(newVal)
  }
}, { deep: true })

// Watch for pending list changes to trigger auto-accept
watch([() => rideStore.bookings, () => autoAccept.value], () => {
  if (autoAccept.value) {
    checkAndAutoAccept()
  }
}, { deep: true, immediate: true })

const getDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371000 // Radius of the earth in m
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

</script>

<style scoped>
.driver-layout {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #f0f0f0;
}

.map-container {
  position: absolute;
  /* Make container larger to prevent white gaps during rotation */
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  z-index: 1;
  background: #e5e7eb;
  /* Heading Up rotation */
  transform: rotateZ(var(--map-rotation, 0deg));
  transform-origin: center center;
  transition: transform 0.5s ease-out;
}

:deep(.custom-map-marker) { background: transparent; border: none; }
:deep(.marker-pin) {
  width: 30px; height: 30px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}
:deep(.nav-arrow-pin) { 
  background: #2e3192; 
  border: 3px solid #fff;
  width: 44px !important;
  height: 44px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.nav-arrow-pin svg) {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}
:deep(.pickup-pin) { background: #3498db; }

/* UI Overlays */
.top-overlay {
  position: absolute;
  top: 0; left: 0; right: 0;
  padding: 1rem;
  z-index: 1000;
  pointer-events: none;
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
.back-btn-inline:hover { background: #e5e7eb; }

.header-avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  flex-shrink: 0;
}
.header-face-img, .passenger-face-img {
  width: 100%; height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
}

.flex-1 { flex: 1; }

.route-card {
  pointer-events: auto;
  background: #fff;
  border-radius: 16px;
  padding: 1rem 1.25rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  border: 1px solid rgba(0,0,0,0.05);
  color: #333;
}

.route-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.route-header h3 {
  font-size: 1.1rem;
  font-weight: 700;
}

.refresh-btn {
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}

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

.requests-list {
  overflow-y: auto;
  flex: 1;
}

.empty-state {
  text-align: center;
  padding: 2rem 0;
  color: #888;
}

.radar-pulse {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: radar 2s infinite;
}
@keyframes radar {
  0% { transform: scale(0.9); opacity: 1; }
  100% { transform: scale(1.2); opacity: 0.5; }
}

.booking-card {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.passenger-preview {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
}

.passenger-avatar-small {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: #eee;
  overflow: hidden;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem;
}

.passenger-name-small {
  font-weight: 600;
  font-size: 0.9rem;
  color: #2e3192;
}

.loc-row {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.85rem; color: #555; margin-bottom: 0.4rem;
}
.dot { width: 10px; height: 10px; border-radius: 50%; }
.pickup-dot { background: #3498db; }
.dropoff-dot { background: #9b59b6; }

.btn-primary {
  background: #2e3192;
  color: #fff;
  border: none;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
}
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
.btn-success {
  background: #10b981;
  color: #fff;
  border: none;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
}
.d-flex { display: flex; }
.gap-2 { gap: 0.5rem; }
.flex-1 { flex: 1; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.w-100 { width: 100%; }

.btn-waze {
  background: #33ccff;
  color: #fff;
  border: none;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 12px rgba(51, 204, 255, 0.3);
}

.btn-google-maps {
  background: #ea4335;
  color: #ffffff;
  border: none;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 12px rgba(234, 67, 53, 0.35);
  transition: all 0.2s ease;
}

.btn-google-maps:hover {
  background: #d93025;
  box-shadow: 0 6px 16px rgba(234, 67, 53, 0.45);
  transform: translateY(-1px);
}

.btn-disabled {
  background: #e2e8f0;
  color: #94a3b8;
  border: 1px dashed #cbd5e1;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: not-allowed;
}

.map-controls {
  position: absolute;
  right: 1rem;
  bottom: 120px; /* Above the bottom sheet drag handle */
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.control-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #fff;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  color: #2e3192;
  cursor: pointer;
  transition: all 0.2s;
}

.control-btn:active {
  transform: scale(0.9);
}

.recenter-btn {
  color: #2e3192;
}

.driver-info {
  display: flex; align-items: center; justify-content: center; gap: 1rem;
  background: #f8f9fa; padding: 1rem; border-radius: 12px;
}
.driver-info.highlight {
  background: #ebf8ff;
  border: 2px solid #3498db;
}
.driver-avatar {
  font-size: 2rem; background: #fff;
  width: 60px; height: 60px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.blink-fast { animation: blink 1s infinite; }
@keyframes blink { 50% { opacity: 0.6; } }

/* ── Auto Accept Toggle Switch in Driver Mode ── */
.auto-accept-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
.aa-lbl {
  font-size: 0.9rem;
  font-weight: 600;
  color: #555;
}
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px; height: 24px;
  flex-shrink: 0;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: rgba(0,0,0,0.06);
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 34px;
  transition: 0.3s;
}
.toggle-slider:before {
  content: "";
  position: absolute;
  height: 16px; width: 16px;
  left: 3px; bottom: 3px;
  background: #aaa;
  border-radius: 50%;
  transition: 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.toggle-switch input:checked + .toggle-slider { background: rgba(46,204,113,0.2); border-color: #2ecc71; }
.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(20px);
  background: #2ecc71;
  box-shadow: 0 0 8px rgba(46,204,113,0.6);
}

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
  top: -6px; right: -6px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 18px; height: 18px;
  font-size: 0.7rem;
  display: flex; align-items: center; justify-content: center;
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
  width: 9px; height: 9px;
  background: #fff;
  border-radius: 50%;
  animation: live-pulse 1.2s infinite;
  flex-shrink: 0;
}
@keyframes live-pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.5; transform:scale(1.4); } }
.mute-btn, .end-call-btn {
  background: rgba(255,255,255,0.25);
  border: none; border-radius: 8px;
  color: white; padding: 5px 9px;
  cursor: pointer; font-size: 0.8rem;
  display: flex; align-items: center; gap: 4px;
  font-weight: 600;
}
.mute-btn { margin-left: auto; }
.end-call-btn { background: rgba(0,0,0,0.3); }

/* ── Call Modal Overlay ──────────────────────────── */
.call-modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999; backdrop-filter: blur(6px);
}
.call-modal {
  background: linear-gradient(145deg, #1a1a2e, #16213e);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 28px; padding: 40px 32px 32px;
  text-align: center; color: white; width: 300px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.5);
}
.call-ring-icon { font-size: 3.5rem; animation: ring-shake 0.6s infinite alternate; margin-bottom: 16px; }
@keyframes ring-shake { 0% { transform: rotate(-12deg); } 100% { transform: rotate(12deg); } }
.call-modal h3 { font-size: 1.3rem; margin: 0 0 6px; }
.call-modal p { font-size: 0.9rem; opacity: 0.75; margin: 0 0 24px; }
.call-modal-actions { display: flex; gap: 14px; }
.accept-call-btn, .decline-call-btn {
  flex: 1; border: none; border-radius: 14px;
  padding: 14px; font-weight: 700; font-size: 0.95rem;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  transition: transform 0.15s;
}
.accept-call-btn:hover, .decline-call-btn:hover { transform: scale(1.04); }
.accept-call-btn { background: linear-gradient(135deg, #00c48c, #00a878); color: white; }
.decline-call-btn { background: linear-gradient(135deg, #ff4757, #c0392b); color: white; }
.call-pop-enter-active { animation: pop-in 0.3s cubic-bezier(0.34,1.56,0.64,1); }
.call-pop-leave-active { animation: pop-out 0.2s ease-in; }
@keyframes pop-in { from { opacity:0; transform:scale(0.7); } to { opacity:1; transform:scale(1); } }
@keyframes pop-out { from { opacity:1; transform:scale(1); } to { opacity:0; transform:scale(0.7); } }

/* ── Chat Drawer ─────────────────────────────────── */
.chat-drawer {
  position: fixed; bottom: 0; left: 0; right: 0;
  height: 68vh;
  background: linear-gradient(160deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 24px 24px 0 0;
  display: flex; flex-direction: column;
  z-index: 8888;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.45);
  border-top: 1px solid rgba(255,255,255,0.08);
}
.chat-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  color: white; font-weight: 600; font-size: 0.95rem;
}
.chat-close-btn {
  background: rgba(255,255,255,0.1);
  border: none; color: white; border-radius: 8px;
  width: 32px; height: 32px; cursor: pointer; font-size: 1rem;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s;
}
.chat-close-btn:hover { background: rgba(255,255,255,0.2); }
.chat-messages {
  flex: 1; overflow-y: auto;
  padding: 16px;
  display: flex; flex-direction: column; gap: 10px;
  scroll-behavior: smooth;
}
.chat-empty {
  display: flex; align-items: center; justify-content: center;
  flex: 1; color: rgba(255,255,255,0.4); font-size: 0.9rem;
}
.chat-bubble { display: flex; flex-direction: column; max-width: 78%; }
.bubble-me { align-self: flex-end; align-items: flex-end; }
.bubble-other { align-self: flex-start; align-items: flex-start; }
.bubble-text {
  background: rgba(255,255,255,0.1);
  border-radius: 16px 16px 4px 16px;
  padding: 10px 14px; color: white;
  font-size: 0.9rem; line-height: 1.45;
  word-break: break-word;
}
.bubble-me .bubble-text {
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  border-radius: 16px 16px 4px 16px;
}
.bubble-time { font-size: 0.68rem; color: rgba(255,255,255,0.35); margin-top: 3px; padding: 0 4px; }
.chat-input-row {
  display: flex; gap: 10px;
  padding: 12px 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.chat-input {
  flex: 1;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px; padding: 11px 16px;
  color: white; font-size: 0.9rem; outline: none;
  transition: border-color 0.2s;
}
.chat-input::placeholder { color: rgba(255,255,255,0.35); }
.chat-input:focus { border-color: rgba(79,142,247,0.7); }
.chat-send-btn {
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  border: none; border-radius: 14px;
  width: 46px; height: 46px;
  display: flex; align-items: center; justify-content: center;
  color: white; cursor: pointer; transition: transform 0.15s; flex-shrink: 0;
}
.chat-send-btn:hover { transform: scale(1.08); }
.chat-send-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.slide-up-enter-active { transition: transform 0.32s cubic-bezier(0.34,1.56,0.64,1), opacity 0.25s; }
.slide-up-leave-active { transition: transform 0.22s ease-in, opacity 0.2s; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); opacity: 0; }
/* ── Document Transport Driver Styles ──────────────── */
.doc-delivery-request-tag {
  display: flex;
  flex-direction: column;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.25);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  text-align: left;
}
.doc-delivery-request-tag.interactive {
  cursor: pointer;
  border-style: dashed;
  transition: all 0.2s ease;
}
.doc-delivery-request-tag.interactive:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.25);
}
.tag-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.2rem;
}
.tag-badge {
  font-size: 0.72rem;
  font-weight: 700;
  color: #3b82f6;
}
.tag-click-prompt {
  font-size: 0.68rem;
  font-weight: 600;
  color: #60a5fa;
  text-decoration: underline;
}
.tag-info-preview {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.document-delivery-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px dashed rgba(59, 130, 246, 0.4);
  border-radius: 8px;
  padding: 0.65rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.document-delivery-mark:hover {
  background: rgba(59, 130, 246, 0.16);
  border-color: #3b82f6;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.2);
}
.mark-badge {
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
}
.mark-link {
  font-size: 0.82rem;
  font-weight: 600;
  color: #60a5fa;
  text-decoration: underline;
}

/* Modal styling for DriverView document preview */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.75); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; z-index: 100000;
}
.modal-content {
  width: 90%; max-width: 420px; padding: 2rem;
  border-radius: 16px; border: 1px solid rgba(139,92,246,0.3);
  background: rgba(22,18,30,0.97);
  box-shadow: 0 20px 45px rgba(0,0,0,0.5), 0 0 35px rgba(139,92,246,0.15);
  display: flex; flex-direction: column; gap: 1.25rem; overflow: hidden;
}
.modal-wave-container {
  position: relative; width: calc(100% + 4rem); margin: -2rem -2rem 0 -2rem;
  height: 90px; background: linear-gradient(135deg, rgba(239,68,68,0.4), rgba(248,113,113,0.2));
  border-bottom: 1px solid rgba(239,68,68,0.2); overflow: hidden;
}
.modal-waves { position: absolute; bottom: -2px; width: 100%; height: 40px; }
.modal-title-wrap { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 10; padding-bottom: 12px; }
.modal-title { font-size: 1.2rem; font-weight: 800; margin: 0; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
.modal-body-scroll {
  max-height: 380px;
  overflow-y: auto;
  padding-right: 0.25rem;
}
.modal-img-container {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
}
.modal-doc-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.modal-doc-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  text-align: left;
}
.mdd-group {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.mdd-lbl {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.5px;
}
.mdd-val {
  font-size: 0.88rem;
  font-weight: 600;
  color: #fff;
  line-height: 1.4;
}

/* ── Inline Booking Type Badges ─────────────────────── */
.inline-type-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 0.82rem;
  color: #aaa;
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
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.25);
}
.inline-type-badge.passenger-badge {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.25);
}
.inline-sep {
  color: #555;
  font-weight: bold;
}

/* ── Delivery Chat Bubbles ───────────────────── */
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
.delivery-proof-photo-wrap, .delivery-sig-wrap {
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

/* ── Delivery Confirmation Modal ────────────────── */
.delivery-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(6px);
  z-index: 9000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 0 0 env(safe-area-inset-bottom, 0px) 0;
}
.delivery-modal-card {
  width: 100%;
  max-width: 480px;
  max-height: 92vh;
  overflow-y: auto;
  border-radius: 24px 24px 0 0;
  background: linear-gradient(160deg, rgba(15,20,40,0.97) 0%, rgba(20,28,55,0.98) 100%);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 24px 20px 36px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.delivery-modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
}
.delivery-modal-icon { font-size: 2rem; }
.delivery-modal-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #fff;
  margin: 0;
}
.delivery-modal-sub {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.45);
  margin: 2px 0 0;
}
.delivery-modal-close {
  margin-left: auto;
  background: rgba(255,255,255,0.07);
  border: none;
  color: rgba(255,255,255,0.6);
  font-size: 1.1rem;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.delivery-modal-close:hover { background: rgba(255,255,255,0.14); }
.delivery-step {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.delivery-step-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: rgba(255,255,255,0.75);
}
.step-badge {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.delivery-cam-box {
  position: relative;
  background: #000;
  border-radius: 14px;
  overflow: hidden;
  aspect-ratio: 4/3;
  border: 1px solid rgba(255,255,255,0.1);
}
.delivery-cam-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.delivery-snap-btn {
  position: absolute;
  bottom: 14px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #4f8ef7, #6c63ff);
  border: none;
  border-radius: 30px;
  color: #fff;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 4px 18px rgba(79,142,247,0.5);
  transition: transform 0.15s, box-shadow 0.15s;
}
.delivery-snap-btn:active { transform: translateX(-50%) scale(0.95); }
.delivery-photo-taken-wrap {
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(16,185,129,0.4);
}
.delivery-photo-taken {
  width: 100%;
  display: block;
  max-height: 200px;
  object-fit: cover;
}
.delivery-retake-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.65);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 20px;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
.delivery-sig-pad-wrap {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.delivery-sig-pad {
  width: 100%;
  height: 120px;
  background: #0f172a;
  border: 1.5px dashed rgba(255,255,255,0.4);
  border-radius: 12px;
  cursor: crosshair;
  touch-action: none;
}
.sig-pad-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sig-pad-hint {
  font-size: 0.72rem;
  color: rgba(255,255,255,0.35);
  font-style: italic;
}
.delivery-clear-sig-btn {
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 8px;
  color: rgba(255,255,255,0.6);
  font-size: 0.75rem;
  padding: 4px 12px;
  cursor: pointer;
  transition: background 0.15s;
}
.delivery-clear-sig-btn:hover { background: rgba(255,255,255,0.12); }
.delivery-confirm-msg-box {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.delivery-confirm-msg-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: rgba(255,255,255,0.35);
}
.delivery-confirm-msg-text {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.75);
  line-height: 1.5;
  margin: 0;
  font-style: italic;
}
.delivery-modal-actions {
  display: flex;
  gap: 12px;
  padding-top: 4px;
}
.delivery-cancel-btn {
  flex: 0 0 auto;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  color: rgba(255,255,255,0.6);
  font-size: 0.9rem;
  font-weight: 600;
  padding: 12px 20px;
  cursor: pointer;
  transition: background 0.15s;
}
.delivery-cancel-btn:hover { background: rgba(255,255,255,0.12); }
.delivery-complete-btn {
  flex: 1;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  border-radius: 14px;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 800;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(16,185,129,0.4);
  transition: transform 0.15s, box-shadow 0.15s, opacity 0.2s;
}
.delivery-complete-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 26px rgba(16,185,129,0.55);
}
.delivery-complete-btn:active:not(:disabled) { transform: scale(0.97); }
.delivery-complete-btn:disabled {
  opacity: 0.38;
  cursor: not-allowed;
  box-shadow: none;
}

/* Delivery modal transition */
.delivery-modal-pop-enter-active { transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s; }
.delivery-modal-pop-leave-active { transition: transform 0.22s ease-in, opacity 0.2s; }
.delivery-modal-pop-enter-from, .delivery-modal-pop-leave-to { transform: translateY(100%); opacity: 0; }

.active-route-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  margin-top: 0.65rem;
}
.active-route-details .loc-row {
  margin: 0;
  color: var(--text-2);
}
.active-route-details .text-truncate {
  max-width: 260px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.82rem;
}

/* ── Tip display elements ── */
.tag-tip-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
  padding: 2px 8px;
  background: rgba(245, 158, 11, 0.18);
  border: 1px solid rgba(245, 158, 11, 0.4);
  border-radius: 20px;
  color: #f59e0b;
  font-size: 0.72rem;
  font-weight: 700;
}
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
</style>
