<template>
  <div>
    <!-- FLOATING LIVE SUPPORT BUTTON -->
    <button 
      @click="toggleModal" 
      type="button" 
      class="floating-support-btn" 
      title="Chat Support"
    >
      <span class="support-btn-icon">🎧</span>
      <span class="support-btn-label">Support</span>
      <span v-if="activeTicket" class="support-status-dot" :class="activeTicket.status"></span>
    </button>

    <!-- SUPPORT CHAT MODAL OVERLAY -->
    <Transition name="fade">
      <div v-if="isOpen" class="support-modal-overlay" @click.self="toggleModal">
        <div class="support-modal-card glass">
          
          <!-- MODAL HEADER -->
          <div class="support-modal-header">
            <div class="header-title">
              <span class="header-icon">🎧</span>
              <div>
                <h3 class="title-text">Live Support Chat</h3>
                <p class="subtitle-text">Connect directly with our 24/7 support agents</p>
              </div>
            </div>
            <div class="header-actions">
              <button 
                @click="minimizeModal" 
                class="header-btn minimize-btn" 
                type="button" 
                title="Minimize Support Chat"
              >
                —
              </button>
              <button 
                @click="closeModal" 
                class="header-btn close-btn" 
                type="button" 
                title="Close Support Chat"
              >
                ✕
              </button>
            </div>
          </div>

          <!-- MODAL BODY -->
          <div class="support-modal-body">
            
            <!-- CASE 1: NO ACTIVE TICKET — CREATE SUPPORT REQUEST FORM -->
            <div v-if="!activeTicket" class="support-form-box">
              <div v-if="submitSuccessMsg" class="alert-box success">
                ✅ {{ submitSuccessMsg }}
              </div>
              <div v-if="submitErrorMsg" class="alert-box error">
                ⚠️ {{ submitErrorMsg }}
              </div>

              <div class="form-group">
                <label class="form-label">📌 Support Category / Topic</label>
                <select v-model="topic" class="form-select">
                  <option value="Booking / Ride Issue">🚗 Booking / Ride Issue</option>
                  <option value="Wallet & Cashout">💳 Wallet & Cashout / Top-up</option>
                  <option value="Account & Verification">👤 Account & Verification</option>
                  <option value="App Bug / Technical Issue">🐛 App Bug / Technical Issue</option>
                  <option value="General Support">❓ General Support</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">💬 How can we assist you today?</label>
                <textarea 
                  v-model="initialMessage" 
                  rows="4" 
                  class="form-textarea" 
                  placeholder="Describe your issue or question in detail..."
                ></textarea>
              </div>

              <button 
                @click="submitTicket" 
                :disabled="isSubmitting || !initialMessage.trim()" 
                type="button" 
                class="btn-submit-support"
              >
                <span v-if="isSubmitting">Submitting Request...</span>
                <span v-else>🚀 Enter Support Queue</span>
              </button>
            </div>

            <!-- CASE 2: ACTIVE OR WAITING TICKET CHAT ROOM -->
            <div v-else class="support-chat-room">
              
              <!-- QUEUE / AGENT STATUS BANNER -->
              <div v-if="activeTicket.status === 'waiting'" class="status-banner waiting">
                <div class="banner-icon">⏳</div>
                <div>
                  <div class="banner-title">You are currently in queue</div>
                  <div class="banner-sub">Queue Position: #{{ activeTicket.queue_position || 1 }}. A support agent will claim your request shortly.</div>
                </div>
              </div>

              <div v-else-if="activeTicket.status === 'active'" class="status-banner active">
                <div class="banner-icon">🟢</div>
                <div>
                  <div class="banner-title">Agent {{ activeTicket.agent_name || 'Support' }} is assisting you live</div>
                  <div class="banner-sub">Topic: {{ activeTicket.topic }}</div>
                </div>
              </div>

              <!-- CHAT MESSAGES THREAD -->
              <div class="chat-messages-container" ref="messagesBox">
                <div 
                  v-for="msg in messages" 
                  :key="msg.id" 
                  :class="['chat-bubble-wrap', msg.sender_type === 'user' ? 'outgoing' : 'incoming']"
                >
                  <div class="sender-info">
                    {{ msg.sender_name }} • {{ msg.created_at }}
                  </div>
                  <div class="chat-bubble">
                    {{ msg.text }}
                  </div>
                </div>
              </div>

              <!-- CHAT INPUT AREA -->
              <div class="chat-input-area">
                <input 
                  v-model="chatReplyText" 
                  @keyup.enter="sendReply" 
                  type="text" 
                  class="chat-reply-input" 
                  placeholder="Type a message to support..." 
                />
                <button 
                  @click="sendReply" 
                  :disabled="!chatReplyText.trim()" 
                  type="button" 
                  class="btn-send-chat"
                >
                  Send 🚀
                </button>
              </div>

            </div>

          </div>

        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { authApi } from '../api/auth'

const props = defineProps({
  user: {
    type: Object,
    default: () => ({})
  },
  role: {
    type: String,
    default: 'Passenger'
  }
})

