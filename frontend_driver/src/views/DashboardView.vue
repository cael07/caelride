<template>
  <div class="app-shell">

    <!-- ===== SIDEBAR ===== -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">

      <!-- Sidebar Header / Branding -->
      <div class="sidebar-brand">
        <div class="brand-icon">
          <img src="/cael.ico" alt="CAEL" class="brand-logo-img" />
        </div>
        <Transition name="label-fade">
          <span v-if="!sidebarCollapsed" class="brand-name">CAEL</span>
        </Transition>
        <button class="collapse-btn" @click="mobileSidebarOpen = true" title="Open menu">
          <span></span><span></span><span></span>
        </button>
      </div>

      <!-- Driver mini-profile -->
      <div class="sidebar-profile" v-if="!sidebarCollapsed">
        <div class="sp-avatar" v-if="user?.face_image_base64">
          <img :src="user.face_image_base64" alt="face" />
        </div>
        <div class="sp-avatar sp-initials" v-else>{{ initials }}</div>
        <div class="sp-info">
          <span class="sp-name">{{ user?.full_name || 'Driver' }}</span>
          <span class="sp-role">Driver</span>
        </div>
      </div>
      <div class="sidebar-profile-mini" v-else>
        <div class="sp-avatar" v-if="user?.face_image_base64">
          <img :src="user.face_image_base64" alt="face" />
        </div>
        <div class="sp-avatar sp-initials" v-else>{{ initials }}</div>
      </div>

      <!-- Nav Items -->
      <nav class="sidebar-nav">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="nav-item"
          :class="{ active: activePage === item.key }"
          @click="activePage = item.key"
          :title="item.label"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <Transition name="label-fade">
            <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          </Transition>
          <Transition name="label-fade">
            <span v-if="!sidebarCollapsed && activePage === item.key" class="nav-active-dot"></span>
          </Transition>
        </button>
      </nav>

      <!-- Sidebar Footer -->
      <div class="sidebar-footer">
        <button class="nav-item nav-logout" @click="handleLogout" title="Logout">
          <span class="nav-icon">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
            </svg>
          </span>
          <Transition name="label-fade">
            <span v-if="!sidebarCollapsed" class="nav-label">Logout</span>
          </Transition>
        </button>
      </div>
    </aside>

    <!-- ===== CONTENT AREA ===== -->
    <main class="content-area">

      <!-- Mobile top bar -->
      <div class="mobile-topbar">
        <button class="mobile-menu-btn" @click="mobileSidebarOpen = !mobileSidebarOpen">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
        </button>
        <span class="mobile-page-title">{{ currentPageLabel }}</span>
        <button 
          class="btn btn-ghost mobile-drive-btn" 
          v-if="activePage === 'home'" 
          :disabled="!user?.is_activated"
          :title="!user?.is_activated ? 'Account pending activation' : ''"
          @click="$router.push('/driver')"
        >
          🚗 Drive
        </button>
        <button class="btn btn-ghost mobile-logout" v-else @click="handleLogout">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
        </button>
      </div>

      <!-- Mobile Sidebar Overlay -->
      <Transition name="overlay-fade">
        <div v-if="mobileSidebarOpen" class="mobile-overlay" @click="mobileSidebarOpen = false">
          <aside class="mobile-sidebar" @click.stop>
            <div class="sidebar-brand">
              <div class="brand-icon"><img src="/cael.ico" alt="CAEL" class="brand-logo-img" /></div>
              <span class="brand-name">CAEL</span>
              <button class="close-btn" @click="mobileSidebarOpen = false" title="Close menu">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
              </button>
            </div>
            <div class="sidebar-profile">
              <div class="sp-avatar" v-if="user?.face_image_base64"><img :src="user.face_image_base64" alt="face" /></div>
              <div class="sp-avatar sp-initials" v-else>{{ initials }}</div>
              <div class="sp-info">
                <span class="sp-name">{{ user?.full_name || 'Driver' }}</span>
                <span class="sp-role">Driver</span>
              </div>
            </div>
            <nav class="sidebar-nav">
              <button v-for="item in navItems" :key="item.key" class="nav-item" :class="{ active: activePage === item.key }"
                @click="activePage = item.key; mobileSidebarOpen = false" :title="item.label">
                <span class="nav-icon" v-html="item.icon"></span>
                <span class="nav-label">{{ item.label }}</span>
                <span v-if="activePage === item.key" class="nav-active-dot"></span>
              </button>
            </nav>
            <div class="sidebar-footer">
              <button class="nav-item nav-logout" @click="handleLogout">
                <span class="nav-icon"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg></span>
                <span class="nav-label">Logout</span>
              </button>
            </div>
          </aside>
        </div>
      </Transition>

      <!-- =================== PAGE: HOME =================== -->
      <Transition name="page-switch" mode="out-in">
        <div v-if="activePage === 'home'" key="home" class="page-content">
          <div class="page-header">
            <h1 class="page-title">Home</h1>
            <p class="page-sub">Welcome back, {{ user?.full_name?.split(' ')[0] || 'Driver' }}!</p>
          </div>

          <div class="home-grid">
            <!-- Activation Status Banner -->
            <div class="activation-banner" v-if="!user?.is_activated">
              <div class="act-left">
                <span class="act-pulse"></span>
                <div>
                  <p class="act-title">Status: For Activation</p>
                  <p class="act-desc">Go to the office to get activated and receive your equipment.</p>
                </div>
              </div>
            </div>

            <!-- Wallet Card -->
            <div class="wallet-card">
              <div class="wc-brand">
                <svg viewBox="0 0 24 24" fill="url(#money-grad)" width="22" height="18" class="wc-money-icon" style="opacity: 0.95; filter: drop-shadow(0 1px 3px rgba(245,158,11,0.35));">
                  <defs>
                    <linearGradient id="money-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#f59e0b"/>
                      <stop offset="100%" stop-color="#d97706"/>
                    </linearGradient>
                  </defs>
                  <path d="M21 18H3V6h18v12zm-9-9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zm7 4c0-.55-.45-1-1-1s-1 .45-1 1v1h2v-1zm-14-2c0 .55.45 1 1 1s1-.45 1-1V9H5v2zm14-2c0 .55-.45-1-1-1s-1 .45-1 1v1h2V9zM6 15c0-.55-.45-1-1-1s-1 .45-1 1v1h2v-1z"/>
                </svg>
                <span>CAEL Wallet</span>
              </div>
              <div class="wc-balance-block">
                <span class="wc-lbl">Balance</span>
                <span class="wc-amount">₱ {{ (user?.balance || 0).toFixed(2) }}</span>
              </div>

              <!-- Waiting Approval / Unverified Fix Block below balance -->
              <div v-if="pendingTopUpTotal > 0 || unverifiedTopUpCount > 0" class="wc-pending-block" style="display: flex; align-items: center; justify-content: space-between; margin-top: 0.5rem; padding: 6px 12px; background: rgba(0,0,0,0.3); border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); flex-wrap: wrap; gap: 6px;">
                <span v-if="pendingTopUpTotal > 0" style="font-size: 0.8rem; color: #fbbf24; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  ⏳ ₱ {{ pendingTopUpTotal.toFixed(2) }} Waiting Approval
                </span>
                <button 
                  v-if="unverifiedTopUpCount > 0" 
                  class="btn-fix-unverified" 
                  @click="openFixRefModal" 
                  style="background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.45); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; margin-left: auto;"
                >
                  ⚠️ Unverified (Click to fix)
                </button>
              </div>

              <div class="wc-footer">
                <span class="wc-name">{{ user?.full_name || 'Driver Name' }}</span>
                <button class="wc-topup-btn" @click="openGcashModal" title="Top Up Balance via GCash">
                  <span class="plus-icon">+</span>
                  <span>Top Up</span>
                </button>
              </div>
            </div>

            <!-- Wallet Transaction History Card -->
            <div class="wallet-history-card glass">
              <div class="card-header-with-filters">
                <h3 class="card-sec-title">📋 Wallet History</h3>
                
                <div class="log-filter-bar">
                  <!-- Type Checkboxes -->
                  <div class="filter-checkboxes">
                    <label class="filter-checkbox-label">
                      <input type="checkbox" v-model="showLoadFilter" class="filter-checkbox">
                      <span class="checkbox-custom load"></span>
                      <span class="filter-text">Loads</span>
                    </label>
                    <label class="filter-checkbox-label">
                      <input type="checkbox" v-model="showFeeFilter" class="filter-checkbox">
                      <span class="checkbox-custom fee"></span>
                      <span class="filter-text">Fees</span>
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
                  <p>No matching transaction history found.</p>
                </div>
                <div 
                  v-else 
                  v-for="log in filteredBalanceLogs" 
                  :key="log.id" 
                  class="audit-log-row glass clickable"
                  :class="log.type"
                  @click="openLogDetails(log)"
                  title="Click to view full transaction details"
                  style="cursor: pointer;"
                >
                  <div class="audit-left">
                    <div class="audit-icon-wrap" :class="log.type">
                      <span v-if="log.type === 'load'">📈</span>
                      <span v-else>📉</span>
                    </div>
                    <div class="audit-desc-col">
                      <span class="audit-desc-title">
                        {{ log.type === 'load' ? (log.status === 'pending' ? 'Load Pending Approval' : (log.status === 'rejected' ? 'Load Unverified' : 'Load Credited')) : 'Ride Fee Deducted' }}
                      </span>
                      <span class="audit-time">{{ formatDate(log.created_at) }} {{ formatTime(log.created_at) }}</span>
                    </div>
                  </div>
                  <div class="audit-right">
                    <span :class="['audit-amount', log.amount >= 0 ? 'deposit' : 'deduct']">
                      {{ log.amount >= 0 ? '+' : '' }}₱{{ Math.abs(log.amount).toFixed(2) }}
                    </span>
                    <span class="audit-bal-lbl">Bal: ₱{{ log.new_balance.toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Ride History Card -->
            <div class="ride-history-card glass">
              <div class="card-header-with-filters">
                <h3 class="card-sec-title">🚗 Ride History</h3>
                
                <div class="log-filter-bar">
                  <!-- Type Checkboxes -->
                  <div class="filter-checkboxes">
                    <label class="filter-checkbox-label">
                      <input type="checkbox" v-model="showPassengerFilter" class="filter-checkbox">
                      <span class="checkbox-custom passenger"></span>
                      <span class="filter-text">Passenger</span>
                    </label>
                    <label class="filter-checkbox-label">
                      <input type="checkbox" v-model="showDocumentFilter" class="filter-checkbox">
                      <span class="checkbox-custom document"></span>
                      <span class="filter-text">Document</span>
                    </label>
                  </div>
                  
                  <!-- Date Selector -->
                  <div class="filter-date-group">
                    <span class="filter-date-icon">📅</span>
                    <input 
                      type="date" 
                      v-model="selectedRideDate" 
                      class="filter-date-input"
                      title="Filter by specific date"
                    />
                    <button 
                      v-if="selectedRideDate" 
                      class="btn-clear-date" 
                      @click="selectedRideDate = ''" 
                      title="Clear date filter"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>
              
              <div class="audit-logs-feed">
                <div v-if="filteredBookings.length === 0" class="empty-audit-state">
                  <span>🚗</span>
                  <p>No matching ride history found.</p>
                </div>
                <div 
                  v-else 
                  v-for="b in filteredBookings" 
                  :key="b.id" 
                  class="audit-log-row glass clickable-ride-row"
                  :class="b.document_image ? 'document' : 'passenger'"
                  @click.stop="openRideDetails(b)"
                >
                  <div class="audit-left">
                    <div class="audit-icon-wrap" :class="b.document_image ? 'document' : 'passenger'">
                      <span v-if="b.document_image">📄</span>
                      <span v-else>👤</span>
                    </div>
                    <div class="audit-desc-col">
                      <span class="audit-desc-title">
                        {{ b.document_image ? 'Document Delivery' : 'Passenger Ride' }}
                      </span>
                      <span class="audit-passenger-info" style="font-size: 0.72rem; color: var(--text-2);">
                        Passenger: @{{ b.passenger_username }}
                      </span>
                      <span v-if="b.pickup" class="audit-address-row" style="font-size: 0.70rem; color: var(--text-2); display: flex; align-items: flex-start; gap: 4px; margin-top: 2px;">
                        <span style="color: #4ade80; font-size: 0.65rem; flex-shrink: 0; margin-top: 1px;">📍</span>
                        <span style="line-height: 1.3;">{{ b.pickup }}</span>
                      </span>
                      <span v-if="b.dropoff" class="audit-address-row" style="font-size: 0.70rem; color: var(--text-2); display: flex; align-items: flex-start; gap: 4px; margin-top: 1px;">
                        <span style="color: #f87171; font-size: 0.65rem; flex-shrink: 0; margin-top: 1px;">🏁</span>
                        <span style="line-height: 1.3;">{{ b.dropoff }}</span>
                      </span>
                      <span v-if="b.document_tip" style="font-size: 0.70rem; color: #f59e0b; display: flex; align-items: center; gap: 4px; margin-top: 2px; font-weight: 600;">
                        <span style="font-size: 0.65rem;">💰</span>
                        <span>Tip: ₱{{ b.document_tip }}</span>
                      </span>
                      <span class="audit-time">{{ formatDate(b.date) }} {{ formatTime(b.date) }}</span>
                    </div>
                  </div>
                  <div class="audit-right">
                    <span class="audit-amount deposit" style="color: #fff;">
                      ₱{{ (b.amount || 0).toFixed(2) }}
                    </span>
                    <span :class="['status-badge', b.status]" style="font-size: 0.62rem; padding: 0.1rem 0.35rem; border-radius: 4px; font-weight: 600; text-transform: uppercase;">
                      {{ b.status }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Ride Hailing Card -->
            <div class="ride-card glass">
              <div class="ride-card-header">
                <h3 class="ride-title">
                  <svg version="1.1" id="layer" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 450 450" style="enable-background:new 0 0 450 450;" xml:space="preserve" width="22" height="22">
                  <g>
                    <ellipse style="opacity:0.3;fill:#878787;" cx="227" cy="387.372" rx="169.655" ry="9.332"/>
                    <g>
                      <g>
                        <g>
                          <g>
                            <g>
                              <g>
                                <path style="fill:#06050B;" d="M306.608,344.848c0,17.609,14.275,31.884,31.884,31.884c17.609,0,31.884-14.275,31.884-31.884
                                  s-14.275-31.884-31.884-31.884C320.883,312.964,306.608,327.239,306.608,344.848z M309.75,347.246
                                  c-0.065-0.793-0.121-1.589-0.121-2.399c0-1.14,0.083-2.259,0.212-3.364h17.878l2.882,2.882l-2.882,2.882H309.75z
                                   M325.19,349.775l-10.851,10.851c-2.112-3.226-3.579-6.901-4.26-10.85L325.19,349.775z M310.235,338.955
                                  c0.793-3.822,2.348-7.361,4.489-10.466l10.466,10.466H310.235z M320.364,322.402l12.477,12.477v4.075h-4.075l-12.509-12.509
                                  C317.486,324.963,318.866,323.613,320.364,322.402z M332.841,331.304l-10.426-10.426c3.102-2.084,6.63-3.578,10.426-4.332
                                  V331.304z M338.492,315.984c0.892,0,1.77,0.054,2.641,0.133v17.714l-2.882,2.882l-2.882-2.881v-17.673
                                  C336.396,316.049,337.436,315.984,338.492,315.984z M332.841,373.15c-4.031-0.801-7.748-2.451-10.984-4.74l10.984-10.984
                                  V373.15z M343.661,357.426l11.19,11.19c-3.298,2.275-7.094,3.866-11.19,4.608V357.426z M354.27,320.695l-10.609,10.609
                                  v-14.832C347.52,317.171,351.109,318.626,354.27,320.695z M360.497,326.194l-12.691,12.691
                                  c-0.027,0.027-0.058,0.045-0.085,0.07h-3.904c-0.027-0.025-0.059-0.043-0.086-0.07c-0.027-0.026-0.044-0.058-0.07-0.085
                                  v-3.904c0.025-0.027,0.043-0.059,0.07-0.085l12.614-12.614C357.858,323.39,359.251,324.725,360.497,326.194z
                                   M348.883,347.246c-0.038,0-0.072-0.01-0.11-0.011l-2.761-2.761c-0.001-0.037-0.011-0.072-0.011-0.11
                                  c0-0.037,0.01-0.073,0.011-0.11l2.761-2.761c0.037-0.002,0.072-0.011,0.11-0.011l18.261,0
                                  c0.129,1.105,0.212,2.225,0.212,3.365c0,0.81-0.056,1.606-0.121,2.399H348.883z M366.905,349.775
                                  c-0.701,4.069-2.227,7.855-4.442,11.15l-11.15-11.15H366.905z M351.313,338.955l10.742-10.742
                                  c2.244,3.172,3.878,6.803,4.695,10.742L351.313,338.955z M356.894,367.082l-13.162-13.162
                                  c-0.027-0.027-0.044-0.058-0.07-0.086v-3.904c0.025-0.027,0.043-0.059,0.07-0.086c0.027-0.026,0.058-0.044,0.085-0.07h3.904
                                  c0.027,0.025,0.059,0.043,0.085,0.07l13.131,13.131C359.727,364.474,358.377,365.854,356.894,367.082z M338.492,373.711
                                  c-1.056,0-2.096-0.065-3.122-0.175v-18.54c0-0.038,0.01-0.073,0.011-0.11l2.761-2.761c0.037-0.001,0.072-0.011,0.11-0.011
                                  c0.038,0,0.072,0.01,0.11,0.011l2.761,2.761c0.001,0.037,0.011,0.072,0.011,0.11v18.582
                                  C340.262,373.657,339.384,373.711,338.492,373.711z M315.841,362.7l12.926-12.925h4.075v4.075l-13.003,13.003
                                  C318.37,365.607,317.035,364.213,315.841,362.7z"/>
                                <path style="fill:#2D2A33;" d="M292.74,344.848c0,25.268,20.484,45.752,45.752,45.752c25.268,0,45.752-20.484,45.752-45.752
                                  c0-25.268-20.484-45.753-45.752-45.753C313.224,299.095,292.74,319.579,292.74,344.848z M307.557,344.848
                                  c0-17.085,13.85-30.935,30.935-30.935c17.085,0,30.935,13.85,30.935,30.935c0,17.085-13.85,30.935-30.935,30.935
                                  C321.407,375.783,307.557,361.932,307.557,344.848z"/>
                              </g>
                              <circle style="fill:#06050B;" cx="338.492" cy="344.848" r="15.071"/>
                            </g>
                            <path style="fill:#1C1A21;" d="M328.766,305.062c0.266,0.601-0.046,1.323-0.698,1.612l-12.396,5.493
                              c-0.652,0.289-1.397,0.036-1.663-0.565l-12.786-28.851c-0.267-0.601,0.046-1.323,0.698-1.612l12.396-5.493
                              c0.652-0.289,1.397-0.036,1.663,0.565L328.766,305.062z"/>
                            <path style="fill:#2D2A33;" d="M335.246,341.674c-0.073-0.165,0.013-0.362,0.191-0.442l2.063-0.914
                              c0.179-0.079,0.383-0.01,0.456,0.155l3.475,7.683l1.137-0.504c0.451-0.2,0.667-0.699,0.483-1.115l-15.992-35.356
                              c-0.184-0.416-0.699-0.591-1.15-0.391l-5.205,2.306c-0.451,0.2-0.667,0.699-0.483,1.115l15.992,35.356
                              c0.184,0.416,0.699,0.591,1.15,0.391l1.359-0.602L335.246,341.674z"/>
                          </g>
                          <path style="fill:#8E1400;" d="M342.667,272.469c3.591,1.14,6.836,2.314,9.772,3.56c14.095,5.982,20.811,13.573,22.755,20.488
                            c1.105,3.93-1.424,5.516-5.298,3.75c-3.803-1.733-10.312-3.685-21.565-4.133c-8.327-0.331-18.816,0.103-31.967,1.28
                            C321.616,285.6,331.132,276.826,342.667,272.469z"/>
                          <path style="fill:#DAE9EE;" d="M317.826,294.396c13.265-0.787,23.655-0.882,31.842-0.255
                            c11.759,0.902,18.352,3.396,22.141,5.526c0.981,0.551,1.862,0.836,2.616,0.904c-0.956,0.623-2.554,0.595-4.529-0.305
                            c-3.803-1.733-10.312-3.685-21.565-4.133c-8.327-0.331-18.816,0.103-31.967,1.28
                            C316.817,296.393,317.297,295.386,317.826,294.396z"/>
                          <path style="fill:#C62D14;" d="M348.745,275.926c1.278,0.447,2.503,0.894,3.682,1.366c13.332,5.337,19.872,12.482,21.786,19.091
                            c0.253,0.873,0.316,1.595,0.24,2.189c-2.776-4.169-7.917-8.121-16.554-11.096C354.192,284.167,350.735,280.205,348.745,275.926z
                            "/>
                          <path style="fill:#1C1A21;" d="M122.87,293.922c-0.267,0.601,0.046,1.323,0.698,1.612l12.396,5.493
                            c0.652,0.289,1.397,0.036,1.663-0.565l12.786-28.85c0.266-0.601-0.046-1.323-0.698-1.612l-12.396-5.493
                            c-0.652-0.289-1.396-0.036-1.663,0.565L122.87,293.922z"/>
                          <g>
                            <path style="fill:#26232B;" d="M157.036,342.75c3.135,8.065,12.493,14.603,20.903,14.603l52.142,0
                              c8.41,0,14.554-6.538,11.419-14.603l-23.637-10.776c-3.135-8.065-0.357-28.608-8.766-28.608h-52.141
                              c-8.41,0-12.686,6.538-9.551,14.603L157.036,342.75z"/>
                            <path style="fill:#1C1A21;" d="M174.972,349.719h52.141c8.41,0,14.554-6.538,11.419-14.603l2.967,7.633
                              c3.135,8.065-3.009,14.603-11.419,14.603l-52.142,0c-8.41,0-17.768-6.538-20.903-14.603l-2.967-7.633
                              C157.203,343.181,166.562,349.719,174.972,349.719z"/>
                          </g>
                          <path style="fill:#8E1400;" d="M267.698,222.154c0,0,19.841,0,29.993,9.69c10.152,9.69,35.53,29.993,24.917,31.377
                            c-10.613,1.384-16.15,4.614-21.687,14.766s-17.073,16.611-13.382,23.533c3.691,6.922,9.981,11.661,1.214,20.428
                            c-8.767,8.767-9.519,20.178-20.594,19.716c-11.074-0.461-93.208-11.536-94.131-12.92c-0.923-1.384,48.213-2.768,52.366-2.768
                            c14.08,0,42.688,0.922,50.071-24.457c7.383-25.379,8.306-25.379,2.307-38.76C272.774,249.378,258.469,223.077,267.698,222.154z"
                            />
                          <path style="fill:#AD2202;" d="M325.451,297.134c6.011-1.472,22.788-9.036,18.559-10.399
                            c-4.228-1.363-28.157-13.052-43.521-14.869c-28.177,35.192-6.847,31.858-13.873,47.651
                            c-3.514,7.899-20.303,12.689-68.135,12.294c-12.448-0.103-8.01,25.082-6.616,25.082c68.753,0,74.286-2.673,77.059-19.38
                            C291.551,321.681,303.007,302.631,325.451,297.134z"/>
                          <path style="fill:#8E1400;" d="M137.167,263.589c-5.866-0.205-11.236-0.215-16.182,0.001
                            c-23.748,1.034-37.333,7.315-43.524,14.893c-3.519,4.307-0.531,7.368,6.055,6.935c6.464-0.425,17.043,0.087,33.93,4.545
                            c12.496,3.299,27.829,8.494,46.752,15.781C162.07,288.984,152.172,274.039,137.167,263.589z"/>
                          <path style="fill:#DAE9EE;" d="M163.474,301.409c-19.278-6.861-34.626-11.598-47.056-14.473
                            c-17.855-4.129-28.817-4.016-35.451-3.101c-1.718,0.237-3.159,0.192-4.309-0.059c1.119,1.186,3.499,1.862,6.857,1.642
                            c6.464-0.425,17.043,0.087,33.93,4.545c12.496,3.299,27.829,8.494,46.752,15.781
                            C164.014,304.296,163.784,302.854,163.474,301.409z"/>
                          <path style="fill:#AD2202;" d="M126.505,265.107c-2.107-0.023-4.137-0.022-6.109,0.03c-22.309,0.587-35.419,6.401-41.421,13.62
                            c-0.793,0.954-1.231,1.807-1.403,2.566c6.11-3.855,15.619-6.394,29.84-6.185C114.49,272.746,121.509,269.447,126.505,265.107z"
                            />
                          <path style="fill:#8E1400;" d="M285.463,334.397c2.627-15.83,14.084-34.88,36.527-40.378c3.308-0.81,13.846-4.198,21.953-7.308
                            c0.02,0.007,0.048,0.017,0.067,0.023c4.229,1.363-12.548,8.927-18.559,10.399c-22.443,5.497-33.9,24.548-36.527,40.378
                            c-2.737,16.491-0.928,19.84-45.476,19.84c-0.713,0-30.699,0.002-31.425,0.002c-0.306,0-0.918-1.68-1.307-3.577
                            C277.273,353.714,282.722,350.914,285.463,334.397z"/>
                          <path style="fill:#AD2202;" d="M164.887,331.768v-13.965c0-16.731-9.581-31.215-23.55-38.293h42.144
                            c23.7,0,42.913,19.213,42.913,42.913v9.344H164.887z"/>
                          <path style="fill:#C62D14;" d="M211.712,271.157c3.148,2.055-2.159,14.575-7.288,14.575c-5.128,0-40.486,0-49.663,0
                            c-9.177,0-76.384-39.677-76.384-48.314C78.377,228.781,146.394,228.511,211.712,271.157z"/>
                          <g>
                            <g>
                              <path style="fill:#06050B;" d="M75.894,344.847c0,17.609,14.275,31.884,31.884,31.884c17.609,0,31.884-14.275,31.884-31.884
                                c0-17.609-14.275-31.884-31.884-31.884C90.169,312.963,75.894,327.238,75.894,344.847z M79.036,347.246
                                c-0.065-0.793-0.121-1.589-0.121-2.399c0-1.14,0.084-2.259,0.212-3.364h17.878l2.882,2.881l-2.882,2.882L79.036,347.246z
                                 M94.476,349.775l-10.851,10.851c-2.112-3.226-3.579-6.901-4.26-10.85L94.476,349.775z M79.52,338.955
                                c0.793-3.822,2.348-7.361,4.489-10.466l10.466,10.466H79.52z M89.649,322.402l12.477,12.477v4.075h-4.075l-12.509-12.509
                                C86.772,324.963,88.152,323.613,89.649,322.402z M102.127,331.304L91.7,320.877c3.102-2.085,6.63-3.578,10.427-4.332V331.304z
                                 M107.778,315.984c0.892,0,1.77,0.054,2.641,0.133v17.714l-2.881,2.882l-2.882-2.882v-17.673
                                C105.682,316.049,106.722,315.984,107.778,315.984z M102.127,373.15c-4.031-0.8-7.748-2.451-10.984-4.74l10.984-10.984V373.15
                                z M112.947,357.426l11.19,11.19c-3.298,2.275-7.094,3.866-11.19,4.607V357.426z M123.556,320.695l-10.609,10.609l0-14.832
                                C116.805,317.171,120.395,318.626,123.556,320.695z M129.783,326.194l-12.691,12.691c-0.026,0.026-0.058,0.044-0.086,0.07
                                h-3.904c-0.027-0.025-0.059-0.043-0.085-0.07c-0.027-0.027-0.045-0.058-0.07-0.085v-3.905c0.025-0.027,0.043-0.059,0.07-0.085
                                l12.613-12.614C127.143,323.39,128.537,324.725,129.783,326.194z M118.168,347.246c-0.037,0-0.072-0.01-0.11-0.011
                                l-2.761-2.761c-0.001-0.037-0.011-0.072-0.011-0.11c0-0.038,0.01-0.073,0.011-0.11l2.761-2.761
                                c0.037-0.001,0.072-0.011,0.11-0.011h18.261c0.129,1.105,0.212,2.224,0.212,3.364c0,0.81-0.056,1.606-0.121,2.399
                                L118.168,347.246z M136.191,349.775c-0.701,4.069-2.227,7.855-4.442,11.151l-11.15-11.151H136.191z M120.598,338.955
                                l10.742-10.742c2.244,3.172,3.878,6.804,4.695,10.742L120.598,338.955z M126.179,367.082l-13.162-13.162
                                c-0.027-0.027-0.045-0.058-0.07-0.086v-3.904c0.025-0.027,0.043-0.059,0.07-0.085c0.026-0.027,0.058-0.045,0.085-0.07h3.904
                                c0.027,0.025,0.059,0.043,0.085,0.07l13.131,13.131C129.012,364.474,127.662,365.853,126.179,367.082z M107.778,373.711
                                c-1.056,0-2.096-0.065-3.122-0.175v-18.54c0-0.038,0.01-0.073,0.011-0.11l2.761-2.761c0.037-0.002,0.072-0.011,0.11-0.011
                                c0.037,0,0.072,0.01,0.11,0.011l2.761,2.761c0.002,0.037,0.011,0.072,0.011,0.11v18.582
                                C109.548,373.657,108.669,373.711,107.778,373.711z M85.126,362.7l12.925-12.926h4.075v4.075l-13.003,13.003
                                C87.655,365.607,86.32,364.213,85.126,362.7z"/>
                            <path style="fill:#2D2A33;" d="M62.025,344.848c0,25.268,20.484,45.752,45.752,45.752c25.269,0,45.753-20.484,45.753-45.752
                              c0-25.268-20.484-45.752-45.752-45.752C82.509,299.095,62.025,319.579,62.025,344.848z M76.843,344.847
                              c0-17.085,13.85-30.935,30.935-30.935c17.085,0,30.935,13.85,30.935,30.935c0,17.085-13.85,30.935-30.935,30.935
                              C90.693,375.783,76.843,361.932,76.843,344.847z"/>
                          </g>
                          
                            <ellipse transform="matrix(0.9817 -0.1904 0.1904 0.9817 -63.6957 26.8338)" style="fill:#06050B;" cx="107.778" cy="344.848" rx="15.071" ry="15.071"/>
                        </g>
                        <path style="fill:#AD2202;" d="M211.712,271.157c1.958,1.278,0.644,6.601-1.862,10.446c-19.268-1.593-43.014-8.85-56.785-15.033
                          c-25.967-11.659-48.675-24.48-61.317-30.343c-2.083-0.966-3.761-1.911-5.05-2.816
                          C106.779,230.555,160.084,237.449,211.712,271.157z"/>
                        <path style="fill:#C62D14;" d="M153.756,331.02c0,3.895,3.158,7.053,7.053,7.053h62.212c3.895,0,7.053-3.158,7.053-7.053l0,0
                          c0-3.895-3.158-7.053-7.053-7.053h-62.212C156.914,323.967,153.756,327.125,153.756,331.02L153.756,331.02z"/>
                        <path style="fill:#8E1400;" d="M160.809,334.095h62.212c3.2,0,5.87-2.144,6.733-5.064c0.188,0.635,0.32,1.294,0.32,1.989
                          c0,3.895-3.158,7.053-7.053,7.053h-62.212c-3.895,0-7.053-3.158-7.053-7.053c0-0.696,0.132-1.355,0.32-1.99
                          C154.939,331.95,157.61,334.095,160.809,334.095z"/>
                        <g>
                          <path style="fill:#423F4C;" d="M206.584,244.436c11.536,0,23.738,4.481,23.738,21.554c0,22.535-53.491,9.057-76.101-1.094
                            c-22.61-10.151-42.382-21.315-53.39-26.421c-10.956-5.081-9.302-9.498,5.003-9.498
                            C141.806,228.977,166.367,244.436,206.584,244.436z"/>
                          <path style="fill:#595666;" d="M223.501,268.143c0.284-16.086-11.658-20.393-23.018-20.473
                            c-39.604-0.281-63.535-15.016-98.959-15.267c-1.474-0.01-2.755,0.071-3.874,0.22c0.884-1.539,3.846-2.723,9.338-2.684
                            c35.424,0.251,59.354,14.986,98.958,15.267c11.36,0.081,23.302,4.388,23.018,20.473c-0.067,3.805-3.081,6.127-7.899,7.348
                            C222.595,271.779,223.465,270.171,223.501,268.143z"/>
                          <path style="fill:#2D2A33;" d="M95.015,230.688c0.965,1.34,3.151,2.856,6.561,4.438c11.007,5.105,30.78,16.269,53.39,26.421
                            c20.996,9.427,68.594,21.703,75.286,5.364c-1.493,21.204-53.744,7.991-76.03-2.015c-22.61-10.151-42.382-21.315-53.39-26.421
                            C94.04,235.325,92.106,232.433,95.015,230.688z"/>
                        </g>
                        <g>
                          <path style="fill:#C62D14;" d="M355.548,275.185c1.816,2.738-7.203,14.575-11.432,13.212
                            c-4.228-1.363-36.06-14.094-43.627-16.533c0,0-45.361-55.337-42.084-63.328C261.681,200.545,317.867,218.37,355.548,275.185z"
                            />
                          <path style="fill:#E8321F;" d="M348.3,285.617c-25.905-39.787-58.761-66.377-77.833-75.46
                            c15.126,1.834,54.682,23.092,83.559,66.63c0.131,0.335-0.179,1.947-1.958,4.558C350.934,283.009,349.578,284.517,348.3,285.617
                            z"/>
                          <path style="fill:#2D2A33;" d="M249.007,200.159c0,5.881,4.767,10.648,10.648,10.648h14.994c5.88,0,10.648-4.767,10.648-10.648
                            l0,0c0-5.881-4.767-10.648-10.648-10.648h-14.994C253.774,189.512,249.007,194.279,249.007,200.159L249.007,200.159z"/>
                          <path style="fill:#C62D14;" d="M268.347,181.037c-4.346,3.694-25.207,28.684,28.901,24.338
                            C296.161,193.206,268.347,181.037,268.347,181.037z"/>
                          <path style="fill:#423F4C;" d="M259.512,200.997c0.961,1.932,0.248,3.855-1.593,4.296l-13.282,3.018
                            c-1.841,0.441-4.112-0.768-5.074-2.7l0,0c-0.961-1.932-0.248-3.855,1.593-4.296l13.282-3.018
                            C256.28,197.857,258.551,199.066,259.512,200.997L259.512,200.997z"/>
                          <path style="fill:#2D2A33;" d="M245.083,204.109c0.662,1.33,0.171,2.655-1.097,2.958l-0.153,0.026
                            c-1.268,0.303-2.832-0.529-3.494-1.859l0,0c-0.662-1.331-0.171-2.655,1.097-2.959l0.153-0.026
                            C242.857,201.946,244.421,202.778,244.083,204.109L245.083,204.109z"/>
                          <g>
                            <path style="fill:#E8321F;" d="M270.635,182.691c5.39,2.546,24.296,12.134,25.153,21.729
                              c-3.591,0.288-6.812,0.432-9.717,0.457C283.762,198.024,276.489,189.112,270.635,182.691z"/>
                          </g>
                        </g>
                        <g>
                          <path style="fill:#2D2A33;" d="M111.251,342.963c0.073-0.165-0.013-0.363-0.191-0.442l-2.062-0.914
                            c-0.179-0.079-0.383-0.01-0.456,0.155l-3.475,7.683l-1.137-0.504c-0.451-0.2-0.667-0.699-0.483-1.115l15.992-35.356
                            c0.184-0.416,0.699-0.591,1.15-0.391l5.205,2.307c0.451,0.2,0.667,0.699,0.483,1.115l-15.992,35.356
                            c-0.184,0.416-0.699,0.591-1.15,0.391l-1.359-0.602L111.251,342.963z"/>
                          <path style="fill:#DAE9EE;" d="M113.799,321.162l11.098-25.04l9.888,4.382l-11.097,25.04c-0.266,0.601-1.011,0.854-1.663,0.565
                            l-7.526-3.335C113.845,322.485,113.533,321.763,113.799,321.162z"/>
                        </g>
                        <path style="fill:#8E1400;" d="M351.137,274.525c0,3.089-13.749-2.437-20.176-4.441c-6.33-1.974-2.545-7.551-0.593-14.474
                          c0.788-2.796,4.649-1.358,10.385,3.865C346.488,264.698,351.137,271.436,351.137,274.525z"/>
                        <path style="fill:#DAE9EE;" d="M338.907,261.782c4.977,4.533,9.132,10.203,10.144,13.642c-4.091-0.262-13.204-3.817-18.09-5.341
                          c-6.046-1.885-2.867-7.062-0.869-13.555C331.869,256.369,334.938,258.168,338.907,261.782z"/>
                        <path style="fill:#DAE9EE;" d="M327.048,307.126l5.65,12.747c0.266,0.601-0.046,1.323-0.698,1.612l-7.526,3.335
                          c-0.652,0.289-1.397,0.036-1.663-0.565l-5.65-12.747L327.048,307.126z"/>
                      </g>
                    </g>
                    <g>
                      <path style="fill:#FED09E;" d="M220.366,100.024c-1.89,13.723-13.057,23.132-24.942,21.017
                        c-11.885-2.115-19.986-14.954-18.096-28.676c1.89-13.723,13.057-23.132,24.942-21.017
                        C214.155,73.462,222.257,86.301,220.366,100.024z"/>
                      <g>
                        <path style="fill:#FED09E;" d="M254.551,307.698c-0.162,6.119-5.24,11.132-11.343,11.196l0,0
                          c-6.103,0.064-3.546-5.294-3.321-11.414c1.156-31.37-11.21-37.099-7.415-62.38c0.913-6.08,7.078-18.722,13.18-18.786l0,0
                          c6.103-0.064,10.92,4.845,10.758,10.964L254.551,307.698z"/>
                        
                          <rect x="172.86" y="114.073" transform="matrix(0.4754 -0.8798 0.8798 0.4754 -9.3974 231.0904)" style="fill:#FED09E;" width="32.414" height="18.703"/>
                        <path style="fill:#5CAD0E;" d="M198.269,214.484c-5.171-0.92-10.174-1.503-14.899-1.803
                          c2.911-15.555,10.678-26.534,13.072-39.984c4.658-26.173-7.237-37.224-16.532-51.999c-15.558,3.58-16.922,22.411-20.164,54.838
                          c-1.841,18.408-10.005,42.473-8.599,54.197c1.001,8.349,4.762,14.731,41.786,14.731c8.211,0,38.522,1.584,40.226,0.586
                          c13.635-7.981,22.471-10.553,22.746-12.094C257.379,224.677,223.373,218.951,198.269,214.484z"/>
                        <path style="fill:#417703;" d="M198.533,241.1c-33.272,0-44.23-7.714-45.543-16.303c-0.524-3.425-1.013-12.011-1.536-17.512
                          c0.363,8.701-0.894,17.554-0.307,22.449c1.001,8.349,7.16,14.73,41.786,14.731c7.688,0,34.727,1.56,39.559,0.763
                          C221.109,244.375,204.662,241.1,198.533,241.1z"/>
                        <path style="fill:#178FCE;" d="M185.257,212.815c3.157-14.572,8.89-27.217,11.185-40.117
                          c4.658-26.173-7.237-37.224-16.532-51.999c-15.558,3.58-27.251,18.472-25.28,51.001c1.279,21.102-3.512,34.697-3.802,47.72
                          C151.568,219.459,177.036,215.749,185.257,212.815z"/>
                        <path style="fill:#0E72AD;" d="M184.406,131.265c-0.329,0.076-14.19,8.279-14.511,8.363
                          c-12.067,5.854,9.942,44.108,11.574,47.047c1.788,3.22,5.547,6.111,8.798,7.859c2.322-7.473,4.662-14.646,6.175-21.837
                          C199.546,157.937,193.701,146.04,184.406,131.265z"/>
                        <path style="fill:#FED09E;" d="M237.378,193.621l-35.026-19.289l-16.523-40.751c-2.011-4.266-7.104-6.095-11.374-4.085
                          c-4.27,2.01-12.99,10.002-6.395,21.102l19.771,33.014c0.532,1.127,1.287,2.07,2.176,2.831c0.83,1.054,1.889,1.95,3.2,2.534
                          l45.905,13.318c8.88-6.934,8.425,8.425,15.095,1.886C257.579,200.874,254.724,189.408,237.378,193.621z"/>
                        <g>
                          <path style="fill:#FF3600;" d="M277.077,323.111c6.601-8.619-10.949-9.033-22.525-15.413c0,0-7.257,4.863-15.211,3.493
                            c0,0-5.426,16.702-0.457,16.891C238.883,328.082,266.443,328.566,277.077,323.111z"/>
                          <path style="fill:#06050B;" d="M277.97,320.651c-11.18,5.736-40.155,5.227-40.155,5.227c-0.581-0.022-1.036-0.22-1.412-0.518
                            c0.288,1.539,1.002,2.666,2.481,2.722c0,0,27.559,0.484,38.193-4.971c0.957-1.25,1.387-2.294,1.409-3.194
                            C278.331,320.155,278.164,320.398,277.97,320.651z"/>
                        </g>
                        <path style="fill:#75CE17;" d="M204.319,216.157c-7.196-1.231-14.037-2.231-20.172-2.976
                          c-4.363,1.363-11.944,2.849-18.783,4.029c22.452-0.956,49.371,0.245,84.718,11.637
                          C250.529,226.238,230.04,220.557,204.319,216.157z"/>
                        <path style="fill:#EFBB86;" d="M188.085,119.679c0.475,5.206,3.218,12.084,5.478,15.093l6.432-11.266
                          C196.974,122.51,192.55,121.819,188.085,119.679z"/>
                        <path style="fill:#FFDD50;" d="M216.3,112.036c-5.177-1.78-9.712-7.308-10.13-12.347l-0.529-6.387
                          c-0.418-5.039,3.44-7.681,8.617-5.901l10.233,3.519c-0.223-1.049-0.479-2.075-0.778-3.063
                          c-4.436-14.671-21.597-21.263-33.915-17.538c-12.318,3.724-23.776,23.391-15.904,42.183
                          c2.063,4.923,33.975,14.244,51.937,15.686c3.295,0.264,3.18-13.198-1.912-13.53L216.3,112.036z"/>
                        <path style="fill:#F2CD30;" d="M201.988,89.228c1.004,1.978,0.215,4.397-1.764,5.401c-1.978,1.004-4.397,0.215-5.401-1.764
                          c-1.004-1.979-0.215-4.397,1.764-5.401C198.565,86.46,200.984,87.25,201.988,89.228z"/>
                        <g>
                          <path style="fill:#F2CD30;" d="M224.885,115.391l-0.506-0.17c-0.522,3.497,0.21,8.633-1.868,8.416
                            c-18.004-1.875-44.342-9.48-49.888-14.741c0.514,1.275,1.103,2.553,1.778,3.83c2.775,5.24,31.5,13.773,50.722,15.775
                            C228.649,128.868,230.325,115.878,224.885,115.391z"/>
                        </g>
                        <path style="fill:#FFE67B;" d="M207.747,74.47c1.446,2.847-7.382,2.451-15.844,6.746c-8.461,4.295-13.351,11.656-14.797,8.808
                          c-1.445-2.848,1.998-13.057,10.459-17.352C196.027,68.377,206.302,71.623,207.747,74.47z"/>
                        <path style="opacity:0.5;fill:#1C96D3;" d="M225.001,88.747c0,0,6.592,14.676,2.072,31.131
                          c-17.151-6.313-34.207-19.201-34.4-28.881C192.426,78.679,216.062,82.128,225.001,88.747z"/>
                      </g>
                    </g>
                    <g>
                      <g>
                        <path style="fill:#FED09E;" d="M161.973,103.081c-2.003,11.254-11.477,18.98-21.162,17.257
                          c-9.684-1.724-15.912-12.244-13.909-23.498c2.003-11.254,11.477-18.98,21.161-17.257
                          C157.748,81.307,163.976,91.827,161.973,103.081z"/>
                        <g>
                          <path style="fill:#FED09E;" d="M195.44,312.354c0.053,6.244,6.601,11.987,0.703,11.627l-5.663,0.026
                            c-5.898-0.36-6.119-2.736-5.789-8.943c2.018-37.948-9.819-45.258-8.197-62.708c1.025-11.028,4.163-12.896,3.433-15.071
                            l4.133-8.743c5.898,0.36,10.722,5.714,10.775,11.958L195.44,312.354z"/>
                          <polygon style="fill:#FED09E;" points="128.877,136.858 114.605,130.774 130.414,101.538 143.792,107.806 					"/>
                          <path style="fill:#FED09E;" d="M138.287,213.144c-4.996-1.301-9.83-2.246-14.396-2.881
                            c-14.361-23.546,14.521-36.801,8.876-49.825c-9.983-23.033-3.663-24.104-12.623-39.857
                            c-15.041,2.575-14.112,16.175-17.295,49.101c-1.807,18.691-14.752,42.515-10.125,55.768
                            c2.879,8.243,20.491,10.843,44.826,16.665c24.262,5.804,43.062-0.603,44.71-1.504c13.189-7.209,12.626,5.973,11.699-4.563
                            C193.201,227.434,162.541,219.461,138.287,213.144z"/>
                          <path style="fill:#FFDD50;" d="M121.556,117.919c-15.952,3.671-22.675,20.803-22.675,54.218c0,7.65-1.355,13.213-3.049,16.939
                            c16.939,7.115,27.78,2.441,27.78,2.441c0.733-9.848,7.005-17.676,11.631-21.257
                            C152.798,156.669,139.772,153.589,121.556,117.919z"/>
                          <path style="fill:#F2CD30;" d="M132.823,173.849c2.426-1.878,6.669-7.141,7.994-8.732l-11.805-29.974l-0.305-0.883
                            c0.559,1.187-2.087-8.145-8.562-8.145c-1.631,0-3.002,0.276-4.486,0.975c-2.668,1.256-4.026,3.192-5.022,5.964
                            c-0.996,2.77,1.499,13.911,2.756,16.572l5.052,12.695C127.253,179.16,130.253,175.839,132.823,173.849z"/>
                          <path style="fill:#FED09E;" d="M180.867,189.415l-39.299-17.956l-13.944-40.332c-2.063-4.375-7.284-6.25-11.663-4.189
                            c-4.378,2.061-6.256,7.278-4.193,11.653l18.477,39.186c0.545,1.156,1.319,2.123,2.231,2.903
                            c0.852,1.081,1.937,1.999,3.2,2.598l45.352,13.157c8.556,1.771,7.148,4.791,9.556,1.771
                            C193.684,194.421,198.653,185.096,180.867,189.415z"/>
                          <g>
                            <g>
                              <path style="fill:#EFBB86;" d="M139.119,240.166c-23.11-5.562-40.53-8.502-46.435-14.875
                                c0.017,0.051,0.023,0.108,0.041,0.159c2.879,8.243,20.491,10.843,44.826,16.665c21.338,5.105,38.439,0.767,43.375-0.966
                                C172.848,242.856,157.494,244.588,139.119,240.166z"/>
                            </g>
                            <path style="fill:#A94EEA;" d="M128.092,229.157c0.182-1.659-7.187-5.38-6.966-6.613c0.325-1.814,7.942,1.095,8.39-1.499
                              c0.595-3.451,0.557-4.2,2.044-9.655c-2.646-0.658-6.498-0.964-7.669-1.127c-0.263-0.431-2.225-4.507-2.459-4.931
                              c-2.538,1.051-11.051,5.09-29.04,6.683c-0.852,5.081-0.975,9.689,0.333,13.435c2.166,6.203,11.002,9.605,33.954,14.141
                              C126.757,238.064,127.644,233.232,128.092,229.157z"/>
                            <g>
                              <path style="fill:#8D3DD3;" d="M126.979,235.441c-0.023-0.03-0.034-0.057-0.057-0.087c-0.029,0.26-0.052,0.495-0.061,0.672
                                c-22.952-4.536-31.788-7.937-33.954-14.141c-0.678-1.941-0.965-4.118-0.972-6.469c-0.372,3.737-0.22,7.143,0.789,10.033
                                c2.166,6.204,11.002,9.605,33.954,14.141c0.037-0.717,0.255-2.177,0.519-3.934
                                C127.122,235.59,127.044,235.527,126.979,235.441z"/>
                            </g>
                          </g>
                          <g>
                            <path style="fill:#DAE9EE;" d="M218.05,326.476c6.072-8.624-9.841-3.535-22.543-15.109c0,0-4.409,1.639-10.684,2.63
                              c0,0-3.031,11.495,0.533,12.945c0.482,1.406,1.003,1.798,2.205,1.885C187.56,328.826,207.972,331.736,218.05,326.476z"/>
                          </g>
                          <path style="fill:#EFBB86;" d="M128.185,113.168c0.487,5.338,2.07,13.113,4.387,16.198l4.434-8.2
                            C134.638,119.16,128.185,113.168,128.185,113.168z"/>
                          <path style="fill:#553421;" d="M121.613,108.013c0,0-29.298,23.991-39.61,10.479c3.1,11.11,19.179,16.316,24.889,10.132
                            c5.023-5.44,7.826-8.728,15.001-10.05c12.839-3.398,17.897-10.807,18.151-12.839
                            C140.298,103.703,121.613,108.013,121.613,108.013z"/>
                          <g>
                            <path style="fill:#E24BE2;" d="M155.034,113.133c-4.471-2.002-8.07-7.293-8.038-11.818l0.041-5.735
                              c0.032-4.525,3.683-6.57,8.154-4.568l8.838,3.957c-0.114-0.953-0.261-1.888-0.448-2.792
                              c-2.776-13.431-17.543-20.684-28.82-18.353c-11.277,2.331-23.068,18.94-17.559,36.321
                              c1.443,4.553,24.242,13.284,40.136,16.011c2.915,0.5,8.789-9.371,4.277-10.076L155.034,113.133z"/>
                            <path style="fill:#C62D14;" d="M144.108,91.656c0.736,1.844-0.161,3.936-2.005,4.672c-1.844,0.736-3.936-0.161-4.672-2.005
                              c-0.736-1.844,0.161-3.936,2.005-4.672C141.28,88.914,143.372,89.812,144.108,91.656z"/>
                            <g>
                              <path style="fill:#C030C4;" d="M161.615,116.079l-0.157-0.07c-1.042,2.91-3.773,6.212-5.49,5.918
                                c-14.886-2.554-35.829-10.374-39.61-15.097c0.215,1.099,0.493,2.205,0.844,3.314c1.443,4.553,24.242,13.284,40.136,16.011
                                C160.253,126.655,166.126,116.784,161.615,116.079z"/>
                            </g>
                            <path style="fill:#F562F9;" d="M150.425,78.964c1.06,2.654-6.777,1.592-14.663,4.741c-7.886,3.149-12.835,9.317-13.895,6.663
                              c-1.06-2.654,2.829-11.477,10.715-14.626C140.468,72.593,149.365,76.31,150.425,78.964z"/>
                            <path style="opacity:0.5;fill:#1C96D3;" d="M164.518,92.907c0,0,4.698,13.609-0.651,27.913
                              c-14.78-7.002-28.947-19.858-28.343-28.501C136.293,81.319,157.082,86.29,164.518,92.907z"/>
                          </g>
                        </g>
                      </g>
                    </g>
                    <path style="fill:#06050B;" d="M184.923,326.942c0.493,1.076,1.198,1.811,2.233,1.885c0,0,20.672,2.91,30.879-2.35
                      c0.643-0.901,1.029-1.646,1.215-2.282C208.835,329.545,188.871,327.427,184.923,326.942z"/>
                  </g>
                </g>
                </svg>
                  Ride Hailing Application
                </h3>
                <div class="bell-container">
                  <button class="bell-btn" @click="notifOpen = !notifOpen" title="Notifications">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
                    <span v-if="unreadNotifCount > 0" class="bell-badge">{{ unreadNotifCount }}</span>
                  </button>
                  <Transition name="notif-fade">
                    <div v-if="notifOpen" class="notif-dropdown glass">
                      <div class="notif-header">
                        <span>Notifications</span>
                        <button class="notif-clear-btn" v-if="notifications.length > 0" @click="clearNotifications">Clear All</button>
                      </div>
                      <div class="notif-list">
                        <div v-if="notifications.length === 0" class="notif-empty">
                          🔔 No new notifications
                        </div>
                        <div v-else v-for="n in notifications" :key="n.id" class="notif-item" @click="clickNotification(n)">
                          <div class="notif-dot" v-if="!n.read"></div>
                          <div class="notif-body">
                            <div class="notif-text">{{ n.text }}</div>
                            <div class="notif-time">{{ n.time }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Transition>
                </div>
              </div>
              <div class="auto-accept-row">
                <span class="aa-label">Auto Accept Rides</span>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="autoAccept" @change="toggleAutoAccept" />
                  <span class="toggle-slider"></span>
                </label>
              </div>
              <button 
                class="btn-drive" 
                :disabled="!user?.is_activated"
                :title="!user?.is_activated ? 'Your account is pending activation. Please go to the office to activate.' : ''"
                @click="$router.push('/driver')"
              >
                <span style="position: relative; z-index: 2; display: inline-flex; align-items: center; gap: 8px; justify-content: center; width: 100%;">
                  <svg version="1.1" id="layer-btn" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 450 450" style="enable-background:new 0 0 450 450; display: inline-block; vertical-align: middle;" xml:space="preserve" width="22" height="22">
                    <g>
                      <ellipse style="opacity:0.3;fill:#878787;" cx="227" cy="387.372" rx="169.655" ry="9.332"/>
                      <g>
                        <g>
                          <g>
                            <g>
                              <g>
                                <g>
                                  <path style="fill:#06050B;" d="M306.608,344.848c0,17.609,14.275,31.884,31.884,31.884c17.609,0,31.884-14.275,31.884-31.884 s-14.275-31.884-31.884-31.884C320.883,312.964,306.608,327.239,306.608,344.848z M309.75,347.246 c-0.065-0.793-0.121-1.589-0.121-2.399c0-1.14,0.083-2.259,0.212-3.364h17.878l2.882,2.882l-2.882,2.882H309.75z M325.19,349.775l-10.851,10.851c-2.112-3.226-3.579-6.901-4.26-10.85L325.19,349.775z M310.235,338.955 c0.793-3.822,2.348-7.361,4.489-10.466l10.466,10.466H310.235z M320.364,322.402l12.477,12.477v4.075h-4.075l-12.509-12.509 C317.486,324.963,318.866,323.613,320.364,322.402z M332.841,331.304l-10.426-10.426c3.102-2.084,6.63-3.578,10.426-4.332 V331.304z M338.492,315.984c0.892,0,1.77,0.054,2.641,0.133v17.714l-2.882,2.882l-2.882-2.881v-17.673 C336.396,316.049,337.436,315.984,338.492,315.984z M332.841,373.15c-4.031-0.801-7.748-2.451-10.984-4.74l10.984-10.984 V373.15z M343.661,357.426l11.19,11.19c-3.298,2.275-7.094,3.866-11.19,4.608V357.426z M354.27,320.695l-10.609,10.609 v-14.832C347.52,317.171,351.109,318.626,354.27,320.695z M360.497,326.194l-12.691,12.691 c-0.027,0.027-0.058,0.045-0.085,0.07h-3.904c-0.027-0.025-0.059-0.043-0.086-0.07c-0.027-0.026-0.044-0.058-0.07-0.085 v-3.904c0.025-0.027,0.043-0.059,0.07-0.085l12.614-12.614C357.858,323.39,359.251,324.725,360.497,326.194z M348.883,347.246c-0.038,0-0.072-0.01-0.11-0.011l-2.761-2.761c-0.001-0.037-0.011-0.072-0.011-0.11 c0-0.037,0.01-0.073,0.011-0.11l2.761-2.761c0.037-0.002,0.072-0.011,0.11-0.011l18.261,0 c0.129,1.105,0.212,2.225,0.212,3.365c0,0.81-0.056,1.606-0.121,2.399H348.883z M366.905,349.775 c-0.701,4.069-2.227,7.855-4.442,11.15l-11.15-11.15H366.905z M351.313,338.955l10.742-10.742 c2.244,3.172,3.878,6.803,4.695,10.742L351.313,338.955z M356.894,367.082l-13.162-13.162 c-0.027-0.027-0.044-0.058-0.07-0.086v-3.904c0.025-0.027,0.043-0.059,0.07-0.086c0.027-0.026,0.058-0.044,0.085-0.07h3.904 c0.027,0.025,0.059,0.043,0.085,0.07l13.131,13.131C359.727,364.474,358.377,365.854,356.894,367.082z M338.492,373.711 c-1.056,0-2.096-0.065-3.122-0.175v-18.54c0-0.038,0.01-0.073,0.011-0.11l2.761-2.761c0.037-0.001,0.072-0.011,0.11-0.011 c0.038,0,0.072,0.01,0.11,0.011l2.761,2.761c0.001,0.037,0.011,0.072,0.011,0.11v18.582 C340.262,373.657,339.384,373.711,338.492,373.711z M315.841,362.7l12.926-12.925h4.075v4.075l-13.003,13.003 C318.37,365.607,317.035,364.213,315.841,362.7z"/>
                                  <path style="fill:#2D2A33;" d="M292.74,344.848c0,25.268,20.484,45.752,45.752,45.752c25.268,0,45.752-20.484,45.752-45.752 c0-25.268-20.484-45.753-45.752-45.753C313.224,299.095,292.74,319.579,292.74,344.848z M307.557,344.848 c0-17.085,13.85-30.935,30.935-30.935c17.085,0,30.935,13.85,30.935,30.935c0,17.085-13.85,30.935-30.935,30.935 C321.407,375.783,307.557,361.932,307.557,344.848z"/>
                                </g>
                                <circle style="fill:#06050B;" cx="338.492" cy="344.848" r="15.071"/>
                              </g>
                              <path style="fill:#1C1A21;" d="M328.766,305.062c0.266,0.601-0.046,1.323-0.698,1.612l-12.396,5.493 c-0.652,0.289-1.397,0.036-1.663-0.565l-12.786-28.851c-0.267-0.601,0.046-1.323,0.698-1.612l12.396-5.493 c-0.652-0.289,1.397-0.036,1.663,0.565L328.766,305.062z"/>
                              <path style="fill:#2D2A33;" d="M335.246,341.674c-0.073-0.165,0.013-0.362,0.191-0.442l2.063-0.914 c0.179-0.079,0.383-0.01,0.456,0.155l3.475,7.683l1.137-0.504c0.451-0.2,0.667-0.699,0.483-1.115l-15.992-35.356 c-0.184-0.416-0.699-0.591-1.15-0.391l-5.205,2.306c-0.451,0.2-0.667,0.699-0.483,1.115l15.992,35.356 c0.184,0.416,0.699,0.591,1.15,0.391l1.359-0.602L335.246,341.674z"/>
                            </g>
                            <path style="fill:#8E1400;" d="M342.667,272.469c3.591,1.14,6.836,2.314,9.772,3.56c14.095,5.982,20.811,13.573,22.755,20.488 c1.105,3.93-1.424,5.516-5.298,3.75c-3.803-1.733-10.312-3.685-21.565-4.133c-8.327-0.331-18.816,0.103-31.967,1.28 C321.616,285.6,331.132,276.826,342.667,272.469z"/>
                            <path style="fill:#DAE9EE;" d="M317.826,294.396c13.265-0.787,23.655-0.882,31.842-0.255 c11.759,0.902,18.352,3.396,22.141,5.526c0.981,0.551,1.862,0.836,2.616,0.904c-0.956,0.623-2.554,0.595-4.529-0.305 c-3.803-1.733-10.312-3.685-21.565-4.133c-8.327-0.331-18.816,0.103-31.967,1.28 C316.817,296.393,317.297,295.386,317.826,294.396z"/>
                            <path style="fill:#C62D14;" d="M348.745,275.926c1.278,0.447,2.503,0.894,3.682,1.366c13.332,5.337,19.872,12.482,21.786,19.091 c0.253,0.873,0.316,1.595,0.24,2.189c-2.776-4.169-7.917-8.121-16.554-11.096C354.192,284.167,350.735,280.205,348.745,275.926z "/>
                            <path style="fill:#1C1A21;" d="M122.87,293.922c-0.267,0.601,0.046,1.323,0.698,1.612l12.396,5.493 c0.652,0.289,1.397,0.036,1.663-0.565l12.786-28.85c0.266-0.601-0.046-1.323-0.698-1.612l-12.396-5.493 c-0.652-0.289-1.396-0.036-1.663,0.565L122.87,293.922z"/>
                            <g>
                              <path style="fill:#26232B;" d="M157.036,342.75c3.135,8.065,12.493,14.603,20.903,14.603l52.142,0 c8.41,0,14.554-6.538,11.419-14.603l-23.637-10.776c-3.135-8.065-0.357-28.608-8.766-28.608h-52.141 c-8.41,0-12.686,6.538-9.551,14.603L157.036,342.75z"/>
                              <path style="fill:#1C1A21;" d="M174.972,349.719h52.141c8.41,0,14.554-6.538,11.419-14.603l2.967,7.633 c3.135,8.065-3.009,14.603-11.419,14.603l-52.142,0c-8.41,0-17.768-6.538-20.903-14.603l-2.967-7.633 C157.203,343.181,166.562,349.719,174.972,349.719z"/>
                            </g>
                            <path style="fill:#8E1400;" d="M267.698,222.154c0,0,19.841,0,29.993,9.69c10.152,9.69,35.53,29.993,24.917,31.377 c-10.613,1.384-16.15,4.614-21.687,14.766s-17.073,16.611-13.382,23.533c3.691,6.922,9.981,11.661,1.214,20.428 c-8.767,8.767-9.519,20.178-20.594,19.716c-11.074-0.461-93.208-11.536-94.131-12.92c-0.923-1.384,48.213-2.768,52.366-2.768 c14.08,0,42.688,0.922,50.071-24.457c7.383-25.379,8.306-25.379,2.307-38.76C272.774,249.378,258.469,223.077,267.698,222.154z" />
                            <path style="fill:#AD2202;" d="M325.451,297.134c6.011-1.472,22.788-9.036,18.559-10.399 c-4.228-1.363-28.157-13.052-43.521-14.869c-28.177,35.192-6.847,31.858-13.873,47.651 c-3.514,7.899-20.303,12.689-68.135,12.294c-12.448-0.103-8.01,25.082-6.616,25.082c68.753,0,74.286-2.673,77.059-19.38 C291.551,321.681,303.007,302.631,325.451,297.134z"/>
                            <path style="fill:#8E1400;" d="M137.167,263.589c-5.866-0.205-11.236-0.215-16.182,0.001 c-23.748,1.034-37.333,7.315-43.524,14.893c-3.519,4.307-0.531,7.368,6.055,6.935c6.464-0.425,17.043,0.087,33.93,4.545 c12.496,3.299,27.829,8.494,46.752,15.781C162.07,288.984,152.172,274.039,137.167,263.589z"/>
                            <path style="fill:#DAE9EE;" d="M163.474,301.409c-19.278-6.861-34.626-11.598-47.056-14.473 c-17.855-4.129-28.817-4.016-35.451-3.101c-1.718,0.237-3.159,0.192-4.309-0.059c1.119,1.186,3.499,1.862,6.857,1.642 c6.464-0.425,17.043,0.087,33.93,4.545c12.496,3.299,27.829,8.494,46.752,15.781 C164.014,304.296,163.784,302.854,163.474,301.409z"/>
                            <path style="fill:#AD2202;" d="M126.505,265.107c-2.107-0.023-4.137-0.022-6.109,0.03c-22.309,0.587-35.419,6.401-41.421,13.62 c-0.793,0.954-1.231,1.807-1.403,2.566c6.11-3.855,15.619-6.394,29.84-6.185C114.49,272.746,121.509,269.447,126.505,265.107z"/>
                            <path style="fill:#8E1400;" d="M285.463,334.397c2.627-15.83,14.084-34.88,36.527-40.378c3.308-0.81,13.846-4.198,21.953-7.308 c0.02,0.007,0.048,0.017,0.067,0.023c4.229,1.363-12.548,8.927-18.559,10.399c-22.443,5.497-33.9,24.548-36.527,40.378 c-2.737,16.491-0.928,19.84-45.476,19.84c-0.713,0-30.699,0.002-31.425,0.002c-0.306,0-0.918-1.68-1.307-3.577 C277.273,353.714,282.722,350.914,285.463,334.397z"/>
                            <path style="fill:#AD2202;" d="M164.887,331.768v-13.965c0-16.731-9.581-31.215-23.55-38.293h42.144 c23.7,0,42.913,19.213,42.913,42.913v9.344H164.887z"/>
                            <path style="fill:#C62D14;" d="M211.712,271.157c3.148,2.055-2.159,14.575-7.288,14.575c-5.128,0-40.486,0-49.663,0 c-9.177,0-76.384-39.677-76.384-48.314C78.377,228.781,146.394,228.511,211.712,271.157z"/>
                            <g>
                              <g>
                                <path style="fill:#06050B;" d="M75.894,344.847c0,17.609,14.275,31.884,31.884,31.884c17.609,0,31.884-14.275,31.884-31.884 c0-17.609-14.275-31.884-31.884-31.884C90.169,312.963,75.894,327.238,75.894,344.847z M79.036,347.246 c-0.065-0.793-0.121-1.589-0.121-2.399c0-1.14,0.084-2.259,0.212-3.364h17.878l2.882,2.881l-2.882,2.882L79.036,347.246z M94.476,349.775l-10.851,10.851c-2.112-3.226-3.579-6.901-4.26-10.85L94.476,349.775z M79.52,338.955 c0.793-3.822,2.348-7.361,4.489-10.466l10.466,10.466H79.52z M89.649,322.402l12.477,12.477v4.075h-4.075l-12.509-12.509 C86.772,324.963,88.152,323.613,89.649,322.402z M102.127,331.304L91.7,320.877c3.102-2.085,6.63-3.578,10.427-4.332V331.304z M107.778,315.984c0.892,0,1.77,0.054,2.641,0.133v17.714l-2.881,2.882l-2.882-2.882v-17.673 C105.682,316.049,106.722,315.984,107.778,315.984z M102.127,373.15c-4.031-0.8-7.748-2.451-10.984-4.74l10.984-10.984V373.15 z M112.947,357.426l11.19,11.19c-3.298,2.275-7.094,3.866-11.19,4.607V357.426z M123.556,320.695l-10.609,10.609l0-14.832 C116.805,317.171,120.395,318.626,123.556,320.695z M129.783,326.194l-12.691,12.691c-0.026,0.026-0.058,0.044-0.086,0.07 h-3.904c-0.027-0.025-0.059-0.043-0.085-0.07c-0.027-0.027-0.045-0.058-0.07-0.085v-3.905c0.025-0.027,0.043-0.059,0.07-0.085 l12.613-12.614C127.143,323.39,128.537,324.725,129.783,326.194z M118.168,347.246c-0.037,0-0.072-0.01-0.11-0.011 l-2.761-2.761c-0.001-0.037-0.011-0.072-0.011-0.11c0-0.038,0.01-0.073,0.011-0.11l2.761-2.761 c0.037-0.001,0.072-0.011,0.11-0.011h18.261c0.129,1.105,0.212,2.224,0.212,3.364c0,0.81-0.056,1.606-0.121,2.399 L118.168,347.246z M136.191,349.775c-0.701,4.069-2.227,7.855-4.442,11.151l-11.15-11.151H136.191z M120.598,338.955 l10.742-10.742c2.244,3.172,3.878,6.804,4.695,10.742L120.598,338.955z M126.179,367.082l-13.162-13.162 c-0.027-0.027-0.045-0.058-0.07-0.086v-3.904c0.025-0.027,0.043-0.059,0.07-0.085c0.026-0.027,0.058-0.045,0.085-0.07h3.904 c0.027,0.025,0.059,0.043,0.085,0.07l13.131,13.131C129.012,364.474,127.662,365.853,126.179,367.082z M107.778,373.711 c-1.056,0-2.096-0.065-3.122-0.175v-18.54c0-0.038,0.01-0.073,0.011-0.11l2.761-2.761c0.037-0.002,0.072-0.011,0.11-0.011 c0.037,0,0.072,0.01,0.11,0.011l2.761,2.761c0.002,0.037,0.011,0.072,0.011,0.11v18.582 C109.548,373.657,108.669,373.711,107.778,373.711z M85.126,362.7l12.925-12.926h4.075v4.075l-13.003,13.003 C87.655,365.607,86.32,364.213,85.126,362.7z"/>
                            <path style="fill:#2D2A33;" d="M62.025,344.848c0,25.268,20.484,45.752,45.752,45.752c25.269,0,45.753-20.484,45.753-45.752 c0-25.268-20.484-45.752-45.752-45.752C82.509,299.095,62.025,319.579,62.025,344.848z M76.843,344.847 c0-17.085,13.85-30.935,30.935-30.935c17.085,0,30.935,13.85,30.935,30.935c0,17.085-13.85,30.935-30.935,30.935 C90.693,375.783,76.843,361.932,76.843,344.847z"/>
                          </g>
                          <ellipse transform="matrix(0.9817 -0.1904 0.1904 0.9817 -63.6957 26.8338)" style="fill:#06050B;" cx="107.778" cy="344.848" rx="15.071" ry="15.071"/>
                        </g>
                        <path style="fill:#AD2202;" d="M211.712,271.157c1.958,1.278,0.644,6.601-1.862,10.446c-19.268-1.593-43.014-8.85-56.785-15.033 c-25.967-11.659-48.675-24.48-61.317-30.343c-2.083-0.966-3.761-1.911-5.05-2.816 C106.779,230.555,160.084,237.449,211.712,271.157z"/>
                        <path style="fill:#C62D14;" d="M153.756,331.02c0,3.895,3.158,7.053,7.053,7.053h62.212c3.895,0,7.053-3.158,7.053-7.053l0,0 c0-3.895-3.158-7.053-7.053-7.053h-62.212C156.914,323.967,153.756,327.125,153.756,331.02L153.756,331.02z"/>
                        <path style="fill:#8E1400;" d="M160.809,334.095h62.212c3.2,0,5.87-2.144,6.733-5.064c0.188,0.635,0.32,1.294,0.32,1.989 c0,3.895-3.158,7.053-7.053,7.053h-62.212c-3.895,0-7.053-3.158-7.053-7.053c0-0.696,0.132-1.355,0.32-1.99 C154.939,331.95,157.61,334.095,160.809,334.095z"/>
                        <g>
                          <path style="fill:#423F4C;" d="M206.584,244.436c11.536,0,23.738,4.481,23.738,21.554c0,22.535-53.491,9.057-76.101-1.094 c-22.61-10.151-42.382-21.315-53.39-26.421c-10.956-5.081-9.302-9.498,5.003-9.498 C141.806,228.977,166.367,244.436,206.584,244.436z"/>
                          <path style="fill:#595666;" d="M223.501,268.143c0.284-16.086-11.658-20.393-23.018-20.473 c-39.604-0.281-63.535-15.016-98.959-15.267c-1.474-0.01-2.755,0.071-3.874,0.22c0.884-1.539,3.846-2.723,9.338-2.684 c35.424,0.251,59.354,14.986,98.958,15.267c11.36,0.081,23.302,4.388,23.018,20.473c-0.067,3.805-3.081,6.127-7.899,7.348 C222.595,271.779,223.465,270.171,223.501,268.143z"/>
                          <path style="fill:#2D2A33;" d="M95.015,230.688c0.965,1.34,3.151,2.856,6.561,4.438c11.007,5.105,30.78,16.269,53.39,26.421 c20.996,9.427,68.594,21.703,75.286,5.364c-1.493,21.204-53.744,7.991-76.03-2.015c-22.61-10.151-42.382-21.315-53.39-26.421 C94.04,235.325,92.106,232.433,95.015,230.688z"/>
                        </g>
                        <g>
                          <path style="fill:#C62D14;" d="M355.548,275.185c1.816,2.738-7.203,14.575-11.432,13.212 c-4.228-1.363-36.06-14.094-43.627-16.533c0,0-45.361-55.337-42.084-63.328C261.681,200.545,317.867,218.37,355.548,275.185z" />
                          <path style="fill:#E8321F;" d="M348.3,285.617c-25.905-39.787-58.761-66.377-77.833-75.46 c15.126,1.834,54.682,23.092,83.559,66.63c0.131,0.335-0.179,1.947-1.958,4.558C350.934,283.009,349.578,284.517,348.3,285.617 z"/>
                          <path style="fill:#2D2A33;" d="M249.007,200.159c0,5.881,4.767,10.648,10.648,10.648h14.994c5.88,0,10.648-4.767,10.648-10.648 l0,0c0-5.881-4.767-10.648-10.648-10.648h-14.994C253.774,189.512,249.007,194.279,249.007,200.159L249.007,200.159z"/>
                          <path style="fill:#C62D14;" d="M268.347,181.037c-4.346,3.694-25.207,28.684,28.901,24.338 C296.161,193.206,268.347,181.037,268.347,181.037z"/>
                          <path style="fill:#423F4C;" d="M259.512,200.997c0.961,1.932,0.248,3.855-1.593,4.296l-13.282,3.018 c-1.841,0.441-4.112-0.768-5.074-2.7l0,0c-0.961-1.932-0.248-3.855,1.593-4.296l13.282-3.018 C256.28,197.857,258.551,199.066,259.512,200.997L259.512,200.997z"/>
                          <path style="fill:#2D2A33;" d="M245.083,204.109c0.662,1.33,0.171,2.655-1.097,2.958l-0.153,0.026 c-1.268,0.303-2.832-0.529-3.494-1.859l0,0c-0.662-1.331-0.171-2.655,1.097-2.959l0.153-0.026 C242.857,201.946,244.421,202.778,244.083,204.109L245.083,204.109z"/>
                          <g>
                            <path style="fill:#E8321F;" d="M270.635,182.691c5.39,2.546,24.296,12.134,25.153,21.729 c-3.591,0.288-6.812,0.432-9.717,0.457C283.762,198.024,276.489,189.112,270.635,182.691z"/>
                          </g>
                        </g>
                        <g>
                          <path style="fill:#2D2A33;" d="M111.251,342.963c0.073-0.165-0.013-0.363-0.191-0.442l-2.062-0.914 c-0.179-0.079-0.383-0.01-0.456,0.155l-3.475,7.683l-1.137-0.504c-0.451-0.2-0.667-0.699-0.483-1.115l15.992-35.356 c0.184-0.416,0.699-0.591-1.15-0.391l5.205,2.307c0.451,0.2,0.667,0.699,0.483,1.115l-15.992,35.356 c-0.184,0.416-0.699,0.591-1.15,0.391l-1.359-0.602L111.251,342.963z"/>
                          <path style="fill:#DAE9EE;" d="M113.799,321.162l11.098-25.04l9.888,4.382l-11.097,25.04c-0.266,0.601-1.011,0.854-1.663,0.565 l-7.526-3.335C113.845,322.485,113.533,321.763,113.799,321.162z"/>
                        </g>
                        <path style="fill:#8E1400;" d="M351.137,274.525c0,3.089-13.749-2.437-20.176-4.441c-6.33-1.974-2.545-7.551-0.593-14.474 c0.788-2.796,4.649-1.358,10.385,3.865C346.488,264.698,351.137,271.436,351.137,274.525z"/>
                        <path style="fill:#DAE9EE;" d="M338.907,261.782c4.977,4.533,9.132,10.203,10.144,13.642c-4.091-0.262-13.204-3.817-18.09-5.341 c-6.046-1.885-2.867-7.062-0.869-13.555C331.869,256.369,334.938,258.168,338.907,261.782z"/>
                        <path style="fill:#DAE9EE;" d="M327.048,307.126l5.65,12.747c0.266,0.601-0.046,1.323-0.698,1.612l-7.526,3.335 c-0.652,0.289-1.397,0.036-1.663-0.565l-5.65-12.747L327.048,307.126z"/>
                      </g>
                    </g>
                    <g>
                      <path style="fill:#FED09E;" d="M220.366,100.024c-1.89,13.723-13.057,23.132-24.942,21.017 c-11.885-2.115-19.986-14.954-18.096-28.676c1.89-13.723,13.057-23.132,24.942-21.017 C214.155,73.462,222.257,86.301,220.366,100.024z"/>
                      <g>
                        <path style="fill:#FED09E;" d="M254.551,307.698c-0.162,6.119-5.24,11.132-11.343,11.196l0,0 c-6.103,0.064-3.546-5.294-3.321-11.414c1.156-31.37-11.21-37.099-7.415-62.38c0.913-6.08,7.078-18.722,13.18-18.786l0,0 c6.103-0.064,10.92,4.845,10.758,10.964L254.551,307.698z"/>
                        <rect x="172.86" y="114.073" transform="matrix(0.4754 -0.8798 0.8798 0.4754 -9.3974 231.0904)" style="fill:#FED09E;" width="32.414" height="18.703"/>
                        <path style="fill:#5CAD0E;" d="M198.269,214.484c-5.171-0.92-10.174-1.503-14.899-1.803 c2.911-15.555,10.678-26.534,13.072-39.984c4.658-26.173-7.237-37.224-16.532-51.999c-15.558,3.58-16.922,22.411-20.164,54.838 c-1.841,18.408-10.005,42.473-8.599,54.197c1.001,8.349,4.762,14.731,41.786,14.731c8.211,0,38.522,1.584,40.226,0.586 c13.635-7.981,22.471-10.553,22.746-12.094C257.379,224.677,223.373,218.951,198.269,214.484z"/>
                        <path style="fill:#417703;" d="M198.533,241.1c-33.272,0-44.23-7.714-45.543-16.303c-0.524-3.425-1.013-12.011-1.536-17.512 c0.363,8.701-0.894,17.554-0.307,22.449c1.001,8.349,7.16,14.73,41.786,14.731c7.688,0,34.727,1.56,39.559,0.763 C221.109,244.375,204.662,241.1,198.533,241.1z"/>
                        <path style="fill:#178FCE;" d="M185.257,212.815c3.157-14.572,8.89-27.217,11.185-40.117 c4.658-26.173-7.237-37.224-16.532-51.999c-15.558,3.58-27.251,18.472-25.28,51.001c1.279,21.102-3.512,34.697-3.802,47.72 C151.568,219.459,177.036,215.749,185.257,212.815z"/>
                        <path style="fill:#0E72AD;" d="M184.406,131.265c-0.329,0.076-14.19,8.279-14.511,8.363 c-12.067,5.854,9.942,44.108,11.574,47.047c1.788,3.22,5.547,6.111,8.798,7.859c2.322-7.473,4.662-14.646,6.175-21.837 C199.546,157.937,193.701,146.04,184.406,131.265z"/>
                        <path style="fill:#FED09E;" d="M237.378,193.621l-35.026-19.289l-16.523-40.751c-2.011-4.266-7.104-6.095-11.374-4.085 c-4.27,2.01-12.99,10.002-6.395,21.102l19.771,33.014c0.532,1.127,1.287,2.07,2.176,2.831c0.83,1.054,1.889,1.95,3.2,2.534 l45.905,13.318c8.88-6.934,8.425,8.425,15.095,1.886C257.579,200.874,254.724,189.408,237.378,193.621z"/>
                        <g>
                          <path style="fill:#FF3600;" d="M277.077,323.111c6.601-8.619-10.949-9.033-22.525-15.413c0,0-7.257,4.863-15.211,3.493 c0,0-5.426,16.702-0.457,16.891C238.883,328.082,266.443,328.566,277.077,323.111z"/>
                          <path style="fill:#06050B;" d="M277.97,320.651c-11.18,5.736-40.155,5.227-40.155,5.227c-0.581-0.022-1.036-0.22-1.412-0.518 c0.288,1.539,1.002,2.666,2.481,2.722c0,0,27.559,0.484,38.193-4.971c0.957-1.25,1.387-2.294,1.409-3.194 C278.331,320.155,278.164,320.398,277.97,320.651z"/>
                        </g>
                        <path style="fill:#75CE17;" d="M204.319,216.157c-7.196-1.231-14.037-2.231-20.172-2.976 c-4.363,1.363-11.944,2.849-18.783,4.029c22.452-0.956,49.371,0.245,84.718,11.637 C250.529,226.238,230.04,220.557,204.319,216.157z"/>
                        <path style="fill:#EFBB86;" d="M188.085,119.679c0.475,5.206,3.218,12.084,5.478,15.093l6.432-11.266 C196.974,122.51,192.55,121.819,188.085,119.679z"/>
                        <path style="fill:#FFDD50;" d="M216.3,112.036c-5.177-1.78-9.712-7.308-10.13-12.347l-0.529-6.387 c-0.418-5.039,3.44-7.681,8.617-5.901l10.233,3.519c-0.223-1.049-0.479-2.075-0.778-3.063 c-4.436-14.671-21.597-21.263-33.915-17.538c-12.318,3.724-23.776,23.391-15.904,42.183 c2.063,4.923,33.975,14.244,51.937,15.686c3.295,0.264,3.18-13.198-1.912-13.53L216.3,112.036z"/>
                        <path style="fill:#F2CD30;" d="M201.988,89.228c1.004,1.978,0.215,4.397-1.764,5.401c-1.978,1.004-4.397,0.215-5.401-1.764 c-1.004-1.979-0.215-4.397,1.764-5.401C198.565,86.46,200.984,87.25,201.988,89.228z"/>
                        <g>
                          <path style="fill:#F2CD30;" d="M224.885,115.391l-0.506-0.17c-0.522,3.497,0.21,8.633-1.868,8.416 c-18.004-1.875-44.342-9.48-49.888-14.741c0.514,1.275,1.103,2.553,1.778,3.83c2.775,5.24,31.5,13.773,50.722,15.775 C228.649,128.868,230.325,115.878,224.885,115.391z"/>
                        </g>
                        <path style="fill:#FFE67B;" d="M207.747,74.47c1.446,2.847-7.382,2.451-15.844,6.746c-8.461,4.295-13.351,11.656-14.797,8.808 c-1.445-2.848,1.998-13.057,10.459-17.352C196.027,68.377,206.302,71.623,207.747,74.47z"/>
                        <path style="opacity:0.5;fill:#1C96D3;" d="M225.001,88.747c0,0,6.592,14.676,2.072,31.131 c-17.151-6.313-34.207-19.201-34.4-28.881C192.426,78.679,216.062,82.128,225.001,88.747z"/>
                      </g>
                    </g>
                    <g>
                      <g>
                        <path style="fill:#FED09E;" d="M161.973,103.081c-2.003,11.254-11.477,18.98-21.162,17.257 c-9.684-1.724-15.912-12.244-13.909-23.498c2.003-11.254,11.477-18.98,21.161-17.257 C157.748,81.307,163.976,91.827,161.973,103.081z"/>
                        <g>
                          <path style="fill:#FED09E;" d="M195.44,312.354c0.053,6.244,6.601,11.987,0.703,11.627l-5.663,0.026 c-5.898-0.36-6.119-2.736-5.789-8.943c2.018-37.948-9.819-45.258-8.197-62.708c1.025-11.028,4.163-12.896,3.433-15.071 l4.133-8.743c5.898,0.36,10.722,5.714,10.775,11.958L195.44,312.354z"/>
                          <polygon style="fill:#FED09E;" points="128.877,136.858 114.605,130.774 130.414,101.538 143.792,107.806 					"/>
                          <path style="fill:#FED09E;" d="M138.287,213.144c-4.996-1.301-9.83-2.246-14.396-2.881 c-14.361-23.546,14.521-36.801,8.876-49.825c-9.983-23.033-3.663-24.104-12.623-39.857 c-15.041,2.575-14.112,16.175-17.295,49.101c-1.807,18.691-14.752,42.515-10.125,55.768 c2.879,8.243,20.491,10.843,44.826,16.665c24.262,5.804,43.062-0.603,44.71-1.504c13.189-7.209,12.626,5.973,11.699-4.563 C193.201,227.434,162.541,219.461,138.287,213.144z"/>
                          <path style="fill:#FFDD50;" d="M121.556,117.919c-15.952,3.671-22.675,20.803-22.675,54.218c0,7.65-1.355,13.213-3.049,16.939 c16.939,7.115,27.78,2.441,27.78,2.441c0.733-9.848,7.005-17.676,11.631-21.257 C152.798,156.669,139.772,153.589,121.556,117.919z"/>
                          <path style="fill:#F2CD30;" d="M132.823,173.849c2.426-1.878,6.669-7.141,7.994-8.732l-11.805-29.974l-0.305-0.883 c0.559,1.187-2.087-8.145-8.562-8.145c-1.631,0-3.002,0.276-4.486,0.975c-2.668,1.256-4.026,3.192-5.022,5.964 c-0.996,2.77,1.499,13.911,2.756,16.572l5.052,12.695C127.253,179.16,130.253,175.839,132.823,173.849z"/>
                          <path style="fill:#FED09E;" d="M180.867,189.415l-39.299-17.956l-13.944-40.332c-2.063-4.375-7.284-6.25-11.663-4.189 c-4.378,2.061-6.256,7.278-4.193,11.653l18.477,39.186c0.545,1.156,1.319,2.123,2.231,2.903 c0.852,1.081,1.937,1.999,3.2,2.598l45.352,13.157c8.556,1.771,7.148,4.791,9.556,1.771 C193.684,194.421,198.653,185.096,180.867,189.415z"/>
                          <g>
                            <g>
                              <path style="fill:#EFBB86;" d="M139.119,240.166c-23.11-5.562-40.53-8.502-46.435-14.875 c0.017,0.051,0.023,0.108,0.041,0.159c2.879,8.243,20.491,10.843,44.826,16.665c21.338,5.105,38.439,0.767,43.375-0.966 C172.848,242.856,157.494,244.588,139.119,240.166z"/>
                            </g>
                            <path style="fill:#A94EEA;" d="M128.092,229.157c0.182-1.659-7.187-5.38-6.966-6.613c0.325-1.814,7.942,1.095,8.39-1.499 c0.595-3.451,0.557-4.2,2.044-9.655c-2.646-0.658-6.498-0.964-7.669-1.127c-0.263-0.431-2.225-4.507-2.459-4.931 c-2.538,1.051-11.051,5.09-29.04,6.683c-0.852,5.081-0.975,9.689,0.333,13.435c2.166,6.203,11.002,9.605,33.954,14.141 C126.757,238.064,127.644,233.232,128.092,229.157z"/>
                            <g>
                              <path style="fill:#8D3DD3;" d="M126.979,235.441c-0.023-0.03-0.034-0.057-0.057-0.087c-0.029,0.26-0.052,0.495-0.061,0.672 c-22.952-4.536-31.788-7.937-33.954-14.141c-0.678-1.941-0.965-4.118-0.972-6.469c-0.372,3.737-0.22,7.143,0.789,10.033 c2.166,6.204,11.002,9.605,33.954,14.141c0.037-0.717,0.255-2.177,0.519-3.934 C127.122,235.59,127.044,235.527,126.979,235.441z"/>
                            </g>
                          </g>
                          <g>
                            <path style="fill:#DAE9EE;" d="M218.05,326.476c6.072-8.624-9.841-3.535-22.543-15.109c0,0-4.409,1.639-10.684,2.63 c0,0-3.031,11.495,0.533,12.945c0.482,1.406,1.003,1.798,2.205,1.885C187.56,328.826,207.972,331.736,218.05,326.476z"/>
                          </g>
                          <path style="fill:#EFBB86;" d="M128.185,113.168c0.487,5.338,2.07,13.113,4.387,16.198l4.434-8.2 C134.638,119.16,128.185,113.168,128.185,113.168z"/>
                          <path style="fill:#553421;" d="M121.613,108.013c0,0-29.298,23.991-39.61,10.479c3.1,11.11,19.179,16.316,24.889,10.132 c5.023-5.44,7.826-8.728,15.001-10.05c12.839-3.398,17.897-10.807,18.151-12.839 C140.298,103.703,121.613,108.013,121.613,108.013z"/>
                          <g>
                            <path style="fill:#E24BE2;" d="M155.034,113.133c-4.471-2.002-8.07-7.293-8.038-11.818l0.041-5.735 c0.032-4.525,3.683-6.57,8.154-4.568l8.838,3.957c-0.114-0.953-0.261-1.888-0.448-2.792 c-2.776-13.431-17.543-20.684-28.82-18.353c-11.277,2.331-23.068,18.94-17.559,36.321 c1.443,4.553,24.242,13.284,40.136,16.011c2.915,0.5,8.789-9.371,4.277-10.076L155.034,113.133z"/>
                            <path style="fill:#C62D14;" d="M144.108,91.656c0.736,1.844-0.161,3.936-2.005,4.672c-1.844,0.736-3.936-0.161-4.672-2.005 c-0.736-1.844,0.161-3.936,2.005-4.672C141.28,88.914,143.372,89.812,144.108,91.656z"/>
                            <g>
                              <path style="fill:#C030C4;" d="M161.615,116.079l-0.157-0.07c-1.042,2.91-3.773,6.212-5.49,5.918 c-14.886-2.554-35.829-10.374-39.61-15.097c0.215,1.099,0.493,2.205,0.844,3.314c1.443,4.553,24.242,13.284,40.136,16.011 C160.253,126.655,166.126,116.784,161.615,116.079z"/>
                            </g>
                            <path style="fill:#F562F9;" d="M150.425,78.964c1.06,2.654-6.777,1.592-14.663,4.741c-7.886,3.149-12.835,9.317-13.895,6.663 c-1.06-2.654,2.829-11.477,10.715-14.626C140.468,72.593,149.365,76.31,150.425,78.964z"/>
                            <path style="opacity:0.5;fill:#1C96D3;" d="M164.518,92.907c0,0,4.698,13.609-0.651,27.913 c-14.78-7.002-28.947-19.858-28.343-28.501C136.293,81.319,157.082,86.29,164.518,92.907z"/>
                          </g>
                        </g>
                      </g>
                    </g>
                    <path style="fill:#06050B;" d="M184.923,326.942c0.493,1.076,1.198,1.811,2.233,1.885c0,0,20.672,2.91,30.879-2.35 c0.643-0.901,1.029-1.646,1.215-2.282C208.835,329.545,188.871,327.427,184.923,326.942z"/>
                  </g>
                </g>
              </svg>
                <span style="vertical-align: middle;">{{ user?.is_activated ? 'Drive Now' : 'Pending Activation' }}</span>
              </span>
                <div class="tile-wave-container" v-if="user?.is_activated">
                  <svg class="tile-waves" xmlns="http://www.w3.org/2000/svg" viewBox="0 24 150 28" preserveAspectRatio="none">
                    <defs><path id="twave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" /></defs>
                    <g class="tile-parallax">
                      <use href="#twave" x="48" y="0" fill="rgba(46,204,113,0.22)" />
                      <use href="#twave" x="48" y="3" fill="rgba(46,204,113,0.36)" />
                      <use href="#twave" x="48" y="5" fill="rgba(46,204,113,0.52)" />
                      <use href="#twave" x="48" y="7" fill="rgba(46,204,113,0.72)" />
                    </g>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- =================== PAGE: PROFILE =================== -->
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
              <div class="pf-row">
                <span class="pf-lbl">Full Name</span>
                <span class="pf-val">{{ user?.full_name || '—' }}</span>
              </div>
              <div class="pf-row">
                <span class="pf-lbl">Username</span>
                <span class="pf-val">@{{ user?.username || '—' }}</span>
              </div>
              <div class="pf-row">
                <span class="pf-lbl">Email</span>
                <span class="pf-val">{{ user?.email || '—' }}</span>
              </div>
              <div class="pf-row">
                <span class="pf-lbl">Role</span>
                <span class="pf-val"><span class="role-badge">{{ user?.role?.toUpperCase() || 'DRIVER' }}</span></span>
              </div>
              <div class="pf-row">
                <span class="pf-lbl">Account Status</span>
                <span v-if="user?.is_activated" class="pf-val text-success">✓ Activated</span>
                <span v-else class="pf-val status-pending">⏳ For Activation</span>
              </div>
            </div>

            <!-- Fingerprint -->
            <div class="fingerprint-section">
              <button v-if="biometricAvailable && !fingerprintEnabled" class="btn-fingerprint" @click="setupFingerprint">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.44-5.57 1.31-.28.14-.62.03-.76-.25-.14-.28-.03-.62.25-.76 1.88-.96 3.94-1.45 6.08-1.45 2.15 0 4.02.48 5.7 1.4.28.15.38.49.23.77-.09.16-.24.25-.43.25zm3.22 5.46c-.07 0-.14-.02-.22-.05-1.94-.77-4.12-1.16-6.48-1.16-2.49 0-4.74.41-6.69 1.21-.28.12-.6.01-.71-.26-.12-.28-.01-.6.26-.71 2.11-.86 4.54-1.3 7.14-1.3 2.52 0 4.86.41 6.95 1.24.27.11.41.42.3.69-.09.21-.3.34-.55.34zM12 21c-.28 0-.5-.22-.5-.5s.22-.5.5-.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2c0 .28-.22.5-.5.5s-.5-.22-.5-.5c0-1.65 1.35-3 3-3s3 1.35 3 3-1.35 3-3 3z"/></svg>
                Enable Fingerprint Login
              </button>
              <div v-else-if="fingerprintEnabled" class="fingerprint-linked">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                Fingerprint Login Linked
              </div>
            </div>
          </div>
        </div>

        <!-- =================== PAGE: DRIVER LICENSE =================== -->
        <div v-else-if="activePage === 'license'" key="license" class="page-content">
          <div class="page-header">
            <h1 class="page-title">Driver's License</h1>
            <p class="page-sub">Your LTO Driver's License details</p>
          </div>
          <div class="doc-page-layout">
            <div class="doc-image-panel glass" @click="openLightbox(licenseImgSrc, 'Driver\'s License')">
              <img v-if="licenseImgSrc" :src="licenseImgSrc" alt="Driver's License" class="doc-full-img" />
              <div v-else class="doc-no-img">
                <span>📄</span>
                <p>No license image uploaded</p>
              </div>
              <div v-if="licenseImgSrc" class="doc-view-overlay">🔍 Tap to enlarge</div>
            </div>
            <div class="doc-info-panel">
              <div class="info-card glass">
                <div class="info-row">
                  <span class="info-lbl">License Number</span>
                  <span class="info-val highlight">{{ user?.license_number || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Full Name</span>
                  <span class="info-val">{{ user?.full_name || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Status</span>
                  <span class="info-val text-success">{{ licenseImgSrc ? 'Uploaded ✓' : 'Pending' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== PAGE: OR =================== -->
        <div v-else-if="activePage === 'or'" key="or" class="page-content">
          <div class="page-header">
            <h1 class="page-title">Original Receipt (OR)</h1>
            <p class="page-sub">Official Receipt of your vehicle</p>
          </div>
          <div class="doc-page-layout">
            <div class="doc-image-panel glass" @click="openLightbox(orImgSrc, 'Original Receipt (OR)')">
              <img v-if="orImgSrc" :src="orImgSrc" alt="Original Receipt" class="doc-full-img" />
              <div v-else class="doc-no-img">
                <span>🧾</span>
                <p>No OR image uploaded</p>
              </div>
              <div v-if="orImgSrc" class="doc-view-overlay">🔍 Tap to enlarge</div>
            </div>
            <div class="doc-info-panel">
              <div class="info-card glass">
                <div class="info-row">
                  <span class="info-lbl">OR Renewal Date</span>
                  <span class="info-val highlight">{{ user?.or_renewal_date || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Status</span>
                  <span class="info-val text-success">{{ orImgSrc ? 'Uploaded ✓' : 'Pending' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== PAGE: CR =================== -->
        <div v-else-if="activePage === 'cr'" key="cr" class="page-content">
          <div class="page-header">
            <h1 class="page-title">Certificate of Registration</h1>
            <p class="page-sub">Vehicle registration details</p>
          </div>
          <div class="doc-page-layout">
            <div class="doc-image-panel glass" @click="openLightbox(crImgSrc, 'Certificate of Registration')">
              <img v-if="crImgSrc" :src="crImgSrc" alt="CR" class="doc-full-img" />
              <div v-else class="doc-no-img">
                <span>🏍️</span>
                <p>No CR image uploaded</p>
              </div>
              <div v-if="crImgSrc" class="doc-view-overlay">🔍 Tap to enlarge</div>
            </div>
            <div class="doc-info-panel">
              <div class="info-card glass">
                <div class="info-row">
                  <span class="info-lbl">Plate Number</span>
                  <span class="info-val highlight">{{ user?.cr_plate_number || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Brand</span>
                  <span class="info-val">{{ user?.cr_brand || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Model</span>
                  <span class="info-val">{{ user?.cr_model || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Color</span>
                  <span class="info-val">{{ user?.cr_color || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Registered Owner</span>
                  <span class="info-val">{{ user?.cr_owner_name || '—' }}</span>
                </div>
                <div class="info-row">
                  <span class="info-lbl">Status</span>
                  <span class="info-val text-success">{{ crImgSrc ? 'Uploaded ✓' : 'Pending' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== PAGE: TARDINESS =================== -->
        <div v-else-if="activePage === 'tardiness'" key="tardiness" class="page-content">
          <div class="page-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div>
              <h1 class="page-title">⏳ Monthly Tardiness Log</h1>
              <p class="page-sub">Monthly list of all tardiness calculated as | Total Work Hours - 10 |</p>
            </div>
          </div>

          <!-- CONTROLS & SUMMARY BAR -->
          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; background: rgba(15, 23, 42, 0.65); padding: 1.25rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.12); backdrop-filter: blur(12px);">
            
            <!-- SELECTABLE CALENDAR SELECT MONTH -->
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 1rem;">
              <div>
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  📅 Select Month
                </label>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <button type="button" class="btn btn-sm" @click="prevDriverTardinessMonth" style="background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 8px; padding: 0.55rem 0.75rem; cursor: pointer;">◀</button>
                  <select 
                    v-model="driverTardinessMonth" 
                    style="padding: 0.6rem 1rem; border-radius: 8px; background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 0.9rem; font-weight: 600; min-width: 200px; cursor: pointer;"
                  >
                    <option v-for="m in driverTardinessMonthOptions" :key="m.value" :value="m.value">
                      {{ m.label }}
                    </option>
                  </select>
                  <button type="button" class="btn btn-sm" @click="nextDriverTardinessMonth" style="background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 8px; padding: 0.55rem 0.75rem; cursor: pointer;">▶</button>
                </div>
              </div>

              <div>
                <label style="display: block; font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px;">
                  📏 Daily Shift Requirement
                </label>
                <div style="padding: 0.6rem 1rem; border-radius: 8px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #10b981; font-size: 0.9rem; font-weight: 700;">
                  10.0 Hours / Day
                </div>
              </div>
            </div>

            <!-- STAT SUMMARY BADGES -->
            <div style="display: flex; flex-wrap: wrap; gap: 0.85rem;">
              <div style="text-align: right; background: rgba(59, 130, 246, 0.1); padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 600;">🗓️ Days in Month</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #60a5fa;">{{ driverTardinessData.totalDaysInMonth }} Days</div>
              </div>
              <div style="text-align: right; background: rgba(239, 68, 68, 0.15); padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.4);">
                <div style="font-size: 0.7rem; color: #fca5a5; font-weight: 600;">⚠️ Days with Tardiness</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #ef4444;">{{ driverTardinessData.tardinessCount }} Days</div>
              </div>
              <div style="text-align: right; background: rgba(245, 158, 11, 0.15); padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid rgba(245, 158, 11, 0.4);">
                <div style="font-size: 0.7rem; color: #fde68a; font-weight: 600;">⏱️ Total Tardiness Hours</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #f59e0b;">{{ driverTardinessData.totalTardinessHours }} hrs</div>
              </div>
            </div>
          </div>

          <!-- TARDINESS TABLE -->
          <div class="table-responsive glass-table-container" style="border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.12); background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(12px);">
            <table class="table custom-table" style="width: 100%; border-collapse: collapse; text-align: left; color: #fff;">
              <thead>
                <tr style="background: rgba(30, 41, 59, 0.9); border-bottom: 2px solid rgba(255, 255, 255, 0.15); font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8;">
                  <th style="padding: 1rem 1.25rem;">Day & Date</th>
                  <th style="padding: 1rem 1.25rem; text-align: center;">Time In</th>
                  <th style="padding: 1rem 1.25rem; text-align: center;">Time Out</th>
                  <th style="padding: 1rem 1.25rem; text-align: center;">Total Work Hours</th>
                  <th style="padding: 1rem 1.25rem; text-align: center;">Shift Standard</th>
                  <th style="padding: 1rem 1.25rem; text-align: center; color: #ef4444;">Tardiness Hours (|Work - 10|)</th>
                  <th style="padding: 1rem 1.25rem; text-align: center;">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="row in driverTardinessData.tardinessRows" 
                  :key="row.dateStr"
                  style="border-bottom: 1px solid rgba(255, 255, 255, 0.08); transition: background 0.2s ease;"
                >
                  <td style="padding: 1rem 1.25rem; font-weight: 700;">
                    <div style="font-size: 0.95rem; color: #ffffff;">Day {{ row.dayNumber }}</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; font-weight: 500;">{{ row.dateFormatted }}</div>
                  </td>
                  <td style="padding: 1rem 1.25rem; text-align: center; font-family: monospace; font-size: 0.95rem; color: #38bdf8; font-weight: 600;">
                    {{ row.timeIn }}
                  </td>
                  <td style="padding: 1rem 1.25rem; text-align: center; font-family: monospace; font-size: 0.95rem; color: #f43f5e; font-weight: 600;">
                    {{ row.timeOut }}
                  </td>
                  <td style="padding: 1rem 1.25rem; text-align: center; font-weight: 700; color: #a855f7;">
                    {{ row.totalWorkHours }} hrs
                  </td>
                  <td style="padding: 1rem 1.25rem; text-align: center; font-weight: 600; color: #94a3b8;">
                    10.0 hrs
                  </td>
                  <td style="padding: 1rem 1.25rem; text-align: center;">
                    <span style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.35rem 0.75rem; border-radius: 8px; font-weight: 800; font-size: 0.95rem; display: inline-block;">
                      {{ row.tardinessHours }} hrs
                    </span>
                  </td>
                  <td style="padding: 1rem 1.25rem; text-align: center;">
                    <span style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; display: inline-block;">
                      ⏳ {{ row.status }}
                    </span>
                  </td>
                </tr>

                <tr v-if="driverTardinessData.tardinessRows.length === 0">
                  <td colspan="7" style="text-align: center; padding: 4rem 1.5rem; color: #94a3b8;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎉</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #10b981; margin-bottom: 0.25rem;">
                      No Tardiness Recorded for {{ driverTardinessMonth }}
                    </div>
                    <div style="font-size: 0.88rem; color: #64748b;">
                      All worked shifts met or exceeded the 10-hour standard requirement for this month.
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </Transition>
    </main>

    <!-- ===== LIGHTBOX ===== -->
    <Teleport to="body">
      <Transition name="lb-fade">
        <div v-if="lightboxSrc" class="lightbox-overlay" @click.self="closeLightbox">
          <div class="lightbox-box">
            <button class="lb-close" @click="closeLightbox">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
            <img :src="lightboxSrc" :alt="lightboxAlt" class="lb-img" />
            <div class="lb-caption" v-if="lightboxAlt">{{ lightboxAlt }}</div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ── Floating Chat Notification Toast ── -->
    <Transition name="toast-slide">
      <div v-if="showChatToast" class="chat-toast glass" @click="openChatFromToast">
        <div class="toast-icon">💬</div>
        <div class="toast-body">
          <div class="toast-title">New message from Passenger</div>
          <div class="toast-text">{{ toastMessage }}</div>
        </div>
        <div class="toast-arrow">➔</div>
      </div>
    </Transition>

    <!-- ── Ride Details Modal ── -->
    <Transition name="lb-fade">
      <div v-if="selectedRide" class="ride-modal-overlay" @click.self="selectedRide = null">
        <div class="ride-details-modal glass">
          <div class="ride-modal-header">
            <div class="ride-modal-title">
              <span class="ride-modal-icon">{{ selectedRide.document_image ? '📄' : '🛵' }}</span>
              <div>
                <h3 style="margin:0; font-size: 1.15rem; font-weight:700; color:#fff;">{{ selectedRide.document_image ? 'Document Delivery' : 'Passenger Ride' }}</h3>
                <span style="font-size: 0.75rem; color: rgba(255,255,255,0.6);">Booking #{{ selectedRide.id }} • {{ formatDate(selectedRide.date) }} {{ formatTime(selectedRide.date) }}</span>
              </div>
            </div>
            <button class="ride-modal-close" @click="selectedRide = null">✕</button>
          </div>

          <div class="ride-modal-body">
            <!-- Summary Bar -->
            <div class="ride-summary-grid">
              <div class="summary-box">
                <span class="summary-lbl">Fare Amount</span>
                <span class="summary-val" style="color: #38bdf8;">₱{{ (selectedRide.amount || 0).toFixed(2) }}</span>
              </div>
              <div v-if="selectedRide.document_tip" class="summary-box">
                <span class="summary-lbl">Tip</span>
                <span class="summary-val" style="color: #fbbf24;">₱{{ selectedRide.document_tip }}</span>
              </div>
              <div class="summary-box">
                <span class="summary-lbl">Status</span>
                <span :class="['status-badge', selectedRide.status]" style="font-size: 0.65rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700; text-transform: uppercase; display: inline-block; text-align: center;">{{ selectedRide.status }}</span>
              </div>
            </div>

            <!-- Route Info -->
            <div class="route-proof-box">
              <div class="route-row-item mb-2">
                <span style="color:#4ade80;">📍</span>
                <div>
                  <span class="summary-lbl" style="display:block;">From (Pickup)</span>
                  <span style="font-size:0.85rem; color:#fff; font-weight:500;">{{ selectedRide.pickup }}</span>
                </div>
              </div>
              <div class="route-row-item">
                <span style="color:#f87171;">🏁</span>
                <div>
                  <span class="summary-lbl" style="display:block;">To (Destination)</span>
                  <span style="font-size:0.85rem; color:#fff; font-weight:500;">{{ selectedRide.dropoff }}</span>
                </div>
              </div>
            </div>

            <!-- People Info -->
            <div class="ride-summary-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 1rem;">
              <div class="summary-box">
                <span class="summary-lbl">Passenger</span>
                <span style="font-size:0.85rem; font-weight:600; color:#fff;">{{ selectedRide.passenger || selectedRide.passenger_username }}</span>
              </div>
              <div class="summary-box">
                <span class="summary-lbl">Driver</span>
                <span style="font-size:0.85rem; font-weight:600; color:#fff;">{{ selectedRide.driver || selectedRide.driver_username || 'Unassigned' }}</span>
              </div>
            </div>

            <!-- Document & Delivery Proof Section -->
            <div v-if="selectedRide.document_image || selectedRide.document_info || selectedRide.received_image || selectedRide.signature_image" class="doc-proof-section">
              <div class="doc-proof-title">
                <span>📦 Document & Delivery Details</span>
              </div>

              <p v-if="selectedRide.document_info" style="font-size: 0.8rem; color: rgba(255,255,255,0.85); margin-bottom: 12px; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 8px;">
                <strong>Description:</strong> {{ selectedRide.document_info }}
              </p>

              <!-- Image Gallery Grid -->
              <div class="doc-gallery-grid">
                <!-- 1. Document Item Photo -->
                <div v-if="selectedRide.document_image" class="gallery-card">
                  <span class="gallery-tag">📄 Item Photo</span>
                  <img :src="selectedRide.document_image" class="gallery-img" @click="previewImage = selectedRide.document_image" alt="Item Photo" />
                </div>

                <!-- 2. Received Photo -->
                <div v-if="selectedRide.received_image" class="gallery-card">
                  <span class="gallery-tag">📷 Received Photo</span>
                  <img :src="selectedRide.received_image" class="gallery-img" @click="previewImage = selectedRide.received_image" alt="Received Photo" />
                </div>

                <!-- 3. Receiver Signature -->
                <div v-if="selectedRide.signature_image" class="gallery-card">
                  <span class="gallery-tag">✍️ Receiver Signature</span>
                  <img :src="selectedRide.signature_image" class="gallery-sig-img" @click="previewImage = selectedRide.signature_image" alt="Receiver Signature" />
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </Transition>

    <!-- ── Fullscreen Image Lightbox Preview ── -->
    <Transition name="lb-fade">
      <div v-if="previewImage" class="lightbox-modal-overlay" @click="previewImage = null">
        <div class="lightbox-card" @click.stop>
          <button class="lightbox-close" @click="previewImage = null">✕</button>
          <img :src="previewImage" class="lightbox-img" alt="Fullscreen Preview" />
        </div>
      </div>
    </Transition>

    <!-- ── GCash Loading Modal Overlay ── -->
    <Transition name="lb-fade">
      <div v-if="showGcashModal" class="gcash-modal-overlay" @click.self="closeGcashModal">
        <div class="gcash-card glass">
          <!-- Step 0: Select Payment Method -->
          <div v-if="gcashStep === 0" class="gcash-step">
            <div class="gcash-header-blue" style="justify-content: center; align-items: center; display: flex; background: linear-gradient(135deg, #1e293b, #0f172a);">
              <span class="gcash-logo" style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 800; color: #fff; letter-spacing: 0.5px;">TOP UP MENU</span>
            </div>
            <div class="gcash-body" style="padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem;">
              <p class="gcash-section-title" style="margin-bottom: 0.75rem; text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Select Top-Up Method</p>
              
              <!-- GCash Option -->
              <button 
                type="button" 
                class="payment-method-btn" 
                @click="paymentMethod = 'gcash'; gcashStep = 1" 
                style="display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 1.2rem; background: rgba(0, 86, 235, 0.12); border: 1px solid rgba(0, 86, 235, 0.45); border-radius: 12px; cursor: pointer; transition: all 0.2s; text-align: left; color: #fff;"
              >
                <div style="display: flex; align-items: center; gap: 12px;">
                  <img src="/gcash_logo1.png" alt="GCash" style="height: 28px; width: 28px; object-fit: contain; border-radius: 4px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));" />
                  <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: 700; color: #fff; font-size: 1.05rem;">GCash</span>
                    <span style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.5);">Instant wallet credit</span>
                  </div>
                </div>
                <span style="font-size: 1.2rem; color: #3b82f6; font-weight: bold;">➔</span>
              </button>

              <!-- Maya Option -->
              <button 
                type="button" 
                class="payment-method-btn" 
                @click="paymentMethod = 'maya'; gcashStep = 1" 
                style="display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 1.2rem; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.45); border-radius: 12px; cursor: pointer; transition: all 0.2s; text-align: left; color: #fff;"
              >
                <div style="display: flex; align-items: center; gap: 12px;">
                  <img src="/maya_logo.png" alt="Maya" style="height: 28px; width: 28px; object-fit: contain; border-radius: 4px;" />
                  <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: 700; font-size: 1.05rem; display: flex; align-items: center; gap: 6px;">
                      Maya 
                    </span>
                    <span style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.5);">Pay with Maya wallet</span>
                  </div>
                </div>
                <span style="font-size: 1.2rem; color: #10b981; font-weight: bold;">➔</span>
              </button>

              <div class="gcash-actions mt-6" style="display: flex; justify-content: flex-end;">
                <button type="button" class="btn btn-ghost" @click="closeGcashModal">Cancel</button>
              </div>
            </div>
          </div>

          <!-- Step 1: Select Amount -->
          <div v-else-if="gcashStep === 1" class="gcash-step">
            <div class="gcash-header-blue" :style="{ background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', justifyContent: 'center', alignItems: 'center', display: 'flex' }">
              <img :src="paymentMethod === 'maya' ? '/maya_logo.png' : '/gcash_logo1.png'" :alt="paymentMethod === 'maya' ? 'Maya' : 'GCash'" class="gcash-logo-img" style="height: 56px; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15)); border-radius: 4px;" />
            </div>
            <div class="gcash-body">
              <p class="gcash-section-title">Select Top-Up Amount</p>
              <div class="gcash-presets-five">
                <button type="button" class="preset-btn" :class="{ active: loadAmount === 100 }" :style="loadAmount === 100 ? { background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', borderColor: paymentMethod === 'maya' ? '#10b981' : '#0056eb' } : {}" @click="loadAmount = 100">₱100</button>
                <button type="button" class="preset-btn" :class="{ active: loadAmount === 200 }" :style="loadAmount === 200 ? { background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', borderColor: paymentMethod === 'maya' ? '#10b981' : '#0056eb' } : {}" @click="loadAmount = 200">₱200</button>
                <button type="button" class="preset-btn" :class="{ active: loadAmount === 300 }" :style="loadAmount === 300 ? { background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', borderColor: paymentMethod === 'maya' ? '#10b981' : '#0056eb' } : {}" @click="loadAmount = 300">₱300</button>
                <button type="button" class="preset-btn" :class="{ active: loadAmount === 500 }" :style="loadAmount === 500 ? { background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', borderColor: paymentMethod === 'maya' ? '#10b981' : '#0056eb' } : {}" @click="loadAmount = 500">₱500</button>
                <button type="button" class="preset-btn" :class="{ active: loadAmount === 1000 }" :style="loadAmount === 1000 ? { background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', borderColor: paymentMethod === 'maya' ? '#10b981' : '#0056eb' } : {}" @click="loadAmount = 1000">₱1000</button>
              </div>
              
              <div class="gcash-selected-amount-card">
                <span class="selected-amt-lbl">Total Credits to Add:</span>
                <span class="selected-amt-val">₱ {{ loadAmount }}.00</span>
              </div>
              
              <div class="gcash-actions mt-6">
                <button class="btn btn-ghost" @click="gcashStep = 0">Back</button>
                <button class="btn btn-gcash-next" :style="{ background: paymentMethod === 'maya' ? '#10b981' : '#0056eb' }" @click="gcashStep = 2">Next</button>
              </div>
            </div>
          </div>

          <!-- Step 2: Scan QR Code -->
          <div v-else-if="gcashStep === 2" class="gcash-step">
            <div class="gcash-header-portal" :style="{ background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', alignItems: 'center', display: 'flex', justifyContent: 'space-between', height: '48px', boxSizing: 'border-box', padding: '0 1rem' }">
              <img :src="paymentMethod === 'maya' ? '/maya_logo.png' : '/gcash_logo1.png'" :alt="paymentMethod === 'maya' ? 'Maya' : 'GCash'" class="gcash-portal-logo-img" style="height: 40px; object-fit: contain; border-radius: 3px;" />
              <span class="qr-pay-label" style="color: #ffffff; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Merchant Payment</span>
            </div>
            <div class="gcash-body portal-bg">
              <div class="qr-display-card">
                <!-- Dynamic QR Code (using a clean public QR API pointing to receiver) -->
                <div class="qr-image-wrapper">
                  <img :src="paymentQrCodeSrc" @error="handleGcashQrError" :alt="paymentMethod === 'maya' ? 'Maya QR Code' : 'GCash QR Code'" class="gcash-qr-image" />
                </div>
                <!-- Download QR Button -->
                <button class="btn-download-qr" :style="{ background: paymentMethod === 'maya' ? 'linear-gradient(135deg, #10b981, #059669)' : 'linear-gradient(135deg, #0056eb, #1a7ef5)' }" @click="downloadQrCode" title="Download QR Code">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zm-8 2V5h2v6h1.17L12 13.17 9.83 11H11zm-6 7h14v2H5z"/></svg>
                  Download {{ paymentMethod === 'maya' ? 'Maya' : 'GCash' }} QR Code
                </button>
                
                <!-- QR Receiver details -->
                <div class="qr-pay-details">
                  <div class="qr-details-row">
                    <span class="qr-det-lbl">Amount</span>
                    <strong class="qr-det-val amount-highlight" :style="{ color: paymentMethod === 'maya' ? '#10b981' : '#0056eb' }">₱ {{ Number(loadAmount).toFixed(2) }}</strong>
                  </div>
                </div>
              </div>

              <!-- Instructions -->
              <div class="qr-instructions" style="background: rgba(254, 243, 199, 0.95); padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid rgba(245, 158, 11, 0.25);">
                <p class="instr-title" style="font-weight: 700; color: #000; margin-bottom: 0.50rem; margin-top: 0;">💡 How to Pay:</p>
                <ol class="instr-list" style="margin-left: 1.25rem; padding-left: 0; display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 0;">
                  <li style="color: #000; font-size: 0.85rem; font-weight: 500;">Open your <strong>{{ paymentMethod === 'maya' ? 'Maya App' : 'GCash App' }}</strong> on your phone.</li>
                  <li style="color: #000; font-size: 0.85rem; font-weight: 500;"><strong>Scan QR or Download and Upload to {{ paymentMethod === 'maya' ? 'MAYA' : 'GCASH' }}</strong>.</li>
                  <li style="color: #000; font-size: 0.85rem; font-weight: 500;">Save and copy the <strong>Reference Number</strong>.</li>
                  <li style="color: #000; font-size: 0.85rem; font-weight: 500;">Enter the <strong>Reference Number</strong> then Proceed.</li>
                </ol>
              </div>

              <div class="portal-actions">
                <button class="btn-portal-back" @click="gcashStep = 1">Back</button>
                <button class="btn-portal-next" :style="{ background: paymentMethod === 'maya' ? '#10b981' : '#0056eb' }" @click="gcashStep = 3">Proceed</button>
              </div>
            </div>
          </div>

          <!-- Step 3: Enter Receipt Reference Number -->
          <div v-else-if="gcashStep === 3" class="gcash-step">
            <div class="gcash-header-portal" :style="{ background: paymentMethod === 'maya' ? '#10b981' : '#0056eb', alignItems: 'center', display: 'flex', justifyContent: 'space-between', height: '48px', boxSizing: 'border-box', padding: '0 1rem' }">
              <img :src="paymentMethod === 'maya' ? '/maya_logo.png' : '/gcash_logo1.png'" :alt="paymentMethod === 'maya' ? 'Maya' : 'GCash'" class="gcash-portal-logo-img" style="height: 40px; object-fit: contain; border-radius: 3px;" />
              <span class="gcash-portal-secure">🔒 Claim Wallet Credit</span>
            </div>
            <div class="gcash-body portal-bg">
              <p class="otp-instruction">Enter the **Reference Number** from your {{ paymentMethod === 'maya' ? 'Maya' : 'GCash' }} payment receipt to credit your wallet.</p>
              
              <div class="ref-input-card">
                <label class="portal-input-lbl">{{ paymentMethod === 'maya' ? 'Maya' : 'GCash' }} Transaction Reference No.</label>
                <input 
                  type="text" 
                  class="ref-code-input"
                  v-model="gcashRefNumber"
                  placeholder="e.g. 5019876543210"
                />
                <p class="ref-input-help">Enter reference number from your receipt.</p>
              </div>

              <div class="otp-helpers mt-4">
                <button type="button" class="btn-otp-shortcut" @click="autocompleteRef">⚡ Fill Mock Ref (5019876543210)</button>
              </div>

              <div class="portal-actions mt-6">
                <button class="btn-portal-back" @click="gcashStep = 2">Back</button>
                <button class="btn-portal-pay" :style="{ background: paymentMethod === 'maya' ? '#10b981' : '#0056eb' }" :disabled="!isValidRefNumber" @click="handleGcashPayment">Submit</button>
              </div>
            </div>
          </div>

          <!-- Step 4: Verification Processing -->
          <div v-else-if="gcashStep === 4" class="gcash-step processing-step">
            <div class="gcash-processing-box">
              <div class="gcash-spinner"></div>
              <h3 class="processing-title">Verifying Payment Reference</h3>
              <p class="processing-desc">{{ processingMessage }}</p>
            </div>
          </div>

          <!-- Step 5: Success Receipt -->
          <div v-else-if="gcashStep === 5" class="gcash-step">
            <div class="gcash-receipt-wrapper">
              <div class="receipt-success-badge">
                <svg viewBox="0 0 24 24" width="36" height="36" fill="white">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
              </div>
              <h2 class="receipt-heading" style="color: #fbbf24;">Top-Up Submitted!</h2>
              <p class="receipt-sub">Waiting for Admin Verification & Approval</p>
              
              <div class="receipt-card">
                <div class="receipt-amount-row">
                  <span class="rcpt-lbl">Amount Submitted</span>
                  <span class="rcpt-amt">₱ {{ Number(loadAmount).toFixed(2) }}</span>
                </div>
                <div class="receipt-details">
                  <div class="rcpt-row">
                    <span>System Ref No.</span>
                    <strong style="color: #3b82f6; font-weight: 800; letter-spacing: 0.5px;">{{ receiptInfo?.system_ref || receiptInfo?.transaction_id || generatedRefNo }}</strong>
                  </div>
                  <div class="rcpt-row">
                    <span>{{ paymentMethod === 'maya' ? 'Maya' : 'GCash' }} Ref No.</span>
                    <strong class="text-success">{{ receiptInfo?.reference_number || gcashRefNumber || '5019876543210' }}</strong>
                  </div>
                  <div class="rcpt-row">
                    <span>Receiver</span>
                    <strong>0966 822 2470 (Caesar L.)</strong>
                  </div>
                  <div class="rcpt-row">
                    <span>Date & Time</span>
                    <strong>{{ new Date().toLocaleString() }}</strong>
                  </div>
                  <div class="rcpt-row">
                    <span>Status</span>
                    <strong style="color: #fbbf24;">⏳ Pending Approval</strong>
                  </div>
                </div>
              </div>

              <button class="btn-receipt-done" @click="completeTopUp">Back to Dashboard</button>
            </div>
          </div>

        </div>
      </div>
    </Transition>

    <!-- ── Wallet History Log Details Modal ── -->
    <Transition name="lb-fade">
      <div v-if="selectedLogDetails" class="gcash-modal-overlay" @click.self="selectedLogDetails = null">
        <div class="gcash-card glass" style="max-width: 420px;">
          <div class="gcash-header-portal" style="align-items: center; display: flex; justify-content: space-between; height: 48px; box-sizing: border-box; padding: 0.5rem 1rem; background: linear-gradient(135deg, #1e293b, #0f172a);">
            <span style="font-family: 'Outfit', sans-serif; font-weight: 800; color: #fff; font-size: 1.1rem; display: flex; align-items: center; gap: 6px;">
              📋 Transaction Details
            </span>
            <button type="button" @click="selectedLogDetails = null" style="background: transparent; border: none; color: #fff; font-size: 1.2rem; cursor: pointer;">✕</button>
          </div>

          <div class="gcash-body" style="padding: 1.25rem; display: flex; flex-direction: column; gap: 1rem;">
            <!-- Amount Badge -->
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1.25rem; text-align: center;">
              <span style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.6); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; display: block; margin-bottom: 4px;">
                {{ selectedLogDetails.type === 'load' ? 'Credit Top-Up' : 'Ride Fee Deduction' }}
              </span>
              <strong :style="{ color: selectedLogDetails.amount >= 0 ? '#10b981' : '#f43f5e', fontSize: '1.8rem', fontWeight: '800' }">
                {{ selectedLogDetails.amount >= 0 ? '+' : '' }}₱{{ Math.abs(selectedLogDetails.amount).toFixed(2) }}
              </strong>
            </div>

            <div class="receipt-card" style="background: #ffffff; color: #1e293b; border-radius: 12px; padding: 1rem;">
              <div class="receipt-details" style="display: flex; flex-direction: column; gap: 0.6rem;">
                <div class="rcpt-row" style="display: flex; justify-content: space-between; font-size: 0.82rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                  <span style="color: #64748b;">System Ref No.</span>
                  <strong style="color: #0056eb; font-weight: 800; letter-spacing: 0.5px;">{{ selectedLogDetails.system_ref || getLogSystemRef(selectedLogDetails) }}</strong>
                </div>

                <div v-if="selectedLogDetails.reference_number" class="rcpt-row" style="display: flex; justify-content: space-between; font-size: 0.82rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                  <span style="color: #64748b;">Provider Ref No.</span>
                  <strong style="color: #059669; font-weight: 700;">{{ selectedLogDetails.reference_number }}</strong>
                </div>

                <div class="rcpt-row" style="display: flex; justify-content: space-between; font-size: 0.82rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                  <span style="color: #64748b;">Payment Method</span>
                  <strong style="text-transform: capitalize; color: #334155;">{{ selectedLogDetails.payment_method || (selectedLogDetails.reference_number ? 'GCash / Maya' : 'System Fee') }}</strong>
                </div>

                <div class="rcpt-row" style="display: flex; justify-content: space-between; font-size: 0.82rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                  <span style="color: #64748b;">Updated Balance</span>
                  <strong style="color: #0f172a; font-weight: 700;">₱{{ Number(selectedLogDetails.new_balance).toFixed(2) }}</strong>
                </div>

                <div class="rcpt-row" style="display: flex; justify-content: space-between; font-size: 0.82rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                  <span style="color: #64748b;">Date & Time</span>
                  <strong style="color: #334155;">{{ formatDate(selectedLogDetails.created_at) }} {{ formatTime(selectedLogDetails.created_at) }}</strong>
                </div>

                <div class="rcpt-row" style="display: flex; justify-content: space-between; font-size: 0.82rem;">
                  <span style="color: #64748b;">Status</span>
                  <strong v-if="selectedLogDetails.status === 'pending'" style="color: #d97706;">⏳ Pending Approval</strong>
                  <strong v-else-if="selectedLogDetails.status === 'rejected'" style="color: #dc2626;">🔴 Unverified</strong>
                  <strong v-else style="color: #10b981;">Completed ✓</strong>
                </div>
              </div>
            </div>

            <div style="display: flex; gap: 8px; justify-content: flex-end;">
              <button class="btn btn-ghost" style="width: 100%; padding: 10px; background: rgba(255,255,255,0.1); color: #fff; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;" @click="selectedLogDetails = null">Close</button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Fix Unverified Top Up Modal -->
    <Transition name="modal-fade">
      <div v-if="showFixRefModal" class="modal-overlay glass-backdrop" @click.self="closeFixRefModal" style="position: fixed; inset: 0; background: rgba(15,23,42,0.85); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; z-index: 9999;">
        <div class="modal-content glass" style="max-width: 440px; width: 90%; padding: 1.5rem; border-radius: 20px; background: rgba(30, 41, 59, 0.95); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
          <h3 style="margin-top: 0; color: #f87171; font-size: 1.25rem; display: flex; align-items: center; gap: 8px;">
            ⚠️ Fix Unverified Top Up
          </h3>
          <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-bottom: 1.25rem; line-height: 1.4;">
            Please enter your <strong>System Reference No.</strong> and corrected <strong>Top Up Reference No.</strong> to resubmit for Admin verification.
          </p>

          <div v-if="fixRefError" class="alert alert-error" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; margin-bottom: 1rem;">
            {{ fixRefError }}
          </div>
          <div v-if="fixRefSuccess" class="alert alert-success" style="background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; margin-bottom: 1rem;">
            {{ fixRefSuccess }}
          </div>

          <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem;">
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 700; color: #38bdf8; margin-bottom: 6px;">System Reference No.</label>
              <input 
                type="text" 
                v-model="fixSystemRef" 
                placeholder="e.g. CAEL-G260831123456789" 
                style="width: 100%; box-sizing: border-box; padding: 10px 14px; font-family: monospace; text-transform: uppercase; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 8px;"
              />
            </div>
            <div>
              <label style="display: block; font-size: 0.8rem; font-weight: 700; color: #fbbf24; margin-bottom: 6px;">Top Up Reference No. (GCash / Maya)</label>
              <input 
                type="text" 
                v-model="fixNewRef" 
                placeholder="e.g. 5019876543210" 
                style="width: 100%; box-sizing: border-box; padding: 10px 14px; font-family: monospace; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 8px;"
              />
            </div>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 10px;">
            <button class="btn btn-ghost btn-sm" style="padding: 8px 16px; background: rgba(255,255,255,0.1); color: #fff; border: none; border-radius: 8px; cursor: pointer;" @click="closeFixRefModal">Cancel</button>
            <button 
              class="btn btn-sm" 
              @click="submitFixRef" 
              :disabled="submittingFixRef || !fixSystemRef || !fixNewRef"
              style="background: #0056eb; color: white; border: none; padding: 8px 18px; border-radius: 8px; font-weight: 700; cursor: pointer;"
            >
              {{ submittingFixRef ? 'Submitting...' : 'Submit' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- LIVE DRIVER SUPPORT CHAT FLOATING WIDGET -->
    <SupportChatModal :user="user" role="Driver" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import SupportChatModal from '../components/SupportChatModal.vue'
import { useRideStore } from '../stores/ride'

import { authApi } from '../api/auth'

const auth      = useAuthStore()
const rideStore = useRideStore()
const router    = useRouter()
const user      = computed(() => auth.user)

// Wallet Transaction History filters & state
const balanceLogs = ref([])
const showLoadFilter = ref(true)
const showFeeFilter = ref(true)
const selectedLogDate = ref('')

const filteredBalanceLogs = computed(() => {
  return balanceLogs.value.filter(log => {
    if (log.type === 'load' && !showLoadFilter.value) return false
    if (log.type === 'fee' && !showFeeFilter.value) return false
    if (selectedLogDate.value && log.created_at) {
      const logDate = log.created_at.split('T')[0]
      if (logDate !== selectedLogDate.value) return false
    }
    return true
  })
})

const showFixRefModal = ref(false)
const fixSystemRef = ref('')
const fixNewRef = ref('')
const fixRefError = ref('')
const fixRefSuccess = ref('')
const submittingFixRef = ref(false)

const pendingTopUpTotal = computed(() => {
  return balanceLogs.value
    .filter(log => log.type === 'load' && (log.status === 'pending' || log.status === 'rejected'))
    .reduce((sum, log) => sum + (log.amount || 0), 0)
})

const unverifiedTopUpCount = computed(() => {
  return balanceLogs.value.filter(log => log.type === 'load' && log.status === 'rejected').length
})

function openFixRefModal() {
  const rejectedLog = balanceLogs.value.find(log => log.type === 'load' && log.status === 'rejected')
  fixSystemRef.value = rejectedLog ? (rejectedLog.system_ref || rejectedLog.reference_number || '') : ''
  fixNewRef.value = ''
  fixRefError.value = ''
  fixRefSuccess.value = ''
  showFixRefModal.value = true
}

function closeFixRefModal() {
  showFixRefModal.value = false
}

function handleTopUpStatusUpdated(e) {
  const data = e.detail || e
  if (data) {
    const target = balanceLogs.value.find(l => String(l.id) === String(data.log_id))
    if (target) {
      target.status = data.status
    }
    if (data.new_balance !== undefined && auth.user) {
      auth.user.balance = data.new_balance
    }
    fetchBalanceLogs()
  }
}

function handleTopUpCreated(e) {
  const data = e.detail || e
  if (data && data.log) {
    const idx = balanceLogs.value.findIndex(l => String(l.id) === String(data.log.id))
    if (idx !== -1) {
      balanceLogs.value[idx] = { ...balanceLogs.value[idx], ...data.log }
    } else {
      balanceLogs.value.unshift(data.log)
    }
  }
}

async function submitFixRef() {
  if (!fixSystemRef.value || !fixNewRef.value) return
  submittingFixRef.value = true
  fixRefError.value = ''
  fixRefSuccess.value = ''
  
  try {
    const res = await authApi.fixTopUpReference(fixSystemRef.value, fixNewRef.value)
    fixRefSuccess.value = res.message || 'Successfully Updated'
    setTimeout(async () => {
      closeFixRefModal()
      await fetchBalanceLogs()
    }, 1200)
  } catch (err) {
    console.error("Fix ref error:", err)
    fixRefError.value = err.response?.data?.detail || "System Reference No. does not exist. Please check."
  } finally {
    submittingFixRef.value = false
  }
}

async function fetchBalanceLogs() {
  try {
    const data = await authApi.getBalanceLogs()
    balanceLogs.value = Array.isArray(data) ? data : (data?.items || [])
  } catch (err) {
    console.error('Failed to fetch balance logs:', err)
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

// Ride History filters & state
const bookings = ref([])
const showPassengerFilter = ref(true)
const showDocumentFilter = ref(true)
const selectedRideDate = ref('')
const selectedRide = ref(null)
const previewImage = ref(null)

const filteredBookings = computed(() => {
  return bookings.value.filter(b => {
    const isDoc = !!b.document_image
    if (isDoc && !showDocumentFilter.value) return false
    if (!isDoc && !showPassengerFilter.value) return false
    if (selectedRideDate.value && b.date) {
      const rideDate = b.date.split('T')[0]
      if (rideDate !== selectedRideDate.value) return false
    }
    return true
  })
})

async function fetchRideBookings() {
  try {
    const data = await authApi.getBookings()
    bookings.value = data || []
  } catch (err) {
    console.error('Failed to fetch bookings history:', err)
  }
}

// Draggable Scroll System for feeds
const isDragging = ref(false)
let startY = 0
let scrollTopStart = 0

function openRideDetails(booking) {
  selectedRide.value = booking
}

function startDrag(e) {
  if (e.pointerType === 'mouse' && e.button !== 0) return
  
  const isInteractive = e.target.closest('button, input, select, textarea, label, a, [role="button"], .clickable-ride-row, .audit-log-row') ||
                        ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'A'].includes(e.target.tagName)
  if (isInteractive) return
  
  const container = e.currentTarget
  isDragging.value = true
  container.classList.add('grabbing')
  startY = e.pageY
  scrollTopStart = container.scrollTop
  try {
    container.setPointerCapture(e.pointerId)
  } catch (err) {
    // ignore
  }
}

function onDrag(e) {
  if (!isDragging.value) return
  const container = e.currentTarget
  const dy = e.pageY - startY
  container.scrollTop = scrollTopStart - dy
}

function endDrag(e) {
  if (!isDragging.value) return
  isDragging.value = false
  const container = e.currentTarget
  container.classList.remove('grabbing')
  try {
    container.releasePointerCapture(e.pointerId)
  } catch (err) {
    // ignore
  }
}

// GCash / Maya Loading System States
const showGcashModal = ref(false)
const gcashStep = ref(0)
const loadAmount = ref(100)
const gcashRefNumber = ref('')
const processingMessage = ref('Securing Connection...')
const receiptInfo = ref(null)
const paymentMethod = ref('gcash') // 'gcash' or 'maya'

const paymentQrCodeSrc = computed(() => {
  const allowed = [100, 200, 300, 500, 1000]
  const amt = allowed.includes(loadAmount.value) ? loadAmount.value : 100
  if (paymentMethod.value === 'maya') {
    return `/maya/qr/maya_${amt}.png`
  }
  return `/gcash/qr/gcash_qr_${amt}a.png`
})

const gcashQrCodeSrc = paymentQrCodeSrc

function handleGcashQrError() {
  console.warn(`Failed to load ${paymentMethod.value} QR code image for ₱${loadAmount.value}`)
}

async function downloadQrCode() {
  try {
    const src = paymentQrCodeSrc.value
    const response = await fetch(src)
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${paymentMethod.value}_qr_${loadAmount.value}.png`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (e) {
    console.error('Failed to download QR code:', e)
  }
}

const isValidAmount = computed(() => {
  return typeof loadAmount.value === 'number' && loadAmount.value >= 10 && loadAmount.value <= 50000
})

const isValidRefNumber = computed(() => {
  const refNum = (gcashRefNumber.value || '').trim().replace(/\s/g, '')
  return refNum.length >= 3
})

function openGcashModal() {
  showGcashModal.value = true
  gcashStep.value = 0
  paymentMethod.value = 'gcash'
  loadAmount.value = 100
  gcashRefNumber.value = ''
  receiptInfo.value = null
}

function closeGcashModal() {
  showGcashModal.value = false
}

function autocompleteRef() {
  gcashRefNumber.value = '5019876543210'
}

const generatedRefNo = ref('')
const selectedLogDetails = ref(null)

function openLogDetails(log) {
  selectedLogDetails.value = log
}

function getLogSystemRef(log) {
  if (!log) return ''
  if (log.system_ref) return log.system_ref
  const refStr = (log.reference_number || '').toLowerCase()
  const prefix = refStr.includes('maya') ? 'M' : (log.reference_number ? 'G' : 'F')
  const dt = log.created_at ? new Date(log.created_at) : new Date()
  const pad = (n) => String(n).padStart(2, '0')
  const dateStr = `${String(dt.getFullYear()).slice(-2)}${pad(dt.getMonth() + 1)}${pad(dt.getDate())}${pad(dt.getHours())}${pad(dt.getMinutes())}${pad(dt.getSeconds())}`
  const rand5 = String((log.id * 12345 + 54321) % 90000 + 10000)
  return `CAEL-${prefix}${dateStr}${rand5}`
}

async function handleGcashPayment() {
  if (!isValidRefNumber.value) return
  gcashStep.value = 4
  processingMessage.value = `Verifying ${paymentMethod.value === 'maya' ? 'Maya' : 'GCash'} transaction reference number...`
  
  setTimeout(() => {
    processingMessage.value = 'Confirming receipt of transfer...'
  }, 1000)

  setTimeout(async () => {
    try {
      processingMessage.value = 'Finalizing CAEL Wallet Load...'
      const res = await authApi.loadBalanceGcashQr(loadAmount.value, gcashRefNumber.value, paymentMethod.value)
      if (res.ok) {
        receiptInfo.value = res
        const prefix = paymentMethod.value === 'maya' ? 'M' : 'G'
        const dt = new Date()
        const pad = (n) => String(n).padStart(2, '0')
        const dateStr = `${String(dt.getFullYear()).slice(-2)}${pad(dt.getMonth() + 1)}${pad(dt.getDate())}${pad(dt.getHours())}${pad(dt.getMinutes())}${pad(dt.getSeconds())}`
        const rand5 = Math.floor(10000 + Math.random() * 90000)
        generatedRefNo.value = res.system_ref || `CAEL-${prefix}${dateStr}${rand5}`
        gcashStep.value = 5
      } else {
        alert(res.message || 'Verification failed. Reference code may be invalid or already used.')
        gcashStep.value = 3
      }
    } catch (err) {
      console.error('QR Load Error:', err)
      alert(err.message || 'Transaction Claim failed. Please check your Reference Number or try again.')
      gcashStep.value = 3
    }
  }, 2200)
}

async function completeTopUp() {
  closeGcashModal()
  // Refresh user data to show correct balance
  try {
    await auth.fetchCurrentUser()
    await fetchBalanceLogs()
  } catch (e) {
    console.error('Failed to refresh user balance:', e)
  }
}

const showChatToast = ref(false)
const toastMessage = ref('')
const notifications = ref([])
const notifOpen = ref(false)

const unreadNotifCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

watch(() => rideStore.chatMessages, (newMsgs) => {
  if (newMsgs.length > 0) {
    const lastMsg = newMsgs[newMsgs.length - 1]
    if (lastMsg.sender === 'other') {
      const exists = notifications.value.some(n => n.text === `Passenger: ${lastMsg.text}` && n.time === lastMsg.time)
      if (!exists) {
        notifications.value.unshift({
          id: Date.now(),
          text: `Passenger: ${lastMsg.text}`,
          time: lastMsg.time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          read: false
        })
        toastMessage.value = lastMsg.text
        showChatToast.value = true
        setTimeout(() => {
          showChatToast.value = false
        }, 5000)
      }
    }
  }
}, { deep: true })

function openChatFromToast() {
  showChatToast.value = false
  rideStore.chatOpen = true
  router.push('/driver')
}

function clearNotifications() {
  notifications.value = []
}

function clickNotification(n) {
  n.read = true
  notifOpen.value = false
  rideStore.chatOpen = true
  router.push('/driver')
}

// ── State ──────────────────────────────────────────────
const sidebarCollapsed  = ref(true)
const mobileSidebarOpen = ref(false)
const activePage        = ref('home')
const autoAccept        = ref(localStorage.getItem('auto_accept') === 'true')
const biometricAvailable = ref(false)
const fingerprintEnabled = ref(false)
const apiHost = ref('http://localhost:8000')
const lightboxSrc = ref('')
const lightboxAlt = ref('')

// ── Nav Items ──────────────────────────────────────────
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
    key: 'license',
    label: "Driver's License",
    icon: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6zm0 4h8v2H6zm10 0h2v2h-2zm0-4h2v2h-2zm-6 0h4v2h-4z"/></svg>`
  },
  {
    key: 'or',
    label: 'Original Receipt',
    icon: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M18 17H6v-2h12v2zm0-4H6v-2h12v2zm0-4H6V7h12v2zM3 22l1.5-1.5L6 22l1.5-1.5L9 22l1.5-1.5L12 22l1.5-1.5L15 22l1.5-1.5L18 22l1.5-1.5L21 22V2l-1.5 1.5L18 2l-1.5 1.5L15 2l-1.5 1.5L12 2l-1.5 1.5L9 2 7.5 3.5 6 2 4.5 3.5 3 2v20z"/></svg>`
  },
  {
    key: 'cr',
    label: 'Certificate of Reg.',
    icon: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 15l-3-3 1.41-1.41L10 13.17l7.59-7.59L19 7l-9 9z"/></svg>`
  },
]

// ── Computed: page label for mobile topbar ─────────────
const currentPageLabel = computed(() => {
  const found = navItems.find(i => i.key === activePage.value)
  return found ? found.label : 'Dashboard'
})

// ── DRIVER TARDINESS MODULE COMPUTED & STATE ────────────────────────────
const driverTardinessMonth = ref('2026-09')
const driverTardinessStandardHours = ref(10.0)

const driverTardinessMonthOptions = [
  { value: '2026-01', label: 'January 2026' },
  { value: '2026-02', label: 'February 2026' },
  { value: '2026-03', label: 'March 2026' },
  { value: '2026-04', label: 'April 2026' },
  { value: '2026-05', label: 'May 2026' },
  { value: '2026-06', label: 'June 2026' },
  { value: '2026-07', label: 'July 2026' },
  { value: '2026-08', label: 'August 2026' },
  { value: '2026-09', label: 'September 2026 (Current)' },
  { value: '2026-10', label: 'October 2026' },
  { value: '2026-11', label: 'November 2026' },
  { value: '2026-12', label: 'December 2026' }
]

function prevDriverTardinessMonth() {
  const [y, m] = driverTardinessMonth.value.split('-').map(Number)
  if (m === 1) {
    driverTardinessMonth.value = `${y - 1}-12`
  } else {
    driverTardinessMonth.value = `${y}-${String(m - 1).padStart(2, '0')}`
  }
}

function nextDriverTardinessMonth() {
  const [y, m] = driverTardinessMonth.value.split('-').map(Number)
  if (m === 12) {
    driverTardinessMonth.value = `${y + 1}-01`
  } else {
    driverTardinessMonth.value = `${y + 1}-${String(m + 1).padStart(2, '0')}`
  }
}

const driverTardinessData = computed(() => {
  const [yearStr, monthStr] = driverTardinessMonth.value.split('-')
  const year = parseInt(yearStr, 10)
  const month = parseInt(monthStr, 10) - 1
  const totalDays = new Date(year, month + 1, 0).getDate()

  const tardinessRows = []

  for (let day = 1; day <= totalDays; day++) {
    const dObj = new Date(year, month, day)
    const dayOfWeek = dObj.getDay()
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6
    const dayFormattedStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const dateLabel = dObj.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric', weekday: 'short' })

    let timeIn = '08:00 AM'
    let timeOut = '06:00 PM'
    let totalWorkHours = 10.0
    let status = 'Present'

    if (isWeekend) {
      status = 'Rest Day'
      totalWorkHours = 0.0
      timeIn = '--:--'
      timeOut = '--:--'
    } else {
      if (day === 3 || day === 14) {
        status = 'Late'
        timeIn = '08:45 AM'
        timeOut = '05:00 PM'
        totalWorkHours = 7.25
      } else if (day === 7 || day === 17) {
        status = 'Early Out'
        timeIn = '08:00 AM'
        timeOut = '03:30 PM'
        totalWorkHours = 6.5
      } else if (day === 12) {
        status = 'Late'
        timeIn = '09:30 AM'
        timeOut = '05:00 PM'
        totalWorkHours = 6.5
      } else {
        status = 'Present'
        timeIn = '08:00 AM'
        timeOut = '06:00 PM'
        totalWorkHours = 10.0
      }
    }

    const tardinessHours = Math.abs(totalWorkHours - driverTardinessStandardHours.value)
    const isTardy = !isWeekend && tardinessHours > 0

    if (isTardy) {
      tardinessRows.push({
        dayNumber: day,
        dateFormatted: dateLabel,
        dateStr: dayFormattedStr,
        timeIn,
        timeOut,
        totalWorkHours: parseFloat(totalWorkHours.toFixed(2)),
        tardinessHours: parseFloat(tardinessHours.toFixed(2)),
        status
      })
    }
  }

  const totalTardinessHours = tardinessRows.reduce((sum, r) => sum + r.tardinessHours, 0)

  return {
    totalDaysInMonth: totalDays,
    tardinessCount: tardinessRows.length,
    tardinessRows,
    totalTardinessHours: parseFloat(totalTardinessHours.toFixed(2))
  }
})

// ── Computed: image sources ────────────────────────────
const licenseImgSrc = computed(() =>
  user.value?.license_image_base64 ||
  (user.value?.license_image_path ? `${apiHost.value}/${user.value.license_image_path}` : '')
)
const orImgSrc = computed(() =>
  user.value?.or_image_base64 ||
  (user.value?.or_image_path ? `${apiHost.value}/${user.value.or_image_path}` : '')
)
const crImgSrc = computed(() =>
  user.value?.cr_image_base64 ||
  (user.value?.cr_image_path ? `${apiHost.value}/${user.value.cr_image_path}` : '')
)

// ── Computed: initials ─────────────────────────────────
const initials = computed(() => {
  const name = user.value?.full_name;
  if (!name) return '?'
  return name.trim().split(/\s+/).map(w => w ? w[0] : '').join('').toUpperCase().slice(0, 2)
})

// ── Lightbox ───────────────────────────────────────────
function openLightbox(src, alt = '') {
  if (!src) return
  lightboxSrc.value = src
  lightboxAlt.value = alt
  document.body.style.overflow = 'hidden'
}
function closeLightbox() {
  lightboxSrc.value = ''
  lightboxAlt.value = ''
  document.body.style.overflow = ''
}
function handleKeydown(e) {
  if (e.key === 'Escape') closeLightbox()
}

// ── Actions ────────────────────────────────────────────
function toggleAutoAccept() {
  localStorage.setItem('auto_accept', autoAccept.value ? 'true' : 'false')
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

async function setupFingerprint() {
  try {
    const challenge = new Uint8Array(32)
    window.crypto.getRandomValues(challenge)
    const userId = new Uint8Array(16)
    window.crypto.getRandomValues(userId)
    const credential = await navigator.credentials.create({
      publicKey: {
        challenge,
        rp: { name: 'CAEL' },
        user: { id: userId, name: user.value.username, displayName: user.value.full_name },
        pubKeyCredParams: [{ alg: -7, type: 'public-key' }],
        timeout: 60000,
        attestation: 'direct',
        userVerification: 'required',
        authenticatorSelection: { authenticatorAttachment: 'platform', userVerification: 'required' }
      }
    })
    if (credential) {
      fingerprintEnabled.value = true
      localStorage.setItem(`fp_${user.value.username}`, 'true')
      alert('Fingerprint login has been enabled!')
    }
  } catch (e) {
    alert('Could not set up fingerprint. Make sure your device supports it.')
  }
}

// ── Lifecycle ──────────────────────────────────────────
onMounted(async () => {
  rideStore.connectWebSocket()
  // Fetch latest driver profile details to capture activation status in real-time
  try {
    if (auth.isAuthenticated) {
      await auth.fetchCurrentUser()
      await fetchBalanceLogs()
      await fetchRideBookings()
    }
  } catch (err) {
    console.warn('Could not refresh user profile on mount:', err)
    // If the token is invalid or expired (401), force a logout and redirect to login
    if (err.message?.includes('401') || err.message?.includes('Unauthorized') || err.message?.includes('token')) {
      auth.logout()
      router.push('/login?error=session_expired')
      return
    }
  }

  const isRender = window.location.hostname.includes('onrender.com')
  const host = import.meta.env.VITE_API_URL || (isRender ? 'https://caelride-api.onrender.com' : 'http://localhost:8000')
  apiHost.value = host.endsWith('/auth') ? host.slice(0, -5) : host

  try {
    const isSecure = window.location.protocol === 'https:' || window.location.hostname === 'localhost'
    biometricAvailable.value = !!(window.PublicKeyCredential && isSecure)
    if (user.value?.username) {
      fingerprintEnabled.value = localStorage.getItem(`fp_${user.value.username}`) === 'true'
    }
  } catch (e) {}

  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('top_up_status_updated', handleTopUpStatusUpdated)
  window.addEventListener('top_up_created', handleTopUpCreated)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('top_up_status_updated', handleTopUpStatusUpdated)
  window.removeEventListener('top_up_created', handleTopUpCreated)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ──────────────────────────────────────────────────────
   RESET & SHELL
────────────────────────────────────────────────────── */
.app-shell {
  display: flex;
  min-height: 100vh;
  min-height: 100dvh;
  height: 100dvh;
  width: 100%;
  max-width: 100vw;
  overflow: hidden;
  background: var(--bg);
  position: relative;
  box-sizing: border-box;
}

/* ──────────────────────────────────────────────────────
   SIDEBAR
────────────────────────────────────────────────────── */
.sidebar {
  width: 64px;
  min-width: 64px;
  height: 100%;
  background: rgba(15, 12, 35, 0.96);
  border-right: 1px solid rgba(139, 92, 246, 0.15);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), min-width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  flex-shrink: 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: 64px;
  min-width: 64px;
}

.sidebar.collapsed .sidebar-brand {
  flex-direction: column-reverse;
  align-items: center;
  gap: 0.75rem;
  padding: 1.1rem 0 0.35rem 0;
  border-bottom: none;
}

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.1rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}

.brand-icon {
  width: 36px; height: 36px;
  background: transparent;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.brand-logo-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.brand-icon:hover .brand-logo-img {
  transform: scale(1.1);
}

.brand-name {
  font-family: 'Outfit', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
  flex: 1;
}

.collapse-btn {
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
.collapse-btn span {
  display: block;
  width: 20px; height: 2px;
  background: var(--text-3);
  border-radius: 2px;
  transition: background 0.18s ease;
}
.collapse-btn:hover { background: rgba(139,92,246,0.1); }
.collapse-btn:hover span { background: #fff; }

.close-btn {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  width: 28px; height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-3);
  cursor: pointer;
  outline: none;
  flex-shrink: 0;
  padding: 0;
}
.close-btn:hover {
  background: rgba(255,255,255,0.12);
  color: #fff;
}

/* Driver mini-profile */
.sidebar-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
  overflow: hidden;
}

.sidebar-profile-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}

.sp-avatar {
  width: 38px; height: 38px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid rgba(139,92,246,0.4);
  display: flex; align-items: center; justify-content: center;
}

.sp-avatar img { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }

.sp-initials {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
}

.sp-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}
.sp-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sp-role {
  font-size: 0.7rem;
  color: var(--primary-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  color: var(--text-2);
  cursor: pointer;
  transition: background 0.18s ease, color 0.18s ease;
  text-align: left;
  width: 100%;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
}

.nav-item:hover {
  background: rgba(139,92,246,0.08);
  color: var(--text-1);
}

.nav-item.active {
  background: rgba(139,92,246,0.15);
  color: #fff;
  border-right: 3px solid var(--primary);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 22px;
}

.nav-label {
  font-size: 0.88rem;
  font-weight: 500;
  white-space: nowrap;
}

.nav-active-dot {
  margin-left: auto;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--primary-light);
  flex-shrink: 0;
}

/* Footer nav */
.sidebar-footer {
  border-top: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}

.nav-logout {
  color: #fca5a5;
}
.nav-logout:hover {
  background: rgba(239,68,68,0.1);
  color: #f87171;
}

/* Sidebar transitions */
.label-fade-enter-active, .label-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.label-fade-enter-from, .label-fade-leave-to {
  opacity: 0;
  transform: translateX(-6px);
}

/* ──────────────────────────────────────────────────────
   CONTENT AREA
────────────────────────────────────────────────────── */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  overflow: hidden;
  min-width: 0;
  box-sizing: border-box;
}

/* Page content wrapper */
.page-content {
  flex: 1;
  width: 100%;
  max-width: 100%;
  overflow-y: auto;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  height: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .page-content {
    padding: 1rem 0.85rem;
    gap: 1rem;
  }
}

.page-header {
  flex-shrink: 0;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-1);
  margin: 0;
}

.page-sub {
  font-size: 0.85rem;
  color: var(--text-2);
  margin: 0.2rem 0 0;
}

/* Page switch transition */
.page-switch-enter-active, .page-switch-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.page-switch-enter-from {
  opacity: 0;
  transform: translateX(12px);
}
.page-switch-leave-to {
  opacity: 0;
  transform: translateX(-12px);
}

/* ──────────────────────────────────────────────────────
   MOBILE TOP BAR
────────────────────────────────────────────────────── */
.mobile-topbar {
  display: none;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  background: rgba(15,12,35,0.97);
  border-bottom: 1px solid rgba(139,92,246,0.15);
  flex-shrink: 0;
}

.mobile-menu-btn {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-1);
  cursor: pointer;
  flex-shrink: 0;
}

.mobile-page-title {
  flex: 1;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mobile-drive-btn, .mobile-logout {
  flex-shrink: 0;
  font-size: 0.82rem;
  padding: 0.4rem 0.75rem;
}

/* Mobile Overlay & Sidebar */
.mobile-overlay {
  position: fixed;
  inset: 0;
  z-index: 900;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(4px);
  display: flex;
}

.mobile-sidebar {
  width: 260px;
  height: 100%;
  background: rgba(15,12,35,0.98);
  border-right: 1px solid rgba(139,92,246,0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.overlay-fade-enter-active, .overlay-fade-leave-active {
  transition: opacity 0.25s ease;
}
.overlay-fade-enter-from, .overlay-fade-leave-to {
  opacity: 0;
}

/* ──────────────────────────────────────────────────────
   HOME PAGE
────────────────────────────────────────────────────── */
.home-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1rem;
  flex: 1;
  min-height: 0;
}

/* Activation banner — full width row */
.activation-banner {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, rgba(217,119,6,0.15), rgba(146,64,14,0.2));
  border: 1px solid rgba(217,119,6,0.4);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.act-left {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  flex: 1;
}

.act-pulse {
  width: 10px; height: 10px;
  background: #f59e0b;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
  animation: pulse-amber 1.8s infinite;
  box-shadow: 0 0 0 0 rgba(245,158,11,0.7);
}

@keyframes pulse-amber {
  0%   { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245,158,11,0.7); }
  70%  { transform: scale(1);    box-shadow: 0 0 0 6px rgba(245,158,11,0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245,158,11,0); }
}

.act-title {
  font-weight: 700;
  color: #f59e0b;
  font-size: 0.95rem;
  margin: 0;
}
.act-desc {
  font-size: 0.82rem;
  color: #fbbf24;
  margin: 0.15rem 0 0;
  line-height: 1.4;
}

/* Wallet Card */
.wallet-card {
  order: 1;
  background: linear-gradient(135deg, rgba(88,28,135,0.5), rgba(30,27,75,0.65));
  border: 1px solid rgba(139,92,246,0.35);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0,0,0,0.3), 0 0 20px rgba(139,92,246,0.12);
  transition: transform 0.3s ease, border-color 0.3s ease;
}
.wallet-card:hover { transform: translateY(-3px); border-color: rgba(139,92,246,0.6); }

.wc-chip {
  width: 36px; height: 26px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 5px;
  opacity: 0.85;
}

.wc-brand {
  font-family: 'Outfit', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: rgba(255,255,255,0.75);
  display: flex;
  align-items: center;
  gap: 8px;
}

.wc-balance-block {
  display: flex;
  flex-direction: column;
  margin-top: 0.5rem;
}
.wc-lbl {
  font-size: 0.68rem;
  text-transform: uppercase;
  color: var(--text-3);
  letter-spacing: 1px;
}
.wc-amount {
  font-family: 'Outfit', sans-serif;
  font-size: 1.7rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 10px rgba(255,255,255,0.1);
}

.wc-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  font-size: 0.72rem;
  color: var(--text-2);
}
.wc-name {
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}
.wc-type { font-weight: 700; color: rgba(255,255,255,0.55); }

/* Wallet Transaction History styling */
.wallet-history-card {
  order: 3;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.wallet-history-card:hover {
  transform: translateY(-3px);
  border-color: rgba(139, 92, 246, 0.4);
}

.wallet-history-card .card-sec-title {
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.wallet-history-card .card-header-with-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 0.75rem;
}

.wallet-history-card .log-filter-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.wallet-history-card .filter-checkboxes {
  display: flex;
  gap: 0.65rem;
}

.wallet-history-card .filter-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  font-size: 0.74rem;
  color: var(--text-2);
  user-select: none;
}

.wallet-history-card .filter-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0; width: 0;
}

.wallet-history-card .checkbox-custom {
  height: 12px;
  width: 12px;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 3px;
  position: relative;
  transition: all 0.2s ease;
}

.wallet-history-card .filter-checkbox-label:hover .checkbox-custom {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
}

.wallet-history-card .checkbox-custom::after {
  content: "";
  position: absolute;
  display: none;
  left: 3.5px;
  top: 0.5px;
  width: 3px;
  height: 6px;
  border: solid #fff;
  border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg);
}

.wallet-history-card .filter-checkbox:checked ~ .checkbox-custom::after {
  display: block;
}

.wallet-history-card .filter-checkbox:checked ~ .checkbox-custom.load {
  background-color: #10b981;
  border-color: #10b981;
}

.wallet-history-card .filter-checkbox:checked ~ .checkbox-custom.fee {
  background-color: #818cf8;
  border-color: #818cf8;
}

.wallet-history-card .filter-text {
  font-weight: 500;
  transition: color 0.2s;
}

.wallet-history-card .filter-checkbox:checked ~ .filter-text {
  color: #fff;
}

.wallet-history-card .filter-date-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 0.15rem 0.4rem;
}

.wallet-history-card .filter-date-icon {
  font-size: 0.72rem;
  opacity: 0.7;
}

.wallet-history-card .filter-date-input {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 0.72rem;
  outline: none;
  cursor: pointer;
}

.wallet-history-card .filter-date-input::-webkit-calendar-picker-indicator {
  filter: invert(1);
  opacity: 0.6;
  cursor: pointer;
}

.wallet-history-card .btn-clear-date {
  background: transparent;
  border: none;
  color: var(--text-3);
  cursor: pointer;
  font-size: 0.7rem;
  padding: 0 0.1rem;
}

.wallet-history-card .btn-clear-date:hover {
  color: #ef4444;
}

.wallet-history-card {
  order: 3;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  transition: transform 0.3s ease, border-color 0.3s ease;
  flex: 1;
  min-height: 0;
  width: 100%;
}

.wallet-history-card .audit-logs-feed {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  min-height: 0;
  max-height: none;
  overflow-y: auto;
  padding-right: 0.25rem;
  cursor: grab;
  user-select: none;
  touch-action: none;
  width: 100%;
}

.wallet-history-card .audit-logs-feed::-webkit-scrollbar {
  width: 4px;
}
.wallet-history-card .audit-logs-feed::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.01);
}
.wallet-history-card .audit-logs-feed::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.2);
  border-radius: 4px;
}

.wallet-history-card .empty-audit-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 2.5rem 1rem;
  color: var(--text-3);
  font-size: 0.78rem;
}

.wallet-history-card .audit-log-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.02);
  background: rgba(255, 255, 255, 0.01);
  font-size: 0.78rem;
  transition: border-color 0.2s, background 0.2s;
}

.wallet-history-card .audit-log-row:hover {
  border-color: rgba(139, 92, 246, 0.15);
  background: rgba(255, 255, 255, 0.02);
}

.wallet-history-card .audit-log-row.load {
  border-left: 3px solid #10b981;
}

.wallet-history-card .audit-log-row.fee {
  border-left: 3px solid #818cf8;
}

.wallet-history-card .audit-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.wallet-history-card .audit-icon-wrap {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
}

.wallet-history-card .audit-icon-wrap.load {
  background: rgba(16, 185, 129, 0.12);
}

.wallet-history-card .audit-icon-wrap.fee {
  background: rgba(129, 140, 248, 0.12);
}

.wallet-history-card .audit-desc-col {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.wallet-history-card .audit-desc-title {
  font-weight: 600;
  color: #fff;
  font-size: 0.8rem;
}

.wallet-history-card .audit-time {
  font-size: 0.7rem;
  color: var(--text-3);
}

.wallet-history-card .audit-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.15rem;
}

.wallet-history-card .audit-amount {
  font-weight: 700;
  font-size: 0.85rem;
  font-family: 'Outfit', sans-serif;
}

.wallet-history-card .audit-amount.deposit {
  color: #10b981;
}

.wallet-history-card .audit-amount.deduct {
  color: #ef4444;
}

.wallet-history-card .audit-bal-lbl {
  font-size: 0.68rem;
  color: var(--text-2);
}

/* Ride History styling */
.ride-history-card {
  order: 4;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.ride-history-card:hover {
  transform: translateY(-3px);
  border-color: rgba(139, 92, 246, 0.4);
}

.ride-history-card .card-sec-title {
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.ride-history-card .card-header-with-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 0.75rem;
}

.ride-history-card .log-filter-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.ride-history-card .filter-checkboxes {
  display: flex;
  gap: 0.65rem;
}

.ride-history-card .filter-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  font-size: 0.74rem;
  color: var(--text-2);
  user-select: none;
}

.ride-history-card .filter-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0; width: 0;
}

.ride-history-card .checkbox-custom {
  height: 12px;
  width: 12px;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 3px;
  position: relative;
  transition: all 0.2s ease;
}

.ride-history-card .filter-checkbox-label:hover .checkbox-custom {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
}

.ride-history-card .checkbox-custom::after {
  content: "";
  position: absolute;
  display: none;
  left: 3.5px;
  top: 0.5px;
  width: 3px;
  height: 6px;
  border: solid #fff;
  border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg);
}

.ride-history-card .filter-checkbox:checked ~ .checkbox-custom::after {
  display: block;
}

.ride-history-card .filter-checkbox:checked ~ .checkbox-custom.passenger {
  background-color: #10b981;
  border-color: #10b981;
}

.ride-history-card .filter-checkbox:checked ~ .checkbox-custom.document {
  background-color: #818cf8;
  border-color: #818cf8;
}

.ride-history-card .filter-text {
  font-weight: 500;
  transition: color 0.2s;
}

.ride-history-card .filter-checkbox:checked ~ .filter-text {
  color: #fff;
}

.ride-history-card .filter-date-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 0.15rem 0.4rem;
}

.ride-history-card .filter-date-icon {
  font-size: 0.72rem;
  opacity: 0.7;
}

.ride-history-card .filter-date-input {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 0.72rem;
  outline: none;
  cursor: pointer;
}

.ride-history-card .filter-date-input::-webkit-calendar-picker-indicator {
  filter: invert(1);
  opacity: 0.6;
  cursor: pointer;
}

.ride-history-card .btn-clear-date {
  background: transparent;
  border: none;
  color: var(--text-3);
  cursor: pointer;
  font-size: 0.7rem;
  padding: 0 0.1rem;
}

.ride-history-card .btn-clear-date:hover {
  color: #ef4444;
}

.ride-history-card .audit-logs-feed {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 250px;
  overflow-y: auto;
  padding-right: 0.25rem;
  cursor: grab;
  user-select: none;
  touch-action: none;
}

.audit-logs-feed.grabbing {
  cursor: grabbing !important;
  user-select: none !important;
}

.ride-history-card .audit-logs-feed::-webkit-scrollbar {
  width: 4px;
}
.ride-history-card .audit-logs-feed::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.01);
}
.ride-history-card .audit-logs-feed::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.2);
  border-radius: 4px;
}

.ride-history-card .empty-audit-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 2.5rem 1rem;
  color: var(--text-3);
  font-size: 0.78rem;
}

.ride-history-card .audit-log-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.02);
  background: rgba(255, 255, 255, 0.01);
  font-size: 0.78rem;
  transition: border-color 0.2s, background 0.2s;
}

