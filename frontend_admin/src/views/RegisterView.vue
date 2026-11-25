<template>
  <div class="auth-page">
    <div class="auth-card glass" style="padding: 2.5rem; max-width: 600px;">
      <!-- Header -->
      <div class="auth-header">
        <div class="header-nav-row">
          <button class="btn-back-arrow" @click="router.push('/dashboard')">←</button>
          <h1 class="auth-title">Register Account</h1>
        </div>
        <p class="auth-subtitle">Create a new administrator or employee account with position-based role</p>
      </div>

      <!-- Registration Type Toggle -->
      <div class="type-toggle-bar">
        <button 
          type="button" 
          :class="['toggle-tab', accountType === 'admin' ? 'active' : '']" 
          @click="accountType = 'admin'"
        >
          🛡️ Admin Level
        </button>
        <button 
          type="button" 
          :class="['toggle-tab', accountType === 'employee' ? 'active' : '']" 
          @click="accountType = 'employee'"
        >
          👤 Employee (Role by Position)
        </button>
      </div>

      <!-- Messages -->
      <Transition name="fade">
        <div v-if="error" class="alert alert-error" role="alert">
          <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
          <div style="flex: 1;">{{ error }}</div>
        </div>
      </Transition>
      <Transition name="fade">
        <div v-if="success" class="alert alert-success" role="alert">
          Successfully registered {{ accountType === 'employee' ? 'employee' : 'admin' }} account! Redirecting...
        </div>
      </Transition>

      <form @submit.prevent="handleSubmit" novalidate>
        <!-- ADMIN FORM FIELDS -->
        <template v-if="accountType === 'admin'">
          <div class="form-group">
            <label class="form-label" for="fullname">Full Name</label>
            <input
              id="fullname"
              v-model="adminForm.full_name"
              type="text"
              class="form-input"
              placeholder="e.g. Jane Dela Cruz"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="username">Username</label>
            <input
              id="username"
              v-model="adminForm.username"
              type="text"
              class="form-input"
              placeholder="e.g. janedc"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="email">Email</label>
            <input
              id="email"
              v-model="adminForm.email"
              type="email"
              class="form-input"
              placeholder="e.g. jane@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="role">Admin Level</label>
            <select id="role" v-model="adminForm.role" class="form-input select-input">
              <option value="admin">Admin</option>
              <option value="super_admin">Super Admin</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="password">Password</label>
            <div class="input-wrap">
              <input
                id="password"
                v-model="adminForm.password"
                :type="showAdminPwd ? 'text' : 'password'"
                class="form-input"
                placeholder="Minimum 8 characters"
                required
              />
              <button type="button" class="eye-btn" @click="showAdminPwd = !showAdminPwd" title="Toggle password visibility">
                <svg v-if="!showAdminPwd" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
              </button>
            </div>
          </div>

          <div class="form-group" style="margin-bottom: 1.5rem;">
            <label class="form-label" for="confirm">Confirm Password</label>
            <div class="input-wrap">
              <input
                id="confirm"
                v-model="adminForm.confirm_password"
                :type="showAdminConfirmPwd ? 'text' : 'password'"
                class="form-input"
                placeholder="Repeat password"
                required
              />
              <button type="button" class="eye-btn" @click="showAdminConfirmPwd = !showAdminConfirmPwd" title="Toggle password visibility">
                <svg v-if="!showAdminConfirmPwd" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
              </button>
            </div>
          </div>
        </template>

        <!-- EMPLOYEE FORM FIELDS -->
        <template v-else>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">First Name *</label>
              <input type="text" v-model="empForm.first_name" required class="form-input" placeholder="e.g. John" />
            </div>

            <div class="form-group">
              <label class="form-label">Middle Name</label>
              <input type="text" v-model="empForm.middle_name" class="form-input" placeholder="Optional" />
            </div>

            <div class="form-group">
              <label class="form-label">Last Name *</label>
              <input type="text" v-model="empForm.last_name" required class="form-input" placeholder="e.g. Doe" />
            </div>

            <div class="form-group">
              <label class="form-label">Username *</label>
              <input type="text" v-model="empForm.username" required class="form-input" placeholder="Enter username" autocomplete="off" />
            </div>

            <div class="form-group">
              <label class="form-label">Email *</label>
              <input type="email" v-model="empForm.email" required class="form-input" placeholder="e.g. john.doe@example.com" />
            </div>

            <div class="form-group">
              <label class="form-label">Age *</label>
              <input type="number" v-model.number="empForm.age" required min="18" class="form-input" placeholder="e.g. 30" />
            </div>

            <div class="form-group">
              <label class="form-label">Sex *</label>
              <select v-model="empForm.sex" required class="form-select select-input">
                <option value="" disabled>Select Sex</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Department *</label>
              <select v-model="empForm.department" required class="form-select select-input">
                <option value="" disabled>Select Department</option>
                <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Position *</label>
              <select v-model="empForm.position" required :disabled="!empForm.department" class="form-select select-input">
                <option value="" disabled>
                  {{ empForm.department ? 'Select Position' : 'Select Dept First' }}
                </option>
                <option v-for="pos in availablePositions" :key="pos" :value="pos">
                  {{ pos }}
                </option>
              </select>
            </div>

            <!-- Position-Based Role Preview Badge -->
            <div class="form-group full-width" v-if="empForm.position">
              <div class="role-preview-box">
                <span class="role-preview-label">Registered System Role:</span>
                <span class="role-preview-badge">{{ computedRoleSlug }}</span>
              </div>
            </div>

            <div class="form-group full-width">
              <label class="form-label">Address *</label>
              <input type="text" v-model="empForm.address" required class="form-input" placeholder="e.g. 123 Main St, Manila" />
            </div>

            <div class="form-group full-width">
              <label class="form-label">Location / Office *</label>
              <input type="text" v-model="empForm.location" required class="form-input" placeholder="e.g. Main Branch" />
            </div>

            <div class="form-group">
              <label class="form-label">Password *</label>
              <div class="input-wrap">
                <input :type="showEmpPwd ? 'text' : 'password'" v-model="empForm.password" required class="form-input" placeholder="Enter password" autocomplete="new-password" />
                <button type="button" class="eye-btn" @click="showEmpPwd = !showEmpPwd" title="Toggle password visibility">
                  <svg v-if="!showEmpPwd" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Confirm Password *</label>
              <div class="input-wrap">
                <input :type="showEmpConfirmPwd ? 'text' : 'password'" v-model="empForm.confirm_password" required class="form-input" placeholder="Confirm password" autocomplete="new-password" />
                <button type="button" class="eye-btn" @click="showEmpConfirmPwd = !showEmpConfirmPwd" title="Toggle password visibility">
                  <svg v-if="!showEmpConfirmPwd" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
                </button>
              </div>
            </div>
          </div>
        </template>

        <button type="submit" class="btn btn-success" :disabled="loading" style="margin-top: 1rem;">
          <span v-if="loading" class="spinner spinner-sm"></span>
          <span>Register {{ accountType === 'employee' ? 'Employee Account' : 'Admin' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authApi } from '../api/auth'

const router = useRouter()
const auth   = useAuthStore()

const accountType = ref('admin') // 'admin' | 'employee'

const showAdminPwd = ref(false)
const showAdminConfirmPwd = ref(false)
const showEmpPwd = ref(false)
const showEmpConfirmPwd = ref(false)

const adminForm = ref({
  full_name: '',
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  role: 'admin'
})

const empForm = ref({
  username: '',
  password: '',
  confirm_password: '',
  first_name: '',
  middle_name: '',
  last_name: '',
  age: null,
  sex: '',
  email: '',
  address: '',
  department: '',
  position: '',
  location: ''
})

const defaultDepartments = ['IT', 'Accounting', 'HR', 'Staff']
const defaultDepartmentPositions = {
  IT: ['IT Admin', 'IT Team Leader', 'Senior Developer', 'Junior developer'],
  Accounting: ['Accounting Admin', 'Acct Team Leader', 'Accountant'],
  HR: ['HR Admin', 'HR Team Leader', 'HR Staff', 'CSR'],
  Staff: ['Staff Admin', 'Staff Team Leader', 'General Staff', 'Operations Staff', 'Support Staff']
}

const savedDeptRaw = localStorage.getItem('cael_departments')
const departments = ref(savedDeptRaw ? JSON.parse(savedDeptRaw) : defaultDepartments)

const savedDeptPosRaw = localStorage.getItem('cael_department_positions')
const departmentPositions = ref(savedDeptPosRaw ? JSON.parse(savedDeptPosRaw) : defaultDepartmentPositions)

const availablePositions = computed(() => {
  return departmentPositions.value[empForm.value.department] || []
})

const computedRoleSlug = computed(() => {
  if (!empForm.value.position) return ''
  return empForm.value.position.trim().toLowerCase().replace(/\s+/g, '_')
})

watch(() => empForm.value.department, () => {
  empForm.value.position = ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

async function handleSubmit() {
  error.value = ''
  
  if (accountType.value === 'admin') {
    if (!adminForm.value.full_name || !adminForm.value.username || !adminForm.value.email || !adminForm.value.password) {
      error.value = 'All admin fields are required.'
      return
    }
    if (adminForm.value.password.length < 8) {
      error.value = 'Password must be at least 8 characters long.'
      return
    }
    if (adminForm.value.password !== adminForm.value.confirm_password) {
      error.value = 'Passwords do not match.'
      return
    }

    loading.value = true
    try {
      await auth.registerAdmin(adminForm.value)
      success.value = true
      setTimeout(() => {
        router.push('/dashboard')
      }, 1500)
    } catch (err) {
      error.value = err.message || 'Admin registration failed.'
    } finally {
      loading.value = false
    }
  } else {
    // Employee registration
    if (!empForm.value.username ||
        !empForm.value.password ||
        !empForm.value.first_name || 
        !empForm.value.last_name || 
        !empForm.value.age || 
        !empForm.value.sex || 
        !empForm.value.email || 
        !empForm.value.address || 
        !empForm.value.department || 
        !empForm.value.position || 
        !empForm.value.location) {
      error.value = 'All employee fields except Middle Name are required.'
      return
    }
    if (empForm.value.age < 18) {
      error.value = 'Employee must be at least 18 years old.'
      return
    }
    if (empForm.value.password.length < 8) {
      error.value = 'Password must be at least 8 characters long.'
      return
    }
    if (empForm.value.password !== empForm.value.confirm_password) {
      error.value = 'Passwords do not match.'
      return
    }

    loading.value = true
    try {
      await authApi.addEmployee({
        username: empForm.value.username,
        password: empForm.value.password,
        first_name: empForm.value.first_name,
        middle_name: empForm.value.middle_name || null,
        last_name: empForm.value.last_name,
        age: parseInt(empForm.value.age),
        sex: empForm.value.sex,
        email: empForm.value.email,
        address: empForm.value.address,
        department: empForm.value.department,
        position: empForm.value.position,
        location: empForm.value.location
      })

      success.value = true
      setTimeout(() => {
        router.push('/dashboard')
      }, 1500)
    } catch (err) {
      error.value = err.message || 'Employee registration failed.'
    } finally {
      loading.value = false
    }
  }
}
</script>

<style scoped>
.header-nav-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.btn-back-arrow {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--border);
  color: var(--text-1);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.2s;
}
.btn-back-arrow:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-2px);
}

.type-toggle-bar {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.35rem;
  border-radius: 12px;
  border: 1px solid var(--border);
  margin-bottom: 1.5rem;
}

.toggle-tab {
  flex: 1;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--text-2);
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-tab.active {
  background: var(--primary);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.full-width {
  grid-column: 1 / -1;
}

.role-preview-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px dashed rgba(99, 102, 241, 0.4);
  padding: 0.6rem 1rem;
  border-radius: 8px;
}

.role-preview-label {
  font-size: 0.8rem;
  color: var(--text-2);
  font-weight: 600;
}

.role-preview-badge {
  font-family: monospace;
  font-weight: 700;
  font-size: 0.85rem;
  color: #a5b4fc;
  background: rgba(99, 102, 241, 0.25);
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  letter-spacing: 0.5px;
}

.select-input {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
  padding-right: 2.5rem;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrap .form-input {
  padding-right: 2.75rem;
  width: 100%;
}

.eye-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-3, #94a3b8);
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  transition: color 0.2s ease;
}

.eye-btn:hover {
  color: var(--text-1, #ffffff);
}

.eye-btn svg {
  width: 18px;
  height: 18px;
}
</style>
