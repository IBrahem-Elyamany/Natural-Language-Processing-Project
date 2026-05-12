import { Link, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="fixed left-0 top-0 h-full w-[260px] bg-surface-container-lowest dark:bg-slate-800 border-r border-outline-variant dark:border-slate-700 shadow-sm dark:shadow-none flex flex-col py-container-margin z-50 transition-colors duration-200">
      <div className="px-gutter mb-stack-lg">
        <div className="flex items-center gap-stack-sm">
          <span className="material-symbols-outlined text-primary font-bold text-headline-md" data-icon="hub">hub</span>
          <span className="font-title-sm text-title-sm font-bold text-primary dark:text-primary-fixed-dim">ROMI</span>
        </div>
        <p className="font-label-caps text-label-caps text-on-surface-variant mt-1 uppercase tracking-wider">Executive Suite</p>
      </div>

      <nav className="flex-1 space-y-1">
        <Link 
          to="/" 
          className={`flex items-center gap-stack-md px-gutter py-stack-md transition-all duration-200 ${
            location.pathname === '/' 
            ? 'text-primary dark:text-primary-fixed-dim font-semibold border-l-4 border-primary bg-primary-container/10 active:scale-[0.98]' 
            : 'text-secondary dark:text-slate-400 font-medium hover:bg-surface-container-low dark:hover:bg-slate-700'
          }`}
        >
          <span className="material-symbols-outlined" data-icon="dashboard">dashboard</span>
          <span className="font-body-md text-body-md">Dashboard</span>
        </Link>

        <Link 
          to="/Database" 
          className={`flex items-center gap-stack-md px-gutter py-stack-md transition-all duration-200 ${
            location.pathname === '/Database' 
            ? 'text-primary dark:text-primary-fixed-dim font-semibold border-l-4 border-primary bg-primary-container/10 active:scale-[0.98]' 
            : 'text-secondary dark:text-slate-400 font-medium hover:bg-surface-container-low dark:hover:bg-slate-700'
          }`}
        >
          <span className="material-symbols-outlined" data-icon="database" style={location.pathname === '/search' ? { fontVariationSettings: "'FILL' 1" } : {}}>database</span>
          <span className="font-body-md text-body-md">Database</span>
        </Link>

      </nav>

      <div className="px-gutter mt-auto">
        <button className="w-full py-stack-md px-stack-lg bg-primary text-on-primary rounded-lg font-label-caps text-label-caps hover:bg-primary-container transition-all active:scale-[0.98] flex items-center justify-center gap-stack-sm">
          <span className="material-symbols-outlined text-[18px]" data-icon="add">add</span>
          Post New Job
        </button>

        <div className="mt-stack-lg flex items-center gap-stack-sm pt-stack-lg border-t border-outline-variant">
          <img 
            alt="Recruiter Profile" 
            className="w-10 h-10 rounded-full bg-surface-variant object-cover" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuBL35dWNQGGxfeRTlcVS3ZJJzPjPPbsdEwuXUbgK6RJqbV9rWz7XQcLKjeCF1l27wIZvjOR_-Lcybt_iWZ_Z5GQhu48Bn-qABESvQGyzCsxWk_LdAsLRZktQlLK6aAcmt_kyVxGu8iCI60nldgdIPXYjb1xW7niWoB3KnPAz3IFEP8EW6ivwe00gkBGX9ss6gjUEkckDJIGphqmL3H9c3xez2RhKlmPAfowt6lTLcitUd4l73uCsj4pQdt5sochbzBgXrQUG9Ape6Go"
          />
          <div className="overflow-hidden">
            <p className="font-body-sm text-body-sm font-bold truncate dark:text-slate-100">Alex Chen</p>
            <p className="font-label-caps text-label-caps text-on-surface-variant truncate">Senior Lead</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