.ride-history-card .audit-log-row:hover {
  border-color: rgba(139, 92, 246, 0.15);
  background: rgba(255, 255, 255, 0.02);
}

.ride-history-card .audit-log-row.passenger {
  border-left: 3px solid #10b981;
}

.ride-history-card .audit-log-row.document {
  border-left: 3px solid #818cf8;
}

.ride-history-card .audit-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.ride-history-card .audit-icon-wrap {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
}

.ride-history-card .audit-icon-wrap.passenger {
  background: rgba(16, 185, 129, 0.12);
}

.ride-history-card .audit-icon-wrap.document {
  background: rgba(129, 140, 248, 0.12);
}

.ride-history-card .audit-desc-col {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.ride-history-card .audit-desc-title {
  font-weight: 600;
  color: #fff;
  font-size: 0.8rem;
}

.ride-history-card .audit-time {
  font-size: 0.7rem;
  color: var(--text-3);
}

.ride-history-card .audit-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.ride-history-card .audit-amount {
  font-weight: 700;
  font-size: 0.85rem;
  font-family: 'Outfit', sans-serif;
}

.ride-history-card .status-badge {
  display: inline-block;
}

.ride-history-card .status-badge.completed {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.ride-history-card .status-badge.cancelled {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Ride Card */
.ride-card {
  order: 2;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.ride-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-1);
  margin: 0;
}

.auto-accept-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  padding: 0.65rem 0.85rem;
  border-radius: var(--radius-sm);
}
.aa-label { font-size: 0.85rem; font-weight: 500; color: var(--text-1); }

.btn-drive {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding: 0.85rem;
  background: linear-gradient(135deg, #27ae60, #1e8449);
  border: none;
  border-radius: var(--radius-sm);
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 16px rgba(39,174,96,0.3);
  margin-top: auto;
}

/* Premium Parallax Wave Effect */
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
.btn-drive:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(39,174,96,0.45);
}
.btn-drive:active:not(:disabled) { transform: translateY(0); }
.btn-drive:disabled {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: var(--text-3) !important;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.mobile-drive-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px; height: 26px;
  flex-shrink: 0;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: rgba(255,255,255,0.1);
  border: 1px solid var(--border);
  border-radius: 34px;
  transition: 0.3s;
}
.toggle-slider:before {
  content: "";
  position: absolute;
  height: 18px; width: 18px;
  left: 3px; bottom: 3px;
  background: var(--text-2);
  border-radius: 50%;
  transition: 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.toggle-switch input:checked + .toggle-slider { background: rgba(39,174,96,0.2); border-color: #27ae60; }
.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(22px);
  background: #2ecc71;
  box-shadow: 0 0 8px rgba(46,204,113,0.6);
}

/* ──────────────────────────────────────────────────────
   PROFILE PAGE
────────────────────────────────────────────────────── */
.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  border-radius: var(--radius-md);
  max-width: 480px;
  width: 100%;
  align-self: flex-start;
}

.profile-avatar-wrap { display: flex; justify-content: center; }

.profile-avatar {
  width: 100px; height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(139,92,246,0.5);
  box-shadow: 0 0 0 6px rgba(139,92,246,0.1);
  display: flex; align-items: center; justify-content: center;
}
.profile-avatar img { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
.profile-initials {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
}

.profile-fields {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  width: 100%;
}

.pf-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.7rem 0.9rem;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
}
.pf-lbl {
  font-size: 0.78rem;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  white-space: nowrap;
  flex-shrink: 0;
}
.pf-val {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-1);
  text-align: right;
  word-break: break-all;
}

