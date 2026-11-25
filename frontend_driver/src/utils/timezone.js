/**
 * Global Timezone Configuration for Manila (Asia/Manila / UTC+8)
 */
export const MANILA_TIMEZONE = 'Asia/Manila'

/**
 * Returns YYYY-MM-DD date string in Manila timezone (Asia/Manila)
 */
export function getManilaDateString(date = new Date()) {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('en-CA', { timeZone: MANILA_TIMEZONE })
}

/**
 * Returns formatted 12-hour time string (e.g. "08:30 AM") in Manila timezone
 */
export function getManilaTimeString(date = new Date(), options = {}) {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleTimeString('en-US', {
    timeZone: MANILA_TIMEZONE,
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    ...options
  })
}

/**
 * Returns formatted date and time string in Manila timezone
 */
export function getManilaDateTimeString(date = new Date()) {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleString('en-US', {
    timeZone: MANILA_TIMEZONE,
    month: 'short',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

/**
 * Formats any date using Manila timezone with custom options
 */
export function formatInManila(date, options = {}) {
  if (!date) return '--'
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleString('en-US', {
    timeZone: MANILA_TIMEZONE,
    ...options
  })
}
