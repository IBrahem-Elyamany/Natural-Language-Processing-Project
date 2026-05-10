import { useTheme } from '../context/ThemeContext';

export default function TopNav({ title = "Recruitment Intelligence" }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="fixed top-0 right-0 left-[260px] h-16 bg-surface/80 dark:bg-slate-800/80 backdrop-blur-md border-b border-outline-variant dark:border-slate-700 flex justify-between items-center px-gutter z-40 transition-colors duration-200">
      <div className="flex items-center gap-stack-md flex-1">
        <h2 className="font-title-sm text-title-sm font-bold text-primary dark:text-primary-fixed-dim hidden md:block">
          {title}
        </h2>
        {/* Search bar from the dashboard, only visible if not on search page maybe? Or keep it global */}
        <div className="relative w-full max-w-md focus-within:ring-2 focus-within:ring-primary rounded-full transition-all ml-4">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant" data-icon="search">search</span>
          <input 
            className="w-full pl-10 pr-4 py-2 bg-surface-container-low dark:bg-slate-800 border-none rounded-full font-body-sm text-body-sm focus:outline-none focus:ring-0 dark:text-slate-100" 
            placeholder="Search candidates or jobs..." 
            type="text"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-stack-md">
        <button 
          onClick={toggleTheme}
          className="p-2 text-on-surface-variant hover:bg-surface-variant/50 dark:hover:bg-inverse-surface/20 rounded-full transition-all flex items-center justify-center"
          title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
        >
          <span className="material-symbols-outlined" data-icon={theme === 'light' ? 'dark_mode' : 'light_mode'}>
            {theme === 'light' ? 'dark_mode' : 'light_mode'}
          </span>
        </button>
        
        <button className="p-2 text-on-surface-variant hover:bg-surface-variant/50 dark:hover:bg-inverse-surface/20 rounded-full transition-all flex items-center justify-center">
          <span className="material-symbols-outlined" data-icon="notifications">notifications</span>
        </button>
        <button className="p-2 text-on-surface-variant hover:bg-surface-variant/50 dark:hover:bg-inverse-surface/20 rounded-full transition-all flex items-center justify-center">
          <span className="material-symbols-outlined" data-icon="help">help</span>
        </button>
        <button className="p-2 text-on-surface-variant hover:bg-surface-variant/50 dark:hover:bg-inverse-surface/20 rounded-full transition-all flex items-center justify-center">
          <span className="material-symbols-outlined" data-icon="apps">apps</span>
        </button>
        
        <div className="h-8 w-px bg-outline-variant dark:bg-outline mx-2"></div>
        
        <img 
          alt="User Avatar" 
          className="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold text-xs object-cover" 
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuAWTzF7AqucjGB_xXsYXGr41ngiF6SYEzcUrNaQNnQxgoPerRjFYp8scf9HARooFJAKavkhVTkBPL24OVIi4MYaOExSgw3vn6CyF4adn_s65t3Jk78h3LbzetdIkir3IfW-Ar1YX7UbVd5D6_tkRXt5d2aM5ramuducYI1UGrFrvEUtSHZ0MWPFZTB46mc52iUsOlLH3GX0Pf1ideDlbkHWMZjADC42gDavTMJ1YLAdGRTiiwasrr4jctBHljYR0K8z5xMy-C9XZVnJ"
        />
      </div>
    </header>
  );
}