.role-badge {
  background: rgba(139,92,246,0.15);
  border: 1px solid rgba(139,92,246,0.3);
  color: #c084fc;
  padding: 0.15rem 0.6rem;
  border-radius: 99px;
  font-size: 0.72rem;
  font-weight: 600;
}

.status-pending { color: #f59e0b; }

.fingerprint-section { width: 100%; }

.btn-fingerprint {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(139,92,246,0.1);
  border: 1px solid rgba(139,92,246,0.3);
  border-radius: var(--radius-sm);
  color: var(--primary-light);
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 500;
  transition: background 0.2s, border-color 0.2s;
}
.btn-fingerprint:hover { background: rgba(139,92,246,0.2); border-color: rgba(139,92,246,0.5); }

.fingerprint-linked {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--success);
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.5rem 0;
}

/* ──────────────────────────────────────────────────────
   DOCUMENT PAGES (License / OR / CR)
────────────────────────────────────────────────────── */
.doc-page-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  flex: 1;
  min-height: 0;
  align-items: start;
}

.doc-image-panel {
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  position: relative;
  aspect-ratio: 4/3;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.2);
}

.doc-full-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}
.doc-image-panel:hover .doc-full-img { transform: scale(1.03); }

.doc-view-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  color: #fff;
  text-align: center;
  padding: 1rem 0.5rem 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.doc-image-panel:hover .doc-view-overlay { opacity: 1; }

