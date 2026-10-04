import { useState } from 'react'

const navigationItems = [
  { label: 'Dashboard', icon: '⌂' },
  { label: 'Students', icon: '◉' },
  { label: 'Teachers', icon: '▣' },
  { label: 'Classes', icon: '▤' },
  { label: 'Attendance', icon: '✓' },
]

const stats = [
  { label: 'Total students', value: '1,248', change: '+8.2%', tone: 'blue' },
  { label: 'Teachers', value: '86', change: '+4.6%', tone: 'purple' },
  { label: 'Classes', value: '42', change: '+2.4%', tone: 'green' },
  { label: 'Attendance today', value: '94.8%', change: '+1.8%', tone: 'orange' },
]

const Dashboard = ({ username, role, onLogout }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [activePage, setActivePage] = useState('Dashboard')

  return (
    <div className={`dashboard-shell ${isSidebarOpen ? '' : 'sidebar-collapsed'}`}>
      <aside className="dashboard-sidebar">
        <div className="dashboard-brand">
          <span className="dashboard-brand-mark">SM</span>
          {isSidebarOpen && <span>School portal</span>}
        </div>

        <nav className="dashboard-nav" aria-label="Main navigation">
          {navigationItems.map((item) => (
            <button
              className={activePage === item.label ? 'active' : ''}
              key={item.label}
              onClick={() => setActivePage(item.label)}
              title={!isSidebarOpen ? item.label : undefined}
              type="button"
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              {isSidebarOpen && <span>{item.label}</span>}
            </button>
          ))}
        </nav>

        <button className="logout-button" onClick={onLogout} type="button">
          <span className="nav-icon" aria-hidden="true">↪</span>
          {isSidebarOpen && <span>Log out</span>}
        </button>
      </aside>

      <section className="dashboard-content">
        <header className="dashboard-header">
          <button
            className="sidebar-toggle"
            onClick={() => setIsSidebarOpen((open) => !open)}
            type="button"
            aria-label={isSidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            ☰
          </button>
          <div className="dashboard-user">
            <span className="user-avatar">{username.charAt(0).toUpperCase()}</span>
            <div>
              <strong>{username}</strong>
              <span>Role: {role.charAt(0).toUpperCase() + role.slice(1)}</span>
            </div>
          </div>
        </header>

        <main className="dashboard-main">
          <div className="dashboard-title">
            <div>
              <p className="dashboard-eyebrow">Overview</p>
              <h1>{activePage}</h1>
              <p>Here is what is happening in your school today.</p>
            </div>
            <button className="dashboard-action" type="button">+ Add new</button>
          </div>

          <div className="stats-grid">
            {stats.map((stat) => (
              <article className="stat-card" key={stat.label}>
                <div className={`stat-icon ${stat.tone}`}>{stat.label.charAt(0)}</div>
                <div>
                  <p>{stat.label}</p>
                  <strong>{stat.value}</strong>
                  <span className="stat-change">{stat.change} this month</span>
                </div>
              </article>
            ))}
          </div>

          <div className="dashboard-panels">
            <article className="dashboard-panel">
              <div className="panel-heading">
                <div>
                  <h2>Attendance overview</h2>
                  <p>Weekly attendance summary</p>
                </div>
                <span className="panel-period">This week</span>
              </div>
              <div className="attendance-chart" aria-label="Attendance chart">
                {[72, 84, 68, 91, 86, 94, 78].map((height, index) => (
                  <div className="chart-column" key={index}>
                    <div className="chart-bar" style={{ height: `${height}%` }} />
                    <span>{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index]}</span>
                  </div>
                ))}
              </div>
            </article>

            <article className="dashboard-panel activity-panel">
              <div className="panel-heading">
                <div>
                  <h2>Recent activity</h2>
                  <p>Latest updates from your school</p>
                </div>
              </div>
              <div className="activity-item"><span className="activity-dot blue" /><p><strong>New student registered</strong><span>Emma Wilson joined Grade 8</span></p><time>10m</time></div>
              <div className="activity-item"><span className="activity-dot purple" /><p><strong>Attendance updated</strong><span>Grade 10 attendance was marked</span></p><time>32m</time></div>
              <div className="activity-item"><span className="activity-dot green" /><p><strong>Class schedule changed</strong><span>Science class moved to Room 204</span></p><time>1h</time></div>
            </article>
          </div>
        </main>
      </section>
    </div>
  )
}

export default Dashboard
