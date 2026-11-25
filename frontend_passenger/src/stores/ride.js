import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useRideStore = defineStore('ride', {
  state: () => ({
    ws: null,
    bookings: [],
    currentBooking: null,
    driverLocation: null, // { lat, lng }
    passengerLocation: null, // { lat, lng }
    // Chat
    chatMessages: [], // [{ sender: 'me'|'other', text, time }]
    chatOpen: false,
    // Call
    incomingCall: false,   // true when we have a pending call_offer
    callActive: false,     // true during live call
    callMuted: false,
    _peerConn: null,       // RTCPeerConnection instance
    _localStream: null,    // MediaStream
    _pendingOffer: null,   // stored SDP offer while waiting for user accept
    // Custom Premium Alert Dialog
    customAlert: {
      show: false,
      title: '',
      message: '',
      type: 'info',
      emoji: '🔔',
      isConfirm: false,
      onConfirm: null,
      onCancel: null
    },
    // Captured document transport state
    documentCapture: {
      image: null,
      info: '',
      tip: ''
    },
  }),

  actions: {
    triggerAlert({ title, message, type = 'info', emoji = '🔔' }) {
      this.customAlert = { show: true, title, message, type, emoji, isConfirm: false, onConfirm: null, onCancel: null }
    },
    triggerConfirm({ title, message, type = 'info', emoji = '❓', onConfirm, onCancel }) {
      this.customAlert = {
        show: true,
        title,
        message,
        type,
        emoji,
        isConfirm: true,
        onConfirm: () => {
          this.closeAlert()
          if (onConfirm) onConfirm()
        },
        onCancel: () => {
          this.closeAlert()
          if (onCancel) onCancel()
        }
      }
    },
    closeAlert() {
      this.customAlert.show = false
    },
    getApiHost() {
      const isLocal = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
      const productionHost = 'https://pythonlogin-api.onrender.com';
      let base = import.meta.env.VITE_API_URL || (isLocal ? 'http://localhost:8000' : productionHost);
      // If VITE_API_URL has /auth at the end, strip it
      if (base.endsWith('/auth')) {
        base = base.replace(/\/auth$/, '');
      }
      return base;
    },

    connectWebSocket() {
      if (this.ws) return
      const auth = useAuthStore()
      if (!auth.user) {
        console.warn("WS: No auth user found")
        return
      }

      const base = this.getApiHost();
      const wsHost = base.replace('http://', 'ws://').replace('https://', 'wss://');
      const wsUrl = `${wsHost}/ride/ws/${auth.user.id}`
      
      console.log("WS: Connecting to", wsUrl)
      this.ws = new WebSocket(wsUrl)
      
      this.ws.onopen = () => {
        console.log("WS: Connection opened")
      }

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        if (data.type === 'new_booking') {
          console.log("WS: New booking received", data.booking)
          this.bookings.push(data.booking)
        } else if (data.type === 'ride_accepted') {
          console.log("DEBUG: Ride Accepted Message Data ->", data)
          if (this.currentBooking && this.currentBooking.id === data.booking_id) {
            // Reassign the whole object to ensure Vue detects the change
            this.currentBooking = {
              ...this.currentBooking,
              status: 'accepted',
              driver_id: data.driver_id,
              driver_name: data.driver_name,
              driver_image: data.driver_image,
              driver_license_number: data.driver_license_number || null,
              driver_plate_number: data.driver_plate_number || null,
              driver_moto_brand: data.driver_moto_brand || null,
              driver_moto_model: data.driver_moto_model || null
            }
          }
        } else if (data.type === 'ride_arrived') {
          console.log("WS: Driver has arrived", data)
          if (this.currentBooking && this.currentBooking.id === data.booking_id) {
            this.currentBooking = {
              ...this.currentBooking,
              status: 'arrived'
            }
            this.triggerAlert({
              title: "Driver Arrived! 🛵",
              message: `${this.currentBooking.driver_name || 'Your driver'} has arrived at your pickup location.`,
              type: "success",
              emoji: "🛵"
            })
          }
        } else if (data.type === 'driver_location') {
          console.log("WS: Received driver location", data)
          // Using == instead of === for loose type matching just in case
          if (this.currentBooking && this.currentBooking.id == data.booking_id) {
            this.driverLocation = { lat: data.lat, lng: data.lng }
          }
        } else if (data.type === 'ride_cancelled') {
          if (this.currentBooking && this.currentBooking.id === data.booking_id) {
            this.currentBooking = null
            this.driverLocation = null
          }
          this.bookings = this.bookings.filter(b => b.id !== data.booking_id)
        } else if (data.type === 'ride_started') {
          console.log("WS: Ride has started", data)
          if (this.currentBooking && this.currentBooking.id === data.booking_id) {
            this.currentBooking = {
              ...this.currentBooking,
              status: 'started'
            }
          }
        } else if (data.type === 'ride_completed') {
          console.log("WS: Ride has been completed", data)
          if (this.currentBooking && this.currentBooking.id === data.booking_id) {
            this.currentBooking.status = 'completed'
            this.currentBooking = null
            this.driverLocation = null
            this.triggerAlert({
              title: "Ride Completed! 🎉",
              message: "Hope you had a great trip. Thank you for riding with us!",
              type: "success",
              emoji: "🎉"
            })
          }
        } else if (data.type === 'booking_taken') {
          // Another driver accepted the ride, remove it from my list
          this.bookings = this.bookings.filter(b => b.id !== data.booking_id)

        } else if (data.type === 'chat_message') {
          this.chatMessages.push({
            sender: 'other',
            text: data.text,
            // Preserve delivery confirmation fields if present
            image: data.image || null,
            signature: data.signature || null,
            is_delivery_confirm: data.is_delivery_confirm || false,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          })
          // Auto-open chat drawer so message is visible
          this.chatOpen = true

        } else if (data.type === 'call_offer') {
          this._pendingOffer = data.sdp
          this.incomingCall = true

        } else if (data.type === 'call_answer') {
          if (this._peerConn) {
            this._peerConn.setRemoteDescription({ type: 'answer', sdp: data.sdp })
          }

        } else if (data.type === 'call_ice') {
          if (this._peerConn && data.candidate) {
            this._peerConn.addIceCandidate(data.candidate).catch(() => {})
          }

        } else if (data.type === 'call_end') {
          this._cleanupCall()
        }
      }
      
      this.ws.onclose = () => {
        console.log("WebSocket connection closed")
        setTimeout(() => this.connectWebSocket(), 3000) // reconnect
      }
    },

    disconnectWebSocket() {
      if (this.ws) {
        this.ws.close()
        this.ws = null
      }
    },

    sendLocationUpdate(bookingId, passengerId, lat, lng) {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({
          type: 'location_update',
          booking_id: bookingId,
          passenger_id: passengerId,
          lat: lat,
          lng: lng
        }))
      }
    },

    updateLocation(bookingId, lat, lng) {
      if (!this.currentBooking) return
      this.sendLocationUpdate(bookingId, this.currentBooking.passenger_id, lat, lng)
    },

    dismissBooking(bookingId) {
      this.bookings = this.bookings.filter(b => b.id !== bookingId)
    },

    async notifyArrived(bookingId) {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();
      
      try {
        const res = await fetch(`${host}/ride/bookings/${bookingId}/arrived`, {
          method: 'POST'
        })
        if (res.ok && this.currentBooking) {
          this.currentBooking.status = 'arrived'
        }
      } catch (err) {
        console.error("Failed to notify arrival:", err)
      }
    },

    async fetchActiveBooking() {
      const auth = useAuthStore()
      if (!auth.user) return
      
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();
      
      try {
        const res = await fetch(`${host}/ride/active/${auth.user.id}`)
        if (res.ok) {
          const booking = await res.json()
          if (booking) {
            this.currentBooking = booking
            this.passengerLocation = { lat: booking.pickup_lat, lng: booking.pickup_lng }
          }
        }
      } catch (err) {
        console.error("Failed to fetch active booking:", err)
      }
    },

    async cancelBooking(bookingId) {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();
      
      try {
        const res = await fetch(`${host}/ride/bookings/${bookingId}/cancel`, {
          method: 'POST'
        })
        if (res.ok) {
          this.currentBooking = null
          this.driverLocation = null
          this.bookings = this.bookings.filter(b => b.id !== bookingId)
          return true
        }
      } catch (err) {
        console.error("Failed to cancel booking:", err)
      }
      return false
    },

    async fetchBookings() {
      const auth = useAuthStore()
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();
      
      try {
        const res = await fetch(`${host}/ride/bookings`)
        if (res.ok) {
          this.bookings = await res.json()
        }
      } catch (err) {
        console.error("Failed to fetch bookings:", err)
      }
    },

    async createBooking(pickupLat, pickupLng, dropoffLat, dropoffLng, pickupAddress = '', dropoffAddress = '', documentImage = null, documentInfo = null, documentTip = null) {
      const auth = useAuthStore()
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();

      try {
        const res = await fetch(`${host}/ride/bookings`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            passenger_id: auth.user.id,
            pickup_lat: pickupLat,
            pickup_lng: pickupLng,
            dropoff_lat: dropoffLat,
            dropoff_lng: dropoffLng,
            pickup_address: pickupAddress,
            dropoff_address: dropoffAddress,
            document_image: documentImage,
            document_info: documentInfo,
            document_tip: documentTip
          })
        })
        const data = await res.json()
        if (res.ok) {
          this.currentBooking = {
            id: data.booking_id,
            passenger_id: auth.user.id,
            status: 'pending',
            pickup_lat: pickupLat,
            pickup_lng: pickupLng,
            dropoff_lat: dropoffLat,
            dropoff_lng: dropoffLng,
            pickup_address: pickupAddress,
            dropoff_address: dropoffAddress,
            document_image: documentImage,
            document_info: documentInfo,
            document_tip: documentTip
          }
          this.passengerLocation = { lat: pickupLat, lng: pickupLng }
          
          // Clear document capture state upon successful booking
          this.documentCapture = {
            image: null,
            info: '',
            tip: ''
          }
          return data.booking_id
        }
      } catch (err) {
        console.error("Failed to create booking:", err)
      }
      return null
    },

    async acceptBooking(bookingId) {
      const auth = useAuthStore()
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();

      try {
        const res = await fetch(`${host}/ride/bookings/${bookingId}/accept`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ driver_id: auth.user.id })
        })
        const data = await res.json()
        if (res.ok) {
          this.currentBooking = data.booking
          return true
        } else {
          // Handle case where ride is already cancelled or taken
          this.triggerAlert({
            title: "Booking Failed ❌",
            message: data.detail || "This ride is no longer available.",
            type: "error",
            emoji: "❌"
          })
          this.bookings = this.bookings.filter(b => b.id !== bookingId)
          return false
        }
      } catch (err) {
        console.error("Failed to accept booking:", err)
      }
      return false
    },

    async startRide(bookingId) {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();
      
      try {
        const res = await fetch(`${host}/ride/bookings/${bookingId}/start`, {
          method: 'POST'
        })
        if (res.ok) {
           if (this.currentBooking) this.currentBooking.status = 'started'
           return true
        }
      } catch (err) {
        console.error("Failed to start ride:", err)
      }
      return false
    },

    async completeRide(bookingId) {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const host = isLocal ? 'http://localhost:8000' : this.getApiHost();
      
      try {
        const res = await fetch(`${host}/ride/bookings/${bookingId}/complete`, {
          method: 'POST'
        })
        if (res.ok) {
           if (this.currentBooking) this.currentBooking.status = 'completed'
           this.currentBooking = null
           this.driverLocation = null
           return true
        }
      } catch (err) {
        console.error("Failed to complete ride:", err)
      }
      return false
    },

    // ── Chat ────────────────────────────────────────────
    sendChatMessage(text, targetUserId) {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return
      const target = targetUserId || (this.currentBooking ? (this.currentBooking.driver_id || this.currentBooking.passenger_id) : null)
      if (!target) {
        console.warn("sendChatMessage: missing target_user_id", this.currentBooking)
        return
      }
      this.ws.send(JSON.stringify({ type: 'chat_message', target_user_id: target, text }))
      this.chatMessages.push({
        sender: 'me',
        text,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      })
    },

    // ── Audio Call ───────────────────────────────────────
    async initiateCall(targetUserId) {
      try {
        this._localStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        this._peerConn = new RTCPeerConnection({
          iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        })
        this._localStream.getTracks().forEach(t => this._peerConn.addTrack(t, this._localStream))

        this._peerConn.onicecandidate = (e) => {
          if (e.candidate && this.ws) {
            this.ws.send(JSON.stringify({
              type: 'call_ice',
              target_user_id: targetUserId,
              candidate: e.candidate
            }))
          }
        }
        this._peerConn.ontrack = (e) => {
          const audio = document.getElementById('remote-audio')
          if (audio) audio.srcObject = e.streams[0]
        }

        const offer = await this._peerConn.createOffer()
        await this._peerConn.setLocalDescription(offer)
        this.ws.send(JSON.stringify({
          type: 'call_offer',
          target_user_id: targetUserId,
          sdp: offer.sdp
        }))
        this.callActive = true
      } catch (err) {
        console.error('Call initiation failed:', err)
        this.triggerAlert({
          title: "Microphone Access 🎤",
          message: "Could not access microphone. Please enable audio permissions for voice calls.",
          type: "warning",
          emoji: "🎤"
        })
      }
    },

    async acceptCall(targetUserId) {
      try {
        this._localStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        this._peerConn = new RTCPeerConnection({
          iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        })
        this._localStream.getTracks().forEach(t => this._peerConn.addTrack(t, this._localStream))

        this._peerConn.onicecandidate = (e) => {
          if (e.candidate && this.ws) {
            this.ws.send(JSON.stringify({
              type: 'call_ice',
              target_user_id: targetUserId,
              candidate: e.candidate
            }))
          }
        }
        this._peerConn.ontrack = (e) => {
          const audio = document.getElementById('remote-audio')
          if (audio) audio.srcObject = e.streams[0]
        }

        await this._peerConn.setRemoteDescription({ type: 'offer', sdp: this._pendingOffer })
        const answer = await this._peerConn.createAnswer()
        await this._peerConn.setLocalDescription(answer)
        this.ws.send(JSON.stringify({
          type: 'call_answer',
          target_user_id: targetUserId,
          sdp: answer.sdp
        }))
        this.incomingCall = false
        this._pendingOffer = null
        this.callActive = true
      } catch (err) {
        console.error('Call accept failed:', err)
      }
    },

    declineCall(targetUserId) {
      const target = targetUserId || (this.currentBooking ? (this.currentBooking.driver_id || this.currentBooking.passenger_id) : null)
      if (this.ws && this.ws.readyState === WebSocket.OPEN && target) {
        this.ws.send(JSON.stringify({ type: 'call_end', target_user_id: target }))
      }
      this._cleanupCall()
    },

    endCall(targetUserId) {
      const target = targetUserId || (this.currentBooking ? (this.currentBooking.driver_id || this.currentBooking.passenger_id) : null)
      if (this.ws && this.ws.readyState === WebSocket.OPEN && target) {
        this.ws.send(JSON.stringify({ type: 'call_end', target_user_id: target }))
      }
      this._cleanupCall()
    },

    toggleMute() {
      if (this._localStream) {
        const track = this._localStream.getAudioTracks()[0]
        if (track) {
          track.enabled = !track.enabled
          this.callMuted = !track.enabled
        }
      }
    },

    _cleanupCall() {
      if (this._peerConn) { this._peerConn.close(); this._peerConn = null }
      if (this._localStream) { this._localStream.getTracks().forEach(t => t.stop()); this._localStream = null }
      const audio = document.getElementById('remote-audio')
      if (audio) audio.srcObject = null
      this.callActive = false
      this.callMuted = false
      this.incomingCall = false
      this._pendingOffer = null
    }
  }
})