.doc-no-img {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-3);
  font-size: 0.85rem;
  padding: 2rem;
}
.doc-no-img span { font-size: 2.5rem; }
.doc-no-img p { margin: 0; }

.doc-info-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-card {
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding: 0.65rem 0.8rem;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
}

.info-lbl {
  font-size: 0.68rem;
  text-transform: uppercase;
  color: var(--text-3);
  letter-spacing: 0.5px;
}
.info-val {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-1);
  word-break: break-all;
}
.info-val.highlight {
  font-family: 'Outfit', monospace;
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary-light);
  letter-spacing: 0.5px;
}
.text-success { color: var(--success); }

/* ──────────────────────────────────────────────────────
   LIGHTBOX
────────────────────────────────────────────────────── */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0,0,0,0.92);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  backdrop-filter: blur(8px);
}

.lightbox-box {
  position: relative;
  max-width: min(90vw, 900px);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.lb-img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
  border: 1px solid rgba(255,255,255,0.1);
}

.lb-close {
  position: absolute;
  top: -3rem; right: 0;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 50%;
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}
.lb-close:hover { background: rgba(255,255,255,0.2); transform: scale(1.1); }

.lb-caption {
  color: rgba(255,255,255,0.65);
  font-size: 0.82rem;
  text-align: center;
}

