import Sidebar from './Sidebar';
import TopNav from './TopNav';
import { Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="bg-background text-on-surface dark:bg-slate-900 dark:text-slate-100 min-h-screen transition-colors duration-200">
      <Sidebar />
      <TopNav />
      <main className="ml-[260px] pt-16 min-h-screen">
        <Outlet />
      </main>
    </div>
  );
}
