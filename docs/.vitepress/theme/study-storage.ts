// 学习数据持久化：localStorage 读写工具
// 四个 key 共同支撑「继续学习 / 收藏 / 掌握状态」体系
//   ik:reading-progress  每篇文章的滚动比例 + 标题 + 最近更新时间
//   ik:recent            最近访问的文章（用于"继续学习"）
//   ik:bookmarks         收藏的文章路径
//   ik:mastery           每篇文章的掌握状态 mastered | learning | todo

const KEYS = {
  progress: 'ik:reading-progress',
  recent: 'ik:recent',
  bookmarks: 'ik:bookmarks',
  mastery: 'ik:mastery',
  reviewReminders: 'ik:review-reminders'
}

const MAX_PROGRESS = 100
const MAX_RECENT = 30

function read<T>(key: string, fallback: T): T {
  try {
    const v = localStorage.getItem(key)
    return v ? (JSON.parse(v) as T) : fallback
  } catch {
    return fallback
  }
}

function write(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch {
    /* 配额满或禁用：静默失败 */
  }
}

/* reading progress */
type ProgressEntry = { scrollRatio: number; title: string; updatedAt: number }
export function getProgress(): Record<string, ProgressEntry> {
  return read(KEYS.progress, {})
}
export function setProgress(path: string, title: string, scrollRatio: number) {
  const all = getProgress()
  all[path] = { scrollRatio, title, updatedAt: Date.now() }
  const entries = Object.entries(all)
  if (entries.length > MAX_PROGRESS) {
    entries.sort((a, b) => b[1].updatedAt - a[1].updatedAt)
    write(KEYS.progress, Object.fromEntries(entries.slice(0, MAX_PROGRESS)))
  } else {
    write(KEYS.progress, all)
  }
}

/* recent */
type RecentEntry = { path: string; title: string; visitedAt: number }
export function getRecent(): RecentEntry[] {
  return read(KEYS.recent, [])
}
export function pushRecent(path: string, title: string) {
  const list = getRecent().filter((r) => r.path !== path)
  list.unshift({ path, title, visitedAt: Date.now() })
  write(KEYS.recent, list.slice(0, MAX_RECENT))
}

/* bookmarks */
export function getBookmarks(): string[] {
  return read(KEYS.bookmarks, [])
}
export function isBookmarked(path: string): boolean {
  return getBookmarks().includes(path)
}
export function toggleBookmark(path: string): boolean {
  const list = getBookmarks()
  const i = list.indexOf(path)
  let active: boolean
  if (i >= 0) {
    list.splice(i, 1)
    active = false
  } else {
    list.unshift(path)
    active = true
  }
  write(KEYS.bookmarks, list)
  return active
}

/* mastery */
type Mastery = 'mastered' | 'learning' | 'todo'
export function getMastery(): Record<string, Mastery> {
  return read(KEYS.mastery, {})
}
export function getMasteryOf(path: string): Mastery {
  return getMastery()[path] || 'todo'
}
export function setMastery(path: string, state: Mastery) {
  const all = getMastery()
  if (state === 'todo') delete all[path]
  else all[path] = state
  write(KEYS.mastery, all)
}

/* review reminders (spaced repetition) */
const INTERVALS = [1, 3, 7]

type ReviewReminder = {
  path: string
  title: string
  masteredAt: number
  remindAt: number
  stage: number
}

export function getReviewReminders(): Record<string, ReviewReminder> {
  return read(KEYS.reviewReminders, {})
}

export function scheduleReview(path: string, title: string) {
  const all = getReviewReminders()
  const now = Date.now()
  const days = INTERVALS[0]
  const remindAt = now + days * 24 * 60 * 60 * 1000
  all[path] = { path, title, masteredAt: now, remindAt, stage: 0 }
  write(KEYS.reviewReminders, all)
}

export function getDueReviews(): ReviewReminder[] {
  const all = getReviewReminders()
  const now = Date.now()
  return Object.values(all).filter(r => r.remindAt <= now && r.stage < INTERVALS.length)
}

export function advanceReview(path: string) {
  const all = getReviewReminders()
  const r = all[path]
  if (!r) return
  if (r.stage >= INTERVALS.length - 1) {
    delete all[path]
  } else {
    const nextStage = r.stage + 1
    const days = INTERVALS[nextStage]
    r.stage = nextStage
    r.remindAt = Date.now() + days * 24 * 60 * 60 * 1000
    all[path] = r
  }
  write(KEYS.reviewReminders, all)
}

export function cancelReview(path: string) {
  const all = getReviewReminders()
  delete all[path]
  write(KEYS.reviewReminders, all)
}