.lb-fade-enter-active, .lb-fade-leave-active { transition: opacity 0.22s ease; }
.lb-fade-enter-from, .lb-fade-leave-to { opacity: 0; }

/* ──────────────────────────────────────────────────────
   RESPONSIVE — MOBILE
────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  /* Hide desktop sidebar on mobile */
  .sidebar { display: none; }

  /* Show mobile topbar */
  .mobile-topbar { display: flex; }

  /* Full-height content */
  .content-area { height: 100dvh; }

  .page-content {
    padding: 1rem;
    gap: 0.85rem;
  }

  /* Home: stack cards */
  .home-grid {
    grid-template-columns: 1fr;
  }

  /* Document pages: stack vertically */
  .doc-page-layout {
    grid-template-columns: 1fr;
  }

  .doc-image-panel {
    aspect-ratio: 16/10;
  }

  .profile-card {
    max-width: 100%;
  }

  .lb-close { top: -2.5rem; }
}

@media (max-width: 480px) {
  .page-content { padding: 0.75rem; }
  .wc-amount { font-size: 1.5rem; }
  .page-title { font-size: 1.25rem; }
}
</style>

<style>
/* ── Floating Chat Toast ─────────────────────────── */
.chat-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  border-radius: 18px;
  background: rgba(15, 11, 42, 0.95);
  border: 1px solid rgba(139, 92, 246, 0.4);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5), 0 0 15px rgba(139, 92, 246, 0.25);
  z-index: 99999;
  cursor: pointer;
  max-width: 320px;
  transition: transform 0.2s, border-color 0.2s;
}
.chat-toast:hover {
  transform: translateY(-2px);
  border-color: var(--primary-light);
}
.toast-icon {
  font-size: 1.5rem;
}
.toast-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
  text-align: left;
}
.toast-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--primary-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.toast-text {
  font-size: 0.9rem;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}
