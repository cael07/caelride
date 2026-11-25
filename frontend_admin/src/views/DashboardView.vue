<template>
  <div class="admin-dashboard-root" :class="{ 'sidebar-collapsed': !isSidebarOpen }" @click="handleGlobalClick">
    <!-- TOP NAVIGATION BAR -->
    <header class="top-navbar glass">
      <div class="navbar-left">
        <button 
          type="button" 
          class="hamburger-btn" 
          @click="isSidebarOpen = !isSidebarOpen"
          :title="isSidebarOpen ? 'Collapse Menu' : 'Expand Menu'"
        >
          <svg v-if="!isSidebarOpen" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>

        <div class="nav-brand" @click="activeView = 'dashboard'">
          <img src="/cael.ico" alt="CAEL Admin" class="brand-logo-img" />
          <div class="brand-text">
            <span class="brand-title">CAEL Enterprise</span>
            <span class="brand-subtitle">Admin Management Portal</span>
          </div>
        </div>
      </div>

      <div class="navbar-center">
        <div class="view-indicator-badge">
          <span class="view-icon">{{ currentViewMeta.icon }}</span>
          <span class="view-label">{{ currentViewMeta.title }}</span>
        </div>
      </div>

      <div class="navbar-right">
        <!-- USER PROFILE DROPDOWN WRAPPER -->
        <div class="user-dropdown-wrapper" ref="profileDropdownRef">
          <button 
            type="button" 
            class="user-profile-pill-btn" 
            @click.stop="isProfileDropdownOpen = !isProfileDropdownOpen"
            :class="{ 'active': isProfileDropdownOpen }"
          >
            <span class="user-avatar-badge">👤</span>
            <div class="user-meta-info">
              <span class="user-name-label">{{ user?.full_name || 'Super Administrator' }}</span>
              <span class="user-role-subtag">{{ (user?.role || 'SUPER_ADMIN').toUpperCase() }}</span>
            </div>
            <span class="dropdown-arrow-icon">{{ isProfileDropdownOpen ? '▲' : '▼' }}</span>
          </button>


          <!-- DROPDOWN MENU -->
          <Transition name="dropdown">
            <div v-if="isProfileDropdownOpen" class="profile-dropdown-menu glass" @click.stop>
              <div class="dropdown-header">
                <div class="dropdown-avatar">👤</div>
                <div class="dropdown-user-details">
                  <span class="dropdown-fullname">{{ user?.full_name || 'Super Administrator' }}</span>
                  <span class="dropdown-email">{{ user?.email || 'admin@cael.com' }}</span>
                  <span class="dropdown-role-badge">{{ user?.role || 'super_admin' }}</span>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <div class="dropdown-body">
                <button 
                  v-if="isRoleSetupAdmin"
                  type="button" 
                  class="dropdown-item" 
                  @click="openRoleSetupModal(); isProfileDropdownOpen = false"
                >
                  <span class="dropdown-item-icon">⚙️</span>
                  <div class="dropdown-item-text">
                    <span class="item-main">Role & Menu Access Setup</span>
                    <span class="item-sub">Configure role menu permissions</span>
                  </div>
                </button>

                <button 
                  type="button" 
                  class="dropdown-item" 
                  @click="navigateToProfile"
                >
                  <span class="dropdown-item-icon">👤</span>
                  <div class="dropdown-item-text">
                    <span class="item-main">View Full Profile</span>
                    <span class="item-sub">Account details & privileges</span>
                  </div>
                </button>


                <button 
                  type="button" 
                  class="dropdown-item" 
                  @click="activeView = 'dashboard'; isProfileDropdownOpen = false"
                >
                  <span class="dropdown-item-icon">📊</span>
                  <div class="dropdown-item-text">
                    <span class="item-main">Dashboard</span>
                    <span class="item-sub">Real-time metrics & analytics</span>
                  </div>
                </button>

              </div>

              <div class="dropdown-divider"></div>

              <div class="dropdown-footer">
                <button 
                  type="button" 
                  class="dropdown-item logout-item" 
                  @click="handleLogout"
                >
                  <span class="dropdown-item-icon">🚪</span>
                  <span class="item-main">Sign Out</span>
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </header>

    <div class="main-layout">
      <!-- SIDEBAR DRAWER MENU -->
      <aside class="sidebar-drawer glass" :class="{ 'collapsed': !isSidebarOpen }">
        <div class="sidebar-content">
          <nav class="sidebar-nav">
            <!-- STANDALONE DASHBOARD MENU ITEM -->
            <div class="nav-group standalone-group" v-if="canAccessMenu('dashboard')">

              <button 
                type="button" 
                :class="['nav-item', 'standalone-nav-item', activeView === 'dashboard' ? 'active' : '']"
                @click="activeView = 'dashboard'"
              >
                <span class="item-icon">📊</span>
                <span class="item-text">Dashboard</span>
              </button>
            </div>

            <!-- MENU GROUP 1: EMPLOYEE MANAGEMENT -->
            <div v-if="canAccessMenuGroup(['employee_list', 'add_employee'])" class="nav-group">

              <button 
                type="button" 
                class="nav-group-header"
                @click="isEmpSubmenuOpen = !isEmpSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">👔</span>
                  <span class="group-name">Employee</span>
                </div>
                <span class="chevron-icon">{{ isEmpSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isEmpSubmenuOpen" class="nav-sub-items">
                  <!-- 👥 Employee List -->
                  <button 
                    v-if="canAccessMenu('employee_list')"
                    type="button" 
                    :class="['nav-item', activeView === 'employee_list' ? 'active' : '']"
                    @click="activeView = 'employee_list'"
                  >
                    <span class="item-icon">👥</span>
                    <span class="item-text">Employee List</span>
                    <span class="item-badge" v-if="employeeUsers.length > 0">{{ employeeUsers.length }}</span>
                  </button>

                  <!-- 👤➕ Add Employee -->
                  <button 
                    v-if="canAccessMenu('add_employee')"
                    type="button" 
                    :class="['nav-item', activeView === 'add_employee' ? 'active' : '']"
                    @click="activeView = 'add_employee'"
                  >
                    <span class="item-icon">👤➕</span>
                    <span class="item-text">Add Employee</span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 2: CORE ACCOUNTS -->
            <div v-if="canAccessMenuGroup(['drivers', 'passengers', 'admins'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isCoreSubmenuOpen = !isCoreSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">👥</span>
                  <span class="group-name">Core Accounts</span>
                </div>
                <span class="chevron-icon">{{ isCoreSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isCoreSubmenuOpen" class="nav-sub-items">
                  <!-- 🏍️ Driver Accounts -->
                  <button 
                    v-if="canAccessMenu('drivers')"
                    type="button" 
                    :class="['nav-item', activeView === 'drivers' ? 'active' : '']"
                    @click="activeView = 'drivers'"
                  >
                    <span class="item-icon">🏍️</span>
                    <span class="item-text">Driver</span>
                    <span class="item-badge" v-if="driverUsers.length > 0">{{ driverUsers.length }}</span>
                  </button>

                  <!-- 👤 Passenger Accounts -->
                  <button 
                    v-if="canAccessMenu('passengers')"
                    type="button" 
                    :class="['nav-item', activeView === 'passengers' ? 'active' : '']"
                    @click="activeView = 'passengers'"
                  >
                    <span class="item-icon">👤</span>
                    <span class="item-text">Passenger</span>
                    <span class="item-badge" v-if="passengerUsers.length > 0">{{ passengerUsers.length }}</span>
                  </button>

                  <!-- 💻 Admin Accounts -->
                  <button 
                    v-if="canAccessMenu('admins')"
                    type="button" 
                    :class="['nav-item', activeView === 'admins' ? 'active' : '']"
                    @click="activeView = 'admins'"
                  >
                    <span class="item-icon">💻</span>
                    <span class="item-text">Admin</span>
                    <span class="item-badge" v-if="adminUsers.length > 0">{{ adminUsers.length }}</span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 3: OPERATIONS & AUDITS -->
            <div v-if="canAccessMenuGroup(['topups', 'bookings', 'doc_bookings', 'stats'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isOpsSubmenuOpen = !isOpsSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">📊</span>
                  <span class="group-name">Operations & Audits</span>
                </div>
                <span class="chevron-icon">{{ isOpsSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isOpsSubmenuOpen" class="nav-sub-items">
                  <button 
                    v-if="canAccessMenu('topups')"
                    type="button" 
                    :class="['nav-item', activeView === 'topups' ? 'active' : '']"
                    @click="activeView = 'topups'"
                  >
                    <span class="item-icon">💳</span>
                    <span class="item-text">Top-Up Verification</span>
                    <span class="item-badge alert-badge" v-if="pendingTopUpCount > 0">{{ pendingTopUpCount }}</span>
                  </button>

                  <button 
                    v-if="canAccessMenu('bookings')"
                    type="button" 
                    :class="['nav-item', activeView === 'bookings' ? 'active' : '']"
                    @click="activeView = 'bookings'"
                  >
                    <span class="item-icon">🚗</span>
                    <span class="item-text">Booking History</span>
                  </button>

                  <button 
                    v-if="canAccessMenu('doc_bookings')"
                    type="button" 
                    :class="['nav-item', activeView === 'doc_bookings' ? 'active' : '']"
                    @click="activeView = 'doc_bookings'"
                  >
                    <span class="item-icon">📄</span>
                    <span class="item-text">Document History</span>
                  </button>

                  <button 
                    v-if="canAccessMenu('stats')"
                    type="button" 
                    :class="['nav-item', activeView === 'stats' ? 'active' : '']"
                    @click="activeView = 'stats'"
                  >
                    <span class="item-icon">📈</span>
                    <span class="item-text">Financial Analytics</span>
                  </button>

                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 4: ACCOUNTING -->
            <div v-if="canAccessMenuGroup(['accounting'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isAccountingSubmenuOpen = !isAccountingSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">💼</span>
                  <span class="group-name">Accounting</span>
                </div>
                <span class="chevron-icon">{{ isAccountingSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isAccountingSubmenuOpen" class="nav-sub-items">
                  <!-- 💼 Financial Management System -->
                  <button 
                    v-if="canAccessMenu('accounting')"
                    type="button" 
                    :class="['nav-item', activeView === 'accounting' ? 'active' : '']"
                    @click="activeView = 'accounting'"
                  >
                    <span class="item-icon">💼</span>
                    <span class="item-text">Financial Management System</span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 5: ATTENDANCE -->
            <div v-if="canAccessMenuGroup(['attendance_timesheet', 'attendance_timelog', 'attendance_overtime', 'attendance_leave', 'attendance_holiday'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isAttendanceSubmenuOpen = !isAttendanceSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">⏰</span>
                  <span class="group-name">Attendance</span>
                </div>
                <span class="chevron-icon">{{ isAttendanceSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isAttendanceSubmenuOpen" class="nav-sub-items">
                  <!-- 📋 Time Sheet -->
                  <button 
                    v-if="canAccessMenu('attendance_timesheet')"
                    type="button" 
                    :class="['nav-item', activeView === 'attendance_timesheet' ? 'active' : '']"
                    @click="activeView = 'attendance_timesheet'"
                  >
                    <span class="item-icon">📋</span>
                    <span class="item-text">Time Sheet</span>
                  </button>

                  <!-- ⏱️ Time Log -->
                  <button 
                    v-if="canAccessMenu('attendance_timelog')"
                    type="button" 
                    :class="['nav-item', activeView === 'attendance_timelog' ? 'active' : '']"
                    @click="activeView = 'attendance_timelog'"
                  >
                    <span class="item-icon">⏱️</span>
                    <span class="item-text">Time Log</span>
                  </button>

                  <!-- ⏰ Overtime -->
                  <button 
                    v-if="canAccessMenu('attendance_overtime')"
                    type="button" 
                    :class="['nav-item', activeView === 'attendance_overtime' ? 'active' : '']"
                    @click="activeView = 'attendance_overtime'"
                  >
                    <span class="item-icon">⏰</span>
                    <span class="item-text">Overtime</span>
                  </button>

                  <!-- 🏖️ Leave -->
                  <button 
                    v-if="canAccessMenu('attendance_leave')"
                    type="button" 
                    :class="['nav-item', activeView === 'attendance_leave' ? 'active' : '']"
                    @click="activeView = 'attendance_leave'"
                  >
                    <span class="item-icon">🏖️</span>
                    <span class="item-text">Leave</span>
                  </button>

                  <!-- 📅 Calendar -->
                  <button 
                    v-if="canAccessMenu('attendance_holiday')"
                    type="button" 
                    :class="['nav-item', activeView === 'attendance_holiday' ? 'active' : '']"
                    @click="activeView = 'attendance_holiday'"
                  >
                    <span class="item-icon">📅</span>
                    <span class="item-text">Calendar</span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 6: PAYROLL -->
            <div v-if="canAccessMenuGroup(['payroll_schedule', 'payroll_salary', 'payroll_leave', 'payroll_generate', 'payroll_advances', 'payroll_contributions', 'payroll_bonus_deduction', 'payroll_ot_nd'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isPayrollSubmenuOpen = !isPayrollSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">💵</span>
                  <span class="group-name">Payroll</span>
                </div>
                <span class="chevron-icon">{{ isPayrollSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isPayrollSubmenuOpen" class="nav-sub-items">
                  <!-- 📅 Working Schedule -->
                  <button 
                    v-if="canAccessMenu('payroll_schedule')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_schedule' ? 'active' : '']"
                    @click="activeView = 'payroll_schedule'"
                  >
                    <span class="item-icon">📅</span>
                    <span class="item-text">Working Schedule</span>
                  </button>

                  <!-- 💰 Salary -->
                  <button 
                    v-if="canAccessMenu('payroll_salary')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_salary' ? 'active' : '']"
                    @click="activeView = 'payroll_salary'"
                  >
                    <span class="item-icon">💰</span>
                    <span class="item-text">Salary</span>
                  </button>

                  <!-- 🏖️ Leave -->
                  <button 
                    v-if="canAccessMenu('payroll_leave')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_leave' ? 'active' : '']"
                    @click="activeView = 'payroll_leave'"
                  >
                    <span class="item-icon">🏖️</span>
                    <span class="item-text">Leave</span>
                  </button>

                  <!-- ⚡ Generate Payroll -->
                  <button 
                    v-if="canAccessMenu('payroll_generate')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_generate' ? 'active' : '']"
                    @click="activeView = 'payroll_generate'"
                  >
                    <span class="item-icon">⚡</span>
                    <span class="item-text">Generate Payroll</span>
                  </button>

                  <!-- 💸 Advances -->
                  <button 
                    v-if="canAccessMenu('payroll_advances')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_advances' ? 'active' : '']"
                    @click="activeView = 'payroll_advances'"
                  >
                    <span class="item-icon">💸</span>
                    <span class="item-text">Advances</span>
                  </button>

                  <!-- 🏛️ Contributions -->
                  <button 
                    v-if="canAccessMenu('payroll_contributions')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_contributions' ? 'active' : '']"
                    @click="activeView = 'payroll_contributions'"
                  >
                    <span class="item-icon">🏛️</span>
                    <span class="item-text">Contributions</span>
                  </button>

                  <!-- 🎁 Bonus / Deduction -->
                  <button 
                    v-if="canAccessMenu('payroll_bonus_deduction')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_bonus_deduction' ? 'active' : '']"
                    @click="activeView = 'payroll_bonus_deduction'"
                  >
                    <span class="item-icon">🎁</span>
                    <span class="item-text">Bonus / Deduction</span>
                  </button>

                  <!-- 🌙 OT & ND Rates -->
                  <button 
                    v-if="canAccessMenu('payroll_ot_nd')"
                    type="button" 
                    :class="['nav-item', activeView === 'payroll_ot_nd' ? 'active' : '']"
                    @click="activeView = 'payroll_ot_nd'"
                  >
                    <span class="item-icon">🌙</span>
                    <span class="item-text">OT & ND Rates</span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 7: SUPPORT -->
            <div v-if="canAccessMenuGroup(['support_chat'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isSupportSubmenuOpen = !isSupportSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">🎧</span>
                  <span class="group-name">Support</span>
                </div>
                <span class="chevron-icon">{{ isSupportSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isSupportSubmenuOpen" class="nav-sub-items">
                  <!-- 💬 Chat Support -->
                  <button 
                    v-if="canAccessMenu('support_chat')"
                    type="button" 
                    :class="['nav-item', activeView === 'support_chat' ? 'active' : '']"
                    @click="activeView = 'support_chat'"
                  >
                    <span class="item-icon">💬</span>
                    <span class="item-text">Chat Support</span>
                    <span class="item-badge alert-badge" v-if="supportWaitingQueue.length > 0">{{ supportWaitingQueue.length }}</span>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- MENU GROUP 8: SETUP -->
            <div v-if="canAccessMenuGroup(['create_department', 'create_position', 'set_access'])" class="nav-group">
              <button 
                type="button" 
                class="nav-group-header"
                @click="isSetupSubmenuOpen = !isSetupSubmenuOpen"
              >
                <div class="group-title">
                  <span class="group-icon">⚙️</span>
                  <span class="group-name">Setup</span>
                </div>
                <span class="chevron-icon">{{ isSetupSubmenuOpen ? '▼' : '►' }}</span>
              </button>

              <Transition name="expand">
                <div v-show="isSetupSubmenuOpen" class="nav-sub-items">
                  <!-- 🏢 Create Department -->
                  <button 
                    v-if="canAccessMenu('create_department')"
                    type="button" 
                    :class="['nav-item', activeView === 'create_department' ? 'active' : '']"
                    @click="activeView = 'create_department'"
                  >
                    <span class="item-icon">🏢</span>
                    <span class="item-text">Create Department</span>
                  </button>

                  <!-- 📌 Create Position -->
                  <button 
                    v-if="canAccessMenu('create_position')"
                    type="button" 
                    :class="['nav-item', activeView === 'create_position' ? 'active' : '']"
                    @click="activeView = 'create_position'"
                  >
                    <span class="item-icon">📌</span>
                    <span class="item-text">Create Position</span>
                  </button>

                  <!-- 🔐 Set Access -->
                  <button 
                    v-if="canAccessMenu('set_access')"
                    type="button" 
                    :class="['nav-item', activeView === 'set_access' ? 'active' : '']"
                    @click="openRoleSetupModal(); activeView = 'set_access'"
                  >
                    <span class="item-icon">🔐</span>
                    <span class="item-text">Set Access</span>
                  </button>
                </div>
              </Transition>
            </div>

          </nav>
        </div>
      </aside>

      <!-- MAIN FULL-PAGE VIEW CONTAINER -->
      <main class="content-container">
        <!-- GLOBAL ALERTS -->
        <Transition name="fade">
          <div v-if="successMsg" class="alert alert-success mt-2" role="alert">
            {{ successMsg }}
          </div>
        </Transition>
        <Transition name="fade">
          <div v-if="error" class="alert alert-error mt-2" role="alert">
            {{ error }}
          </div>
        </Transition>

        <!-- VIEW 0: DASHBOARD VIEW -->
        <div v-if="activeView === 'dashboard'" class="page-view glass dashboard-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">📊 Dashboard</h2>
            </div>
            
            <button type="button" class="refresh-blue-icon-btn" @click="refreshDashboardData" title="Refresh Analytics">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
              </svg>
            </button>
          </div>


          <!-- INLINE 4 CARDS WITH COUNTING ANIMATION -->
          <div class="dashboard-inline-cards-grid">
            
            <!-- CARD 1: TOTAL INCOME FEE -->
            <div class="dash-stat-card glass card-income-fee">
              <div class="card-top-row">
                <div class="card-icon-badge icon-income-fee">💰</div>
                <span class="card-trend-tag positive">+12.5%</span>
              </div>
              <div class="card-content-body">
                <span class="card-metric-title">Total Income Fee</span>
                <h3 class="card-metric-value">₱{{ formatAnimatedCurrency(animatedIncomeFee) }}</h3>
                <span class="card-metric-sub">Platform fees & ride commissions</span>
              </div>
            </div>

            <!-- CARD 2: TOTAL LOAD INCOME -->
            <div class="dash-stat-card glass card-load-income">
              <div class="card-top-row">
                <div class="card-icon-badge icon-load-income">💳</div>
                <span class="card-trend-tag positive">+8.4%</span>
              </div>
              <div class="card-content-body">
                <span class="card-metric-title">Total Load Income</span>
                <h3 class="card-metric-value">₱{{ formatAnimatedCurrency(animatedLoadIncome) }}</h3>
                <span class="card-metric-sub">Approved GCash, Maya & Cash top-ups</span>
              </div>
            </div>

            <!-- CARD 3: TOTAL EXPENSE -->
            <div class="dash-stat-card glass card-expense">
              <div class="card-top-row">
                <div class="card-icon-badge icon-expense">💸</div>
                <span class="card-trend-tag neutral">Prepared</span>
              </div>
              <div class="card-content-body">
                <span class="card-metric-title">Total Expense</span>
                <h3 class="card-metric-value">₱{{ formatAnimatedCurrency(animatedExpense) }}</h3>
                <span class="card-metric-sub">Operational expenses (0 for future integration)</span>
              </div>
            </div>

            <!-- CARD 4: TOTAL COMPLETED RIDES -->
            <div class="dash-stat-card glass card-completed-rides">
              <div class="card-top-row">
                <div class="card-icon-badge icon-completed-rides">🏁</div>
                <span class="card-trend-tag badge-count">{{ Math.floor(animatedCompletedRides) }} Rides</span>
              </div>
              <div class="card-content-body">
                <span class="card-metric-title">Total Completed Rides</span>
                <h3 class="card-metric-value">{{ Math.floor(animatedCompletedRides) }}</h3>
                <span class="card-metric-sub">Completed delivery & passenger bookings</span>
              </div>
            </div>

          </div>

          <!-- Statistics & Balance Audit Section (From Backup) -->
          <div class="stats-audit-grid">
            <!-- SVG Point Graph Card -->
            <div class="stats-card glass">
              <h3 class="card-sec-title">📈 System Balance Timeline</h3>
              <div class="chart-container-wrap">
                <div class="chart-container" style="position: relative;">
                  <svg :viewBox="`0 0 ${chartWidth} ${chartHeight}`" class="balance-svg-chart">
                    <!-- Grid Lines -->
                    <line :x1="chartPadding" :y1="chartPadding" :x2="chartWidth - chartPadding" :y2="chartPadding" class="chart-gridline" />
                    <line :x1="chartPadding" :y1="chartHeight - chartPadding" :x2="chartWidth - chartPadding" :y2="chartHeight - chartPadding" class="chart-gridline" />
                    
                    <!-- Y-Axis Labels & Gridlines -->
                    <g class="chart-y-axis" v-if="loadChartPoints.length > 0">
                      <!-- Max Tick -->
                      <text :x="chartPadding - 8" :y="chartPadding + 3" text-anchor="end" class="chart-axis-label">₱{{ chartMaxVal.toFixed(0) }}</text>
                      
                      <!-- Mid Tick Gridline & Label -->
                      <line :x1="chartPadding" :y1="chartHeight / 2" :x2="chartWidth - chartPadding" :y2="chartHeight / 2" class="chart-gridline" />
                      <text :x="chartPadding - 8" :y="chartHeight / 2 + 3" text-anchor="end" class="chart-axis-label">₱{{ ((chartMaxVal + chartMinVal) / 2).toFixed(0) }}</text>
                      
                      <!-- Min Tick -->
                      <text :x="chartPadding - 8" :y="chartHeight - chartPadding + 3" text-anchor="end" class="chart-axis-label">₱{{ chartMinVal.toFixed(0) }}</text>
                    </g>

                    <!-- Chart Lines -->
                    <path v-if="loadChartPath" :d="loadChartPath" class="chart-line load-line" />
                    <path v-if="feeChartPath" :d="feeChartPath" class="chart-line fee-line" />
                    
                    <!-- Chart Points (Load) -->
                    <circle 
                      v-for="(p, idx) in loadChartPoints" 
                      :key="'load-' + idx"
                      :cx="p.x"
                      :cy="p.y"
                      r="4.5"
                      class="chart-point load-point"
                      @mouseenter="hoveredPoint = p"
                      @mouseleave="hoveredPoint = null"
                    />

                    <!-- Chart Points (Fee) -->
                    <circle 
                      v-for="(p, idx) in feeChartPoints" 
                      :key="'fee-' + idx"
                      :cx="p.x"
                      :cy="p.y"
                      r="4.5"
                      class="chart-point fee-point"
                      @mouseenter="hoveredPoint = p"
                      @mouseleave="hoveredPoint = null"
                    />
                  </svg>
                  <!-- Glowing Neon Tooltip -->
                  <Transition name="fade">
                    <div 
                      v-if="hoveredPoint" 
                      class="chart-tooltip" 
                      :class="hoveredPoint.type"
                      :style="{ 
                        left: ((hoveredPoint.x / chartWidth) * 100) + '%', 
                        top: ((hoveredPoint.y / chartHeight) * 100) + '%',
                        borderColor: hoveredPoint.type === 'load' ? 'var(--success)' : 'var(--primary-light)',
                        boxShadow: hoveredPoint.type === 'load' ? '0 8px 24px rgba(0, 0, 0, 0.5), 0 0 15px var(--success-glow)' : '0 8px 24px rgba(0, 0, 0, 0.5), 0 0 15px var(--primary-glow)'
                      }"
                    >
                      <div class="tooltip-arrow" :style="{ borderRight: hoveredPoint.type === 'load' ? '1px solid var(--success)' : '1px solid var(--primary-light)', borderBottom: hoveredPoint.type === 'load' ? '1px solid var(--success)' : '1px solid var(--primary-light)' }"></div>
                      <span class="tooltip-badge" :style="{ fontSize: '0.62rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: hoveredPoint.type === 'load' ? 'var(--success)' : 'var(--primary-light)', fontWeight: '700', marginBottom: '0.15rem' }">
                        {{ hoveredPoint.type === 'load' ? 'Top up' : "System Income" }}
                      </span>
                      <span class="tooltip-total">₱{{ hoveredPoint.total.toFixed(2) }}</span>
                      <span class="tooltip-change" :style="{ fontSize: '0.68rem', color: hoveredPoint.change >= 0 ? 'var(--success)' : 'var(--error)', marginTop: '0.1rem', fontWeight: '500' }">
                        {{ hoveredPoint.change >= 0 ? '+' : '' }}₱{{ hoveredPoint.change.toFixed(2) }}
                      </span>
                      <span class="tooltip-date" style="margin-top: 0.15rem;">{{ formatDate(hoveredPoint.date) }}</span>
                    </div>
                  </Transition>
                </div>
                <!-- X-Axis Labels -->
                <div class="chart-labels">
                  <span v-if="loadChartPoints.length > 0">{{ formatDate(loadChartPoints[0].date) }}</span>
                  <span style="flex: 1;"></span>
                  <span v-if="loadChartPoints.length > 1">{{ formatDate(loadChartPoints[loadChartPoints.length - 1].date) }}</span>
                </div>
                <!-- Legend -->
                <div class="chart-legend" style="display: flex; gap: 1.5rem; justify-content: center; margin-top: 0.75rem; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 0.75rem;">
                  <div class="legend-item" style="display: flex; align-items: center; gap: 0.4rem;">
                    <span class="legend-dot" style="width: 8px; height: 8px; border-radius: 50%; background-color: var(--success); box-shadow: 0 0 6px var(--success);"></span>
                    <span style="color: var(--text-2); font-weight: 500;">Top up</span>
                  </div>
                  <div class="legend-item" style="display: flex; align-items: center; gap: 0.4rem;">
                    <span class="legend-dot" style="width: 8px; height: 8px; border-radius: 50%; background-color: var(--primary-light); box-shadow: 0 0 6px var(--primary-light);"></span>
                    <span style="color: var(--text-2); font-weight: 500;">System Income</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Transactions Feed Card -->
            <div class="audit-card glass">
              <div class="card-header-with-filters">
                <h3 class="card-sec-title">🕵️ Transactions</h3>
                
                <div class="log-filter-bar">
                  <!-- Type Checkboxes -->
                  <div class="filter-checkboxes">
                    <label class="filter-checkbox-label">
                      <input type="checkbox" v-model="showLoadFilter" class="filter-checkbox checkbox-load">
                      <span class="checkbox-custom load"></span>
                      <span class="filter-text">Top up</span>
                      <span class="filter-count-badge" style="font-size: 0.72rem; opacity: 0.8; background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 2px 6px; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.25); font-weight: 700; margin-left: 4px;">{{ loadCount }}</span>
                    </label>
                    <label class="filter-checkbox-label">
                      <input type="checkbox" v-model="showFeeFilter" class="filter-checkbox checkbox-fee">
                      <span class="checkbox-custom fee"></span>
                      <span class="filter-text">System Income</span>
                      <span class="filter-count-badge" style="font-size: 0.72rem; opacity: 0.8; background: rgba(59, 130, 246, 0.15); color: #3b82f6; padding: 2px 6px; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.25); font-weight: 700; margin-left: 4px;">{{ feeCount }}</span>
                    </label>
                  </div>
                  
                  <!-- Date Selector -->
                  <div class="filter-date-group">
                    <span class="filter-date-icon">📅</span>
                    <input 
                      type="date" 
                      v-model="selectedLogDate" 
                      class="filter-date-input"
                      title="Filter by specific date"
                    />
                    <button 
                      v-if="selectedLogDate" 
                      class="btn-clear-date" 
                      @click="selectedLogDate = ''" 
                      title="Clear date filter"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>
              
              <div class="audit-logs-feed">
                <div v-if="filteredBalanceLogs.length === 0" class="empty-audit-state">
                  <span>📋</span>
                  <p>No matching balance log history found.</p>
                </div>
                <div 
                  v-else 
                  v-for="log in filteredBalanceLogs" 
                  :key="log.id" 
                  class="audit-log-row glass"
                  :class="log.type"
                >
                  <!-- Line 1: Target Name (Left) | Amount (Right: Blue for +, Red for -, White for 0) -->
                  <div class="audit-row-top" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                    <span class="audit-target-name" style="font-weight: 600; font-size: 0.88rem; color: #ffffff;">
                      @{{ log.username }}
                    </span>
                    <span 
                      class="audit-amount" 
                      :style="{
                        fontWeight: '700',
                        fontSize: '0.88rem',
                        fontFamily: 'monospace',
                        color: log.amount > 0 ? '#3b82f6' : (log.amount < 0 ? '#ef4444' : '#ffffff')
                      }"
                    >
                      {{ log.amount > 0 ? '+' : (log.amount < 0 ? '-' : '') }}₱{{ Math.abs(log.amount).toFixed(2) }}
                    </span>
                  </div>

                  <!-- Line 2: Created By (Left - Blue) | Date and Time (Right) -->
                  <div class="audit-row-mid" style="display: flex; justify-content: space-between; align-items: center; width: 100%; font-size: 0.78rem;">
                    <span class="audit-created-by" style="color: #3b82f6; font-weight: 600;">
                      @{{ log.created_by }}
                    </span>
                    <span class="audit-datetime" style="color: #94a3b8; font-weight: 500;">
                      {{ formatDate(log.created_at) }} {{ formatTime(log.created_at) }}
                    </span>
                  </div>

                  <!-- Line 3: Ref Number (Same as current color: Amber/Gold) -->
                  <div v-if="log.reference_number" class="audit-row-bot" style="display: flex; align-items: center; width: 100%;">
                    <span class="audit-ref-no" style="font-size: 0.72rem; color: #f59e0b; font-weight: 600;">
                      Ref: {{ log.reference_number }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW: FULL PAGE USER PROFILE DETAILS -->

        <div v-if="activeView === 'user_profile'" class="page-view glass profile-page-view">

          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">👤 Full Page Account Profile</h2>
              <p class="view-subheading">Comprehensive details for current administrator session</p>
            </div>
            
            <button class="btn btn-ghost btn-sm" @click="activeView = 'dashboard'">
              ← Back to Dashboard
            </button>
          </div>

          <div class="profile-card-grid">
            <div class="profile-main-card glass">
              <div class="profile-avatar-large">👤</div>
              <div class="profile-identity">
                <h3 class="profile-name">{{ user?.full_name || 'Super Administrator' }}</h3>
                <span class="profile-username">@{{ user?.username || 'admin' }}</span>
                <span class="profile-role-badge">{{ (user?.role || 'super_admin').toUpperCase() }}</span>
              </div>
            </div>

            <div class="profile-details-card glass">
              <h4 class="card-section-title">Account Information</h4>
              <div class="info-list">
                <div class="info-row">
                  <span class="info-label">Full Name</span>
                  <span class="info-val">{{ user?.full_name || 'N/A' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Username</span>
                  <span class="info-val font-mono">@{{ user?.username || 'N/A' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Email Address</span>
                  <span class="info-val">{{ user?.email || 'N/A' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Account Role</span>
                  <span class="info-val role-badge">{{ user?.role || 'super_admin' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Account Status</span>
                  <span class="info-val status-badge active">Active</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Activation Verification</span>
                  <span class="info-val status-badge active">Verified</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Current Balance</span>
                  <span class="info-val balance-text">₱{{ (user?.balance || 0).toFixed(2) }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">Date Registered</span>
                  <span class="info-val">{{ formatDate(user?.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW 1: REGISTERED EMPLOYEES (FULL PAGE) -->
        <div v-else-if="activeView === 'employee_list'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">👥 Registered Employees</h2>
              <span class="count-pill">{{ filteredEmployees.length }} Employees</span>
            </div>
            
            <div class="view-actions">
              <div class="search-input-box glass">
                <span class="search-icon">🔍</span>
                <input 
                  type="text" 
                  v-model="employeeSearch" 
                  placeholder="Search employees..." 
                  class="search-input"
                />
                <button v-if="employeeSearch" class="clear-search-btn" @click="employeeSearch = ''">✕</button>
              </div>

              <button class="btn btn-primary btn-sm inline-btn" @click="activeView = 'add_employee'">
                👤➕ Add Employee
              </button>
              <button class="btn btn-ghost btn-sm inline-btn" @click="fetchUsers" :disabled="loading">
                🔄 Refresh
              </button>
            </div>
          </div>

          <!-- Table Container -->
          <div class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th @click="toggleSort('full_name')" class="sortable-th">
                    Name / Email <span class="sort-icon">{{ getSortIcon('full_name') }}</span>
                  </th>
                  <th @click="toggleSort('username')" class="sortable-th">
                    Username <span class="sort-icon">{{ getSortIcon('username') }}</span>
                  </th>
                  <th @click="toggleSort('department')" class="sortable-th">
                    Department <span class="sort-icon">{{ getSortIcon('department') }}</span>
                  </th>
                  <th @click="toggleSort('position')" class="sortable-th">
                    Position / Role <span class="sort-icon">{{ getSortIcon('position') }}</span>
                  </th>
                  <th @click="toggleSort('location')" class="sortable-th">
                    Location <span class="sort-icon">{{ getSortIcon('location') }}</span>
                  </th>
                  <th @click="toggleSort('is_active')" class="sortable-th">
                    Status <span class="sort-icon">{{ getSortIcon('is_active') }}</span>
                  </th>
                  <th @click="toggleSort('created_at')" class="sortable-th">
                    Registered Date <span class="sort-icon">{{ getSortIcon('created_at') }}</span>
                  </th>
                  <th style="text-align: right;">Action</th>
                </tr>
              </thead>
              <TransitionGroup tag="tbody" name="list">
                <tr v-for="u in displayedEmployees" :key="u.id" class="user-row">
                  <td data-label="Name / Email">
                    <div class="name-col">
                      <span class="u-name">{{ u.full_name }}</span>
                      <span class="u-email">{{ u.email }}</span>
                    </div>
                  </td>
                  <td data-label="Username"><span class="u-username">@{{ u.username }}</span></td>
                  <td data-label="Department">
                    <span class="dept-badge">{{ u.department || 'IT' }}</span>
                  </td>
                  <td data-label="Position / Role">
                    <div class="pos-col">
                      <span class="pos-title">{{ u.position || u.role }}</span>
                      <span :class="['role-badge', u.role]">{{ u.role }}</span>
                    </div>
                  </td>
                  <td data-label="Location">
                    <span class="loc-text">{{ u.location || 'Main Office' }}</span>
                  </td>
                  <td data-label="Status">
                    <span :class="['status-badge', u.is_active ? 'active' : 'disabled']">
                      {{ u.is_active ? 'Active' : 'Disabled' }}
                    </span>
                  </td>
                  <td data-label="Registered Date">
                    <span class="date-text">{{ formatDate(u.created_at) }}</span>
                  </td>
                  <td data-label="Action">
                    <div class="action-btn-group">
                      <button 
                        :disabled="isTogglingActive === u.id || u.role === 'super_admin'"
                        :class="['btn', 'btn-sm', u.is_active ? 'btn-disable' : 'btn-enable']"
                        @click="handleToggleActive(u)"
                      >
                        {{ u.is_active ? 'Disable' : 'Enable' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </TransitionGroup>
            </table>
          </div>
        </div>

        <!-- VIEW 2: ADD EMPLOYEE (FULL PAGE FORM) -->
        <div v-else-if="activeView === 'add_employee'" class="page-view glass full-form-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">👤➕ Register New Employee</h2>
              <p class="view-subheading">Create employee user account with position-based role assignment</p>
            </div>
            
            <button class="btn btn-ghost btn-sm" @click="activeView = 'employee_list'">
              ← Back to Employee List
            </button>
          </div>

          <form @submit.prevent="submitEmployeeForm" class="employee-full-form" autocomplete="off">
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Username *</label>
                <input type="text" v-model="employeeForm.username" required class="form-input" placeholder="Enter username" autocomplete="off" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Password *</label>
                <div class="input-wrap">
                  <input :type="showEmployeePassword ? 'text' : 'password'" v-model="employeeForm.password" required class="form-input" placeholder="Enter password" autocomplete="new-password" />
                  <button type="button" class="eye-btn" @click="showEmployeePassword = !showEmployeePassword" title="Toggle password visibility">
                    <svg v-if="!showEmployeePassword" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                    <svg v-else viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
                  </button>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">First Name *</label>
                <input type="text" v-model="employeeForm.first_name" required class="form-input" placeholder="e.g. John" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Middle Name</label>
                <input type="text" v-model="employeeForm.middle_name" class="form-input" placeholder="Optional" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Last Name *</label>
                <input type="text" v-model="employeeForm.last_name" required class="form-input" placeholder="e.g. Doe" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Age *</label>
                <input type="number" v-model.number="employeeForm.age" required min="18" class="form-input" placeholder="e.g. 30" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Sex *</label>
                <div class="select-wrapper">
                  <select v-model="employeeForm.sex" required class="form-select select-input">
                    <option value="" disabled selected>Select Sex</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">Email *</label>
                <input type="email" v-model="employeeForm.email" required class="form-input" placeholder="e.g. john.doe@example.com" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Department *</label>
                <div class="select-wrapper">
                  <select v-model="employeeForm.department" required class="form-select select-input">
                    <option value="" disabled selected>Select Department</option>
                    <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
                  </select>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">Position *</label>
                <div class="select-wrapper">
                  <select v-model="employeeForm.position" required :disabled="!employeeForm.department" class="form-select select-input">
                    <option value="" disabled selected>
                      {{ employeeForm.department ? 'Select Position' : 'Select Department First' }}
                    </option>
                    <option v-for="pos in availablePositions" :key="pos" :value="pos">
                      {{ pos }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- Position-Based Role Preview Badge -->
              <div class="form-group full-width" v-if="employeeForm.position">
                <div class="role-preview-box">
                  <span class="role-preview-label">Registered System Role:</span>
                  <span class="role-preview-badge">{{ computedEmpRoleSlug }}</span>
                </div>
              </div>

              <div class="form-group full-width">
                <label class="form-label">Address *</label>
                <input type="text" v-model="employeeForm.address" required class="form-input" placeholder="e.g. 123 Main St, Manila" />
              </div>

              <div class="form-group full-width">
                <label class="form-label">Location / Office *</label>
                <input type="text" v-model="employeeForm.location" required class="form-input" placeholder="e.g. Branch / Office Room" />
              </div>
            </div>

            <!-- Feedback -->
            <div v-if="employeeSuccess" class="alert alert-success mt-2">{{ employeeSuccess }}</div>
            <div v-if="employeeError" class="alert alert-error mt-2">{{ employeeError }}</div>

            <div class="form-actions-row">
              <button type="submit" class="btn btn-success" :disabled="isAddingEmployee">
                <span v-if="isAddingEmployee" class="spinner spinner-sm"></span>
                <span>👤 Register Employee</span>
              </button>
            </div>
          </form>
        </div>

        <!-- VIEW 3: DRIVER ACCOUNTS (FULL PAGE) -->
        <div v-else-if="activeView === 'drivers'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🏍️ Driver Accounts</h2>
              <span class="count-pill">{{ filteredDrivers.length }} Drivers</span>
            </div>
            
            <div class="view-actions">
              <div class="search-input-box glass">
                <span class="search-icon">🔍</span>
                <input 
                  type="text" 
                  v-model="driverSearch" 
                  placeholder="Search drivers..." 
                  class="search-input"
                />
                <button v-if="driverSearch" class="clear-search-btn" @click="driverSearch = ''">✕</button>
              </div>

              <button class="btn btn-ghost btn-sm inline-btn" @click="fetchUsers" :disabled="loading">
                🔄 Refresh
              </button>
            </div>
          </div>

          <div class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th @click="toggleSort('full_name')" class="sortable-th">
                    Name / Email <span class="sort-icon">{{ getSortIcon('full_name') }}</span>
                  </th>
                  <th @click="toggleSort('username')" class="sortable-th">
                    Username <span class="sort-icon">{{ getSortIcon('username') }}</span>
                  </th>
                  <th @click="toggleSort('role')" class="sortable-th">
                    Role <span class="sort-icon">{{ getSortIcon('role') }}</span>
                  </th>
                  <th @click="toggleSort('is_activated')" class="sortable-th">
                    Activated <span class="sort-icon">{{ getSortIcon('is_activated') }}</span>
                  </th>
                  <th @click="toggleSort('is_active')" class="sortable-th">
                    Status <span class="sort-icon">{{ getSortIcon('is_active') }}</span>
                  </th>
                  <th @click="toggleSort('balance')" class="sortable-th">
                    Balance <span class="sort-icon">{{ getSortIcon('balance') }}</span>
                  </th>
                  <th @click="toggleSort('created_at')" class="sortable-th">
                    Registered Date <span class="sort-icon">{{ getSortIcon('created_at') }}</span>
                  </th>
                  <th style="text-align: right;">Action</th>
                </tr>
              </thead>
              <TransitionGroup tag="tbody" name="list">
                <tr v-for="u in displayedDrivers" :key="u.id" class="user-row">
                  <td data-label="Name / Email">
                    <div class="name-col">
                      <span class="u-name">{{ u.full_name }}</span>
                      <span class="u-email">{{ u.email }}</span>
                    </div>
                  </td>
                  <td data-label="Username"><span class="u-username">@{{ u.username }}</span></td>
                  <td data-label="Role"><span class="role-badge driver">DRIVER</span></td>
                  <td data-label="Activated">
                    <label class="switch-wrap">
                      <input type="checkbox" :checked="u.is_activated" @change="handleToggleActivated(u)" />
                      <span class="slider"></span>
                    </label>
                  </td>
                  <td data-label="Status">
                    <span :class="['status-badge', u.is_active ? 'active' : 'disabled']">
                      {{ u.is_active ? 'Active' : 'Disabled' }}
                    </span>
                  </td>
                  <td data-label="Balance">
                    <div class="balance-cell">
                      <span class="balance-amount">₱{{ (u.balance || 0).toFixed(2) }}</span>
                      <div class="balance-actions">
                        <button class="btn-circle btn-deduct" @click="promptDeduct(u)">−</button>
                        <button class="btn-circle btn-add" @click="promptAdd(u)">+</button>
                      </div>
                    </div>
                  </td>
                  <td data-label="Registered Date">
                    <span class="date-text">{{ formatDate(u.created_at) }}</span>
                  </td>
                  <td data-label="Action">
                    <button 
                      :class="['btn', 'btn-sm', u.is_active ? 'btn-disable' : 'btn-enable']"
                      @click="handleToggleActive(u)"
                    >
                      {{ u.is_active ? 'Disable' : 'Enable' }}
                    </button>
                  </td>
                </tr>
              </TransitionGroup>
            </table>
          </div>
        </div>

        <!-- VIEW 4: PASSENGER ACCOUNTS (FULL PAGE) -->
        <div v-else-if="activeView === 'passengers'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">👤 Passenger Accounts</h2>
              <span class="count-pill">{{ filteredPassengers.length }} Passengers</span>
            </div>
            
            <div class="view-actions">
              <div class="search-input-box glass">
                <span class="search-icon">🔍</span>
                <input 
                  type="text" 
                  v-model="passengerSearch" 
                  placeholder="Search passengers..." 
                  class="search-input"
                />
                <button v-if="passengerSearch" class="clear-search-btn" @click="passengerSearch = ''">✕</button>
              </div>

              <button class="btn btn-ghost btn-sm inline-btn" @click="fetchUsers" :disabled="loading">
                🔄 Refresh
              </button>
            </div>
          </div>

          <div class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th @click="toggleSort('full_name')" class="sortable-th">
                    Name / Email <span class="sort-icon">{{ getSortIcon('full_name') }}</span>
                  </th>
                  <th @click="toggleSort('username')" class="sortable-th">
                    Username <span class="sort-icon">{{ getSortIcon('username') }}</span>
                  </th>
                  <th @click="toggleSort('role')" class="sortable-th">
                    Role <span class="sort-icon">{{ getSortIcon('role') }}</span>
                  </th>
                  <th @click="toggleSort('is_activated')" class="sortable-th">
                    Activated <span class="sort-icon">{{ getSortIcon('is_activated') }}</span>
                  </th>
                  <th @click="toggleSort('is_active')" class="sortable-th">
                    Status <span class="sort-icon">{{ getSortIcon('is_active') }}</span>
                  </th>
                  <th @click="toggleSort('balance')" class="sortable-th">
                    Balance <span class="sort-icon">{{ getSortIcon('balance') }}</span>
                  </th>
                  <th @click="toggleSort('created_at')" class="sortable-th">
                    Registered Date <span class="sort-icon">{{ getSortIcon('created_at') }}</span>
                  </th>
                  <th style="text-align: right;">Action</th>
                </tr>
              </thead>
              <TransitionGroup tag="tbody" name="list">
                <tr v-for="u in displayedPassengers" :key="u.id" class="user-row">
                  <td data-label="Name / Email">
                    <div class="name-col">
                      <span class="u-name">{{ u.full_name }}</span>
                      <span class="u-email">{{ u.email }}</span>
                    </div>
                  </td>
                  <td data-label="Username"><span class="u-username">@{{ u.username }}</span></td>
                  <td data-label="Role"><span class="role-badge passenger">PASSENGER</span></td>
                  <td data-label="Activated">
                    <label class="switch-wrap">
                      <input type="checkbox" :checked="u.is_activated" @change="handleToggleActivated(u)" />
                      <span class="slider"></span>
                    </label>
                  </td>
                  <td data-label="Status">
                    <span :class="['status-badge', u.is_active ? 'active' : 'disabled']">
                      {{ u.is_active ? 'Active' : 'Disabled' }}
                    </span>
                  </td>
                  <td data-label="Balance">
                    <div class="balance-cell">
                      <span class="balance-amount">₱{{ (u.balance || 0).toFixed(2) }}</span>
                      <div class="balance-actions">
                        <button class="btn-circle btn-deduct" @click="promptDeduct(u)">−</button>
                        <button class="btn-circle btn-add" @click="promptAdd(u)">+</button>
                      </div>
                    </div>
                  </td>
                  <td data-label="Registered Date">
                    <span class="date-text">{{ formatDate(u.created_at) }}</span>
                  </td>
                  <td data-label="Action">
                    <button 
                      :class="['btn', 'btn-sm', u.is_active ? 'btn-disable' : 'btn-enable']"
                      @click="handleToggleActive(u)"
                    >
                      {{ u.is_active ? 'Disable' : 'Enable' }}
                    </button>
                  </td>
                </tr>
              </TransitionGroup>
            </table>
          </div>
        </div>

        <!-- VIEW 5: ADMIN ACCOUNTS (FULL PAGE) -->
        <div v-else-if="activeView === 'admins'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">💻 Admin Accounts</h2>
              <span class="count-pill">{{ filteredAdmins.length }} Admins</span>
            </div>
            
            <div class="view-actions">
              <div class="search-input-box glass">
                <span class="search-icon">🔍</span>
                <input 
                  type="text" 
                  v-model="adminSearch" 
                  placeholder="Search admins..." 
                  class="search-input"
                />
                <button v-if="adminSearch" class="clear-search-btn" @click="adminSearch = ''">✕</button>
              </div>

              <button class="btn btn-primary btn-sm inline-btn" @click="router.push('/register')">
                🛡️ Register Admin
              </button>
              <button class="btn btn-ghost btn-sm inline-btn" @click="fetchUsers" :disabled="loading">
                🔄 Refresh
              </button>
            </div>
          </div>

          <div class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th @click="toggleSort('full_name')" class="sortable-th">
                    Name / Email <span class="sort-icon">{{ getSortIcon('full_name') }}</span>
                  </th>
                  <th @click="toggleSort('username')" class="sortable-th">
                    Username <span class="sort-icon">{{ getSortIcon('username') }}</span>
                  </th>
                  <th @click="toggleSort('role')" class="sortable-th">
                    Admin Level <span class="sort-icon">{{ getSortIcon('role') }}</span>
                  </th>
                  <th @click="toggleSort('is_active')" class="sortable-th">
                    Status <span class="sort-icon">{{ getSortIcon('is_active') }}</span>
                  </th>
                  <th @click="toggleSort('created_at')" class="sortable-th">
                    Registered Date <span class="sort-icon">{{ getSortIcon('created_at') }}</span>
                  </th>
                  <th style="text-align: right;">Action</th>
                </tr>
              </thead>
              <TransitionGroup tag="tbody" name="list">
                <tr v-for="u in displayedAdmins" :key="u.id" class="user-row">
                  <td data-label="Name / Email">
                    <div class="name-col">
                      <span class="u-name">{{ u.full_name }}</span>
                      <span class="u-email">{{ u.email }}</span>
                    </div>
                  </td>
                  <td data-label="Username"><span class="u-username">@{{ u.username }}</span></td>
                  <td data-label="Admin Level">
                    <span :class="['role-badge', u.role]">{{ u.role?.toUpperCase() }}</span>
                  </td>
                  <td data-label="Status">
                    <span :class="['status-badge', u.is_active ? 'active' : 'disabled']">
                      {{ u.is_active ? 'Active' : 'Disabled' }}
                    </span>
                  </td>
                  <td data-label="Registered Date">
                    <span class="date-text">{{ formatDate(u.created_at) }}</span>
                  </td>
                  <td data-label="Action">
                    <button 
                      :disabled="u.role === 'super_admin'"
                      :class="['btn', 'btn-sm', u.is_active ? 'btn-disable' : 'btn-enable']"
                      @click="handleToggleActive(u)"
                    >
                      {{ u.is_active ? 'Disable' : 'Enable' }}
                    </button>
                  </td>
                </tr>
              </TransitionGroup>
            </table>
          </div>
        </div>

        <!-- VIEW 6: TOP-UP MONITORING & VERIFICATION -->
        <div v-else-if="activeView === 'topups'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">💳 Top-Up Verification & Monitoring</h2>
              <span class="count-pill alert-pill" v-if="pendingTopUpCount > 0">{{ pendingTopUpCount }} Pending</span>
            </div>
            
            <button class="btn btn-ghost btn-sm inline-btn" @click="fetchTopUpMonitoring(true)">
              🔄 Refresh Logs
            </button>
          </div>

          <div class="search-bar-wrap mb-3">
            <div class="search-input-box glass">
              <span class="search-icon">🔍</span>
              <input 
                type="text" 
                v-model="topUpSearch" 
                placeholder="Search reference number or username..." 
                class="search-input"
              />
            </div>
          </div>

          <div class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Method</th>
                  <th>Ref Number</th>
                  <th>System Ref</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Time</th>
                  <th style="text-align: right;">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in filteredTopUpLogs" :key="log.id" class="user-row">
                  <td>@{{ log.username }}</td>
                  <td><span class="method-tag">{{ log.payment_method?.toUpperCase() || 'GCASH' }}</span></td>
                  <td><code class="ref-code">{{ log.reference_number || 'N/A' }}</code></td>
                  <td><code class="ref-code sys-ref">{{ log.system_ref || 'N/A' }}</code></td>
                  <td><span class="amount-tag">₱{{ (log.amount || 0).toFixed(2) }}</span></td>
                  <td>
                    <span :class="['status-badge', log.status]">
                      {{ log.status?.toUpperCase() }}
                    </span>
                  </td>
                  <td><span class="date-text">{{ formatDate(log.created_at) }}</span></td>
                  <td style="text-align: right;">
                    <div class="action-btn-group" v-if="log.status === 'pending'">
                      <button class="btn btn-sm btn-enable" @click="handleVerifyTopUp(log.id)">Verify</button>
                      <button class="btn btn-sm btn-disable" @click="handleUnverifyTopUp(log.id)">Reject</button>
                    </div>
                    <span v-else class="status-done-lbl">Verified</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- VIEW 7: BOOKING HISTORY (NON-DOCUMENT ONLY) -->
        <div v-else-if="activeView === 'bookings'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🚗 Booking History</h2>
              <span class="count-pill">{{ filteredBookings.length }} Non-Document Rides</span>
            </div>
            
            <button class="btn btn-ghost btn-sm inline-btn" @click="fetchBookings">
              🔄 Refresh Bookings
            </button>
          </div>

          <!-- Date Range Filter Bar (Default 7 Days) -->
          <div class="bookings-filter-bar glass mb-3">
            <span class="filter-label">📅 Date Range Filter:</span>
            <div class="filter-inputs">
              <div class="filter-date-group">
                <span class="filter-date-label">Start:</span>
                <input 
                  type="date" 
                  v-model="bookingStartDate" 
                  class="filter-date-input"
                  title="Start Date"
                />
                <button 
                  v-if="bookingStartDate" 
                  class="btn-clear-date" 
                  @click="bookingStartDate = ''" 
                  title="Clear start date"
                >
                  ✕
                </button>
              </div>
              
              <div class="filter-date-group">
                <span class="filter-date-label">End:</span>
                <input 
                  type="date" 
                  v-model="bookingEndDate" 
                  class="filter-date-input"
                  title="End Date"
                />
                <button 
                  v-if="bookingEndDate" 
                  class="btn-clear-date" 
                  @click="bookingEndDate = ''" 
                  title="Clear end date"
                >
                  ✕
                </button>
              </div>

              <button type="button" class="btn btn-ghost btn-xs" @click="resetBookingDateRange('bookings')">
                Reset 7 Days
              </button>
            </div>
          </div>

          <div v-if="filteredBookings.length === 0" class="empty-state">
            <span style="font-size: 2.5rem;">🚗</span>
            <p>No non-document ride bookings recorded in this date range.</p>
          </div>

          <div v-else class="bookings-days-list">
            <div v-for="group in bookingsByDay" :key="group.date" class="booking-day-group glass">
              <div class="day-group-header">
                <span class="day-date-icon">📅</span>
                <span class="day-date-title">{{ formatDate(group.date) }}</span>
                <span class="day-count-badge">{{ group.list.length }} rides</span>
              </div>
              
              <div class="table-container">
                <table class="users-table bookings-table">
                  <thead>
                    <tr>
                      <th>Passenger</th>
                      <th>Driver</th>
                      <th>Pickup</th>
                      <th>Dropoff</th>
                      <th>Fare Amount</th>
                      <th>Time</th>
                      <th style="text-align: right;">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="b in group.list" :key="b.id" class="user-row">
                      <td>
                        <div class="name-col">
                          <span class="u-name">{{ b.passenger }}</span>
                          <span class="u-username">@{{ b.passenger_username }}</span>
                        </div>
                      </td>
                      <td>
                        <div class="name-col" v-if="b.driver_username && b.driver_username !== 'Unassigned'">
                          <span class="u-name">{{ b.driver }}</span>
                          <span class="u-username">@{{ b.driver_username }}</span>
                        </div>
                        <span v-else class="unassigned-lbl">Unassigned</span>
                      </td>
                      <td>{{ b.pickup }}</td>
                      <td>{{ b.dropoff }}</td>
                      <td><span class="fare-amount">₱{{ (b.amount || 0).toFixed(2) }}</span></td>
                      <td>{{ formatTime(b.date) }}</td>
                      <td style="text-align: right;">
                        <span :class="['status-badge', b.status]">{{ b.status?.toUpperCase() }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW 7B: DOCUMENT HISTORY (DOCUMENT DELIVERIES ONLY) -->
        <div v-else-if="activeView === 'doc_bookings'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">📄 Document History</h2>
              <span class="count-pill">{{ filteredDocBookings.length }} Document Deliveries</span>
            </div>
            
            <button class="btn btn-ghost btn-sm inline-btn" @click="fetchBookings">
              🔄 Refresh Documents
            </button>
          </div>

          <!-- Date Range Filter Bar (Default 7 Days) -->
          <div class="bookings-filter-bar glass mb-3">
            <span class="filter-label">📅 Date Range Filter:</span>
            <div class="filter-inputs">
              <div class="filter-date-group">
                <span class="filter-date-label">Start:</span>
                <input 
                  type="date" 
                  v-model="docBookingStartDate" 
                  class="filter-date-input"
                  title="Start Date"
                />
                <button 
                  v-if="docBookingStartDate" 
                  class="btn-clear-date" 
                  @click="docBookingStartDate = ''" 
                  title="Clear start date"
                >
                  ✕
                </button>
              </div>
              
              <div class="filter-date-group">
                <span class="filter-date-label">End:</span>
                <input 
                  type="date" 
                  v-model="docBookingEndDate" 
                  class="filter-date-input"
                  title="End Date"
                />
                <button 
                  v-if="docBookingEndDate" 
                  class="btn-clear-date" 
                  @click="docBookingEndDate = ''" 
                  title="Clear end date"
                >
                  ✕
                </button>
              </div>

              <button type="button" class="btn btn-ghost btn-xs" @click="resetBookingDateRange('doc_bookings')">
                Reset 7 Days
              </button>
            </div>
          </div>

          <div v-if="filteredDocBookings.length === 0" class="empty-state">
            <span style="font-size: 2.5rem;">📄</span>
            <p>No document or package deliveries recorded in this date range.</p>
          </div>

          <div v-else class="bookings-days-list">
            <div v-for="group in docBookingsByDay" :key="group.date" class="booking-day-group glass">
              <div class="day-group-header">
                <span class="day-date-icon">📅</span>
                <span class="day-date-title">{{ formatDate(group.date) }}</span>
                <span class="day-count-badge">{{ group.list.length }} deliveries</span>
              </div>
              
              <div class="table-container">
                <table class="users-table bookings-table">
                  <thead>
                    <tr>
                      <th>Sender</th>
                      <th>Rider / Driver</th>
                      <th>Pickup Address</th>
                      <th>Delivery Address</th>
                      <th>Document / Package Info</th>
                      <th>Tip</th>
                      <th>Fare Price</th>
                      <th>Proof / Attachments</th>
                      <th>Time</th>
                      <th style="text-align: right;">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="b in group.list" :key="b.id" class="user-row">
                      <td>
                        <div class="name-col">
                          <span class="u-name">{{ b.passenger }}</span>
                          <span class="u-username">@{{ b.passenger_username }}</span>
                        </div>
                      </td>
                      <td>
                        <div class="name-col" v-if="b.driver_username && b.driver_username !== 'Unassigned'">
                          <span class="u-name">{{ b.driver }}</span>
                          <span class="u-username">@{{ b.driver_username }}</span>
                        </div>
                        <span v-else class="unassigned-lbl">Unassigned</span>
                      </td>
                      <td>{{ b.pickup }}</td>
                      <td>{{ b.dropoff }}</td>
                      <td>
                        <span class="doc-info-text">{{ b.document_info || 'Document Package' }}</span>
                      </td>
                      <td>
                        <span v-if="b.document_tip" class="tip-tag">💰 ₱{{ b.document_tip }}</span>
                        <span v-else class="unassigned-lbl">—</span>
                      </td>
                      <td><span class="fare-amount">₱{{ (b.amount || 0).toFixed(2) }}</span></td>
                      <td>
                        <div class="proof-thumbnails-row">
                          <button v-if="b.document_image" type="button" class="btn-proof-preview" @click="selectedPreviewImage = b.document_image" title="View Document Image">
                            📄 Photo
                          </button>
                          <button v-if="b.received_image" type="button" class="btn-proof-preview" @click="selectedPreviewImage = b.received_image" title="View Recipient Photo">
                            📷 Received
                          </button>
                          <button v-if="b.signature_image" type="button" class="btn-proof-preview" @click="selectedPreviewImage = b.signature_image" title="View Recipient Signature">
                            ✍️ Signature
                          </button>
                          <span v-if="!b.document_image && !b.received_image && !b.signature_image" class="unassigned-lbl">No attachments</span>
                        </div>
                      </td>
                      <td>{{ formatTime(b.date) }}</td>
                      <td style="text-align: right;">
                        <span :class="['status-badge', b.status]">{{ b.status?.toUpperCase() }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW 8: FINANCIAL STATS -->
        <div v-else-if="activeView === 'stats'" class="page-view glass">
          <div class="view-header">
            <h2 class="view-heading">📈 Financial Analytics & System Load</h2>
            <button class="btn btn-ghost btn-sm inline-btn" @click="fetchBalanceData">🔄 Refresh Data</button>
          </div>

          <div class="stats-overview-grid">
            <div class="stat-card glass">
              <span class="stat-icon">💰</span>
              <div class="stat-meta">
                <span class="stat-title">Total Driver Balance</span>
                <span class="stat-val">₱{{ totalDriverBalance.toFixed(2) }}</span>
              </div>
            </div>
            <div class="stat-card glass">
              <span class="stat-icon">👥</span>
              <div class="stat-meta">
                <span class="stat-title">Total Users</span>
                <span class="stat-val">{{ users.length }}</span>
              </div>
            </div>
            <div class="stat-card glass">
              <span class="stat-icon">💳</span>
              <div class="stat-meta">
                <span class="stat-title">Pending Top-Ups</span>
                <span class="stat-val">{{ pendingTopUpCount }}</span>
              </div>
            </div>
          </div>
        </div>



        <!-- VIEW: ACCOUNTING MODULE -->
        <div v-else-if="activeView === 'accounting'" class="page-view glass accounting-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">💼 Financial Management System</h2>
              <p class="view-subheading">Accounting & Financial Management System module integration</p>
            </div>
          </div>

          <div class="accounting-card-container" style="display: flex; justify-content: center; align-items: center; min-height: 420px; padding: 2.5rem 1rem;">
            <div class="glass-card accounting-card" style="max-width: 540px; width: 100%; text-align: center; padding: 3rem 2rem; border-radius: 20px; background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4); backdrop-filter: blur(12px);">
              <div class="acc-icon-badge" style="width: 80px; height: 80px; margin: 0 auto 1.5rem auto; background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 51, 234, 0.2)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; border: 1px solid rgba(59, 130, 246, 0.35); box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);">
                💼
              </div>
              <h3 style="font-size: 1.6rem; font-weight: 700; color: #ffffff; margin-bottom: 0.75rem; letter-spacing: -0.02em;">Financial Management System</h3>
              <p style="color: #94a3b8; font-size: 0.98rem; line-height: 1.6; margin-bottom: 2.25rem;">
                Connect to accounting module to synchronize ledger entries, financial statements, and automated calculations.
              </p>
              <button type="button" class="btn btn-primary btn-lg" style="padding: 0.85rem 2.25rem; font-size: 1.02rem; font-weight: 600; border-radius: 12px; display: inline-flex; align-items: center; gap: 0.6rem; box-shadow: 0 8px 20px rgba(59, 130, 246, 0.35); cursor: pointer;">
                <span>⚡ Connect to Accounting Module</span>
              </button>
            </div>
          </div>
        </div>

        
        <!-- VIEW: ATTENDANCE - TIME SHEET -->
        <div v-else-if="activeView === 'attendance_timesheet'" class="page-view glass attendance-page-view">
          <div class="view-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="header-title-box">
              <h2 class="view-heading">📋 Employee Time Sheet Calendar</h2>
              <p class="view-subheading">Track employee attendance, time in, time out, break durations, and total delivered hours</p>
            </div>

            <!-- CURRENT USER LOG IN / LOG OUT ATTENDANCE BADGE & BUTTONS -->
            <div class="user-attendance-banner glass" style="padding: 0.85rem 1.25rem; border-radius: 12px; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; gap: 1rem;">
              <div style="display: flex; align-items: center; gap: 0.55rem;">
                <span style="font-size: 1.4rem;">👤</span>
                <div>
                  <div style="font-size: 0.88rem; font-weight: 700; color: #fff;">{{ userCurrentName }}</div>
                  <div style="font-size: 0.75rem; color: #94a3b8;">
                    Status: 
                    <span v-if="currentUserAttendanceState.isClockedIn" style="color: #10b981; font-weight: 700;">🟢 Logged In ({{ currentUserAttendanceState.timeIn }})</span>
                    <span v-else style="color: #ef4444; font-weight: 700;">🔴 Logged Out ({{ currentUserAttendanceState.timeOut || 'Not Clocked In Today' }})</span>
                  </div>
                </div>
              </div>

              <div style="display: flex; gap: 0.5rem; align-items: center;">
                <button 
                  type="button" 
                  class="btn btn-sm" 
                  :disabled="currentUserAttendanceState.isClockedIn"
                  @click="clockInCurrentUser"
                  style="background: #10b981; color: #fff; border: none; padding: 0.45rem 0.85rem; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.35rem;"
                >
                  ⚡ Log In
                </button>
                <button 
                  type="button" 
                  class="btn btn-sm" 
                  :disabled="!currentUserAttendanceState.isClockedIn"
                  @click="clockOutCurrentUser"
                  style="background: #ef4444; color: #fff; border: none; padding: 0.45rem 0.85rem; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.35rem;"
                >
                  🛑 Log Out
                </button>
                <button 
                  type="button" 
                  class="btn btn-ghost btn-sm" 
                  @click="clearAllAttendanceLogs"
                  title="Clear all logs for clean manual testing"
                  style="padding: 0.45rem 0.65rem; border-radius: 8px; font-size: 0.78rem; font-weight: 600;"
                >
                  🧹 Clear Logs
                </button>
                <button 
                  type="button" 
                  class="btn btn-ghost btn-sm" 
                  @click="seedSampleTimesheetLogs"
                  title="Populate mock data for testing calculations"
                  style="padding: 0.45rem 0.65rem; border-radius: 8px; font-size: 0.78rem; font-weight: 600;"
                >
                  🌱 Sample Data
                </button>
              </div>
            </div>
          </div>

          <!-- SUMMARY CARDS & FILTERS BAR -->
          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; background: rgba(15, 23, 42, 0.6); padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);">
            
            <!-- MONTH DROPDOWN & EMPLOYEE SELECTOR -->
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 1rem;">
              <div>
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  📅 Select Month
                </label>
                <select 
                  v-model="selectedTimesheetMonth" 
                  style="padding: 0.6rem 1rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600; min-width: 200px; cursor: pointer;"
                >
                  <option v-for="m in timesheetMonthOptions" :key="m.value" :value="m.value">
                    {{ m.label }}
                  </option>
                </select>
              </div>

              <div>
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  👤 Select Employee
                </label>
                <select 
                  v-model="selectedTimesheetEmployeeId" 
                  style="padding: 0.6rem 1rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600; min-width: 220px; cursor: pointer;"
                >
                  <option value="current_user">Current User ({{ userCurrentName }})</option>
                  <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="emp.id">
                    {{ emp.full_name || emp.username }} ({{ emp.position || emp.role || 'Employee' }})
                  </option>
                </select>
              </div>
            </div>

            <!-- STAT SUMMARY BADGES (CLICKABLE FILTERS) -->
            <div style="display: flex; flex-wrap: wrap; gap: 0.85rem;">
              <!-- PRESENT BADGE -->
              <div 
                @click="setTimesheetFilter('Present')"
                :style="{
                  textAlign: 'right',
                  background: timesheetStatusFilter === 'Present' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: timesheetStatusFilter === 'Present' ? '2px solid #10b981' : '1px solid rgba(16, 185, 129, 0.3)',
                  boxShadow: timesheetStatusFilter === 'Present' ? '0 0 12px rgba(16, 185, 129, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Present logs only (click again to show all)"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🟢 Present</span>
                  <span v-if="timesheetStatusFilter === 'Present'" style="font-size: 0.6rem; background: #10b981; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #10b981;">{{ timesheetSummary.presentDays }}</div>
              </div>

              <!-- LATE BADGE -->
              <div 
                @click="setTimesheetFilter('Late')"
                :style="{
                  textAlign: 'right',
                  background: timesheetStatusFilter === 'Late' ? 'rgba(245, 158, 11, 0.35)' : 'rgba(245, 158, 11, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: timesheetStatusFilter === 'Late' ? '2px solid #f59e0b' : '1px solid rgba(245, 158, 11, 0.3)',
                  boxShadow: timesheetStatusFilter === 'Late' ? '0 0 12px rgba(245, 158, 11, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Late logs only (click again to show all)"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🟠 Late</span>
                  <span v-if="timesheetStatusFilter === 'Late'" style="font-size: 0.6rem; background: #f59e0b; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #f59e0b;">{{ timesheetSummary.lateDays }}</div>
              </div>

              <!-- EARLY OUT BADGE -->
              <div 
                @click="setTimesheetFilter('Early Out')"
                :style="{
                  textAlign: 'right',
                  background: timesheetStatusFilter === 'Early Out' ? 'rgba(59, 130, 246, 0.35)' : 'rgba(59, 130, 246, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: timesheetStatusFilter === 'Early Out' ? '2px solid #3b82f6' : '1px solid rgba(59, 130, 246, 0.3)',
                  boxShadow: timesheetStatusFilter === 'Early Out' ? '0 0 12px rgba(59, 130, 246, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Early Out logs only (click again to show all)"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🔵 Early Out</span>
                  <span v-if="timesheetStatusFilter === 'Early Out'" style="font-size: 0.6rem; background: #3b82f6; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #3b82f6;">{{ timesheetSummary.earlyOutDays }}</div>
              </div>

              <!-- ABSENT BADGE -->
              <div 
                @click="setTimesheetFilter('Absent')"
                :style="{
                  textAlign: 'right',
                  background: timesheetStatusFilter === 'Absent' ? 'rgba(239, 68, 68, 0.35)' : 'rgba(239, 68, 68, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: timesheetStatusFilter === 'Absent' ? '2px solid #ef4444' : '1px solid rgba(239, 68, 68, 0.3)',
                  boxShadow: timesheetStatusFilter === 'Absent' ? '0 0 12px rgba(239, 68, 68, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Absent logs only (click again to show all)"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🔴 Absent</span>
                  <span v-if="timesheetStatusFilter === 'Absent'" style="font-size: 0.6rem; background: #ef4444; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #ef4444;">{{ timesheetSummary.absentDays }}</div>
              </div>

              <!-- HOLIDAYS BADGE -->
              <div 
                @click="setTimesheetFilter('Holiday')"
                :style="{
                  textAlign: 'right',
                  background: timesheetStatusFilter === 'Holiday' ? 'rgba(16, 185, 129, 0.4)' : 'rgba(16, 185, 129, 0.15)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: timesheetStatusFilter === 'Holiday' ? '2px solid #10b981' : '1px solid rgba(16, 185, 129, 0.4)',
                  boxShadow: timesheetStatusFilter === 'Holiday' ? '0 0 12px rgba(16, 185, 129, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Holiday logs only (click again to show all)"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🎉 Holidays</span>
                  <span v-if="timesheetStatusFilter === 'Holiday'" style="font-size: 0.6rem; background: #10b981; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #10b981;">{{ timesheetSummary.holidayDays }}</div>
              </div>

              <!-- TOTAL DELIVERED / SHOW ALL BADGE -->
              <div 
                @click="setTimesheetFilter('all')"
                :style="{
                  textAlign: 'right',
                  background: timesheetStatusFilter === 'all' ? 'rgba(56, 189, 248, 0.25)' : 'rgba(56, 189, 248, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: timesheetStatusFilter === 'all' ? '2px solid #38bdf8' : '1px solid rgba(56, 189, 248, 0.3)',
                  boxShadow: timesheetStatusFilter === 'all' ? '0 0 10px rgba(56, 189, 248, 0.4)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to show ALL timesheet logs"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>⚡ Show All (Total)</span>
                  <span v-if="timesheetStatusFilter === 'all'" style="font-size: 0.6rem; background: #38bdf8; color: #0f172a; font-weight: 800; padding: 1px 4px; border-radius: 3px;">ALL</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #38bdf8;">{{ timesheetSummary.totalDeliveredHours.toFixed(1) }} hrs</div>
              </div>
            </div>
          </div>

          <!-- TIMESHEET CALENDAR TABLE CARD WITH SCROLLABLE CONTAINER -->
          <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                <span>📅</span> Timesheet Logs for {{ selectedTimesheetMonthLabel }}
                <span v-if="timesheetStatusFilter !== 'all'" style="font-size: 0.78rem; background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.2rem 0.65rem; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.4); display: inline-flex; align-items: center; gap: 0.4rem;">
                  Filtered: <strong>{{ timesheetStatusFilter }}</strong>
                  <button type="button" @click="timesheetStatusFilter = 'all'" style="background: rgba(239, 68, 68, 0.25); border: none; color: #fca5a5; cursor: pointer; font-weight: 800; padding: 1px 6px; border-radius: 4px; font-size: 0.72rem;">✕ Show All</button>
                </span>
              </h3>
              <div style="display: flex; gap: 0.4rem; align-items: center; font-size: 0.78rem; flex-wrap: wrap;">
                <span @click="setTimesheetFilter('Present')" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: timesheetStatusFilter === 'Present' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '700', border: timesheetStatusFilter === 'Present' ? '1px solid #10b981' : '1px solid transparent' }">🟢 Present</span>
                <span @click="setTimesheetFilter('Late')" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: timesheetStatusFilter === 'Late' ? 'rgba(245, 158, 11, 0.35)' : 'rgba(245, 158, 11, 0.1)', color: '#f59e0b', fontWeight: '700', border: timesheetStatusFilter === 'Late' ? '1px solid #f59e0b' : '1px solid transparent' }">🟠 Late</span>
                <span @click="setTimesheetFilter('Early Out')" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: timesheetStatusFilter === 'Early Out' ? 'rgba(59, 130, 246, 0.35)' : 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', fontWeight: '700', border: timesheetStatusFilter === 'Early Out' ? '1px solid #3b82f6' : '1px solid transparent' }">🔵 Early Out</span>
                <span @click="setTimesheetFilter('Absent')" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: timesheetStatusFilter === 'Absent' ? 'rgba(239, 68, 68, 0.35)' : 'rgba(239, 68, 68, 0.1)', color: '#ef4444', fontWeight: '700', border: timesheetStatusFilter === 'Absent' ? '1px solid #ef4444' : '1px solid transparent' }">🔴 Absent</span>
                <span @click="setTimesheetFilter('Holiday')" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: timesheetStatusFilter === 'Holiday' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '700', border: timesheetStatusFilter === 'Holiday' ? '1px solid #10b981' : '1px solid transparent' }">🎉 Holiday</span>
                <span @click="setTimesheetFilter('all')" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: timesheetStatusFilter === 'all' ? 'rgba(56, 189, 248, 0.35)' : 'rgba(56, 189, 248, 0.1)', color: '#38bdf8', fontWeight: '700', border: timesheetStatusFilter === 'all' ? '1px solid #38bdf8' : '1px solid transparent' }">⚡ All</span>
              </div>
            </div>

            <!-- SCROLLABLE TABLE CONTAINER (MAX HEIGHT 580PX WITH STICKY HEADERS) -->
            <div 
              ref="timesheetScrollContainer"
              class="table-responsive timesheet-drag-scroll" 
              :class="{ 'is-dragging': isDraggingTable }"
              @mousedown="onTableMouseDown"
              @mouseleave="onTableMouseLeave"
              @mouseup="onTableMouseUp"
              @mousemove="onTableMouseMove"
              style="max-height: 580px; overflow-y: auto; overflow-x: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);"
            >
              <table class="data-table" style="width: 100%; border-collapse: collapse; position: relative;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">date</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">name</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">status</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">time in</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">time in photo</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">time in address</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">time out</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">log out photo</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">log out address</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">working hours</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Lunch break</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Break time</th>
                    <th style="padding: 0.85rem 1rem; text-align: right; color: #38bdf8; position: sticky; top: 0; background: #0f172a; z-index: 5;">Delivered hours</th>
                    <th v-if="canAccessMenu('attendance_approver')" style="padding: 0.85rem 1rem; text-align: center; color: #f43f5e; position: sticky; top: 0; background: #0f172a; z-index: 5;">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="row in filteredTimesheetRecords" 
                    :key="row.date"
                    :style="{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      fontSize: '0.88rem',
                      background: row.isHoliday ? 'rgba(16, 185, 129, 0.12)' : (row.isWeekend ? 'rgba(30, 41, 59, 0.25)' : (row.isToday ? 'rgba(59, 130, 246, 0.12)' : 'transparent'))
                    }"
                  >
                    <!-- DATE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <span :style="{ fontWeight: '600', color: row.isToday ? '#60a5fa' : (row.isHoliday ? '#10b981' : (row.isWeekend ? '#94a3b8' : '#e2e8f0')) }">
                        {{ row.formattedDate }}
                      </span>
                      <span v-if="row.isToday" style="margin-left: 0.4rem; background: rgba(59, 130, 246, 0.3); color: #60a5fa; font-size: 0.7rem; padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 700;">TODAY</span>
                      <span v-else-if="row.isHoliday" style="margin-left: 0.4rem; background: rgba(16, 185, 129, 0.25); color: #10b981; font-size: 0.7rem; padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 700;">HOLIDAY</span>
                      <span v-else-if="row.isWeekend" style="margin-left: 0.4rem; background: rgba(148, 163, 184, 0.15); color: #94a3b8; font-size: 0.7rem; padding: 0.15rem 0.4rem; border-radius: 4px;">WEEKEND</span>
                    </td>

                    <!-- NAME (HOLIDAY NAME ON UNWORKED HOLIDAY, OR EMPLOYEE NAME) -->
                    <td style="padding: 0.85rem 1rem; font-weight: 600; color: #fff; white-space: nowrap;">
                      <span v-if="row.isHoliday && row.status === 'Holiday'" style="color: #10b981; font-weight: 700;">
                        🎉 {{ row.employeeName }}
                      </span>
                      <span v-else-if="row.isWeekend && row.status === 'Weekend'" style="color: #94a3b8; font-weight: 600;">
                        ☕ {{ row.employeeName }}
                      </span>
                      <span v-else>
                        {{ row.employeeName }}
                      </span>
                    </td>

                    <!-- STATUS BADGE WITH SELECTOR OVERRIDE -->
                    <td style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <span v-if="row.isHoliday && row.status === 'Holiday'" :style="getStatusBadgeStyle('Holiday')">
                        🎉 {{ row.holidayType || 'Regular Holiday' }}
                      </span>
                      <span v-else-if="row.isWeekend && row.status === 'Weekend'" :style="getStatusBadgeStyle('Weekend')">
                        ☕ Rest Day
                      </span>
                      <span v-else :style="getStatusBadgeStyle(row.status)">
                        <template v-if="row.status === 'Present'">🟢 Present</template>
                        <template v-else-if="row.status === 'Late'">🟠 Late</template>
                        <template v-else-if="row.status === 'Early Out'">🔵 Early Out</template>
                        <template v-else-if="row.status === 'Absent'">🔴 Absent</template>
                        <template v-else>{{ row.status }}</template>
                      </span>
                    </td>

                    <!-- TIME IN -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <span v-if="row.timeIn && row.timeIn !== '--:--'" style="color: #10b981; font-weight: 600; background: rgba(16, 185, 129, 0.1); padding: 0.2rem 0.5rem; border-radius: 6px;">
                        🟢 {{ row.timeIn }}
                      </span>
                      <span v-else style="color: #64748b;">--:--</span>
                    </td>

                    <!-- TIME IN PHOTO -->
                    <td style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <button 
                        v-if="row.timeInPhoto" 
                        type="button" 
                        @click="openPhotoPreviewModal(row.timeInPhoto, 'Time In', row)"
                        style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; gap: 0.35rem; transition: all 0.2s;"
                        title="Click to view Time In Photo Verification"
                      >
                        📸 View Photo
                      </button>
                      <span v-else-if="row.photoPurged" style="color: #64748b; font-size: 0.75rem;" title="Purged after 30 days to save space">
                        🗑️ Purged (>30d)
                      </span>
                      <span v-else style="color: #64748b;">--</span>
                    </td>

                    <!-- TIME IN ADDRESS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #cbd5e1; font-size: 0.82rem;">
                      <span v-if="row.timeInAddress && row.timeInAddress !== '--'" style="display: inline-flex; align-items: center; gap: 0.35rem; background: rgba(16, 185, 129, 0.1); padding: 0.2rem 0.6rem; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.2); color: #34d399;">
                        📍 {{ row.timeInAddress }}
                      </span>
                      <span v-else style="color: #64748b;">--</span>
                    </td>

                    <!-- TIME OUT -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <span v-if="row.timeOut && row.timeOut !== '--:--'" style="color: #f43f5e; font-weight: 600; background: rgba(244, 63, 94, 0.1); padding: 0.2rem 0.5rem; border-radius: 6px;">
                        🔴 {{ row.timeOut }}
                      </span>
                      <span v-else style="color: #64748b;">--:--</span>
                    </td>

                    <!-- LOG OUT PHOTO -->
                    <td style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <button 
                        v-if="row.timeOutPhoto" 
                        type="button" 
                        @click="openPhotoPreviewModal(row.timeOutPhoto, 'Log Out', row)"
                        style="background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.3); color: #fca5a5; padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; gap: 0.35rem; transition: all 0.2s;"
                        title="Click to view Log Out Photo Verification"
                      >
                        📸 View Photo
                      </button>
                      <span v-else-if="row.photoPurged" style="color: #64748b; font-size: 0.75rem;" title="Purged after 30 days to save space">
                        🗑️ Purged (>30d)
                      </span>
                      <span v-else style="color: #64748b;">--</span>
                    </td>

                    <!-- LOG OUT ADDRESS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #cbd5e1; font-size: 0.82rem;">
                      <span v-if="row.timeOutAddress && row.timeOutAddress !== '--'" style="display: inline-flex; align-items: center; gap: 0.35rem; background: rgba(244, 63, 94, 0.1); padding: 0.2rem 0.6rem; border-radius: 6px; border: 1px solid rgba(244, 63, 94, 0.2); color: #fca5a5;">
                        📍 {{ row.timeOutAddress }}
                      </span>
                      <span v-else style="color: #64748b;">--</span>
                    </td>

                    <!-- WORKING HOURS (ALWAYS 8) -->
                    <td style="padding: 0.85rem 1rem; text-align: center; font-weight: 600; color: #cbd5e1;">
                      {{ row.workingHours }}
                    </td>

                    <!-- LUNCH BREAK (30MINS) -->
                    <td style="padding: 0.85rem 1rem; text-align: center; color: #cbd5e1;">
                      {{ row.lunchBreak }}
                    </td>

                    <!-- BREAK TIME 30(MINS) -->
                    <td style="padding: 0.85rem 1rem; text-align: center; color: #cbd5e1;">
                      {{ row.breakTime }}
                    </td>

                    <!-- DELIVERED HOURS -->
                    <td style="padding: 0.85rem 1rem; text-align: right; font-weight: 700;">
                      <span :style="{ color: row.deliveredHours > 0 ? '#38bdf8' : '#64748b' }">
                        {{ row.deliveredHours > 0 ? row.deliveredHours.toFixed(1) + ' hrs' : '0.0 hrs' }}
                      </span>
                    </td>

                    <!-- ACTION COLUMN (SHOWN WHEN ATTENDANCE APPROVER SLIDER IS ENABLED IN SET ACCESS) -->
                    <td v-if="canAccessMenu('attendance_approver')" style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <button 
                        type="button" 
                        @click="clearTimesheetRowData(row)"
                        style="background: rgba(239, 68, 68, 0.18); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; padding: 0.3rem 0.75rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; gap: 0.35rem; transition: all 0.2s; box-shadow: 0 2px 6px rgba(239, 68, 68, 0.2);"
                        title="Clear attendance row data for this date"
                      >
                        🗑️ Clear Data
                      </button>
                    </td>
                  </tr>

                  <tr v-if="filteredTimesheetRecords.length === 0">
                    <td :colspan="canAccessMenu('attendance_approver') ? 14 : 13" style="text-align: center; padding: 3.5rem 1.5rem; color: #94a3b8;">
                      <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                      <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.25rem;">
                        No timesheet records match filter "{{ timesheetStatusFilter }}"
                      </div>
                      <button type="button" class="btn btn-sm btn-primary" @click="timesheetStatusFilter = 'all'" style="margin-top: 0.75rem; padding: 0.45rem 1.1rem; border-radius: 8px; cursor: pointer; background: linear-gradient(135deg, #3b82f6, #6366f1); border: none; color: #fff; font-weight: 700;">
                        Show All Timesheet Logs
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VIEW: ATTENDANCE - TIME LOG -->
        <div v-else-if="activeView === 'attendance_timelog'" class="page-view glass attendance-page-view">
          <div class="view-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="header-title-box">
              <h2 class="view-heading">⏱️ Attendance & Manual Time Log Requests</h2>
              <p class="view-subheading">File manual attendance adjustments, missing punches, overtime pre-approvals, schedule changes, and leaves</p>
            </div>

            <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
              <div style="display: flex; align-items: center; gap: 0.5rem; background: rgba(30, 41, 59, 0.8); padding: 0.4rem 0.85rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.12);">
                <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">🎭 Active Admin Role:</span>
                <select v-model="simulatedAdminRole" style="background: transparent; border: none; color: #38bdf8; font-size: 0.85rem; font-weight: 700; cursor: pointer; outline: none;">
                  <option value="auto" style="background: #1e293b; color: #38bdf8;">👤 Actual Logged-in User ({{ (user?.role || user?.account_role || 'hr_staff').toUpperCase() }})</option>
                  <option value="super_admin" style="background: #1e293b; color: #38bdf8;">👑 Super Admin (Access All)</option>
                  <option value="it_admin" style="background: #1e293b; color: #60a5fa;">💻 IT Admin (IT Members Only)</option>
                  <option value="hr_admin" style="background: #1e293b; color: #10b981;">👥 HR Admin (HR Members Only)</option>
                  <option value="accounting_admin" style="background: #1e293b; color: #f59e0b;">💼 Accounting Admin (Accounting Members)</option>
                  <option value="ops_admin" style="background: #1e293b; color: #c084fc;">🚚 Ops Admin (Ops Members)</option>
                  <option value="hr_staff" style="background: #1e293b; color: #94a3b8;">👤 HR Staff (View Only - Lock Actions)</option>
                  <option value="staff" style="background: #1e293b; color: #94a3b8;">👤 Regular Staff (View Only - Lock Actions)</option>
                </select>
              </div>

              <button 
                type="button" 
                class="btn btn-primary" 
                @click="openTimeLogModal"
                style="padding: 0.65rem 1.35rem; font-weight: 700; border-radius: 10px; display: inline-flex; align-items: center; gap: 0.5rem; background: linear-gradient(135deg, #10b981, #059669); border: none; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35); cursor: pointer;"
              >
                <span style="font-size: 1.2rem; line-height: 1;">+</span>
                <span>File Manual Log Request</span>
              </button>
            </div>
          </div>

          <!-- STAT CARDS -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(59, 130, 246, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">📝</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Total Requests</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #fff;">{{ manualTimeLogs.length }}</div>
              </div>
            </div>
            <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(245, 158, 11, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">⏳</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Pending Approval</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #f59e0b;">{{ manualTimeLogs.filter(l => l.status === 'Pending').length }}</div>
              </div>
            </div>
            <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(16, 185, 129, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">✅</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Approved Logs</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #10b981;">{{ manualTimeLogs.filter(l => l.status === 'Approved').length }}</div>
              </div>
            </div>
            <div class="glass-card" style="padding: 1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(239, 68, 68, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">❌</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Rejected</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #ef4444;">{{ manualTimeLogs.filter(l => l.status === 'Rejected').length }}</div>
              </div>
            </div>
          </div>

          <!-- TABLE CONTAINER -->
          <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff;">📋 Manual Time Log & Attendance Audit Table</h3>
              <span style="font-size: 0.8rem; color: #94a3b8;">Showing {{ manualTimeLogs.length }} request entries</span>
            </div>

            <div 
              class="table-responsive timesheet-drag-scroll" 
              @mousedown="onTableMouseDown"
              @mouseleave="onTableMouseLeave"
              @mouseup="onTableMouseUp"
              @mousemove="onTableMouseMove"
              style="max-height: 520px; overflow-y: auto; overflow-x: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); cursor: grab;"
            >
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Request Type</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Employee</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Date / Period</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Details</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Reason</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Status</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Approver</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Approver Date</th>
                    <th v-if="canApproveModule('timelog')" style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="log in manualTimeLogs" 
                    :key="log.id"
                    :style="{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      fontSize: '0.88rem',
                      background: log.status === 'Approved' ? 'rgba(16, 185, 129, 0.15)' : (log.status === 'Rejected' ? 'rgba(239, 68, 68, 0.08)' : 'transparent'),
                      borderLeft: log.status === 'Approved' ? '4px solid #10b981' : (log.status === 'Rejected' ? '4px solid #ef4444' : '4px solid #f59e0b')
                    }"
                  >
                    <!-- REQUEST TYPE -->
                    <td style="padding: 0.85rem 1rem; font-weight: 700; white-space: nowrap;">
                      <span v-if="log.type === 'Missing In'" style="color: #60a5fa;">📥 Missing In</span>
                      <span v-else-if="log.type === 'Missing Out'" style="color: #f43f5e;">📤 Missing Out</span>
                      <span v-else-if="log.type === 'Missing In and Out'" style="color: #c084fc;">🔄 Missing In & Out</span>
                      <span v-else-if="log.type === 'Overtime'" style="color: #f59e0b;">⏰ Overtime</span>
                      <span v-else-if="log.type === 'Change Schedule'" style="color: #38bdf8;">📅 Change Schedule</span>
                      <span v-else-if="log.type === 'Leave'" style="color: #10b981;">🏖️ Leave</span>
                      <span v-else>{{ log.type }}</span>
                    </td>

                    <!-- EMPLOYEE -->
                    <td style="padding: 0.85rem 1rem; font-weight: 600; color: #fff; white-space: nowrap;">
                      {{ log.employeeName }}
                    </td>

                    <!-- DATE / PERIOD -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #cbd5e1; font-weight: 600;">
                      {{ log.dateRange }}
                    </td>

                    <!-- DETAILS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #94a3b8; font-size: 0.82rem;">
                      {{ log.details }}
                    </td>

                    <!-- REASON -->
                    <td style="padding: 0.85rem 1rem; color: #cbd5e1; max-width: 240px; font-size: 0.82rem; line-height: 1.4;">
                      {{ log.reason }}
                    </td>

                    <!-- STATUS -->
                    <td style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <span 
                        v-if="log.status === 'Approved'"
                        style="background: rgba(16, 185, 129, 0.25); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.5); padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; display: inline-block;"
                      >
                        🟢 Approved
                      </span>
                      <span 
                        v-else-if="log.status === 'Rejected'"
                        style="background: rgba(239, 68, 68, 0.25); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.5); padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; display: inline-block;"
                      >
                        🔴 Rejected
                      </span>
                      <span 
                        v-else
                        style="background: rgba(245, 158, 11, 0.25); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.5); padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; display: inline-block;"
                      >
                        🟠 Pending
                      </span>
                    </td>

                    <!-- APPROVER -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #cbd5e1; font-size: 0.82rem;">
                      {{ log.approver }}
                    </td>

                    <!-- APPROVER DATE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #94a3b8; font-size: 0.82rem;">
                      {{ log.approverDate }}
                    </td>

                    <!-- ACTIONS -->
                    <td v-if="canApproveModule('timelog')" style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <div v-if="canUserActionRequest(log)" style="display: flex; gap: 0.35rem; justify-content: center;">
                        <button 
                          type="button" 
                          title="Approve Request"
                          :disabled="log.status === 'Approved'"
                          @click="approveTimeLogRequest(log.id)"
                          style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.25rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700; cursor: pointer;"
                        >
                          ✓ Approve
                        </button>
                        <button 
                          type="button" 
                          title="Reject Request"
                          :disabled="log.status === 'Rejected'"
                          @click="rejectTimeLogRequest(log.id)"
                          style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.25rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700; cursor: pointer;"
                        >
                          ✕ Reject
                        </button>
                      </div>
                      <span v-else style="font-size: 0.75rem; color: #64748b; font-style: italic; background: rgba(30, 41, 59, 0.5); padding: 0.2rem 0.5rem; border-radius: 4px; border: 1px solid rgba(255,255,255,0.05);">
                        🔒 {{ getRequiredAdminLabel(log) }} Only
                      </span>
                    </td>
                  </tr>

                  <tr v-if="manualTimeLogs.length === 0">
                    <td colspan="9" style="text-align: center; padding: 3rem; color: #94a3b8;">
                      No manual time log requests found. Click <strong>+ File Manual Log Request</strong> to add one.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- MODAL FOR MANUAL TIME LOG REQUEST -->
          <div v-if="isTimeLogModalOpen" class="modal-overlay" style="position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 1rem;">
            <div class="glass-card modal-content" style="max-width: 520px; width: 100%; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 1.75rem; box-shadow: 0 25px 50px rgba(0,0,0,0.5); max-height: 90vh; overflow-y: auto;">
              
              <!-- MODAL HEADER -->
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.85rem;">
                <h3 style="font-size: 1.2rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                  <span>⏱️</span> File Attendance & Time Log Request
                </h3>
                <button type="button" @click="closeTimeLogModal" style="background: transparent; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer; line-height: 1;">✕</button>
              </div>

              <form @submit.prevent="submitTimeLogRequest">
                <!-- 1. REQUEST TYPE SELECTOR (FIRST AND ONLY PRIMARY SELECTOR AT START) -->
                <div style="margin-bottom: 1.25rem;">
                  <label style="display: block; font-size: 0.82rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">
                    📌 Select Request Type
                  </label>
                  <select 
                    v-model="timelogRequestType"
                    style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.4); color: #fff; font-size: 0.95rem; font-weight: 700; cursor: pointer; outline: none;"
                  >
                    <option value="Missing In">Missing In</option>
                    <option value="Missing Out">Missing Out</option>
                    <option value="Missing In and Out">Missing In and Out</option>
                    <option value="Overtime">Overtime</option>
                    <option value="Change Schedule">Change Schedule</option>
                    <option value="Leave" :disabled="currentUserAvailableLeaveCredits <= 0">
                      🏖️ Leave {{ currentUserAvailableLeaveCredits <= 0 ? '(0 Leave Credits - Disabled)' : `(${currentUserAvailableLeaveCredits} Day${currentUserAvailableLeaveCredits > 1 ? 's' : ''} Available)` }}
                    </option>
                  </select>
                </div>

                <!-- DYNAMIC FIELDS BASED ON REQUEST TYPE -->

                <!-- CASE: MISSING IN -->
                <div v-if="timelogRequestType === 'Missing In'" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem;">
                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Date</label>
                    <input type="date" v-model="timelogForm.date" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                  </div>
                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🟢 Time In</label>
                    <input type="time" v-model="timelogForm.timeIn" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                  </div>
                </div>

                <!-- CASE: MISSING OUT -->
                <div v-else-if="timelogRequestType === 'Missing Out'" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem;">
                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Date</label>
                    <input type="date" v-model="timelogForm.date" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                  </div>
                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🔴 Time Out</label>
                    <input type="time" v-model="timelogForm.timeOut" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                  </div>
                </div>

                <!-- CASE: MISSING IN AND OUT -->
                <div v-else-if="timelogRequestType === 'Missing In and Out'" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem;">
                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Date</label>
                    <input type="date" v-model="timelogForm.date" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                  </div>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🟢 Time In</label>
                      <input type="time" v-model="timelogForm.timeIn" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🔴 Time Out</label>
                      <input type="time" v-model="timelogForm.timeOut" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                  </div>
                </div>

                <!-- CASE: OVERTIME -->
                <div v-else-if="timelogRequestType === 'Overtime'" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem;">
                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Date</label>
                    <input type="date" v-model="timelogForm.date" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                  </div>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">⏰ Overtime In</label>
                      <input type="time" v-model="timelogForm.otIn" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">⏰ Overtime Out</label>
                      <input type="time" v-model="timelogForm.otOut" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                  </div>
                </div>

                <!-- CASE: CHANGE SCHEDULE -->
                <div v-else-if="timelogRequestType === 'Change Schedule'" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem;">
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Start Date</label>
                      <input type="date" v-model="timelogForm.startDate" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 End Date</label>
                      <input type="date" v-model="timelogForm.endDate" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                  </div>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🟢 New Time In</label>
                      <input type="time" v-model="timelogForm.timeIn" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🔴 New Time Out</label>
                      <input type="time" v-model="timelogForm.timeOut" required style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" />
                    </div>
                  </div>
                </div>

                <!-- CASE: LEAVE -->
                <div v-else-if="timelogRequestType === 'Leave'" style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem; background: rgba(30, 41, 59, 0.5); padding: 1rem; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.25);">
                  
                  <!-- USER MAXIMUM AVAILABLE LEAVE CREDITS DISPLAY -->
                  <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(15, 23, 42, 0.7); padding: 0.75rem 1rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div>
                      <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">User Maximum Available Leave Balance</div>
                      <div style="font-size: 1.15rem; font-weight: 800; color: #10b981; display: flex; align-items: center; gap: 0.4rem; margin-top: 0.15rem;">
                        <span>🏖️ {{ currentUserAvailableLeaveCredits }} Day{{ currentUserAvailableLeaveCredits !== 1 ? 's' : '' }} Available</span>
                      </div>
                    </div>
                    <span style="font-size: 0.75rem; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 6px; font-weight: 700;">
                      Current User Max Limit
                    </span>
                  </div>

                  <div>
                    <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">🏖️ Leave Type</label>
                    <select v-model="timelogForm.leaveType" style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; cursor: pointer;">
                      <option value="Sick Leave">Sick Leave</option>
                      <option value="Vacation Leave">Vacation Leave</option>
                    </select>
                  </div>

                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Date From</label>
                      <input 
                        type="date" 
                        v-model="timelogForm.startDate" 
                        @change="handleLeaveDateChange"
                        required 
                        style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" 
                      />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">📅 Date To</label>
                      <input 
                        type="date" 
                        v-model="timelogForm.endDate" 
                        :min="timelogForm.startDate"
                        :max="maxAllowedLeaveEndDate"
                        @change="handleLeaveDateChange"
                        required 
                        style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem;" 
                      />
                    </div>
                  </div>

                  <!-- SELECTED DURATION SUMMARY BADGE -->
                  <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); padding: 0.5rem 0.85rem; border-radius: 8px; font-size: 0.82rem;">
                    <span style="color: #cbd5e1;">Duration: <strong style="color: #38bdf8;">{{ selectedLeaveDaysCount }} Day{{ selectedLeaveDaysCount !== 1 ? 's' : '' }}</strong> selected</span>
                    <span style="color: #94a3b8; font-size: 0.78rem;">Limit: <strong style="color: #10b981;">{{ currentUserAvailableLeaveCredits }} Day{{ currentUserAvailableLeaveCredits !== 1 ? 's' : '' }} Max</strong></span>
                  </div>

                  <!-- WARNING / NOTIFICATION BANNER IF AUTO-ADJUSTED -->
                  <div v-if="leaveAdjustmentMessage" style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 0.6rem 0.85rem; color: #fbbf24; font-size: 0.8rem; line-height: 1.4;">
                    {{ leaveAdjustmentMessage }}
                  </div>

                </div>

                <!-- REASON INPUT (COMMON TO ALL TYPES) -->
                <div style="margin-bottom: 1.5rem;">
                  <label style="display: block; font-size: 0.8rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.35rem;">💬 Reason</label>
                  <textarea 
                    v-model="timelogForm.reason" 
                    rows="3" 
                    required 
                    placeholder="Provide detailed reason for this log request..."
                    style="width: 100%; padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; resize: vertical;"
                  ></textarea>
                </div>

                <!-- SUBMIT & CANCEL BUTTONS -->
                <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
                  <button 
                    type="button" 
                    @click="closeTimeLogModal"
                    style="padding: 0.65rem 1.25rem; border-radius: 8px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; font-weight: 600; cursor: pointer;"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    style="padding: 0.65rem 1.5rem; border-radius: 8px; background: linear-gradient(135deg, #10b981, #059669); border: none; color: #fff; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);"
                  >
                    Submit Request
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>



        <!-- VIEW: ATTENDANCE - OVERTIME -->
        <div v-else-if="activeView === 'attendance_overtime'" class="page-view glass attendance-page-view">
          <div class="view-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="header-title-box">
              <h2 class="view-heading">⏰ Overtime Management & Audit</h2>
              <p class="view-subheading">Populated overtime logs per user from time logs, rate multipliers, and pending/approved/denied status filtering</p>
            </div>
          </div>

          <!-- CONTROLS & STAT SUMMARY BADGES WITH CLICKABLE STATUS FILTERS -->
          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; background: rgba(15, 23, 42, 0.65); padding: 1.25rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.12); backdrop-filter: blur(12px);">
            
            <!-- EMPLOYEE SELECTOR -->
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 1rem;">
              <div>
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  👤 Select Employee / Driver
                </label>
                <select 
                  v-model="selectedOvertimeEmployeeId" 
                  style="padding: 0.6rem 1rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600; min-width: 220px; cursor: pointer;"
                >
                  <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="emp.id">
                    {{ emp.full_name || emp.username }} ({{ emp.position || emp.role || 'Employee' }})
                  </option>
                </select>
              </div>
            </div>

            <!-- CLICKABLE STAT BADGES (ALL, PENDING, APPROVED, DENIED) -->
            <div style="display: flex; flex-wrap: wrap; gap: 0.85rem;">
              <!-- ALL OVERTIME BADGE -->
              <div 
                @click="overtimeStatusFilter = 'all'"
                :style="{
                  textAlign: 'right',
                  background: overtimeStatusFilter === 'all' ? 'rgba(56, 189, 248, 0.25)' : 'rgba(56, 189, 248, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: overtimeStatusFilter === 'all' ? '2px solid #38bdf8' : '1px solid rgba(56, 189, 248, 0.3)',
                  boxShadow: overtimeStatusFilter === 'all' ? '0 0 10px rgba(56, 189, 248, 0.4)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to show ALL overtime requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>⚡ All Overtime</span>
                  <span v-if="overtimeStatusFilter === 'all'" style="font-size: 0.6rem; background: #38bdf8; color: #0f172a; font-weight: 800; padding: 1px 4px; border-radius: 3px;">ALL</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #38bdf8;">{{ overtimeSummary.totalCount }} Requests ({{ overtimeSummary.totalOtHours }} hrs)</div>
              </div>

              <!-- PENDING BADGE (NORMAL AMBER) -->
              <div 
                @click="overtimeStatusFilter = 'Pending'"
                :style="{
                  textAlign: 'right',
                  background: overtimeStatusFilter === 'Pending' ? 'rgba(245, 158, 11, 0.35)' : 'rgba(245, 158, 11, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: overtimeStatusFilter === 'Pending' ? '2px solid #f59e0b' : '1px solid rgba(245, 158, 11, 0.3)',
                  boxShadow: overtimeStatusFilter === 'Pending' ? '0 0 12px rgba(245, 158, 11, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Pending overtime requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>⏳ Normal Pending</span>
                  <span v-if="overtimeStatusFilter === 'Pending'" style="font-size: 0.6rem; background: #f59e0b; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #f59e0b;">{{ overtimeSummary.pendingCount }} Pending</div>
              </div>

              <!-- APPROVED BADGE (COLOR GREEN) -->
              <div 
                @click="overtimeStatusFilter = 'Approved'"
                :style="{
                  textAlign: 'right',
                  background: overtimeStatusFilter === 'Approved' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: overtimeStatusFilter === 'Approved' ? '2px solid #10b981' : '1px solid rgba(16, 185, 129, 0.3)',
                  boxShadow: overtimeStatusFilter === 'Approved' ? '0 0 12px rgba(16, 185, 129, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Green Approved overtime requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🟢 Green Approved</span>
                  <span v-if="overtimeStatusFilter === 'Approved'" style="font-size: 0.6rem; background: #10b981; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #10b981;">{{ overtimeSummary.approvedCount }} Approved</div>
              </div>

              <!-- DENIED BADGE (COLOR RED) -->
              <div 
                @click="overtimeStatusFilter = 'Denied'"
                :style="{
                  textAlign: 'right',
                  background: overtimeStatusFilter === 'Denied' ? 'rgba(239, 68, 68, 0.35)' : 'rgba(239, 68, 68, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: overtimeStatusFilter === 'Denied' ? '2px solid #ef4444' : '1px solid rgba(239, 68, 68, 0.3)',
                  boxShadow: overtimeStatusFilter === 'Denied' ? '0 0 12px rgba(239, 68, 68, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Red Denied overtime requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🔴 Red Denied</span>
                  <span v-if="overtimeStatusFilter === 'Denied'" style="font-size: 0.6rem; background: #ef4444; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #ef4444;">{{ overtimeSummary.deniedCount }} Denied</div>
              </div>
            </div>
          </div>

          <!-- OVERTIME TABLE POPULATED PER USER -->
          <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                <span>📋</span> Overtime Filings per User
                <span v-if="overtimeStatusFilter !== 'all'" style="font-size: 0.78rem; background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.2rem 0.65rem; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.4); display: inline-flex; align-items: center; gap: 0.4rem;">
                  Filter: <strong>{{ overtimeStatusFilter }}</strong>
                  <button type="button" @click="overtimeStatusFilter = 'all'" style="background: rgba(239, 68, 68, 0.25); border: none; color: #fca5a5; cursor: pointer; font-weight: 800; padding: 1px 6px; border-radius: 4px; font-size: 0.72rem;">✕ Show All</button>
                </span>
              </h3>

              <!-- STATUS FILTER BUTTONS BAR -->
              <div style="display: flex; gap: 0.4rem; align-items: center; font-size: 0.78rem; flex-wrap: wrap;">
                <span @click="overtimeStatusFilter = 'all'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: overtimeStatusFilter === 'all' ? 'rgba(56, 189, 248, 0.35)' : 'rgba(56, 189, 248, 0.1)', color: '#38bdf8', fontWeight: '700', border: overtimeStatusFilter === 'all' ? '1px solid #38bdf8' : '1px solid transparent' }">⚡ All</span>
                <span @click="overtimeStatusFilter = 'Pending'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: overtimeStatusFilter === 'Pending' ? 'rgba(245, 158, 11, 0.35)' : 'rgba(245, 158, 11, 0.1)', color: '#f59e0b', fontWeight: '700', border: overtimeStatusFilter === 'Pending' ? '1px solid #f59e0b' : '1px solid transparent' }">⏳ Pending (Normal)</span>
                <span @click="overtimeStatusFilter = 'Approved'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: overtimeStatusFilter === 'Approved' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '700', border: overtimeStatusFilter === 'Approved' ? '1px solid #10b981' : '1px solid transparent' }">🟢 Approved (Green)</span>
                <span @click="overtimeStatusFilter = 'Denied'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: overtimeStatusFilter === 'Denied' ? 'rgba(239, 68, 68, 0.35)' : 'rgba(239, 68, 68, 0.1)', color: '#ef4444', fontWeight: '700', border: overtimeStatusFilter === 'Denied' ? '1px solid #ef4444' : '1px solid transparent' }">🔴 Denied (Red)</span>
              </div>
            </div>

            <!-- TABLE SCROLLABLE -->
            <div 
              class="table-responsive timesheet-drag-scroll" 
              @mousedown="onTableMouseDown"
              @mouseleave="onTableMouseLeave"
              @mouseup="onTableMouseUp"
              @mousemove="onTableMouseMove"
              style="max-height: 540px; overflow-y: auto; overflow-x: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); cursor: grab;"
            >
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Employee / User</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Date</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">OT Window & Hours</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Reason / Work Details</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Status</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Approver</th>
                    <th v-if="canApproveModule('overtime')" style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="log in filteredOvertimeLogs" 
                    :key="log.id"
                    :style="{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      fontSize: '0.88rem',
                      background: log.status === 'Approved' ? 'rgba(16, 185, 129, 0.12)' : (log.status === 'Denied' || log.status === 'Rejected' ? 'rgba(239, 68, 68, 0.1)' : 'transparent'),
                      borderLeft: log.status === 'Approved' ? '4px solid #10b981' : (log.status === 'Denied' || log.status === 'Rejected' ? '4px solid #ef4444' : '4px solid #f59e0b')
                    }"
                  >
                    <!-- EMPLOYEE / USER -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="font-weight: 700; color: #fff;">{{ log.employeeName }}</div>
                      <div style="font-size: 0.75rem; color: #94a3b8;">{{ log.department || 'Operations' }}</div>
                    </td>

                    <!-- DATE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; font-weight: 600; color: #60a5fa;">
                      📅 {{ log.dateRange }}
                    </td>

                    <!-- OT DETAILS & HOURS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="color: #a855f7; font-weight: 700;">{{ log.details }}</div>
                    </td>

                    <!-- REASON -->
                    <td style="padding: 0.85rem 1rem; color: #cbd5e1; font-size: 0.82rem; max-width: 240px;">
                      {{ log.reason }}
                    </td>

                    <!-- STATUS BADGE (GREEN APPROVED, RED DENIED, NORMAL PENDING) -->
                    <td style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <span 
                        v-if="log.status === 'Approved'" 
                        style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.82rem; display: inline-block;"
                      >
                        🟢 Approved
                      </span>
                      <span 
                        v-else-if="log.status === 'Denied' || log.status === 'Rejected'" 
                        style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.82rem; display: inline-block;"
                      >
                        🔴 Denied
                      </span>
                      <span 
                        v-else 
                        style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.82rem; display: inline-block;"
                      >
                        ⏳ Normal Pending
                      </span>
                    </td>

                    <!-- APPROVER DETAILS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; font-size: 0.8rem; color: #94a3b8;">
                      <div>{{ log.approver || '--' }}</div>
                      <div v-if="log.approverDate && log.approverDate !== '--'" style="font-size: 0.72rem; color: #64748b;">{{ log.approverDate }}</div>
                    </td>

                    <!-- ACTIONS: APPROVE (GREEN) / DENY (RED) -->
                    <td v-if="canApproveModule('overtime')" style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <div style="display: flex; gap: 0.4rem; justify-content: center;">
                        <button 
                          type="button"
                          @click="approveOvertimeRequest(log)"
                          :disabled="log.status === 'Approved'"
                          style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.3rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem; cursor: pointer;"
                          title="Approve Overtime (Green)"
                        >
                          ✅ Approve
                        </button>
                        <button 
                          type="button"
                          @click="denyOvertimeRequest(log)"
                          :disabled="log.status === 'Denied' || log.status === 'Rejected'"
                          style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.3rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem; cursor: pointer;"
                          title="Deny Overtime (Red)"
                        >
                          ❌ Deny
                        </button>
                      </div>
                    </td>
                  </tr>

                  <tr v-if="filteredOvertimeLogs.length === 0">
                    <td colspan="7" style="text-align: center; padding: 3.5rem 1.5rem; color: #94a3b8;">
                      <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                      <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.25rem;">
                        No overtime requests match filter "{{ overtimeStatusFilter }}"
                      </div>
                      <button type="button" class="btn btn-sm btn-primary" @click="overtimeStatusFilter = 'all'" style="margin-top: 0.75rem; padding: 0.45rem 1.1rem; border-radius: 8px; cursor: pointer; background: linear-gradient(135deg, #3b82f6, #6366f1); border: none; color: #fff; font-weight: 700;">
                        Show All Overtime Filings
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VIEW: ATTENDANCE - LEAVE -->
        <div v-else-if="activeView === 'attendance_leave'" class="page-view glass attendance-page-view">
          <div class="view-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="header-title-box">
              <h2 class="view-heading">🏖️ Employee Leave Management & Audit</h2>
              <p class="view-subheading">Populated leave requests per user (Sick Leave, Vacation Leave), approval status, and pending/approved/denied filtering</p>
            </div>
          </div>

          <!-- CONTROLS & STAT SUMMARY BADGES WITH CLICKABLE STATUS FILTERS -->
          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; background: rgba(15, 23, 42, 0.65); padding: 1.25rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.12); backdrop-filter: blur(12px);">
            
            <!-- EMPLOYEE SELECTOR -->
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 1rem;">
              <div>
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  👤 Select Employee / Driver
                </label>
                <select 
                  v-model="selectedLeaveEmployeeId" 
                  style="padding: 0.6rem 1rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600; min-width: 220px; cursor: pointer;"
                >
                  <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="emp.id">
                    {{ emp.full_name || emp.username }} ({{ emp.position || emp.role || 'Employee' }})
                  </option>
                </select>
              </div>
            </div>

            <!-- CLICKABLE STAT BADGES (ALL, PENDING, APPROVED, DENIED) -->
            <div style="display: flex; flex-wrap: wrap; gap: 0.85rem;">
              <!-- ALL LEAVE BADGE -->
              <div 
                @click="leaveStatusFilter = 'all'"
                :style="{
                  textAlign: 'right',
                  background: leaveStatusFilter === 'all' ? 'rgba(56, 189, 248, 0.25)' : 'rgba(56, 189, 248, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: leaveStatusFilter === 'all' ? '2px solid #38bdf8' : '1px solid rgba(56, 189, 248, 0.3)',
                  boxShadow: leaveStatusFilter === 'all' ? '0 0 10px rgba(56, 189, 248, 0.4)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to show ALL leave requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>⚡ All Leaves</span>
                  <span v-if="leaveStatusFilter === 'all'" style="font-size: 0.6rem; background: #38bdf8; color: #0f172a; font-weight: 800; padding: 1px 4px; border-radius: 3px;">ALL</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #38bdf8;">{{ leaveSummary.totalCount }} Requests ({{ leaveSummary.totalLeaveDays }} days)</div>
              </div>

              <!-- PENDING BADGE (NORMAL AMBER) -->
              <div 
                @click="leaveStatusFilter = 'Pending'"
                :style="{
                  textAlign: 'right',
                  background: leaveStatusFilter === 'Pending' ? 'rgba(245, 158, 11, 0.35)' : 'rgba(245, 158, 11, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: leaveStatusFilter === 'Pending' ? '2px solid #f59e0b' : '1px solid rgba(245, 158, 11, 0.3)',
                  boxShadow: leaveStatusFilter === 'Pending' ? '0 0 12px rgba(245, 158, 11, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Pending leave requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>⏳ Normal Pending</span>
                  <span v-if="leaveStatusFilter === 'Pending'" style="font-size: 0.6rem; background: #f59e0b; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #f59e0b;">{{ leaveSummary.pendingCount }} Pending</div>
              </div>

              <!-- APPROVED BADGE (COLOR GREEN) -->
              <div 
                @click="leaveStatusFilter = 'Approved'"
                :style="{
                  textAlign: 'right',
                  background: leaveStatusFilter === 'Approved' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: leaveStatusFilter === 'Approved' ? '2px solid #10b981' : '1px solid rgba(16, 185, 129, 0.3)',
                  boxShadow: leaveStatusFilter === 'Approved' ? '0 0 12px rgba(16, 185, 129, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Green Approved leave requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🟢 Green Approved</span>
                  <span v-if="leaveStatusFilter === 'Approved'" style="font-size: 0.6rem; background: #10b981; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #10b981;">{{ leaveSummary.approvedCount }} Approved</div>
              </div>

              <!-- DENIED BADGE (COLOR RED) -->
              <div 
                @click="leaveStatusFilter = 'Denied'"
                :style="{
                  textAlign: 'right',
                  background: leaveStatusFilter === 'Denied' ? 'rgba(239, 68, 68, 0.35)' : 'rgba(239, 68, 68, 0.1)',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '10px',
                  border: leaveStatusFilter === 'Denied' ? '2px solid #ef4444' : '1px solid rgba(239, 68, 68, 0.3)',
                  boxShadow: leaveStatusFilter === 'Denied' ? '0 0 12px rgba(239, 68, 68, 0.5)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  userSelect: 'none'
                }"
                title="Click to filter Red Denied leave requests"
              >
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
                  <span>🔴 Red Denied</span>
                  <span v-if="leaveStatusFilter === 'Denied'" style="font-size: 0.6rem; background: #ef4444; color: #fff; padding: 1px 4px; border-radius: 3px; font-weight: 800;">ACTIVE</span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #ef4444;">{{ leaveSummary.deniedCount }} Denied</div>
              </div>
            </div>
          </div>

          <!-- LEAVE TABLE POPULATED PER USER -->
          <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                <span>📋</span> Employee Leave Records per User
                <span v-if="leaveStatusFilter !== 'all'" style="font-size: 0.78rem; background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.2rem 0.65rem; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.4); display: inline-flex; align-items: center; gap: 0.4rem;">
                  Filter: <strong>{{ leaveStatusFilter }}</strong>
                  <button type="button" @click="leaveStatusFilter = 'all'" style="background: rgba(239, 68, 68, 0.25); border: none; color: #fca5a5; cursor: pointer; font-weight: 800; padding: 1px 6px; border-radius: 4px; font-size: 0.72rem;">✕ Show All</button>
                </span>
              </h3>

              <!-- STATUS FILTER BUTTONS BAR -->
              <div style="display: flex; gap: 0.4rem; align-items: center; font-size: 0.78rem; flex-wrap: wrap;">
                <span @click="leaveStatusFilter = 'all'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: leaveStatusFilter === 'all' ? 'rgba(56, 189, 248, 0.35)' : 'rgba(56, 189, 248, 0.1)', color: '#38bdf8', fontWeight: '700', border: leaveStatusFilter === 'all' ? '1px solid #38bdf8' : '1px solid transparent' }">⚡ All</span>
                <span @click="leaveStatusFilter = 'Pending'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: leaveStatusFilter === 'Pending' ? 'rgba(245, 158, 11, 0.35)' : 'rgba(245, 158, 11, 0.1)', color: '#f59e0b', fontWeight: '700', border: leaveStatusFilter === 'Pending' ? '1px solid #f59e0b' : '1px solid transparent' }">⏳ Pending (Normal)</span>
                <span @click="leaveStatusFilter = 'Approved'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: leaveStatusFilter === 'Approved' ? 'rgba(16, 185, 129, 0.35)' : 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '700', border: leaveStatusFilter === 'Approved' ? '1px solid #10b981' : '1px solid transparent' }">🟢 Approved (Green)</span>
                <span @click="leaveStatusFilter = 'Denied'" style="cursor: pointer; padding: 0.25rem 0.55rem; border-radius: 6px; user-select: none;" :style="{ background: leaveStatusFilter === 'Denied' ? 'rgba(239, 68, 68, 0.35)' : 'rgba(239, 68, 68, 0.1)', color: '#ef4444', fontWeight: '700', border: leaveStatusFilter === 'Denied' ? '1px solid #ef4444' : '1px solid transparent' }">🔴 Denied (Red)</span>
              </div>
            </div>

            <!-- TABLE SCROLLABLE -->
            <div 
              class="table-responsive timesheet-drag-scroll" 
              @mousedown="onTableMouseDown"
              @mouseleave="onTableMouseLeave"
              @mouseup="onTableMouseUp"
              @mousemove="onTableMouseMove"
              style="max-height: 540px; overflow-y: auto; overflow-x: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); cursor: grab;"
            >
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Employee / User</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Leave Type</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Date Range</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Reason / Details</th>
                    <th style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Status</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Approver</th>
                    <th v-if="canApproveModule('leave')" style="padding: 0.85rem 1rem; text-align: center; position: sticky; top: 0; background: #0f172a; z-index: 5;">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="log in filteredLeaveLogs" 
                    :key="log.id"
                    :style="{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      fontSize: '0.88rem',
                      background: log.status === 'Approved' ? 'rgba(16, 185, 129, 0.12)' : (log.status === 'Denied' || log.status === 'Rejected' ? 'rgba(239, 68, 68, 0.1)' : 'transparent'),
                      borderLeft: log.status === 'Approved' ? '4px solid #10b981' : (log.status === 'Denied' || log.status === 'Rejected' ? '4px solid #ef4444' : '4px solid #f59e0b')
                    }"
                  >
                    <!-- EMPLOYEE / USER -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="font-weight: 700; color: #fff;">{{ log.employeeName }}</div>
                      <div style="font-size: 0.75rem; color: #94a3b8;">{{ log.department || 'Operations' }}</div>
                    </td>

                    <!-- LEAVE TYPE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; font-weight: 700; color: #10b981;">
                      🏖️ {{ log.details }}
                    </td>

                    <!-- DATE RANGE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; font-weight: 600; color: #60a5fa;">
                      📅 {{ log.dateRange }}
                    </td>

                    <!-- REASON -->
                    <td style="padding: 0.85rem 1rem; color: #cbd5e1; font-size: 0.82rem; max-width: 260px;">
                      {{ log.reason }}
                    </td>

                    <!-- STATUS BADGE (GREEN APPROVED, RED DENIED, NORMAL PENDING) -->
                    <td style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <span 
                        v-if="log.status === 'Approved'" 
                        style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.82rem; display: inline-block;"
                      >
                        🟢 Approved
                      </span>
                      <span 
                        v-else-if="log.status === 'Denied' || log.status === 'Rejected'" 
                        style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.82rem; display: inline-block;"
                      >
                        🔴 Denied
                      </span>
                      <span 
                        v-else 
                        style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.82rem; display: inline-block;"
                      >
                        ⏳ Normal Pending
                      </span>
                    </td>

                    <!-- APPROVER DETAILS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; font-size: 0.8rem; color: #94a3b8;">
                      <div>{{ log.approver || '--' }}</div>
                      <div v-if="log.approverDate && log.approverDate !== '--'" style="font-size: 0.72rem; color: #64748b;">{{ log.approverDate }}</div>
                    </td>

                    <!-- ACTIONS: APPROVE (GREEN) / DENY (RED) -->
                    <td v-if="canApproveModule('leave')" style="padding: 0.85rem 1rem; text-align: center; white-space: nowrap;">
                      <div style="display: flex; gap: 0.4rem; justify-content: center;">
                        <button 
                          type="button"
                          @click="approveLeaveRequest(log)"
                          :disabled="log.status === 'Approved'"
                          style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.3rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem; cursor: pointer;"
                          title="Approve Leave (Green)"
                        >
                          ✅ Approve
                        </button>
                        <button 
                          type="button"
                          @click="denyLeaveRequest(log)"
                          :disabled="log.status === 'Denied' || log.status === 'Rejected'"
                          style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.3rem 0.6rem; border-radius: 6px; font-weight: 700; font-size: 0.75rem; cursor: pointer;"
                          title="Deny Leave (Red)"
                        >
                          ❌ Deny
                        </button>
                      </div>
                    </td>
                  </tr>

                  <tr v-if="filteredLeaveLogs.length === 0">
                    <td colspan="7" style="text-align: center; padding: 3.5rem 1.5rem; color: #94a3b8;">
                      <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                      <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.25rem;">
                        No leave requests match filter "{{ leaveStatusFilter }}"
                      </div>
                      <button type="button" class="btn btn-sm btn-primary" @click="leaveStatusFilter = 'all'" style="margin-top: 0.75rem; padding: 0.45rem 1.1rem; border-radius: 8px; cursor: pointer; background: linear-gradient(135deg, #3b82f6, #6366f1); border: none; color: #fff; font-weight: 700;">
                        Show All Leave Filings
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>



        <!-- VIEW: ATTENDANCE - CALENDAR & HOLIDAYS -->
        <div v-else-if="activeView === 'attendance_holiday'" class="page-view glass attendance-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">📅 Attendance & Holiday Calendar</h2>
              <p class="view-subheading">Monthly visual attendance tracking calendar with status, time in, time out, and Philippine holidays</p>
            </div>
          </div>

          <!-- VISUAL CALENDAR WIDGET WITH ATTENDANCE STATUS & TIMESTAMPS -->
          <div class="calendar-widget-section glass" style="padding: 2rem; border-radius: 16px; margin-bottom: 2rem; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.1);">
            <!-- CALENDAR HEADER & MONTH NAVIGATOR -->
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
              <div>
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                  📅 Attendance & Holidays Calendar ({{ calendarYear }})
                </h3>
                <p style="font-size: 0.85rem; color: #94a3b8;">
                  Shows daily attendance status, time in, time out, and Philippine holidays. Click any date to configure a holiday.
                </p>
              </div>

              <!-- MONTH NAVIGATION -->
              <div style="display: flex; align-items: center; gap: 0.75rem; background: rgba(30, 41, 59, 0.8); padding: 0.4rem 0.8rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.15);">
                <button type="button" @click="prevCalendarMonth" class="btn btn-ghost btn-xs" style="color: #60a5fa; font-weight: 700; font-size: 1rem; padding: 0.2rem 0.6rem; cursor: pointer;" title="Previous Month">
                  ◀
                </button>
                <span style="font-weight: 700; color: #fff; min-width: 140px; text-align: center; font-size: 0.95rem;">
                  {{ monthNames[calendarMonth] }} {{ calendarYear }}
                </span>
                <button type="button" @click="nextCalendarMonth" class="btn btn-ghost btn-xs" style="color: #60a5fa; font-weight: 700; font-size: 1rem; padding: 0.2rem 0.6rem; cursor: pointer;" title="Next Month">
                  ▶
                </button>
              </div>
            </div>

            <!-- ATTENDANCE & HOLIDAY STATUS LEGEND BAR -->
            <div style="display: flex; flex-wrap: wrap; gap: 1.25rem; margin-bottom: 1.25rem; padding: 0.75rem 1rem; background: rgba(30, 41, 59, 0.4); border-radius: 10px; font-size: 0.82rem;">
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: #10b981;"></span>
                <span style="color: #10b981; font-weight: 700;">🟢 Present</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: #f59e0b;"></span>
                <span style="color: #f59e0b; font-weight: 700;">🟠 Late</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: #3b82f6;"></span>
                <span style="color: #3b82f6; font-weight: 700;">🔵 Early Out</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: #ef4444;"></span>
                <span style="color: #ef4444; font-weight: 700;">🔴 Absent</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 10px; height: 10px; border-radius: 3px; background: rgba(16, 185, 129, 0.8);"></span>
                <span style="color: #10b981; font-weight: 700;">🎉 Holiday</span>
              </div>
            </div>

            <!-- CALENDAR GRID CONTAINER -->
            <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.5rem; text-align: center;">
              <!-- WEEKDAY HEADERS -->
              <div v-for="dayName in ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']" :key="dayName" style="padding: 0.5rem 0; font-size: 0.75rem; font-weight: 700; color: #94a3b8; letter-spacing: 0.5px;">
                {{ dayName }}
              </div>

              <!-- CALENDAR DAYS -->
              <div 
                v-for="(item, idx) in calendarDays" 
                :key="idx" 
                @click="item.day && selectCalendarDate(item.dateStr)"
                :style="getDayStyle(item)"
              >
                <template v-if="item.day">
                  <!-- TOP CELL ROW: DAY NUMBER + STATUS BADGE -->
                  <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 0.25rem;">
                    <span :style="{ fontSize: '0.85rem', fontWeight: '800', color: item.color || '#fff' }">
                      {{ item.day }}
                    </span>
                    <span 
                      :style="{
                        fontSize: '0.62rem',
                        fontWeight: '700',
                        padding: '0.12rem 0.35rem',
                        borderRadius: '4px',
                        background: item.bg,
                        color: item.color,
                        border: item.border
                      }"
                    >
                      {{ item.statusText }}
                    </span>
                  </div>
                  
                  <!-- CELL DETAILS: HOLIDAY NAME OR TIME IN / TIME OUT -->
                  <div style="width: 100%; display: flex; flex-direction: column; gap: 0.15rem; font-size: 0.66rem; text-align: left;">
                    <span 
                      v-if="item.holiday" 
                      style="color: #10b981; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
                      :title="item.holiday.name"
                    >
                      🎉 {{ item.holiday.name }}
                    </span>
                    <template v-else-if="!item.isWeekend">
                      <span v-if="item.timeIn && item.timeIn !== '--:--'" style="color: #10b981; font-weight: 600;">
                        🟢 In: {{ item.timeIn }}
                      </span>
                      <span v-if="item.timeOut && item.timeOut !== '--:--'" style="color: #f43f5e; font-weight: 600;">
                        🔴 Out: {{ item.timeOut }}
                      </span>
                      <span v-if="(!item.timeIn || item.timeIn === '--:--') && (!item.timeOut || item.timeOut === '--:--')" style="color: #ef4444; font-weight: 600; font-size: 0.62rem;">
                        No Time Log
                      </span>
                    </template>
                  </div>
                </template>
              </div>
            </div>
          </div>

          <!-- ASSIGN / ADD HOLIDAY FORM CARD -->
          <div v-if="canAccessMenu('attendance_approver')" class="schedule-form-section glass" style="padding: 2rem; border-radius: 16px; margin-bottom: 2rem; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.1);">
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;">
              <span>📅🎉</span> {{ editingHolidayId ? 'Edit Holiday' : 'Add New Holiday' }}
            </h3>

            <form @submit.prevent="submitHoliday" autocomplete="off">
              <div class="form-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; align-items: end;">
                
                <!-- HOLIDAY CALENDAR / DATE -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Holiday Date *</label>
                  <input 
                    type="date" 
                    v-model="holidayForm.date" 
                    required 
                    class="form-input" 
                    style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;"
                  />
                </div>

                <!-- HOLIDAY NAME -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Holiday Name *</label>
                  <input 
                    type="text" 
                    v-model="holidayForm.name" 
                    required 
                    placeholder="e.g. Independence Day" 
                    class="form-input" 
                    style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;"
                  />
                </div>

                <!-- HOLIDAY TYPE -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Holiday Type *</label>
                  <div class="select-wrapper">
                    <select v-model="holidayForm.type" required class="form-select select-input" style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
                      <option value="Regular Holiday">Regular Holiday</option>
                      <option value="Special Working Holiday">Special Working Holiday</option>
                      <option value="Special Non-Working Holiday">Special Non-Working Holiday</option>
                    </select>
                  </div>
                </div>

              </div>

              <div style="margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button v-if="editingHolidayId" type="button" class="btn btn-ghost" @click="cancelEditHoliday" style="padding: 0.75rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer;">
                  Cancel Edit
                </button>
                <button type="submit" class="btn btn-primary" style="padding: 0.75rem 1.75rem; border-radius: 10px; font-weight: 600; cursor: pointer;">
                  {{ editingHolidayId ? '✏️ Update Holiday' : '💾 Save Holiday' }}
                </button>
              </div>

              <!-- FEEDBACK ALERTS -->
              <div v-if="holidaySuccess" class="alert alert-success mt-2" style="margin-top: 1rem;">{{ holidaySuccess }}</div>
              <div v-if="holidayError" class="alert alert-error mt-2" style="margin-top: 1rem;">{{ holidayError }}</div>
            </form>
          </div>

          <!-- ASSIGNED HOLIDAYS TABLE -->
          <div class="table-container glass" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff;">📋 Configured Holiday Calendar</h3>
              <span class="item-badge" style="background: rgba(236, 72, 153, 0.2); color: #f472b6; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                {{ assignedHolidays.length }} Holidays
              </span>
            </div>

            <div class="table-responsive">
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); text-align: left; font-size: 0.85rem; color: #94a3b8;">
                    <th style="padding: 0.85rem 1rem;">Date</th>
                    <th style="padding: 0.85rem 1rem;">Holiday Name</th>
                    <th style="padding: 0.85rem 1rem;">Type</th>
                    <th style="padding: 0.85rem 1rem;">Status</th>
                    <th v-if="canAccessMenu('attendance_approver')" style="padding: 0.85rem 1rem; text-align: center;">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="h in assignedHolidays" :key="h.id" style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem;">
                    <td style="padding: 1rem; white-space: nowrap;">
                      <span style="font-weight: 600; color: #38bdf8;">📅 {{ formatDate(h.date) }}</span>
                    </td>
                    <td style="padding: 1rem; font-weight: 600; color: #fff;">{{ h.name }}</td>
                    <td style="padding: 1rem;">
                      <span 
                        :style="{
                          padding: '0.35rem 0.65rem',
                          borderRadius: '6px',
                          fontSize: '0.8rem',
                          fontWeight: '700',
                          background: h.type === 'Regular Holiday' ? 'rgba(168, 85, 247, 0.2)' : (h.type === 'Special Non-Working Holiday' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)'),
                          color: h.type === 'Regular Holiday' ? '#c084fc' : (h.type === 'Special Non-Working Holiday' ? '#f87171' : '#fbbf24')
                        }"
                      >
                        {{ h.type }}
                      </span>
                    </td>
                    <td style="padding: 1rem;">
                      <span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                        {{ h.status || 'Active' }}
                      </span>
                    </td>
                    <td v-if="canAccessMenu('attendance_approver')" style="padding: 1rem; text-align: center; white-space: nowrap;">
                      <button type="button" class="btn btn-ghost btn-sm" @click="editHoliday(h)" style="color: #3b82f6; padding: 0.35rem 0.65rem; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.3); background: rgba(59, 130, 246, 0.1); cursor: pointer; margin-right: 0.4rem;" title="Edit Holiday">
                        ✏️
                      </button>
                      <button type="button" class="btn btn-ghost btn-sm" @click="removeHoliday(h.id)" style="color: #ef4444; padding: 0.35rem 0.65rem; border-radius: 6px; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.1); cursor: pointer;" title="Remove Holiday">
                        🗑️
                      </button>
                    </td>
                  </tr>
                  <tr v-if="assignedHolidays.length === 0">
                    <td :colspan="canAccessMenu('attendance_approver') ? 5 : 4" style="text-align: center; padding: 2rem; color: #94a3b8;">
                      No holiday schedules configured yet. Use the form above to add a holiday.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VIEW: PAYROLL - WORKING SCHEDULE -->
        <div v-else-if="activeView === 'payroll_schedule'" class="page-view glass payroll-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">📅 Working Schedule</h2>
              <p class="view-subheading">Configure employee shift schedules, working hours, and shift assignments</p>
            </div>
          </div>

          <!-- ASSIGN WORKING SCHEDULE FORM CARD -->
          <div class="schedule-form-section glass" style="padding: 2rem; border-radius: 16px; margin-bottom: 2rem; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.1);">
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;">
              <span>👤⏰</span> Assign Employee Schedule
            </h3>

            <form @submit.prevent="submitWorkingSchedule" autocomplete="off">
              <div class="form-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; align-items: end;">
                
                <!-- DROPDOWN EMPLOYEES -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Select Employee *</label>
                  <div class="select-wrapper">
                    <select v-model="scheduleForm.employee_id" required class="form-select select-input" style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
                      <option value="" disabled>Select an Employee</option>
                      <option v-for="u in availableEmployeeOptions" :key="u.id" :value="u.id">
                        {{ u.full_name || (u.first_name ? u.first_name + ' ' + u.last_name : u.username) }} (@{{ u.username }}) - {{ u.position || u.role }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- TIME FROM -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Time From *</label>
                  <input 
                    type="time" 
                    v-model="scheduleForm.time_from" 
                    required 
                    class="form-input" 
                    style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;"
                  />
                </div>

                <!-- TIME TO -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Time To *</label>
                  <input 
                    type="time" 
                    v-model="scheduleForm.time_to" 
                    required 
                    class="form-input" 
                    style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;"
                  />
                </div>



              </div>

              <div style="margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button v-if="editingScheduleId" type="button" class="btn btn-ghost" @click="cancelEditSchedule" style="padding: 0.75rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer;">
                  Cancel Edit
                </button>
                <button type="submit" class="btn btn-primary" style="padding: 0.75rem 1.75rem; border-radius: 10px; font-weight: 600; cursor: pointer;">
                  {{ editingScheduleId ? '✏️ Update Schedule' : '💾 Save Schedule' }}
                </button>
              </div>

              <!-- FEEDBACK ALERTS -->
              <div v-if="scheduleSuccess" class="alert alert-success mt-2" style="margin-top: 1rem;">{{ scheduleSuccess }}</div>
              <div v-if="scheduleError" class="alert alert-error mt-2" style="margin-top: 1rem;">{{ scheduleError }}</div>
            </form>
          </div>

          <!-- ASSIGNED WORKING SCHEDULES TABLE -->
          <div class="table-container glass" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff;">📋 Assigned Employee Schedules</h3>
              <span class="item-badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                {{ assignedSchedules.length }} Schedules
              </span>
            </div>

            <div class="table-responsive">
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); text-align: left; font-size: 0.85rem; color: #94a3b8;">
                    <th style="padding: 0.85rem 1rem;">Employee</th>
                    <th style="padding: 0.85rem 1rem;">Position / Role</th>
                    <th style="padding: 0.85rem 1rem;">Time From</th>
                    <th style="padding: 0.85rem 1rem;">Time To</th>
                    <th style="padding: 0.85rem 1rem;">Status</th>
                    <th v-if="canAccessMenu('payroll_approver')" style="padding: 0.85rem 1rem; text-align: center;">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="sched in assignedSchedules" :key="sched.id" style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem;">
                    <td style="padding: 1rem;">
                      <div style="font-weight: 600; color: #fff;">{{ sched.employee_name }}</div>
                      <div style="font-size: 0.8rem; color: #94a3b8;">@{{ sched.username }}</div>
                    </td>
                    <td style="padding: 1rem; color: #cbd5e1;">{{ sched.position }}</td>
                    <td style="padding: 1rem;"><span style="background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 0.35rem 0.65rem; border-radius: 6px; font-weight: 600;">{{ sched.time_from }}</span></td>
                    <td style="padding: 1rem;"><span style="background: rgba(239, 68, 68, 0.15); color: #f87171; padding: 0.35rem 0.65rem; border-radius: 6px; font-weight: 600;">{{ sched.time_to }}</span></td>
                    <td style="padding: 1rem;">
                      <span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                        {{ sched.status }}
                      </span>
                    </td>
                    <td v-if="canAccessMenu('payroll_approver')" style="padding: 1rem; text-align: center; white-space: nowrap;">
                      <button type="button" class="btn btn-ghost btn-sm" @click="editSchedule(sched)" style="color: #3b82f6; padding: 0.35rem 0.65rem; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.3); background: rgba(59, 130, 246, 0.1); cursor: pointer; margin-right: 0.4rem;" title="Edit Schedule">
                        ✏️
                      </button>
                      <button type="button" class="btn btn-ghost btn-sm" @click="removeSchedule(sched.id)" style="color: #ef4444; padding: 0.35rem 0.65rem; border-radius: 6px; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.1); cursor: pointer;" title="Remove Schedule">
                        🗑️
                      </button>
                    </td>
                  </tr>
                  <tr v-if="assignedSchedules.length === 0">
                    <td :colspan="canAccessMenu('payroll_approver') ? 6 : 5" style="text-align: center; padding: 2rem; color: #94a3b8;">
                      No working schedules assigned yet. Use the form above to assign a schedule.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VIEW: PAYROLL - SALARY -->
        <div v-else-if="activeView === 'payroll_salary'" class="page-view glass payroll-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">💰 Salary</h2>
              <p class="view-subheading">Manage employee base salary structure, rates, and compensation setup</p>
            </div>
          </div>

          <!-- ASSIGN EMPLOYEE SALARY FORM CARD -->
          <div class="schedule-form-section glass" style="padding: 2rem; border-radius: 16px; margin-bottom: 2rem; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.1);">
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;">
              <span>👤💰</span> Assign Employee Salary
            </h3>

            <form @submit.prevent="submitSalary" autocomplete="off">
              <div class="form-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; align-items: end;">
                
                <!-- DROPDOWN EMPLOYEES -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Select Employee *</label>
                  <div class="select-wrapper">
                    <select v-model="salaryForm.employee_id" required class="form-select select-input" style="width: 100%; padding: 0.75rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
                      <option value="" disabled>Select an Employee</option>
                      <option v-for="u in availableSalaryEmployeeOptions" :key="u.id" :value="u.id">
                        {{ u.full_name || (u.first_name ? u.first_name + ' ' + u.last_name : u.username) }} (@{{ u.username }}) - {{ u.position || u.role }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- SALARY AMOUNT (₱) -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">Salary Amount (₱) *</label>
                  <div style="position: relative;">
                    <span style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: #64748b; font-weight: 600;">₱</span>
                    <input 
                      type="number" 
                      step="0.01" 
                      min="0" 
                      v-model.number="salaryForm.salary_amount" 
                      required 
                      placeholder="e.g. 25000.00" 
                      class="form-input" 
                      style="width: 100%; padding: 0.75rem 1rem 0.75rem 2.2rem; border-radius: 10px; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.15); color: #fff;"
                    />
                  </div>
                </div>

              </div>

              <div style="margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button v-if="editingSalaryId" type="button" class="btn btn-ghost" @click="cancelEditSalary" style="padding: 0.75rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer;">
                  Cancel Edit
                </button>
                <button type="submit" class="btn btn-primary" style="padding: 0.75rem 1.75rem; border-radius: 10px; font-weight: 600; cursor: pointer;">
                  {{ editingSalaryId ? '✏️ Update Salary' : '💾 Save Salary' }}
                </button>
              </div>

              <!-- FEEDBACK ALERTS -->
              <div v-if="salarySuccess" class="alert alert-success mt-2" style="margin-top: 1rem;">{{ salarySuccess }}</div>
              <div v-if="salaryError" class="alert alert-error mt-2" style="margin-top: 1rem;">{{ salaryError }}</div>
            </form>
          </div>

          <!-- ASSIGNED EMPLOYEE SALARIES TABLE -->
          <div class="table-container glass" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff;">📋 Employee Salary Records</h3>
              <span class="item-badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                {{ assignedSalaries.length }} Records
              </span>
            </div>

            <div class="table-responsive">
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); text-align: left; font-size: 0.85rem; color: #94a3b8;">
                    <th style="padding: 0.85rem 1rem;">Employee</th>
                    <th style="padding: 0.85rem 1rem;">Position / Role</th>
                    <th style="padding: 0.85rem 1rem;">Base Salary</th>
                    <th style="padding: 0.85rem 1rem;">Status</th>
                    <th v-if="canAccessMenu('payroll_approver')" style="padding: 0.85rem 1rem; text-align: center;">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="sal in assignedSalaries" :key="sal.id" style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem;">
                    <td style="padding: 1rem;">
                      <div style="font-weight: 600; color: #fff;">{{ sal.employee_name }}</div>
                      <div style="font-size: 0.8rem; color: #94a3b8;">@{{ sal.username }}</div>
                    </td>
                    <td style="padding: 1rem; color: #cbd5e1;">{{ sal.position }}</td>
                    <td style="padding: 1rem;">
                      <span style="background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 0.35rem 0.65rem; border-radius: 6px; font-weight: 700; font-family: monospace;">
                        ₱{{ (sal.salary_amount || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                      </span>
                    </td>
                    <td style="padding: 1rem;">
                      <span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                        {{ sal.status }}
                      </span>
                    </td>
                    <td v-if="canAccessMenu('payroll_approver')" style="padding: 1rem; text-align: center; white-space: nowrap;">
                      <button type="button" class="btn btn-ghost btn-sm" @click="editSalary(sal)" style="color: #3b82f6; padding: 0.35rem 0.65rem; border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.3); background: rgba(59, 130, 246, 0.1); cursor: pointer; margin-right: 0.4rem;" title="Edit Salary">
                        ✏️
                      </button>
                      <button type="button" class="btn btn-ghost btn-sm" @click="removeSalary(sal.id)" style="color: #ef4444; padding: 0.35rem 0.65rem; border-radius: 6px; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.1); cursor: pointer;" title="Remove Salary">
                        🗑️
                      </button>
                    </td>
                  </tr>
                  <tr v-if="assignedSalaries.length === 0">
                    <td :colspan="canAccessMenu('payroll_approver') ? 5 : 4" style="text-align: center; padding: 2rem; color: #94a3b8;">
                      No employee salary records found. Use the form above to assign a salary.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VIEW: PAYROLL - LEAVE BALANCES & CREDITS -->
        <div v-else-if="activeView === 'payroll_leave'" class="page-view glass payroll-page-view">
          <div class="view-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="header-title-box">
              <h2 class="view-heading">🏖️ Payroll Leave & Accrual Balances</h2>
              <p class="view-subheading">Employee annual leave allocations, monthly accrual rate, approved leave taken, and available leave credits</p>
            </div>

            <!-- EMPLOYEE SELECTOR DROPDOWN -->
            <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
              <label style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">
                👤 Select Employee:
              </label>
              <select 
                v-model="selectedPayrollLeaveEmployeeId"
                style="padding: 0.6rem 1rem; border-radius: 10px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600; min-width: 240px; cursor: pointer;"
              >
                <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="emp.id">
                  {{ emp.full_name || emp.username }} ({{ emp.position || emp.role || 'Employee' }})
                </option>
              </select>
            </div>
          </div>

          <!-- SUMMARY METRIC CARDS FOR SELECTED EMPLOYEE / OVERVIEW -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(56, 189, 248, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">📅</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Annual Total Set</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #38bdf8;">{{ selectedEmployeeLeaveMetrics.totalSet }} Days/Yr</div>
                <div style="font-size: 0.72rem; color: #64748b;">(Accrual: +{{ selectedEmployeeLeaveMetrics.monthlyIncrement }} Days/Mo)</div>
              </div>
            </div>

            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(168, 85, 247, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">📈</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Accrued YTD ({{ currentMonthName }} {{ currentYear }})</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #c084fc;">{{ selectedEmployeeLeaveMetrics.accruedYTD }} Days</div>
                <div style="font-size: 0.72rem; color: #a78bfa;">{{ selectedEmployeeLeaveMetrics.accruedNote || `${currentMonthIndex}/12 Months` }}</div>
              </div>
            </div>

            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(239, 68, 68, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">🏖️</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Approved Leave Taken</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #f87171;">{{ selectedEmployeeLeaveMetrics.approvedUsedYTD }} Days</div>
                <div style="font-size: 0.72rem; color: #64748b;">Taken in {{ currentYear }}</div>
              </div>
            </div>

            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(16, 185, 129, 0.3); display: flex; align-items: center; gap: 1rem; box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(16, 185, 129, 0.2); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">🟢</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Available Leave Balance</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #10b981;">{{ selectedEmployeeLeaveMetrics.availableLeave }} Days</div>
                <div style="font-size: 0.72rem; color: #34d399;">(Accrued - Approved Taken)</div>
              </div>
            </div>

            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 46px; height: 46px; border-radius: 10px; background: rgba(245, 158, 11, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">📜</div>
              <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Last Year Record ({{ currentYear - 1 }})</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #f59e0b;">{{ selectedEmployeeLeaveMetrics.priorYearRemaining }} Days</div>
                <div style="font-size: 0.72rem; color: #64748b;">Saved Remaining Balance</div>
              </div>
            </div>
          </div>

          <!-- ALL EMPLOYEES LEAVE CREDIT BALANCES TABLE -->
          <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                <span>📋</span> Employee Payroll Leave Summary & Accruals Table
              </h3>
              <span style="font-size: 0.8rem; color: #94a3b8;">
                Accrual Rule: If created in current year, Accrued YTD = (Current Month - Creation Month) × (Total Set / 12); else Accrued YTD = Current Month × (Total Set / 12)
              </span>
            </div>

            <div class="table-responsive" style="max-height: 520px; overflow-y: auto; overflow-x: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Employee</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Position / Department</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Total Set (Annual)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Monthly Increment</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Accrued YTD</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Approved Taken</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Available Leave</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Last Year Record ({{ currentYear - 1 }})</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="row in employeePayrollLeaveTable" 
                    :key="row.employeeId"
                    :style="{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      fontSize: '0.88rem',
                      background: selectedPayrollLeaveEmployeeId !== 'all' && String(selectedPayrollLeaveEmployeeId) === String(row.employeeId) ? 'rgba(56, 189, 248, 0.15)' : 'transparent'
                    }"
                  >
                    <!-- EMPLOYEE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="font-weight: 700; color: #fff;">{{ row.employeeName }}</div>
                      <div style="font-size: 0.75rem; color: #94a3b8;">@{{ row.username }}</div>
                    </td>

                    <!-- POSITION / DEPT -->
                    <td style="padding: 0.85rem 1rem; color: #cbd5e1; white-space: nowrap;">
                      {{ row.position }}
                    </td>

                    <!-- TOTAL SET (ANNUAL) -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <span style="font-weight: 700; color: #38bdf8;">{{ row.totalSet }} Days</span>
                    </td>

                    <!-- MONTHLY INCREMENT (SET / 12) -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #a855f7; font-weight: 600;">
                      +{{ row.monthlyIncrement }} Days/Mo
                    </td>

                    <!-- ACCRUED YTD -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="color: #c084fc; font-weight: 700;">{{ row.accruedYTD }} Days</div>
                      <div style="font-size: 0.72rem; color: #94a3b8;">{{ row.accruedNote }}</div>
                    </td>

                    <!-- APPROVED TAKEN -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #f87171; font-weight: 700;">
                      {{ row.approvedUsedYTD }} Days
                    </td>

                    <!-- AVAILABLE LEAVE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.88rem; display: inline-block;">
                        🟢 {{ row.availableLeave }} Available Days
                      </span>
                    </td>

                    <!-- LAST YEAR RECORD -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #f59e0b; font-weight: 600; font-size: 0.82rem;">
                      📜 {{ row.priorYearRemaining }} Days Remaining
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- VIEW: PAYROLL - GENERATE PAYROLL -->
        <div v-else-if="activeView === 'payroll_generate'" class="page-view glass payroll-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">⚡ Generate & Compute Payroll</h2>
              <p class="view-subheading">Semi-monthly (1st & 2nd Period) payroll processing with automated daily/minute rate deductions for tardiness & early out</p>
            </div>
          </div>

          <!-- GLOBAL SUCCESS ALERT -->
          <div v-if="payrollProcessSuccess" style="margin-bottom: 1.25rem; padding: 1rem 1.25rem; background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; color: #34d399; font-weight: 600; font-size: 0.92rem; display: flex; align-items: center; gap: 0.75rem;">
            <span>✅</span> {{ payrollProcessSuccess }}
          </div>

          <!-- CONTROLS & FILTER BAR -->
          <div class="glass-card" style="padding: 1.25rem 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;">
            <!-- DROPDOWNS ROW -->
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1.25rem; margin-bottom: 1rem;">
              
              <!-- SELECT YEAR DROPDOWN -->
              <div style="flex: 1; min-width: 140px; max-width: 180px;">
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  📅 Select Year
                </label>
                <select v-model="selectedPayrollYear" style="width: 100%; padding: 0.65rem 1rem; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: #fff; font-weight: 700; font-size: 0.9rem; cursor: pointer;">
                  <option v-for="yr in yearOptions" :key="yr" :value="yr">
                    Year {{ yr }}
                  </option>
                </select>
              </div>

              <!-- SELECT PERIOD DROPDOWN -->
              <div style="flex: 2; min-width: 280px;">
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  📆 Select Salary Period (Jan to Dec)
                </label>
                <select v-model="selectedPayrollPeriodKey" style="width: 100%; padding: 0.65rem 1rem; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: #fff; font-weight: 600; font-size: 0.9rem; cursor: pointer;">
                  <option v-for="p in payrollPeriodOptions" :key="p.key" :value="p.key">
                    {{ p.label }}
                  </option>
                </select>
              </div>

              <!-- SELECT EMPLOYEE DROPDOWN -->
              <div style="flex: 1.5; min-width: 240px;">
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  👤 Select Employee
                </label>
                <select v-model="selectedPayrollGenerateEmployeeId" style="width: 100%; padding: 0.65rem 1rem; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: #fff; font-weight: 600; font-size: 0.9rem; cursor: pointer;">
                  <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="emp.id">
                    {{ emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username) }} (@{{ emp.username }})
                  </option>
                </select>
              </div>

              <!-- PERIOD COVERAGE BADGE -->
              <div style="padding: 0.75rem 1.25rem; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; text-align: right;">
                <div style="font-size: 0.72rem; color: #38bdf8; font-weight: 700; text-transform: uppercase;">Period Date Span</div>
                <div style="font-size: 0.95rem; font-weight: 800; color: #fff;">{{ currentSelectedPeriodInfo.start }} to {{ currentSelectedPeriodInfo.end }}</div>
                <div style="font-size: 0.72rem; color: #94a3b8;">{{ selectedEmployeePayrollDetails?.workingDaysInPeriod }} Working Days Span (Includes Weekday Holidays)</div>
              </div>

            </div>

            <!-- ACTION BUTTONS ROW (BELOW DROPDOWNS INSIDE THE CARD - INLINE) -->
            <div style="display: flex; justify-content: flex-end; align-items: center; gap: 0.75rem; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 1rem; flex-wrap: nowrap;">
              <button v-if="canAccessMenu('payroll_approver')" @click="processPayrollRun" type="button" class="btn btn-primary" style="padding: 0.65rem 1.6rem; font-weight: 700; border-radius: 10px; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); cursor: pointer; white-space: nowrap;">
                <span>⚡ Process & Disburse Payslip</span>
              </button>
              <button @click="downloadPayslipPDF(selectedEmployeePayrollDetails)" type="button" class="btn btn-secondary" style="padding: 0.65rem 1.35rem; font-weight: 700; border-radius: 10px; display: inline-flex; align-items: center; gap: 0.5rem; background: linear-gradient(135deg, #0284c7, #0369a1); border: none; color: #fff; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3); cursor: pointer; white-space: nowrap;">
                <span>📥 Download PDF Payslip</span>
              </button>
            </div>
          </div>

          <!-- SUMMARY METRICS CARDS -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            
            <!-- MONTHLY SALARY -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(56, 189, 248, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">💵</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Monthly Salary</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #38bdf8;">₱{{ selectedEmployeePayrollDetails.monthlySalary.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}</div>
                <div style="font-size: 0.7rem; color: #64748b;">Standard 22 Days/Mo</div>
              </div>
            </div>

            <!-- DAILY & MINUTE RATE -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(168, 85, 247, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">⏱️</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Daily / Minute Rate</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #c084fc;">₱{{ selectedEmployeePayrollDetails.dailyRate.toFixed(2) }} <span style="font-size: 0.72rem; color: #94a3b8;">/day</span></div>
                <div style="font-size: 0.7rem; color: #a78bfa;">₱{{ selectedEmployeePayrollDetails.minuteRate.toFixed(4) }} / min</div>
              </div>
            </div>

            <!-- PERIOD BASE GROSS -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(245, 158, 11, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">📈</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Period Base Gross</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #f59e0b;">₱{{ selectedEmployeePayrollDetails.periodBaseGross.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}</div>
                <div style="font-size: 0.7rem; color: #64748b;">{{ selectedEmployeePayrollDetails.workingDaysInPeriod }} Days Base (₱{{ selectedEmployeePayrollDetails.earnedBaseGross.toFixed(2) }} Earned)</div>
              </div>
            </div>

            <!-- APPROVED LEAVE (+) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(16, 185, 129, 0.25); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(16, 185, 129, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🏖️</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Approved Leave Pay (+)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #34d399;">+₱{{ selectedEmployeePayrollDetails.leavePay.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #10b981;">{{ selectedEmployeePayrollDetails.leaveDays }} Paid Leave Day(s)</div>
              </div>
            </div>

            <!-- APPROVED OVERTIME PAY (+) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(168, 85, 247, 0.3); display: flex; align-items: center; gap: 1rem; box-shadow: 0 0 15px rgba(168, 85, 247, 0.15);">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(168, 85, 247, 0.2); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">⏰</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Approved Overtime Pay (+)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #c084fc;">+₱{{ (selectedEmployeePayrollDetails.overtimePay || 0).toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #a78bfa;">{{ selectedEmployeePayrollDetails.overtimeHours || 0 }} OT Hour(s) Approved</div>
              </div>
            </div>

            <!-- NIGHT DIFFERENTIAL PAY (+) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(59, 130, 246, 0.3); display: flex; align-items: center; gap: 1rem; box-shadow: 0 0 15px rgba(59, 130, 246, 0.15);">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(59, 130, 246, 0.2); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🌙</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Night Differential Pay (+)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #60a5fa;">+₱{{ (selectedEmployeePayrollDetails.nightDiffPay || 0).toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #93c5fd;">{{ selectedEmployeePayrollDetails.nightDiffHours || 0 }} ND Hour(s) (10PM-6AM)</div>
              </div>
            </div>

            <!-- ABSENT DAYS DEDUCTION -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(239, 68, 68, 0.3); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(239, 68, 68, 0.2); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🚫</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Absent Days Penalty</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #ef4444;">-₱{{ selectedEmployeePayrollDetails.absentDeduction.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #f87171;">{{ selectedEmployeePayrollDetails.absentDays }} Day(s) Absent</div>
              </div>
            </div>

            <!-- TARDINESS DEDUCTIONS -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(239, 68, 68, 0.25); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(239, 68, 68, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">📉</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Tardiness Penalty</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #f87171;">-₱{{ selectedEmployeePayrollDetails.tardinessDeduction.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #ef4444;">{{ selectedEmployeePayrollDetails.totalPenaltyMins }} mins penalty</div>
              </div>
            </div>

            <!-- CONTRIBUTIONS (-) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(147, 51, 234, 0.25); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(147, 51, 234, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🏛️</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Contributions (-)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #c084fc;">-₱{{ selectedEmployeePayrollDetails.totalPeriodContributions.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #a855f7;">
                  {{ selectedEmployeePayrollDetails.totalPeriodContributions > 0 ? 'Statutory Contributions Active' : 'No Active Rules' }}
                </div>
              </div>
            </div>

            <!-- PERIOD BONUS (+) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(16, 185, 129, 0.25); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(16, 185, 129, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🎁</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Period Bonus (+)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #34d399;">+₱{{ selectedEmployeePayrollDetails.totalPeriodBonus.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #10b981;">Scheduled in Period</div>
              </div>
            </div>

            <!-- PERIOD DEDUCTION (-) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(244, 63, 94, 0.25); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(244, 63, 94, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🔻</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Period Deduction (-)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #fb7185;">-₱{{ selectedEmployeePayrollDetails.totalPeriodDeduction.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #f43f5e;">Scheduled in Period</div>
              </div>
            </div>

            <!-- CASH ADVANCES (-) (2ND PERIOD ONLY) -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(234, 88, 12, 0.25); display: flex; align-items: center; gap: 1rem;">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(234, 88, 12, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">💸</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Cash Advances (-)</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #fb923c;">-₱{{ selectedEmployeePayrollDetails.totalPeriodCashAdvances.toFixed(2) }}</div>
                <div style="font-size: 0.7rem; color: #f97316;">
                  {{ selectedEmployeePayrollDetails.isSecondPeriod ? '2nd Period Deducted' : 'Skipped (2nd Period Only)' }}
                </div>
              </div>
            </div>

            <!-- NET SALARY PAYABLE -->
            <div class="glass-card" style="padding: 1.1rem 1.25rem; border-radius: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(16, 185, 129, 0.35); display: flex; align-items: center; gap: 1rem; box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);">
              <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(16, 185, 129, 0.2); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">🟢</div>
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Net Period Pay</div>
                <div style="font-size: 1.3rem; font-weight: 900; color: #10b981;">₱{{ selectedEmployeePayrollDetails.netSalary.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}</div>
                <div style="font-size: 0.7rem; color: #34d399;">Per Period Computed Net</div>
              </div>
            </div>
          </div>

          <!-- DETAILED PAYSLIP BREAKDOWN CARD -->
          <div class="glass-card" style="padding: 1.75rem; border-radius: 16px; background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;">
            <div style="margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 1rem;">
              <h3 style="font-size: 1.2rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.6rem;">
                <span>🧾</span> Semi-Monthly Payslip Breakdown
              </h3>
              <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.2rem;">
                Employee: <strong style="color: #fff;">{{ selectedEmployeePayrollDetails.employeeName }}</strong> (@{{ selectedEmployeePayrollDetails.username }}) — {{ selectedEmployeePayrollDetails.position }}
              </p>
            </div>

            <!-- COMPUTATION EXPLANATION / FORMULA TABLE -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
              
              <!-- 1. SALARY RATE BREAKDOWN -->
              <div style="padding: 1.25rem; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                <h4 style="font-size: 0.88rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.75rem; text-transform: uppercase;">1. Salary Rate Breakdown</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Monthly Base Salary:</span>
                  <strong style="color: #fff;">₱{{ selectedEmployeePayrollDetails.monthlySalary.toFixed(2) }}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Monthly Working Days:</span>
                  <strong style="color: #fff;">22 Days</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Salary Per Day (Salary / 22):</span>
                  <strong style="color: #38bdf8;">₱{{ selectedEmployeePayrollDetails.dailyRate.toFixed(2) }} / day</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Salary Per Minute (Daily Rate / 480):</span>
                  <strong style="color: #c084fc;">₱{{ selectedEmployeePayrollDetails.minuteRate.toFixed(4) }} / min</strong>
                </div>
              </div>

              <!-- 2. PERIOD COVERAGE & BASE GROSS -->
              <div style="padding: 1.25rem; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                <h4 style="font-size: 0.88rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.75rem; text-transform: uppercase;">2. Period Coverage & Base Gross</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Selected Period:</span>
                  <strong style="color: #fff;">{{ currentSelectedPeriodInfo.label }}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Working Days Span:</span>
                  <strong style="color: #fff;">{{ selectedEmployeePayrollDetails.workingDaysInPeriod }} Days</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Days Present / Logged:</span>
                  <strong style="color: #34d399;">{{ selectedEmployeePayrollDetails.presentDays }} Day(s)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Approved Paid Leave Days:</span>
                  <strong style="color: #38bdf8;">{{ selectedEmployeePayrollDetails.leaveDays }} Day(s) (+₱{{ selectedEmployeePayrollDetails.leavePay.toFixed(2) }})</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Days Absent:</span>
                  <strong style="color: #f87171;">{{ selectedEmployeePayrollDetails.absentDays }} Day(s)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Earned Base Gross (Present × Daily):</span>
                  <strong style="color: #f59e0b;">₱{{ selectedEmployeePayrollDetails.earnedBaseGross.toFixed(2) }}</strong>
                </div>
              </div>

              <!-- 3. TARDINESS & ABSENT DEDUCTIONS -->
              <div style="padding: 1.25rem; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.15);">
                <h4 style="font-size: 0.88rem; font-weight: 700; color: #f87171; margin-bottom: 0.75rem; text-transform: uppercase;">3. Tardiness & Absent Penalties</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Absent Days Deduction:</span>
                  <strong style="color: #f87171;">-₱{{ selectedEmployeePayrollDetails.absentDeduction.toFixed(2) }}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Total Penalty Minutes:</span>
                  <strong style="color: #f87171;">{{ selectedEmployeePayrollDetails.totalPenaltyMins }} mins</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Tardiness Minute Deduction:</span>
                  <strong style="color: #ef4444;">-₱{{ selectedEmployeePayrollDetails.tardinessDeduction.toFixed(2) }}</strong>
                </div>
              </div>

              <!-- 4. STATUTORY CONTRIBUTIONS -->
              <div style="padding: 1.25rem; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                  <h4 style="font-size: 0.88rem; font-weight: 700; color: #c084fc; text-transform: uppercase; margin: 0;">4. Statutory Contributions</h4>
                  <span style="font-size: 0.68rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; background: rgba(168, 85, 247, 0.2); color: #c084fc;">Statutory</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Applied State:</span>
                  <strong :style="{ color: selectedEmployeePayrollDetails.totalPeriodContributions > 0 ? '#34d399' : '#94a3b8' }">
                    {{ selectedEmployeePayrollDetails.totalPeriodContributions > 0 ? 'Active Deductions Applied' : 'No Active Rules' }}
                  </strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Configured Rules Count:</span>
                  <strong style="color: #fff;">{{ (selectedEmployeePayrollDetails?.contributionItems || []).length }} Rules</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Total Contributions Deduction:</span>
                  <strong style="color: #c084fc;">-₱{{ (selectedEmployeePayrollDetails?.totalPeriodContributions || 0).toFixed(2) }}</strong>
                </div>
              </div>

              <!-- 5. PERIOD BONUS & DEDUCTION -->
              <div style="padding: 1.25rem; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.15);">
                <h4 style="font-size: 0.88rem; font-weight: 700; color: #34d399; margin-bottom: 0.75rem; text-transform: uppercase;">5. Period Bonus & Deduction</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Scheduled Period Bonuses:</span>
                  <strong style="color: #34d399;">+₱{{ (selectedEmployeePayrollDetails?.totalPeriodBonus || 0).toFixed(2) }}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Scheduled Period Deductions:</span>
                  <strong style="color: #f87171;">-₱{{ (selectedEmployeePayrollDetails?.totalPeriodDeduction || 0).toFixed(2) }}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Net Bonus/Deduction Adjust:</span>
                  <strong :style="{ color: ((selectedEmployeePayrollDetails?.totalPeriodBonus || 0) - (selectedEmployeePayrollDetails?.totalPeriodDeduction || 0)) >= 0 ? '#34d399' : '#f87171' }">
                    {{ ((selectedEmployeePayrollDetails?.totalPeriodBonus || 0) - (selectedEmployeePayrollDetails?.totalPeriodDeduction || 0)) >= 0 ? '+' : '' }}₱{{ ((selectedEmployeePayrollDetails?.totalPeriodBonus || 0) - (selectedEmployeePayrollDetails?.totalPeriodDeduction || 0)).toFixed(2) }}
                  </strong>
                </div>
              </div>

              <!-- 6. CASH ADVANCES (2ND PERIOD ONLY) -->
              <div style="padding: 1.25rem; background: rgba(0,0,0,0.25); border-radius: 12px; border: 1px solid rgba(234, 88, 12, 0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                  <h4 style="font-size: 0.88rem; font-weight: 700; color: #fb923c; text-transform: uppercase; margin: 0;">6. Cash Advances</h4>
                  <span style="font-size: 0.68rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; background: rgba(234, 88, 12, 0.2); color: #fb923c;">2nd Period Only</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Applied Period:</span>
                  <strong :style="{ color: selectedEmployeePayrollDetails?.isSecondPeriod ? '#fb923c' : '#94a3b8' }">
                    {{ selectedEmployeePayrollDetails?.isSecondPeriod ? '2nd Period (Active)' : 'Skipped on 1st Period' }}
                  </strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Approved Advance Filings:</span>
                  <strong style="color: #fff;">{{ (selectedEmployeePayrollDetails?.cashAdvanceItems || []).length }} Request(s)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                  <span>Total Cash Advance Deduction:</span>
                  <strong style="color: #fb923c;">-₱{{ (selectedEmployeePayrollDetails?.totalPeriodCashAdvances || 0).toFixed(2) }}</strong>
                </div>
              </div>

            </div>

            <!-- CONTRIBUTIONS ITEMIZATION BREAKDOWN -->
            <div v-if="(selectedEmployeePayrollDetails?.contributionItems || []).length > 0" style="margin-top: 1rem; padding: 1rem; background: rgba(147, 51, 234, 0.08); border: 1px solid rgba(147, 51, 234, 0.25); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #c084fc; margin-bottom: 0.5rem;">🏛️ Itemized Statutory Contribution Deductions:</h5>
              <div v-for="c in selectedEmployeePayrollDetails.contributionItems" :key="c.id" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>🏛️ {{ c.name }} <span v-if="c.calc_type === 'msc_table'" style="color: #94a3b8;">(MSC Table Range fit)</span><span v-else style="color: #94a3b8;">({{ c.total_rate }}% rate, employee share)</span></span>
                <span style="color: #c084fc; font-weight: 700;">-₱{{ ((c.emp_amount != null ? c.emp_amount : c.empAmt) || 0).toFixed(2) }}</span>
              </div>
            </div>

            <!-- BONUS ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="(selectedEmployeePayrollDetails?.periodBonuses || []).length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #34d399; margin-bottom: 0.5rem;">🎁 Itemized Period Bonus Additions:</h5>
              <div v-for="b in selectedEmployeePayrollDetails.periodBonuses" :key="b.id" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>🎁 {{ b.name }} <span v-if="b.notes" style="color: #94a3b8;">({{ b.notes }})</span></span>
                <span style="color: #34d399; font-weight: 700;">+₱{{ (parseFloat(b.amount) || 0).toFixed(2) }}</span>
              </div>
            </div>

            <!-- DEDUCTION ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="(selectedEmployeePayrollDetails?.periodDeductions || []).length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #fb7185; margin-bottom: 0.5rem;">🔻 Itemized Period Deduction Penalties:</h5>
              <div v-for="d in selectedEmployeePayrollDetails.periodDeductions" :key="d.id" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>🔻 {{ d.name }} <span v-if="d.notes" style="color: #94a3b8;">({{ d.notes }})</span></span>
                <span style="color: #fb7185; font-weight: 700;">-₱{{ (parseFloat(d.amount) || 0).toFixed(2) }}</span>
              </div>
            </div>

            <!-- CASH ADVANCE ITEMIZATION BREAKDOWN IF 2ND PERIOD AND ANY -->
            <div v-if="selectedEmployeePayrollDetails?.isSecondPeriod && (selectedEmployeePayrollDetails?.cashAdvanceItems || []).length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(234, 88, 12, 0.08); border: 1px solid rgba(234, 88, 12, 0.25); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #fb923c; margin-bottom: 0.5rem;">💸 Itemized Cash Advance Deductions (2nd Period Only):</h5>
              <div v-for="adv in selectedEmployeePayrollDetails.cashAdvanceItems" :key="adv.id" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>💸 Cash Advance Request #{{ adv.id }} <span v-if="adv.reason" style="color: #94a3b8;">({{ adv.reason }})</span></span>
                <span style="color: #fb923c; font-weight: 700;">-₱{{ (parseFloat(adv.amount) || 0).toFixed(2) }}</span>
              </div>
            </div>

            <!-- TARDINESS ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="selectedEmployeePayrollDetails.tardyLogs && selectedEmployeePayrollDetails.tardyLogs.length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #f87171; margin-bottom: 0.5rem;">⚠️ Itemized Tardiness / Early Out Instances in Period:</h5>
              <div v-for="log in selectedEmployeePayrollDetails.tardyLogs" :key="log.date" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>📅 {{ log.date }} — {{ log.reason }}</span>
                <span style="color: #f87171; font-weight: 700;">-{{ (log.tardyMins || 0) + (log.earlyOutMins || 0) }} mins (-₱{{ (((log.tardyMins || 0) + (log.earlyOutMins || 0)) * selectedEmployeePayrollDetails.minuteRate).toFixed(2) }})</span>
              </div>
            </div>

            <!-- APPROVED LEAVE DAYS ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="selectedEmployeePayrollDetails.leaveLogs && selectedEmployeePayrollDetails.leaveLogs.length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #34d399; margin-bottom: 0.5rem;">🏖️ Itemized Approved Paid Leave Days in Period:</h5>
              <div v-for="log in selectedEmployeePayrollDetails.leaveLogs" :key="log.date" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>📅 {{ log.date }} — {{ log.details || log.reason || 'Approved Paid Leave' }}</span>
                <span style="color: #34d399; font-weight: 700;">+1 Paid Day (+₱{{ selectedEmployeePayrollDetails.dailyRate.toFixed(2) }})</span>
              </div>
            </div>

            <!-- APPROVED OVERTIME ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="selectedEmployeePayrollDetails.overtimeLogs && selectedEmployeePayrollDetails.overtimeLogs.length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(168, 85, 247, 0.08); border: 1px solid rgba(168, 85, 247, 0.25); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #c084fc; margin-bottom: 0.5rem;">⏰ Itemized Approved Overtime Filings in Period:</h5>
              <div v-for="log in selectedEmployeePayrollDetails.overtimeLogs" :key="log.id || log.date" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>📅 {{ log.date }} — {{ log.details }} <span style="color: #94a3b8;">({{ log.reason }})</span></span>
                <span style="color: #c084fc; font-weight: 700;">+{{ log.hours }} hrs @ {{ log.rateMultiplier }}x (+₱{{ log.amount.toFixed(2) }})</span>
              </div>
            </div>

            <!-- NIGHT DIFFERENTIAL ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="(selectedEmployeePayrollDetails?.nightDiffPay || 0) > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #60a5fa; margin-bottom: 0.5rem;">🌙 Itemized Night Differential (10:00 PM - 06:00 AM) Additions:</h5>
              <div style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between;">
                <span>🌙 {{ selectedEmployeePayrollDetails.nightDiffHours }} Night Diff Hour(s) worked @ {{ selectedEmployeePayrollDetails.nightDiffRatePercent || 10 }}% additional hourly rate</span>
                <span style="color: #60a5fa; font-weight: 700;">+₱{{ (selectedEmployeePayrollDetails.nightDiffPay || 0).toFixed(2) }}</span>
              </div>
            </div>

            <!-- ABSENT DAYS ITEMIZATION BREAKDOWN IF ANY -->
            <div v-if="selectedEmployeePayrollDetails.absentLogs && selectedEmployeePayrollDetails.absentLogs.length > 0" style="margin-top: 0.5rem; padding: 1rem; background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 10px;">
              <h5 style="font-size: 0.82rem; font-weight: 700; color: #f87171; margin-bottom: 0.5rem;">🚫 Itemized Absent Days (Un-clocked Workdays in Period):</h5>
              <div v-for="log in selectedEmployeePayrollDetails.absentLogs" :key="log.date" style="font-size: 0.8rem; color: #e2e8f0; display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>📅 {{ log.date }} — {{ log.reason }}</span>
                <span style="color: #f87171; font-weight: 700;">-1 Day (-₱{{ selectedEmployeePayrollDetails.dailyRate.toFixed(2) }})</span>
              </div>
            </div>

          </div>

          <!-- ALL EMPLOYEES PERIOD PAYROLL COMPUTATION TABLE -->
          <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                <span>📊</span> All Employees Period Payroll Summary Table
              </h3>
              <span style="font-size: 0.8rem; color: #94a3b8;">
                Period: <strong>{{ currentSelectedPeriodInfo.label }}</strong>
              </span>
            </div>

            <div class="table-responsive" style="max-height: 520px; overflow-y: auto; overflow-x: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
              <table class="data-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Employee</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Monthly Salary</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Daily Rate</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Working / Logged</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Period Gross</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Absent Penalty (-)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Tardy Penalty (-)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Contrib (-) <span style="font-size: 0.65rem; color: #c084fc;">(1st Per)</span></th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Overtime Pay (+)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Night Diff (+)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Bonus (+)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Deduction (-)</th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Advances (-) <span style="font-size: 0.65rem; color: #fb923c;">(2nd Per)</span></th>
                    <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Net Period Pay</th>
                    <th v-if="canAccessMenu('payroll_approver')" style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a; z-index: 5;">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="row in employeeGeneratePayrollTable" 
                    :key="row.employeeId"
                    :style="{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      fontSize: '0.88rem',
                      background: String(selectedPayrollGenerateEmployeeId) === String(row.employeeId) ? 'rgba(56, 189, 248, 0.15)' : 'transparent'
                    }"
                  >
                    <!-- EMPLOYEE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="font-weight: 700; color: #fff;">{{ row.employeeName }}</div>
                      <div style="font-size: 0.75rem; color: #94a3b8;">@{{ row.username }} — {{ row.position }}</div>
                    </td>

                    <!-- MONTHLY SALARY -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #cbd5e1;">
                      ₱{{ row.monthlySalary.toFixed(2) }}
                    </td>

                    <!-- DAILY RATE -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #38bdf8; font-weight: 600;">
                      ₱{{ row.dailyRate.toFixed(2) }}
                    </td>

                    <!-- WORKING / LOGGED DAYS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #e2e8f0;">
                      <div>{{ row.workingDaysInPeriod }} Days</div>
                      <div style="font-size: 0.72rem; color: #34d399;">
                        {{ row.presentDays }} Logged
                        <span v-if="row.leaveDays > 0" style="color: #38bdf8; font-weight: 700;">({{ row.leaveDays }} Leave)</span>
                      </div>
                    </td>

                    <!-- PERIOD GROSS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #f59e0b; font-weight: 700;">
                      ₱{{ row.periodBaseGross.toFixed(2) }}
                    </td>

                    <!-- ABSENT PENALTY -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #ef4444; font-weight: 700;">
                      -₱{{ row.absentDeduction.toFixed(2) }}
                      <div style="font-size: 0.7rem; color: #f87171;">{{ row.absentDays }} Day(s)</div>
                    </td>

                    <!-- MINUTE DEDUCTION -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #ef4444; font-weight: 700;">
                      -₱{{ row.tardinessDeduction.toFixed(2) }}
                    </td>

                    <!-- CONTRIBUTIONS (1ST PERIOD ONLY) -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #c084fc; font-weight: 700;">
                      -₱{{ (row.totalPeriodContributions || 0).toFixed(2) }}
                    </td>

                    <!-- OVERTIME PAY -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #c084fc; font-weight: 700;">
                      +₱{{ (row.overtimePay || 0).toFixed(2) }}
                      <div v-if="row.overtimeHours > 0" style="font-size: 0.7rem; color: #a78bfa;">{{ row.overtimeHours }} OT hrs</div>
                    </td>

                    <!-- NIGHT DIFFERENTIAL PAY -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #60a5fa; font-weight: 700;">
                      +₱{{ (row.nightDiffPay || 0).toFixed(2) }}
                      <div v-if="row.nightDiffHours > 0" style="font-size: 0.7rem; color: #93c5fd;">{{ row.nightDiffHours }} ND hrs</div>
                    </td>

                    <!-- PERIOD BONUS -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #34d399; font-weight: 700;">
                      +₱{{ row.totalPeriodBonus.toFixed(2) }}
                    </td>

                    <!-- PERIOD DEDUCTION -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #f87171; font-weight: 700;">
                      -₱{{ row.totalPeriodDeduction.toFixed(2) }}
                    </td>

                    <!-- CASH ADVANCES (2ND PERIOD ONLY) -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #fb923c; font-weight: 700;">
                      -₱{{ (row.totalPeriodCashAdvances || 0).toFixed(2) }}
                    </td>

                    <!-- NET PERIOD PAY -->
                    <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.88rem; display: inline-block;">
                        🟢 ₱{{ row.netSalary.toFixed(2) }}
                      </span>
                    </td>

                    <!-- ACTION -->
                    <td v-if="canAccessMenu('payroll_approver')" style="padding: 0.85rem 1rem; white-space: nowrap;">
                      <div style="display: flex; gap: 0.35rem; align-items: center;">
                        <button @click="selectedPayrollGenerateEmployeeId = row.employeeId" class="btn btn-ghost btn-sm" style="font-size: 0.78rem; padding: 0.25rem 0.6rem;">
                          👁️ View
                        </button>
                        <button @click="downloadPayslipPDF(row)" type="button" class="btn btn-primary btn-sm" style="font-size: 0.78rem; padding: 0.25rem 0.6rem; background: rgba(2, 132, 199, 0.2); border: 1px solid rgba(2, 132, 199, 0.4); color: #38bdf8; font-weight: 700;">
                          📥 PDF
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- VIEW: PAYROLL - CASH ADVANCES -->
        <div v-else-if="activeView === 'payroll_advances'" class="page-view glass payroll-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">💸 Cash Advances Management</h2>
              <p class="view-subheading">Submit cash advance requests, track request approval status, and manage employee salary advances</p>
            </div>
            <div class="header-action-box">
              <button 
                type="button" 
                class="btn btn-secondary" 
                @click="loadCashAdvancesFromStorage(); cashAdvanceSuccess = 'Cash advance records refreshed!'"
                style="display: flex; align-items: center; gap: 0.4rem; padding: 0.6rem 1.1rem; font-weight: 700; border-radius: 10px;"
              >
                🔄 Refresh Records
              </button>
            </div>
          </div>

          <!-- SUCCESS & ERROR ALERT TOASTS -->
          <Transition name="fade">
            <div v-if="cashAdvanceSuccess" style="margin-bottom: 1.25rem; padding: 0.85rem 1.25rem; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34d399; border-radius: 12px; font-weight: 600; display: flex; justify-content: space-between; align-items: center;">
              <span>✅ {{ cashAdvanceSuccess }}</span>
              <button @click="cashAdvanceSuccess = ''" style="background: transparent; border: none; color: #34d399; font-size: 1rem; cursor: pointer;">✕</button>
            </div>
          </Transition>

          <Transition name="fade">
            <div v-if="cashAdvanceError" style="margin-bottom: 1.25rem; padding: 0.85rem 1.25rem; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; border-radius: 12px; font-weight: 600; display: flex; justify-content: space-between; align-items: center;">
              <span>⚠️ {{ cashAdvanceError }}</span>
              <button @click="cashAdvanceError = ''" style="background: transparent; border: none; color: #f87171; font-size: 1rem; cursor: pointer;">✕</button>
            </div>
          </Transition>

          <!-- TOP SUMMARY CARDS (4 INLINE CARDS IN A ROW) -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: rgba(15, 23, 42, 0.6); padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08); display: flex; flex-direction: column; gap: 0.5rem;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">📋 Total Requests</span>
              <span style="font-size: 1.6rem; font-weight: 800; color: #38bdf8;">{{ cashAdvanceSummary.totalCount }}</span>
              <span style="font-size: 0.72rem; color: #64748b;">All submitted cash advances</span>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(245, 158, 11, 0.25); display: flex; flex-direction: column; gap: 0.5rem;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #f59e0b; text-transform: uppercase; letter-spacing: 0.5px;">⏳ Pending Approval</span>
              <span style="font-size: 1.6rem; font-weight: 800; color: #fbbf24;">{{ cashAdvanceSummary.pendingCount }} <span style="font-size: 0.85rem; color: #f59e0b;">(₱{{ cashAdvanceSummary.pendingAmount.toLocaleString('en-US', { minimumFractionDigits: 2 }) }})</span></span>
              <span style="font-size: 0.72rem; color: #f59e0b;">Awaiting admin review</span>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(16, 185, 129, 0.25); display: flex; flex-direction: column; gap: 0.5rem;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #10b981; text-transform: uppercase; letter-spacing: 0.5px;">✅ Approved Advances</span>
              <span style="font-size: 1.6rem; font-weight: 800; color: #34d399;">{{ cashAdvanceSummary.approvedCount }} <span style="font-size: 0.85rem; color: #10b981;">(₱{{ cashAdvanceSummary.approvedAmount.toLocaleString('en-US', { minimumFractionDigits: 2 }) }})</span></span>
              <span style="font-size: 0.72rem; color: #34d399;">Approved for disbursement</span>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(239, 68, 68, 0.25); display: flex; flex-direction: column; gap: 0.5rem;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #ef4444; text-transform: uppercase; letter-spacing: 0.5px;">❌ Denied Requests</span>
              <span style="font-size: 1.6rem; font-weight: 800; color: #f87171;">{{ cashAdvanceSummary.deniedCount }}</span>
              <span style="font-size: 0.72rem; color: #f87171;">Rejected advance requests</span>
            </div>
          </div>

          <!-- STACKED CONTAINER BELOW SUMMARY CARDS -->
          <div style="display: flex; flex-direction: column; gap: 1.5rem;">
            
            <!-- 1. ADVANCE REQUEST FORM (STACKED VERTICAL FORM) -->
            <div style="background: rgba(15, 23, 42, 0.7); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
              <div style="display: flex; align-items: center; gap: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                <span style="font-size: 1.2rem;">💸</span>
                <div>
                  <h3 style="font-size: 1rem; font-weight: 700; color: #fff; margin: 0;">Request Cash Advance</h3>
                  <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">Fill in the details below to submit a new salary cash advance request.</p>
                </div>
              </div>

              <div style="display: flex; flex-direction: column; gap: 1.25rem; max-width: 780px;">
                <!-- ROW 1: EMPLOYEE (REQUESTED FOR) & CREATED BY -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                  <!-- REQUESTED FOR / BENEFICIARY EMPLOYEE -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      👤 Requested For (Employee)
                    </label>
                    <select 
                      v-model="selectedAdvanceEmployeeId" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.88rem; font-weight: 600; cursor: pointer;"
                    >
                      <option value="current_user">Me ({{ userCurrentName }})</option>
                      <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="String(emp.id)">
                        {{ emp.full_name || emp.username }} ({{ emp.role || 'Employee' }})
                      </option>
                    </select>
                  </div>

                  <!-- CREATED BY (CREATOR NAME - LOCKED TO LOGGED IN USER) -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      ✍️ Created By (Logged In Account)
                    </label>
                    <select 
                      v-model="selectedCreatedByName" 
                      disabled
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 0.88rem; font-weight: 700; cursor: not-allowed; opacity: 0.85;"
                    >
                      <option value="current_user">Me ({{ userCurrentName }})</option>
                    </select>
                  </div>
                </div>

                <!-- ROW 2: ADVANCE AMOUNT & REASON -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                  <!-- ADVANCE AMOUNT -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      💰 Advance Amount (₱)
                    </label>
                    <input 
                      type="number" 
                      step="100" 
                      min="1" 
                      v-model.number="cashAdvanceForm.amount" 
                      placeholder="Enter amount (e.g. 2500)" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #34d399; font-size: 1rem; font-weight: 700;"
                      required
                    />
                  </div>

                  <!-- REASON / PURPOSE -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      📝 Reason / Purpose
                    </label>
                    <input 
                      type="text" 
                      v-model="cashAdvanceForm.reason" 
                      placeholder="Reason for advance..." 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.88rem;"
                      required
                    />
                  </div>
                </div>

                <!-- ROW 3: SUBMIT BUTTON -->
                <div style="padding-top: 0.25rem;">
                  <button 
                    type="button" 
                    @click="submitCashAdvanceRequest" 
                    class="btn btn-primary" 
                    style="width: auto; min-width: 220px; padding: 0.75rem 1.5rem; font-weight: 700; border-radius: 10px; font-size: 0.88rem; display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem; background: linear-gradient(135deg, #10b981, #059669); border: none; cursor: pointer;"
                  >
                    🚀 Submit Cash Advance Request
                  </button>
                </div>
              </div>
            </div>

            <!-- 2. CASH ADVANCES LIST TABLE (BELOW REQUEST FORM) -->
            <div style="background: rgba(15, 23, 42, 0.7); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
              <!-- STATUS FILTER BAR -->
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 0.75rem;">
                <h3 style="font-size: 1rem; font-weight: 700; color: #fff; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                  📜 Cash Advances History & Approvals
                </h3>

                <!-- FILTER BUTTONS -->
                <div style="display: flex; gap: 0.4rem; background: rgba(30, 41, 59, 0.6); padding: 0.25rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                  <button 
                    @click="cashAdvanceStatusFilter = 'all'" 
                    :style="{
                      padding: '0.35rem 0.75rem',
                      fontSize: '0.78rem',
                      fontWeight: '700',
                      borderRadius: '6px',
                      border: 'none',
                      cursor: 'pointer',
                      background: cashAdvanceStatusFilter === 'all' ? '#38bdf8' : 'transparent',
                      color: cashAdvanceStatusFilter === 'all' ? '#0f172a' : '#94a3b8'
                    }"
                  >
                    All ({{ cashAdvancesLogs.length }})
                  </button>
                  <button 
                    @click="cashAdvanceStatusFilter = 'Pending'" 
                    :style="{
                      padding: '0.35rem 0.75rem',
                      fontSize: '0.78rem',
                      fontWeight: '700',
                      borderRadius: '6px',
                      border: 'none',
                      cursor: 'pointer',
                      background: cashAdvanceStatusFilter === 'Pending' ? '#f59e0b' : 'transparent',
                      color: cashAdvanceStatusFilter === 'Pending' ? '#0f172a' : '#94a3b8'
                    }"
                  >
                    Pending ({{ cashAdvanceSummary.pendingCount }})
                  </button>
                  <button 
                    @click="cashAdvanceStatusFilter = 'Approved'" 
                    :style="{
                      padding: '0.35rem 0.75rem',
                      fontSize: '0.78rem',
                      fontWeight: '700',
                      borderRadius: '6px',
                      border: 'none',
                      cursor: 'pointer',
                      background: cashAdvanceStatusFilter === 'Approved' ? '#10b981' : 'transparent',
                      color: cashAdvanceStatusFilter === 'Approved' ? '#0f172a' : '#94a3b8'
                    }"
                  >
                    Approved ({{ cashAdvanceSummary.approvedCount }})
                  </button>
                  <button 
                    @click="cashAdvanceStatusFilter = 'Denied'" 
                    :style="{
                      padding: '0.35rem 0.75rem',
                      fontSize: '0.78rem',
                      fontWeight: '700',
                      borderRadius: '6px',
                      border: 'none',
                      cursor: 'pointer',
                      background: cashAdvanceStatusFilter === 'Denied' ? '#ef4444' : 'transparent',
                      color: cashAdvanceStatusFilter === 'Denied' ? '#fff' : '#94a3b8'
                    }"
                  >
                    Denied ({{ cashAdvanceSummary.deniedCount }})
                  </button>
                </div>
              </div>

              <!-- TABLE -->
              <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                  <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">
                      <th style="padding: 0.75rem 0.85rem;">ID</th>
                      <th style="padding: 0.75rem 0.85rem;">Requested For</th>
                      <th style="padding: 0.75rem 0.85rem;">Created By</th>
                      <th style="padding: 0.75rem 0.85rem;">Amount</th>
                      <th style="padding: 0.75rem 0.85rem;">Reason / Purpose</th>
                      <th style="padding: 0.75rem 0.85rem;">Timestamp</th>
                      <th style="padding: 0.75rem 0.85rem; text-align: center;">Status</th>
                      <th v-if="canApproveModule('cash_advances')" style="padding: 0.75rem 0.85rem; text-align: center;">Admin Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="filteredCashAdvancesLogs.length === 0">
                      <td :colspan="canApproveModule('cash_advances') ? 8 : 7" style="padding: 2rem; text-align: center; color: #64748b; font-size: 0.9rem;">
                        No cash advance records found matching filter.
                      </td>
                    </tr>
                    <tr 
                      v-for="item in filteredCashAdvancesLogs" 
                      :key="item.id"
                      style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.86rem;"
                    >
                      <td style="padding: 0.85rem; font-weight: 700; color: #38bdf8; white-space: nowrap;">
                        {{ item.id }}
                      </td>
                      <td style="padding: 0.85rem; font-weight: 600; color: #fff; white-space: nowrap;">
                        {{ item.employee_name }}
                      </td>
                      <td style="padding: 0.85rem; font-weight: 600; color: #38bdf8; white-space: nowrap;">
                        ✍️ {{ item.created_by || item.employee_name || 'System' }}
                      </td>
                      <td style="padding: 0.85rem; font-weight: 800; color: #34d399; white-space: nowrap;">
                        ₱{{ (parseFloat(item.amount) || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                      </td>
                      <td style="padding: 0.85rem; color: #cbd5e1; min-width: 160px;">
                        {{ item.reason }}
                      </td>
                      <td style="padding: 0.85rem; color: #94a3b8; font-size: 0.78rem; white-space: nowrap;">
                        🕒 {{ item.timestamp }}
                      </td>
                      <td style="padding: 0.85rem; text-align: center; white-space: nowrap;">
                        <span 
                          :style="{
                            background: item.status === 'Approved' ? 'rgba(16, 185, 129, 0.2)' : (item.status === 'Denied' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)'),
                            color: item.status === 'Approved' ? '#10b981' : (item.status === 'Denied' ? '#ef4444' : '#f59e0b'),
                            border: item.status === 'Approved' ? '1px solid rgba(16, 185, 129, 0.4)' : (item.status === 'Denied' ? '1px solid rgba(239, 68, 68, 0.4)' : '1px solid rgba(245, 158, 11, 0.4)'),
                            padding: '0.25rem 0.65rem',
                            borderRadius: '6px',
                            fontSize: '0.78rem',
                            fontWeight: '700',
                            display: 'inline-block'
                          }"
                        >
                          <template v-if="item.status === 'Approved'">🟢 Approved</template>
                          <template v-else-if="item.status === 'Denied'">🔴 Denied</template>
                          <template v-else>🟡 Pending</template>
                        </span>
                      </td>
                      <td v-if="canApproveModule('cash_advances')" style="padding: 0.85rem; text-align: center; white-space: nowrap;">
                        <div v-if="item.status === 'Pending'" style="display: flex; justify-content: center; gap: 0.4rem;">
                          <button 
                            @click="approveCashAdvance(item)" 
                            type="button"
                            style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34d399; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;"
                            title="Approve Cash Advance Request"
                          >
                            ✅ Approve
                          </button>
                          <button 
                            @click="denyCashAdvance(item)" 
                            type="button"
                            style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;"
                            title="Deny Cash Advance Request"
                          >
                            ❌ Deny
                          </button>
                        </div>
                        <div v-else style="font-size: 0.75rem; color: #64748b;">
                          <span v-if="item.approved_by">{{ item.status }} by {{ item.approved_by }}</span>
                          <span v-else>Completed</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </div>

        <!-- VIEW: PAYROLL - CONTRIBUTIONS -->
        <div v-else-if="activeView === 'payroll_contributions'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🏛️ Payroll Salary Contributions Management</h2>
              <p class="view-subheading">Configure employee salary contribution rates, toggle 50/50 employer contribution split matching, and preview real-time net salary deductions</p>
            </div>
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="loadContributionRulesFromStorage(); contribSuccessMessage = 'Contribution rules refreshed!'"
              style="display: flex; align-items: center; gap: 0.4rem; padding: 0.55rem 1.1rem; border-radius: 10px; font-weight: 700; font-size: 0.85rem;"
            >
              🔄 Refresh Rules
            </button>
          </div>

          <!-- FEEDBACK ALERTS -->
          <div v-if="contribSuccessMessage" class="alert alert-success mt-2" style="margin-bottom: 1.25rem;">
            <span>✅ {{ contribSuccessMessage }}</span>
          </div>
          <div v-if="contribErrorMessage" class="alert alert-error mt-2" style="margin-bottom: 1.25rem;">
            <span>⚠️ {{ contribErrorMessage }}</span>
          </div>

          <!-- STACKED COLLAPSIBLE CARDS -->
          <div style="display: flex; flex-direction: column; gap: 1.5rem;">

            <!-- CARD 1: CREATE & CONFIGURE CONTRIBUTION RULE (COLLAPSIBLE) -->
            <div id="contrib-card-1" style="background: rgba(15, 23, 42, 0.7); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden;">
              <!-- CARD HEADER (COLLAPSIBLE TOGGLE) -->
              <div 
                @click="isContribCard1Open = !isContribCard1Open" 
                style="padding: 1.25rem 1.5rem; background: rgba(30, 41, 59, 0.8); display: flex; align-items: center; justify-content: space-between; cursor: pointer; user-select: none; border-bottom: 1px solid rgba(255,255,255,0.08);"
              >
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                  <span style="font-size: 1.25rem;">➕</span>
                  <div>
                    <h3 style="font-size: 1rem; font-weight: 700; color: #fff; margin: 0;">
                      {{ editingContribId ? '✏️ Edit Contribution Rule' : '➕ Create Contribution Rule' }}
                    </h3>
                    <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">Define contribution percentage rate and toggle 50/50 employer-employee split share</p>
                  </div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                  <span style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 0.2rem 0.6rem; border-radius: 20px;">
                    {{ isContribCard1Open ? 'Click to Collapse ▲' : 'Click to Expand ▼' }}
                  </span>
                </div>
              </div>

              <!-- CARD BODY -->
              <div v-show="isContribCard1Open" style="padding: 1.5rem;">
                <form @submit.prevent="applyContributionRule" style="display: flex; flex-direction: column; gap: 1.25rem; max-width: 780px;">
                  
                  <!-- ROW 1: CONTRIBUTION NAME & COMPUTATION METHOD SELECTOR -->
                  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                    <!-- CONTRIBUTION NAME -->
                    <div>
                      <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        🏷️ Contribution Name
                      </label>
                      <input 
                        type="text" 
                        v-model="contributionForm.name" 
                        placeholder="e.g. SSS Contribution, PhilHealth, Pag-IBIG, W/Tax..." 
                        style="width: 100%; padding: 0.7rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600;"
                        required
                      />
                    </div>

                    <!-- COMPUTATION TYPE SELECTION -->
                    <div>
                      <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        ⚙️ Computation Method Type
                      </label>
                      <select 
                        v-model="contributionForm.calc_type" 
                        style="width: 100%; padding: 0.7rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 0.9rem; font-weight: 700; cursor: pointer;"
                      >
                        <option value="percentage">📊 Current Savings / Salary Percentage Rate (%)</option>
                        <option value="msc_table">📋 Monthly Compensation Bracket Table (MSC Schedule)</option>
                      </select>
                    </div>
                  </div>

                  <!-- MODE A: PERCENTAGE RATE CONFIGURATION -->
                  <div v-if="contributionForm.calc_type === 'percentage'" style="display: flex; flex-direction: column; gap: 1.25rem;">
                    <!-- EMPLOYEE SALARY PERCENTAGE (%) SLIDER & INPUT -->
                    <div>
                      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <label style="font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.5px;">
                          📊 Employee Salary Percentage Rate (%)
                        </label>
                        <span style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 0.2rem 0.65rem; border-radius: 6px; font-family: monospace;">
                          {{ (parseFloat(contributionForm.rate) || 0).toFixed(2) }}%
                        </span>
                      </div>
                      
                      <div style="display: flex; align-items: center; gap: 1rem;">
                        <!-- SLIDER -->
                        <input 
                          type="range" 
                          min="0" 
                          max="25" 
                          step="0.1" 
                          v-model.number="contributionForm.rate" 
                          style="flex: 1; accent-color: #38bdf8; height: 8px; border-radius: 4px; cursor: pointer;"
                        />
                        <!-- NUMBER FIELD -->
                        <input 
                          type="number" 
                          step="0.1" 
                          min="0" 
                          max="100" 
                          v-model.number="contributionForm.rate" 
                          style="width: 110px; padding: 0.55rem 0.75rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-weight: 700; font-size: 0.9rem; text-align: right;"
                        />
                      </div>
                    </div>

                    <!-- HALF EMPLOYEE AND EMPLOYER CONTRIBUTION SLIDER/TOGGLE -->
                    <div style="background: rgba(30, 41, 59, 0.6); padding: 1rem 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                        <div>
                          <div style="font-size: 0.88rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.4rem;">
                            ⚖️ Apply Half Employee & Employer Contribution (50/50 Split)
                          </div>
                          <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem;">
                            When ENABLED: 50% is deducted from employee salary and 50% is matched by employer. When DISABLED: 100% is deducted from employee salary.
                          </div>
                        </div>

                        <label class="toggle-switch" style="cursor: pointer; margin: 0;">
                          <input type="checkbox" v-model="contributionForm.split_half" />
                          <span class="toggle-slider"></span>
                        </label>
                      </div>

                      <!-- SPLIT PREVIEW BADGE -->
                      <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px dashed rgba(255,255,255,0.1); display: flex; gap: 0.75rem; align-items: center;">
                        <span v-if="contributionForm.split_half" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.3rem 0.75rem; border-radius: 8px; font-size: 0.8rem; font-weight: 700;">
                          🟢 50/50 Shared: Result Split 50% Employee / 50% Employer (e.g. ₱1,000 Total → ₱500 Employee / ₱500 Employer)
                        </span>
                        <span v-else style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.3rem 0.75rem; border-radius: 8px; font-size: 0.8rem; font-weight: 700;">
                          ⚪ 100% Employee Share: Full Result Deducted from Employee | Employer Share ₱0
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- MODE B: MONTHLY COMPENSATION BRACKET TABLE (MSC SCHEDULE) -->
                  <!-- MODE B: DYNAMIC MONTHLY COMPENSATION BRACKET TABLE (MSC SCHEDULE) -->
                  <div v-else-if="contributionForm.calc_type === 'msc_table'" style="display: flex; flex-direction: column; gap: 1.25rem; background: rgba(30, 41, 59, 0.6); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                      <div>
                        <h4 style="font-size: 0.95rem; font-weight: 700; color: #fff; margin: 0;">📋 Dynamic Monthly Salary Credit (MSC) Bracket Builder</h4>
                        <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">Add compensation ranges, MSC credits, and Employee/Employer shares one by one below.</p>
                      </div>
                      <div style="display: flex; gap: 0.5rem;">
                        <button type="button" @click="loadDefaultSeedBrackets" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 0.35rem 0.75rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">
                          ⚡ Load Standard Preset
                        </button>
                        <button type="button" @click="clearAllMscBrackets" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 0.35rem 0.75rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">
                          🗑️ Clear Brackets
                        </button>
                      </div>
                    </div>

                    <!-- INPUT FIELDS TO ADD BRACKET ENTRY ONE BY ONE -->
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 1rem; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.25);">
                      <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        ➕ Add Compensation Bracket Entry
                      </div>
                      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem; align-items: end;">
                        <div>
                          <label style="display: block; font-size: 0.7rem; color: #94a3b8; margin-bottom: 0.25rem;">Range From (₱)</label>
                          <input type="number" step="0.01" v-model.number="newBracketInput.min_sal" placeholder="0.00" style="width: 100%; padding: 0.45rem 0.65rem; border-radius: 6px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.82rem;" />
                        </div>
                        <div>
                          <label style="display: block; font-size: 0.7rem; color: #94a3b8; margin-bottom: 0.25rem;">Range To (₱)</label>
                          <input type="number" step="0.01" v-model.number="newBracketInput.max_sal" placeholder="4999.99" style="width: 100%; padding: 0.45rem 0.65rem; border-radius: 6px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.82rem;" />
                        </div>
                        <div>
                          <label style="display: block; font-size: 0.7rem; color: #38bdf8; margin-bottom: 0.25rem; font-weight: 700;">MSC Credit (₱)</label>
                          <input type="number" step="0.01" v-model.number="newBracketInput.msc" placeholder="5000.00" style="width: 100%; padding: 0.45rem 0.65rem; border-radius: 6px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.4); color: #38bdf8; font-weight: 700; font-size: 0.82rem;" />
                        </div>
                        <div>
                          <label style="display: block; font-size: 0.7rem; color: #94a3b8; margin-bottom: 0.25rem;">Employee Share %</label>
                          <input type="number" step="0.1" v-model.number="newBracketInput.emp_pct" placeholder="5.0" style="width: 100%; padding: 0.45rem 0.65rem; border-radius: 6px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.82rem;" />
                        </div>
                        <div>
                          <label style="display: block; font-size: 0.7rem; color: #94a3b8; margin-bottom: 0.25rem;">Employer Share %</label>
                          <input type="number" step="0.1" v-model.number="newBracketInput.er_pct" placeholder="10.0" style="width: 100%; padding: 0.45rem 0.65rem; border-radius: 6px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.82rem;" />
                        </div>
                        <div>
                          <label style="display: block; font-size: 0.7rem; color: #94a3b8; margin-bottom: 0.25rem;">EC Amount (₱)</label>
                          <input type="number" step="1" v-model.number="newBracketInput.ec" placeholder="10" style="width: 100%; padding: 0.45rem 0.65rem; border-radius: 6px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.82rem;" />
                        </div>
                        <div>
                          <button type="button" @click="addMscBracketRow" style="width: 100%; padding: 0.5rem; border-radius: 6px; background: linear-gradient(135deg, #10b981, #059669); color: #fff; font-weight: 700; border: none; font-size: 0.8rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.3rem;">
                            ➕ Add Row
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- LIVE BRACKET TABLE DISPLAY -->
                    <div style="overflow-x: auto;">
                      <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.84rem;">
                        <thead>
                          <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); color: #94a3b8; text-transform: uppercase; font-size: 0.74rem;">
                            <th style="padding: 0.75rem 0.65rem;">Monthly Range of Compensation From</th>
                            <th style="padding: 0.75rem 0.65rem;">Monthly Range of Compensation To</th>
                            <th style="padding: 0.75rem 0.65rem;">Monthly Salary Credit (MSC)</th>
                            <th style="padding: 0.75rem 0.65rem;">Employee Share (5%)</th>
                            <th style="padding: 0.75rem 0.65rem;">Employer Share (10% + EC)</th>
                            <th style="padding: 0.75rem 0.65rem;">Total Monthly Contribution</th>
                            <th style="padding: 0.75rem 0.65rem; text-align: center;">Action</th>
                          </tr>
                        </thead>
                        <tbody v-if="contributionForm.msc_brackets && contributionForm.msc_brackets.length > 0">
                          <tr v-for="(b, idx) in contributionForm.msc_brackets" :key="idx" style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <!-- RANGE FROM -->
                            <td style="padding: 0.65rem; color: #cbd5e1; font-family: monospace;">
                              <template v-if="editingMscBracketIndex === idx">
                                <input type="number" step="0.01" v-model.number="editingMscBracketForm.min_sal" style="width: 100px; padding: 0.35rem 0.5rem; border-radius: 6px; background: rgba(15, 23, 42, 0.95); border: 1px solid #38bdf8; color: #fff; font-size: 0.8rem;" />
                              </template>
                              <template v-else>
                                ₱{{ (parseFloat(b.min_sal) || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                              </template>
                            </td>

                            <!-- RANGE TO -->
                            <td style="padding: 0.65rem; color: #cbd5e1; font-family: monospace;">
                              <template v-if="editingMscBracketIndex === idx">
                                <input type="number" step="0.01" v-model.number="editingMscBracketForm.max_sal" style="width: 100px; padding: 0.35rem 0.5rem; border-radius: 6px; background: rgba(15, 23, 42, 0.95); border: 1px solid #38bdf8; color: #fff; font-size: 0.8rem;" />
                              </template>
                              <template v-else>
                                ₱{{ (parseFloat(b.max_sal) || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                              </template>
                            </td>

                            <!-- MSC CREDIT -->
                            <td style="padding: 0.65rem; color: #38bdf8; font-weight: 700; font-family: monospace;">
                              <template v-if="editingMscBracketIndex === idx">
                                <input type="number" step="0.01" v-model.number="editingMscBracketForm.msc" style="width: 100px; padding: 0.35rem 0.5rem; border-radius: 6px; background: rgba(15, 23, 42, 0.95); border: 1px solid #38bdf8; color: #38bdf8; font-weight: 700; font-size: 0.8rem;" />
                              </template>
                              <template v-else>
                                ₱{{ (parseFloat(b.msc) || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                              </template>
                            </td>

                            <!-- EMPLOYEE SHARE -->
                            <td style="padding: 0.65rem; color: #f87171; font-weight: 700; font-family: monospace;">
                              <template v-if="editingMscBracketIndex === idx">
                                <div style="display: flex; align-items: center; gap: 0.3rem;">
                                  <input type="number" step="0.1" v-model.number="editingMscBracketForm.emp_pct" style="width: 65px; padding: 0.35rem 0.4rem; border-radius: 6px; background: rgba(15, 23, 42, 0.95); border: 1px solid #f87171; color: #f87171; font-size: 0.8rem;" /> %
                                </div>
                              </template>
                              <template v-else>
                                -₱{{ ((b.msc * ((b.emp_pct ?? 5.0) / 100))).toLocaleString('en-US', { minimumFractionDigits: 2 }) }} <span style="font-size: 0.7rem; color: #94a3b8;">({{ b.emp_pct ?? 5 }}%)</span>
                              </template>
                            </td>

                            <!-- EMPLOYER SHARE -->
                            <td style="padding: 0.65rem; color: #c084fc; font-weight: 700; font-family: monospace;">
                              <template v-if="editingMscBracketIndex === idx">
                                <div style="display: flex; align-items: center; gap: 0.3rem; flex-wrap: wrap;">
                                  <input type="number" step="0.1" v-model.number="editingMscBracketForm.er_pct" style="width: 65px; padding: 0.35rem 0.4rem; border-radius: 6px; background: rgba(15, 23, 42, 0.95); border: 1px solid #c084fc; color: #c084fc; font-size: 0.8rem;" /> % +₱
                                  <input type="number" step="1" v-model.number="editingMscBracketForm.ec" style="width: 55px; padding: 0.35rem 0.4rem; border-radius: 6px; background: rgba(15, 23, 42, 0.95); border: 1px solid #c084fc; color: #c084fc; font-size: 0.8rem;" /> EC
                                </div>
                              </template>
                              <template v-else>
                                +₱{{ ((b.msc * ((b.er_pct ?? 10.0) / 100)) + (b.ec || 0)).toLocaleString('en-US', { minimumFractionDigits: 2 }) }} <span style="font-size: 0.7rem; color: #94a3b8;">({{ b.er_pct ?? 10 }}% +₱{{ b.ec || 0 }} EC)</span>
                              </template>
                            </td>

                            <!-- TOTAL MONTHLY CONTRIBUTION -->
                            <td style="padding: 0.65rem; color: #34d399; font-weight: 800; font-family: monospace;">
                              <template v-if="editingMscBracketIndex === idx">
                                ₱{{ (((editingMscBracketForm.msc || 0) * (((editingMscBracketForm.emp_pct || 0) + (editingMscBracketForm.er_pct || 0)) / 100)) + (editingMscBracketForm.ec || 0)).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                              </template>
                              <template v-else>
                                ₱{{ ((b.msc * (((b.emp_pct ?? 5.0) + (b.er_pct ?? 10.0)) / 100)) + (b.ec || 0)).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                              </template>
                            </td>

                            <!-- ACTIONS: ICON ONLY -->
                            <td style="padding: 0.65rem; text-align: center; white-space: nowrap;">
                              <div v-if="editingMscBracketIndex === idx" style="display: flex; gap: 0.35rem; justify-content: center;">
                                <button 
                                  type="button" 
                                  @click="saveEditingMscBracketRow(idx)" 
                                  title="Save Row" 
                                  style="background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.5); padding: 0.35rem 0.5rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem;"
                                >
                                  💾
                                </button>
                                <button 
                                  type="button" 
                                  @click="cancelEditingMscBracketRow" 
                                  title="Cancel Edit" 
                                  style="background: rgba(148, 163, 184, 0.2); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.4); padding: 0.35rem 0.5rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem;"
                                >
                                  ❌
                                </button>
                              </div>
                              <div v-else style="display: flex; gap: 0.35rem; justify-content: center;">
                                <button 
                                  type="button" 
                                  @click="startEditingMscBracketRow(idx, b)" 
                                  title="Edit Row" 
                                  style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); padding: 0.35rem 0.5rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem;"
                                >
                                  ✏️
                                </button>
                                <button 
                                  type="button" 
                                  @click="removeMscBracketRow(idx)" 
                                  title="Delete Row" 
                                  style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.25rem 0.5rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem;"
                                >
                                  🗑️
                                </button>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                        <tbody v-else>
                          <tr>
                            <td colspan="7" style="padding: 1.5rem; text-align: center; color: #94a3b8;">
                              No compensation brackets added yet. Input a bracket above and click <strong>➕ Add Row</strong> to construct your custom MSC table.
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <!-- ROW 4: SUBMIT BUTTONS -->
                  <div style="display: flex; gap: 0.75rem; padding-top: 0.25rem;">
                    <button 
                      type="submit" 
                      class="btn btn-primary" 
                      style="padding: 0.75rem 1.75rem; font-weight: 700; border-radius: 10px; font-size: 0.88rem; background: linear-gradient(135deg, #38bdf8, #0284c7); border: none; cursor: pointer;"
                    >
                      {{ editingContribId ? '✏️ Update Contribution Rule' : '🚀 Apply Contribution Rule' }}
                    </button>

                    <button 
                      v-if="editingContribId" 
                      type="button" 
                      @click="resetContributionForm" 
                      class="btn btn-ghost" 
                      style="padding: 0.75rem 1.25rem; font-weight: 600; border-radius: 10px; font-size: 0.88rem; cursor: pointer;"
                    >
                      Cancel Edit
                    </button>
                  </div>

                </form>
              </div>
            </div>

            <!-- CARD 2: CURRENT USER SALARY & CONTRIBUTION DEDUCTIONS RESULT (COLLAPSIBLE) -->
            <div style="background: rgba(15, 23, 42, 0.7); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden;">
              <!-- CARD HEADER -->
              <div 
                @click="isContribCard2Open = !isContribCard2Open" 
                style="padding: 1.25rem 1.5rem; background: rgba(30, 41, 59, 0.8); display: flex; align-items: center; justify-content: space-between; cursor: pointer; user-select: none; border-bottom: 1px solid rgba(255,255,255,0.08);"
              >
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                  <span style="font-size: 1.25rem;">💰</span>
                  <div>
                    <h3 style="font-size: 1rem; font-weight: 700; color: #fff; margin: 0;">
                      Contribution Deductions & Net Pay Result
                    </h3>
                    <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">Live breakdown based on active user salary and configured contribution rules</p>
                  </div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                  <span style="font-size: 0.8rem; font-weight: 700; color: #10b981; background: rgba(16, 185, 129, 0.15); padding: 0.2rem 0.6rem; border-radius: 20px;">
                    {{ isContribCard2Open ? 'Click to Collapse ▲' : 'Click to Expand ▼' }}
                  </span>
                </div>
              </div>

              <!-- CARD BODY -->
              <div v-show="isContribCard2Open" style="padding: 1.5rem;">
                
                <!-- CONTROLS: SELECT USER & SALARY AMOUNT -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; background: rgba(30, 41, 59, 0.5); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      👤 Target Employee Account
                    </label>
                    <select 
                      v-model="selectedContribEmployeeId" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.88rem; font-weight: 600; cursor: pointer;"
                    >
                      <option value="current_user">Current User ({{ userCurrentName }})</option>
                      <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="String(emp.id)">
                        {{ emp.full_name || emp.username }} ({{ emp.role || 'Employee' }})
                      </option>
                    </select>
                  </div>

                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #34d399; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      💵 Base Monthly Salary (₱)
                    </label>
                    <input 
                      type="number" 
                      step="500" 
                      min="1" 
                      v-model.number="customBaseSalary" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; font-size: 1rem; font-weight: 700; font-family: monospace;"
                    />
                  </div>
                </div>

                <!-- 4 SUMMARY CARDS (4 COLUMNS INLINE) -->
                <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem;">
                  <!-- GROSS BASE SALARY -->
                  <div style="background: rgba(30, 41, 59, 0.7); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid #38bdf8;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">💵 Gross Monthly Salary</span>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #fff; margin-top: 0.35rem; font-family: monospace;">
                      ₱{{ (customBaseSalary || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                    </div>
                    <span style="font-size: 0.72rem; color: #64748b;">Set Base Rate</span>
                  </div>

                  <!-- TOTAL DEDUCTIONS -->
                  <div style="background: rgba(30, 41, 59, 0.7); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid #ef4444;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">📉 Employee Deductions</span>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #f87171; margin-top: 0.35rem; font-family: monospace;">
                      -₱{{ totalEmployeeDeductions.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                    </div>
                    <span style="font-size: 0.72rem; color: #ef4444; font-weight: 700;">{{ totalEmployeeDeductionsPct }}% Total Deductions</span>
                  </div>

                  <!-- EMPLOYER MATCH -->
                  <div style="background: rgba(30, 41, 59, 0.7); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid #a855f7;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">🏢 Employer Contribution Match</span>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #c084fc; margin-top: 0.35rem; font-family: monospace;">
                      +₱{{ totalEmployerContributions.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                    </div>
                    <span style="font-size: 0.72rem; color: #a855f7; font-weight: 700;">{{ totalEmployerContributionsPct }}% Paid by Employer</span>
                  </div>

                  <!-- NET TAKE HOME -->
                  <div style="background: rgba(16, 185, 129, 0.15); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.4); border-left: 4px solid #10b981;">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #34d399; text-transform: uppercase;">💰 Net Take-Home Salary</span>
                    <div style="font-size: 1.45rem; font-weight: 900; color: #34d399; margin-top: 0.35rem; font-family: monospace;">
                      ₱{{ netTakeHomeSalary.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                    </div>
                    <span style="font-size: 0.72rem; color: #10b981; font-weight: 700;">Estimated Net Pay</span>
                  </div>
                </div>

                <!-- BREAKDOWN TABLE -->
                <div style="overflow-x: auto;">
                  <h4 style="font-size: 0.9rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem;">📊 Contribution Rules Breakdown Table</h4>
                  <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                      <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">
                        <th style="padding: 0.75rem;">Contribution Name</th>
                        <th style="padding: 0.75rem;">Calculation Method</th>
                        <th style="padding: 0.75rem;">Total Result (₱)</th>
                        <th style="padding: 0.75rem;">Split / Matched Range</th>
                        <th style="padding: 0.75rem;">Employee Share</th>
                        <th style="padding: 0.75rem;">Employer Match</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="calculatedContributionsBreakdown.length === 0">
                        <td colspan="6" style="padding: 1.5rem; text-align: center; color: #64748b;">No active contribution rules configured.</td>
                      </tr>
                      <tr v-for="item in calculatedContributionsBreakdown" :key="item.id" style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.86rem;">
                        <td style="padding: 0.85rem; font-weight: 700; color: #fff;">{{ item.name }}</td>
                        <td style="padding: 0.85rem; font-weight: 700; font-family: monospace;">
                          <span v-if="item.calc_type === 'msc_table'" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                            📋 MSC ₱{{ (item.msc_amount || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                          </span>
                          <span v-else style="color: #38bdf8;">
                            {{ item.total_rate.toFixed(2) }}%
                          </span>
                        </td>
                        <td style="padding: 0.85rem; font-weight: 700; color: #38bdf8; font-family: monospace;">₱{{ item.total_amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</td>
                        <td style="padding: 0.85rem;">
                          <span v-if="item.calc_type === 'msc_table'" style="background: rgba(168, 85, 247, 0.2); color: #c084fc; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                            🎯 Fit Range: ₱{{ (item.matched_bracket?.min_sal || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }} - ₱{{ (item.matched_bracket?.max_sal || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                          </span>
                          <span v-else-if="item.split_half" style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                            ⚖️ 50/50 Shared
                          </span>
                          <span v-else style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                            👤 100% Employee
                          </span>
                        </td>
                        <td style="padding: 0.85rem; color: #f87171; font-weight: 800; font-family: monospace;">-₱{{ item.emp_amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</td>
                        <td style="padding: 0.85rem; color: #c084fc; font-weight: 800; font-family: monospace;">+₱{{ item.er_amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

              </div>
            </div>

            <!-- CARD 3: CONFIGURED CONTRIBUTION RULES LIST (COLLAPSIBLE) -->
            <div style="background: rgba(15, 23, 42, 0.7); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden;">
              <!-- CARD HEADER -->
              <div 
                @click="isContribCard3Open = !isContribCard3Open" 
                style="padding: 1.25rem 1.5rem; background: rgba(30, 41, 59, 0.8); display: flex; align-items: center; justify-content: space-between; cursor: pointer; user-select: none; border-bottom: 1px solid rgba(255,255,255,0.08);"
              >
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                  <span style="font-size: 1.25rem;">📋</span>
                  <div>
                    <h3 style="font-size: 1rem; font-weight: 700; color: #fff; margin: 0;">
                      Configured Contribution Rules ({{ contributionRules.length }})
                    </h3>
                    <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">Manage active rules, toggle 50/50 contribution splits, and modify percentage rates</p>
                  </div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                  <span style="font-size: 0.8rem; font-weight: 700; color: #a855f7; background: rgba(168, 85, 247, 0.15); padding: 0.2rem 0.6rem; border-radius: 20px;">
                    {{ isContribCard3Open ? 'Click to Collapse ▲' : 'Click to Expand ▼' }}
                  </span>
                </div>
              </div>

              <!-- CARD BODY -->
              <div v-show="isContribCard3Open" style="padding: 1.5rem;">
                <div style="overflow-x: auto;">
                  <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                      <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">
                        <th style="padding: 0.75rem 0.85rem;">Rule Name</th>
                        <th style="padding: 0.75rem 0.85rem;">Computation Type</th>
                        <th style="padding: 0.75rem 0.85rem;">Split Mode / Salary Range Fit</th>
                        <th style="padding: 0.75rem 0.85rem;">Est. Employee Deduction</th>
                        <th style="padding: 0.75rem 0.85rem; text-align: center;">Status</th>
                        <th v-if="canAccessMenu('payroll_approver')" style="padding: 0.75rem 0.85rem; text-align: center;">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="contributionRules.length === 0">
                        <td :colspan="canAccessMenu('payroll_approver') ? 6 : 5" style="padding: 2rem; text-align: center; color: #64748b;">No contribution rules added yet.</td>
                      </tr>
                      <tr 
                        v-for="rule in contributionRules" 
                        :key="rule.id" 
                        style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.86rem;"
                      >
                        <td style="padding: 0.85rem; font-weight: 700; color: #fff;">{{ rule.name }}</td>
                        <td style="padding: 0.85rem;">
                          <span v-if="rule.calc_type === 'msc_table'" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                            📋 MSC Bracket Table
                          </span>
                          <span v-else style="font-weight: 800; color: #38bdf8; font-family: monospace;">
                            {{ (rule.rate || 0).toFixed(2) }}%
                          </span>
                        </td>
                        <td style="padding: 0.85rem;">
                          <div v-if="rule.calc_type === 'msc_table'" style="display: flex; flex-direction: column; gap: 0.2rem;">
                            <span style="background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700; width: fit-content;">
                              🎯 Range Fit: ₱{{ (getRuleMatchedBracket(rule).min_sal || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }} - ₱{{ (getRuleMatchedBracket(rule).max_sal || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                            </span>
                            <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 600;">
                              (MSC Credit: ₱{{ (getRuleMatchedBracket(rule).msc || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }})
                            </span>
                          </div>
                          <template v-else>
                            <span v-if="rule.split_half" style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                              ⚖️ 50/50 Shared
                            </span>
                            <span v-else style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                              👤 100% Employee
                            </span>
                          </template>
                        </td>
                        <td style="padding: 0.85rem; color: #f87171; font-weight: 700; font-family: monospace;">
                          -₱{{ getRuleEstimatedEmployeeDeduction(rule).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                        </td>
                        <td style="padding: 0.85rem; text-align: center;">
                          <label class="toggle-switch" style="cursor: pointer; margin: 0; display: inline-block;" title="Toggle Rule Status (On/Off)">
                            <input type="checkbox" :checked="rule.is_active" @change="toggleContributionRule(rule)" />
                            <span class="toggle-slider"></span>
                          </label>
                        </td>
                        <td style="padding: 0.85rem; text-align: center;">
                          <div style="display: flex; justify-content: center; gap: 0.4rem;">
                            <button 
                              type="button" 
                              @click="editContributionRule(rule)"
                              title="Edit Contribution Rule"
                              style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.85rem; cursor: pointer;"
                            >
                              ✏️
                            </button>
                            <button 
                              type="button" 
                              @click="deleteContributionRule(rule.id)"
                              title="Delete Contribution Rule"
                              style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.85rem; cursor: pointer;"
                            >
                              🗑️
                            </button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- VIEW: PAYROLL - BONUS / DEDUCTION -->
        <div v-else-if="activeView === 'payroll_bonus_deduction'" class="page-view glass">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🎁 Payroll Bonus & Deduction Management</h2>
              <p class="view-subheading">Assign one-time or recurring bonus additions and deduction penalties for specific employee salary periods</p>
            </div>
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="loadBonusDeductionsFromStorage(); bonusDeductionSuccess = 'Bonus & Deduction records refreshed!'"
              style="display: flex; align-items: center; gap: 0.4rem; padding: 0.55rem 1.1rem; border-radius: 10px; font-weight: 700; font-size: 0.85rem;"
            >
              🔄 Refresh Records
            </button>
          </div>

          <!-- FEEDBACK ALERTS -->
          <div v-if="bonusDeductionSuccess" class="alert alert-success mt-2" style="margin-bottom: 1.25rem;">
            <span>✅ {{ bonusDeductionSuccess }}</span>
          </div>
          <div v-if="bonusDeductionError" class="alert alert-error mt-2" style="margin-bottom: 1.25rem;">
            <span>⚠️ {{ bonusDeductionError }}</span>
          </div>

          <div style="display: flex; flex-direction: column; gap: 1.5rem;">
            
            <!-- CARD 1: ADD BONUS / DEDUCTION FORM -->
            <div style="background: rgba(15, 23, 42, 0.7); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
              <div style="display: flex; align-items: center; gap: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                <span style="font-size: 1.2rem;">🎁</span>
                <div>
                  <h3 style="font-size: 1rem; font-weight: 700; color: #fff; margin: 0;">Add Employee Bonus or Deduction</h3>
                  <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">Create a bonus addition or deduction penalty bound strictly to a specific salary period.</p>
                </div>
              </div>

              <form @submit.prevent="submitBonusDeduction" style="display: flex; flex-direction: column; gap: 1.25rem; max-width: 780px;">
                <!-- ROW 1: TYPE & EMPLOYEE -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                  <!-- TYPE SELECTOR -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      🏷️ Record Type
                    </label>
                    <select 
                      v-model="bonusDeductionForm.type" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 0.88rem; font-weight: 700; cursor: pointer;"
                    >
                      <option value="bonus">🎁 Bonus / Incentive (Addition +)</option>
                      <option value="deduction">🔻 Deduction / Penalty (Subtraction -)</option>
                    </select>
                  </div>

                  <!-- EMPLOYEE DROPDOWN -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      👤 Target Employee Account
                    </label>
                    <select 
                      v-model="bonusDeductionForm.employee_id" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.88rem; font-weight: 600; cursor: pointer;"
                      required
                    >
                      <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="String(emp.id)">
                        {{ emp.full_name || emp.username }} ({{ emp.role || 'Employee' }})
                      </option>
                    </select>
                  </div>
                </div>

                <!-- ROW 2: NAME & AMOUNT -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                  <!-- BONUS / DEDUCTION NAME -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      📝 Bonus / Deduction Name
                    </label>
                    <input 
                      type="text" 
                      v-model="bonusDeductionForm.name" 
                      placeholder="e.g. Performance Incentive, 13th Month, Uniform Fee..." 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.88rem;"
                      required
                    />
                  </div>

                  <!-- AMOUNT -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #34d399; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      💰 Amount (₱)
                    </label>
                    <input 
                      type="number" 
                      step="any" 
                      min="0.01" 
                      v-model.number="bonusDeductionForm.amount" 
                      placeholder="Enter amount (e.g. 2500)" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; font-size: 1rem; font-weight: 700; font-family: monospace;"
                      required
                    />
                  </div>
                </div>

                <!-- ROW 3: SALARY PERIOD & REASON / NOTES -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                  <!-- SALARY PERIOD SELECTION -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #c084fc; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      📅 Target Salary Period (Where Added)
                    </label>
                    <select 
                      v-model="bonusDeductionForm.period_key" 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(192, 132, 252, 0.4); color: #c084fc; font-size: 0.88rem; font-weight: 700; cursor: pointer;"
                      required
                    >
                      <option v-for="p in payrollPeriodOptions" :key="p.key" :value="p.key">
                        {{ p.label }}
                      </option>
                    </select>
                  </div>

                  <!-- REASON / NOTES -->
                  <div>
                    <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                      📌 Reason / Remarks (Optional)
                    </label>
                    <input 
                      type="text" 
                      v-model="bonusDeductionForm.notes" 
                      placeholder="Remarks or justification..." 
                      style="width: 100%; padding: 0.65rem 0.9rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.88rem;"
                    />
                  </div>
                </div>

                <!-- SUBMIT BUTTON -->
                <div style="padding-top: 0.25rem;">
                  <button 
                    type="submit" 
                    class="btn btn-primary" 
                    style="padding: 0.75rem 1.75rem; font-weight: 700; border-radius: 10px; font-size: 0.88rem; background: linear-gradient(135deg, #10b981, #059669); border: none; cursor: pointer;"
                  >
                    ➕ Add Bonus / Deduction Record
                  </button>
                </div>
              </form>
            </div>

            <!-- CARD 2: LIST TABLE -->
            <div id="bonus-deduction-records-table" style="background: rgba(15, 23, 42, 0.7); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; padding: 1.5rem;">
              <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.25rem;">
                <div>
                  <h3 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin: 0;">📋 Employee Bonus & Deduction Records</h3>
                  <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.2rem 0 0 0;">View, filter, and manage assigned bonuses and deductions per salary period.</p>
                </div>

                <!-- FILTERS -->
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                  <!-- TYPE FILTER -->
                  <select v-model="bonusDeductionTypeFilter" style="padding: 0.45rem 0.75rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.8rem; cursor: pointer;">
                    <option value="all">All Types</option>
                    <option value="bonus">🎁 Bonus Only</option>
                    <option value="deduction">🔻 Deduction Only</option>
                  </select>

                  <!-- EMPLOYEE FILTER -->
                  <select v-model="bonusDeductionEmployeeFilter" style="padding: 0.45rem 0.75rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.8rem; cursor: pointer;">
                    <option value="all">All Employees</option>
                    <option v-for="emp in availableSalaryEmployeeOptions" :key="emp.id" :value="String(emp.id)">
                      {{ emp.full_name || emp.username }}
                    </option>
                  </select>

                  <!-- PERIOD FILTER -->
                  <select v-model="bonusDeductionPeriodFilter" style="padding: 0.45rem 0.75rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.8rem; cursor: pointer;">
                    <option value="all">All Periods</option>
                    <option v-for="p in payrollPeriodOptions" :key="p.key" :value="p.key">
                      {{ p.label }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- TABLE -->
              <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                  <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; background: rgba(30, 41, 59, 0.5);">
                      <th style="padding: 0.75rem 0.85rem;">Type</th>
                      <th style="padding: 0.75rem 0.85rem;">Employee</th>
                      <th style="padding: 0.75rem 0.85rem;">Bonus / Deduction Name</th>
                      <th style="padding: 0.75rem 0.85rem;">Amount (₱)</th>
                      <th style="padding: 0.75rem 0.85rem;">Target Salary Period</th>
                      <th style="padding: 0.75rem 0.85rem;">Created By / Date</th>
                      <th style="padding: 0.75rem 0.85rem; text-align: center;">Status</th>
                      <th v-if="canAccessMenu('payroll_approver')" style="padding: 0.75rem 0.85rem; text-align: center;">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="filteredBonusDeductionList.length === 0">
                      <td :colspan="canAccessMenu('payroll_approver') ? 8 : 7" style="padding: 2rem; text-align: center; color: #64748b;">No bonus or deduction records found.</td>
                    </tr>
                    <tr v-for="item in filteredBonusDeductionList" :key="item.id" style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.86rem;">
                      <!-- TYPE -->
                      <td style="padding: 0.85rem;">
                        <span v-if="item.type === 'bonus'" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                          🎁 Bonus (+)
                        </span>
                        <span v-else style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                          🔻 Deduction (-)
                        </span>
                      </td>

                      <!-- EMPLOYEE -->
                      <td style="padding: 0.85rem; font-weight: 700; color: #fff;">
                        <div>{{ item.employee_name }}</div>
                        <div style="font-size: 0.72rem; color: #94a3b8;">@{{ item.username }}</div>
                      </td>

                      <!-- NAME & REMARKS -->
                      <td style="padding: 0.85rem;">
                        <div style="font-weight: 700; color: #e2e8f0;">{{ item.name }}</div>
                        <div v-if="item.notes" style="font-size: 0.74rem; color: #94a3b8;">{{ item.notes }}</div>
                      </td>

                      <!-- AMOUNT -->
                      <td style="padding: 0.85rem; font-weight: 800; font-family: monospace;">
                        <span :style="{ color: item.type === 'bonus' ? '#34d399' : '#f87171' }">
                          {{ item.type === 'bonus' ? '+' : '-' }}₱{{ (parseFloat(item.amount) || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
                        </span>
                      </td>

                      <!-- SALARY PERIOD -->
                      <td style="padding: 0.85rem;">
                        <span style="background: rgba(192, 132, 252, 0.15); color: #c084fc; border: 1px solid rgba(192, 132, 252, 0.3); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                          📅 {{ getPeriodLabel(item.period_key) }}
                        </span>
                      </td>

                      <!-- CREATED BY / DATE -->
                      <td style="padding: 0.85rem; color: #94a3b8; font-size: 0.78rem;">
                        <div>✍️ {{ item.created_by || 'Admin' }}</div>
                        <div>🕒 {{ item.created_at }}</div>
                      </td>

                      <!-- STATUS -->
                      <td style="padding: 0.85rem; text-align: center;">
                        <label class="toggle-switch" style="cursor: pointer; margin: 0; display: inline-block;" title="Toggle Status (On/Off)">
                          <input type="checkbox" :checked="item.is_active" @change="toggleBonusDeductionStatus(item)" />
                          <span class="toggle-slider"></span>
                        </label>
                      </td>

                      <!-- ACTION -->
                      <td v-if="canAccessMenu('payroll_approver')" style="padding: 0.85rem; text-align: center;">
                        <button 
                          type="button" 
                          @click="deleteBonusDeduction(item.id)" 
                          title="Delete Record"
                          style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 0.3rem 0.5rem; border-radius: 6px; font-size: 0.8rem; cursor: pointer;"
                        >
                          🗑️
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </div>

        <!-- 🌙 OT & ND RATES MANAGEMENT VIEW -->
        <div v-else-if="activeView === 'payroll_ot_nd'" class="page-view glass">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
              <div>
                <h2 class="view-heading" style="margin: 0; display: flex; align-items: center; gap: 0.6rem;">
                  <span>🌙</span> Overtime & Night Differential (OT & ND) Rates
                </h2>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem;">
                  Configure dynamic rate multipliers for Overtime and Night Differential (10:00 PM - 06:00 AM) applied across payroll.
                </p>
              </div>

              <div style="display: flex; gap: 0.75rem;">
                <button 
                  type="button" 
                  @click="resetOtNdRatesToDefault" 
                  class="btn btn-secondary" 
                  style="font-size: 0.82rem; padding: 0.6rem 1.1rem; border-radius: 10px;"
                >
                  🔄 Reset Defaults
                </button>
                <button 
                  type="button" 
                  @click="saveOtNdRatesToStorage" 
                  class="btn btn-primary" 
                  style="font-size: 0.82rem; padding: 0.6rem 1.25rem; border-radius: 10px; background: linear-gradient(135deg, #a855f7, #7e22ce); border: none; font-weight: 700;"
                >
                  💾 Save & Apply Dynamic Rates
                </button>
              </div>
            </div>

            <!-- SUCCESS ALERT -->
            <div v-if="payrollOtNdSuccess" style="margin-bottom: 1.25rem; padding: 0.85rem 1.25rem; background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.4); border-radius: 12px; color: #c084fc; display: flex; align-items: center; justify-content: space-between; font-size: 0.88rem; font-weight: 600;">
              <span>✅ {{ payrollOtNdSuccess }}</span>
              <button @click="payrollOtNdSuccess = ''" style="background: transparent; border: none; color: #c084fc; font-size: 1rem; cursor: pointer;">✕</button>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem;">
              
              <!-- CARD 1: OVERTIME RATE MULTIPLIERS -->
              <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(168, 85, 247, 0.25);">
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem;">
                  <span style="font-size: 1.3rem;">⏰</span>
                  <h3 style="font-size: 1.05rem; font-weight: 700; color: #c084fc; margin: 0;">Overtime Rate Multipliers</h3>
                </div>

                <div style="display: flex; flex-direction: column; gap: 1.1rem;">
                  <!-- REGULAR OT -->
                  <div>
                    <label style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.35rem;">
                      <span>Regular Workday Overtime Rate:</span>
                      <strong style="color: #c084fc;">{{ otNdRates.regularOtMultiplier }}x ({{ (otNdRates.regularOtMultiplier * 100).toFixed(0) }}%)</strong>
                    </label>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                      <input 
                        type="number" 
                        step="0.05" 
                        min="1" 
                        max="5" 
                        v-model.number="otNdRates.regularOtMultiplier" 
                        style="width: 100%; padding: 0.6rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(168, 85, 247, 0.3); color: #fff; font-size: 0.9rem; font-weight: 700;"
                      />
                      <span style="font-size: 0.8rem; color: #94a3b8; white-space: nowrap;">multiplier</span>
                    </div>
                    <span style="font-size: 0.72rem; color: #94a3b8;">Standard statutory minimum is 1.25x (125% hourly rate)</span>
                  </div>

                  <!-- RESTDAY OT -->
                  <div>
                    <label style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.35rem;">
                      <span>Rest Day / Special Day Overtime Rate:</span>
                      <strong style="color: #c084fc;">{{ otNdRates.restdayOtMultiplier }}x ({{ (otNdRates.restdayOtMultiplier * 100).toFixed(0) }}%)</strong>
                    </label>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                      <input 
                        type="number" 
                        step="0.05" 
                        min="1" 
                        max="5" 
                        v-model.number="otNdRates.restdayOtMultiplier" 
                        style="width: 100%; padding: 0.6rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(168, 85, 247, 0.3); color: #fff; font-size: 0.9rem; font-weight: 700;"
                      />
                      <span style="font-size: 0.8rem; color: #94a3b8; white-space: nowrap;">multiplier</span>
                    </div>
                    <span style="font-size: 0.72rem; color: #94a3b8;">Standard statutory minimum is 1.30x (130% hourly rate)</span>
                  </div>

                  <!-- HOLIDAY OT -->
                  <div>
                    <label style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.35rem;">
                      <span>Regular Holiday Overtime Rate:</span>
                      <strong style="color: #c084fc;">{{ otNdRates.holidayOtMultiplier }}x ({{ (otNdRates.holidayOtMultiplier * 100).toFixed(0) }}%)</strong>
                    </label>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                      <input 
                        type="number" 
                        step="0.05" 
                        min="1" 
                        max="5" 
                        v-model.number="otNdRates.holidayOtMultiplier" 
                        style="width: 100%; padding: 0.6rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(168, 85, 247, 0.3); color: #fff; font-size: 0.9rem; font-weight: 700;"
                      />
                      <span style="font-size: 0.8rem; color: #94a3b8; white-space: nowrap;">multiplier</span>
                    </div>
                    <span style="font-size: 0.72rem; color: #94a3b8;">Standard statutory regular holiday rate is 2.00x (200% hourly rate)</span>
                  </div>
                </div>
              </div>

              <!-- CARD 2: NIGHT DIFFERENTIAL (ND) RATE -->
              <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(59, 130, 246, 0.3);">
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem;">
                  <span style="font-size: 1.3rem;">🌙</span>
                  <h3 style="font-size: 1.05rem; font-weight: 700; color: #60a5fa; margin: 0;">Night Differential (ND) Rate</h3>
                </div>

                <div style="display: flex; flex-direction: column; gap: 1.1rem;">
                  <!-- ND PERCENTAGE -->
                  <div>
                    <label style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.35rem;">
                      <span>Night Differential Addition Rate (%):</span>
                      <strong style="color: #60a5fa;">+{{ otNdRates.nightDiffPercentage }}% Additional Pay</strong>
                    </label>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                      <input 
                        type="number" 
                        step="1" 
                        min="0" 
                        max="100" 
                        v-model.number="otNdRates.nightDiffPercentage" 
                        style="width: 100%; padding: 0.6rem 0.85rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(59, 130, 246, 0.3); color: #fff; font-size: 0.9rem; font-weight: 700;"
                      />
                      <span style="font-size: 0.88rem; color: #60a5fa; font-weight: 700;">%</span>
                    </div>
                    <span style="font-size: 0.72rem; color: #94a3b8;">Statutory minimum is 10% additional hourly rate for hours in 10:00 PM - 06:00 AM</span>
                  </div>

                  <!-- TIME WINDOW BOX -->
                  <div style="padding: 1rem; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 12px;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #93c5fd; margin-bottom: 0.4rem;">
                      ⏱️ Automatic Night Shift Window Rule:
                    </div>
                    <p style="font-size: 0.78rem; color: #cbd5e1; margin: 0; line-height: 1.4;">
                      Night Differential automatically applies to any work shift or overtime hours falling between <strong style="color: #fff;">10:00 PM (22:00)</strong> and <strong style="color: #fff;">06:00 AM (06:00)</strong>.
                    </p>
                  </div>
                </div>
              </div>

            </div>

            <!-- LIVE IMPACT CALCULATOR PREVIEW -->
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.1);">
              <h3 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                <span>📊</span> Dynamic Rates Impact Simulator (Sample ₱35,000 Monthly Salary)
              </h3>
              
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
                <div style="padding: 1rem; background: rgba(0,0,0,0.25); border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
                  <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">Hourly Base Rate</div>
                  <div style="font-size: 1.1rem; font-weight: 800; color: #38bdf8;">₱198.86 / hr</div>
                  <div style="font-size: 0.7rem; color: #64748b;">(₱35,000 / 22 days / 8 hrs)</div>
                </div>

                <div style="padding: 1rem; background: rgba(0,0,0,0.25); border-radius: 10px; border: 1px solid rgba(168, 85, 247, 0.2);">
                  <div style="font-size: 0.75rem; color: #c084fc; font-weight: 600;">1 Hr Regular Overtime</div>
                  <div style="font-size: 1.1rem; font-weight: 800; color: #c084fc;">₱{{ (198.8636 * otNdRates.regularOtMultiplier).toFixed(2) }}</div>
                  <div style="font-size: 0.7rem; color: #a78bfa;">(₱198.86 × {{ otNdRates.regularOtMultiplier }}x)</div>
                </div>

                <div style="padding: 1rem; background: rgba(0,0,0,0.25); border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.2);">
                  <div style="font-size: 0.75rem; color: #60a5fa; font-weight: 600;">1 Hr Night Differential (10PM-6AM)</div>
                  <div style="font-size: 1.1rem; font-weight: 800; color: #60a5fa;">+₱{{ (198.8636 * (otNdRates.nightDiffPercentage / 100)).toFixed(2) }}</div>
                  <div style="font-size: 0.7rem; color: #93c5fd;">(+{{ otNdRates.nightDiffPercentage }}% additional hourly pay)</div>
                </div>

                <div style="padding: 1rem; background: rgba(0,0,0,0.25); border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.2);">
                  <div style="font-size: 0.75rem; color: #34d399; font-weight: 600;">1 Hr Night Shift Overtime</div>
                  <div style="font-size: 1.1rem; font-weight: 800; color: #34d399;">₱{{ (198.8636 * otNdRates.regularOtMultiplier + 198.8636 * (otNdRates.nightDiffPercentage / 100)).toFixed(2) }}</div>
                  <div style="font-size: 0.7rem; color: #6ee7b7;">(OT Pay + Night Diff Pay combined)</div>
                </div>
              </div>
            </div>

            <!-- ANIMATED BONUS / DEDUCTION RESULT MODAL POPUP (SUCCESS / FAIL) -->
            <Transition name="fade">
              <div 
                v-if="showBonusDeductionModal" 
                style="position: fixed; inset: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(10px); padding: 1.5rem;"
                @click.self="showBonusDeductionModal = false"
              >
                <div 
                  style="width: 100%; max-width: 480px; background: rgba(30, 41, 59, 0.95); border-radius: 24px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); overflow: hidden; animation: popInModal 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);"
                >
                  <!-- MODAL HEADER ANIMATED ICON -->
                  <div style="padding: 2.25rem 2rem 1.25rem; text-align: center; display: flex; flex-direction: column; align-items: center;">
                    
                    <!-- SUCCESS ANIMATED ICON -->
                    <div 
                      v-if="bonusDeductionModalStatus === 'success'" 
                      style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.3)); border: 2px solid #10b981; display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; box-shadow: 0 0 30px rgba(16, 185, 129, 0.4); animation: pulseGlowSuccess 2s infinite ease-in-out;"
                    >
                      <svg style="width: 44px; height: 44px; color: #34d399; filter: drop-shadow(0 2px 8px rgba(16, 185, 129, 0.5));" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
                      </svg>
                    </div>

                    <!-- ERROR ANIMATED ICON -->
                    <div 
                      v-else 
                      style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(185, 28, 28, 0.3)); border: 2px solid #ef4444; display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; box-shadow: 0 0 30px rgba(239, 68, 68, 0.4); animation: shakeError 0.4s ease-in-out;"
                    >
                      <svg style="width: 44px; height: 44px; color: #f87171; filter: drop-shadow(0 2px 8px rgba(239, 68, 68, 0.5));" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </div>

                    <h3 style="font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0 0 0.5rem 0;">
                      {{ bonusDeductionModalTitle }}
                    </h3>
                    <p style="font-size: 0.88rem; color: #94a3b8; margin: 0; line-height: 1.5;">
                      {{ bonusDeductionModalMessage }}
                    </p>
                  </div>

                  <!-- RECORD DETAILS SUMMARY (IF SUCCESS RECORD EXISTS) -->
                  <div 
                    v-if="bonusDeductionModalDetails" 
                    style="margin: 0 1.5rem 1.5rem; background: rgba(15, 23, 42, 0.6); padding: 1.1rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);"
                  >
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; font-size: 0.82rem; color: #94a3b8;">
                      <span>👤 Employee:</span>
                      <strong style="color: #fff;">{{ bonusDeductionModalDetails.employee_name }}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; font-size: 0.82rem; color: #94a3b8;">
                      <span>🏷️ Record Type:</span>
                      <span :style="{ color: bonusDeductionModalDetails.type === 'bonus' ? '#34d399' : '#f87171', fontWeight: '700' }">
                        {{ bonusDeductionModalDetails.type === 'bonus' ? '🎁 Bonus (+)' : '🔻 Deduction (-)' }}
                      </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; font-size: 0.82rem; color: #94a3b8;">
                      <span>💰 Amount:</span>
                      <strong :style="{ color: bonusDeductionModalDetails.type === 'bonus' ? '#34d399' : '#f87171', fontFamily: 'monospace', fontSize: '1rem' }">
                        {{ bonusDeductionModalDetails.type === 'bonus' ? '+' : '-' }}₱{{ bonusDeductionModalDetails.amount.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                      </strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: #94a3b8;">
                      <span>📅 Period:</span>
                      <span style="color: #c084fc; font-weight: 700;">{{ getPeriodLabel(bonusDeductionModalDetails.period_key) }}</span>
                    </div>
                  </div>

                  <!-- MODAL FOOTER BUTTONS -->
                  <div style="padding: 1.25rem 1.5rem; background: rgba(15, 23, 42, 0.5); border-top: 1px solid rgba(255,255,255,0.08); display: flex; gap: 0.75rem; justify-content: flex-end;">
                    <button 
                      @click="showBonusDeductionModal = false" 
                      type="button" 
                      class="btn btn-secondary" 
                      style="padding: 0.65rem 1.25rem; font-weight: 700; border-radius: 10px; font-size: 0.85rem;"
                    >
                      Close
                    </button>
                    <button 
                      v-if="bonusDeductionModalStatus === 'success'" 
                      @click="showBonusDeductionModal = false; scrollToBonusDeductionTable()" 
                      type="button" 
                      class="btn btn-primary" 
                      style="padding: 0.65rem 1.25rem; font-weight: 700; border-radius: 10px; font-size: 0.85rem; background: linear-gradient(135deg, #38bdf8, #0284c7); border: none; cursor: pointer;"
                    >
                      📋 View Records Table
                    </button>
                  </div>
                </div>
              </div>
            </Transition>
          </div>

        <!-- VIEW: SUPPORT - CHAT SUPPORT -->
        <div v-else-if="activeView === 'support_chat'" class="page-view glass support-page-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🎧 Live Chat Support Console</h2>
              <p class="view-subheading">Manage incoming waiting queues, assist active user sessions concurrently, and monitor daily support work history</p>
            </div>
          </div>

          <!-- TOP SUPPORT TABS -->
          <div style="display: flex; gap: 0.75rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.75rem;">
            <button 
              @click="activeSupportTab = 'queue'"
              type="button" 
              :style="{
                padding: '0.65rem 1.25rem',
                borderRadius: '10px',
                fontWeight: '700',
                fontSize: '0.9rem',
                border: 'none',
                cursor: 'pointer',
                background: activeSupportTab === 'queue' ? 'linear-gradient(135deg, #3b82f6, #1d4ed8)' : 'rgba(15, 23, 42, 0.6)',
                color: '#fff',
                boxShadow: activeSupportTab === 'queue' ? '0 4px 15px rgba(59, 130, 246, 0.4)' : 'none'
              }"
            >
              📥 Waiting Queue
              <span v-if="supportWaitingQueue.length > 0" style="background: #ef4444; color: #fff; padding: 0.15rem 0.55rem; border-radius: 20px; font-size: 0.75rem; margin-left: 0.4rem;">{{ supportWaitingQueue.length }}</span>
            </button>

            <button 
              @click="activeSupportTab = 'active'"
              type="button" 
              :style="{
                padding: '0.65rem 1.25rem',
                borderRadius: '10px',
                fontWeight: '700',
                fontSize: '0.9rem',
                border: 'none',
                cursor: 'pointer',
                background: activeSupportTab === 'active' ? 'linear-gradient(135deg, #10b981, #047857)' : 'rgba(15, 23, 42, 0.6)',
                color: '#fff',
                boxShadow: activeSupportTab === 'active' ? '0 4px 15px rgba(16, 185, 129, 0.4)' : 'none'
              }"
            >
              💬 Active Live Chat Sessions
              <span v-if="activeSupportSessions.length > 0" style="background: rgba(255,255,255,0.2); color: #fff; padding: 0.15rem 0.55rem; border-radius: 20px; font-size: 0.75rem; margin-left: 0.4rem;">{{ activeSupportSessions.length }}</span>
            </button>

            <button 
              @click="activeSupportTab = 'monitor'"
              type="button" 
              :style="{
                padding: '0.65rem 1.25rem',
                borderRadius: '10px',
                fontWeight: '700',
                fontSize: '0.9rem',
                border: 'none',
                cursor: 'pointer',
                background: activeSupportTab === 'monitor' ? 'linear-gradient(135deg, #8b5cf6, #6d28d9)' : 'rgba(15, 23, 42, 0.6)',
                color: '#fff',
                boxShadow: activeSupportTab === 'monitor' ? '0 4px 15px rgba(139, 92, 246, 0.4)' : 'none'
              }"
            >
              📊 Daily Support Work Monitor
              <span style="background: rgba(255,255,255,0.2); color: #fff; padding: 0.15rem 0.55rem; border-radius: 20px; font-size: 0.75rem; margin-left: 0.4rem;">{{ dailySupportMonitorLogs.length }} Chatted Today</span>
            </button>
          </div>

          <!-- TAB 1: WAITING QUEUE -->
          <div v-if="activeSupportTab === 'queue'">
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                  <span>📥</span> Support Request Queue Channel
                </h3>
                <span style="font-size: 0.8rem; color: #94a3b8;">
                  Users currently waiting in queue for support agent assistance
                </span>
              </div>

              <div v-if="supportWaitingQueue.length === 0" style="text-align: center; padding: 3rem 1rem; color: #94a3b8;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🎉</div>
                <h4 style="font-size: 1.1rem; color: #fff; font-weight: 700;">No Users in Waiting Queue</h4>
                <p style="font-size: 0.85rem; margin-top: 0.3rem;">All support channels are currently clear!</p>
              </div>

              <div v-else style="display: flex; flex-direction: column; gap: 1rem;">
                <div 
                  v-for="qItem in supportWaitingQueue" 
                  :key="qItem.id"
                  style="padding: 1.25rem; border-radius: 12px; background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem;"
                >
                  <div style="flex: 1; min-width: 260px;">
                    <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.35rem;">
                      <span style="font-size: 1rem; font-weight: 800; color: #fff;">{{ qItem.userName }}</span>
                      <span style="font-size: 0.75rem; color: #38bdf8;">@{{ qItem.username }}</span>
                      <span style="font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 6px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-weight: 700;">{{ qItem.roleLabel }}</span>
                      <span v-if="qItem.priority === 'Urgent'" style="font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 6px; background: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: 800;">🔥 Urgent</span>
                    </div>

                    <div style="font-size: 0.88rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.25rem;">
                      Topic: {{ qItem.topic }}
                    </div>

                    <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.4;">
                      "{{ qItem.messageSnippet }}"
                    </div>
                  </div>

                  <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="text-align: right; font-size: 0.75rem; color: #94a3b8;">
                      <div>Waiting {{ qItem.waitTime }}</div>
                      <div style="color: #64748b;">Created {{ qItem.createdTime }}</div>
                    </div>

                    <button 
                      @click="claimSupportQueueItem(qItem)" 
                      type="button" 
                      class="btn btn-primary" 
                      style="padding: 0.6rem 1.25rem; font-weight: 700; font-size: 0.85rem; border-radius: 8px; display: inline-flex; align-items: center; gap: 0.4rem; cursor: pointer; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);"
                    >
                      <span>🎧 Accept & Start Chat</span>
                    </button>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- TAB 2: ACTIVE LIVE CHAT WORKSPACE -->
          <div v-else-if="activeSupportTab === 'active'">
            <div v-if="!currentActiveSession" style="text-align: center; padding: 4rem 1rem; color: #94a3b8;" class="glass-card">
              <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">💬</div>
              <h4 style="font-size: 1.1rem; color: #fff; font-weight: 700;">No Active Live Chat Session Selected</h4>
              <p style="font-size: 0.85rem; margin-top: 0.3rem;">Select an item from the waiting queue to begin assisting a user!</p>
              <button @click="activeSupportTab = 'queue'" class="btn btn-primary" style="margin-top: 1rem; padding: 0.6rem 1.25rem;">Go to Waiting Queue</button>
            </div>

            <div v-else style="display: grid; grid-template-columns: 280px 1fr; gap: 1.25rem;">
              
              <!-- LEFT SIDEBAR: ACTIVE CONCURRENT CHAT CHANNELS -->
              <div class="glass-card" style="padding: 1.25rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
                <h4 style="font-size: 0.88rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.85rem;">
                  Active Concurrent Channels ({{ activeSupportSessions.length }})
                </h4>

                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <div 
                    v-for="sess in activeSupportSessions"
                    :key="sess.id"
                    @click="currentActiveSessionId = sess.id"
                    :style="{
                      padding: '0.85rem',
                      borderRadius: '10px',
                      cursor: 'pointer',
                      background: currentActiveSessionId === sess.id ? 'rgba(56, 189, 248, 0.18)' : 'rgba(0,0,0,0.25)',
                      border: currentActiveSessionId === sess.id ? '1px solid rgba(56, 189, 248, 0.4)' : '1px solid rgba(255,255,255,0.05)'
                    }"
                  >
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                      <div style="font-size: 0.88rem; font-weight: 700; color: #fff;">{{ sess.userName }}</div>
                      <span style="font-size: 0.68rem; padding: 0.1rem 0.45rem; border-radius: 4px; background: rgba(56, 189, 248, 0.2); color: #38bdf8; font-weight: 600;">
                        🎧 {{ sess.agentName || 'Agent' }}
                      </span>
                    </div>
                    <div style="font-size: 0.72rem; color: #38bdf8;">{{ sess.roleLabel }}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ sess.topic }}</div>
                  </div>
                </div>
              </div>

              <!-- RIGHT: LIVE CHAT MESSAGING CONSOLE -->
              <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); display: flex; flex-direction: column; height: 580px;">
                
                <!-- CHAT HEADER -->
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.85rem; margin-bottom: 1rem;">
                  <div>
                    <div style="display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;">
                      <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff;">{{ currentActiveSession.userName }}</h3>
                      <span style="font-size: 0.75rem; color: #38bdf8;">@{{ currentActiveSession.username }}</span>
                      <span style="font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 6px; background: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: 700;">🟢 Live Session</span>
                      <span v-if="currentActiveSession.agentName" style="font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 6px; background: rgba(56, 189, 248, 0.2); color: #38bdf8; font-weight: 700;">Agent: {{ currentActiveSession.agentName }}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #f59e0b; margin-top: 0.15rem;">Topic: {{ currentActiveSession.topic }}</div>
                  </div>

                  <div style="display: flex; gap: 0.6rem;">
                    <button @click="resolveSupportSession(currentActiveSession)" type="button" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.82rem; font-weight: 700; border-radius: 8px; background: linear-gradient(135deg, #10b981, #047857);">
                      ✅ Resolve & Complete
                    </button>
                  </div>
                </div>

                <!-- CHAT MESSAGES SCROLL AREA -->
                <div style="flex: 1; overflow-y: auto; padding: 0.75rem; background: rgba(0,0,0,0.3); border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.85rem;">
                  <div 
                    v-for="msg in currentActiveSession.messages" 
                    :key="msg.id"
                    :style="{
                      alignSelf: msg.sender === 'agent' ? 'flex-end' : 'flex-start',
                      maxWidth: '75%'
                    }"
                  >
                    <div style="font-size: 0.7rem; color: #94a3b8; margin-bottom: 0.15rem;" :style="{ textAlign: msg.sender === 'agent' ? 'right' : 'left' }">
                      {{ msg.senderName }} • {{ msg.time }}
                    </div>

                    <div 
                      :style="{
                        padding: '0.75rem 1rem',
                        borderRadius: msg.sender === 'agent' ? '14px 14px 2px 14px' : '14px 14px 14px 2px',
                        background: msg.sender === 'agent' ? 'linear-gradient(135deg, #3b82f6, #1d4ed8)' : 'rgba(30, 41, 59, 0.85)',
                        border: msg.sender === 'agent' ? 'none' : '1px solid rgba(255,255,255,0.1)',
                        color: '#fff',
                        fontSize: '0.88rem',
                        lineHeight: '1.45'
                      }"
                    >
                      {{ msg.text }}
                    </div>
                  </div>
                </div>

                <!-- QUICK CANNED RESPONSES -->
                <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.75rem;">
                  <span style="font-size: 0.72rem; color: #94a3b8; align-self: center;">Quick Replies:</span>
                  <button @click="sendCannedResponse('Hello! How can I assist you today?')" type="button" style="font-size: 0.72rem; padding: 0.25rem 0.6rem; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; cursor: pointer;">
                    "Hello! How can I assist you today?"
                  </button>
                  <button @click="sendCannedResponse('Let me check your account details and transactions.')" type="button" style="font-size: 0.72rem; padding: 0.25rem 0.6rem; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; cursor: pointer;">
                    "Checking account details..."
                  </button>
                  <button @click="sendCannedResponse('Your support ticket has been resolved successfully!')" type="button" style="font-size: 0.72rem; padding: 0.25rem 0.6rem; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; cursor: pointer;">
                    "Resolved successfully!"
                  </button>
                </div>

                <!-- INPUT & SEND ACTION -->
                <div style="display: flex; gap: 0.75rem;">
                  <input 
                    v-model="supportChatMessageInput"
                    @keyup.enter="sendSupportMessage"
                    type="text" 
                    placeholder="Type support reply message..." 
                    style="flex: 1; padding: 0.75rem 1rem; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: #fff; font-size: 0.88rem;"
                  />
                  <button @click="sendSupportMessage" type="button" class="btn btn-primary" style="padding: 0.75rem 1.5rem; font-weight: 700; border-radius: 10px;">
                    Send 🚀
                  </button>
                </div>

              </div>

            </div>
          </div>

          <!-- TAB 3: DAILY SUPPORT WORK MONITOR -->
          <div v-else-if="activeSupportTab === 'monitor'">
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <div>
                  <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                    <span>📊</span> Daily Support Work Monitor & History Log
                  </h3>
                  <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.15rem;">
                    Track and audit all user chat sessions completed daily by support agents
                  </p>
                </div>

                <div style="padding: 0.6rem 1rem; background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 10px; font-size: 0.85rem; color: #c084fc; font-weight: 700;">
                  Today Total Chatted: {{ dailySupportMonitorLogs.length }} Users
                </div>
              </div>

              <div class="table-responsive" style="max-height: 520px; overflow-y: auto; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
                <table class="data-table" style="width: 100%; border-collapse: collapse;">
                  <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.15); text-align: left; font-size: 0.85rem; color: #94a3b8; background: #0f172a;">
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">User</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Role</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Topic / Issue</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Session Span</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Duration</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Support Agent</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Outcome</th>
                      <th style="padding: 0.85rem 1rem; position: sticky; top: 0; background: #0f172a;">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="log in dailySupportMonitorLogs" 
                      :key="log.id"
                      style="border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.88rem;"
                    >
                      <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                        <div style="font-weight: 700; color: #fff;">{{ log.userName }}</div>
                        <div style="font-size: 0.75rem; color: #94a3b8;">@{{ log.username }}</div>
                      </td>

                      <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #38bdf8; font-weight: 600;">
                        {{ log.roleLabel }}
                      </td>

                      <td style="padding: 0.85rem 1rem; color: #f59e0b; font-weight: 600;">
                        {{ log.topic }}
                      </td>

                      <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #cbd5e1;">
                        {{ log.startTime }} - {{ log.endTime }}
                      </td>

                      <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #c084fc; font-weight: 600;">
                        ⏱️ {{ log.duration }}
                      </td>

                      <td style="padding: 0.85rem 1rem; white-space: nowrap; color: #e2e8f0;">
                        {{ log.agentName }}
                      </td>

                      <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                        <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 0.25rem 0.65rem; border-radius: 6px; font-weight: 700; font-size: 0.8rem;">
                          ✅ {{ log.outcome }}
                        </span>
                      </td>

                      <td style="padding: 0.85rem 1rem; white-space: nowrap;">
                        <button @click="selectedHistoryTranscriptModal = log" type="button" class="btn btn-ghost btn-sm" style="font-size: 0.78rem; padding: 0.25rem 0.65rem;">
                          👁️ View Transcript
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW: CREATE DEPARTMENT -->
        <div v-else-if="activeView === 'create_department'" class="page-view glass full-form-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🏢 Create & Manage Departments</h2>
              <p class="view-subheading">Define company departments used for employee categorization and role assignment</p>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <!-- FORM CARD -->
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                ➕ Add New Department
              </h3>

              <Transition name="fade">
                <div v-if="deptAlertMessage" :class="['alert', deptAlertStatus === 'success' ? 'alert-success' : 'alert-error']" style="margin-bottom: 1rem;">
                  {{ deptAlertMessage }}
                </div>
              </Transition>

              <form @submit.prevent="addDepartment" style="display: flex; flex-direction: column; gap: 1rem;">
                <div class="form-group">
                  <label class="form-label">Department Name *</label>
                  <input 
                    type="text" 
                    v-model="newDepartmentInput" 
                    required 
                    class="form-input" 
                    placeholder="e.g. Logistics, Marketing, Operations" 
                  />
                </div>

                <button type="submit" class="btn btn-primary" style="align-self: flex-start; padding: 0.65rem 1.5rem; border-radius: 8px;">
                  💾 Save Department
                </button>
              </form>
            </div>

            <!-- DEPARTMENTS LIST CARD -->
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between;">
                <span>📋 Active Departments ({{ departments.length }})</span>
              </h3>

              <div style="display: flex; flex-direction: column; gap: 0.75rem; max-height: 400px; overflow-y: auto;">
                <div 
                  v-for="dept in departments" 
                  :key="dept" 
                  class="glass" 
                  style="display: flex; justify-content: space-between; align-items: center; padding: 0.85rem 1rem; border-radius: 10px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);"
                >
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.2rem;">🏢</span>
                    <div>
                      <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">{{ dept }}</div>
                      <div style="font-size: 0.75rem; color: #94a3b8;">
                        {{ (departmentPositions[dept] || []).length }} Position(s) Defined
                      </div>
                    </div>
                  </div>

                  <button 
                    type="button" 
                    class="btn btn-ghost btn-sm" 
                    @click="removeDepartment(dept)"
                    style="color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.1);"
                    title="Delete Department"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW: CREATE POSITION -->
        <div v-else-if="activeView === 'create_position'" class="page-view glass full-form-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">📌 Create & Link Positions</h2>
              <p class="view-subheading">Define employee positions connected to specific company departments</p>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <!-- FORM CARD -->
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                ➕ Add New Position
              </h3>

              <Transition name="fade">
                <div v-if="posAlertMessage" :class="['alert', posAlertStatus === 'success' ? 'alert-success' : 'alert-error']" style="margin-bottom: 1rem;">
                  {{ posAlertMessage }}
                </div>
              </Transition>

              <form @submit.prevent="addPosition" style="display: flex; flex-direction: column; gap: 1rem;">
                <div class="form-group">
                  <label class="form-label">Select Department *</label>
                  <div class="select-wrapper">
                    <select v-model="selectedDeptForPosition" required class="form-select select-input">
                      <option value="" disabled selected>Select Department</option>
                      <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
                    </select>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">Position Title *</label>
                  <input 
                    type="text" 
                    v-model="newPositionInput" 
                    required 
                    class="form-input" 
                    placeholder="e.g. Lead Logistics Manager" 
                  />
                </div>

                <button type="submit" class="btn btn-primary" style="align-self: flex-start; padding: 0.65rem 1.5rem; border-radius: 8px;">
                  💾 Save Position
                </button>
              </form>
            </div>

            <!-- POSITIONS LIST CARD BY DEPARTMENT -->
            <div class="glass-card" style="padding: 1.5rem; border-radius: 16px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 1rem;">
                📋 Configured Positions per Department
              </h3>

              <div style="display: flex; flex-direction: column; gap: 1rem; max-height: 420px; overflow-y: auto;">
                <div v-for="dept in departments" :key="dept" style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <div style="font-size: 0.82rem; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.25rem;">
                    🏢 {{ dept }} Department
                  </div>

                  <div v-if="!departmentPositions[dept] || departmentPositions[dept].length === 0" style="font-size: 0.8rem; color: #64748b; font-style: italic; padding-left: 0.5rem;">
                    No positions defined yet for this department.
                  </div>

                  <div 
                    v-for="pos in departmentPositions[dept] || []" 
                    :key="pos" 
                    class="glass" 
                    style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0.85rem; border-radius: 8px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06);"
                  >
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                      <span style="font-size: 0.9rem;">📌</span>
                      <span style="font-weight: 600; color: #e2e8f0; font-size: 0.88rem;">{{ pos }}</span>
                      <span style="font-family: monospace; font-size: 0.72rem; color: #a5b4fc; background: rgba(99, 102, 241, 0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">
                        {{ pos.toLowerCase().replace(/\s+/g, '_') }}
                      </span>
                    </div>

                    <button 
                      type="button" 
                      class="btn btn-ghost btn-sm" 
                      @click="removePosition(dept, pos)"
                      style="color: #ef4444; padding: 0.2rem 0.5rem; font-size: 0.78rem;"
                      title="Delete Position"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- VIEW: SET ACCESS -->
        <div v-else-if="activeView === 'set_access'" class="page-view glass full-form-view">
          <div class="view-header">
            <div class="header-title-box">
              <h2 class="view-heading">🔐 Role & Menu Access Rights Setup</h2>
              <p class="view-subheading">Configure role permissions and menu access rights for company departments and administrative positions</p>
            </div>
          </div>

          <div class="glass-card" style="padding: 2rem; border-radius: 20px; background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255,255,255,0.12); margin-bottom: 2rem;">
            
            <!-- SELECT ROLE DROPDOWN -->
            <div class="role-select-form-group" style="margin-bottom: 1.75rem;">
              <label class="role-select-label" style="font-size: 0.95rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; display: block;">
                🏢 Select Department — Position to Configure:
              </label>
              <div class="role-select-wrapper">
                <select v-model="selectedRoleToConfigure" class="role-select-dropdown" @change="handleRoleSelectionChange">
                  <optgroup v-for="dept in departments" :key="dept" :label="'🏢 Department: ' + dept">
                    <option 
                      v-for="pos in (departmentPositions[dept] || [])" 
                      :key="dept + '-' + pos" 
                      :value="pos.trim().toLowerCase().replace(/\s+/g, '_')"
                    >
                      {{ dept }} — {{ pos }}
                    </option>
                  </optgroup>
                  <optgroup label="⚙️ System & Default Roles">
                    <option v-for="r in defaultRolesList" :key="r.key" :value="r.key">
                      {{ r.label }}
                    </option>
                  </optgroup>
                </select>
                <span class="select-arrow-icon">▼</span>
              </div>
              <p class="role-select-hint">
                Currently configuring menu access rights for <strong style="color: #38bdf8;">{{ getRoleLabel(selectedRoleToConfigure) }}</strong>. Toggle items ON or OFF below, then click Save Access Rights.
              </p>
            </div>

            <!-- COLLAPSIBLE / GROUPED MENU ACCESS RIGHTS SWITCHES -->
            <div class="menu-permissions-list">
              
              <!-- GROUP 1: EMPLOYEE MANAGEMENT -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('employee')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.employee ? '▼' : '►' }}</span>
                    <span class="perm-group-title">👔 Employee Management</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('employee') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('employee') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('employee') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('employee') ? 'FULL ACCESS' : (isGroupAnyEnabled('employee') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('employee') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('employee')" 
                        @change="toggleGroupMaster('employee', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.employee" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">👥</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Employee List</span>
                        <span class="perm-item-sub">Access registered employees table</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.employee_list" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">👤➕</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Add Employee</span>
                        <span class="perm-item-sub">Access employee registration form</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.add_employee" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 2: CORE ACCOUNTS -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('core')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.core ? '▼' : '►' }}</span>
                    <span class="perm-group-title">👥 User & Account Management</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('core') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('core') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('core') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('core') ? 'FULL ACCESS' : (isGroupAnyEnabled('core') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('core') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('core')" 
                        @change="toggleGroupMaster('core', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.core" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🏍️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Drivers</span>
                        <span class="perm-item-sub">Manage driver accounts and verifications</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.drivers" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">👤</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Passengers</span>
                        <span class="perm-item-sub">Manage passenger accounts</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.passengers" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">💻</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Admins</span>
                        <span class="perm-item-sub">Manage administrator privileges</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.admins" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 3: OPERATIONS & VERIFICATION -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('ops')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.ops ? '▼' : '►' }}</span>
                    <span class="perm-group-title">⚡ Operations & Verification</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('ops') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('ops') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('ops') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('ops') ? 'FULL ACCESS' : (isGroupAnyEnabled('ops') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('ops') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('ops')" 
                        @change="toggleGroupMaster('ops', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.ops" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">💳</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Top-up Requests</span>
                        <span class="perm-item-sub">Approve/reject balance top-ups</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.topups" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🚗</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Bookings</span>
                        <span class="perm-item-sub">Access ride booking history</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.bookings" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">📄</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Document Bookings</span>
                        <span class="perm-item-sub">Access document delivery history</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.doc_bookings" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">📈</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Financial Stats</span>
                        <span class="perm-item-sub">Access platform income analytics</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.stats" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 4: ACCOUNTING & FMS -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('accounting')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.accounting ? '▼' : '►' }}</span>
                    <span class="perm-group-title">💼 Accounting & Financial Management</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('accounting') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('accounting') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('accounting') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('accounting') ? 'FULL ACCESS' : (isGroupAnyEnabled('accounting') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('accounting') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('accounting')" 
                        @change="toggleGroupMaster('accounting', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.accounting" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">💼</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Accounting</span>
                        <span class="perm-item-sub">Access Financial Management System</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.accounting" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 5: ATTENDANCE & TIME TRACKING -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('attendance')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.attendance ? '▼' : '►' }}</span>
                    <span class="perm-group-title">⏰ Attendance & Time Tracking</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('attendance') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('attendance') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('attendance') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('attendance') ? 'FULL ACCESS' : (isGroupAnyEnabled('attendance') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('attendance') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('attendance')" 
                        @change="toggleGroupMaster('attendance', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.attendance" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">📋</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Time Sheet</span>
                        <span class="perm-item-sub">Access monthly attendance timesheet</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_timesheet" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">⏱️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Time Log</span>
                        <span class="perm-item-sub">Access daily time in/out logs</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_timelog" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">⏰</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Overtime</span>
                        <span class="perm-item-sub">Access overtime request approvals</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_overtime" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🏖️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Leave</span>
                        <span class="perm-item-sub">Access employee leave management</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_leave" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">📸</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Photo Verification Required</span>
                        <span class="perm-item-sub">Require camera photo capture modal on clock in / clock out</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_photo_verification" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🎉</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Holiday</span>
                        <span class="perm-item-sub">Access company holiday calendar</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_holiday" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch" style="border-top: 1px dashed rgba(255,255,255,0.12); padding-top: 0.75rem; margin-top: 0.5rem;">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🛡️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name" style="color: #60a5fa; font-weight: 700;">Attendance Approver Role</span>
                        <span class="perm-item-sub">Enable action column & approval controls in Attendance & Time Tracking</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.attendance_approver" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 6: PAYROLL SYSTEM -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('payroll')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.payroll ? '▼' : '►' }}</span>
                    <span class="perm-group-title">💵 Payroll System</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('payroll') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('payroll') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('payroll') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('payroll') ? 'FULL ACCESS' : (isGroupAnyEnabled('payroll') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('payroll') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('payroll')" 
                        @change="toggleGroupMaster('payroll', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.payroll" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">📅</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Working Schedule</span>
                        <span class="perm-item-sub">Access employee working shift schedules</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_schedule" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">💰</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Salary Setup</span>
                        <span class="perm-item-sub">Access base salary configurations</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_salary" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🏖️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Payroll Leave</span>
                        <span class="perm-item-sub">Access paid leave calculations</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_leave" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">⚡</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Generate Payroll</span>
                        <span class="perm-item-sub">Compute & disburse semi-monthly payroll</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_generate" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">💸</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Cash Advances</span>
                        <span class="perm-item-sub">Manage & approve employee cash advances</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_advances" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🏛️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Contributions</span>
                        <span class="perm-item-sub">Configure salary contributions & 50/50 employer match</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_contributions" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🌙</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">OT & ND Rates</span>
                        <span class="perm-item-sub">Configure dynamic rate multipliers for Overtime & Night Differential</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_ot_nd" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch" style="border-top: 1px dashed rgba(255,255,255,0.12); padding-top: 0.75rem; margin-top: 0.5rem;">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🛡️</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name" style="color: #34d399; font-weight: 700;">Payroll Approver Role</span>
                        <span class="perm-item-sub">Enable action column & approval controls in Payroll System</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.payroll_approver" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 7: LIVE SUPPORT -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('support')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.support ? '▼' : '►' }}</span>
                    <span class="perm-group-title">🎧 Live Chat Support</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('support') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('support') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('support') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('support') ? 'FULL ACCESS' : (isGroupAnyEnabled('support') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('support') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('support')" 
                        @change="toggleGroupMaster('support', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.support" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">💬</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Chat Support Console</span>
                        <span class="perm-item-sub">Access live customer chat console</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.support_chat" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 8: SETUP & PERMISSIONS -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('setup')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.setup ? '▼' : '►' }}</span>
                    <span class="perm-group-title">⚙️ Setup & Menu Access</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('setup') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('setup') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('setup') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('setup') ? 'FULL ACCESS' : (isGroupAnyEnabled('setup') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('setup') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('setup')" 
                        @change="toggleGroupMaster('setup', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.setup" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🏢</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Create Department</span>
                        <span class="perm-item-sub">Access department creation setup</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.create_department" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">📌</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Create Position</span>
                        <span class="perm-item-sub">Access position creation setup</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.create_position" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>

                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🔐</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">Set Access</span>
                        <span class="perm-item-sub">Access role permission configurator</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.set_access" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- GROUP 9: OVERVIEW DASHBOARD -->
              <div class="perm-group">
                <div class="perm-group-header" @click="togglePermGroup('overview')">
                  <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span class="perm-chevron">{{ isPermGroupOpen.overview ? '▼' : '►' }}</span>
                    <span class="perm-group-title">🌐 System Overview</span>
                    <span 
                      class="group-status-badge" 
                      :style="{
                        background: isGroupAnyEnabled('overview') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: isGroupAnyEnabled('overview') ? '#10b981' : '#f87171',
                        border: isGroupAnyEnabled('overview') ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                        padding: '0.15rem 0.6rem',
                        borderRadius: '20px',
                        fontSize: '0.72rem',
                        fontWeight: '700'
                      }"
                    >
                      {{ isGroupAllEnabled('overview') ? 'FULL ACCESS' : (isGroupAnyEnabled('overview') ? 'PARTIAL' : 'DISABLED') }}
                    </span>
                  </div>

                  <div style="display: flex; align-items: center; gap: 0.6rem;" @click.stop>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #cbd5e1; user-select: none;">Group Access</span>
                    <label class="toggle-switch" :title="isGroupAnyEnabled('overview') ? 'Disable all permissions in this group' : 'Enable all permissions in this group'">
                      <input 
                        type="checkbox" 
                        :checked="isGroupAnyEnabled('overview')" 
                        @change="toggleGroupMaster('overview', $event.target.checked)" 
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                <div v-show="isPermGroupOpen.overview" class="perm-group-body">
                  <div class="perm-item-switch">
                    <div class="perm-item-meta">
                      <span class="perm-item-icon">🌐</span>
                      <div class="perm-item-text">
                        <span class="perm-item-name">System Overview</span>
                        <span class="perm-item-sub">Access main system overview dashboard</span>
                      </div>
                    </div>
                    <label class="toggle-switch">
                      <input type="checkbox" v-model="menuSwitches.overview" />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              </div>

            </div>

            <!-- ERROR ALERT IF ANY -->
            <div v-if="saveAlertMessage && saveAlertStatus === 'error'" class="modal-save-alert error" style="margin-top: 1.5rem;">
              {{ saveAlertMessage }}
            </div>

            <!-- ACTION FOOTER BAR -->
            <div style="display: flex; justify-content: flex-end; align-items: center; gap: 1rem; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
              <button 
                type="button" 
                class="btn btn-primary save-perm-btn" 
                @click="saveRolePermissions"
                :disabled="isSavingPermissions"
                style="padding: 0.75rem 2.25rem; font-weight: 700; border-radius: 12px; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);"
              >
                <span v-if="isSavingPermissions">Saving...</span>
                <span v-else>💾 Save Access Rights</span>
              </button>
            </div>

          </div>


        </div>

      </main>
    </div>

      <!-- LIVE CAMERA ATTENDANCE CAPTURE MODAL -->
      <Transition name="fade">
        <div v-if="showCameraCaptureModal" class="modal-overlay" style="position: fixed; inset: 0; background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(10px); display: flex; align-items: center; justify-content: center; z-index: 10000; padding: 1rem;">
          <div class="glass-card" style="width: 100%; max-width: 440px; padding: 2rem; border-radius: 24px; background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255,255,255,0.18); text-align: center; position: relative; box-shadow: 0 25px 60px -12px rgba(0,0,0,0.8);">
            
            <button type="button" @click="cancelCameraPhotoCapture" style="position: absolute; top: 1.2rem; right: 1.2rem; background: rgba(255,255,255,0.1); border: none; color: #cbd5e1; width: 34px; height: 34px; border-radius: 50%; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s;" title="Close & Cancel">✕</button>

            <div style="font-size: 1.25rem; font-weight: 800; color: #fff; margin-bottom: 0.35rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
              <span>📸</span>
              <span>{{ cameraCaptureMode }} Photo Verification</span>
            </div>
            
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1.5rem; line-height: 1.4;">
              Position your face inside the camera frame below and click <strong>Capture Photo</strong> to proceed with your attendance {{ cameraCaptureMode }}.
            </p>

            <!-- CAMERA / PREVIEW VIEWPORT CONTAINER -->
            <div style="width: 280px; height: 280px; margin: 0 auto 1.5rem; border-radius: 20px; overflow: hidden; border: 3px solid #38bdf8; box-shadow: 0 0 25px rgba(56, 189, 248, 0.35); position: relative; background: #000; display: flex; align-items: center; justify-content: center;">
              
              <!-- LIVE VIDEO STREAM -->
              <video 
                v-show="!cameraCapturedPhoto && !cameraCaptureError" 
                ref="cameraVideoRef" 
                autoplay 
                playsinline 
                muted 
                style="width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1);"
              ></video>

              <!-- FACE OVERLAY GUIDELINE RING (WHEN STREAMING) -->
              <div v-if="!cameraCapturedPhoto && !cameraCaptureError" style="position: absolute; inset: 20px; border: 2px dashed rgba(56, 189, 248, 0.6); border-radius: 50%; pointer-events: none; box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);"></div>

              <!-- CAPTURED STILL PHOTO PREVIEW -->
              <img 
                v-if="cameraCapturedPhoto" 
                :src="cameraCapturedPhoto" 
                style="width: 100%; height: 100%; object-fit: cover;" 
                alt="Captured Face Photo" 
              />

              <!-- ERROR STATE IF CAMERA UNAPPROVED OR OFF -->
              <div v-if="cameraCaptureError" style="padding: 1.5rem; color: #f87171; font-size: 0.85rem; font-weight: 600; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📷⚠️</div>
                <div>{{ cameraCaptureError }}</div>
                <button type="button" @click="startCameraStream" style="margin-top: 1rem; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #60a5fa; padding: 0.4rem 0.85rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">
                  🔄 Retry Camera Access
                </button>
              </div>
            </div>

            <!-- ACTION BUTTONS -->
            <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
              <!-- WHEN LIVE STREAMING: SNAP BUTTON -->
              <template v-if="!cameraCapturedPhoto">
                <button 
                  type="button" 
                  @click="snapCameraSnapshot" 
                  :disabled="!!cameraCaptureError" 
                  style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: #fff; border: none; padding: 0.75rem 1.6rem; border-radius: 12px; font-weight: 700; font-size: 0.92rem; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transition: all 0.2s;"
                >
                  📸 Capture Photo
                </button>
                <button 
                  type="button" 
                  @click="cancelCameraPhotoCapture" 
                  style="background: rgba(255, 255, 255, 0.08); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.15); padding: 0.75rem 1.25rem; border-radius: 12px; font-weight: 600; font-size: 0.9rem; cursor: pointer;"
                >
                  Cancel
                </button>
              </template>

              <!-- WHEN STILL PHOTO IS CAPTURED: CONFIRM OR RETAKE -->
              <template v-else>
                <button 
                  type="button" 
                  @click="confirmCameraPhotoCapture" 
                  style="background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; padding: 0.75rem 1.6rem; border-radius: 12px; font-weight: 700; font-size: 0.92rem; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); transition: all 0.2s;"
                >
                  ✅ Confirm & Proceed
                </button>
                <button 
                  type="button" 
                  @click="retakeCameraSnapshot" 
                  style="background: rgba(245, 158, 11, 0.18); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.35); padding: 0.75rem 1.25rem; border-radius: 12px; font-weight: 700; font-size: 0.9rem; cursor: pointer; display: inline-flex; align-items: center; gap: 0.4rem;"
                >
                  🔄 Retake Photo
                </button>
              </template>
            </div>

          </div>
        </div>
      </Transition>

      <!-- ATTENDANCE VERIFICATION PHOTO MODAL -->
      <Transition name="fade">
        <div v-if="showPhotoModal" class="modal-overlay" @click.self="showPhotoModal = false" style="position: fixed; inset: 0; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 1rem;">
          <div class="glass-card" style="width: 100%; max-width: 420px; padding: 2rem; border-radius: 20px; background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255,255,255,0.15); text-align: center; position: relative; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);">
            <button type="button" @click="showPhotoModal = false" style="position: absolute; top: 1rem; right: 1rem; background: rgba(255,255,255,0.1); border: none; color: #cbd5e1; width: 32px; height: 32px; border-radius: 50%; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
            
            <div style="font-size: 1.15rem; font-weight: 800; color: #fff; margin-bottom: 0.25rem;">
              📸 {{ activePhotoMeta.title }} Photo Verification
            </div>
            <div style="font-size: 0.82rem; color: #94a3b8; margin-bottom: 1.25rem;">
              {{ activePhotoMeta.employeeName }} — {{ activePhotoMeta.date }} @ {{ activePhotoMeta.time }}
            </div>

            <!-- PHOTO CONTAINER -->
            <div style="width: 260px; height: 260px; margin: 0 auto 1.25rem; border-radius: 16px; overflow: hidden; border: 2px solid rgba(56, 189, 248, 0.4); box-shadow: 0 0 20px rgba(56, 189, 248, 0.25); position: relative; background: #000;">
              <img :src="activePhotoMeta.photoUrl" style="width: 100%; height: 100%; object-fit: cover;" alt="Attendance Photo" />
              <div style="position: absolute; bottom: 0.5rem; right: 0.5rem; background: rgba(16, 185, 129, 0.9); color: #fff; font-size: 0.7rem; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">
                ✅ VERIFIED USER
              </div>
            </div>

            <div style="font-size: 0.8rem; color: #cbd5e1; background: rgba(255,255,255,0.05); padding: 0.75rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); text-align: left;">
              <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 0.2rem;">📍 Verification Location</div>
              <div style="font-weight: 600; color: #e2e8f0; line-height: 1.3;">{{ activePhotoMeta.address || 'HQ - Metro Manila, PH' }}</div>
            </div>
          </div>
        </div>
      </Transition>

    <!-- BALANCE MODAL -->
    <div v-if="showBalanceModal" class="modal-overlay" @click.self="closeBalanceModal">
      <div class="modal-content glass">
        <h3 class="modal-title">
          {{ modalMode === 'add' ? '📈 Add Balance' : '📉 Deduct Balance' }}
        </h3>
        <p class="modal-desc">
          Enter amount to {{ modalMode === 'add' ? 'ADD to' : 'DEDUCT from' }} 
          <span class="modal-username">@{{ modalUser?.username }}</span>'s account (₱):
        </p>
        
        <div class="modal-input-group">
          <span class="modal-currency">₱</span>
          <input 
            ref="modalInputRef"
            type="number" 
            step="0.01" 
            min="0.01"
            v-model="modalAmountStr" 
            placeholder="0.00" 
            class="modal-input"
            @keyup.enter="confirmBalanceModal"
            @keyup.esc="closeBalanceModal"
          />
        </div>
        
        <div class="modal-btn-group">
          <button class="btn btn-ghost modal-btn-cancel" @click="closeBalanceModal">Cancel</button>
          <button 
            class="btn modal-btn-confirm" 
            :class="modalMode === 'add' ? 'confirm-add' : 'confirm-deduct'" 
            @click="confirmBalanceModal"
            :disabled="!isValidAmount"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>



    <!-- ACCESS RIGHTS SAVED SUCCESS POPUP MODAL -->
    <div v-if="showAccessSavedSuccessModal" class="modal-overlay access-success-overlay" @click.self="showAccessSavedSuccessModal = false">
      <div class="modal-content glass access-success-card">
        
        <!-- ANIMATED CHECKMARK ICON -->
        <div class="animated-checkmark-wrapper">
          <div class="checkmark-circle">
            <svg class="checkmark-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
              <circle class="checkmark-circle-bg" cx="26" cy="26" r="23" fill="none"/>
              <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
          </div>
        </div>

        <h3 class="access-success-title">Access Rights Saved!</h3>
        <p class="access-success-subtitle">
          Permissions updated successfully for <strong>{{ accessSavedSuccessDetails.roleLabel }}</strong>
        </p>

        <div class="access-success-details-box">
          <div class="details-row">
            <span class="details-label">Configured Role / Position:</span>
            <strong class="details-value">{{ accessSavedSuccessDetails.roleLabel }}</strong>
          </div>
          <div class="details-row" style="margin-top: 0.5rem;">
            <span class="details-label">Access State:</span>
            <span class="details-badge">🟢 Real-Time Sync Active</span>
          </div>
        </div>

        <button 
          type="button" 
          class="btn btn-primary access-success-btn" 
          @click="showAccessSavedSuccessModal = false"
        >
          <span>Great, Got it!</span>
        </button>

      </div>
    </div>

    <!-- PROOF ATTACHMENT PREVIEW MODAL -->
    <div v-if="selectedPreviewImage" class="modal-overlay" @click.self="selectedPreviewImage = null">
      <div class="modal-content glass preview-image-modal" style="max-width: 550px; padding: 1.25rem;">
        <div class="role-modal-header" style="padding-bottom: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <h3 class="modal-title" style="font-size: 1rem; color: #fff;">🖼️ Document Proof Attachment</h3>
          <button type="button" class="modal-close-btn" @click="selectedPreviewImage = null">✕</button>
        </div>
        <div class="preview-modal-body" style="padding-top: 1rem; text-align: center;">
          <img :src="selectedPreviewImage" alt="Document Proof" style="max-width: 100%; max-height: 70vh; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);" />
        </div>
      </div>
    </div>

    <!-- CHAT TRANSCRIPT HISTORY MODAL -->
    <div v-if="selectedHistoryTranscriptModal" class="modal-overlay" @click.self="selectedHistoryTranscriptModal = null">
      <div class="modal-content glass" style="max-width: 600px; width: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15); padding-bottom: 0.85rem; margin-bottom: 1rem;">
          <div>
            <h3 class="modal-title">📜 Conversation Transcript</h3>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.2rem;">
              User: <strong style="color: #fff;">{{ selectedHistoryTranscriptModal.userName }}</strong> ({{ selectedHistoryTranscriptModal.roleLabel }}) — Agent: {{ selectedHistoryTranscriptModal.agentName }}
            </p>
          </div>
          <button type="button" class="modal-close-btn" @click="selectedHistoryTranscriptModal = null">✕</button>
        </div>

        <div style="max-height: 380px; overflow-y: auto; padding: 0.85rem; background: rgba(0,0,0,0.3); border-radius: 12px; margin-bottom: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;">
          <div v-for="(t, idx) in selectedHistoryTranscriptModal.transcript" :key="idx" style="padding: 0.65rem 0.85rem; border-radius: 8px; background: rgba(255,255,255,0.05); font-size: 0.85rem; color: #e2e8f0;">
            <strong style="color: #38bdf8;">{{ t.sender }}:</strong> {{ t.text }}
          </div>
        </div>

        <div style="text-align: right;">
          <button class="btn btn-ghost" @click="selectedHistoryTranscriptModal = null">Close</button>
        </div>
      </div>
    </div>


  </div>
</template>


<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { getManilaDateString, getManilaTimeString, getManilaDateTimeString, formatInManila } from '../utils/timezone'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authApi } from '../api/auth'

const router = useRouter()
const auth   = useAuthStore()
const user   = computed(() => auth.user)

// SIDEBAR & NAVIGATION STATES
const isSidebarOpen = ref(true)
const isProfileDropdownOpen = ref(false)
const profileDropdownRef = ref(null)

const activeView = ref('dashboard') // 'dashboard' | 'employee_list' | 'add_employee' | 'drivers' | 'passengers' | 'admins' | 'topups' | 'bookings' | 'stats' | 'overview' | 'user_profile'
const showEmployeePassword = ref(false)

const isEmpSubmenuOpen = ref(false)
const isCoreSubmenuOpen = ref(false)
const isOpsSubmenuOpen = ref(false)
const isAccountingSubmenuOpen = ref(false)
const isAttendanceSubmenuOpen = ref(false)
const isPayrollSubmenuOpen = ref(false)
const isSupportSubmenuOpen = ref(true)
const isSetupSubmenuOpen = ref(true)

// CORE DATA STATES & USER CATEGORIZATION LOGIC
const users = ref([])

function isEmployeeUser(u) {
  if (!u) return false
  const role = (u.role || '').toLowerCase()
  return (
    !!u.department || 
    !!u.position || 
    (role !== 'passenger' && role !== 'driver' && role !== 'admin' && role !== 'super_admin')
  )
}

const employeeUsers = computed(() => (users.value || []).filter(u => isEmployeeUser(u)))

// WORKING SCHEDULE FORM & DATA STATE
const editingScheduleId = ref(null)
const scheduleForm = ref({
  employee_id: '',
  time_from: '08:00',
  time_to: '17:00'
})
const scheduleSuccess = ref('')
const scheduleError = ref('')
const assignedSchedules = ref([
  { id: 1, employee_id: 1, employee_name: 'Juan Dela Cruz', username: 'juan_dc', position: 'IT Admin', time_from: '08:00 AM', time_to: '05:00 PM', status: 'Active' },
  { id: 2, employee_id: 2, employee_name: 'Maria Santos', username: 'maria_s', position: 'Accountant', time_from: '09:00 AM', time_to: '06:00 PM', status: 'Active' }
])

const availableEmployeeOptions = computed(() => {
  const empList = employeeUsers.value || []
  const userList = users.value || []
  const list = empList.length > 0 ? [...empList] : [...userList]
  
  if (editingScheduleId.value) {
    const currentSched = assignedSchedules.value.find(s => s.id === editingScheduleId.value)
    if (currentSched) {
      const exists = list.some(u => 
        String(u.id) === String(scheduleForm.value.employee_id) || 
        String(u.id) === String(currentSched.employee_id) || 
        u.username === currentSched.username
      )
      if (!exists && currentSched.employee_name) {
        list.unshift({
          id: currentSched.employee_id || currentSched.username || currentSched.id,
          full_name: currentSched.employee_name,
          username: currentSched.username,
          position: currentSched.position || 'Employee',
          role: 'employee'
        })
      }
    }
  }
  return list
})

function format12HourTime(time24) {
  if (!time24) return ''
  const [hStr, mStr] = time24.split(':')
  let h = parseInt(hStr, 10)
  const ampm = h >= 12 ? 'PM' : 'AM'
  h = h % 12 || 12
  return `${h.toString().padStart(2, '0')}:${mStr} ${ampm}`
}

function parse12HourTo24Hour(time12) {
  if (!time12) return '08:00'
  const match = time12.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i)
  if (!match) return time12
  let [_, hrs, mins, ampm] = match
  let h = parseInt(hrs, 10)
  if (ampm.toUpperCase() === 'PM' && h < 12) h += 12
  if (ampm.toUpperCase() === 'AM' && h === 12) h = 0
  return `${h.toString().padStart(2, '0')}:${mins}`
}

function editSchedule(sched) {
  editingScheduleId.value = sched.id
  const pool = availableEmployeeOptions.value
  const targetEmp = pool.find(u => 
    (sched.employee_id && String(u.id) === String(sched.employee_id)) || 
    (sched.username && u.username?.toLowerCase() === sched.username?.toLowerCase()) ||
    (sched.employee_name && (u.full_name === sched.employee_name || (u.first_name + ' ' + u.last_name) === sched.employee_name))
  )
  
  if (targetEmp) {
    scheduleForm.value.employee_id = targetEmp.id
  } else {
    scheduleForm.value.employee_id = sched.employee_id || sched.username || ''
  }

  scheduleForm.value.time_from = parse12HourTo24Hour(sched.time_from)
  scheduleForm.value.time_to = parse12HourTo24Hour(sched.time_to)
  scheduleSuccess.value = ''
  scheduleError.value = ''
}

function cancelEditSchedule() {
  editingScheduleId.value = null
  scheduleForm.value = {
    employee_id: '',
    time_from: '08:00',
    time_to: '17:00'
  }
}

function submitWorkingSchedule() {
  scheduleSuccess.value = ''
  scheduleError.value = ''
  if (!scheduleForm.value.employee_id) {
    scheduleError.value = 'Please select an employee.'
    return
  }
  if (!scheduleForm.value.time_from || !scheduleForm.value.time_to) {
    scheduleError.value = 'Please specify both Time From and Time To.'
    return
  }
  
  const pool = availableEmployeeOptions.value
  const targetEmp = pool.find(u => String(u.id) === String(scheduleForm.value.employee_id) || u.username === scheduleForm.value.employee_id)
  const empId = targetEmp ? targetEmp.id : scheduleForm.value.employee_id
  const empName = targetEmp ? (targetEmp.full_name || (targetEmp.first_name ? targetEmp.first_name + ' ' + targetEmp.last_name : targetEmp.username)) : 'Selected Employee'
  const empUser = targetEmp ? targetEmp.username : 'employee'
  const empPos = targetEmp ? (targetEmp.position || targetEmp.role || 'Employee') : 'Employee'

  if (editingScheduleId.value) {
    const idx = assignedSchedules.value.findIndex(s => s.id === editingScheduleId.value)
    if (idx !== -1) {
      assignedSchedules.value[idx] = {
        ...assignedSchedules.value[idx],
        employee_id: empId,
        employee_name: empName,
        username: empUser,
        position: empPos,
        time_from: format12HourTime(scheduleForm.value.time_from),
        time_to: format12HourTime(scheduleForm.value.time_to)
      }
    }
    scheduleSuccess.value = `Working schedule updated successfully for ${empName} (${format12HourTime(scheduleForm.value.time_from)} to ${format12HourTime(scheduleForm.value.time_to)})!`
    cancelEditSchedule()
  } else {
    assignedSchedules.value.unshift({
      id: Date.now(),
      employee_id: empId,
      employee_name: empName,
      username: empUser,
      position: empPos,
      time_from: format12HourTime(scheduleForm.value.time_from),
      time_to: format12HourTime(scheduleForm.value.time_to),
      status: 'Active'
    })
    scheduleSuccess.value = `Working schedule assigned successfully for ${empName} (${format12HourTime(scheduleForm.value.time_from)} to ${format12HourTime(scheduleForm.value.time_to)})!`
    cancelEditSchedule()
  }
}

function removeSchedule(schedId) {
  if (editingScheduleId.value === schedId) {
    cancelEditSchedule()
  }
  assignedSchedules.value = assignedSchedules.value.filter(s => s.id !== schedId)
}


// SALARY FORM & DATA STATE
const editingSalaryId = ref(null)
const salaryForm = ref({
  employee_id: '',
  salary_amount: null
})
const salarySuccess = ref('')
const salaryError = ref('')
const assignedSalaries = ref([
  { id: 1, employee_id: 1, employee_name: 'Juan Dela Cruz', username: 'juan_dc', position: 'IT Admin', salary_amount: 35000.00, status: 'Active' },
  { id: 2, employee_id: 2, employee_name: 'Maria Santos', username: 'maria_s', position: 'Accountant', salary_amount: 28000.00, status: 'Active' }
])

const availableSalaryEmployeeOptions = computed(() => {
  const empList = employeeUsers.value || []
  const userList = users.value || []
  const list = empList.length > 0 ? [...empList] : [...userList]
  
  if (editingSalaryId.value) {
    const currentSal = assignedSalaries.value.find(s => s.id === editingSalaryId.value)
    if (currentSal) {
      const exists = list.some(u => 
        String(u.id) === String(salaryForm.value.employee_id) || 
        String(u.id) === String(currentSal.employee_id) || 
        u.username === currentSal.username
      )
      if (!exists && currentSal.employee_name) {
        list.unshift({
          id: currentSal.employee_id || currentSal.username || currentSal.id,
          full_name: currentSal.employee_name,
          username: currentSal.username,
          position: currentSal.position || 'Employee',
          role: 'employee'
        })
      }
    }
  }
  return list
})

function editSalary(sal) {
  editingSalaryId.value = sal.id
  const pool = availableSalaryEmployeeOptions.value
  const targetEmp = pool.find(u => 
    (sal.employee_id && String(u.id) === String(sal.employee_id)) || 
    (sal.username && u.username?.toLowerCase() === sal.username?.toLowerCase()) ||
    (sal.employee_name && (u.full_name === sal.employee_name || (u.first_name + ' ' + u.last_name) === sal.employee_name))
  )
  
  if (targetEmp) {
    salaryForm.value.employee_id = targetEmp.id
  } else {
    salaryForm.value.employee_id = sal.employee_id || sal.username || ''
  }

  salaryForm.value.salary_amount = sal.salary_amount
  salarySuccess.value = ''
  salaryError.value = ''
}

function cancelEditSalary() {
  editingSalaryId.value = null
  salaryForm.value = {
    employee_id: '',
    salary_amount: null
  }
}

function submitSalary() {
  salarySuccess.value = ''
  salaryError.value = ''
  if (!salaryForm.value.employee_id) {
    salaryError.value = 'Please select an employee.'
    return
  }
  if (salaryForm.value.salary_amount == null || salaryForm.value.salary_amount < 0) {
    salaryError.value = 'Please enter a valid salary amount.'
    return
  }
  
  const pool = availableSalaryEmployeeOptions.value
  const targetEmp = pool.find(u => String(u.id) === String(salaryForm.value.employee_id) || u.username === salaryForm.value.employee_id)
  const empId = targetEmp ? targetEmp.id : salaryForm.value.employee_id
  const empName = targetEmp ? (targetEmp.full_name || (targetEmp.first_name ? targetEmp.first_name + ' ' + targetEmp.last_name : targetEmp.username)) : 'Selected Employee'
  const empUser = targetEmp ? targetEmp.username : 'employee'
  const empPos = targetEmp ? (targetEmp.position || targetEmp.role || 'Employee') : 'Employee'
  const amount = parseFloat(salaryForm.value.salary_amount)

  if (editingSalaryId.value) {
    const idx = assignedSalaries.value.findIndex(s => s.id === editingSalaryId.value)
    if (idx !== -1) {
      assignedSalaries.value[idx] = {
        ...assignedSalaries.value[idx],
        employee_id: empId,
        employee_name: empName,
        username: empUser,
        position: empPos,
        salary_amount: amount
      }
    }
    salarySuccess.value = `Salary updated successfully for ${empName} (₱${amount.toLocaleString('en-US', { minimumFractionDigits: 2 })})!`
    cancelEditSalary()
  } else {
    assignedSalaries.value.unshift({
      id: Date.now(),
      employee_id: empId,
      employee_name: empName,
      username: empUser,
      position: empPos,
      salary_amount: amount,
      status: 'Active'
    })
    salarySuccess.value = `Salary assigned successfully for ${empName} (₱${amount.toLocaleString('en-US', { minimumFractionDigits: 2 })})!`
    cancelEditSalary()
  }
}

function removeSalary(salId) {
  if (editingSalaryId.value === salId) {
    cancelEditSalary()
  }
  assignedSalaries.value = assignedSalaries.value.filter(s => s.id !== salId)
}


// TIMESHEET DATA & ATTENDANCE LOGIC
const userCurrentName = computed(() => {
  if (!user.value) return 'Admin User'
  return user.value.full_name || (user.value.first_name ? `${user.value.first_name} ${user.value.last_name}` : user.value.username) || 'Admin User'
})

const currentUserAttendanceState = ref({
  isClockedIn: false,
  timeIn: '',
  timeOut: '',
  todayDateStr: getManilaDateString()
})


// MANUAL TIME LOGS & ATTENDANCE REQUESTS STATE
const isTimeLogModalOpen = ref(false)
const timelogRequestType = ref('Missing In')

const timelogForm = ref({
  date: getManilaDateString(),
  startDate: getManilaDateString(),
  endDate: getManilaDateString(),
  timeIn: '08:00',
  timeOut: '17:00',
  otIn: '17:00',
  otOut: '20:00',
  leaveType: 'Sick Leave',
  reason: ''
})




// SIMULATED ADMIN ROLE FOR ROLE-BASED TIMELOG ACTIONS
const simulatedAdminRole = ref('auto')

const manualTimeLogs = ref([
  {
    id: 1,
    type: 'Missing In',
    employeeName: 'Juan Dela Cruz',
    employeeRole: 'it',
    department: 'IT',
    dateRange: '2026-09-20',
    details: 'In: 08:00 AM',
    reason: 'Biometric scanner offline during morning punch in',
    status: 'Approved',
    approver: 'HR Manager - Maria Santos',
    approverDate: '2026-09-20 09:15 AM'
  },
  {
    id: 2,
    type: 'Overtime',
    employeeName: 'Juan Dela Cruz',
    employeeRole: 'it',
    department: 'IT',
    dateRange: '2026-09-22',
    details: 'OT In: 05:00 PM | OT Out: 08:00 PM (3 hrs)',
    reason: 'Critical database server migration and patch deployment',
    status: 'Approved',
    approver: 'Tech Lead - Pedro Penduko',
    approverDate: '2026-09-22 08:30 PM'
  },
  {
    id: 3,
    type: 'Missing Out',
    employeeName: 'Pedro Penduko',
    employeeRole: 'hr',
    department: 'HR',
    dateRange: '2026-09-23',
    details: 'Out: 05:15 PM',
    reason: 'Building wide power interruption during dismissal',
    status: 'Pending',
    approver: '--',
    approverDate: '--'
  },
  {
    id: 4,
    type: 'Leave',
    employeeName: 'Maria Santos',
    employeeRole: 'accounting',
    department: 'Accounting',
    dateRange: '2026-09-28 to 2026-09-29',
    details: 'Sick Leave (2 Days)',
    reason: 'Scheduled medical procedure and recovery rest',
    status: 'Pending',
    approver: '--',
    approverDate: '--'
  }
])

function getUserDepartment(userObj) {
  if (!userObj) return ''
  const dept = (userObj.department || '').toLowerCase().trim()
  if (dept) {
    if (dept.includes('acc') || dept.includes('finance')) return 'accounting'
    if (dept.includes('hr') || dept.includes('human')) return 'hr'
    if (dept.includes('it') || dept.includes('tech')) return 'it'
    if (dept.includes('ops') || dept.includes('operation')) return 'operations'
    return dept
  }
  const roleStr = (userObj.role || userObj.account_role || userObj.position || '').toLowerCase().trim()
  if (roleStr.includes('acc') || roleStr.includes('finance')) return 'accounting'
  if (roleStr.includes('hr') || roleStr.includes('human')) return 'hr'
  if (roleStr.includes('it') || roleStr.includes('tech')) return 'it'
  if (roleStr.includes('ops') || roleStr.includes('operation')) return 'operations'
  return roleStr
}

function getLogDepartment(log) {
  if (!log) return ''
  if (log.department) {
    const d = log.department.toLowerCase().trim()
    if (d.includes('acc') || d.includes('finance')) return 'accounting'
    if (d.includes('hr') || d.includes('human')) return 'hr'
    if (d.includes('it') || d.includes('tech')) return 'it'
    if (d.includes('ops') || d.includes('operation')) return 'operations'
    return d
  }
  const empId = log.employeeId || log.user_id || log.employee_id
  const empName = log.employeeName || log.employee_name || log.username
  if (empId || empName) {
    const emp = (employeeUsers.value || []).find(u => String(u.id) === String(empId) || u.username === empName || u.full_name === empName) ||
                (users.value || []).find(u => String(u.id) === String(empId) || u.username === empName || u.full_name === empName)
    if (emp) {
      return getUserDepartment(emp)
    }
  }
  const roleStr = (log.employeeRole || log.position || log.role || '').toLowerCase()
  if (roleStr.includes('acc') || roleStr.includes('finance')) return 'accounting'
  if (roleStr.includes('hr') || roleStr.includes('human')) return 'hr'
  if (roleStr.includes('it') || roleStr.includes('tech')) return 'it'
  if (roleStr.includes('ops') || roleStr.includes('operation')) return 'operations'
  return roleStr
}

function getEmployeeRoleGroup(log) {
  return getLogDepartment(log)
}

function canUserActionRequest(log) {
  const activeUser = user.value
  if (!activeUser) return false

  const rawRole = (activeUser.role || activeUser.account_role || activeUser.position || '').toLowerCase().replace(/\s+/g, '_')
  
  // 1. Super Admin can approve ALL departments
  if (rawRole === 'super_admin' || rawRole === 'superadmin') {
    return true
  }

  // 2. Check if the user's role has approver permission enabled in Set Access
  const hasApprover = canAccessMenu('attendance_approver') || canAccessMenu('payroll_approver')
  if (!hasApprover) {
    return false
  }

  // 3. Department matching check: Approver can ONLY approve requests from their SAME department
  const approverDept = getUserDepartment(activeUser)
  const logDept = getLogDepartment(log)

  if (!approverDept || !logDept) {
    return true // Default allow if department is unspecified
  }

  return approverDept === logDept
}

function getRequiredAdminLabel(log) {
  const dept = getLogDepartment(log)
  if (dept.includes('it')) return 'IT Dept'
  if (dept.includes('hr')) return 'HR Dept'
  if (dept.includes('accounting')) return 'Accounting Dept'
  if (dept.includes('ops') || dept.includes('operation')) return 'Ops Dept'
  return 'Same Dept'
}

function openTimeLogModal() {
  leaveAdjustmentMessage.value = ''
  timelogRequestType.value = 'Missing In'
  const todayStr = getManilaDateString()
  timelogForm.value = {
    date: todayStr,
    startDate: todayStr,
    endDate: todayStr,
    timeIn: '08:00',
    timeOut: '17:00',
    otIn: '17:00',
    otOut: '20:00',
    leaveType: 'Sick Leave',
    reason: ''
  }
  isTimeLogModalOpen.value = true
}

function closeTimeLogModal() {
  isTimeLogModalOpen.value = false
}

function formatTimeString(time24) {
  if (!time24) return ''
  const parts = time24.split(':')
  let h = parseInt(parts[0], 10)
  const m = parts[1] || '00'
  const ampm = h >= 12 ? 'PM' : 'AM'
  h = h % 12 || 12
  return `${String(h).padStart(2, '0')}:${m} ${ampm}`
}

function submitTimeLogRequest() {
  if (!timelogForm.value.reason.trim()) {
    alert('Please enter a reason for your manual log request.')
    return
  }

  if (timelogRequestType.value === 'Leave') {
    if (currentUserAvailableLeaveCredits.value <= 0) {
      alert('You have 0 leave credits remaining. Cannot file a leave request.')
      return
    }
    validateAndAdjustLeaveDates()
  }

  let dateRange = timelogForm.value.date
  let details = ''

  if (timelogRequestType.value === 'Missing In') {
    dateRange = timelogForm.value.date
    details = `In: ${formatTimeString(timelogForm.value.timeIn)}`
  } else if (timelogRequestType.value === 'Missing Out') {
    dateRange = timelogForm.value.date
    details = `Out: ${formatTimeString(timelogForm.value.timeOut)}`
  } else if (timelogRequestType.value === 'Missing In and Out') {
    dateRange = timelogForm.value.date
    details = `In: ${formatTimeString(timelogForm.value.timeIn)} | Out: ${formatTimeString(timelogForm.value.timeOut)}`
  } else if (timelogRequestType.value === 'Overtime') {
    dateRange = timelogForm.value.date
    let otH = 0
    const inM = parseTimeToMinutes(formatTimeString(timelogForm.value.otIn))
    const outM = parseTimeToMinutes(formatTimeString(timelogForm.value.otOut))
    if (inM != null && outM != null) {
      let diff = outM - inM
      if (diff < 0) diff += 1440
      if (diff > 0) otH = parseFloat((diff / 60).toFixed(2))
    }
    details = `OT In: ${formatTimeString(timelogForm.value.otIn)} | OT Out: ${formatTimeString(timelogForm.value.otOut)} (${otH > 0 ? otH : 3.0} hrs @ 1.25x)`
  } else if (timelogRequestType.value === 'Change Schedule') {
    dateRange = `${timelogForm.value.startDate} to ${timelogForm.value.endDate}`
    details = `New Shift: ${formatTimeString(timelogForm.value.timeIn)} - ${formatTimeString(timelogForm.value.timeOut)}`
  } else if (timelogRequestType.value === 'Leave') {
    const daysCount = selectedLeaveDaysCount.value
    dateRange = timelogForm.value.startDate === timelogForm.value.endDate 
      ? timelogForm.value.startDate 
      : `${timelogForm.value.startDate} to ${timelogForm.value.endDate}`
    details = `${timelogForm.value.leaveType} (${daysCount} Day${daysCount !== 1 ? 's' : ''})`
  }

  manualTimeLogs.value.unshift({
    id: Date.now(),
    type: timelogRequestType.value,
    employeeName: userCurrentName.value || 'Current User',
    employeeId: selectedTimesheetEmployeeId.value === 'current_user' ? (user.value?.id || '1') : selectedTimesheetEmployeeId.value,
    username: user.value?.username || 'user',
    dateRange,
    details,
    timeIn: formatTimeString(timelogForm.value.timeIn),
    timeOut: formatTimeString(timelogForm.value.timeOut),
    reason: timelogForm.value.reason.trim(),
    status: 'Pending',
    approver: '--',
    approverDate: '--'
  })

  closeTimeLogModal()
}

function parseTimeToMinutes(timeStr) {
  if (!timeStr) return null
  const clean = String(timeStr).trim().toUpperCase()
  const match = clean.match(/(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?/)
  if (!match) return null
  let h = parseInt(match[1], 10)
  const m = parseInt(match[2] || '0', 10)
  const ampm = match[3]

  if (ampm) {
    if (ampm === 'PM' && h < 12) h += 12
    if (ampm === 'AM' && h === 12) h = 0
  }
  return h * 60 + m
}

function formatMinutesTo12Hr(totalMinutes) {
  if (totalMinutes == null || isNaN(totalMinutes)) return '--:--'
  let h = Math.floor(totalMinutes / 60) % 24
  const m = totalMinutes % 60
  const ampm = h >= 12 ? 'PM' : 'AM'
  h = h % 12 || 12
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')} ${ampm}`
}

function computeAttendanceMetrics(timeInStr, timeOutStr) {
  const inMins = parseTimeToMinutes(timeInStr) ?? 480
  const outMins = parseTimeToMinutes(timeOutStr) ?? 1020

  const stdInMins = 480 // 08:00 AM
  const stdOutMins = 1020 // 05:00 PM

  const isLate = inMins > stdInMins
  const isEarlyOut = outMins < stdOutMins

  let status = 'Present'
  if (isLate && isEarlyOut) {
    status = 'Late / Early Out'
  } else if (isLate) {
    status = 'Late'
  } else if (isEarlyOut) {
    status = 'Early Out'
  }

  let elapsedMinutes = outMins - inMins
  if (elapsedMinutes < 0) elapsedMinutes += 24 * 60
  let deliveredHours = Math.round((elapsedMinutes / 60.0) * 100) / 100
  if (deliveredHours >= 4.0) {
    deliveredHours = Math.max(0, Math.round((deliveredHours - 1.0) * 100) / 100)
  }

  const formattedIn = formatMinutesTo12Hr(inMins)
  const formattedOut = formatMinutesTo12Hr(outMins)

  return {
    status,
    isLate,
    isEarlyOut,
    timeIn: formattedIn,
    timeOut: formattedOut,
    deliveredHours
  }
}

function parseSingleDateStrToISO(str) {
  if (!str) return null
  const clean = String(str).trim()

  const isoMatch = clean.match(/(\d{4})-(\d{1,2})-(\d{1,2})/)
  if (isoMatch) {
    const y = isoMatch[1]
    const m = String(isoMatch[2]).padStart(2, '0')
    const d = String(isoMatch[3]).padStart(2, '0')
    return `${y}-${m}-${d}`
  }

  const slashMatch = clean.match(/(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?/)
  if (slashMatch) {
    const m = String(slashMatch[1]).padStart(2, '0')
    const d = String(slashMatch[2]).padStart(2, '0')
    let y = slashMatch[3]
    if (!y) {
      y = getManilaDateString().slice(0, 4)
    } else if (y.length === 2) {
      y = `20${y}`
    }
    return `${y}-${m}-${d}`
  }

  const dObj = new Date(clean)
  if (!isNaN(dObj.getTime())) {
    const y = dObj.getFullYear()
    const m = String(dObj.getMonth() + 1).padStart(2, '0')
    const d = String(dObj.getDate()).padStart(2, '0')
    return `${y}-${m}-${d}`
  }

  return null
}

function parseAllDatesFromItem(item) {
  if (!item) return [getManilaDateString()]
  const raw = String(item.dateRange || item.date || item.reason || '').trim()
  if (!raw) return [getManilaDateString()]

  const foundDates = []

  const slashMatches = raw.match(/\b\d{1,2}\/\d{1,2}(?:\/\d{2,4})?\b/g)
  if (slashMatches) {
    slashMatches.forEach(sm => {
      const iso = parseSingleDateStrToISO(sm)
      if (iso && !foundDates.includes(iso)) foundDates.push(iso)
    })
  }

  const isoMatches = raw.match(/\b\d{4}-\d{2}-\d{2}\b/g)
  if (isoMatches) {
    isoMatches.forEach(im => {
      if (!foundDates.includes(im)) foundDates.push(im)
    })
  }

  if (foundDates.length > 0) {
    return foundDates
  }

  try {
    const parts = raw.split(/to|--/)
    parts.forEach(p => {
      const iso = parseSingleDateStrToISO(p.trim())
      if (iso && !foundDates.includes(iso)) foundDates.push(iso)
    })
    if (foundDates.length > 0) return foundDates
  } catch (e) {}

  return [getManilaDateString()]
}

function extractTimesFromLogItem(item, targetDate = '') {
  let timeInRaw = item.timeIn || ''
  let timeOutRaw = item.timeOut || ''
  const details = String(item.details || '')
  const reason = String(item.reason || '')
  const combined = `${details} ${reason}`

  let targetShort = ''
  if (targetDate) {
    const parts = targetDate.split('-')
    if (parts.length === 3) {
      targetShort = `${parseInt(parts[1], 10)}/${parseInt(parts[2], 10)}`
    }
  }

  if (targetShort && combined.includes(targetShort)) {
    const snippet = combined.slice(combined.indexOf(targetShort))
    const snippetIn = snippet.match(/(?:in|start)?\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)/i)
    if (snippetIn && snippetIn[1] && !snippetIn[1].includes('/')) {
      timeInRaw = snippetIn[1]
    }
  }

  if (!timeInRaw && details) {
    const inMatch = details.match(/In:\s*([0-9:]+\s*(?:AM|PM)?)/i)
    if (inMatch) timeInRaw = inMatch[1]
  }
  if (!timeOutRaw && details) {
    const outMatch = details.match(/Out:\s*([0-9:]+\s*(?:AM|PM)?)/i)
    if (outMatch) timeOutRaw = outMatch[1]
  }

  if (!timeInRaw) {
    const inMatch = combined.match(/\b(?:in\s*(?:at)?\s*)?(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b/i)
    if (inMatch) timeInRaw = inMatch[1]
  }
  if (!timeOutRaw) {
    const outMatch = combined.match(/\b(?:out\s*(?:at)?\s*)?(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b/i)
    if (outMatch) timeOutRaw = outMatch[1]
  }

  return {
    timeIn: timeInRaw || '08:00 AM',
    timeOut: timeOutRaw || '05:00 PM'
  }
}

function getTimesheetLogForDate(dateStr, targetEmpId = null, targetEmpName = null) {
  const keysToTry = []
  if (targetEmpId && targetEmpId !== 'current_user') {
    keysToTry.push(`${targetEmpId}_${dateStr}`)
  }
  if (targetEmpName) {
    keysToTry.push(`${targetEmpName}_${dateStr}`)
  }
  if (user.value?.username) {
    keysToTry.push(`${user.value.username}_${dateStr}`)
  }
  if (user.value?.id) {
    keysToTry.push(`${user.value.id}_${dateStr}`)
  }
  keysToTry.push(dateStr)

  for (const k of keysToTry) {
    if (timesheetLogs.value[k]) return timesheetLogs.value[k]
  }

  // Fallback match from approved manualTimeLogs
  const approvedMatch = (manualTimeLogs.value || []).find(l => {
    if (l.status !== 'Approved') return false
    const parsedDates = parseAllDatesFromItem(l)
    if (parsedDates.includes(dateStr)) return true
    const d = String(l.date || l.dateRange || '')
    const isDateMatch = d.includes(dateStr) || dateStr.includes(d)
    if (!isDateMatch) return false

    if (targetEmpName) {
      const logName = (l.employeeName || l.employee_name || '').toLowerCase()
      const tName = targetEmpName.toLowerCase()
      if (logName && tName && !logName.includes(tName) && !tName.includes(logName)) {
        return false
      }
    }
    return true
  })

  if (approvedMatch) {
    if (approvedMatch.type === 'Leave') {
      return {
        status: 'Leave',
        statusText: '🏖️ Leave',
        timeIn: '--:--',
        timeOut: '--:--',
        deliveredHours: 8.0,
        address: 'Approved Leave'
      }
    }
    const extracted = extractTimesFromLogItem(approvedMatch, dateStr)
    const metrics = computeAttendanceMetrics(extracted.timeIn, extracted.timeOut)
    return {
      status: metrics.status,
      statusText: `🟢 ${metrics.status}`,
      timeIn: metrics.timeIn,
      timeOut: metrics.timeOut,
      deliveredHours: metrics.deliveredHours,
      address: 'HQ - Metro Manila, PH'
    }
  }

  return null
}

function syncApprovedTimeLogToTimesheet(item) {
  if (!item) return

  const targetDates = parseAllDatesFromItem(item)
  const empName = item.employeeName || item.employee_name || userCurrentName.value
  const empId = String(item.employeeId || item.user_id || '1')
  const empKey = item.username || empId

  targetDates.forEach(targetDate => {
    const existingLog = timesheetLogs.value[`${empKey}_${targetDate}`] || 
                        timesheetLogs.value[`${empId}_${targetDate}`] || 
                        timesheetLogs.value[`${empName}_${targetDate}`] || 
                        timesheetLogs.value[targetDate] || {}

    let newLog = { ...existingLog }

    if (item.type === 'Leave') {
      newLog = {
        ...newLog,
        employeeName: empName,
        status: 'Leave',
        statusText: '🏖️ Leave',
        timeIn: '--:--',
        timeOut: '--:--',
        deliveredHours: 8.0,
        address: 'Approved Leave'
      }
    } else if (item.type === 'Change Schedule') {
      let timeFrom = '08:00 AM'
      let timeTo = '05:00 PM'
      if (item.details) {
        const times = item.details.match(/([0-9]{1,2}:[0-9]{2}\s*(?:AM|PM)?)/gi)
        if (times && times.length >= 2) {
          timeFrom = times[0]
          timeTo = times[1]
        }
      }
      const metrics = computeAttendanceMetrics(timeFrom, timeTo)
      newLog = {
        ...newLog,
        employeeName: empName,
        status: metrics.status,
        statusText: `🟢 ${metrics.status} (Approved Shift)`,
        scheduleDetails: `Shift: ${metrics.timeIn} - ${metrics.timeOut}`,
        timeIn: metrics.timeIn,
        timeOut: metrics.timeOut,
        deliveredHours: metrics.deliveredHours,
        address: existingLog.address && existingLog.address !== '--' ? existingLog.address : 'HQ - Metro Manila, PH (Approved Schedule)'
      }
    } else {
      const extracted = extractTimesFromLogItem(item, targetDate)
      
      let curIn = extracted.timeIn
      let curOut = extracted.timeOut

      if (item.type === 'Missing In') {
        curIn = extracted.timeIn
        if (existingLog.timeOut && existingLog.timeOut !== '--:--' && extracted.timeOut === '05:00 PM') {
          curOut = existingLog.timeOut
        }
      } else if (item.type === 'Missing Out') {
        curOut = extracted.timeOut
        if (existingLog.timeIn && existingLog.timeIn !== '--:--' && extracted.timeIn === '08:00 AM') {
          curIn = existingLog.timeIn
        }
      }

      const metrics = computeAttendanceMetrics(curIn, curOut)

      let statusText = `🟢 ${metrics.status}`
      if (metrics.status === 'Late') statusText = '⚠️ Late'
      if (metrics.status === 'Early Out') statusText = '⏳ Early Out'
      if (metrics.status === 'Late / Early Out') statusText = '⚠️ Late / Early Out'

      newLog = {
        ...existingLog,
        employeeName: empName,
        status: metrics.status,
        statusText,
        timeIn: metrics.timeIn,
        timeOut: metrics.timeOut,
        deliveredHours: metrics.deliveredHours,
        address: existingLog.address && existingLog.address !== '--' ? existingLog.address : 'HQ - Metro Manila, PH'
      }
    }

    timesheetLogs.value[`${empKey}_${targetDate}`] = newLog
    timesheetLogs.value[`${empId}_${targetDate}`] = newLog
    timesheetLogs.value[`${empName}_${targetDate}`] = newLog
    timesheetLogs.value[targetDate] = newLog
  })

  saveAttendanceToStorage()
}

function approveTimeLogRequest(id) {
  const item = manualTimeLogs.value.find(l => l.id === id)
  if (item) {
    item.status = 'Approved'
    item.approver = (userCurrentName.value || 'Admin')
    item.approverDate = getManilaDateTimeString()

    syncApprovedTimeLogToTimesheet(item)
  }
}

function rejectTimeLogRequest(id) {
  const item = manualTimeLogs.value.find(l => l.id === id)
  if (item) {
    item.status = 'Rejected'
    item.approver = (userCurrentName.value || 'Admin')
    item.approverDate = getManilaDateTimeString()
  }
}

function clearTimesheetRowData(row) {
  if (!row || !row.date) return
  const dateStr = row.date
  const empName = row.employeeName || userCurrentName.value || 'Employee'

  if (!confirm(`Are you sure you want to clear attendance time log data for ${empName} on ${row.formattedDate || dateStr}?`)) {
    return
  }

  const empId = selectedTimesheetEmployeeId.value !== 'current_user' ? selectedTimesheetEmployeeId.value : (user.value?.id || '1')
  const username = user.value?.username || 'user'

  const keysToDelete = [
    dateStr,
    `${empId}_${dateStr}`,
    `${username}_${dateStr}`,
    `${empName}_${dateStr}`,
    `current_user_${dateStr}`
  ]

  Object.keys(timesheetLogs.value).forEach(k => {
    if (k === dateStr || k.endsWith(`_${dateStr}`)) {
      keysToDelete.push(k)
    }
  })

  keysToDelete.forEach(k => {
    delete timesheetLogs.value[k]
  })

  if (manualTimeLogs.value && manualTimeLogs.value.length > 0) {
    manualTimeLogs.value.forEach(item => {
      const dates = parseAllDatesFromItem(item)
      if (dates.includes(dateStr)) {
        item.status = 'Cleared'
      }
    })
  }

  saveAttendanceToStorage()
}

// Store user log entries per date

// TABLE DRAG-TO-SCROLL STATE & LOGIC
const timesheetScrollContainer = ref(null)
const isDraggingTable = ref(false)
let dragStartX = 0
let dragStartY = 0
let dragScrollLeft = 0
let dragScrollTop = 0

function onTableMouseDown(e) {
  if (e.button !== 0) return
  if (['BUTTON', 'INPUT', 'SELECT', 'A', 'OPTION'].includes(e.target.tagName)) return
  
  isDraggingTable.value = true
  const el = timesheetScrollContainer.value || e.currentTarget
  dragStartX = e.pageX - el.offsetLeft
  dragStartY = e.pageY - el.offsetTop
  dragScrollLeft = el.scrollLeft
  dragScrollTop = el.scrollTop
}

function onTableMouseLeave() {
  isDraggingTable.value = false
}

function onTableMouseUp() {
  isDraggingTable.value = false
}

function onTableMouseMove(e) {
  if (!isDraggingTable.value) return
  e.preventDefault()
  const el = timesheetScrollContainer.value || e.currentTarget
  const x = e.pageX - el.offsetLeft
  const y = e.pageY - el.offsetTop
  const walkX = (x - dragStartX) * 1.5
  const walkY = (y - dragStartY) * 1.5
  el.scrollLeft = dragScrollLeft - walkX
  el.scrollTop = dragScrollTop - walkY
}

// Store user log entries per date (Starts EMPTY for clean manual testing)
const timesheetLogs = ref({})

function saveAttendanceToStorage() {
  try {
    const key = `timesheet_logs_${selectedTimesheetEmployeeId.value}_${user.value?.username || 'user'}`
    localStorage.setItem(key, JSON.stringify(timesheetLogs.value))
  } catch (e) {}
}

function loadAttendanceFromStorage() {
  try {
    const key = `timesheet_logs_${selectedTimesheetEmployeeId.value}_${user.value?.username || 'user'}`
    const saved = localStorage.getItem(key)
    if (saved) {
      timesheetLogs.value = JSON.parse(saved)
    } else {
      timesheetLogs.value = {}
    }
  } catch (e) {
    timesheetLogs.value = {}
  }
  autoClockInOnLogin()
}


function generateFallbackAvatar(mode) {
  const initials = (userCurrentName.value || 'USER').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
  const color = mode === 'Time In' ? '#10b981' : '#f43f5e'
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
    <rect width="300" height="300" fill="#0f172a"/>
    <circle cx="150" cy="120" r="60" fill="${color}" opacity="0.2" stroke="${color}" stroke-width="4"/>
    <text x="150" y="132" font-size="42" font-weight="bold" fill="#ffffff" text-anchor="middle" font-family="sans-serif">${initials}</text>
    <rect x="30" y="210" width="240" height="50" rx="10" fill="rgba(255,255,255,0.08)"/>
    <text x="150" y="240" font-size="16" font-weight="bold" fill="#38bdf8" text-anchor="middle" font-family="sans-serif">📸 ${mode} Verified</text>
  </svg>`
  return 'data:image/svg+xml;base64,' + btoa(svg)
}

const showCameraCaptureModal = ref(false)
const cameraStream = ref(null)
const cameraVideoRef = ref(null)
const cameraCaptureMode = ref('Time In')
const cameraCapturePromise = ref(null)
const cameraCapturedPhoto = ref(null)
const cameraCaptureError = ref('')
const isCameraStarting = ref(false)

function isPhotoVerificationRequired() {
  return canAccessMenu('attendance_photo_verification')
}

async function startCameraStream() {
  isCameraStarting.value = true
  cameraCaptureError.value = ''
  try {
    if (typeof navigator !== 'undefined' && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 640 } }
      })
      cameraStream.value = stream
      await new Promise(r => setTimeout(r, 100))
      if (cameraVideoRef.value) {
        cameraVideoRef.value.srcObject = stream
        await cameraVideoRef.value.play()
      }
    } else {
      cameraCaptureError.value = 'Camera device not supported on this browser.'
    }
  } catch (err) {
    console.error('Camera stream access error:', err)
    cameraCaptureError.value = 'Unable to access camera device. Please allow camera permissions.'
  } finally {
    isCameraStarting.value = false
  }
}

function stopCameraStream() {
  if (cameraStream.value) {
    cameraStream.value.getTracks().forEach(track => track.stop())
    cameraStream.value = null
  }
}

function snapCameraSnapshot() {
  if (!cameraVideoRef.value) return
  const video = cameraVideoRef.value
  const canvas = document.createElement('canvas')
  canvas.width = 400
  canvas.height = 400
  const ctx = canvas.getContext('2d')

  const minDim = Math.min(video.videoWidth || 400, video.videoHeight || 400)
  const startX = ((video.videoWidth || 400) - minDim) / 2
  const startY = ((video.videoHeight || 400) - minDim) / 2

  ctx.drawImage(video, startX, startY, minDim, minDim, 0, 0, 400, 400)
  cameraCapturedPhoto.value = canvas.toDataURL('image/jpeg', 0.85)
}

function retakeCameraSnapshot() {
  cameraCapturedPhoto.value = null
}

function confirmCameraPhotoCapture() {
  const photo = cameraCapturedPhoto.value || generateFallbackAvatar(cameraCaptureMode.value)
  stopCameraStream()
  showCameraCaptureModal.value = false
  if (cameraCapturePromise.value) {
    cameraCapturePromise.value(photo)
    cameraCapturePromise.value = null
  }
}

function cancelCameraPhotoCapture() {
  stopCameraStream()
  showCameraCaptureModal.value = false
  if (cameraCapturePromise.value) {
    cameraCapturePromise.value(null)
    cameraCapturePromise.value = null
  }
}

async function captureAttendancePhoto(mode = 'Time In') {
  // If photo verification is disabled in Set Access for user's role, skip camera modal & return null!
  if (!isPhotoVerificationRequired()) {
    return null
  }

  cameraCaptureMode.value = mode
  cameraCapturedPhoto.value = null
  cameraCaptureError.value = ''
  showCameraCaptureModal.value = true

  await startCameraStream()

  return new Promise((resolve) => {
    cameraCapturePromise.value = resolve
  })
}

function purgeExpiredAttendancePhotos() {
  const now = Date.now()
  const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000
  let purgedAny = false

  Object.keys(timesheetLogs.value).forEach(dateStr => {
    const logDate = new Date(dateStr).getTime()
    if (!isNaN(logDate) && (now - logDate) > THIRTY_DAYS_MS) {
      const log = timesheetLogs.value[dateStr]
      if (log && (log.timeInPhoto || log.timeOutPhoto)) {
        log.timeInPhoto = null
        log.timeOutPhoto = null
        log.photoPurged = true
        purgedAny = true
      }
    }
  })

  if (purgedAny) {
    saveAttendanceToStorage()
  }
}

const showPhotoModal = ref(false)
const activePhotoMeta = ref({
  title: 'Time In',
  employeeName: '',
  date: '',
  time: '',
  address: '',
  photoUrl: ''
})

function openPhotoPreviewModal(photoUrl, title, row) {
  if (!photoUrl) return
  activePhotoMeta.value = {
    title,
    employeeName: row.employeeName,
    date: row.formattedDate,
    time: title === 'Time In' ? row.timeIn : row.timeOut,
    address: title === 'Time In' ? row.timeInAddress : row.timeOutAddress,
    photoUrl
  }
  showPhotoModal.value = true
}

async function getDeviceGPSAddress() {
  const fallback = user.value?.location || user.value?.address || 'HQ - Metro Manila, PH'
  if (typeof navigator === 'undefined' || !navigator.geolocation) {
    return fallback
  }
  return new Promise((resolve) => {
    let resolved = false
    const finish = (addr) => {
      if (!resolved) {
        resolved = true
        resolve(addr)
      }
    }
    const timer = setTimeout(() => finish(fallback), 1500)

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        try {
          const controller = new AbortController()
          const fetchTimer = setTimeout(() => controller.abort(), 1200)
          const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`, { signal: controller.signal })
          clearTimeout(fetchTimer)
          if (res.ok) {
            const data = await res.json()
            if (data && data.display_name) {
              const parts = data.display_name.split(',').map(s => s.trim()).filter(Boolean)
              const shortAddr = parts.slice(0, 3).join(', ')
              clearTimeout(timer)
              finish(shortAddr)
              return
            }
          }
        } catch (e) {}
        clearTimeout(timer)
        finish(`${lat.toFixed(4)}°, ${lng.toFixed(4)}° - Manila, PH`)
      },
      () => {
        clearTimeout(timer)
        finish(fallback)
      },
      { timeout: 1500, enableHighAccuracy: false }
    )
  })
}

async function autoClockInOnLogin() {
  const todayStr = getManilaDateString()
  currentUserAttendanceState.value.todayDateStr = todayStr
  const existingLog = timesheetLogs.value[todayStr]

  // If there is ALREADY data (timeIn is recorded), SKIP IT, don't insert or update!
  if (existingLog && existingLog.timeIn && existingLog.timeIn !== '--:--') {
    purgeExpiredAttendancePhotos()
    syncCurrentUserClockState()
    return
  }

  // If photo verification is enabled for user role, launch live camera modal!
  const photo = await captureAttendancePhoto('Time In')
  if (isPhotoVerificationRequired() && photo === null) {
    return
  }

  const timeStr = getManilaTimeString()
  const now = new Date()
  const isLate = now.getHours() > 8 || (now.getHours() === 8 && now.getMinutes() > 30)
  const status = isLate ? 'Late' : 'Present'
  const gpsAddress = await getDeviceGPSAddress()

  timesheetLogs.value[todayStr] = {
    status,
    timeIn: timeStr,
    timeInAddress: gpsAddress,
    timeInPhoto: photo,
    timeOut: '--:--',
    timeOutAddress: '--',
    timeOutPhoto: null,
    deliveredHours: 0.0
  }
  saveAttendanceToStorage()
  syncCurrentUserClockState()
}

async function autoClockOutOnLogout() {
  const todayStr = getManilaDateString()
  const existingLog = timesheetLogs.value[todayStr]

  // If there is ALREADY data (timeOut is recorded), SKIP IT, don't insert or update!
  if (existingLog && existingLog.timeOut && existingLog.timeOut !== '--:--') {
    return
  }

  if (existingLog && existingLog.timeIn && existingLog.timeIn !== '--:--') {
    const photo = await captureAttendancePhoto('Log Out')
    if (isPhotoVerificationRequired() && photo === null) {
      return
    }

    const timeOutStr = getManilaTimeString()
    const gpsAddress = await getDeviceGPSAddress()
    const now = new Date()
    const isEarly = now.getHours() < 17
    const status = isEarly ? 'Early Out' : existingLog.status

    timesheetLogs.value[todayStr] = {
      ...existingLog,
      status,
      timeOut: timeOutStr,
      timeOutAddress: gpsAddress,
      timeOutPhoto: photo,
      deliveredHours: 8.0
    }
    saveAttendanceToStorage()
  }
}

function syncCurrentUserClockState() {
  const todayStr = currentUserAttendanceState.value.todayDateStr
  const todayLog = timesheetLogs.value[todayStr]
  if (todayLog && todayLog.timeIn && todayLog.timeIn !== '--:--') {
    currentUserAttendanceState.value.timeIn = todayLog.timeIn
    if (todayLog.timeOut && todayLog.timeOut !== '--:--') {
      currentUserAttendanceState.value.isClockedIn = false
      currentUserAttendanceState.value.timeOut = todayLog.timeOut
    } else {
      currentUserAttendanceState.value.isClockedIn = true
      currentUserAttendanceState.value.timeOut = ''
    }
  } else {
    currentUserAttendanceState.value.isClockedIn = false
    currentUserAttendanceState.value.timeIn = ''
    currentUserAttendanceState.value.timeOut = ''
  }
}

function clearAllAttendanceLogs() {
  timesheetLogs.value = {}
  saveAttendanceToStorage()
  syncCurrentUserClockState()
}

function seedSampleTimesheetLogs() {
  timesheetLogs.value = {
    '2026-09-01': { status: 'Present', timeIn: '08:00 AM', timeInAddress: 'HQ - Metro Manila, PH', timeOut: '05:00 PM', timeOutAddress: 'HQ - Metro Manila, PH', deliveredHours: 8.0 },
    '2026-09-02': { status: 'Present', timeIn: '08:00 AM', timeInAddress: 'HQ - Metro Manila, PH', timeOut: '05:00 PM', timeOutAddress: 'HQ - Metro Manila, PH', deliveredHours: 8.0 },
    '2026-09-03': { status: 'Late', timeIn: '08:45 AM', timeInAddress: 'Branch 2 - QC, PH', timeOut: '05:00 PM', timeOutAddress: 'Branch 2 - QC, PH', deliveredHours: 7.25 },
    '2026-09-04': { status: 'Early Out', timeIn: '08:00 AM', timeInAddress: 'HQ - Metro Manila, PH', timeOut: '04:00 PM', timeOutAddress: 'HQ - Metro Manila, PH', deliveredHours: 7.0 },
    '2026-09-07': { status: 'Present', timeIn: '08:00 AM', timeInAddress: 'HQ - Metro Manila, PH', timeOut: '05:00 PM', timeOutAddress: 'HQ - Metro Manila, PH', deliveredHours: 8.0 }
  }
  saveAttendanceToStorage()
  syncCurrentUserClockState()
}

async function clockInCurrentUser() {
  await autoClockInOnLogin()
}

async function clockOutCurrentUser() {
  const todayStr = getManilaDateString()
  currentUserAttendanceState.value.todayDateStr = todayStr
  const existingLog = timesheetLogs.value[todayStr] || { status: 'Present', timeIn: '08:00 AM', timeInAddress: 'HQ - Metro Manila, PH' }

  if (existingLog.timeOut && existingLog.timeOut !== '--:--') {
    currentUserAttendanceState.value.isClockedIn = false
    currentUserAttendanceState.value.timeOut = existingLog.timeOut
    return
  }

  const photo = await captureAttendancePhoto('Log Out')
  if (isPhotoVerificationRequired() && photo === null) {
    return
  }

  const timeOutStr = getManilaTimeString()
  const gpsAddress = await getDeviceGPSAddress()
  const now = new Date()
  const isEarly = now.getHours() < 17
  const status = isEarly ? 'Early Out' : existingLog.status

  timesheetLogs.value[todayStr] = {
    ...existingLog,
    status,
    timeOut: timeOutStr,
    timeOutAddress: gpsAddress,
    timeOutPhoto: photo,
    deliveredHours: 8.0
  }
  saveAttendanceToStorage()
  syncCurrentUserClockState()
}

function updateRowStatus(dateStr, newStatus) {
  if (!timesheetLogs.value[dateStr]) {
    timesheetLogs.value[dateStr] = { status: newStatus, timeIn: '--:--', timeOut: '--:--', deliveredHours: 0.0 }
  }
  timesheetLogs.value[dateStr].status = newStatus
  if (newStatus === 'Present') {
    timesheetLogs.value[dateStr].timeIn = '08:00 AM'
    timesheetLogs.value[dateStr].timeOut = '05:00 PM'
    timesheetLogs.value[dateStr].deliveredHours = 8.0
  } else if (newStatus === 'Late') {
    timesheetLogs.value[dateStr].timeIn = '08:45 AM'
    timesheetLogs.value[dateStr].timeOut = '05:00 PM'
    timesheetLogs.value[dateStr].deliveredHours = 7.25
  } else if (newStatus === 'Early Out') {
    timesheetLogs.value[dateStr].timeIn = '08:00 AM'
    timesheetLogs.value[dateStr].timeOut = '04:00 PM'
    timesheetLogs.value[dateStr].deliveredHours = 7.0
  } else if (newStatus === 'Absent') {
    timesheetLogs.value[dateStr].timeIn = '--:--'
    timesheetLogs.value[dateStr].timeOut = '--:--'
    timesheetLogs.value[dateStr].deliveredHours = 0.0
  }
  saveAttendanceToStorage()
}

// Default selected month YYYY-MM dynamically based on Manila timezone date
const selectedTimesheetMonth = ref(getManilaDateString().slice(0, 7))
const selectedTimesheetEmployeeId = ref('current_user')

const timesheetMonthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const timesheetMonthOptions = computed(() => {
  const currentMonthVal = getManilaDateString().slice(0, 7)
  const [curYearStr] = currentMonthVal.split('-')
  const curYear = parseInt(curYearStr, 10) || new Date().getFullYear()

  const options = []
  for (let m = 1; m <= 12; m++) {
    const val = `${curYear}-${String(m).padStart(2, '0')}`
    const isCurrent = val === currentMonthVal
    const name = timesheetMonthNames[m - 1]
    options.push({
      value: val,
      label: `${name} ${curYear}${isCurrent ? ' (Current)' : ''}`
    })
  }

  if (selectedTimesheetMonth.value && !options.some(o => o.value === selectedTimesheetMonth.value)) {
    const [y, mStr] = selectedTimesheetMonth.value.split('-')
    const mIdx = parseInt(mStr, 10) - 1
    if (mIdx >= 0 && mIdx < 12) {
      options.push({
        value: selectedTimesheetMonth.value,
        label: `${timesheetMonthNames[mIdx]} ${y}`
      })
    }
  }

  return options
})

const selectedTimesheetMonthLabel = computed(() => {
  const found = timesheetMonthOptions.value.find(m => m.value === selectedTimesheetMonth.value)
  return found ? found.label.replace(' (Current)', '') : selectedTimesheetMonth.value
})

function getStatusBadgeStyle(status) {
  if (status === 'Present') {
    return {
      background: 'rgba(16, 185, 129, 0.2)',
      color: '#10b981',
      border: '1px solid rgba(16, 185, 129, 0.4)',
      padding: '0.25rem 0.65rem',
      borderRadius: '6px',
      fontSize: '0.78rem',
      fontWeight: '700',
      display: 'inline-block'
    }
  }
  if (status === 'Absent') {
    return {
      background: 'rgba(239, 68, 68, 0.2)',
      color: '#ef4444',
      border: '1px solid rgba(239, 68, 68, 0.4)',
      padding: '0.25rem 0.65rem',
      borderRadius: '6px',
      fontSize: '0.78rem',
      fontWeight: '700',
      display: 'inline-block'
    }
  }
  if (status === 'Late / Early Out' || (status?.includes('Late') && status?.includes('Early Out'))) {
    return {
      background: 'rgba(249, 115, 22, 0.2)',
      color: '#f97316',
      border: '1px solid rgba(249, 115, 22, 0.4)',
      padding: '0.25rem 0.65rem',
      borderRadius: '6px',
      fontSize: '0.78rem',
      fontWeight: '700',
      display: 'inline-block'
    }
  }
  if (status === 'Late' || status?.includes('Late')) {
    return {
      background: 'rgba(245, 158, 11, 0.2)',
      color: '#f59e0b',
      border: '1px solid rgba(245, 158, 11, 0.4)',
      padding: '0.25rem 0.65rem',
      borderRadius: '6px',
      fontSize: '0.78rem',
      fontWeight: '700',
      display: 'inline-block'
    }
  }
  if (status === 'Early Out' || status?.includes('Early Out')) {
    return {
      background: 'rgba(59, 130, 246, 0.2)',
      color: '#3b82f6',
      border: '1px solid rgba(59, 130, 246, 0.4)',
      padding: '0.25rem 0.65rem',
      borderRadius: '6px',
      fontSize: '0.78rem',
      fontWeight: '700',
      display: 'inline-block'
    }
  }
  if (status === 'Holiday' || status?.includes('Holiday')) {
    return {
      background: 'rgba(16, 185, 129, 0.25)',
      color: '#10b981',
      border: '1px solid rgba(16, 185, 129, 0.5)',
      padding: '0.25rem 0.65rem',
      borderRadius: '6px',
      fontSize: '0.78rem',
      fontWeight: '700',
      display: 'inline-block'
    }
  }
  return {
    background: 'rgba(148, 163, 184, 0.15)',
    color: '#94a3b8',
    border: '1px solid rgba(148, 163, 184, 0.3)',
    padding: '0.25rem 0.65rem',
    borderRadius: '6px',
    fontSize: '0.78rem',
    fontWeight: '600',
    display: 'inline-block'
  }
}

const timesheetStatusFilter = ref('all') // 'all' | 'Present' | 'Late' | 'Early Out' | 'Absent' | 'Holiday'

function setTimesheetFilter(filterKey) {
  if (timesheetStatusFilter.value === filterKey) {
    timesheetStatusFilter.value = 'all'
  } else {
    timesheetStatusFilter.value = filterKey
  }
}

const allTimesheetRecords = computed(() => {
  const monthVal = selectedTimesheetMonth.value || getManilaDateString().slice(0, 7)
  const [yearStr, monthStr] = monthVal.split('-')
  const year = parseInt(yearStr, 10)
  const month = parseInt(monthStr, 10) - 1 // 0-indexed
  
  const totalDays = new Date(year, month + 1, 0).getDate()
  const todayStr = currentUserAttendanceState.value.todayDateStr
  
  let targetEmpName = userCurrentName.value
  if (selectedTimesheetEmployeeId.value !== 'current_user') {
    const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(selectedTimesheetEmployeeId.value))
    if (emp) {
      targetEmpName = emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username)
    }
  }

  const records = []
  for (let day = 1; day <= totalDays; day++) {
    const dObj = new Date(year, month, day)
    const dayOfWeek = dObj.getDay() // 0 = Sun, 6 = Sat
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6
    
    const dayFormattedStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const isToday = dayFormattedStr === todayStr
    const dateLabel = dObj.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric', weekday: 'short' })

    const holidayMatch = assignedHolidays.value.find(h => h.date === dayFormattedStr)
    const log = getTimesheetLogForDate(dayFormattedStr, selectedTimesheetEmployeeId.value, targetEmpName)

    let empDisplayName = targetEmpName
    let status = 'Not Clocked In'
    let timeIn = '--:--'
    let tInAddr = '--'
    let timeOut = '--:--'
    let tOutAddr = '--'
    let deliveredHours = 0.0
    let address = '--'

    if (log && ((log.timeIn && log.timeIn !== '--:--') || log.status)) {
      status = log.status || 'Present'
      timeIn = log.timeIn || '--:--'
      tInAddr = log.timeInAddress || log.address || (timeIn !== '--:--' ? 'HQ - Metro Manila, PH' : '--')
      timeOut = log.timeOut || '--:--'
      tOutAddr = log.timeOutAddress || log.address || (timeOut !== '--:--' ? 'HQ - Metro Manila, PH' : '--')
      deliveredHours = log.deliveredHours != null ? log.deliveredHours : 8.0
      address = tInAddr !== '--' ? tInAddr : tOutAddr
    } else if (holidayMatch) {
      empDisplayName = holidayMatch.name
      status = 'Holiday'
      timeIn = '--:--'
      tInAddr = 'N/A (Holiday)'
      timeOut = '--:--'
      tOutAddr = 'N/A (Holiday)'
      deliveredHours = 8.0
      address = 'N/A (Holiday)'
    } else if (isWeekend) {
      empDisplayName = 'Weekend / Rest Day'
      status = 'Weekend'
      timeIn = '--:--'
      tInAddr = 'N/A (Rest Day)'
      timeOut = '--:--'
      tOutAddr = 'N/A (Rest Day)'
      deliveredHours = 0.0
      address = 'N/A (Rest Day)'
    } else {
      if (log) {
        status = log.status || 'Not Clocked In'
        timeIn = log.timeIn || '--:--'
        tInAddr = log.timeInAddress || log.address || (timeIn !== '--:--' ? 'HQ - Metro Manila, PH' : '--')
        timeOut = log.timeOut || '--:--'
        tOutAddr = log.timeOutAddress || log.address || (timeOut !== '--:--' ? 'HQ - Metro Manila, PH' : '--')
        deliveredHours = log.deliveredHours != null ? log.deliveredHours : (status === 'Absent' ? 0.0 : 8.0)
        address = tInAddr !== '--' ? tInAddr : tOutAddr
      } else {
        status = 'Not Clocked In'
        timeIn = '--:--'
        tInAddr = '--'
        timeOut = '--:--'
        tOutAddr = '--'
        deliveredHours = 0.0
        address = '--'
      }
    }

    records.push({
      date: dayFormattedStr,
      formattedDate: dateLabel,
      employeeName: empDisplayName,
      status,
      timeIn,
      timeInAddress: tInAddr,
      timeInPhoto: log?.timeInPhoto || null,
      timeOut,
      timeOutAddress: tOutAddr,
      timeOutPhoto: log?.timeOutPhoto || null,
      photoPurged: !!log?.photoPurged,
      workingHours: '8',
      lunchBreak: '30 mins',
      breakTime: '30 mins',
      deliveredHours,
      isWeekend,
      isHoliday: !!holidayMatch,
      holidayName: holidayMatch?.name || '',
      holidayType: holidayMatch?.type || '',
      address,
      isToday
    })
  }

  return records
})

const filteredTimesheetRecords = computed(() => {
  const all = allTimesheetRecords.value
  if (timesheetStatusFilter.value === 'all') {
    return all
  }
  if (timesheetStatusFilter.value === 'Holiday') {
    return all.filter(r => r.isHoliday || r.status === 'Holiday')
  }
  if (timesheetStatusFilter.value === 'Late') {
    return all.filter(r => r.status?.includes('Late'))
  }
  if (timesheetStatusFilter.value === 'Early Out') {
    return all.filter(r => r.status?.includes('Early Out'))
  }
  return all.filter(r => r.status === timesheetStatusFilter.value)
})

const timesheetSummary = computed(() => {
  const records = allTimesheetRecords.value
  const presentDays = records.filter(r => r.status === 'Present').length
  const lateDays = records.filter(r => r.status?.includes('Late')).length
  const absentDays = records.filter(r => r.status === 'Absent').length
  const earlyOutDays = records.filter(r => r.status?.includes('Early Out')).length
  const holidayDays = records.filter(r => r.isHoliday || r.status === 'Holiday').length
  const workDays = records.filter(r => !r.isWeekend && !r.isHoliday).length
  const totalDeliveredHours = records.reduce((sum, r) => sum + r.deliveredHours, 0)
  return { presentDays, lateDays, absentDays, earlyOutDays, holidayDays, workDays, totalDeliveredHours }
})

// ── OVERTIME MODULE COMPUTED & STATE LOGIC ─────────────────────────────
const overtimeStatusFilter = ref('all') // 'all' | 'Pending' | 'Approved' | 'Denied'
const selectedOvertimeEmployeeId = ref('1')
const showOvertimeModal = ref(false)
const overtimeForm = ref({
  employee_id: '',
  date: getManilaDateString(),
  otIn: '17:00',
  otOut: '20:00',
  rate: '1.25x (Regular OT)',
  reason: ''
})

const populatedOvertimeLogs = computed(() => {
  const list = []
  // 1. From manualTimeLogs (entries with type === 'Overtime')
  manualTimeLogs.value.forEach(log => {
    if (log.type === 'Overtime') {
      list.push({
        id: log.id,
        employeeId: log.employeeId || 'emp_1',
        employeeName: log.employeeName,
        department: log.department || 'Operations',
        dateRange: log.dateRange,
        details: log.details,
        reason: log.reason,
        status: log.status === 'Rejected' ? 'Denied' : log.status,
        approver: log.approver,
        approverDate: log.approverDate
      })
    }
  })

  // 2. Pre-populated overtime records per user
  const defaultOvertimeRecords = [
    {
      id: 101,
      employeeId: '1',
      employeeName: 'Juan Dela Cruz',
      department: 'IT',
      dateRange: '2026-09-22',
      details: 'OT In: 05:00 PM | OT Out: 08:00 PM (3.0 hrs @ 1.25x)',
      reason: 'Critical database server migration and patch deployment',
      status: 'Approved',
      approver: 'Tech Lead - Pedro Penduko',
      approverDate: '2026-09-22 08:30 PM'
    },
    {
      id: 102,
      employeeId: '2',
      employeeName: 'Maria Santos',
      department: 'Accounting',
      dateRange: '2026-09-24',
      details: 'OT In: 05:00 PM | OT Out: 07:30 PM (2.5 hrs @ 1.25x)',
      reason: 'Month-end financial audit report preparation',
      status: 'Pending',
      approver: '--',
      approverDate: '--'
    },
    {
      id: 103,
      employeeId: '3',
      employeeName: 'Pedro Penduko',
      department: 'HR',
      dateRange: '2026-09-25',
      details: 'OT In: 05:00 PM | OT Out: 09:00 PM (4.0 hrs @ 1.50x)',
      reason: 'Urgent weekend driver onboarding document verification',
      status: 'Denied',
      approver: 'HR Director - Anna Cruz',
      approverDate: '2026-09-25 09:15 PM'
    },
    {
      id: 104,
      employeeId: 'drv_1',
      employeeName: 'Ricardo Dalisay',
      department: 'Drivers / Fleet Ops',
      dateRange: '2026-09-26',
      details: 'OT In: 06:00 PM | OT Out: 10:00 PM (4.0 hrs @ 1.25x)',
      reason: 'Extended night rush hour passenger service deployment',
      status: 'Approved',
      approver: 'Fleet Manager - Juan Dela Cruz',
      approverDate: '2026-09-26 10:05 PM'
    },
    {
      id: 105,
      employeeId: 'drv_2',
      employeeName: 'Lito Lapid',
      department: 'Drivers / Fleet Ops',
      dateRange: '2026-09-26',
      details: 'OT In: 05:00 PM | OT Out: 07:00 PM (2.0 hrs @ 1.25x)',
      reason: 'Special corporate charter trip shuttle assistance',
      status: 'Pending',
      approver: '--',
      approverDate: '--'
    },
    {
      id: 106,
      employeeId: '1',
      employeeName: 'Juan Dela Cruz',
      department: 'IT',
      dateRange: '2026-10-04',
      details: 'OT In: 05:00 PM | OT Out: 08:00 PM (3.0 hrs @ 1.25x)',
      reason: 'Emergency server infrastructure upgrade and patch deployment',
      status: 'Approved',
      approver: 'Tech Lead - Pedro Penduko',
      approverDate: '2026-10-04 08:30 PM'
    }
  ]

  defaultOvertimeRecords.forEach(rec => {
    if (!list.some(l => l.id === rec.id)) {
      list.push(rec)
    }
  })

  return list
})

const filteredOvertimeLogs = computed(() => {
  let list = populatedOvertimeLogs.value
  if (selectedOvertimeEmployeeId.value !== 'all') {
    list = list.filter(l => String(l.employeeId) === String(selectedOvertimeEmployeeId.value) || l.employeeName.includes(selectedOvertimeEmployeeId.value))
  }
  if (overtimeStatusFilter.value !== 'all') {
    if (overtimeStatusFilter.value === 'Denied') {
      list = list.filter(l => l.status === 'Denied' || l.status === 'Rejected')
    } else {
      list = list.filter(l => l.status === overtimeStatusFilter.value)
    }
  }
  return list
})

const overtimeSummary = computed(() => {
  const all = populatedOvertimeLogs.value.filter(l => String(l.employeeId) === String(selectedOvertimeEmployeeId.value) || l.employeeName.includes(selectedOvertimeEmployeeId.value))
  const totalCount = all.length
  const pendingCount = all.filter(l => l.status === 'Pending').length
  const approvedCount = all.filter(l => l.status === 'Approved').length
  const deniedCount = all.filter(l => l.status === 'Denied' || l.status === 'Rejected').length
  
  let totalOtHours = 0
  all.forEach(l => {
    const match = l.details?.match(/\((\d+(?:\.\d+)?)\s*hrs/)
    if (match) {
      totalOtHours += parseFloat(match[1])
    } else {
      totalOtHours += 3.0
    }
  })

  return {
    totalCount,
    pendingCount,
    approvedCount,
    deniedCount,
    totalOtHours: parseFloat(totalOtHours.toFixed(1))
  }
})

function approveOvertimeRequest(log) {
  log.status = 'Approved'
  log.approver = (userCurrentName.value || 'Admin') + ' (Admin)'
  log.approverDate = getManilaDateTimeString()
  
  const orig = manualTimeLogs.value.find(m => m.id === log.id)
  if (orig) {
    orig.status = 'Approved'
    orig.approver = log.approver
    orig.approverDate = log.approverDate
  }

  syncApprovedTimeLogToTimesheet(log)
}

function denyOvertimeRequest(log) {
  log.status = 'Denied'
  log.approver = (userCurrentName.value || 'Admin') + ' (Admin)'
  log.approverDate = getManilaDateTimeString()

  const orig = manualTimeLogs.value.find(m => m.id === log.id)
  if (orig) {
    orig.status = 'Rejected'
    orig.approver = log.approver
    orig.approverDate = log.approverDate
  }
}

// ── LEAVE MODULE COMPUTED & STATE LOGIC ─────────────────────────────
const leaveStatusFilter = ref('all') // 'all' | 'Pending' | 'Approved' | 'Denied'
const selectedLeaveEmployeeId = ref('1')

const populatedLeaveLogs = computed(() => {
  const list = []
  // 1. From manualTimeLogs (entries with type === 'Leave')
  manualTimeLogs.value.forEach(log => {
    if (log.type === 'Leave') {
      list.push({
        id: log.id,
        employeeId: log.employeeId || 'emp_1',
        employeeName: log.employeeName,
        department: log.department || 'Operations',
        dateRange: log.dateRange,
        details: log.details,
        reason: log.reason,
        status: log.status === 'Rejected' ? 'Denied' : log.status,
        approver: log.approver,
        approverDate: log.approverDate
      })
    }
  })

  // 2. Pre-populated leave records per user
  const defaultLeaveRecords = [
    {
      id: 201,
      employeeId: '2',
      employeeName: 'Maria Santos',
      department: 'Accounting',
      dateRange: '2026-09-28 to 2026-09-29',
      details: 'Sick Leave (2 Days)',
      reason: 'Scheduled medical procedure and recovery rest',
      status: 'Pending',
      approver: '--',
      approverDate: '--'
    },
    {
      id: 202,
      employeeId: '1',
      employeeName: 'Juan Dela Cruz',
      department: 'IT',
      dateRange: '2026-09-15 to 2026-09-17',
      details: 'Vacation Leave (3 Days)',
      reason: 'Annual family vacation trip to Boracay',
      status: 'Approved',
      approver: 'HR Manager - Anna Cruz',
      approverDate: '2026-09-10 02:30 PM'
    },
    {
      id: 203,
      employeeId: '3',
      employeeName: 'Pedro Penduko',
      department: 'HR',
      dateRange: '2026-09-21',
      details: 'Emergency Leave (1 Day)',
      reason: 'Home plumbing emergency and repair maintenance',
      status: 'Approved',
      approver: 'HR Director - Anna Cruz',
      approverDate: '2026-09-21 08:15 AM'
    },
    {
      id: 204,
      employeeId: 'drv_1',
      employeeName: 'Ricardo Dalisay',
      department: 'Drivers / Fleet Ops',
      dateRange: '2026-10-02 to 2026-10-03',
      details: 'Sick Leave (2 Days)',
      reason: 'Fever and viral flu symptoms recommendation for rest',
      status: 'Pending',
      approver: '--',
      approverDate: '--'
    },
    {
      id: 205,
      employeeId: 'drv_2',
      employeeName: 'Lito Lapid',
      department: 'Drivers / Fleet Ops',
      dateRange: '2026-09-05',
      details: 'Personal Leave (1 Day)',
      reason: 'Renewal of driver license and LTO appointment',
      status: 'Denied',
      approver: 'Fleet Manager - Juan Dela Cruz',
      approverDate: '2026-09-04 05:00 PM'
    }
  ]

  defaultLeaveRecords.forEach(rec => {
    if (!list.some(l => l.id === rec.id)) {
      list.push(rec)
    }
  })

  return list
})

const filteredLeaveLogs = computed(() => {
  let list = populatedLeaveLogs.value
  if (selectedLeaveEmployeeId.value !== 'all') {
    list = list.filter(l => String(l.employeeId) === String(selectedLeaveEmployeeId.value) || l.employeeName.includes(selectedLeaveEmployeeId.value))
  }
  if (leaveStatusFilter.value !== 'all') {
    if (leaveStatusFilter.value === 'Denied') {
      list = list.filter(l => l.status === 'Denied' || l.status === 'Rejected')
    } else {
      list = list.filter(l => l.status === leaveStatusFilter.value)
    }
  }
  return list
})

const leaveSummary = computed(() => {
  const all = populatedLeaveLogs.value.filter(l => String(l.employeeId) === String(selectedLeaveEmployeeId.value) || l.employeeName.includes(selectedLeaveEmployeeId.value))
  const totalCount = all.length
  const pendingCount = all.filter(l => l.status === 'Pending').length
  const approvedCount = all.filter(l => l.status === 'Approved').length
  const deniedCount = all.filter(l => l.status === 'Denied' || l.status === 'Rejected').length
  
  let totalLeaveDays = 0
  all.forEach(l => {
    const match = l.details?.match(/\((\d+)\s*Day/)
    if (match) {
      totalLeaveDays += parseInt(match[1], 10)
    } else {
      totalLeaveDays += 1
    }
  })

  return {
    totalCount,
    pendingCount,
    approvedCount,
    deniedCount,
    totalLeaveDays
  }
})

function approveLeaveRequest(log) {
  log.status = 'Approved'
  log.approver = (userCurrentName.value || 'Admin') + ' (Admin)'
  log.approverDate = getManilaDateTimeString()
  
  const orig = manualTimeLogs.value.find(m => m.id === log.id)
  if (orig) {
    orig.status = 'Approved'
    orig.approver = log.approver
    orig.approverDate = log.approverDate
  }

  syncApprovedTimeLogToTimesheet(log)
}

function denyLeaveRequest(log) {
  log.status = 'Denied'
  log.approver = (userCurrentName.value || 'Admin') + ' (Admin)'
  log.approverDate = getManilaDateTimeString()

  const orig = manualTimeLogs.value.find(m => m.id === log.id)
  if (orig) {
    orig.status = 'Rejected'
    orig.approver = log.approver
    orig.approverDate = log.approverDate
  }
}

// ── PAYROLL & ACCRUAL LEAVE CREDIT LOGIC ─────────────────────────
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]
const monthShortNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const selectedPayrollLeaveEmployeeId = ref('1')

const currentYear = computed(() => new Date().getFullYear())
const currentMonthIndex = computed(() => new Date().getMonth() + 1) // 1..12 (e.g. 9 for Sept)
const currentMonthName = computed(() => monthNames[new Date().getMonth()])

// Annual allocated leave set per employee (default 12 days per year)
const employeeAnnualLeaveSetMap = ref({
  '1': 12,     // Juan Dela Cruz
  '2': 12,     // Maria Santos
  '3': 12,     // Pedro Penduko
  'drv_1': 12, // Ricardo Dalisay
  'drv_2': 12  // Lito Lapid
})

// Historical remaining leave records from prior years (saved for audit history)
const priorYearLeaveRecords = ref([
  { employeeId: '1', employeeName: 'Juan Dela Cruz', year: 2025, totalSet: 12, accrued: 12, approvedUsed: 2, remaining: 10.0 },
  { employeeId: '2', employeeName: 'Maria Santos', year: 2025, totalSet: 12, accrued: 12, approvedUsed: 4, remaining: 8.0 },
  { employeeId: '3', employeeName: 'Pedro Penduko', year: 2025, totalSet: 12, accrued: 12, approvedUsed: 1, remaining: 11.0 },
  { employeeId: 'drv_1', employeeName: 'Ricardo Dalisay', year: 2025, totalSet: 12, accrued: 12, approvedUsed: 5, remaining: 7.0 },
  { employeeId: 'drv_2', employeeName: 'Lito Lapid', year: 2025, totalSet: 12, accrued: 12, approvedUsed: 3, remaining: 9.0 }
])

// Default / Mock creation dates for testing / fallback
const mockEmployeeCreationDateMap = {
  '1': '2025-01-15T08:00:00',     // Juan Dela Cruz (Created prior year 2025)
  '2': '2026-04-10T08:00:00',     // Maria Santos (Created April 2026 - current year)
  '3': '2026-06-01T08:00:00',     // Pedro Penduko (Created June 2026 - current year)
  'drv_1': '2024-11-20T08:00:00', // Ricardo Dalisay (Created prior year 2024)
  'drv_2': '2026-02-14T08:00:00'  // Lito Lapid (Created Feb 2026 - current year)
}

function calculateLeaveMetricsForEmployee(emp) {
  const empIdStr = String(emp.id || emp.employeeId)
  const empName = emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username || emp.employeeName || 'Employee')
  
  const totalSet = employeeAnnualLeaveSetMap.value[empIdStr] || 12
  const monthlyIncrement = parseFloat((totalSet / 12).toFixed(2)) // Monthly accrual rate (12/12 = 1.0)
  
  // Account creation date check (Year and Month)
  const rawCreatedAt = emp.created_at || emp.createdDate || emp.registration_date || mockEmployeeCreationDateMap[empIdStr] || '2025-01-01T08:00:00'
  const creationDate = new Date(rawCreatedAt)
  const createdYear = creationDate.getFullYear()
  const createdMonth = creationDate.getMonth() + 1 // 1..12

  let accruedMonths = currentMonthIndex.value
  let accruedNote = `${currentMonthIndex.value} Months Accrued (Jan - ${currentMonthName.value})`

  if (createdYear === currentYear.value) {
    // Registered in current year: Accrued YTD = current month - created month
    accruedMonths = Math.max(0, currentMonthIndex.value - createdMonth)
    const monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const createdMonthName = monthNamesShort[createdMonth - 1] || `Mo ${createdMonth}`
    accruedNote = `${currentMonthIndex.value} - ${createdMonth} = ${accruedMonths} Mos (Hired ${createdMonthName} ${createdYear})`
  } else if (createdYear > currentYear.value) {
    accruedMonths = 0
    accruedNote = `0 Mos (Hired Future Year ${createdYear})`
  }

  // Accrued YTD = Accrued Months * (totalSet / 12)
  const accruedYTD = parseFloat((accruedMonths * monthlyIncrement).toFixed(1))
  
  // Approved Leave Taken this year (2026)
  const approvedLogs = populatedLeaveLogs.value.filter(l => {
    const isEmpMatch = String(l.employeeId) === empIdStr || l.employeeName.toLowerCase().includes(empName.toLowerCase())
    return isEmpMatch && l.status === 'Approved'
  })

  let approvedUsedYTD = 0
  approvedLogs.forEach(l => {
    const match = l.details?.match(/\((\d+)\s*Day/)
    if (match) {
      approvedUsedYTD += parseInt(match[1], 10)
    } else {
      approvedUsedYTD += 1
    }
  })

  // Available Leave = Accrued YTD - Approved Used YTD (starts at 0, adds result per month, resets next year)
  const availableLeave = Math.max(0, parseFloat((accruedYTD - approvedUsedYTD).toFixed(1)))

  // Prior Year Remaining (Saved record from previous year)
  const priorRecord = priorYearLeaveRecords.value.find(p => String(p.employeeId) === empIdStr)
  const priorYearRemaining = priorRecord ? priorRecord.remaining : parseFloat((totalSet * 0.75).toFixed(1))

  return {
    employeeId: empIdStr,
    employeeName: empName,
    username: emp.username || 'employee',
    position: emp.position || emp.department || emp.role || 'Employee',
    totalSet,
    monthlyIncrement,
    createdYear,
    createdMonth,
    accruedMonths,
    accruedNote,
    accruedYTD,
    approvedUsedYTD,
    availableLeave,
    priorYearRemaining
  }
}

const employeePayrollLeaveTable = computed(() => {
  const options = availableSalaryEmployeeOptions.value
  return options.map(emp => calculateLeaveMetricsForEmployee(emp))
})

const selectedEmployeeLeaveMetrics = computed(() => {
  if (selectedPayrollLeaveEmployeeId.value === 'all') {
    const table = employeePayrollLeaveTable.value
    if (table.length === 0) {
      return { totalSet: 12, monthlyIncrement: 1.0, accruedYTD: 9.0, approvedUsedYTD: 0, availableLeave: 9.0, priorYearRemaining: 8.0 }
    }
    const avgSet = Math.round(table.reduce((a, b) => a + b.totalSet, 0) / table.length)
    const totalAccrued = table.reduce((a, b) => a + b.accruedYTD, 0)
    const totalUsed = table.reduce((a, b) => a + b.approvedUsedYTD, 0)
    const totalAvail = table.reduce((a, b) => a + b.availableLeave, 0)
    const totalPrior = table.reduce((a, b) => a + b.priorYearRemaining, 0)
    return {
      totalSet: avgSet,
      monthlyIncrement: (avgSet / 12).toFixed(2),
      accruedYTD: totalAccrued.toFixed(1),
      approvedUsedYTD: totalUsed.toFixed(1),
      availableLeave: totalAvail.toFixed(1),
      priorYearRemaining: totalPrior.toFixed(1)
    }
  }

  const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(selectedPayrollLeaveEmployeeId.value))
  if (emp) {
    return calculateLeaveMetricsForEmployee(emp)
  }
  return { totalSet: 12, monthlyIncrement: 1.0, accruedYTD: 9.0, approvedUsedYTD: 0, availableLeave: 9.0, priorYearRemaining: 8.0 }
})

// LEAVE CREDITS & DYNAMIC DATE RANGE LIMITER FOR LEAVE REQUESTS
const leaveAdjustmentMessage = ref('')

const currentUserAvailableLeaveCredits = computed(() => {
  const activeUser = user.value || { id: '1', full_name: userCurrentName.value }
  const metrics = calculateLeaveMetricsForEmployee(activeUser)
  return Math.max(0, Math.floor(metrics.availableLeave))
})

const maxAllowedLeaveEndDate = computed(() => {
  if (!timelogForm.value.startDate || currentUserAvailableLeaveCredits.value <= 0) return timelogForm.value.startDate
  return addDaysToDateStr(timelogForm.value.startDate, currentUserAvailableLeaveCredits.value - 1)
})

const selectedLeaveDaysCount = computed(() => {
  if (!timelogForm.value.startDate || !timelogForm.value.endDate) return 0
  return calculateDaysBetween(timelogForm.value.startDate, timelogForm.value.endDate)
})

function addDaysToDateStr(dateStr, days) {
  if (!dateStr) return ''
  const d = new Date(dateStr + 'T00:00:00')
  d.setDate(d.getDate() + days)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

function calculateDaysBetween(d1Str, d2Str) {
  if (!d1Str || !d2Str) return 0
  const d1 = new Date(d1Str + 'T00:00:00')
  const d2 = new Date(d2Str + 'T00:00:00')
  const diffTime = d2.getTime() - d1.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 3600 * 24)) + 1
  return diffDays > 0 ? diffDays : 0
}

function validateAndAdjustLeaveDates() {
  if (timelogRequestType.value !== 'Leave') return
  leaveAdjustmentMessage.value = ''

  if (currentUserAvailableLeaveCredits.value <= 0) {
    timelogRequestType.value = 'Missing In'
    alert('You have 0 available leave credits. Leave selection has been disabled.')
    return
  }

  const start = timelogForm.value.startDate
  let end = timelogForm.value.endDate

  if (!start) return

  // If end date is before start date, snap end date to start date
  if (!end || end < start) {
    timelogForm.value.endDate = start
    end = start
  }

  const requestedDays = calculateDaysBetween(start, end)
  const maxCredits = currentUserAvailableLeaveCredits.value

  if (requestedDays > maxCredits) {
    const adjustedEnd = addDaysToDateStr(start, maxCredits - 1)
    timelogForm.value.endDate = adjustedEnd
    leaveAdjustmentMessage.value = `⚠️ You only have ${maxCredits} day${maxCredits > 1 ? 's' : ''} of leave available. Date To automatically adjusted from ${end} to ${adjustedEnd} (${maxCredits} day${maxCredits > 1 ? 's' : ''}).`
  }
}

function handleLeaveDateChange() {
  validateAndAdjustLeaveDates()
}

watch([timelogRequestType, () => timelogForm.value.startDate, () => timelogForm.value.endDate, currentUserAvailableLeaveCredits], () => {
  if (timelogRequestType.value === 'Leave') {
    validateAndAdjustLeaveDates()
  }
})

// ── GENERATE PAYROLL MODULE COMPUTED & STATE LOGIC ───────────────────
const selectedPayrollYear = ref(2026)
const yearOptions = ref([2026, 2025, 2024, 2023, 2022])
const selectedPayrollPeriodKey = ref('oct_2_2026')
const selectedPayrollGenerateEmployeeId = ref('1')
const payrollProcessSuccess = ref('')

const payrollPeriodOptions = computed(() => {
  const Y = selectedPayrollYear.value || 2026
  const list = []

  for (let m = 1; m <= 12; m++) {
    const monthName = monthNames[m - 1]
    const monthShort = monthShortNames[m - 1]
    const monthSlug = monthShort.toLowerCase()

    // 1st Period: 16th to end of previous month
    let prevY = Y
    let prevM = m - 1
    if (prevM < 1) {
      prevM = 12
      prevY = Y - 1
    }
    const prevMonthShort = monthShortNames[prevM - 1]
    const lastDayPrevMonth = new Date(prevY, prevM, 0).getDate()

    const p1Start = `${prevY}-${String(prevM).padStart(2, '0')}-16`
    const p1End = `${prevY}-${String(prevM).padStart(2, '0')}-${String(lastDayPrevMonth).padStart(2, '0')}`

    list.push({
      key: `${monthSlug}_1_${Y}`,
      label: `${monthName} 1st Period (${prevMonthShort} 16 - ${prevMonthShort} ${lastDayPrevMonth}, ${prevY})`,
      start: p1Start,
      end: p1End,
      year: Y,
      month: m,
      period: 1
    })

    // 2nd Period: 1st to 15th of current month
    const p2Start = `${Y}-${String(m).padStart(2, '0')}-01`
    const p2End = `${Y}-${String(m).padStart(2, '0')}-15`

    list.push({
      key: `${monthSlug}_2_${Y}`,
      label: `${monthName} 2nd Period (${monthShort} 01 - ${monthShort} 15, ${Y})`,
      start: p2Start,
      end: p2End,
      year: Y,
      month: m,
      period: 2
    })
  }

  return list
})

watch(selectedPayrollYear, (newYear) => {
  const opts = payrollPeriodOptions.value
  if (!opts || opts.length === 0) return
  const currentBase = String(selectedPayrollPeriodKey.value || '').replace(/_\d{4}$/, '')
  const matchingKey = `${currentBase}_${newYear}`
  const match = opts.find(p => p.key === matchingKey)
  if (match) {
    selectedPayrollPeriodKey.value = match.key
  } else {
    const oct2 = opts.find(p => p.key === `oct_2_${newYear}`)
    selectedPayrollPeriodKey.value = oct2 ? oct2.key : opts[opts.length - 1].key
  }
}, { immediate: true })

const currentSelectedPeriodInfo = computed(() => {
  const match = payrollPeriodOptions.value.find(p => p.key === selectedPayrollPeriodKey.value)
  if (match) return match
  return payrollPeriodOptions.value.find(p => p.key === `oct_2_${selectedPayrollYear.value}`) || payrollPeriodOptions.value[0]
})

function getWorkingDaysCountInPeriod(startStr, endStr) {
  let count = 0
  const cur = new Date(startStr)
  const end = new Date(endStr)
  while (cur <= end) {
    const dayOfWeek = cur.getDay() // 0 = Sun, 6 = Sat
    if (dayOfWeek !== 0 && dayOfWeek !== 6) {
      count++ // Weekdays included (even if it's a holiday)
    }
    cur.setDate(cur.getDate() + 1)
  }
  return count
}

const mockEmployeeTardinessMap = {
  '1_2026-09-04': { tardyMins: 25, earlyOutMins: 0, reason: 'Late In (08:25 AM)' },
  '1_2026-09-10': { tardyMins: 15, earlyOutMins: 10, reason: 'Late In (08:15 AM) & Early Out (04:50 PM)' },
  '1_2026-08-20': { tardyMins: 20, earlyOutMins: 0, reason: 'Late In (08:20 AM)' },
  '2_2026-09-02': { tardyMins: 40, earlyOutMins: 0, reason: 'Traffic Delay (08:40 AM)' },
  '2_2026-09-11': { tardyMins: 0, earlyOutMins: 20, reason: 'Personal Appointment (04:40 PM)' },
  '3_2026-09-08': { tardyMins: 30, earlyOutMins: 15, reason: 'Subway Break (08:30 AM)' },
  'drv_1_2026-09-05': { tardyMins: 20, earlyOutMins: 0, reason: 'Vehicle Inspection' },
  'drv_2_2026-09-14': { tardyMins: 15, earlyOutMins: 15, reason: 'Fleet Shift Handover' }
}

function getEmployeeAttendanceAnalysisInPeriod(empIdStr, username, startStr, endStr) {
  let tardyMins = 0
  let earlyOutMins = 0
  let presentDaysCount = 0
  let absentDaysCount = 0
  let holidayCount = 0
  let leaveDaysCount = 0
  let workingDaysCount = 0
  const logs = []
  const absentLogs = []
  const leaveLogs = []

  let userLogs = {}
  try {
    const keysToTry = [
      `timesheet_logs_${empIdStr}_${username || 'user'}`,
      `timesheet_logs_${empIdStr}_user`,
      `timesheet_logs_current_user_${username || 'user'}`
    ]
    for (const k of keysToTry) {
      const saved = localStorage.getItem(k)
      if (saved) {
        userLogs = JSON.parse(saved)
        break
      }
    }
  } catch (e) {}

  if (Object.keys(userLogs).length === 0 && String(selectedTimesheetEmployeeId.value) === String(empIdStr)) {
    userLogs = timesheetLogs.value || {}
  }

  // Retrieve approved leave records for this employee
  const empLeaveLogs = (populatedLeaveLogs.value || []).filter(l => {
    const matchId = String(l.employeeId) === String(empIdStr)
    const matchName = username && l.employeeName && (l.employeeName.toLowerCase().includes(username.toLowerCase()) || username.toLowerCase().includes(l.employeeName.toLowerCase()))
    const isApproved = l.status === 'Approved'
    return (matchId || matchName) && isApproved
  })

  const cur = new Date(startStr)
  const end = new Date(endStr)

  while (cur <= end) {
    const yyyymmdd = cur.toISOString().split('T')[0]
    const dayOfWeek = cur.getDay() // 0 = Sun, 6 = Sat
    const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6)
    const holidayMatch = (assignedHolidays.value || []).find(h => h.date === yyyymmdd)

    if (!isWeekend) {
      workingDaysCount++
      if (holidayMatch) {
        holidayCount++
      } else {
        const mockKey = `${empIdStr}_${yyyymmdd}`
        const mockEntry = mockEmployeeTardinessMap[mockKey]
        const logEntry = userLogs[yyyymmdd]

        // Check if employee has an approved leave request on this date
        const leaveMatch = empLeaveLogs.find(l => {
          if (!l.dateRange) return false
          if (l.dateRange.includes(' to ')) {
            const [s, e] = l.dateRange.split(' to ').map(str => str.trim())
            return yyyymmdd >= s && yyyymmdd <= e
          }
          return l.dateRange.trim() === yyyymmdd
        })

        const isLeaveDay = leaveMatch || (logEntry && (logEntry.status === 'Leave' || logEntry.type === 'Leave'))

        // Check if employee has a clock-in record, manual time log, or mock entry
        const manualMatch = (manualTimeLogs.value || []).find(ml => {
          const mlId = String(ml.employeeId || '')
          const mlName = String(ml.employeeName || ml.username || '').toLowerCase()
          const matchEmp = (mlId === empIdStr || (mlId === 'current_user' && empIdStr === '1') || (username && mlName.includes(username.toLowerCase())))
          let isDateMatch = false
          if (ml.dateRange) {
            if (ml.dateRange.includes(' to ')) {
              const [s, e] = ml.dateRange.split(' to ').map(str => toIsoDate(str.trim()))
              isDateMatch = yyyymmdd >= s && yyyymmdd <= e
            } else {
              isDateMatch = toIsoDate(ml.dateRange) === yyyymmdd
            }
          }
          return matchEmp && isDateMatch
        })

        const hasClockIn = manualMatch || (logEntry && (logEntry.status === 'Present' || logEntry.status === 'Late' || logEntry.status === 'Early Out' || (logEntry.timeIn && logEntry.timeIn !== '--:--')))
        
        // Default demo accounts ('1', '2', '3') default to present if no explicit log is saved so demo tables populate smoothly
        const isDefaultDemoAccount = ['1', '2', '3'].includes(String(empIdStr))

        if (isLeaveDay) {
          leaveDaysCount++
          presentDaysCount++
          leaveLogs.push({
            date: yyyymmdd,
            details: leaveMatch?.details || logEntry?.leaveType || logEntry?.reason || 'Approved Paid Leave',
            reason: leaveMatch?.reason || 'Approved Leave Application'
          })
        } else if (hasClockIn) {
          presentDaysCount++
          const tMins = logEntry?.tardyMins != null ? logEntry.tardyMins : (mockEntry?.tardyMins || (logEntry?.status === 'Late' ? 30 : 0))
          const eoMins = logEntry?.earlyOutMins != null ? logEntry.earlyOutMins : (mockEntry?.earlyOutMins || (logEntry?.status === 'Early Out' ? 30 : 0))
          tardyMins += tMins
          earlyOutMins += eoMins

          const extracted = manualMatch ? extractTimesFromLog(manualMatch) : { tIn: logEntry?.timeIn || '08:00 AM', tOut: logEntry?.timeOut || '05:00 PM' }
          logs.push({
            date: yyyymmdd,
            timeIn: extracted.tIn || '08:00 AM',
            timeOut: extracted.tOut || '05:00 PM',
            tardyMins: tMins,
            earlyOutMins: eoMins,
            reason: manualMatch?.reason || mockEntry?.reason || (tMins > 0 ? `Late Clock In (${extracted.tIn})` : `Clock Entry (${extracted.tIn} - ${extracted.tOut})`)
          })
        } else if (mockEntry) {
          presentDaysCount++
          tardyMins += mockEntry.tardyMins || 0
          earlyOutMins += mockEntry.earlyOutMins || 0
          logs.push({ date: yyyymmdd, timeIn: '08:00 AM', timeOut: '05:00 PM', ...mockEntry })
        } else if (isDefaultDemoAccount) {
          presentDaysCount++
          logs.push({ date: yyyymmdd, timeIn: '08:00 AM', timeOut: '05:00 PM', tardyMins: 0, earlyOutMins: 0 })
        } else {
          absentDaysCount++
          absentLogs.push({
            date: yyyymmdd,
            reason: 'No clock-in record found (Absent)'
          })
        }
      }
    }
    cur.setDate(cur.getDate() + 1)
  }

  return {
    workingDaysCount,
    presentDaysCount,
    absentDaysCount,
    holidayCount,
    leaveDaysCount,
    tardyMins,
    earlyOutMins,
    totalPenaltyMins: tardyMins + earlyOutMins,
    logs,
    absentLogs,
    leaveLogs
  }
}

function calculateContributionsForSalary(salaryAmount) {
  if (!contributionRules.value || contributionRules.value.length === 0) {
    loadContributionRulesFromStorage()
  }
  const baseSal = parseFloat(salaryAmount) || 0
  const activeRules = (contributionRules.value && contributionRules.value.length > 0)
    ? contributionRules.value.filter(r => r.is_active !== false)
    : defaultContributionRulesSeed.filter(r => r.is_active !== false)

  let totalEmployeeDeduction = 0
  let totalEmployerContribution = 0

  const items = activeRules.map(rule => {
    let empAmt = 0
    let erAmt = 0

    if (rule.calc_type === 'msc_table') {
      const brackets = (rule.msc_brackets && rule.msc_brackets.length > 0) ? rule.msc_brackets : defaultMscBracketsSeed
      const matchedBracket = brackets.find(b => baseSal >= b.min_sal && baseSal <= b.max_sal) || brackets[brackets.length - 1]
      const msc = matchedBracket ? matchedBracket.msc : 0
      const empPct = matchedBracket ? (matchedBracket.emp_pct ?? rule.msc_emp_pct ?? 5.0) : 5.0
      const erPct = matchedBracket ? (matchedBracket.er_pct ?? rule.msc_er_pct ?? 10.0) : 10.0
      const ecAmt = matchedBracket ? (matchedBracket.ec ?? rule.msc_ec_amount ?? 0) : 0

      empAmt = (msc * empPct) / 100
      erAmt = (msc * erPct) / 100 + ecAmt
    } else {
      const rate = parseFloat(rule.rate) || 0
      const fullResultAmt = (baseSal * rate) / 100
      empAmt = fullResultAmt
      erAmt = 0

      if (rule.split_half) {
        empAmt = fullResultAmt / 2
        erAmt = fullResultAmt / 2
      }
    }

    totalEmployeeDeduction += empAmt
    totalEmployerContribution += erAmt

    return {
      id: rule.id,
      name: rule.name,
      calc_type: rule.calc_type || 'percentage',
      emp_amount: empAmt,
      er_amount: erAmt,
      empAmt,
      erAmt,
      total_rate: rule.rate || 0
    }
  })

  return {
    items,
    totalEmployeeDeduction,
    totalEmployerContribution
  }
}

function toIsoDate(dStr) {
  if (!dStr) return ''
  const clean = String(dStr).trim()
  if (/^\d{4}-\d{2}-\d{2}$/.test(clean)) return clean
  if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(clean)) {
    const [m, d, y] = clean.split('/')
    return `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`
  }
  const dt = new Date(clean)
  if (!isNaN(dt.getTime())) {
    const y = dt.getFullYear()
    const m = String(dt.getMonth() + 1).padStart(2, '0')
    const d = String(dt.getDate()).padStart(2, '0')
    return `${y}-${m}-${d}`
  }
  return clean
}

// ── PAYROLL OT & ND RATES MODULE LOGIC ───────────────────
const otNdRates = ref({
  regularOtMultiplier: 1.25,
  restdayOtMultiplier: 1.30,
  holidayOtMultiplier: 2.00,
  nightShiftOtMultiplier: 1.375,
  nightDiffPercentage: 10
})

const payrollOtNdSuccess = ref('')

function loadOtNdRatesFromStorage() {
  try {
    const saved = localStorage.getItem('cael_payroll_ot_nd_rates')
    if (saved) {
      const parsed = JSON.parse(saved)
      otNdRates.value = { ...otNdRates.value, ...parsed }
    }
  } catch (e) {}
}

function saveOtNdRatesToStorage() {
  try {
    localStorage.setItem('cael_payroll_ot_nd_rates', JSON.stringify(otNdRates.value))
    payrollOtNdSuccess.value = 'Overtime and Night Differential rate settings saved successfully!'
  } catch (e) {}
}

function resetOtNdRatesToDefault() {
  otNdRates.value = {
    regularOtMultiplier: 1.25,
    restdayOtMultiplier: 1.30,
    holidayOtMultiplier: 2.00,
    nightShiftOtMultiplier: 1.375,
    nightDiffPercentage: 10
  }
  saveOtNdRatesToStorage()
  payrollOtNdSuccess.value = 'Reset to statutory default rates (Regular OT 1.25x, Restday 1.30x, Holiday 2.00x, Night Diff 10%)!'
}

function extractTimesFromLog(l) {
  let tIn = l.timeIn || l.otIn || ''
  let tOut = l.timeOut || l.otOut || ''
  const details = l.details || ''

  if (details) {
    const inMatch = details.match(/(?:OT\s*)?In:\s*([0-9]{1,2}(?::[0-9]{2})?\s*(?:AM|PM)?)/i)
    const outMatch = details.match(/(?:OT\s*)?Out:\s*([0-9]{1,2}(?::[0-9]{2})?\s*(?:AM|PM)?)/i)
    if (inMatch && outMatch) {
      if (!tIn) tIn = inMatch[1].trim()
      if (!tOut) tOut = outMatch[1].trim()
    } else {
      const shiftMatch = details.match(/(?:New\s*Shift:\s*)?([0-9]{1,2}(?::[0-9]{2})?\s*(?:AM|PM)?)\s*(?:-|to)\s*([0-9]{1,2}(?::[0-9]{2})?\s*(?:AM|PM)?)/i)
      if (shiftMatch) {
        if (!tIn) tIn = shiftMatch[1].trim()
        if (!tOut) tOut = shiftMatch[2].trim()
      }
    }
  }

  return { tIn, tOut }
}

function calculateNightDiffHours(inTimeStr, outTimeStr) {
  const inMins = parseTimeToMinutes(inTimeStr)
  const outMins = parseTimeToMinutes(outTimeStr)
  if (inMins === null || outMins === null) return 0

  let shiftStart = inMins
  let shiftEnd = outMins
  if (shiftEnd < shiftStart) {
    shiftEnd += 1440 // Spans past midnight
  }
  if (shiftEnd === shiftStart) return 0

  let totalNdMins = 0
  const windows = [
    { s: -120, e: 360 },
    { s: 1320, e: 1800 },
    { s: 2760, e: 3240 }
  ]

  windows.forEach(w => {
    const oStart = Math.max(shiftStart, w.s)
    const oEnd = Math.min(shiftEnd, w.e)
    if (oEnd > oStart) {
      totalNdMins += (oEnd - oStart)
    }
  })

  return parseFloat((totalNdMins / 60).toFixed(2))
}

function computePayrollForEmployee(emp, period) {
  const empIdStr = String(emp.id || emp.employeeId)
  const empName = emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username || emp.employeeName || 'Employee')

  if (!otNdRates.value || !otNdRates.value.regularOtMultiplier) {
    loadOtNdRatesFromStorage()
  }

  // Base Salary lookup from assignedSalaries or fallback
  const salaryObj = assignedSalaries.value.find(s => String(s.employee_id) === empIdStr || s.username === emp.username)
  const monthlySalary = salaryObj ? salaryObj.salary_amount : (emp.salary_amount || (empIdStr === '1' ? 35000 : (empIdStr === '2' ? 28000 : 30000)))
  
  const monthlyWorkingDays = 22
  const dailyRate = monthlySalary / monthlyWorkingDays
  const minuteRate = dailyRate / 480 // 8 hours * 60 mins
  const hourlyRate = dailyRate / 8

  const attendanceInfo = getEmployeeAttendanceAnalysisInPeriod(empIdStr, emp.username, period.start, period.end)

  const workingDaysInPeriod = attendanceInfo.workingDaysCount
  const leaveDays = attendanceInfo.leaveDaysCount || 0
  const leavePay = leaveDays * dailyRate
  const presentDays = attendanceInfo.presentDaysCount + attendanceInfo.holidayCount
  const absentDays = attendanceInfo.absentDaysCount

  const periodBaseGross = workingDaysInPeriod * dailyRate
  const absentDeduction = absentDays * dailyRate
  const tardinessDeduction = attendanceInfo.totalPenaltyMins * minuteRate

  const earnedBaseGross = Math.max(0, periodBaseGross - absentDeduction)
  const periodBaseMinutes = workingDaysInPeriod * 480

  // 1. Calculate Approved Overtime Pay & Night Differential in Period
  const empOvertimeLogs = (populatedOvertimeLogs.value || []).concat(manualTimeLogs.value || []).filter(l => {
    const logEmpId = String(l.employeeId || l.employee_id || '')
    const matchId = logEmpId === empIdStr || 
                    (logEmpId === 'current_user' && empIdStr === '1') || 
                    (logEmpId.replace(/\D/g, '') === empIdStr.replace(/\D/g, '') && logEmpId.replace(/\D/g, '').length > 0)
    
    const logEmpName = String(l.employeeName || l.username || '').toLowerCase().trim()
    const targetName = String(empName || '').toLowerCase().trim()
    const targetUsername = String(emp.username || '').toLowerCase().trim()
    
    const matchName = (logEmpName && targetName && (logEmpName.includes(targetName) || targetName.includes(logEmpName))) ||
                      (logEmpName && targetUsername && (logEmpName.includes(targetUsername) || targetUsername.includes(logEmpName)))
    
    const logStatus = String(l.status || '').toLowerCase().trim()
    const isApprovedOrPending = logStatus === 'approved' || logStatus === 'confirmed' || logStatus === 'passed' || logStatus === 'pending' || !l.status

    return (matchId || matchName) && isApprovedOrPending
  })

  let totalPeriodOvertimeHours = 0
  let totalPeriodOvertimePay = 0
  let totalPeriodNightDiffHours = 0
  const overtimeLogsInPeriod = []
  const processedNdDatesMap = {}

  empOvertimeLogs.forEach(l => {
    let isDateInPeriod = false
    const rawDateStr = String(l.dateRange || l.date || l.otDate || '').trim()

    if (rawDateStr) {
      if (rawDateStr.includes(' to ')) {
        const parts = rawDateStr.split(' to ').map(s => toIsoDate(s.trim()))
        const s = parts[0]
        const e = parts[1] || parts[0]
        isDateInPeriod = (s <= period.end && e >= period.start)
      } else {
        const d = toIsoDate(rawDateStr)
        isDateInPeriod = (d >= period.start && d <= period.end)
      }
    }

    if (isDateInPeriod) {
      const isOtType = l.type === 'Overtime' || (l.details && l.details.toLowerCase().includes('ot'))
      const extracted = extractTimesFromLog(l)
      let otInStr = extracted.tIn
      let otOutStr = extracted.tOut

      let otHours = parseFloat(l.hours || l.otHours || 0)
      let rateMultiplier = parseFloat(otNdRates.value?.regularOtMultiplier || 1.25)

      if (l.rate) {
        const rMatch = String(l.rate).match(/(\d+(?:\.\d+)?)x/)
        if (rMatch) rateMultiplier = parseFloat(rMatch[1])
      } else if (l.details) {
        const rateMatch = l.details.match(/@\s*(\d+(?:\.\d+)?)x/i)
        if (rateMatch) {
          rateMultiplier = parseFloat(rateMatch[1])
        }
      }

      if (otHours === 0 && l.details) {
        const hrsMatch = l.details.match(/(\d+(?:\.\d+)?)\s*hrs?/i)
        if (hrsMatch) {
          otHours = parseFloat(hrsMatch[1])
        }
      }

      if (otHours === 0 && otInStr && otOutStr) {
        const inMins = parseTimeToMinutes(otInStr)
        const outMins = parseTimeToMinutes(otOutStr)
        if (inMins !== null && outMins !== null) {
          let diff = outMins - inMins
          if (diff < 0) diff += 1440
          if (diff > 0) {
            otHours = parseFloat((diff / 60).toFixed(2))
          }
        }
      }

      // Night Diff calculation for this entry if it falls between 10PM and 6AM
      if (otInStr && otOutStr) {
        const ndH = calculateNightDiffHours(otInStr, otOutStr)
        if (ndH > 0) {
          const dateKey = toIsoDate(rawDateStr)
          if (!processedNdDatesMap[dateKey] || ndH > processedNdDatesMap[dateKey]) {
            totalPeriodNightDiffHours += (ndH - (processedNdDatesMap[dateKey] || 0))
            processedNdDatesMap[dateKey] = ndH
          }
        }
      }

      if (isOtType) {
        if (otHours === 0) otHours = 2.0 // Fallback default if unparsed

        const otAmount = otHours * hourlyRate * rateMultiplier
        totalPeriodOvertimeHours += otHours
        totalPeriodOvertimePay += otAmount

        overtimeLogsInPeriod.push({
          id: l.id,
          date: rawDateStr,
          hours: otHours,
          rateMultiplier,
          amount: parseFloat(otAmount.toFixed(2)),
          details: l.details || `${otHours} hrs @ ${rateMultiplier}x`,
          reason: l.reason || 'Overtime Work'
        })
      }
    }
  })

  // 1b. Calculate Night Diff from Regular Shift Attendance Logs in Period
  if (attendanceInfo.logs && attendanceInfo.logs.length > 0) {
    attendanceInfo.logs.forEach(log => {
      if (log.timeIn && log.timeOut) {
        const ndH = calculateNightDiffHours(log.timeIn, log.timeOut)
        if (ndH > 0) {
          const dateKey = log.date
          if (!processedNdDatesMap[dateKey] || ndH > processedNdDatesMap[dateKey]) {
            totalPeriodNightDiffHours += (ndH - (processedNdDatesMap[dateKey] || 0))
            processedNdDatesMap[dateKey] = ndH
          }
        }
      }
    })
  }

  const nightDiffRatePercent = parseFloat(otNdRates.value?.nightDiffPercentage || 10)
  const ndHourlyAddon = hourlyRate * (nightDiffRatePercent / 100)
  const totalPeriodNightDiffPay = totalPeriodNightDiffHours * ndHourlyAddon

  // Check period number (1st or 2nd period of the month)
  const isFirstPeriod = (period.period === 1)
  const isSecondPeriod = (period.period === 2)

  // 2. Contributions Deduction (APPLIED WHEN CONTRIBUTION RULES ARE ACTIVE)
  if (!contributionRules.value || contributionRules.value.length === 0) {
    loadContributionRulesFromStorage()
  }
  const contribs = calculateContributionsForSalary(monthlySalary)
  const totalPeriodContributions = contribs.totalEmployeeDeduction
  const contributionItems = contribs.items

  // 3. Bonus & Deduction (APPLIED BASED ON SCHEDULE SET IN PERIOD_KEY)
  const bonusDeductionInfo = getEmployeeBonusDeductionsInPeriod(empIdStr, period.key)
  const totalPeriodBonus = bonusDeductionInfo.totalPeriodBonus
  const totalPeriodDeduction = bonusDeductionInfo.totalPeriodDeduction

  // 4. Cash Advances Deduction (DEDUCTED ONLY EVERY SECOND PERIOD OF THE MONTH)
  let totalPeriodCashAdvances = 0
  let approvedCashAdvanceItems = []
  if (isSecondPeriod) {
    if (cashAdvancesLogs.value.length === 0) {
      loadCashAdvancesFromStorage()
    }
    approvedCashAdvanceItems = cashAdvancesLogs.value.filter(adv => 
      adv.status === 'Approved' && 
      (String(adv.employee_id) === empIdStr || (emp.username && adv.username === emp.username))
    )
    totalPeriodCashAdvances = approvedCashAdvanceItems.reduce((sum, item) => sum + (parseFloat(item.amount) || 0), 0)
  }

  // Net Period Salary Formula:
  // Net = Earned Base Gross + Overtime Pay + Night Diff Pay - Tardiness - Contributions + Bonus - Deduction - Cash Advances
  const finalNetSalary = Math.max(0, earnedBaseGross + totalPeriodOvertimePay + totalPeriodNightDiffPay - tardinessDeduction - totalPeriodContributions + totalPeriodBonus - totalPeriodDeduction - totalPeriodCashAdvances)

  return {
    employeeId: empIdStr,
    employeeName: empName,
    username: emp.username || 'employee',
    position: emp.position || emp.department || emp.role || 'Employee',
    monthlySalary: parseFloat(monthlySalary.toFixed(2)),
    monthlyWorkingDays,
    dailyRate: parseFloat(dailyRate.toFixed(2)),
    minuteRate: parseFloat(minuteRate.toFixed(4)),
    hourlyRate: parseFloat(hourlyRate.toFixed(2)),
    workingDaysInPeriod,
    presentDays,
    absentDays,
    leaveDays,
    leavePay: parseFloat(leavePay.toFixed(2)),
    periodBaseGross: parseFloat(periodBaseGross.toFixed(2)),
    absentDeduction: parseFloat(absentDeduction.toFixed(2)),
    earnedBaseGross: parseFloat(earnedBaseGross.toFixed(2)),
    periodBaseMinutes,
    isFirstPeriod,
    isSecondPeriod,
    tardyMins: attendanceInfo.tardyMins,
    earlyOutMins: attendanceInfo.earlyOutMins,
    totalPenaltyMins: attendanceInfo.totalPenaltyMins,
    tardinessDeduction: parseFloat(tardinessDeduction.toFixed(2)),
    totalPeriodContributions: parseFloat(totalPeriodContributions.toFixed(2)),
    contributionItems: contributionItems || [],
    totalPeriodBonus: parseFloat(totalPeriodBonus.toFixed(2)),
    totalPeriodDeduction: parseFloat(totalPeriodDeduction.toFixed(2)),
    periodBonuses: bonusDeductionInfo.bonuses || [],
    periodDeductions: bonusDeductionInfo.deductions || [],
    totalPeriodCashAdvances: parseFloat(totalPeriodCashAdvances.toFixed(2)),
    cashAdvanceItems: approvedCashAdvanceItems || [],
    approvedCashAdvanceItems: approvedCashAdvanceItems || [],
    overtimePay: parseFloat(totalPeriodOvertimePay.toFixed(2)),
    overtimeHours: parseFloat(totalPeriodOvertimeHours.toFixed(2)),
    overtimeLogs: overtimeLogsInPeriod || [],
    nightDiffPay: parseFloat(totalPeriodNightDiffPay.toFixed(2)),
    nightDiffHours: parseFloat(totalPeriodNightDiffHours.toFixed(2)),
    nightDiffRatePercent,
    netSalary: parseFloat(finalNetSalary.toFixed(2)),
    tardyLogs: attendanceInfo.logs || [],
    absentLogs: attendanceInfo.absentLogs || [],
    leaveLogs: attendanceInfo.leaveLogs || []
  }
}

const employeeGeneratePayrollTable = computed(() => {
  const period = currentSelectedPeriodInfo.value
  const options = availableSalaryEmployeeOptions.value
  return options.map(emp => computePayrollForEmployee(emp, period))
})

const selectedEmployeePayrollDetails = computed(() => {
  const period = currentSelectedPeriodInfo.value
  const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(selectedPayrollGenerateEmployeeId.value))
  if (emp) {
    return computePayrollForEmployee(emp, period)
  }
  const defaultEmp = availableSalaryEmployeeOptions.value[0] || { id: '1', full_name: 'Juan Dela Cruz', username: 'juan_dc', position: 'IT Admin' }
  return computePayrollForEmployee(defaultEmp, period)
})

function processPayrollRun() {
  const empName = selectedEmployeePayrollDetails.value.employeeName
  const periodLabel = currentSelectedPeriodInfo.value.label
  payrollProcessSuccess.value = `Payroll successfully processed and disbursed for ${empName} (${periodLabel})! Payslip generated.`
  setTimeout(() => {
    payrollProcessSuccess.value = ''
  }, 6000)
}

function downloadPayslipPDF(payrollDetails) {
  const details = payrollDetails || selectedEmployeePayrollDetails.value
  if (!details) return

  const period = currentSelectedPeriodInfo.value
  const contribs = details.contributionItems || []

  // Extract statutory contribution values
  const sssObj = contribs.find(c => String(c.name || '').toLowerCase().includes('sss'))
  const sssAmount = sssObj ? (parseFloat(sssObj.emp_amount) || 0) : 0

  const pagibigObj = contribs.find(c => {
    const n = String(c.name || '').toLowerCase()
    return n.includes('pag-ibig') || n.includes('pagibig') || n.includes('hdmf')
  })
  const pagibigAmount = pagibigObj ? (parseFloat(pagibigObj.emp_amount) || 0) : 0

  const philhealthObj = contribs.find(c => String(c.name || '').toLowerCase().includes('philhealth'))
  const philhealthAmount = philhealthObj ? (parseFloat(philhealthObj.emp_amount) || 0) : 0

  const taxObj = contribs.find(c => {
    const n = String(c.name || '').toLowerCase()
    return n.includes('tax') || n.includes('w/tax') || n.includes('withholding')
  })
  const taxAmount = taxObj ? (parseFloat(taxObj.emp_amount) || 0) : 0

  const printWin = window.open('', '_blank', 'width=900,height=950')
  if (!printWin) {
    alert('Please allow popups for this site to download/print the PDF payslip.')
    return
  }

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Payslip - ${details.employeeName} (${period.label})</title>
  <style>
    @page { size: A4; margin: 15mm; }
    * { box-sizing: border-box; }
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #0f172a;
      background: #f8fafc;
      margin: 0;
      padding: 20px;
    }
    .payslip-container {
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      border: 2px solid #0f172a;
      border-radius: 12px;
      padding: 32px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    .header-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #cbd5e1;
      padding-bottom: 18px;
      margin-bottom: 24px;
    }
    .company-title {
      font-size: 24px;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.5px;
    }
    .document-title {
      font-size: 13px;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-top: 4px;
    }
    .period-box {
      text-align: right;
      background: #f1f5f9;
      padding: 10px 18px;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
    }
    .period-label {
      font-size: 11px;
      font-weight: 700;
      color: #475569;
      text-transform: uppercase;
    }
    .period-dates {
      font-size: 15px;
      font-weight: 800;
      color: #0284c7;
      margin-top: 2px;
    }
    .employee-info-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px 24px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 16px 20px;
      margin-bottom: 28px;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
    }
    .info-label { color: #64748b; font-weight: 600; }
    .info-value { color: #0f172a; font-weight: 700; }
    
    .section-heading {
      font-size: 14px;
      font-weight: 800;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 12px;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 6px;
    }

    .payslip-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 28px;
    }
    .payslip-table th {
      background: #0f172a;
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 10px 16px;
      text-align: left;
    }
    .payslip-table td {
      padding: 12px 16px;
      border-bottom: 1px solid #e2e8f0;
      font-size: 13px;
    }
    .item-title { font-weight: 700; color: #1e293b; }
    .item-sub { font-size: 11px; color: #64748b; margin-top: 2px; }
    .amount-cell {
      text-align: right;
      font-family: 'Courier New', Courier, monospace;
      font-weight: 700;
      font-size: 14px;
    }
    .text-deduction { color: #dc2626; }
    .text-addition { color: #16a34a; }

    .total-salary-card {
      background: #0f172a;
      color: #ffffff;
      border-radius: 10px;
      padding: 20px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 20px;
    }
    .total-title {
      font-size: 16px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .total-sub {
      font-size: 11px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .total-value {
      font-size: 28px;
      font-weight: 900;
      color: #4ade80;
      font-family: 'Courier New', Courier, monospace;
    }

    .no-print-bar {
      margin-bottom: 20px;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
    }
    .print-btn {
      background: #0284c7;
      color: #ffffff;
      border: none;
      padding: 10px 22px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
    }
    @media print {
      .no-print-bar { display: none !important; }
      body { background: #fff; padding: 0; }
      .payslip-container { border: none; box-shadow: none; padding: 0; }
    }
  </style>
</head>
<body>
  <div class="no-print-bar">
    <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
  </div>

  <div class="payslip-container">
    <div class="header-banner">
      <div>
        <div class="company-name">EMPLOYEE PAYSLIP</div>
        <div class="document-title">Official Salary Disbursement Document</div>
      </div>
      <div class="period-box">
        <div class="period-label">Payslip Date Span</div>
        <div class="period-dates">${period.start} to ${period.end}</div>
      </div>
    </div>

    <div class="employee-info-grid">
      <div class="info-row"><span class="info-label">Employee Name:</span> <span class="info-value">${details.employeeName}</span></div>
      <div class="info-row"><span class="info-label">Username:</span> <span class="info-value">@${details.username}</span></div>
      <div class="info-row"><span class="info-label">Position / Title:</span> <span class="info-value">${details.position}</span></div>
      <div class="info-row"><span class="info-label">Monthly Salary:</span> <span class="info-value">₱${details.monthlySalary.toLocaleString('en-US', {minimumFractionDigits: 2})}</span></div>
      <div class="info-row"><span class="info-label">Daily Rate:</span> <span class="info-value">₱${details.dailyRate.toFixed(2)}/day</span></div>
      <div class="info-row"><span class="info-label">Working Days in Period:</span> <span class="info-value">${details.workingDaysInPeriod} Days (${details.presentDays - (details.leaveDays || 0)} Logged, ${details.leaveDays || 0} Leave, ${details.absentDays} Absent)</span></div>
    </div>

    <div class="section-heading">Salary Breakdown & Deductions</div>

    <table class="payslip-table">
      <thead>
        <tr>
          <th style="width: 65%;">Description / Item Name</th>
          <th style="width: 35%; text-align: right;">Amount (₱)</th>
        </tr>
      </thead>
      <tbody>
        <!-- BASE SALARY -->
        <tr>
          <td>
            <div class="item-title">Salary (Period Base Gross)</div>
            <div class="item-sub">${details.workingDaysInPeriod} working days × ₱${details.dailyRate.toFixed(2)}/day</div>
          </td>
          <td class="amount-cell text-addition">₱${details.periodBaseGross.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        </tr>

        <!-- APPROVED LEAVE PAY (IF HAS VALUE) -->
        ${details.leavePay > 0 ? `
        <tr>
          <td>
            <div class="item-title">Approved Paid Leave Pay (+)</div>
            <div class="item-sub">${details.leaveDays} day(s) approved leave × ₱${details.dailyRate.toFixed(2)}/day</div>
          </td>
          <td class="amount-cell text-addition">+₱${details.leavePay.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        </tr>
        ` : ''}

        <!-- APPROVED OVERTIME PAY (IF HAS VALUE) -->
        ${(details.overtimePay || 0) > 0 ? `
        <tr>
          <td>
            <div class="item-title">Approved Overtime Pay (+)</div>
            <div class="item-sub">${details.overtimeHours || 0} OT hour(s) approved in period</div>
          </td>
          <td class="amount-cell text-addition">+₱${details.overtimePay.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        </tr>
        ` : ''}

        <!-- APPROVED NIGHT DIFFERENTIAL PAY (IF HAS VALUE) -->
        ${(details.nightDiffPay || 0) > 0 ? `
        <tr>
          <td>
            <div class="item-title">Night Differential Pay (+)</div>
            <div class="item-sub">${details.nightDiffHours || 0} hour(s) worked between 10:00 PM - 06:00 AM (${details.nightDiffRatePercent || 10}% ND rate)</div>
          </td>
          <td class="amount-cell text-addition">+₱${details.nightDiffPay.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        </tr>
        ` : ''}

        <!-- ABSENT PENALTY (IF HAS VALUE) -->
        ${details.absentDeduction > 0 ? `
        <tr>
          <td>
            <div class="item-title">Absent Penalty (Un-clocked Workdays)</div>
            <div class="item-sub">${details.absentDays} day(s) absent × ₱${details.dailyRate.toFixed(2)}/day</div>
          </td>
          <td class="amount-cell text-deduction">-₱${details.absentDeduction.toFixed(2)}</td>
        </tr>
        ` : ''}

        <!-- STATUTORY CONTRIBUTIONS -->
        <tr>
          <td>
            <div class="item-title">SSS Contribution</div>
            <div class="item-sub">${details.isFirstPeriod ? '1st Period Statutory Contribution' : 'Skipped (1st Period Only)'}</div>
          </td>
          <td class="amount-cell text-deduction">${sssAmount > 0 ? '-₱' + sssAmount.toFixed(2) : '₱0.00'}</td>
        </tr>

        <tr>
          <td>
            <div class="item-title">Pag-IBIG Contribution</div>
            <div class="item-sub">${details.isFirstPeriod ? '1st Period Statutory Contribution' : 'Skipped (1st Period Only)'}</div>
          </td>
          <td class="amount-cell text-deduction">${pagibigAmount > 0 ? '-₱' + pagibigAmount.toFixed(2) : '₱0.00'}</td>
        </tr>

        <tr>
          <td>
            <div class="item-title">PhilHealth Contribution</div>
            <div class="item-sub">${details.isFirstPeriod ? '1st Period Statutory Contribution' : 'Skipped (1st Period Only)'}</div>
          </td>
          <td class="amount-cell text-deduction">${philhealthAmount > 0 ? '-₱' + philhealthAmount.toFixed(2) : '₱0.00'}</td>
        </tr>

        <tr>
          <td>
            <div class="item-title">Withholding Tax (Tax)</div>
            <div class="item-sub">${details.isFirstPeriod ? '1st Period Statutory Tax' : 'Skipped (1st Period Only)'}</div>
          </td>
          <td class="amount-cell text-deduction">${taxAmount > 0 ? '-₱' + taxAmount.toFixed(2) : '₱0.00'}</td>
        </tr>

        <!-- TARDINESS (IF HAS VALUE) -->
        ${(details.tardinessDeduction > 0 || details.totalPenaltyMins > 0) ? `
        <tr>
          <td>
            <div class="item-title">Tardiness & Early Out Penalty</div>
            <div class="item-sub">${details.totalPenaltyMins} mins penalty × ₱${details.minuteRate.toFixed(4)}/min</div>
          </td>
          <td class="amount-cell text-deduction">-₱${details.tardinessDeduction.toFixed(2)}</td>
        </tr>
        ` : ''}

        <!-- ADVANCES (IF EXIST) -->
        ${details.totalPeriodCashAdvances > 0 ? `
        <tr>
          <td>
            <div class="item-title">Advances (Cash Advances)</div>
            <div class="item-sub">Approved 2nd Period Cash Advance Requests</div>
          </td>
          <td class="amount-cell text-deduction">-₱${details.totalPeriodCashAdvances.toFixed(2)}</td>
        </tr>
        ` : ''}

        <!-- BONUS IF EXIST -->
        ${details.totalPeriodBonus > 0 ? `
        <tr>
          <td>
            <div class="item-title">Bonus</div>
            <div class="item-sub">Scheduled Period Bonus Additions</div>
          </td>
          <td class="amount-cell text-addition">+₱${details.totalPeriodBonus.toFixed(2)}</td>
        </tr>
        ` : ''}

        <!-- DEDUCTIONS IF EXIST -->
        ${details.totalPeriodDeduction > 0 ? `
        <tr>
          <td>
            <div class="item-title">Deductions</div>
            <div class="item-sub">Scheduled Period Deduction Penalties</div>
          </td>
          <td class="amount-cell text-deduction">-₱${details.totalPeriodDeduction.toFixed(2)}</td>
        </tr>
        ` : ''}
      </tbody>
    </table>

    <div class="total-salary-card">
      <div>
        <div class="total-title">Total Salary</div>
        <div class="total-sub">Net Take Home Pay for this Salary Period</div>
      </div>
      <div class="total-value">₱${details.netSalary.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
    </div>
  </div>

  \<script>
    window.onload = function() {
      setTimeout(function() { window.print(); }, 350);
    }
  <\/script>
</body>
</html>`

  printWin.document.write(html)
  printWin.document.close()
}

// HOLIDAY FORM & DATA STATE
const calendarYear = ref(new Date().getFullYear())
const calendarMonth = ref(new Date().getMonth()) // Default current month (0-indexed)

function prevCalendarMonth() {
  if (calendarMonth.value === 0) {
    calendarMonth.value = 11
    calendarYear.value--
  } else {
    calendarMonth.value--
  }
}

function nextCalendarMonth() {
  if (calendarMonth.value === 11) {
    calendarMonth.value = 0
    calendarYear.value++
  } else {
    calendarMonth.value++
  }
}

const editingHolidayId = ref(null)
const holidayForm = ref({
  name: '',
  date: '',
  type: 'Regular Holiday'
})
const holidaySuccess = ref('')
const holidayError = ref('')
const assignedHolidays = ref([
  { id: 1, name: "New Year's Day", date: '2026-01-01', type: 'Regular Holiday', status: 'Active' },
  { id: 2, name: 'EDSA People Power Anniversary', date: '2026-02-25', type: 'Special Working Holiday', status: 'Active' },
  { id: 3, name: 'Maundy Thursday', date: '2026-04-02', type: 'Regular Holiday', status: 'Active' },
  { id: 4, name: 'Good Friday', date: '2026-04-03', type: 'Regular Holiday', status: 'Active' },
  { id: 5, name: 'Araw ng Kagitingan', date: '2026-04-09', type: 'Regular Holiday', status: 'Active' },
  { id: 6, name: 'Labor Day', date: '2026-05-01', type: 'Regular Holiday', status: 'Active' },
  { id: 7, name: 'Independence Day', date: '2026-06-12', type: 'Regular Holiday', status: 'Active' },
  { id: 8, name: 'Ninoy Aquino Day', date: '2026-08-21', type: 'Special Non-Working Holiday', status: 'Active' },
  { id: 9, name: 'National Heroes Day', date: '2026-08-31', type: 'Regular Holiday', status: 'Active' },
  { id: 10, name: "All Saints' Day", date: '2026-11-01', type: 'Special Non-Working Holiday', status: 'Active' },
  { id: 11, name: "All Souls' Day", date: '2026-11-02', type: 'Special Non-Working Holiday', status: 'Active' },
  { id: 12, name: 'Bonifacio Day', date: '2026-11-30', type: 'Regular Holiday', status: 'Active' },
  { id: 13, name: 'Feast of the Immaculate Conception', date: '2026-12-08', type: 'Special Non-Working Holiday', status: 'Active' },
  { id: 14, name: 'Christmas Day', date: '2026-12-25', type: 'Regular Holiday', status: 'Active' },
  { id: 15, name: 'Rizal Day', date: '2026-12-30', type: 'Regular Holiday', status: 'Active' },
  { id: 16, name: 'Last Day of the Year', date: '2026-12-31', type: 'Special Non-Working Holiday', status: 'Active' }
])

const calendarDays = computed(() => {
  const year = calendarYear.value
  const month = calendarMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  
  let targetEmpName = userCurrentName.value
  if (selectedTimesheetEmployeeId.value !== 'current_user') {
    const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(selectedTimesheetEmployeeId.value))
    if (emp) {
      targetEmpName = emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username)
    }
  }

  const days = []
  for (let i = 0; i < firstDay; i++) {
    days.push({ day: null, dateStr: '', holiday: null })
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const monthStr = (month + 1).toString().padStart(2, '0')
    const dayStr = d.toString().padStart(2, '0')
    const dateStr = `${year}-${monthStr}-${dayStr}`
    
    const holiday = assignedHolidays.value.find(h => h.date === dateStr)
    const dObj = new Date(year, month, d)
    const dayOfWeek = dObj.getDay()
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6
    
    const log = getTimesheetLogForDate(dateStr, selectedTimesheetEmployeeId.value, targetEmpName)

    let status = 'Absent'
    let statusText = '🔴 Absent'
    let bg = 'rgba(239, 68, 68, 0.15)'
    let border = '1px solid rgba(239, 68, 68, 0.35)'
    let color = '#ef4444'
    let timeIn = '--:--'
    let timeOut = '--:--'

    if (log && ((log.timeIn && log.timeIn !== '--:--') || log.status)) {
      status = log.status || 'Present'
      timeIn = log.timeIn || '--:--'
      timeOut = log.timeOut || '--:--'
      if (status === 'Present') {
        statusText = holiday ? '🟢 Present (Holiday)' : (isWeekend ? '🟢 Present (Rest Day)' : '🟢 Present')
        bg = 'rgba(16, 185, 129, 0.18)'
        border = '1px solid #10b981'
        color = '#10b981'
      } else if (status === 'Late') {
        statusText = holiday ? '🟠 Late (Holiday)' : (isWeekend ? '🟠 Late (Rest Day)' : '🟠 Late')
        bg = 'rgba(245, 158, 11, 0.18)'
        border = '1px solid #f59e0b'
        color = '#f59e0b'
      } else if (status === 'Early Out') {
        statusText = holiday ? '🔵 Early Out (Holiday)' : (isWeekend ? '🔵 Early Out (Rest Day)' : '🔵 Early Out')
        bg = 'rgba(59, 130, 246, 0.18)'
        border = '1px solid #3b82f6'
        color = '#3b82f6'
      } else if (status === 'Late / Early Out') {
        statusText = holiday ? '🟠 Late / Early Out (Holiday)' : (isWeekend ? '🟠 Late / Early Out (Rest Day)' : '🟠 Late / Early Out')
        bg = 'rgba(249, 115, 22, 0.18)'
        border = '1px solid #f97316'
        color = '#f97316'
      } else if (status === 'Absent') {
        statusText = '🔴 Absent'
        bg = 'rgba(239, 68, 68, 0.18)'
        border = '1px solid #ef4444'
        color = '#ef4444'
      }
    } else if (holiday) {
      status = 'Holiday'
      statusText = '🎉 ' + (holiday.type === 'Regular Holiday' ? 'Regular' : 'Holiday')
      bg = 'rgba(16, 185, 129, 0.25)'
      border = '1px solid rgba(16, 185, 129, 0.5)'
      color = '#10b981'
    } else if (isWeekend) {
      status = 'Weekend'
      statusText = '☕ Rest'
      bg = 'rgba(30, 41, 59, 0.45)'
      border = '1px solid rgba(255, 255, 255, 0.08)'
      color = '#94a3b8'
    }

    days.push({ 
      day: d, 
      dateStr, 
      holiday,
      isWeekend,
      status,
      statusText,
      bg,
      border,
      color,
      timeIn,
      timeOut
    })
  }
  return days
})

function selectCalendarDate(dateStr) {
  if (!dateStr) return
  holidayForm.value.date = dateStr
  const existing = assignedHolidays.value.find(h => h.date === dateStr)
  if (existing) {
    editHoliday(existing)
  } else {
    editingHolidayId.value = null
    holidayForm.value.name = ''
    holidayForm.value.type = 'Regular Holiday'
  }
}

function getHolidayTitle(h) {
  if (!h) return ''
  return `${h.name} (${h.type})`
}

function getDayStyle(item) {
  if (!item.day) return { minHeight: '85px', border: 'none', background: 'transparent' }
  return {
    minHeight: '85px',
    padding: '0.45rem',
    borderRadius: '10px',
    background: item.bg || 'rgba(30, 41, 59, 0.6)',
    border: item.border || '1px solid rgba(255,255,255,0.08)',
    boxShadow: item.status === 'Holiday' ? '0 0 10px rgba(16, 185, 129, 0.25)' : (item.status === 'Present' ? '0 0 8px rgba(16, 185, 129, 0.2)' : 'none'),
    cursor: 'pointer',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    transition: 'all 0.2s ease'
  }
}

function getDayNumberColor(item) {
  const t = item.holiday?.type
  if (t === 'Regular Holiday') return '#ef4444'
  if (t === 'Special Non-Working Holiday') return '#60a5fa'
  if (t === 'Special Working Holiday') return '#fbbf24'
  return '#e2e8f0'
}

function getDayNumberStyle(item) {
  return {
    fontSize: '0.85rem',
    fontWeight: '700',
    color: getDayNumberColor(item)
  }
}

function getHolidayBadgeBg(t) {
  if (t === 'Regular Holiday') return 'rgba(239, 68, 68, 0.85)'
  if (t === 'Special Non-Working Holiday') return 'rgba(59, 130, 246, 0.85)'
  return 'rgba(245, 158, 11, 0.85)'
}

function getHolidayBadgeStyle(holiday) {
  if (!holiday) return {}
  return {
    fontSize: '0.68rem',
    fontWeight: '700',
    lineHeight: '1.2',
    textAlign: 'left',
    marginTop: '0.2rem',
    padding: '0.15rem 0.35rem',
    borderRadius: '4px',
    width: '100%',
    boxSizing: 'border-box',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    background: getHolidayBadgeBg(holiday.type),
    color: '#ffffff'
  }
}

function editHoliday(h) {
  editingHolidayId.value = h.id
  holidayForm.value = {
    name: h.name,
    date: h.date,
    type: h.type || 'Regular Holiday'
  }
  holidaySuccess.value = ''
  holidayError.value = ''
}

function cancelEditHoliday() {
  editingHolidayId.value = null
  holidayForm.value = {
    name: '',
    date: '',
    type: 'Regular Holiday'
  }
}

function submitHoliday() {
  holidaySuccess.value = ''
  holidayError.value = ''
  if (!holidayForm.value.name.trim()) {
    holidayError.value = 'Please enter a holiday name.'
    return
  }
  if (!holidayForm.value.date) {
    holidayError.value = 'Please select a holiday date.'
    return
  }

  if (editingHolidayId.value) {
    const idx = assignedHolidays.value.findIndex(h => h.id === editingHolidayId.value)
    if (idx !== -1) {
      assignedHolidays.value[idx] = {
        ...assignedHolidays.value[idx],
        name: holidayForm.value.name.trim(),
        date: holidayForm.value.date,
        type: holidayForm.value.type
      }
    }
    holidaySuccess.value = `Holiday updated successfully for ${holidayForm.value.name}!`
    cancelEditHoliday()
  } else {
    assignedHolidays.value.unshift({
      id: Date.now(),
      name: holidayForm.value.name.trim(),
      date: holidayForm.value.date,
      type: holidayForm.value.type,
      status: 'Active'
    })
    holidaySuccess.value = `Holiday added successfully for ${holidayForm.value.name}!`
    cancelEditHoliday()
  }
}

function removeHoliday(hId) {
  if (editingHolidayId.value === hId) {
    cancelEditHoliday()
  }
  assignedHolidays.value = assignedHolidays.value.filter(h => h.id !== hId)
}



// REAL-TIME SUPPORT CHAT SYSTEM STATE & LOGIC
const activeSupportTab = ref('queue') // 'queue' | 'active' | 'monitor'
const supportWaitingQueue = ref([])
const activeSupportSessions = ref([])
const dailySupportMonitorLogs = ref([])
const currentActiveSessionId = ref(null)
const supportChatMessageInput = ref('')
const selectedHistoryTranscriptModal = ref(null)
let supportPollTimer = null

const currentActiveSession = computed(() => {
  if (!currentActiveSessionId.value && activeSupportSessions.value.length > 0) {
    return activeSupportSessions.value[0]
  }
  return activeSupportSessions.value.find(s => s.id === currentActiveSessionId.value) || activeSupportSessions.value[0] || null
})

async function fetchSupportData() {
  try {
    // 1. Fetch waiting queue
    const waitingRes = await authApi.getSupportWaitingTickets()
    supportWaitingQueue.value = (waitingRes || []).map(q => ({
      id: q.id,
      userName: q.user_name,
      username: q.user_name.toLowerCase().replace(/\s+/g, '_'),
      roleLabel: q.user_role || 'User',
      topic: q.topic,
      messageSnippet: q.message_snippet,
      createdTime: q.created_at,
      waitTime: q.time_ago || 'Just now',
      priority: (q.topic || '').includes('Urgent') || (q.topic || '').includes('Issue') ? 'Urgent' : 'Normal'
    }))

    // 2. Fetch all active live chat sessions across all users & admins
    const activeRes = await authApi.getSupportActiveTickets()
    const activeList = []

    for (const ticket of activeRes || []) {
      const msgRes = await authApi.getSupportTicketMessages(ticket.id)
      activeList.push({
        id: ticket.id,
        userName: ticket.user_name,
        username: ticket.user_name.toLowerCase().replace(/\s+/g, '_'),
        roleLabel: ticket.user_role || 'User',
        topic: ticket.topic,
        agentName: ticket.agent_name,
        messages: (msgRes.messages || []).map(m => ({
          id: m.id,
          sender: m.sender_type,
          senderName: m.sender_name,
          text: m.text,
          time: m.created_at
        }))
      })
    }
    activeSupportSessions.value = activeList
    if (activeList.length > 0 && !currentActiveSessionId.value) {
      currentActiveSessionId.value = activeList[0].id
    }

    // 3. Fetch support work history (daily monitor)
    const historyRes = await authApi.getSupportHistory()
    dailySupportMonitorLogs.value = (historyRes || []).map(h => ({
      id: h.id,
      userName: h.user_name,
      username: h.user_name.toLowerCase().replace(/\s+/g, '_'),
      roleLabel: h.user_role,
      topic: h.topic,
      startTime: h.created_at,
      endTime: h.resolved_at || 'In Progress',
      duration: h.message_count + ' msgs',
      agentName: h.agent_name,
      outcome: h.status === 'resolved' ? 'Resolved' : h.status,
      transcript: []
    }))
  } catch (err) {
    console.error('Error fetching support data:', err)
  }
}

async function claimSupportQueueItem(qItem) {
  try {
    const currentAgentName = user.value?.full_name || 'Admin Support'
    await authApi.claimSupportTicket(qItem.id, currentAgentName)
    activeSupportTab.value = 'active'
    currentActiveSessionId.value = qItem.id
    await fetchSupportData()
  } catch (err) {
    alert('Failed to claim support ticket: ' + err.message)
  }
}

async function sendSupportMessage() {
  if (!supportChatMessageInput.value.trim() || !currentActiveSession.value) return
  const text = supportChatMessageInput.value.trim()
  supportChatMessageInput.value = ''
  try {
    const currentAgentName = user.value?.full_name || 'Admin Support'
    await authApi.sendSupportTicketMessage(currentActiveSession.value.id, 'agent', currentAgentName, text)
    await fetchSupportData()
  } catch (err) {
    alert('Failed to send message: ' + err.message)
  }
}

function sendCannedResponse(text) {
  supportChatMessageInput.value = text
  sendSupportMessage()
}

async function resolveSupportSession(session) {
  if (!session) return
  try {
    await authApi.resolveSupportTicket(session.id)
    await fetchSupportData()
    if (activeSupportSessions.value.length > 0) {
      currentActiveSessionId.value = activeSupportSessions.value[0].id
    } else {
      currentActiveSessionId.value = null
      activeSupportTab.value = 'queue'
    }
  } catch (err) {
    alert('Failed to resolve support session: ' + err.message)
  }
}

// Start live polling for support requests
onMounted(() => {
  fetchSupportData()
  supportPollTimer = setInterval(fetchSupportData, 3000)
})

onUnmounted(() => {
  if (supportPollTimer) clearInterval(supportPollTimer)
})

// ROLE PERMISSIONS & ACCESS SETUP MODAL STATE
const isRoleSetupAdmin = computed(() => {
  const r = (user.value?.role || '').toLowerCase()
  return r === 'admin' || r === 'super_admin' || r === 'superadmin'
})
const showRoleSetupModal = ref(false)
const selectedRoleToConfigure = ref('admin')
const savedRolePermsRaw = localStorage.getItem('cael_role_permissions')
const rolePermissionsMap = ref(savedRolePermsRaw ? JSON.parse(savedRolePermsRaw) : {})
const isSavingPermissions = ref(false)
const saveAlertMessage = ref('')
const saveAlertStatus = ref('success')
const showAccessSavedSuccessModal = ref(false)
const accessSavedSuccessDetails = ref({ roleLabel: '', message: '' })

const isPermGroupOpen = ref({
  employee: false,
  core: false,
  ops: false,
  accounting: false,
  attendance: false,
  payroll: false,
  support: false,
  setup: false,
  overview: false
})

const menuSwitches = ref({
  employee_list: true,
  add_employee: true,
  drivers: true,
  passengers: true,
  admins: true,
  topups: true,
  bookings: true,
  doc_bookings: true,
  stats: true,
  accounting: true,
  attendance_timesheet: true,
  attendance_timelog: true,
  attendance_overtime: true,
  attendance_leave: true,
  attendance_holiday: true,
  attendance_photo_verification: true,
  attendance_approver: true,
  payroll_schedule: true,
  payroll_salary: true,
  payroll_leave: true,
  payroll_generate: true,
  payroll_advances: true,
  payroll_contributions: true,
  payroll_bonus_deduction: true,
  payroll_ot_nd: true,
  payroll_approver: true,
  support_chat: true,
  create_department: true,
  create_position: true,
  set_access: true,
  overview: true
})

const defaultRolesList = [
  { key: 'super_admin', label: 'Super Administrator' },
  { key: 'admin', label: 'Admin' },
  { key: 'it_admin', label: 'IT Admin' },
  { key: 'senior_developer', label: 'Senior Developer' },
  { key: 'hr_staff', label: 'HR Staff' },
  { key: 'finance_staff', label: 'Finance Staff' },
  { key: 'operations_manager', label: 'Operations Manager' },
  { key: 'driver', label: 'Driver' },
  { key: 'passenger', label: 'Passenger' }
]

const availableRolesToConfigure = computed(() => {
  const map = new Map()
  
  // 1. Department - Position pairs created in Setup
  departments.value.forEach(dept => {
    const positions = departmentPositions.value[dept] || []
    positions.forEach(pos => {
      const k = pos.trim().toLowerCase().replace(/\s+/g, '_')
      map.set(k, { key: k, label: `${dept} - ${pos.trim()}` })
    })
  })

  // 2. Default System Roles
  defaultRolesList.forEach(r => {
    const k = r.key.toLowerCase()
    if (!map.has(k)) {
      map.set(k, { key: k, label: r.label })
    }
  })

  // 3. Positions from registered employee accounts
  employeeUsers.value.forEach(emp => {
    if (emp.position) {
      const k = emp.position.trim().toLowerCase().replace(/\s+/g, '_')
      if (!map.has(k)) {
        const deptPrefix = emp.department ? `${emp.department} - ` : ''
        map.set(k, { key: k, label: `${deptPrefix}${emp.position.trim()}` })
      }
    }
  })

  return Array.from(map.values())
})

function getRoleLabel(roleKey) {
  const found = availableRolesToConfigure.value.find(r => r.key.toLowerCase() === (roleKey || '').toLowerCase())
  if (found) return found.label
  return (roleKey || 'Admin').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function handleRoleSelectionChange() {
  saveAlertMessage.value = ''
  const roleKey = (selectedRoleToConfigure.value || '').toLowerCase().replace(/\s+/g, '_')
  const savedConfig = rolePermissionsMap.value[roleKey] || rolePermissionsMap.value[selectedRoleToConfigure.value]
  
  if (savedConfig && typeof savedConfig === 'object') {
    // Show saved data if there is already saved data so it will also be editable!
    menuSwitches.value = {
      employee_list: savedConfig.employee_list !== false,
      add_employee: savedConfig.add_employee !== false,
      drivers: savedConfig.drivers !== false,
      passengers: savedConfig.passengers !== false,
      admins: savedConfig.admins !== false,
      topups: savedConfig.topups !== false,
      bookings: savedConfig.bookings !== false,
      doc_bookings: savedConfig.doc_bookings !== false,
      stats: savedConfig.stats !== false,
      accounting: savedConfig.accounting !== false,
      attendance_timesheet: savedConfig.attendance_timesheet !== false,
      attendance_timelog: savedConfig.attendance_timelog !== false,
      attendance_tardiness: savedConfig.attendance_tardiness !== false,
      attendance_absent: savedConfig.attendance_absent !== false,
      attendance_overtime: savedConfig.attendance_overtime !== false,
      attendance_leave: savedConfig.attendance_leave !== false,
      attendance_holiday: savedConfig.attendance_holiday !== false,
      attendance_photo_verification: savedConfig.attendance_photo_verification !== false,
      attendance_approver: savedConfig.attendance_approver !== false,
      payroll_schedule: savedConfig.payroll_schedule !== false,
      payroll_salary: savedConfig.payroll_salary !== false,
      payroll_leave: savedConfig.payroll_leave !== false,
      payroll_generate: savedConfig.payroll_generate !== false,
      payroll_advances: savedConfig.payroll_advances !== false,
      payroll_contributions: savedConfig.payroll_contributions !== false,
      payroll_bonus_deduction: savedConfig.payroll_bonus_deduction !== false,
      payroll_ot_nd: savedConfig.payroll_ot_nd !== false,
      payroll_approver: savedConfig.payroll_approver !== false,
      support_chat: savedConfig.support_chat !== false,
      create_department: savedConfig.create_department !== false,
      create_position: savedConfig.create_position !== false,
      set_access: savedConfig.set_access !== false,
      overview: savedConfig.overview !== false
    }
  } else {
    // Unsaved role defaults
    menuSwitches.value = {
      employee_list: true,
      add_employee: true,
      drivers: true,
      passengers: true,
      admins: true,
      topups: true,
      bookings: true,
      doc_bookings: true,
      stats: true,
      accounting: true,
      attendance_timesheet: true,
      attendance_timelog: true,
      attendance_tardiness: true,
      attendance_absent: true,
      attendance_overtime: true,
      attendance_leave: true,
      attendance_holiday: true,
      attendance_photo_verification: true,
      attendance_approver: true,
      payroll_schedule: true,
      payroll_salary: true,
      payroll_leave: true,
      payroll_generate: true,
      payroll_advances: true,
      payroll_contributions: true,
      payroll_bonus_deduction: true,
      payroll_ot_nd: true,
      payroll_approver: true,
      support_chat: true,
      create_department: true,
      create_position: true,
      set_access: true,
      overview: true
    }
  }
}

async function openRoleSetupModal() {
  activeView.value = 'set_access'
  saveAlertMessage.value = ''
  try {
    const permissions = await authApi.getRolePermissions()
    if (permissions && typeof permissions === 'object') {
      rolePermissionsMap.value = permissions
    }
  } catch (err) {
    console.warn('Failed to fetch role permissions:', err)
  }
  handleRoleSelectionChange()
}

function closeRoleSetupModal() {
  showRoleSetupModal.value = false
  saveAlertMessage.value = ''
}

function togglePermGroup(groupKey) {
  if (isPermGroupOpen.value[groupKey] !== undefined) {
    isPermGroupOpen.value[groupKey] = !isPermGroupOpen.value[groupKey]
  }
}

const groupMenuKeysMap = {
  employee: ['employee_list', 'add_employee'],
  core: ['drivers', 'passengers', 'admins'],
  ops: ['topups', 'bookings', 'doc_bookings', 'stats'],
  accounting: ['accounting'],
  attendance: ['attendance_timesheet', 'attendance_timelog', 'attendance_overtime', 'attendance_leave', 'attendance_holiday', 'attendance_photo_verification', 'attendance_approver'],
  payroll: ['payroll_schedule', 'payroll_salary', 'payroll_leave', 'payroll_generate', 'payroll_advances', 'payroll_contributions', 'payroll_bonus_deduction', 'payroll_ot_nd', 'payroll_approver'],
  support: ['support_chat'],
  setup: ['create_department', 'create_position', 'set_access'],
  overview: ['overview']
}

function isGroupAllEnabled(groupKey) {
  const keys = groupMenuKeysMap[groupKey] || []
  return keys.length > 0 && keys.every(k => !!menuSwitches.value[k])
}

function isGroupAnyEnabled(groupKey) {
  const keys = groupMenuKeysMap[groupKey] || []
  return keys.some(k => !!menuSwitches.value[k])
}

function toggleGroupMaster(groupKey, forceVal = null) {
  const keys = groupMenuKeysMap[groupKey] || []
  const enable = forceVal !== null ? forceVal : !isGroupAnyEnabled(groupKey)
  keys.forEach(k => {
    menuSwitches.value[k] = enable
  })
}

async function saveRolePermissions() {
  isSavingPermissions.value = true
  saveAlertMessage.value = ''
  try {
    const roleKey = (selectedRoleToConfigure.value || '').toLowerCase().replace(/\s+/g, '_')
    const payload = {
      role: roleKey,
      menu_access: { ...menuSwitches.value }
    }
    const res = await authApi.saveRolePermission(payload)
    
    // Update local permissions state immediately and sync to localStorage
    rolePermissionsMap.value[roleKey] = { ...menuSwitches.value }
    localStorage.setItem('cael_role_permissions', JSON.stringify(rolePermissionsMap.value))
    
    // Show animated checkmark modal popup instead of bottom alert text!
    const roleLabel = getRoleLabel(selectedRoleToConfigure.value)
    accessSavedSuccessDetails.value = {
      roleLabel: roleLabel,
      message: res?.message || `Permissions updated successfully for role '${roleLabel}'`
    }
    showAccessSavedSuccessModal.value = true
    saveAlertMessage.value = ''
  } catch (err) {
    saveAlertStatus.value = 'error'
    saveAlertMessage.value = err.message || 'Failed to save permissions'
  } finally {
    isSavingPermissions.value = false
  }
}

function canAccessMenu(menuKey) {
  const activeUser = user.value
  const rawRole = activeUser?.role || activeUser?.account_role || activeUser?.position || ''
  const userRole = rawRole.toLowerCase().replace(/\s+/g, '_')
  
  if (userRole === 'super_admin' || userRole === 'superadmin') {
    const roleConfig = rolePermissionsMap.value[userRole] || rolePermissionsMap.value[rawRole.toLowerCase()]
    if (roleConfig && typeof roleConfig === 'object' && roleConfig[menuKey] !== undefined) {
      return !!roleConfig[menuKey]
    }
    return true // Super Administrator default has full access
  }
  
  const roleConfig = rolePermissionsMap.value[userRole] || rolePermissionsMap.value[rawRole.toLowerCase()]
  if (roleConfig && typeof roleConfig === 'object') {
    if (menuKey === 'dashboard' && roleConfig.overview !== undefined) return !!roleConfig.overview
    if (roleConfig[menuKey] !== undefined) {
      return !!roleConfig[menuKey]
    }
  }
  return true
}

function canAccessMenuGroup(menuKeys) {
  return menuKeys.some(key => canAccessMenu(key))
}

async function fetchRolePermissionsData() {
  try {
    const perms = await authApi.getRolePermissions()
    if (perms) rolePermissionsMap.value = perms
  } catch (e) {
    console.error("Failed to load role permissions:", e)
  }
}




const viewMetas = {
  dashboard: { title: 'Dashboard', icon: '📊' },
  employee_list: { title: 'Employee List', icon: '👥' },
  add_employee: { title: 'Add Employee', icon: '👤➕' },
  drivers: { title: 'Driver Accounts', icon: '🏍️' },
  passengers: { title: 'Passenger Accounts', icon: '👤' },
  admins: { title: 'Admin Accounts', icon: '💻' },
  topups: { title: 'Top-Up Verification', icon: '💳' },
  bookings: { title: 'Booking History', icon: '🚗' },
  doc_bookings: { title: 'Document History', icon: '📄' },
  stats: { title: 'Financial Analytics', icon: '📈' },
  accounting: { title: 'Financial Management System', icon: '💼' },
  attendance_timesheet: { title: 'Time Sheet', icon: '📋' },
  attendance_timelog: { title: 'Time Log', icon: '⏱️' },
  attendance_overtime: { title: 'Overtime', icon: '⏰' },
  attendance_leave: { title: 'Leave', icon: '🏖️' },
  attendance_holiday: { title: 'Calendar', icon: '📅' },
  payroll_schedule: { title: 'Working Schedule', icon: '📅' },
  payroll_salary: { title: 'Salary', icon: '💰' },
  payroll_leave: { title: 'Leave', icon: '🏖️' },
  payroll_generate: { title: 'Generate Payroll', icon: '⚡' },
  payroll_advances: { title: 'Cash Advances', icon: '💸' },
  payroll_contributions: { title: 'Contributions', icon: '🏛️' },
  payroll_bonus_deduction: { title: 'Bonus / Deduction', icon: '🎁' },
  payroll_ot_nd: { title: 'OT & ND Rates', icon: '🌙' },
  support_chat: { title: 'Chat Support', icon: '💬' },
  create_department: { title: 'Create Department', icon: '🏢' },
  create_position: { title: 'Create Position', icon: '📌' },
  set_access: { title: 'Set Access', icon: '🔐' },
  user_profile: { title: 'User Profile', icon: '👤' }
}

const currentViewMeta = computed(() => viewMetas[activeView.value] || { title: 'Dashboard', icon: '⚙️' })

function handleGlobalClick(e) {
  if (profileDropdownRef.value && !profileDropdownRef.value.contains(e.target)) {
    isProfileDropdownOpen.value = false
  }
}

function navigateToProfile() {
  activeView.value = 'user_profile'
  isProfileDropdownOpen.value = false
}

// SORTING STATE
const sortField = ref('created_at')
const sortDir = ref('desc')

function toggleSort(field) {
  if (sortField.value === field) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDir.value = 'asc'
  }
}

function getSortIcon(field) {
  if (sortField.value !== field) return '↕'
  return sortDir.value === 'asc' ? '▲' : '▼'
}

// SEARCH STATES
const employeeSearch = ref('')
const driverSearch = ref('')
const passengerSearch = ref('')
const adminSearch = ref('')
const topUpSearch = ref('')

// DATA STATES
const loading = ref(false)
const error = ref('')
const successMsg = ref('')
const balanceLogs = ref([])
const bookings = ref([])

// ADD EMPLOYEE FORM STATE
const isAddingEmployee = ref(false)
const employeeError = ref('')
const employeeSuccess = ref('')
const employeeForm = ref({
  username: '',
  password: '',
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

function resetEmployeeForm() {
  employeeForm.value = {
    username: '',
    password: '',
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
  }
  employeeError.value = ''
  employeeSuccess.value = ''
}

// ── MODULE APPROVERS PERMISSIONS STATE & LOGIC ───────────────────
const selectedApproverTargetEmpId = ref('')
const selectedApproverModuleType = ref('cash_advances')
const approverSuccessMessage = ref('')
const approverErrorMessage = ref('')

const defaultModuleApprovers = {
  cash_advances: ['superadmin', 'admin', '1'],
  timelog: ['superadmin', 'admin', '1'],
  overtime: ['superadmin', 'admin', '1'],
  leave: ['superadmin', 'admin', '1']
}

const moduleApprovers = ref({ ...defaultModuleApprovers })

function loadModuleApproversFromStorage() {
  try {
    const saved = localStorage.getItem('cael_module_approvers')
    if (saved) {
      const parsed = JSON.parse(saved)
      moduleApprovers.value = {
        cash_advances: parsed.cash_advances || [...defaultModuleApprovers.cash_advances],
        timelog: parsed.timelog || [...defaultModuleApprovers.timelog],
        overtime: parsed.overtime || [...defaultModuleApprovers.overtime],
        leave: parsed.leave || [...defaultModuleApprovers.leave]
      }
    } else {
      moduleApprovers.value = { ...defaultModuleApprovers }
      saveModuleApproversToStorage()
    }
  } catch (e) {
    moduleApprovers.value = { ...defaultModuleApprovers }
  }
}

function saveModuleApproversToStorage() {
  try {
    localStorage.setItem('cael_module_approvers', JSON.stringify(moduleApprovers.value))
  } catch (e) {}
}

function canApproveModule(moduleKey) {
  if (['timelog', 'overtime', 'leave', 'holiday', 'attendance_timesheet', 'attendance_timelog', 'attendance_overtime', 'attendance_leave', 'attendance_holiday'].includes(moduleKey)) {
    return canAccessMenu('attendance_approver')
  }
  if (['cash_advances', 'payroll_generate', 'schedule', 'salary', 'contributions', 'payroll_schedule', 'payroll_salary', 'payroll_leave', 'payroll_advances', 'payroll_contributions', 'payroll_bonus_deduction'].includes(moduleKey)) {
    return canAccessMenu('payroll_approver')
  }

  const currentUser = user.value
  if (!currentUser) return true

  const rawRole = (currentUser.role || currentUser.account_role || currentUser.position || '').toLowerCase().replace(/\s+/g, '_')
  const username = (currentUser.username || '').toLowerCase()
  const userId = String(currentUser.id || '')

  if (rawRole === 'super_admin' || rawRole === 'superadmin' || rawRole === 'admin') {
    return true
  }

  const allowedList = moduleApprovers.value[moduleKey] || []
  return allowedList.some(identifier => {
    const idStr = String(identifier).toLowerCase()
    return idStr === username || idStr === userId || idStr === rawRole
  })
}

function getApproverDisplayName(id) {
  const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(id) || String(u.username) === String(id)) ||
              users.value.find(u => String(u.id) === String(id) || String(u.username) === String(id))
  return emp ? (emp.full_name || emp.username) : id
}

function assignModuleApprover() {
  approverSuccessMessage.value = ''
  approverErrorMessage.value = ''

  if (!selectedApproverTargetEmpId.value) {
    approverErrorMessage.value = 'Please select an employee/account first.'
    return
  }

  const targetEmp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(selectedApproverTargetEmpId.value)) ||
                    users.value.find(u => String(u.id) === String(selectedApproverTargetEmpId.value))

  if (!targetEmp) {
    approverErrorMessage.value = 'Selected employee record not found.'
    return
  }

  const empIdentifier = String(targetEmp.id || targetEmp.username || targetEmp.email)
  const empName = targetEmp.full_name || targetEmp.username || 'Employee'
  const moduleKey = selectedApproverModuleType.value

  if (!moduleApprovers.value[moduleKey]) {
    moduleApprovers.value[moduleKey] = []
  }

  const currentList = moduleApprovers.value[moduleKey]
  if (currentList.includes(empIdentifier) || (targetEmp.username && currentList.includes(targetEmp.username))) {
    approverErrorMessage.value = `${empName} is already assigned as an approver for this module.`
    return
  }

  moduleApprovers.value[moduleKey].push(empIdentifier)
  saveModuleApproversToStorage()

  const moduleLabels = {
    cash_advances: 'Cash Advances',
    timelog: 'Time Log',
    overtime: 'Overtime',
    leave: 'Leave'
  }

  approverSuccessMessage.value = `Successfully assigned ${empName} as ${moduleLabels[moduleKey]} Approver!`
  selectedApproverTargetEmpId.value = ''
}

function revokeModuleApprover(moduleKey, identifier) {
  approverSuccessMessage.value = ''
  approverErrorMessage.value = ''

  if (!moduleApprovers.value[moduleKey]) return

  moduleApprovers.value[moduleKey] = moduleApprovers.value[moduleKey].filter(id => String(id) !== String(identifier))
  saveModuleApproversToStorage()

  const moduleLabels = {
    cash_advances: 'Cash Advances',
    timelog: 'Time Log',
    overtime: 'Overtime',
    leave: 'Leave'
  }

  approverSuccessMessage.value = `Revoked approver permission for ${moduleLabels[moduleKey]}.`
}

// ── CASH ADVANCES MODULE COMPUTED & STATE LOGIC ───────────────────
const cashAdvanceStatusFilter = ref('all') // 'all' | 'Pending' | 'Approved' | 'Denied'
const selectedAdvanceEmployeeId = ref('current_user')
const selectedCreatedByName = ref('current_user')
const cashAdvanceSuccess = ref('')
const cashAdvanceError = ref('')

const cashAdvanceForm = ref({
  amount: 2500,
  reason: 'Emergency Medical & Personal Expense'
})

const defaultCashAdvancesSeed = [
  {
    id: 'ADV-1003',
    employee_id: '1',
    employee_name: 'Super Administrator',
    created_by: 'Super Administrator',
    username: 'superadmin',
    amount: 2500,
    reason: 'Emergency Medical & Personal Expense',
    timestamp: '2026-10-03 09:15 AM',
    status: 'Pending',
    approved_by: null,
    approved_at: null
  },
  {
    id: 'ADV-1002',
    employee_id: '2',
    employee_name: 'Juan Dela Cruz',
    created_by: 'Juan Dela Cruz',
    username: 'jdelacruz',
    amount: 5000,
    reason: 'Vehicle Maintenance & Parts Replacement',
    timestamp: '2026-09-28 02:30 PM',
    status: 'Approved',
    approved_by: 'Super Administrator',
    approved_at: '2026-09-28 04:00 PM'
  },
  {
    id: 'ADV-1001',
    employee_id: '3',
    employee_name: 'Maria Santos',
    created_by: 'Maria Santos',
    username: 'msantos',
    amount: 1500,
    reason: 'Utility Bill Payment',
    timestamp: '2026-09-20 11:00 AM',
    status: 'Denied',
    approved_by: 'Super Administrator',
    approved_at: '2026-09-20 01:15 PM'
  }
]

const cashAdvancesLogs = ref([])

function loadCashAdvancesFromStorage() {
  try {
    const saved = localStorage.getItem('cael_cash_advances_logs')
    if (saved) {
      cashAdvancesLogs.value = JSON.parse(saved)
    } else {
      cashAdvancesLogs.value = [...defaultCashAdvancesSeed]
      saveCashAdvancesToStorage()
    }
  } catch (e) {
    cashAdvancesLogs.value = [...defaultCashAdvancesSeed]
  }
}

function saveCashAdvancesToStorage() {
  try {
    localStorage.setItem('cael_cash_advances_logs', JSON.stringify(cashAdvancesLogs.value))
  } catch (e) {}
}

function submitCashAdvanceRequest() {
  cashAdvanceSuccess.value = ''
  cashAdvanceError.value = ''
  
  const amt = parseFloat(cashAdvanceForm.value.amount)
  if (isNaN(amt) || amt <= 0) {
    cashAdvanceError.value = 'Please enter a valid advance amount greater than 0.'
    return
  }

  let empName = userCurrentName.value || 'Super Administrator'
  let empId = user.value?.id || '1'
  let uName = user.value?.username || 'user'

  if (selectedAdvanceEmployeeId.value !== 'current_user') {
    const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(selectedAdvanceEmployeeId.value))
    if (emp) {
      empName = emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username)
      empId = String(emp.id)
      uName = emp.username || 'user'
    }
  }

  const createdByName = userCurrentName.value || 'Super Administrator'

  const newId = `ADV-${Math.floor(1000 + Math.random() * 9000)}`
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' })
  const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
  const timestamp = `${dateStr} ${timeStr}`

  const newRecord = {
    id: newId,
    employee_id: String(empId),
    employee_name: empName,
    created_by: createdByName,
    username: uName,
    amount: amt,
    reason: (cashAdvanceForm.value.reason || '').trim() || 'Cash Advance Request',
    timestamp,
    status: 'Pending',
    approved_by: null,
    approved_at: null
  }

  cashAdvancesLogs.value.unshift(newRecord)
  saveCashAdvancesToStorage()

  cashAdvanceSuccess.value = `Cash advance request of ₱${amt.toLocaleString('en-US', { minimumFractionDigits: 2 })} submitted successfully for ${empName} (${newId})!`
  cashAdvanceForm.value.amount = 2500
  cashAdvanceForm.value.reason = ''
}

function approveCashAdvance(item) {
  item.status = 'Approved'
  item.approved_by = userCurrentName.value || 'Super Administrator'
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' })
  const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
  item.approved_at = `${dateStr} ${timeStr}`
  saveCashAdvancesToStorage()
  cashAdvanceSuccess.value = `Cash advance request ${item.id} (₱${item.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}) APPROVED for ${item.employee_name}.`
}

function denyCashAdvance(item) {
  item.status = 'Denied'
  item.approved_by = userCurrentName.value || 'Super Administrator'
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' })
  const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
  item.approved_at = `${dateStr} ${timeStr}`
  saveCashAdvancesToStorage()
  cashAdvanceError.value = `Cash advance request ${item.id} (₱${item.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}) DENIED for ${item.employee_name}.`
}

const filteredCashAdvancesLogs = computed(() => {
  let logs = cashAdvancesLogs.value
  if (cashAdvanceStatusFilter.value !== 'all') {
    logs = logs.filter(l => l.status === cashAdvanceStatusFilter.value)
  }
  return logs
})

const cashAdvanceSummary = computed(() => {
  const all = cashAdvancesLogs.value
  const pending = all.filter(l => l.status === 'Pending')
  const approved = all.filter(l => l.status === 'Approved')
  const denied = all.filter(l => l.status === 'Denied')

  const totalPendingAmount = pending.reduce((sum, l) => sum + (parseFloat(l.amount) || 0), 0)
  const totalApprovedAmount = approved.reduce((sum, l) => sum + (parseFloat(l.amount) || 0), 0)

  return {
    totalCount: all.length,
    pendingCount: pending.length,
    pendingAmount: totalPendingAmount,
    approvedCount: approved.length,
    approvedAmount: totalApprovedAmount,
    deniedCount: denied.length
  }
})

// ── PAYROLL CONTRIBUTIONS MODULE LOGIC ───────────────────
const isContribCard1Open = ref(true)
const isContribCard2Open = ref(true)
const isContribCard3Open = ref(true)

const selectedContribEmployeeId = ref('current_user')
const customBaseSalary = ref(35000)

const contribSuccessMessage = ref('')
const contribErrorMessage = ref('')

const editingContribId = ref(null)
const contributionForm = ref({
  name: 'SSS Contribution',
  calc_type: 'msc_table',
  rate: 4.5,
  split_half: true,
  is_active: true,
  msc_emp_pct: 5.0,
  msc_er_pct: 10.0,
  msc_ec_amount: 30.0,
  msc_brackets: []
})

const newBracketInput = ref({
  min_sal: 0,
  max_sal: 4999.99,
  msc: 5000,
  emp_pct: 5.0,
  er_pct: 10.0,
  ec: 10
})

const defaultMscBracketsSeed = [
  { min_sal: 0, max_sal: 4999.99, msc: 5000, emp_pct: 5.0, er_pct: 10.0, ec: 10 },
  { min_sal: 5000, max_sal: 9999.99, msc: 10000, emp_pct: 5.0, er_pct: 10.0, ec: 10 },
  { min_sal: 10000, max_sal: 14999.99, msc: 15000, emp_pct: 5.0, er_pct: 10.0, ec: 15 },
  { min_sal: 15000, max_sal: 19999.99, msc: 20000, emp_pct: 5.0, er_pct: 10.0, ec: 20 },
  { min_sal: 20000, max_sal: 24999.99, msc: 25000, emp_pct: 5.0, er_pct: 10.0, ec: 25 },
  { min_sal: 25000, max_sal: 29999.99, msc: 30000, emp_pct: 5.0, er_pct: 10.0, ec: 30 },
  { min_sal: 30000, max_sal: 999999.00, msc: 35000, emp_pct: 5.0, er_pct: 10.0, ec: 30 }
]

// Initialize default form brackets with seed
contributionForm.value.msc_brackets = defaultMscBracketsSeed.map(b => ({ ...b }))

function addMscBracketRow() {
  if (newBracketInput.value.min_sal === null || newBracketInput.value.min_sal === undefined ||
      newBracketInput.value.max_sal === null || newBracketInput.value.max_sal === undefined ||
      !newBracketInput.value.msc) {
    contribErrorMessage.value = 'Please provide valid Range From, Range To, and MSC values.'
    return
  }
  if (!contributionForm.value.msc_brackets) {
    contributionForm.value.msc_brackets = []
  }

  const minVal = parseFloat(newBracketInput.value.min_sal) || 0
  const maxVal = parseFloat(newBracketInput.value.max_sal) || 0
  const mscVal = parseFloat(newBracketInput.value.msc) || 0
  const empPctVal = newBracketInput.value.emp_pct !== undefined ? parseFloat(newBracketInput.value.emp_pct) : 5.0
  const erPctVal = newBracketInput.value.er_pct !== undefined ? parseFloat(newBracketInput.value.er_pct) : 10.0
  const ecVal = parseFloat(newBracketInput.value.ec) || 0

  contributionForm.value.msc_brackets.push({
    min_sal: minVal,
    max_sal: maxVal,
    msc: mscVal,
    emp_pct: empPctVal,
    er_pct: erPctVal,
    ec: ecVal
  })

  contributionForm.value.msc_brackets.sort((a, b) => a.min_sal - b.min_sal)

  const nextMin = parseFloat((maxVal + 0.01).toFixed(2))
  const nextMax = parseFloat((nextMin + 4999.99).toFixed(2))
  const nextMsc = Math.round(nextMin + 5000)

  newBracketInput.value = {
    min_sal: nextMin,
    max_sal: nextMax,
    msc: nextMsc,
    emp_pct: 5.0,
    er_pct: 10.0,
    ec: 10
  }
  contribErrorMessage.value = ''
  contribSuccessMessage.value = 'Added compensation bracket row!'
}

const editingMscBracketIndex = ref(null)
const editingMscBracketForm = ref({
  min_sal: 0,
  max_sal: 0,
  msc: 0,
  emp_pct: 5.0,
  er_pct: 10.0,
  ec: 10
})

function startEditingMscBracketRow(index, b) {
  editingMscBracketIndex.value = index
  editingMscBracketForm.value = {
    min_sal: b.min_sal,
    max_sal: b.max_sal,
    msc: b.msc,
    emp_pct: b.emp_pct ?? 5.0,
    er_pct: b.er_pct ?? 10.0,
    ec: b.ec ?? 10
  }
}

function cancelEditingMscBracketRow() {
  editingMscBracketIndex.value = null
}

function saveEditingMscBracketRow(index) {
  if (editingMscBracketIndex.value === null) return
  const list = contributionForm.value.msc_brackets
  if (list && index >= 0 && index < list.length) {
    list[index] = {
      min_sal: parseFloat(editingMscBracketForm.value.min_sal) || 0,
      max_sal: parseFloat(editingMscBracketForm.value.max_sal) || 0,
      msc: parseFloat(editingMscBracketForm.value.msc) || 0,
      emp_pct: editingMscBracketForm.value.emp_pct !== undefined ? parseFloat(editingMscBracketForm.value.emp_pct) : 5.0,
      er_pct: editingMscBracketForm.value.er_pct !== undefined ? parseFloat(editingMscBracketForm.value.er_pct) : 10.0,
      ec: parseFloat(editingMscBracketForm.value.ec) || 0
    }
    list.sort((a, b) => a.min_sal - b.min_sal)
    contribSuccessMessage.value = 'Updated bracket row successfully!'
  }
  editingMscBracketIndex.value = null
}

function removeMscBracketRow(index) {
  if (editingMscBracketIndex.value === index) {
    editingMscBracketIndex.value = null
  }
  if (contributionForm.value.msc_brackets && index >= 0 && index < contributionForm.value.msc_brackets.length) {
    contributionForm.value.msc_brackets.splice(index, 1)
  }
}

function loadDefaultSeedBrackets() {
  editingMscBracketIndex.value = null
  contributionForm.value.msc_brackets = defaultMscBracketsSeed.map(b => ({ ...b }))
  contribSuccessMessage.value = 'Loaded standard MSC bracket template!'
}

function clearAllMscBrackets() {
  editingMscBracketIndex.value = null
  contributionForm.value.msc_brackets = []
  contribSuccessMessage.value = 'Cleared all bracket entries.'
}

const defaultContributionRulesSeed = [
  {
    id: 'CONTRIB-101',
    name: 'SSS Contribution Schedule',
    calc_type: 'msc_table',
    msc_emp_pct: 5.0,
    msc_er_pct: 10.0,
    msc_ec_amount: 30.0,
    msc_brackets: defaultMscBracketsSeed.map(b => ({ ...b })),
    rate: 15.0,
    split_half: false,
    is_active: true,
    created_at: '2026-10-03'
  },
  {
    id: 'CONTRIB-102',
    name: 'PhilHealth Insurance',
    calc_type: 'percentage',
    msc_emp_pct: 5.0,
    msc_er_pct: 10.0,
    msc_ec_amount: 30.0,
    msc_brackets: [],
    rate: 2.5,
    split_half: true,
    is_active: true,
    created_at: '2026-10-03'
  },
  {
    id: 'CONTRIB-103',
    name: 'Pag-IBIG HDMF',
    calc_type: 'percentage',
    msc_emp_pct: 5.0,
    msc_er_pct: 10.0,
    msc_ec_amount: 30.0,
    msc_brackets: [],
    rate: 2.0,
    split_half: true,
    is_active: true,
    created_at: '2026-10-03'
  },
  {
    id: 'CONTRIB-104',
    name: 'BIR Withholding Tax',
    calc_type: 'percentage',
    msc_emp_pct: 5.0,
    msc_er_pct: 10.0,
    msc_ec_amount: 30.0,
    msc_brackets: [],
    rate: 5.0,
    split_half: false,
    is_active: true,
    created_at: '2026-10-03'
  }
]

const contributionRules = ref([])

function loadContributionRulesFromStorage() {
  try {
    const saved = localStorage.getItem('cael_payroll_contribution_rules')
    if (saved) {
      contributionRules.value = JSON.parse(saved)
    } else {
      contributionRules.value = [...defaultContributionRulesSeed]
      saveContributionRulesToStorage()
    }
  } catch (e) {
    contributionRules.value = [...defaultContributionRulesSeed]
  }
}

function saveContributionRulesToStorage() {
  try {
    localStorage.setItem('cael_payroll_contribution_rules', JSON.stringify(contributionRules.value))
  } catch (e) {}
}

watch(selectedContribEmployeeId, (newId) => {
  if (newId === 'current_user') {
    const userSal = assignedSalaries.value.find(s => s.employee_name === userCurrentName.value)
    if (userSal && userSal.salary_amount) customBaseSalary.value = userSal.salary_amount
    else customBaseSalary.value = 35000
  } else {
    const emp = assignedSalaries.value.find(s => String(s.employee_id) === String(newId) || String(s.id) === String(newId))
    if (emp && emp.salary_amount) customBaseSalary.value = emp.salary_amount
    else customBaseSalary.value = 35000
  }
}, { immediate: true })

function applyContributionRule() {
  contribSuccessMessage.value = ''
  contribErrorMessage.value = ''

  if (!contributionForm.value.name || !contributionForm.value.name.trim()) {
    contribErrorMessage.value = 'Please provide a valid contribution name.'
    return
  }

  const rateNum = parseFloat(contributionForm.value.rate) || 0
  const mscEmpPct = parseFloat(contributionForm.value.msc_emp_pct) || 5.0
  const mscErPct = parseFloat(contributionForm.value.msc_er_pct) || 10.0
  const mscEcAmt = parseFloat(contributionForm.value.msc_ec_amount) || 0

  if (editingContribId.value) {
    const index = contributionRules.value.findIndex(r => String(r.id) === String(editingContribId.value))
    if (index !== -1) {
      const updatedRule = {
        ...contributionRules.value[index],
        name: contributionForm.value.name.trim(),
        calc_type: contributionForm.value.calc_type || 'percentage',
        rate: rateNum,
        split_half: !!contributionForm.value.split_half,
        msc_emp_pct: mscEmpPct,
        msc_er_pct: mscErPct,
        msc_ec_amount: mscEcAmt,
        msc_brackets: contributionForm.value.msc_brackets ? [...contributionForm.value.msc_brackets] : []
      }
      contributionRules.value.splice(index, 1, updatedRule)
      contributionRules.value = [...contributionRules.value]
      contribSuccessMessage.value = `Updated contribution rule "${updatedRule.name}" successfully!`
    }
    editingContribId.value = null
  } else {
    const newId = `CONTRIB-${Math.floor(100 + Math.random() * 900)}`
    const newRule = {
      id: newId,
      name: contributionForm.value.name.trim(),
      calc_type: contributionForm.value.calc_type || 'percentage',
      rate: rateNum,
      split_half: !!contributionForm.value.split_half,
      msc_emp_pct: mscEmpPct,
      msc_er_pct: mscErPct,
      msc_ec_amount: mscEcAmt,
      msc_brackets: contributionForm.value.msc_brackets ? [...contributionForm.value.msc_brackets] : [],
      is_active: true,
      created_at: new Date().toISOString().split('T')[0]
    }
    contributionRules.value.unshift(newRule)
    contributionRules.value = [...contributionRules.value]
    contribSuccessMessage.value = `Created contribution rule "${newRule.name}" successfully!`
  }

  saveContributionRulesToStorage()
  resetContributionForm()
}

function resetContributionForm() {
  editingContribId.value = null
  contributionForm.value = {
    name: '',
    calc_type: 'percentage',
    rate: 4.5,
    split_half: true,
    is_active: true,
    msc_emp_pct: 5.0,
    msc_er_pct: 10.0,
    msc_ec_amount: 30.0,
    msc_brackets: []
  }
}

function editContributionRule(rule) {
  contribSuccessMessage.value = ''
  contribErrorMessage.value = ''
  editingContribId.value = rule.id
  contributionForm.value = {
    name: rule.name,
    calc_type: rule.calc_type || 'percentage',
    rate: rule.rate || 4.5,
    split_half: rule.split_half !== false,
    is_active: rule.is_active !== false,
    msc_emp_pct: rule.msc_emp_pct ?? 5.0,
    msc_er_pct: rule.msc_er_pct ?? 10.0,
    msc_ec_amount: rule.msc_ec_amount ?? 30.0,
    msc_brackets: (rule.msc_brackets && rule.msc_brackets.length > 0) ? JSON.parse(JSON.stringify(rule.msc_brackets)) : defaultMscBracketsSeed.map(b => ({ ...b }))
  }
  isContribCard1Open.value = true
  
  // Smooth scroll up to Card 1 form
  setTimeout(() => {
    const card1El = document.getElementById('contrib-card-1')
    if (card1El) {
      card1El.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 50)
}

function toggleContributionRule(rule) {
  rule.is_active = !rule.is_active
  saveContributionRulesToStorage()
  contribSuccessMessage.value = `Contribution rule "${rule.name}" is now ${rule.is_active ? 'Active' : 'Inactive'}.`
}

function deleteContributionRule(ruleId) {
  const rule = contributionRules.value.find(r => r.id === ruleId)
  const name = rule ? rule.name : ruleId
  contributionRules.value = contributionRules.value.filter(r => r.id !== ruleId)
  saveContributionRulesToStorage()
  contribSuccessMessage.value = `Deleted contribution rule "${name}".`
}

function getRuleMatchedBracket(rule, salary = customBaseSalary.value) {
  const sal = parseFloat(salary) || 0
  const brackets = (rule.msc_brackets && rule.msc_brackets.length > 0) ? rule.msc_brackets : defaultMscBracketsSeed
  const matched = brackets.find(b => sal >= b.min_sal && sal <= b.max_sal) || brackets[brackets.length - 1]
  return matched || { min_sal: 0, max_sal: 0, msc: 0, emp_pct: 5.0, er_pct: 10.0, ec: 0 }
}

function getRuleEstimatedEmployeeDeduction(rule) {
  const sal = parseFloat(customBaseSalary.value) || 0
  if (rule.calc_type === 'msc_table') {
    const b = getRuleMatchedBracket(rule, sal)
    const empPct = b.emp_pct ?? rule.msc_emp_pct ?? 5.0
    return (b.msc * empPct) / 100
  } else {
    const rate = rule.split_half ? (rule.rate / 2) : rule.rate
    return (sal * rate) / 100
  }
}

const activeContributionRules = computed(() => contributionRules.value.filter(r => r.is_active))

const calculatedContributionsBreakdown = computed(() => {
  const baseSal = parseFloat(customBaseSalary.value) || 0
  return activeContributionRules.value.map(rule => {
    if (rule.calc_type === 'msc_table') {
      const brackets = (rule.msc_brackets && rule.msc_brackets.length > 0) ? rule.msc_brackets : defaultMscBracketsSeed
      const matchedBracket = brackets.find(b => baseSal >= b.min_sal && baseSal <= b.max_sal) || brackets[brackets.length - 1]
      const msc = matchedBracket ? matchedBracket.msc : 0
      const empPct = matchedBracket ? (matchedBracket.emp_pct ?? rule.msc_emp_pct ?? 5.0) : 5.0
      const erPct = matchedBracket ? (matchedBracket.er_pct ?? rule.msc_er_pct ?? 10.0) : 10.0
      const ecAmt = matchedBracket ? (matchedBracket.ec ?? rule.msc_ec_amount ?? 0) : 0

      const empAmt = (msc * empPct) / 100
      const erAmt = (msc * erPct) / 100 + ecAmt
      const totalAmt = empAmt + erAmt

      return {
        id: rule.id,
        name: rule.name,
        calc_type: 'msc_table',
        total_rate: empPct + erPct,
        msc_amount: msc,
        matched_bracket: matchedBracket || { min_sal: 0, max_sal: 0, msc: 0 },
        full_result_amount: totalAmt,
        split_half: false,
        emp_rate: empPct,
        emp_amount: empAmt,
        er_rate: erPct,
        er_amount: erAmt,
        ec_amount: ecAmt,
        total_amount: totalAmt
      }
    } else {
      const fullResultAmt = (baseSal * rule.rate) / 100
      let empAmt = fullResultAmt
      let erAmt = 0
      let empRate = rule.rate
      let erRate = 0

      if (rule.split_half) {
        empAmt = fullResultAmt / 2
        erAmt = fullResultAmt / 2
        empRate = rule.rate / 2
        erRate = rule.rate / 2
      }

      return {
        id: rule.id,
        name: rule.name,
        calc_type: 'percentage',
        total_rate: rule.rate,
        msc_amount: baseSal,
        full_result_amount: fullResultAmt,
        split_half: rule.split_half,
        emp_rate: empRate,
        emp_amount: empAmt,
        er_rate: erRate,
        er_amount: erAmt,
        ec_amount: 0,
        total_amount: fullResultAmt
      }
    }
  })
})

const totalEmployeeDeductions = computed(() => {
  return calculatedContributionsBreakdown.value.reduce((sum, item) => sum + item.emp_amount, 0)
})

const totalEmployerContributions = computed(() => {
  return calculatedContributionsBreakdown.value.reduce((sum, item) => sum + item.er_amount, 0)
})

const netTakeHomeSalary = computed(() => {
  const baseSal = parseFloat(customBaseSalary.value) || 0
  return Math.max(0, baseSal - totalEmployeeDeductions.value)
})

const totalEmployeeDeductionsPct = computed(() => {
  const baseSal = parseFloat(customBaseSalary.value) || 0
  if (baseSal <= 0) return '0.00'
  return ((totalEmployeeDeductions.value / baseSal) * 100).toFixed(2)
})

const totalEmployerContributionsPct = computed(() => {
  const baseSal = parseFloat(customBaseSalary.value) || 0
  if (baseSal <= 0) return '0.00'
  return ((totalEmployerContributions.value / baseSal) * 100).toFixed(2)
})

// ── PAYROLL BONUS & DEDUCTION MODULE LOGIC ───────────────────
const bonusDeductionTypeFilter = ref('all') // 'all' | 'bonus' | 'deduction'
const bonusDeductionEmployeeFilter = ref('all')
const bonusDeductionPeriodFilter = ref('all')
const bonusDeductionSuccess = ref('')
const bonusDeductionError = ref('')

const bonusDeductionForm = ref({
  type: 'bonus',
  employee_id: '1',
  name: '',
  amount: 1000,
  period_key: 'sep_2',
  notes: ''
})

const defaultBonusDeductionsSeed = [
  {
    id: 'BD-1001',
    type: 'bonus',
    employee_id: '1',
    employee_name: 'Juan Dela Cruz',
    username: 'juan_dc',
    name: 'Quarterly Performance Bonus',
    amount: 2500,
    period_key: 'sep_2',
    notes: 'Exceeded KPI targets for Q3',
    is_active: true,
    created_at: '2026-09-02',
    created_by: 'Super Administrator'
  },
  {
    id: 'BD-1002',
    type: 'deduction',
    employee_id: '1',
    employee_name: 'Juan Dela Cruz',
    username: 'juan_dc',
    name: 'Uniform Replacement Fee',
    amount: 500,
    period_key: 'sep_2',
    notes: '2 Set Company Polo Shirts',
    is_active: true,
    created_at: '2026-09-05',
    created_by: 'Super Administrator'
  },
  {
    id: 'BD-1003',
    type: 'bonus',
    employee_id: '2',
    employee_name: 'Maria Santos',
    username: 'msantos',
    name: 'Attendance Incentive',
    amount: 1500,
    period_key: 'sep_2',
    notes: 'Perfect attendance for August',
    is_active: true,
    created_at: '2026-09-01',
    created_by: 'Super Administrator'
  }
]

const payrollBonusDeductionList = ref([])

function loadBonusDeductionsFromStorage() {
  try {
    const saved = localStorage.getItem('cael_payroll_bonus_deductions')
    if (saved) {
      payrollBonusDeductionList.value = JSON.parse(saved)
    } else {
      payrollBonusDeductionList.value = [...defaultBonusDeductionsSeed]
      saveBonusDeductionsToStorage()
    }
  } catch (e) {
    payrollBonusDeductionList.value = [...defaultBonusDeductionsSeed]
  }
}

function saveBonusDeductionsToStorage() {
  try {
    localStorage.setItem('cael_payroll_bonus_deductions', JSON.stringify(payrollBonusDeductionList.value))
  } catch (e) {}
}

function getPeriodLabel(key) {
  const p = payrollPeriodOptions.value.find(item => item.key === key)
  return p ? p.label : key
}

const showBonusDeductionModal = ref(false)
const bonusDeductionModalStatus = ref('success') // 'success' | 'error'
const bonusDeductionModalTitle = ref('')
const bonusDeductionModalMessage = ref('')
const bonusDeductionModalDetails = ref(null)

function scrollToBonusDeductionTable() {
  setTimeout(() => {
    const el = document.getElementById('bonus-deduction-records-table')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 100)
}

function submitBonusDeduction() {
  bonusDeductionSuccess.value = ''
  bonusDeductionError.value = ''

  if (!bonusDeductionForm.value.name || !bonusDeductionForm.value.name.trim()) {
    const errText = 'Please provide a valid Bonus / Deduction name.'
    bonusDeductionError.value = errText
    bonusDeductionModalStatus.value = 'error'
    bonusDeductionModalTitle.value = 'Validation Failed'
    bonusDeductionModalMessage.value = errText
    bonusDeductionModalDetails.value = null
    showBonusDeductionModal.value = true
    return
  }

  const amt = parseFloat(bonusDeductionForm.value.amount)
  if (isNaN(amt) || amt <= 0) {
    const errText = 'Please enter a valid monetary amount greater than ₱0.00.'
    bonusDeductionError.value = errText
    bonusDeductionModalStatus.value = 'error'
    bonusDeductionModalTitle.value = 'Invalid Amount'
    bonusDeductionModalMessage.value = errText
    bonusDeductionModalDetails.value = null
    showBonusDeductionModal.value = true
    return
  }

  const emp = availableSalaryEmployeeOptions.value.find(u => String(u.id) === String(bonusDeductionForm.value.employee_id))
  const empName = emp ? (emp.full_name || (emp.first_name ? `${emp.first_name} ${emp.last_name}` : emp.username)) : 'Employee'
  const uName = emp ? (emp.username || 'user') : 'user'

  const periodLabel = getPeriodLabel(bonusDeductionForm.value.period_key)

  const newId = `BD-${Math.floor(1000 + Math.random() * 9000)}`
  const newRecord = {
    id: newId,
    type: bonusDeductionForm.value.type || 'bonus',
    employee_id: String(bonusDeductionForm.value.employee_id),
    employee_name: empName,
    username: uName,
    name: bonusDeductionForm.value.name.trim(),
    amount: amt,
    period_key: bonusDeductionForm.value.period_key,
    notes: (bonusDeductionForm.value.notes || '').trim(),
    is_active: true,
    created_at: new Date().toISOString().split('T')[0],
    created_by: userCurrentName.value || 'Super Administrator'
  }

  payrollBonusDeductionList.value.unshift(newRecord)
  saveBonusDeductionsToStorage()

  const typeText = newRecord.type === 'bonus' ? 'Bonus addition (+)' : 'Deduction (-)'
  const successText = `Added ${typeText} "${newRecord.name}" (₱${amt.toFixed(2)}) for ${empName} under period ${periodLabel}!`
  bonusDeductionSuccess.value = successText

  // Trigger Modal Animated Popup
  bonusDeductionModalStatus.value = 'success'
  bonusDeductionModalTitle.value = newRecord.type === 'bonus' ? '🎁 Bonus Added Successfully!' : '🔻 Deduction Added Successfully!'
  bonusDeductionModalMessage.value = `New ${typeText} record of ₱${amt.toLocaleString('en-US', { minimumFractionDigits: 2 })} created for ${empName} under ${periodLabel}!`
  bonusDeductionModalDetails.value = newRecord
  showBonusDeductionModal.value = true

  bonusDeductionForm.value.name = ''
  bonusDeductionForm.value.notes = ''
}

function toggleBonusDeductionStatus(item) {
  item.is_active = !item.is_active
  saveBonusDeductionsToStorage()
  bonusDeductionSuccess.value = `Record "${item.name}" is now ${item.is_active ? 'Active' : 'Inactive'}.`
}

function deleteBonusDeduction(id) {
  const item = payrollBonusDeductionList.value.find(b => b.id === id)
  const name = item ? item.name : id
  payrollBonusDeductionList.value = payrollBonusDeductionList.value.filter(b => b.id !== id)
  saveBonusDeductionsToStorage()
  bonusDeductionSuccess.value = `Deleted record "${name}".`
}

function getEmployeeBonusDeductionsInPeriod(empIdStr, periodKey) {
  const all = payrollBonusDeductionList.value
  const activeItems = all.filter(b => b.is_active !== false && String(b.employee_id) === String(empIdStr) && b.period_key === periodKey)
  
  const bonuses = activeItems.filter(b => b.type === 'bonus')
  const deductions = activeItems.filter(b => b.type === 'deduction')

  const totalPeriodBonus = bonuses.reduce((sum, b) => sum + (parseFloat(b.amount) || 0), 0)
  const totalPeriodDeduction = deductions.reduce((sum, b) => sum + (parseFloat(b.amount) || 0), 0)

  return {
    bonuses,
    deductions,
    totalPeriodBonus,
    totalPeriodDeduction
  }
}

const filteredBonusDeductionList = computed(() => {
  let list = payrollBonusDeductionList.value
  if (bonusDeductionTypeFilter.value !== 'all') {
    list = list.filter(b => b.type === bonusDeductionTypeFilter.value)
  }
  if (bonusDeductionEmployeeFilter.value !== 'all') {
    list = list.filter(b => String(b.employee_id) === String(bonusDeductionEmployeeFilter.value))
  }
  if (bonusDeductionPeriodFilter.value !== 'all') {
    list = list.filter(b => b.period_key === bonusDeductionPeriodFilter.value)
  }
  return list
})

watch(activeView, (newVal) => {
  if (newVal === 'add_employee') {
    resetEmployeeForm()
  }
  if (newVal === 'attendance_timesheet') {
    loadAttendanceFromStorage()
  }
  if (newVal === 'payroll_advances') {
    loadCashAdvancesFromStorage()
  }
  if (newVal === 'payroll_contributions') {
    loadContributionRulesFromStorage()
  }
  if (newVal === 'payroll_bonus_deduction') {
    loadBonusDeductionsFromStorage()
  }
  if (newVal && newVal.startsWith('attendance_')) {
    isAttendanceSubmenuOpen.value = true
  }
  if (newVal && newVal.startsWith('payroll_')) {
    isPayrollSubmenuOpen.value = true
  }
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

function saveDepartmentsToStorage() {
  localStorage.setItem('cael_departments', JSON.stringify(departments.value))
}

function saveDepartmentPositionsToStorage() {
  localStorage.setItem('cael_department_positions', JSON.stringify(departmentPositions.value))
}

// FOR CREATE DEPARTMENT VIEW
const newDepartmentInput = ref('')
const deptAlertMessage = ref('')
const deptAlertStatus = ref('success')

function addDepartment() {
  deptAlertMessage.value = ''
  const name = newDepartmentInput.value.trim()
  if (!name) {
    deptAlertMessage.value = 'Please enter a department name.'
    deptAlertStatus.value = 'error'
    return
  }
  if (departments.value.some(d => d.toLowerCase() === name.toLowerCase())) {
    deptAlertMessage.value = `Department "${name}" already exists.`
    deptAlertStatus.value = 'error'
    return
  }
  departments.value.push(name)
  if (!departmentPositions.value[name]) {
    departmentPositions.value[name] = []
  }
  saveDepartmentsToStorage()
  saveDepartmentPositionsToStorage()
  newDepartmentInput.value = ''
  deptAlertMessage.value = `Department "${name}" created successfully!`
  deptAlertStatus.value = 'success'
}

function removeDepartment(deptName) {
  if (confirm(`Are you sure you want to delete department "${deptName}"?`)) {
    departments.value = departments.value.filter(d => d !== deptName)
    delete departmentPositions.value[deptName]
    saveDepartmentsToStorage()
    saveDepartmentPositionsToStorage()
  }
}

// FOR CREATE POSITION VIEW
const selectedDeptForPosition = ref('')
const newPositionInput = ref('')
const posAlertMessage = ref('')
const posAlertStatus = ref('success')

function addPosition() {
  posAlertMessage.value = ''
  if (!selectedDeptForPosition.value) {
    posAlertMessage.value = 'Please select a department.'
    posAlertStatus.value = 'error'
    return
  }
  const posName = newPositionInput.value.trim()
  if (!posName) {
    posAlertMessage.value = 'Please enter a position name.'
    posAlertStatus.value = 'error'
    return
  }
  
  const currentList = departmentPositions.value[selectedDeptForPosition.value] || []
  if (currentList.some(p => p.toLowerCase() === posName.toLowerCase())) {
    posAlertMessage.value = `Position "${posName}" already exists in ${selectedDeptForPosition.value}.`
    posAlertStatus.value = 'error'
    return
  }

  if (!departmentPositions.value[selectedDeptForPosition.value]) {
    departmentPositions.value[selectedDeptForPosition.value] = []
  }
  departmentPositions.value[selectedDeptForPosition.value].push(posName)
  saveDepartmentPositionsToStorage()
  newPositionInput.value = ''
  posAlertMessage.value = `Position "${posName}" added to ${selectedDeptForPosition.value}!`
  posAlertStatus.value = 'success'
}

function removePosition(deptName, posName) {
  if (confirm(`Are you sure you want to delete position "${posName}" from ${deptName}?`)) {
    if (departmentPositions.value[deptName]) {
      departmentPositions.value[deptName] = departmentPositions.value[deptName].filter(p => p !== posName)
      saveDepartmentPositionsToStorage()
    }
  }
}

const availablePositions = computed(() => {
  if (!employeeForm.value.department) return []
  return departmentPositions.value[employeeForm.value.department] || []
})

const computedEmpRoleSlug = computed(() => {
  if (!employeeForm.value.position) return ''
  return employeeForm.value.position.trim().toLowerCase().replace(/\s+/g, '_')
})

// BALANCE MODAL STATE
const showBalanceModal = ref(false)
const modalMode = ref('add')
const modalUser = ref(null)
const modalAmountStr = ref('')

function openBalanceModal(targetUser, mode) {
  modalUser.value = targetUser
  modalMode.value = mode
  modalAmountStr.value = ''
  showBalanceModal.value = true
}

function closeBalanceModal() {
  showBalanceModal.value = false
  modalUser.value = null
}

function promptAdd(targetUser) {
  openBalanceModal(targetUser, 'add')
}

function promptDeduct(targetUser) {
  openBalanceModal(targetUser, 'deduct')
}

const isValidAmount = computed(() => {
  const val = parseFloat(modalAmountStr.value)
  return !isNaN(val) && val > 0
})

async function confirmBalanceModal() {
  if (!isValidAmount.value || !modalUser.value) return
  const val = parseFloat(modalAmountStr.value)
  const finalAmount = modalMode.value === 'add' ? val : -val
  const userId = modalUser.value.id
  
  closeBalanceModal()
  
  try {
    const res = await authApi.updateBalance(userId, finalAmount)
    if (res.ok) {
      successMsg.value = `Updated balance for @${modalUser.value.username} to ₱${res.balance.toFixed(2)}`
      fetchUsers()
    }
  } catch (err) {
    error.value = err.message || 'Failed to update balance'
  }
}

function sortList(list, field, dir) {
  const arr = [...list]
  arr.sort((a, b) => {
    let valA = a[field]
    let valB = b[field]

    if (valA == null) valA = ''
    if (valB == null) valB = ''

    let comparison = 0
    if (field === 'created_at') {
      const timeA = valA ? new Date(valA).getTime() : 0
      const timeB = valB ? new Date(valB).getTime() : 0
      comparison = timeA - timeB
    } else if (typeof valA === 'number' && typeof valB === 'number') {
      comparison = valA - valB
    } else if (typeof valA === 'boolean' && typeof valB === 'boolean') {
      comparison = (valA ? 1 : 0) - (valB ? 1 : 0)
    } else {
      comparison = String(valA).localeCompare(String(valB))
    }

    return dir === 'asc' ? comparison : -comparison
  })
  return arr
}

// COMPUTED LISTS
const driverUsers = computed(() => users.value.filter(u => u.role === 'driver'))
const passengerUsers = computed(() => users.value.filter(u => u.role === 'passenger'))
const adminUsers = computed(() => users.value.filter(u => u.role === 'admin' || u.role === 'super_admin'))

const filteredEmployees = computed(() => {
  const q = employeeSearch.value.toLowerCase().trim()
  let list = employeeUsers.value
  if (q) {
    list = list.filter(u => 
      u.full_name?.toLowerCase().includes(q) ||
      u.email?.toLowerCase().includes(q) ||
      u.username?.toLowerCase().includes(q) ||
      u.department?.toLowerCase().includes(q) ||
      u.position?.toLowerCase().includes(q) ||
      u.role?.toLowerCase().includes(q)
    )
  }
  return sortList(list, sortField.value, sortDir.value)
})

const displayedEmployees = computed(() => filteredEmployees.value)

const filteredDrivers = computed(() => {
  const q = driverSearch.value.toLowerCase().trim()
  let list = driverUsers.value
  if (q) {
    list = list.filter(u => 
      u.full_name?.toLowerCase().includes(q) ||
      u.email?.toLowerCase().includes(q) ||
      u.username?.toLowerCase().includes(q)
    )
  }
  return sortList(list, sortField.value, sortDir.value)
})

const displayedDrivers = computed(() => filteredDrivers.value)

const filteredPassengers = computed(() => {
  const q = passengerSearch.value.toLowerCase().trim()
  let list = passengerUsers.value
  if (q) {
    list = list.filter(u => 
      u.full_name?.toLowerCase().includes(q) ||
      u.email?.toLowerCase().includes(q) ||
      u.username?.toLowerCase().includes(q)
    )
  }
  return sortList(list, sortField.value, sortDir.value)
})

const displayedPassengers = computed(() => filteredPassengers.value)

const filteredAdmins = computed(() => {
  const q = adminSearch.value.toLowerCase().trim()
  let list = adminUsers.value
  if (q) {
    list = list.filter(u => 
      u.full_name?.toLowerCase().includes(q) ||
      u.email?.toLowerCase().includes(q) ||
      u.username?.toLowerCase().includes(q)
    )
  }
  return sortList(list, sortField.value, sortDir.value)
})

const displayedAdmins = computed(() => filteredAdmins.value)

const pendingTopUpCount = computed(() => balanceLogs.value.filter(l => l.status === 'pending').length)
const totalDriverBalance = computed(() => driverUsers.value.reduce((acc, u) => acc + (u.balance || 0), 0))

const filteredTopUpLogs = computed(() => {
  const q = topUpSearch.value.toLowerCase().trim()
  if (!q) return balanceLogs.value
  return balanceLogs.value.filter(l => 
    l.username?.toLowerCase().includes(q) ||
    l.reference_number?.toLowerCase().includes(q) ||
    l.system_ref?.toLowerCase().includes(q)
  )
})

// BACKUP GRAPH & AUDIT STATES AND COMPUTED PROPERTIES
const balanceStats = ref([])
const hoveredPoint = ref(null)

const chartWidth = 500
const chartHeight = 220
const chartPadding = 40

const chartMaxVal = computed(() => {
  if (!balanceStats.value || balanceStats.value.length === 0) return 100
  const allTotals = balanceStats.value.flatMap(s => [s.load_total || 0, s.fee_total || 0])
  return Math.max(...allTotals, 100)
})

const chartMinVal = computed(() => {
  if (!balanceStats.value || balanceStats.value.length === 0) return 0
  const allTotals = balanceStats.value.flatMap(s => [s.load_total || 0, s.fee_total || 0])
  return Math.min(...allTotals, 0)
})

const loadChartPoints = computed(() => {
  if (!balanceStats.value || balanceStats.value.length === 0) return []
  const N = balanceStats.value.length
  
  const maxVal = chartMaxVal.value
  const minVal = chartMinVal.value
  const range = maxVal - minVal || 1
  
  return balanceStats.value.map((s, idx) => {
    let x = chartPadding
    if (N > 1) {
      x = chartPadding + (idx / (N - 1)) * (chartWidth - 2 * chartPadding)
    } else {
      x = chartWidth / 2
    }
    const y = chartHeight - chartPadding - (((s.load_total || 0) - minVal) / range) * (chartHeight - 2 * chartPadding)
    return {
      x,
      y,
      date: s.date,
      total: s.load_total || 0,
      change: s.load_change || 0,
      type: 'load'
    }
  })
})

const feeChartPoints = computed(() => {
  if (!balanceStats.value || balanceStats.value.length === 0) return []
  const N = balanceStats.value.length
  
  const maxVal = chartMaxVal.value
  const minVal = chartMinVal.value
  const range = maxVal - minVal || 1
  
  return balanceStats.value.map((s, idx) => {
    let x = chartPadding
    if (N > 1) {
      x = chartPadding + (idx / (N - 1)) * (chartWidth - 2 * chartPadding)
    } else {
      x = chartWidth / 2
    }
    const y = chartHeight - chartPadding - (((s.fee_total || 0) - minVal) / range) * (chartHeight - 2 * chartPadding)
    return {
      x,
      y,
      date: s.date,
      total: s.fee_total || 0,
      change: s.fee_change || 0,
      type: 'fee'
    }
  })
})

const loadChartPath = computed(() => {
  const pts = loadChartPoints.value
  if (pts.length < 2) return ''
  return pts.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
})

const feeChartPath = computed(() => {
  const pts = feeChartPoints.value
  if (pts.length < 2) return ''
  return pts.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
})

// TRANSACTION AUDIT FILTERS
const showLoadFilter = ref(true)
const showFeeFilter = ref(true)
const selectedLogDate = ref('')

const filteredBalanceLogs = computed(() => {
  return balanceLogs.value.filter(log => {
    if (log.type === 'load' && !showLoadFilter.value) return false
    if (log.type === 'fee' && !showFeeFilter.value) return false
    
    if (selectedLogDate.value && log.created_at) {
      const logDateStr = log.created_at.split('T')[0]
      if (logDateStr !== selectedLogDate.value) return false
    }
    
    return true
  })
})

const loadCount = computed(() => {
  return balanceLogs.value.filter(log => {
    if (log.type !== 'load') return false
    if (selectedLogDate.value && log.created_at) {
      const logDateStr = log.created_at.split('T')[0]
      if (logDateStr !== selectedLogDate.value) return false
    }
    return true
  }).length
})

const feeCount = computed(() => {
  return balanceLogs.value.filter(log => {
    if (log.type !== 'fee') return false
    if (selectedLogDate.value && log.created_at) {
      const logDateStr = log.created_at.split('T')[0]
      if (logDateStr !== selectedLogDate.value) return false
    }
    return true
  }).length
})

// BOOKING DATE RANGE & COLLAPSE LOGIC
function formatDateString(date) {
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

const todayDate = new Date()
const defaultStartDate = formatDateString(new Date(todayDate.getTime() - 7 * 24 * 60 * 60 * 1000))
const defaultEndDate = formatDateString(todayDate)

// Non-document booking date range (Default 7 days)
const bookingStartDate = ref(defaultStartDate)
const bookingEndDate = ref(defaultEndDate)

// Document history date range (Default 7 days)
const docBookingStartDate = ref(defaultStartDate)
const docBookingEndDate = ref(defaultEndDate)

const collapsedDays = ref({})
const loadingBookings = ref(false)
const selectedPreviewImage = ref(null)

function resetBookingDateRange(type) {
  if (type === 'doc_bookings') {
    docBookingStartDate.value = defaultStartDate
    docBookingEndDate.value = defaultEndDate
  } else {
    bookingStartDate.value = defaultStartDate
    bookingEndDate.value = defaultEndDate
  }
}

// 1. FILTERED NON-DOCUMENT BOOKINGS (RIDE HAIL ONLY)
const filteredBookings = computed(() => {
  return bookings.value.filter(b => {
    const isDoc = !!(b.document_image || b.document_info || b.document_tip || b.received_image || b.signature_image)
    if (isDoc) return false

    if (!b.date) return false
    const bDateStr = b.date.split('T')[0]
    if (bookingStartDate.value && bDateStr < bookingStartDate.value) return false
    if (bookingEndDate.value && bDateStr > bookingEndDate.value) return false
    return true
  })
})

const bookingsByDay = computed(() => {
  const map = {}
  filteredBookings.value.forEach(b => {
    const dateKey = b.date ? b.date.split('T')[0] : 'Unknown'
    if (!map[dateKey]) map[dateKey] = []
    map[dateKey].push(b)
  })
  return Object.keys(map).sort().reverse().map(date => ({
    date,
    list: map[date]
  }))
})

// 2. FILTERED DOCUMENT BOOKINGS (DOCUMENT DELIVERIES ONLY)
const filteredDocBookings = computed(() => {
  return bookings.value.filter(b => {
    const isDoc = !!(b.document_image || b.document_info || b.document_tip || b.received_image || b.signature_image)
    if (!isDoc) return false

    if (!b.date) return false
    const bDateStr = b.date.split('T')[0]
    if (docBookingStartDate.value && bDateStr < docBookingStartDate.value) return false
    if (docBookingEndDate.value && bDateStr > docBookingEndDate.value) return false
    return true
  })
})

const docBookingsByDay = computed(() => {
  const map = {}
  filteredDocBookings.value.forEach(b => {
    const dateKey = b.date ? b.date.split('T')[0] : 'Unknown'
    if (!map[dateKey]) map[dateKey] = []
    map[dateKey].push(b)
  })
  return Object.keys(map).sort().reverse().map(date => ({
    date,
    list: map[date]
  }))
})

const allDaysCollapsed = computed(() => {
  if (bookingsByDay.value.length === 0) return true
  return bookingsByDay.value.every(group => isCollapsed(group.date))
})

function isCollapsed(date) {
  return collapsedDays.value[date] !== false
}

function toggleDayCollapse(date) {
  const current = isCollapsed(date)
  collapsedDays.value = {
    ...collapsedDays.value,
    [date]: current ? false : true
  }
}

function toggleAllDays() {
  const targetState = !allDaysCollapsed.value
  const nextCollapsed = {}
  bookingsByDay.value.forEach(group => {
    nextCollapsed[group.date] = targetState ? true : false
  })
  collapsedDays.value = nextCollapsed
}

// ANALYTICS & GRAPH COMPUTED DATA (PAST 7 DAYS)
const past7DaysData = computed(() => {
  const result = []
  const today = new Date()
  
  for (let i = 6; i >= 0; i--) {
    const d = new Date()
    d.setDate(today.getDate() - i)
    const dateStr = d.toISOString().split('T')[0]
    const dayLabel = d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
    const dayShort = d.toLocaleDateString('en-US', { weekday: 'short' })
    
    // Calculate totals for date
    const dayBookings = bookings.value.filter(b => b.date && b.date.startsWith(dateStr))
    const dayCompletedRides = dayBookings.filter(b => (b.status || '').toLowerCase() === 'completed').length
    const dayBookingIncome = dayBookings.reduce((acc, b) => acc + (b.amount || 0), 0)
    
    const dayBalanceLogs = balanceLogs.value.filter(l => l.created_at && l.created_at.startsWith(dateStr) && l.status === 'approved')
    const dayLoadIncome = dayBalanceLogs.reduce((acc, l) => acc + (l.amount || 0), 0)
    
    const totalDayRevenue = dayBookingIncome + dayLoadIncome
    
    result.push({
      date: dateStr,
      label: dayLabel,
      shortLabel: dayShort,
      rides: dayCompletedRides,
      bookingIncome: dayBookingIncome,
      loadIncome: dayLoadIncome,
      totalRevenue: totalDayRevenue
    })
  }
  return result
})

const maxRevenueValue = computed(() => {
  const max = Math.max(...past7DaysData.value.map(d => d.totalRevenue), 100)
  return max * 1.15
})

const revenueChartPoints = computed(() => {
  const data = past7DaysData.value
  const width = 600
  const height = 180
  const padding = 20
  
  return data.map((d, i) => {
    const x = padding + (i / Math.max(data.length - 1, 1)) * (width - 2 * padding)
    const y = height - padding - (d.totalRevenue / maxRevenueValue.value) * (height - 2 * padding)
    return { x, y, val: d.totalRevenue, label: d.shortLabel, fullDate: d.label }
  })
})

const revenueLinePath = computed(() => {
  const points = revenueChartPoints.value
  if (points.length === 0) return ''
  
  let d = `M ${points[0].x} ${points[0].y}`
  for (let i = 1; i < points.length; i++) {
    const prev = points[i - 1]
    const curr = points[i]
    const cx = (prev.x + curr.x) / 2
    d += ` C ${cx} ${prev.y}, ${cx} ${curr.y}, ${curr.x} ${curr.y}`
  }
  return d
})

const revenueAreaPath = computed(() => {
  const linePath = revenueLinePath.value
  if (!linePath) return ''
  const points = revenueChartPoints.value
  const lastPoint = points[points.length - 1]
  const firstPoint = points[0]
  return `${linePath} L ${lastPoint.x} 180 L ${firstPoint.x} 180 Z`
})

const maxRideCount = computed(() => {
  const max = Math.max(...past7DaysData.value.map(d => d.rides), 5)
  return max
})

const totalRoleUsersCount = computed(() => {
  return (driverUsers.value.length + passengerUsers.value.length + employeeUsers.value.length + adminUsers.value.length) || 1
})

const driverPercent = computed(() => Math.round((driverUsers.value.length / totalRoleUsersCount.value) * 100))
const passengerPercent = computed(() => Math.round((passengerUsers.value.length / totalRoleUsersCount.value) * 100))
const employeePercent = computed(() => Math.round((employeeUsers.value.length / totalRoleUsersCount.value) * 100))
const adminPercent = computed(() => Math.round((adminUsers.value.length / totalRoleUsersCount.value) * 100))

// ANIMATED COUNTER STATES & LOGIC FOR DASHBOARD CARDS
const animatedIncomeFee = ref(0)
const animatedLoadIncome = ref(0)
const animatedExpense = ref(0)
const animatedCompletedRides = ref(0)

const targetIncomeFee = computed(() => {
  const bookingTotal = bookings.value.filter(b => (b.amount || 0) > 0).reduce((acc, b) => acc + (b.amount || 0), 0)
  const feeLogTotal = balanceLogs.value
    .filter(l => (l.reference_number || '').includes('-F') || (l.payment_method || '').includes('fee'))
    .reduce((acc, l) => acc + Math.abs(l.amount || 0), 0)
  return bookingTotal + feeLogTotal
})

const targetLoadIncome = computed(() => {
  return balanceLogs.value
    .filter(l => l.status === 'approved' && (l.amount || 0) > 0 && !(l.reference_number || '').includes('-F'))
    .reduce((acc, l) => acc + (l.amount || 0), 0)
})

const targetExpense = computed(() => 0) // 0 for now as requested for future connection

const targetCompletedRides = computed(() => {
  return bookings.value.filter(b => (b.status || '').toLowerCase() === 'completed').length
})

function animateValue(start, end, duration, onUpdate) {
  const startTime = performance.now()
  function update(currentTime) {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    // Smooth ease-out cubic animation
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    const current = start + (end - start) * easeProgress
    onUpdate(current)
    if (progress < 1) {
      requestAnimationFrame(update)
    }
  }
  requestAnimationFrame(update)
}

function triggerCountingAnimation() {
  animateValue(0, targetIncomeFee.value, 1200, val => animatedIncomeFee.value = val)
  animateValue(0, targetLoadIncome.value, 1200, val => animatedLoadIncome.value = val)
  animateValue(0, targetExpense.value, 1200, val => animatedExpense.value = val)
  animateValue(0, targetCompletedRides.value, 1200, val => animatedCompletedRides.value = val)
}

function refreshDashboardData() {
  fetchUsers()
  fetchBalanceData()
  fetchBookings()
  setTimeout(() => {
    triggerCountingAnimation()
  }, 200)
}

function formatAnimatedCurrency(val) {
  return (val || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

watch(activeView, (newView) => {
  if (newView === 'dashboard') {
    triggerCountingAnimation()
  }
})

watch([targetIncomeFee, targetLoadIncome, targetCompletedRides], () => {
  if (activeView.value === 'dashboard') {
    triggerCountingAnimation()
  }
})

// API ACTIONS

async function fetchUsers() {
  error.value = ''
  loading.value = true
  try {
    const list = await authApi.getUsers()
    users.value = list
  } catch (err) {
    error.value = err.message || 'Failed to fetch users list.'
  } finally {
    loading.value = false
  }
}

async function fetchBalanceData() {
  try {
    const [logs, stats] = await Promise.all([
      authApi.getBalanceLogs(),
      authApi.getBalanceStats()
    ])
    balanceLogs.value = logs
    balanceStats.value = stats
  } catch (e) {
    console.error("Failed to fetch balance stats/logs:", e)
  }
}

async function fetchTopUpMonitoring() {
  await fetchBalanceData()
}

async function fetchBookings() {
  try {
    const res = await authApi.getBookings()
    bookings.value = res
  } catch (e) {
    console.error("Failed to fetch bookings:", e)
  }
}

async function handleToggleActive(targetUser) {
  try {
    const res = await authApi.toggleActive(targetUser.id)
    if (res.ok) fetchUsers()
  } catch (err) {
    error.value = err.message || 'Failed to update user status.'
  }
}

async function handleToggleActivated(targetUser) {
  try {
    const res = await authApi.toggleActivated(targetUser.id)
    if (res.ok) fetchUsers()
  } catch (err) {
    error.value = err.message || 'Failed to toggle activation state.'
  }
}

async function handleVerifyTopUp(logId) {
  try {
    await authApi.verifyTopUp(logId)
    fetchBalanceData()
    fetchUsers()
  } catch (err) {
    error.value = err.message || 'Failed to verify top-up'
  }
}

async function handleUnverifyTopUp(logId) {
  try {
    await authApi.unverifyTopUp(logId)
    fetchBalanceData()
  } catch (err) {
    error.value = err.message || 'Failed to reject top-up'
  }
}

async function submitEmployeeForm() {
  employeeError.value = ''
  employeeSuccess.value = ''

  if (!employeeForm.value.username ||
      !employeeForm.value.password ||
      !employeeForm.value.first_name || 
      !employeeForm.value.last_name || 
      !employeeForm.value.age || 
      !employeeForm.value.sex || 
      !employeeForm.value.email || 
      !employeeForm.value.address || 
      !employeeForm.value.department || 
      !employeeForm.value.position || 
      !employeeForm.value.location) {
    employeeError.value = 'All fields except Middle Name are required.'
    return
  }

  isAddingEmployee.value = true
  try {
    await authApi.addEmployee({
      username: employeeForm.value.username,
      password: employeeForm.value.password,
      first_name: employeeForm.value.first_name,
      middle_name: employeeForm.value.middle_name || null,
      last_name: employeeForm.value.last_name,
      age: parseInt(employeeForm.value.age),
      sex: employeeForm.value.sex,
      email: employeeForm.value.email,
      address: employeeForm.value.address,
      department: employeeForm.value.department,
      position: employeeForm.value.position,
      location: employeeForm.value.location
    })
    
    employeeSuccess.value = 'Employee added successfully!'
    resetEmployeeForm()
    fetchUsers()
    setTimeout(() => {
      activeView.value = 'employee_list'
    }, 1200)
  } catch (err) {
    employeeError.value = err.message || 'Failed to add employee.'
  } finally {
    isAddingEmployee.value = false
  }
}

function formatDate(isoStr) {
  if (!isoStr) return 'N/A'
  try {
    const d = new Date(isoStr)
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  } catch (e) {
    return isoStr
  }
}

function formatTime(isoStr) {
  if (!isoStr) return ''
  try {
    const d = new Date(isoStr)
    return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  } catch (e) {
    return ''
  }
}

function getDefaultCurrentUserId() {
  if (!user.value) return '1'
  const currentUserId = user.value.id || user.value.employee_id || user.value.username
  
  const options = availableSalaryEmployeeOptions.value || []
  if (options.length > 0) {
    const match = options.find(u => 
      String(u.id) === String(currentUserId) ||
      String(u.employee_id) === String(currentUserId) ||
      (u.username && user.value.username && u.username === user.value.username) ||
      (u.full_name && user.value.full_name && u.full_name.toLowerCase() === user.value.full_name.toLowerCase()) ||
      (u.first_name && user.value.first_name && `${u.first_name} ${u.last_name}`.toLowerCase() === `${user.value.first_name} ${user.value.last_name}`.toLowerCase())
    )
    if (match) {
      return String(match.id || match.employee_id || match.username)
    }
  }

  return String(currentUserId || '1')
}

function syncDefaultUserSelections() {
  const currentId = getDefaultCurrentUserId()
  if (currentId) {
    if (typeof selectedOvertimeEmployeeId !== 'undefined') selectedOvertimeEmployeeId.value = String(currentId)
    if (typeof selectedLeaveEmployeeId !== 'undefined') selectedLeaveEmployeeId.value = String(currentId)
    if (typeof selectedPayrollLeaveEmployeeId !== 'undefined') selectedPayrollLeaveEmployeeId.value = String(currentId)
    if (typeof selectedPayrollGenerateEmployeeId !== 'undefined') selectedPayrollGenerateEmployeeId.value = String(currentId)
  }
}

async function handleLogout() {
  await autoClockOutOnLogout()
  auth.logout()
  router.push('/login')
}

onMounted(async () => {
  loadAttendanceFromStorage()
  loadCashAdvancesFromStorage()
  loadModuleApproversFromStorage()
  loadContributionRulesFromStorage()
  await Promise.all([
    fetchUsers(),
    fetchBalanceData(),
    fetchBookings(),
    fetchRolePermissionsData()
  ])
  syncDefaultUserSelections()
  triggerCountingAnimation()
})
</script>

<style scoped>
.timesheet-drag-scroll {
  cursor: grab;
  user-select: none;
}
.timesheet-drag-scroll.is-dragging {
  cursor: grabbing !important;
}

.admin-dashboard-root {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg-dark, #0b0f19);
  color: var(--text-1, #f3f4f6);
}

/* TOP NAVBAR */
.top-navbar {
  height: 60px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
  box-sizing: border-box;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.hamburger-btn {
  background: transparent;
  border: none;
  color: var(--text-1);
  padding: 0.35rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.2s ease;
  box-shadow: none;
}

.hamburger-btn:hover {
  opacity: 0.8;
  background: transparent;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  cursor: pointer;
}

.brand-logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
  color: #ffffff;
}

.brand-subtitle {
  font-size: 0.68rem;
  color: #94a3b8;
}

.view-indicator-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: none;
  padding: 0;
  font-weight: 700;
  font-size: 0.95rem;
  color: #ffffff;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  position: relative;
}

.header-settings-btn {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0.25rem !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, opacity 0.2s ease;
  outline: none;
}

.header-settings-btn:hover {
  transform: rotate(45deg);
  opacity: 0.85;
  background: transparent !important;
}

.header-settings-btn svg {
  stroke: #94a3b8;
  transition: stroke 0.2s ease;
}

.header-settings-btn:hover svg {
  stroke: #ffffff;
}

/* USER PROFILE DROPDOWN WRAPPER */
.user-dropdown-wrapper {
  position: relative;
}

.user-profile-pill-btn {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: transparent;
  padding: 0.25rem 0.35rem;
  border-radius: 0;
  border: none;
  color: var(--text-1);
  cursor: pointer;
  transition: opacity 0.2s ease;
  box-shadow: none;
}

.user-profile-pill-btn:hover, .user-profile-pill-btn.active {
  background: transparent;
  opacity: 0.85;
}

.user-avatar-badge {
  font-size: 1rem;
}

.user-meta-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.user-name-label {
  font-size: 0.82rem;
  font-weight: 600;
}

.user-role-subtag {
  font-size: 0.65rem;
  color: #a5b4fc;
  font-weight: 700;
}

.dropdown-arrow-icon {
  font-size: 0.6rem;
  color: #94a3b8;
  margin-left: 0.2rem;
}

/* PROFILE DROPDOWN MENU */
.profile-dropdown-menu {
  position: absolute;
  top: 48px;
  right: 0;
  width: 260px;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  z-index: 200;
  overflow: hidden;
  backdrop-filter: blur(16px);
}

.dropdown-header {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  background: rgba(255, 255, 255, 0.03);
}

.dropdown-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.dropdown-user-details {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.dropdown-fullname {
  font-weight: 700;
  font-size: 0.88rem;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-email {
  font-size: 0.75rem;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-role-badge {
  display: inline-flex;
  margin-top: 0.2rem;
  font-size: 0.65rem;
  font-weight: 700;
  color: #a5b4fc;
  background: rgba(99, 102, 241, 0.18);
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
  width: fit-content;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  width: 100%;
}

.dropdown-body, .dropdown-footer {
  padding: 0.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: transparent;
  border: none;
  color: var(--text-1);
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  width: 100%;
  text-align: left;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.dropdown-item-icon {
  font-size: 1rem;
}

.dropdown-item-text {
  display: flex;
  flex-direction: column;
}

.item-main {
  font-size: 0.85rem;
  font-weight: 600;
}

.item-sub {
  font-size: 0.7rem;
  color: #94a3b8;
}

.logout-item {
  color: #fca5a5;
}

.logout-item:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

/* LAYOUT & SIDEBAR */
.main-layout {
  display: flex;
  flex: 1;
  width: 100%;
  min-height: calc(100vh - 60px);
}

.sidebar-drawer {
  width: 240px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  flex-direction: column;
  transition: all 0.25s ease;
  flex-shrink: 0;
}

.sidebar-drawer.collapsed {
  width: 0;
  overflow: hidden;
  opacity: 0;
  padding: 0;
}

.sidebar-content {
  padding: 1.25rem 0.75rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.nav-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.45rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-group-header:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.04);
}

.group-title {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.chevron-icon {
  font-size: 0.6rem;
  opacity: 0.7;
}

.nav-sub-items {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding-left: 0.4rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: transparent;
  border: none;
  color: #cbd5e1;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.84rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  width: 100%;
  text-align: left;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
}

.nav-item.active {
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #ffffff;
  font-weight: 600;
}

.item-icon {
  font-size: 1rem;
}

.item-text {
  flex: 1;
}

.item-badge {
  background: rgba(255, 255, 255, 0.12);
  padding: 0.1rem 0.45rem;
  border-radius: 99px;
  font-size: 0.7rem;
  font-weight: 700;
}

.item-badge.alert-badge {
  background: #ef4444;
  color: #ffffff;
}

/* CONTENT CONTAINER & PAGES */
.content-container {
  flex: 1;
  padding: 1.5rem 2rem;
  overflow-y: auto;
}

.page-view {
  padding: 1.75rem;
  border-radius: 14px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 1rem;
}

.header-title-box {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.view-heading {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.count-pill {
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  border: 1px solid rgba(99, 102, 241, 0.3);
  padding: 0.15rem 0.65rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
}

.view-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* PERFECT SEARCH & DROPDOWN ALIGNMENT */
.search-input-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  height: 38px;
  padding: 0 0.85rem;
  box-sizing: border-box;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 240px;
}

.search-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  line-height: 1;
  flex-shrink: 0;
  opacity: 0.7;
}

.search-input {
  flex: 1;
  height: 100%;
  border: none;
  background: transparent;
  color: #ffffff;
  font-size: 0.84rem;
  outline: none;
  padding: 0;
  margin: 0;
  line-height: normal;
}

.search-input::placeholder {
  color: #94a3b8;
}

.clear-search-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-search-btn:hover {
  color: #ffffff;
}

.inline-btn {
  height: 38px;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0 0.85rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
}

/* SELECT DROPDOWNS */
.select-wrapper {
  position: relative;
  width: 100%;
}

.select-input,
.form-select {
  width: 100%;
  height: 42px;
  display: flex;
  align-items: center;
  padding: 0 2.2rem 0 0.85rem;
  border-radius: 10px;
  background-color: rgba(15, 23, 42, 0.85) !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  color: #f8fafc !important;
  font-size: 0.9rem;
  outline: none;
  box-sizing: border-box;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338bdf8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.85rem center;
  background-size: 1em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-input:focus,
.form-select:focus {
  border-color: #38bdf8 !important;
  background-color: rgba(15, 23, 42, 0.95) !important;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
}

.select-input:disabled,
.form-select:disabled {
  background-color: rgba(15, 23, 42, 0.4) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
  color: #64748b !important;
  cursor: not-allowed !important;
  opacity: 0.65;
}

/* POPUP OPTIONS */
.select-input option,
.form-select option,
select option {
  background-color: #0f172a !important;
  color: #f8fafc !important;
  padding: 10px 14px;
}

.select-input option:disabled,
.form-select option:disabled,
select option:disabled {
  background-color: #0f172a !important;
  color: #64748b !important;
}


/* FULL PAGE PROFILE VIEW */
.profile-page-view {
  max-width: 900px;
  margin: 0 auto;
}

.profile-card-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.5rem;
}

.profile-main-card {
  padding: 2rem 1.5rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.profile-avatar-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.2);
  border: 2px solid rgba(99, 102, 241, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
}

.profile-identity {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

.profile-name {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0;
}

.profile-username {
  font-family: monospace;
  color: #a5b4fc;
  font-size: 0.88rem;
}

.profile-role-badge {
  margin-top: 0.4rem;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #a5b4fc;
  padding: 0.2rem 0.75rem;
  border-radius: 99px;
  font-weight: 700;
  font-size: 0.72rem;
}

.profile-details-card {
  padding: 1.75rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.card-section-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 1.2rem 0;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0.6rem;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.06);
}

.info-label {
  font-size: 0.85rem;
  color: #94a3b8;
}

.info-val {
  font-size: 0.88rem;
  font-weight: 600;
  color: #ffffff;
}

.font-mono {
  font-family: monospace;
  color: #a5b4fc;
}

.balance-text {
  color: #34d399;
  font-weight: 700;
}

/* TABLES */
.table-container {
  width: 100%;
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.2);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.users-table th, .users-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.84rem;
}

.users-table th {
  background: rgba(255, 255, 255, 0.03);
  color: #94a3b8;
  font-weight: 600;
}

.sortable-th {
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}

.sortable-th:hover {
  color: #a5b4fc;
}

.sort-icon {
  font-size: 0.7rem;
  margin-left: 0.25rem;
}

.name-col {
  display: flex;
  flex-direction: column;
}

.u-name {
  font-weight: 600;
  color: #ffffff;
}

.u-email {
  font-size: 0.78rem;
  color: #94a3b8;
}

.u-username {
  color: #a5b4fc;
  font-family: monospace;
  font-size: 0.82rem;
}

.role-badge {
  display: inline-flex;
  padding: 0.15rem 0.5rem;
  border-radius: 99px;
  font-size: 0.7rem;
  font-weight: 600;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #60a5fa;
}

.role-badge.driver {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.3);
}

.role-badge.passenger {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border-color: rgba(245, 158, 11, 0.3);
}

.status-badge {
  display: inline-flex;
  padding: 0.15rem 0.5rem;
  border-radius: 99px;
  font-size: 0.7rem;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.status-badge.disabled {
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
}

.dept-badge {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #34d399;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  font-size: 0.74rem;
  font-weight: 600;
}

/* TRANSITIONS */
.dropdown-enter-active, .dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* SEPARATE SETTING BUTTON ON LEFT SIDE OF USER PROFILE */
.header-settings-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #f1f5f9;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.header-settings-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.5);
  transform: rotate(35deg);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.3);
}


/* FIXED FULL-SCREEN MODAL OVERLAY (LIGHT BACKDROP BLUR SCREEN) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 1rem;
  box-sizing: border-box;
  animation: modalFadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* GENERAL MODAL CONTENT CARD (LIGHT SCREEN STYLE) */
.modal-content {
  background: #ffffff;
  color: #0f172a;
  border-radius: 16px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.8);
  border: 1px solid #e2e8f0;
  max-width: 500px;
  width: 100%;
  padding: 1.75rem;
  box-sizing: border-box;
  transform: translateY(0);
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.94) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.5rem 0;
}

.modal-desc {
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 1.2rem;
}

.modal-username {
  font-weight: 600;
  color: #2563eb;
}

.modal-input-group {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #cbd5e1;
  border-radius: 10px;
  padding: 0.5rem 0.85rem;
  margin-bottom: 1.5rem;
  transition: border-color 0.2s ease;
}

.modal-input-group:focus-within {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.modal-currency {
  font-size: 1.1rem;
  font-weight: 700;
  color: #64748b;
  margin-right: 0.5rem;
}

.modal-input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 1.1rem;
  font-weight: 600;
  color: #0f172a;
  outline: none;
}

.modal-btn-group {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* ROLE SETUP POP-UP MODAL (LIGHT SCREEN STYLE) */
.role-modal-content {
  max-width: 640px;
  width: 95%;
  max-height: 88vh;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
  background: #ffffff;
  color: #0f172a;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  box-shadow: 0 30px 70px -15px rgba(15, 23, 42, 0.35);
}

.role-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.role-modal-icon {
  font-size: 1.4rem;
}

.role-modal-header .modal-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
}

.modal-close-btn {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #64748b;
  font-size: 1.1rem;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.role-modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  background: transparent;
}

.role-select-form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  background: rgba(15, 23, 42, 0.6);
  padding: 1.25rem;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.role-select-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.role-select-wrapper {
  position: relative;
  width: 100%;
}

.role-select-dropdown {
  width: 100%;
  padding: 0.75rem 2.2rem 0.75rem 1rem;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 10px;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 600;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.role-select-dropdown:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
}

.select-arrow-icon {
  position: absolute;
  right: 0.9rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.75rem;
  color: #94a3b8;
  pointer-events: none;
}

.role-select-hint {
  font-size: 0.82rem;
  color: #94a3b8;
  margin-top: 0.35rem;
}

.role-select-hint strong {
  color: #38bdf8;
}

.menu-permissions-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.perm-group {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.perm-group:hover {
  border-color: rgba(255, 255, 255, 0.2);
}

.perm-group-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1.25rem;
  background: rgba(30, 41, 59, 0.6);
  border: none;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  text-align: left;
  transition: background 0.2s ease;
}

.perm-group-header:hover {
  background: rgba(51, 65, 85, 0.7);
}

.perm-group-title {
  color: #ffffff;
}

.perm-chevron {
  color: #38bdf8;
  font-size: 0.8rem;
}

.perm-group-body {
  padding: 0.75rem 1.25rem 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(15, 23, 42, 0.4);
}

.perm-item-switch {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.7rem 0.85rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.2s ease;
}

.perm-item-switch:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(56, 189, 248, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.perm-item-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.perm-item-icon {
  font-size: 1.15rem;
}

.perm-item-text {
  display: flex;
  flex-direction: column;
}

.perm-item-name {
  font-size: 0.88rem;
  font-weight: 600;
  color: #ffffff;
}

.perm-item-sub {
  font-size: 0.76rem;
  color: #94a3b8;
}

/* iOS LIGHT STYLE TOGGLE SWITCH */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 25px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(255, 255, 255, 0.2);
  transition: .25s ease;
  border-radius: 25px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 19px;
  width: 19px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .25s ease;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

input:checked + .toggle-slider {
  background-color: #10b981;
}

input:checked + .toggle-slider:before {
  transform: translateX(21px);
}

.modal-save-alert {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
}

.modal-save-alert.success {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #047857;
}

.modal-save-alert.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

/* ANIMATED CHECKMARK & SUCCESS MODAL POPUP */
.access-success-overlay {
  z-index: 11000 !important;
  backdrop-filter: blur(8px);
}

.access-success-card {
  max-width: 440px !important;
  width: 90% !important;
  text-align: center;
  padding: 2.25rem 2rem !important;
  border-radius: 24px !important;
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(16, 185, 129, 0.2) !important;
  animation: modalPopIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes modalPopIn {
  from {
    opacity: 0;
    transform: scale(0.85) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animated-checkmark-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1.25rem;
}

.checkmark-circle {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
}

.checkmark-svg {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: block;
  stroke-width: 3.5;
  stroke: #10b981;
  stroke-miterlimit: 10;
  box-shadow: inset 0px 0px 0px #10b981;
}

.checkmark-circle-bg {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 3.5;
  stroke-miterlimit: 10;
  stroke: #10b981;
  fill: none;
  animation: strokeCircle 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: strokeCheck 0.4s cubic-bezier(0.65, 0, 0.45, 1) 0.35s forwards;
}

@keyframes strokeCircle {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes strokeCheck {
  100% {
    stroke-dashoffset: 0;
  }
}

.access-success-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.4rem;
}

.access-success-subtitle {
  font-size: 0.88rem;
  color: #94a3b8;
  margin-bottom: 1.25rem;
  line-height: 1.4;
}

.access-success-details-box {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1.5rem;
  text-align: left;
}

.details-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.details-label {
  color: #94a3b8;
}

.details-value {
  color: #38bdf8;
  font-weight: 700;
}

.details-badge {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
}

.access-success-btn {
  width: 100%;
  padding: 0.75rem 1.5rem;
  font-weight: 700;
  font-size: 0.95rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #10b981, #059669);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
  cursor: pointer;
  border: none;
  color: #fff;
  transition: all 0.2s ease;
}

.access-success-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
}

.role-modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.8rem;
  padding: 1.1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.save-perm-btn {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #ffffff;
  border: none;
  padding: 0.65rem 1.35rem;
  border-radius: 99px;
  font-weight: 600;
  font-size: 0.9rem;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-perm-btn:hover:not(:disabled) {
  opacity: 0.94;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
}

/* STANDALONE DASHBOARD NAV ITEM */
.standalone-group {
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.standalone-nav-item {
  width: 100%;
  font-weight: 700;
  font-size: 0.95rem;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.standalone-nav-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
  color: #ffffff !important;
  border-color: #2563eb !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

/* INLINE 4 CARDS DASHBOARD GRID */
.dashboard-inline-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.75rem;
}

@media (max-width: 1200px) {
  .dashboard-inline-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .dashboard-inline-cards-grid {
    grid-template-columns: 1fr;
  }
}

.dash-stat-card {
  background: rgba(30, 41, 59, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.35rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.dash-stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.4);
}

.dash-stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
}

.card-income-fee::before {
  background: linear-gradient(90deg, #10b981, #059669);
}

.card-load-income::before {
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
}

.card-expense::before {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.card-completed-rides::before {
  background: linear-gradient(90deg, #8b5cf6, #6d28d9);
}

.card-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.card-icon-badge {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}

.icon-income-fee {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.icon-load-income {
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.icon-expense {
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.icon-completed-rides {
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.card-trend-tag {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.6rem;
  border-radius: 99px;
}

.card-trend-tag.positive {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.card-trend-tag.neutral {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.25);
}

.card-trend-tag.badge-count {
  background: rgba(139, 92, 246, 0.15);
  color: #c4b5fd;
  border: 1px solid rgba(139, 92, 246, 0.25);
}

.card-content-body {
  display: flex;
  flex-direction: column;
}

.card-metric-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 0.35rem;
}

.card-metric-value {
  font-size: 1.65rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
  margin: 0 0 0.25rem 0;
  font-feature-settings: "tnum";
  font-variant-numeric: tabular-nums;
}

.card-metric-sub {
  font-size: 0.76rem;
  color: #64748b;
}

.refresh-blue-icon-btn {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0.25rem !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, opacity 0.2s ease;
  outline: none;
}

.refresh-blue-icon-btn:hover {
  transform: rotate(180deg);
  opacity: 0.85;
  background: transparent !important;
}

.refresh-blue-icon-btn svg {
  stroke: #3b82f6;
  transition: stroke 0.2s ease;
}

.refresh-blue-icon-btn:hover svg {
  stroke: #60a5fa;
}

/* DASHBOARD CHARTS & ANALYTICS GRID */
.dashboard-charts-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.chart-card {
  background: rgba(30, 41, 59, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  transition: border-color 0.25s ease;
}

.chart-card:hover {
  border-color: rgba(99, 102, 241, 0.3);
}

.chart-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chart-header-title {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.chart-icon {
  font-size: 1.5rem;
}

.chart-heading {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.chart-subheading {
  font-size: 0.78rem;
  color: #94a3b8;
  margin: 0.15rem 0 0 0;
}

.chart-legend {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.8rem;
  color: #94a3b8;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.revenue-dot { background: #3b82f6; }
.driver-dot { background: #8b5cf6; }
.passenger-dot { background: #10b981; }
.employee-dot { background: #f59e0b; }
.admin-dot { background: #ec4899; }

.analytics-svg-chart {
  width: 100%;
  height: 200px;
  overflow: visible;
}

.chart-dot {
  transition: r 0.2s ease, fill 0.2s ease;
  cursor: pointer;
}

.chart-dot:hover {
  r: 8;
  fill: #60a5fa;
}

.chart-card-dual-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

@media (max-width: 992px) {
  .chart-card-dual-grid {
    grid-template-columns: 1fr;
  }
}

/* BAR CHART STYLING */
.bar-chart-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 160px;
  padding-top: 1rem;
  gap: 0.75rem;
}

.bar-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
  gap: 0.4rem;
}

.bar-value {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
}

.bar-track {
  width: 100%;
  max-width: 32px;
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.bar-fill {
  width: 100%;
  background: linear-gradient(180deg, #6366f1 0%, #3b82f6 100%);
  border-radius: 8px 8px 0 0;
  transition: height 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.bar-column:hover .bar-fill {
  background: linear-gradient(180deg, #818cf8 0%, #60a5fa 100%);
}

.bar-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

/* USER DISTRIBUTION LIST */
.user-dist-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 0.5rem;
}

.dist-item {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.dist-row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85rem;
}

.dist-label {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  color: #e2e8f0;
  font-weight: 600;
}

.dist-count {
  color: #94a3b8;
  font-weight: 700;
  font-size: 0.82rem;
}

.dist-progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 99px;
  overflow: hidden;
}

.dist-progress-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.6s ease;
}

.driver-fill { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.passenger-fill { background: linear-gradient(90deg, #10b981, #34d399); }
.employee-fill { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.admin-fill { background: linear-gradient(90deg, #ec4899, #f472b6); }

/* BACKUP GRAPH & AUDIT GRID STYLES */
.stats-audit-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

@media (max-width: 900px) {
  .stats-audit-grid {
    grid-template-columns: 1fr;
  }
}

.card-sec-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-1, #ffffff);
  margin-top: 0;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  letter-spacing: 0.3px;
}

/* Inline Card Header & Filters for Transactions */
.card-header-with-filters {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.card-header-with-filters .card-sec-title {
  margin-bottom: 0;
  white-space: nowrap;
}

.log-filter-bar {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: nowrap;
}

.filter-checkboxes {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-2, #94a3b8);
  cursor: pointer;
  user-select: none;
  transition: color 0.2s ease;
}

.filter-checkbox-label:hover {
  color: var(--text-1, #ffffff);
}

.filter-checkbox {
  width: 14px;
  height: 14px;
  cursor: pointer;
  accent-color: #6366f1;
}

.filter-checkbox.checkbox-load {
  accent-color: #10b981;
}

.filter-checkbox.checkbox-fee {
  accent-color: #3b82f6;
}

.filter-text {
  font-size: 0.8rem;
  color: #e2e8f0;
}

.filter-date-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  padding: 0.2rem 0.5rem;
  transition: border-color 0.2s ease;
}

.filter-date-group:focus-within,
.filter-date-group:hover {
  border-color: rgba(99, 102, 241, 0.5);
}

.filter-date-icon {
  font-size: 0.75rem;
  opacity: 0.8;
}

.filter-date-input {
  background: transparent;
  border: none;
  color: #e2e8f0;
  font-size: 0.75rem;
  font-family: inherit;
  outline: none;
  cursor: pointer;
  color-scheme: dark;
}

.btn-clear-date {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0 2px;
  line-height: 1;
  transition: color 0.2s ease;
}

.btn-clear-date:hover {
  color: #ef4444;
}

.stats-card, .audit-card {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.chart-container-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.balance-svg-chart {
  width: 100%;
  height: auto;
  overflow: visible;
}

.chart-gridline {
  stroke: rgba(255, 255, 255, 0.08);
  stroke-width: 1;
  stroke-dasharray: 4, 4;
}

.chart-axis-label {
  font-size: 0.65rem;
  fill: #94a3b8;
  font-weight: 500;
}

.chart-line {
  stroke-width: 3;
  fill: none;
}

.chart-line.load-line {
  stroke: #10b981;
  filter: drop-shadow(0 0 5px rgba(16, 185, 129, 0.35));
}

.chart-line.fee-line {
  stroke: #8b5cf6;
  filter: drop-shadow(0 0 5px rgba(139, 92, 246, 0.35));
}

.chart-point {
  fill: #fff;
  cursor: pointer;
  transition: r 0.2s cubic-bezier(0.4, 0, 0.2, 1), fill 0.2s, stroke 0.2s;
}

.chart-point.load-point {
  stroke: #10b981;
  stroke-width: 2.5;
}

.chart-point.load-point:hover {
  r: 7.5;
  fill: #10b981;
  stroke: #fff;
}

.chart-point.fee-point {
  stroke: #8b5cf6;
  stroke-width: 2.5;
}

.chart-point.fee-point:hover {
  r: 7.5;
  fill: #8b5cf6;
  stroke: #fff;
}

.chart-labels {
  display: flex;
  font-size: 0.72rem;
  color: #94a3b8;
  padding: 0 0.5rem;
}

.chart-tooltip {
  position: absolute;
  background: rgba(22, 18, 30, 0.95);
  border: 1px solid #8b5cf6;
  border-radius: 6px;
  padding: 0.45rem 0.65rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5), 0 0 15px rgba(139, 92, 246, 0.25);
  transform: translate(-50%, calc(-100% - 8px));
  z-index: 10;
}

.tooltip-arrow {
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 8px;
  height: 8px;
  background: rgba(22, 18, 30, 0.95);
  border-right: 1px solid #8b5cf6;
  border-bottom: 1px solid #8b5cf6;
}

.tooltip-total {
  font-family: monospace;
  font-weight: 700;
  color: #fff;
  font-size: 0.85rem;
}

.tooltip-date {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 0.15rem;
}

.audit-logs-feed {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 220px;
  overflow-y: auto;
  padding-right: 0.35rem;
}

.audit-log-row {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.65rem 0.85rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(255, 255, 255, 0.02);
  font-size: 0.82rem;
  transition: border-color 0.2s, background 0.2s;
}

.audit-log-row.load {
  border-left: 3px solid #10b981;
}

.audit-log-row.fee {
  border-left: 3px solid #3b82f6;
}

.bookings-filter-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.bookings-filter-bar .filter-label {
  font-weight: 600;
  font-size: 0.85rem;
  color: #e2e8f0;
}

.bookings-filter-bar .filter-inputs {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* PROOF ATTACHMENTS & DOCUMENT TAGS */
.proof-thumbnails-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.btn-proof-preview {
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: #a5b4fc;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-proof-preview:hover {
  background: rgba(99, 102, 241, 0.3);
  color: #ffffff;
  border-color: #6366f1;
}

.doc-info-text {
  font-size: 0.82rem;
  color: #e2e8f0;
  font-weight: 500;
}

.tip-tag {
  font-size: 0.82rem;
  color: #f59e0b;
  font-weight: 700;
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
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  transition: color 0.2s ease;
}

.eye-btn:hover {
  color: #ffffff;
}

.eye-btn svg {
  width: 18px;
  height: 18px;
}

@keyframes popInModal {
  0% { opacity: 0; transform: scale(0.85) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes pulseGlowSuccess {
  0%, 100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); transform: scale(1); }
  50% { box-shadow: 0 0 35px rgba(16, 185, 129, 0.65); transform: scale(1.05); }
}

@keyframes shakeError {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}
</style>