const isOpen = ref(false)
const isMinimized = ref(false)
const topic = ref('Booking / Ride Issue')
const initialMessage = ref('')
const isSubmitting = ref(false)
const submitSuccessMsg = ref('')
const submitErrorMsg = ref('')

const activeTicket = ref(null)
const messages = ref([])
const chatReplyText = ref('')
const messagesBox = ref(null)
let pollInterval = null

const userName = computed(() => {
  return props.user?.full_name || props.user?.username || localStorage.getItem('user_name') || 'Passenger User'
})

function minimizeModal() {
  isMinimized.value = true
  isOpen.value = false
}

function closeModal() {
  isMinimized.value = false
  isOpen.value = false
  stopPolling()
}

function toggleModal() {
  isMinimized.value = false
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    checkActiveTicket()
    startPolling()
  } else {
    stopPolling()
  }
}

async function checkActiveTicket() {
  try {
    const res = await authApi.getMyActiveSupportTicket(userName.value)
    if (res && res.ticket) {
      activeTicket.value = res.ticket
      messages.value = res.messages || []
      await nextTick()
      scrollToBottom()
    } else {
      activeTicket.value = null
      messages.value = []
    }
  } catch (err) {
    console.error('Check active support ticket error:', err)
  }
}

async function submitTicket() {
  if (!initialMessage.value.trim()) return
  isSubmitting.value = true
  submitSuccessMsg.value = ''
  submitErrorMsg.value = ''
  try {
    await authApi.createSupportTicket(
      userName.value,
      props.role || 'Passenger',
      topic.value,
      initialMessage.value.trim(),
      props.user?.id || null
    )
    initialMessage.value = ''
    submitSuccessMsg.value = 'Support request created successfully! Entering queue...'
    await checkActiveTicket()
  } catch (err) {
    submitErrorMsg.value = err.message || 'Failed to submit support ticket.'
  } finally {
    isSubmitting.value = false
  }
}

async function sendReply() {
  if (!chatReplyText.value.trim() || !activeTicket.value) return
  const text = chatReplyText.value.trim()
  chatReplyText.value = ''
  try {
    await authApi.sendSupportMessage(activeTicket.value.id, 'user', userName.value, text)
    await checkActiveTicket()
  } catch (err) {
    console.error('Send reply error:', err)
  }
}

function scrollToBottom() {
  if (messagesBox.value) {
    messagesBox.value.scrollTop = messagesBox.value.scrollHeight
  }
}

function startPolling() {
  stopPolling()
  pollInterval = setInterval(checkActiveTicket, 3000)
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

onMounted(() => {
  checkActiveTicket()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.floating-support-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 999;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #fff;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
  cursor: pointer;
  transition: all 0.25s ease;
}

.floating-support-btn:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6);
}

.support-btn-icon {
  font-size: 1.15rem;
}

.support-status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #f59e0b;
}

.support-status-dot.active {
  background: #10b981;
}

.support-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.support-modal-card {
  width: 100%;
  max-width: 520px;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 85vh;
}

.support-modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  font-size: 1.5rem;
}

.title-text {
  font-size: 1.1rem;
  font-weight: 800;
  color: #fff;
  margin: 0;
}

.subtitle-text {
  font-size: 0.78rem;
  color: #94a3b8;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.header-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
  color: #cbd5e1;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.18);
  color: #fff;
}

.minimize-btn:hover {
  background: rgba(56, 189, 248, 0.25);
  color: #38bdf8;
  border-color: rgba(56, 189, 248, 0.4);
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.25);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.4);
}

.support-modal-body {
  padding: 1.25rem 1.5rem;
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 700;
  color: #cbd5e1;
  margin-bottom: 0.4rem;
}

.form-select, .form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: #fff;
  font-size: 0.88rem;
  box-sizing: border-box;
}

.btn-submit-support {
  width: 100%;
  padding: 0.85rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #fff;
  font-weight: 800;
  font-size: 0.95rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.status-banner {
  padding: 0.85rem 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
}

.status-banner.waiting {
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #fbbf24;
}

.status-banner.active {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #34d399;
}

.banner-title {
  font-weight: 800;
}

.banner-sub {
  font-size: 0.75rem;
  opacity: 0.85;
}

.chat-messages-container {
  flex: 1;
  min-height: 250px;
  max-height: 380px;
  overflow-y: auto;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 14px;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.chat-bubble-wrap {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.chat-bubble-wrap.outgoing {
  align-self: flex-end;
}

.chat-bubble-wrap.incoming {
  align-self: flex-start;
}

.sender-info {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-bottom: 0.2rem;
}

.outgoing .sender-info {
  text-align: right;
}

.chat-bubble {
  padding: 0.75rem 1rem;
  font-size: 0.88rem;
  line-height: 1.4;
  color: #fff;
}

.outgoing .chat-bubble {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 16px 16px 2px 16px;
}

.incoming .chat-bubble {
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px 16px 16px 2px;
}

.chat-input-area {
  display: flex;
  gap: 0.6rem;
}

.chat-reply-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  color: #fff;
  font-size: 0.88rem;
}

.btn-send-chat {
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #fff;
  font-weight: 700;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.alert-box {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.alert-box.success {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.alert-box.error {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