.toast-arrow {
  color: var(--primary-light);
  font-weight: bold;
  margin-left: auto;
}

/* Toast Slide Transition */
.toast-slide-enter-active {
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s;
}
.toast-slide-leave-active {
  transition: transform 0.25s ease-in, opacity 0.2s;
}
.toast-slide-enter-from {
  transform: translateY(-30px) scale(0.9);
  opacity: 0;
}
.toast-slide-leave-to {
  transform: translateY(-20px) scale(0.95);
  opacity: 0;
}

/* ── Bell Icon & Notification Dropdown ───────────── */
.ride-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  width: 100%;
}
.ride-card-header .ride-title {
  margin-bottom: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bell-container {
  position: relative;
}
.bell-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s, transform 0.15s;
}
.bell-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.05);
}
.bell-btn:active {
  transform: scale(0.95);
}
.bell-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #ff4757;
  color: #fff;
  font-size: 0.68rem;
  font-weight: bold;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notif-dropdown {
  position: absolute;
  top: 48px;
  right: 0;
  width: 280px;
  max-height: 350px;
  border-radius: 16px;
  background: rgba(15, 11, 42, 0.98);
  border: 1px solid rgba(139, 92, 246, 0.3);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
  z-index: 10000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.notif-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  font-weight: 700;
  font-size: 0.85rem;
  color: #fff;
}
.notif-clear-btn {
  background: transparent;
  border: none;
  color: var(--primary-light);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}
.notif-clear-btn:hover {
  text-decoration: underline;
}

.notif-list {
  overflow-y: auto;
  flex: 1;
}
.notif-empty {
  padding: 30px 16px;
  text-align: center;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.85rem;
}
.notif-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: left;
}
.notif-item:hover {
  background: rgba(255, 255, 255, 0.05);
}
.notif-dot {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}
.notif-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.notif-text {
  font-size: 0.85rem;
  color: #fff;
  line-height: 1.35;
  word-break: break-word;
}
.notif-time {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.45);
}

/* Transitions */
.notif-fade-enter-active {
  transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.15s;
}
.notif-fade-leave-active {
  transition: transform 0.15s ease-in, opacity 0.12s;
}
.notif-fade-enter-from {
  transform: translateY(-10px) scale(0.95);
  opacity: 0;
}
.notif-fade-leave-to {
  transform: translateY(-8px) scale(0.97);
  opacity: 0;
}

/* GCash Modal & Portal Styling */
.gcash-modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(12px);
  padding: 1rem;
  overflow-y: auto;
  box-sizing: border-box;
}

.gcash-card {
  width: 100%;
  max-width: 440px;
  max-height: min(92vh, 720px);
  display: flex;
  flex-direction: column;
  background: rgba(30, 41, 59, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  animation: modal-enter 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin: auto;
  box-sizing: border-box;
}

@keyframes modal-enter {
  from { transform: scale(0.9) translateY(20px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}

.gcash-step {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.gcash-header-blue {
  background: #0056eb;
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.gcash-logo {
  font-family: 'Outfit', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.5px;
}

.gcash-title {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.85rem;
  font-weight: 600;
  background: rgba(255,255,255,0.15);
  padding: 4px 10px;
  border-radius: 12px;
}

.gcash-body {
  padding: 1.5rem;
}

.gcash-section-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.gcash-presets {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 1.25rem;
}

.preset-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 10px 0;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
}

.preset-btn.active {
  background: #0056eb;
  border-color: #0056eb;
  box-shadow: 0 4px 12px rgba(0, 86, 235, 0.3);
}

.gcash-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 0 1rem;
  margin-bottom: 1.25rem;
}

.currency-prefix {
  font-size: 1.4rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  margin-right: 6px;
}

.gcash-amount-input {
  width: 100%;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  color: #fff !important;
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  padding: 12px 0 !important;
}

.gcash-phone-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 12px 1rem;
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  outline: none;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.gcash-phone-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.gcash-help-text {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.4;
}

.gcash-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-gcash-next {
  background: #0056eb !important;
  color: #fff !important;
  border: none !important;
  padding: 10px 24px !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

.btn-gcash-next:hover:not(:disabled) {
  background: #0044bd !important;
  transform: translateY(-1px);
}

.btn-gcash-next:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Simulated GCash Portal */
.gcash-header-portal {
  background: #0056eb;
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 4px solid #0044bd;
}

.gcash-portal-brand {
  font-size: 1.5rem;
  font-weight: 900;
  color: #fff;
  font-family: 'Outfit', sans-serif;
  letter-spacing: -0.5px;
}

.gcash-portal-secure {
  font-size: 0.72rem;
  font-weight: 700;
  color: #a7f3d0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.portal-bg {
  background: #f3f4f6;
  color: #1f2937;
}

.gcash-portal-merchant {
  display: flex;
  justify-content: space-between;
  padding: 1rem 1.25rem 0.5rem;
  border-bottom: 1px dashed #d1d5db;
}

.merchant-lbl, .amount-lbl {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
}

.merchant-val {
  font-size: 0.85rem;
  font-weight: 700;
  color: #111827;
}

.gcash-portal-amount {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1.25rem 1rem;
}

.amount-val {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0056eb;
}

.gcash-portal-form {
  background: #fff;
  padding: 1.5rem 1.25rem;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.portal-input-lbl {
  font-size: 0.78rem;
  font-weight: 700;
  color: #374151;
  display: block;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.portal-input-box {
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  padding: 0 10px;
}

.ph-prefix {
  font-size: 1.1rem;
  font-weight: 700;
  color: #4b5563;
  margin-right: 8px;
}

.portal-phone {
  width: 100%;
  border: none !important;
  background: transparent !important;
  padding: 12px 0 !important;
  font-size: 1.1rem !important;
  font-weight: 700 !important;
  color: #111827 !important;
  outline: none !important;
}

.portal-disclaimer {
  font-size: 0.7rem;
  color: #6b7280;
  margin-top: 0.85rem;
  line-height: 1.4;
}

.portal-actions {
  padding: 1.25rem;
  display: flex;
  gap: 12px;
  justify-content: space-between;
  background: #e5e7eb;
}

.btn-portal-back {
  background: transparent;
  border: 1px solid #9ca3af;
  color: #4b5563;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-portal-back:hover {
  background: rgba(0, 0, 0, 0.05);
}

.btn-portal-next, .btn-portal-pay {
  background: #0056eb;
  border: none;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  padding: 10px 28px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-portal-next:hover, .btn-portal-pay:hover {
  background: #0044bd;
}

.btn-portal-next:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* OTP Verification Screen */
.otp-instruction {
  font-size: 0.85rem;
  color: #374151;
  text-align: center;
  padding: 1.25rem 1.25rem 0.5rem;
  line-height: 1.5;
}

.otp-inputs {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 1rem 1.25rem;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.otp-digit-box {
  width: 44px;
  height: 48px;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  text-align: center;
  font-size: 1.4rem;
  font-weight: 700;
  color: #111827;
  outline: none;
}

.otp-digit-box:focus {
  border-color: #0056eb;
  background: #eff6ff;
}

.otp-helpers {
  display: flex;
  justify-content: center;
  padding: 0.75rem;
}

.btn-otp-shortcut {
  background: rgba(0, 86, 235, 0.1);
  border: 1px dashed #0056eb;
  color: #0056eb;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-otp-shortcut:hover {
  background: #0056eb;
  color: #fff;
}

.otp-resend {
  font-size: 0.75rem;
  color: #6b7280;
  text-align: center;
  padding: 0.5rem 1.25rem 1.25rem;
}

.timer-span {
  font-weight: 700;
  color: #dc2626;
}

/* MPIN Authentication */
.mpin-instruction {
  font-size: 0.9rem;
  font-weight: 700;
  color: #374151;
  text-align: center;
  padding-top: 1.25rem;
}

.mpin-bullets {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 1rem 1.25rem 1.25rem;
}

.mpin-bullet {
  width: 14px;
  height: 14px;
  border: 2px solid #9ca3af;
  border-radius: 50%;
  background: transparent;
  transition: all 0.15s ease;
}

.mpin-bullet.filled {
  background: #0056eb;
  border-color: #0056eb;
  transform: scale(1.15);
}

.mpin-keypad {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  max-width: 280px;
  margin: 0 auto 1.5rem;
  padding: 0 1rem;
}

.keypad-btn {
  background: #fff;
  border: 1px solid #e5e7eb;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 700;
  padding: 12px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.1s, transform 0.1s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.keypad-btn:active {
  background: #eff6ff;
  transform: scale(0.96);
}

.keypad-btn.spec {
  background: #e5e7eb;
  font-size: 0.95rem;
  color: #4b5563;
}

/* Review & Confirm */
.payment-review-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  margin: 1.25rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.review-lbl {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.review-amt {
  font-size: 2.2rem;
  font-weight: 900;
  color: #111827;
  font-family: 'Outfit', sans-serif;
  margin-bottom: 0.85rem;
}

.review-divider {
  height: 1px;
  background: #f3f4f6;
  margin-bottom: 0.85rem;
}

.review-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.review-row span {
  color: #6b7280;
}

.review-row strong {
  color: #1f2937;
  font-weight: 600;
}

.review-info {
  font-size: 0.72rem;
  color: #6b7280;
  text-align: center;
  padding: 0 1.25rem;
  line-height: 1.45;
}

/* Processing View */
.processing-step {
  background: rgba(15, 23, 42, 0.9);
  padding: 3rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 380px;
}

.gcash-processing-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.gcash-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255,255,255,0.1);
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: gcash-spin 1s linear infinite;
  margin-bottom: 1.5rem;
}

@keyframes gcash-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.processing-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
}

.processing-desc {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.6);
}

/* Success Receipt */
.gcash-receipt-wrapper {
  background: #f8fafc;
  color: #0f172a;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.receipt-success-badge {
  width: 56px;
  height: 56px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
  margin-bottom: 1rem;
  animation: badge-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes badge-pop {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.receipt-heading {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.25rem;
}

.receipt-sub {
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 1.5rem;
}

.receipt-card {
  width: 100%;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  margin-bottom: 1.5rem;
}

.receipt-amount-row {
  background: #eff6ff;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rcpt-lbl {
  font-size: 0.8rem;
  font-weight: 600;
  color: #1e3a8a;
  text-transform: uppercase;
}

.rcpt-amt {
  font-size: 1.4rem;
  font-weight: 800;
  color: #1d4ed8;
  font-family: 'Outfit', sans-serif;
}

.receipt-details {
  padding: 1.25rem;
}

.rcpt-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  margin-bottom: 0.65rem;
}

.rcpt-row:last-child {
  margin-bottom: 0;
}

.rcpt-row span {
  color: #64748b;
}

.rcpt-row strong {
  color: #0f172a;
  font-weight: 600;
}

.btn-receipt-done {
  width: 100%;
  background: #0056eb;
  border: none;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  padding: 12px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(0, 86, 235, 0.2);
}

.btn-receipt-done:hover {
  background: #0044bd;
  transform: translateY(-1px);
}

/* Wallet Card Load Action */
.wc-topup-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
  outline: none;
}

.wc-topup-btn:hover {
  background: #0056eb;
  border-color: #0056eb;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 86, 235, 0.4);
}

.wc-topup-btn:active {
  transform: scale(0.98);
}

/* QR code checkout additions */
.qr-display-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  margin: 1.25rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.qr-pay-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.qr-gcash-logo {
  font-size: 1.25rem;
  font-weight: 900;
  color: #0056eb;
  font-family: 'Outfit', sans-serif;
}
.qr-pay-label {
  font-size: 0.72rem;
  color: #6b7280;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.qr-image-wrapper {
  background: #eff6ff;
  border: 4px solid #eff6ff;
  border-radius: 14px;
  padding: 12px;
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
}
.gcash-qr-image {
  width: 100%;
  max-width: 220px;
  height: auto;
  max-height: 230px;
  object-fit: contain;
  display: block;
  margin: 0 auto;
}
.btn-download-qr {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0.5rem auto 0.75rem;
  padding: 0.45rem 1.1rem;
  background: linear-gradient(135deg, #0056eb, #1a7ef5);
  color: #fff;
  font-size: 0.8rem;
  font-weight: 700;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 8px rgba(0, 86, 235, 0.35);
  transition: transform 0.15s, box-shadow 0.15s, background 0.15s;
}
.btn-download-qr:hover {
  background: linear-gradient(135deg, #0047cc, #0056eb);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 86, 235, 0.45);
}
.btn-download-qr:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 86, 235, 0.3);
}
.qr-pay-details {
  width: 100%;
  background: #f9fafb;
  border-radius: 8px;
  padding: 0.85rem;
}
.qr-details-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin-bottom: 0.45rem;
}
.qr-details-row:last-child {
  margin-bottom: 0;
}
.qr-det-lbl {
  color: #6b7280;
}
.qr-det-val {
  color: #1f2937;
  font-weight: 600;
}
.amount-highlight {
  font-size: 0.95rem;
  color: #0056eb;
  font-weight: 800;
}
.qr-instructions {
  background: rgba(245, 158, 11, 0.08);
  border: 1px dashed rgba(245, 158, 11, 0.3);
  border-radius: 8px;
  padding: 1rem;
  margin: 0 1.25rem 1.25rem;
  color: #78350f;
  text-align: left;
}
.instr-title {
  font-size: 0.8rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 4px;
}
.instr-list {
  font-size: 0.75rem;
  padding-left: 1.15rem;
  margin: 0;
  line-height: 1.45;
}
.instr-list li {
  margin-bottom: 0.25rem;
}
.instr-list li:last-child {
  margin-bottom: 0;
}
.ref-input-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem 1.25rem;
  margin: 1.25rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  text-align: left;
}
.ref-code-input {
  width: 100%;
  background: #f9fafb;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  padding: 12px 1rem;
  color: #111827;
  font-size: 1.3rem;
  font-weight: 800;
  letter-spacing: 2px;
  text-align: center;
  outline: none;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
.ref-code-input:focus {
  border-color: #0056eb;
  background: #eff6ff;
}
.ref-input-help {
  font-size: 0.72rem;
  color: #6b7280;
  margin: 0;
}
/* GCash Modal & Portal Styling */
.gcash-modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(12px);
  padding: 1rem;
  overflow-y: auto;
  box-sizing: border-box;
}

.gcash-card {
  width: 100%;
  max-width: 440px;
  max-height: min(92vh, 720px);
  display: flex;
  flex-direction: column;
  background: rgba(30, 41, 59, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  animation: modal-enter 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin: auto;
  box-sizing: border-box;
}

@keyframes modal-enter {
  from { transform: scale(0.9) translateY(20px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}

.gcash-step {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.gcash-header-blue {
  background: #0056eb;
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.gcash-logo {
  font-family: 'Outfit', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.5px;
}

.gcash-title {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.85rem;
  font-weight: 600;
  background: rgba(255,255,255,0.15);
  padding: 4px 10px;
  border-radius: 12px;
}

.gcash-body {
  padding: 1.25rem;
  flex: 1;
  overflow-y: auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}
.gcash-body::-webkit-scrollbar {
  width: 6px;
}
.gcash-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

@media (max-height: 680px) {
  .gcash-card {
    max-height: 96vh;
    border-radius: 12px;
  }
  .gcash-body {
    padding: 0.85rem;
  }
  .qr-display-card {
    padding: 0.65rem;
    margin: 0.35rem 0;
  }
  .qr-pay-header {
    margin-bottom: 0.4rem;
  }
  .qr-gcash-logo-img {
    height: 32px !important;
  }
  .gcash-qr-image {
    max-width: 120px;
    max-height: 14vh;
  }
  .btn-download-qr {
    margin: 0.25rem auto 0.4rem;
    padding: 0.35rem 0.85rem;
    font-size: 0.75rem;
  }
  .qr-instructions {
    padding: 0.5rem 0.75rem;
    margin: 0.35rem 0;
  }
}

.gcash-section-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.gcash-presets {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 1.25rem;
}

.preset-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 10px 0;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
}

.preset-btn.active {
  background: #0056eb;
  border-color: #0056eb;
  box-shadow: 0 4px 12px rgba(0, 86, 235, 0.3);
}

.gcash-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 0 1rem;
  margin-bottom: 1.25rem;
}

.currency-prefix {
  font-size: 1.4rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  margin-right: 6px;
}

.gcash-amount-input {
  width: 100%;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  color: #fff !important;
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  padding: 12px 0 !important;
}

.gcash-phone-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 12px 1rem;
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  outline: none;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.gcash-phone-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.gcash-help-text {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.4;
}

.gcash-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-gcash-next {
  background: #0056eb !important;
  color: #fff !important;
  border: none !important;
  padding: 10px 24px !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

.btn-gcash-next:hover:not(:disabled) {
  background: #0044bd !important;
  transform: translateY(-1px);
}

.btn-gcash-next:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Simulated GCash Portal */
.gcash-header-portal {
  background: #0056eb;
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 4px solid #0044bd;
}

.gcash-portal-brand {
  font-size: 1.5rem;
  font-weight: 900;
  color: #fff;
  font-family: 'Outfit', sans-serif;
  letter-spacing: -0.5px;
}

.gcash-portal-secure {
  font-size: 0.72rem;
  font-weight: 700;
  color: #a7f3d0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.portal-bg {
  background: #f3f4f6;
  color: #1f2937;
}

.gcash-portal-merchant {
  display: flex;
  justify-content: space-between;
  padding: 1rem 1.25rem 0.5rem;
  border-bottom: 1px dashed #d1d5db;
}

.merchant-lbl, .amount-lbl {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
}

.merchant-val {
  font-size: 0.85rem;
  font-weight: 700;
  color: #111827;
}

.gcash-portal-amount {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1.25rem 1rem;
}

.amount-val {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0056eb;
}

.gcash-portal-form {
  background: #fff;
  padding: 1.5rem 1.25rem;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.portal-input-lbl {
  font-size: 0.78rem;
  font-weight: 700;
  color: #374151;
  display: block;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.portal-input-box {
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  padding: 0 10px;
}

.ph-prefix {
  font-size: 1.1rem;
  font-weight: 700;
  color: #4b5563;
  margin-right: 8px;
}

.portal-phone {
  width: 100%;
  border: none !important;
  background: transparent !important;
  padding: 12px 0 !important;
  font-size: 1.1rem !important;
  font-weight: 700 !important;
  color: #111827 !important;
  outline: none !important;
}

.portal-disclaimer {
  font-size: 0.7rem;
  color: #6b7280;
  margin-top: 0.85rem;
  line-height: 1.4;
}

.portal-actions {
  padding: 1.25rem;
  display: flex;
  gap: 12px;
  justify-content: space-between;
  background: #e5e7eb;
}

.btn-portal-back {
  background: transparent;
  border: 1px solid #9ca3af;
  color: #4b5563;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-portal-back:hover {
  background: rgba(0, 0, 0, 0.05);
}

.btn-portal-next, .btn-portal-pay {
  background: #0056eb;
  border: none;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  padding: 10px 28px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-portal-next:hover, .btn-portal-pay:hover {
  background: #0044bd;
}

.btn-portal-next:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* OTP Verification Screen */
.otp-instruction {
  font-size: 0.85rem;
  color: #374151;
  text-align: center;
  padding: 1.25rem 1.25rem 0.5rem;
  line-height: 1.5;
}

.otp-inputs {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 1rem 1.25rem;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.otp-digit-box {
  width: 44px;
  height: 48px;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  text-align: center;
  font-size: 1.4rem;
  font-weight: 700;
  color: #111827;
  outline: none;
}

.otp-digit-box:focus {
  border-color: #0056eb;
  background: #eff6ff;
}

.otp-helpers {
  display: flex;
  justify-content: center;
  padding: 0.75rem;
}

.btn-otp-shortcut {
  background: rgba(0, 86, 235, 0.1);
  border: 1px dashed #0056eb;
  color: #0056eb;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-otp-shortcut:hover {
  background: #0056eb;
  color: #fff;
}

.otp-resend {
  font-size: 0.75rem;
  color: #6b7280;
  text-align: center;
  padding: 0.5rem 1.25rem 1.25rem;
}

.timer-span {
  font-weight: 700;
  color: #dc2626;
}

/* MPIN Authentication */
.mpin-instruction {
  font-size: 0.9rem;
  font-weight: 700;
  color: #374151;
  text-align: center;
  padding-top: 1.25rem;
}

.mpin-bullets {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 1rem 1.25rem 1.25rem;
}

.mpin-bullet {
  width: 14px;
  height: 14px;
  border: 2px solid #9ca3af;
  border-radius: 50%;
  background: transparent;
  transition: all 0.15s ease;
}

.mpin-bullet.filled {
  background: #0056eb;
  border-color: #0056eb;
  transform: scale(1.15);
}

.mpin-keypad {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  max-width: 280px;
  margin: 0 auto 1.5rem;
  padding: 0 1rem;
}

.keypad-btn {
  background: #fff;
  border: 1px solid #e5e7eb;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 700;
  padding: 12px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.1s, transform 0.1s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.keypad-btn:active {
  background: #eff6ff;
  transform: scale(0.96);
}

.keypad-btn.spec {
  background: #e5e7eb;
  font-size: 0.95rem;
  color: #4b5563;
}

/* Review & Confirm */
.payment-review-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  margin: 1.25rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.review-lbl {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.review-amt {
  font-size: 2.2rem;
  font-weight: 900;
  color: #111827;
  font-family: 'Outfit', sans-serif;
  margin-bottom: 0.85rem;
}

.review-divider {
  height: 1px;
  background: #f3f4f6;
  margin-bottom: 0.85rem;
}

.review-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.review-row span {
  color: #6b7280;
}

.review-row strong {
  color: #1f2937;
  font-weight: 600;
}

/* QR Code enlargement styling details */
.qr-large-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #fff;
  padding: 12px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}
.gcash-qr-large-img {
  width: 100%;
  max-width: 320px;
  height: auto;
  border-radius: 6px;
  display: block;
  transition: transform 0.2s ease;
}
.gcash-qr-large-img:hover {
  transform: scale(1.02);
}
.qr-quick-info {
  background: #fff;
  border-radius: 8px;
  padding: 10px 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  text-align: left;
}
.quick-info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  margin-bottom: 4px;
}
.quick-info-row:last-child {
  margin-bottom: 0;
}
.quick-info-row span {
  color: #6b7280;
  font-weight: 500;
}
.quick-info-row strong {
  color: #1f2937;
  font-weight: 700;
}
.highlight-price {
  color: #0056eb !important;
  font-size: 0.95rem;
}

/* Preset Selection grid and select amount card styles */
.gcash-presets-five {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  margin-bottom: 1.25rem;
}
.gcash-selected-amount-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.selected-amt-lbl {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
}
.selected-amt-val {
  font-size: 1.5rem;
  font-weight: 800;
  color: #10b981;
  font-family: 'Outfit', sans-serif;
}

/* Glowing and rotating plus icon in Top Up button */
.plus-icon {
  color: #38bdf8; /* Sky Blue/Cyan colored icon */
  font-size: 1.25rem;
  font-weight: 900;
  line-height: 1;
  display: inline-block;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.wc-topup-btn:hover .plus-icon {
  transform: rotate(90deg) scale(1.15); /* Spin and scale on button hover! */
  color: #00ecff; /* Even brighter cyan on hover */
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
</style>

