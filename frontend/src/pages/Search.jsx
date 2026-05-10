export default function Search() {
  return (
    <div className="max-w-[1200px] mx-auto p-container-margin">
      {/* Search Hero Section */}
      <section className="mb-stack-lg">
        <div className="bg-white dark:bg-slate-800 p-8 rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm mb-12 relative overflow-hidden transition-colors duration-200">
          <div className="relative z-10">
            <h3 className="font-headline-md text-headline-md text-on-surface dark:text-slate-100 mb-2">Semantic Candidate Search</h3>
            <p className="font-body-md text-body-md text-on-surface-variant dark:text-slate-400 mb-8 max-w-2xl">Describe your ideal candidate in natural language. Our AI analyzes technical depth, experience velocity, and cultural alignment from across your database.</p>
            
            <div className="flex flex-col gap-4 p-4 bg-surface-container-low dark:bg-slate-800 rounded-xl border border-outline-variant dark:border-slate-700 focus-within:ring-2 focus-within:ring-primary transition-all">
              <div className="flex-1 relative">
                <textarea 
                  className="w-full h-32 bg-transparent border-none focus:ring-0 font-body-md text-body-md text-on-surface dark:text-slate-100 placeholder:text-outline resize-none" 
                  placeholder="Paste the job description or specific key requirements here to semantic search across the dataset..."
                ></textarea>
                <div className="absolute bottom-1 right-2 flex items-center gap-stack-sm">
                  <span className="font-label-caps text-label-caps text-on-surface-variant">0 / 5000 characters</span>
                </div>
              </div>
              <div className="flex justify-end pt-2 border-t border-outline-variant/50 dark:border-slate-700/50">
                <button className="bg-primary text-on-primary px-8 py-3 rounded-lg font-label-caps text-label-caps flex items-center gap-2 hover:opacity-95 shadow-md active:scale-95 transition-all">
                  <span className="material-symbols-outlined" data-icon="search">search</span>
                  Search Database
                </button>
              </div>
            </div>
            
            <div className="mt-4 flex gap-2 overflow-x-auto pb-2">
              <span className="font-label-caps text-label-caps text-on-surface-variant flex items-center py-1">SUGGESTED:</span>
              <button className="px-3 py-1 bg-secondary-container/30 text-secondary dark:text-secondary-fixed-dim border border-secondary-container rounded-full font-label-caps text-[10px] hover:bg-secondary-container/50 transition-colors">Frontend Architect</button>
              <button className="px-3 py-1 bg-secondary-container/30 text-secondary dark:text-secondary-fixed-dim border border-secondary-container rounded-full font-label-caps text-[10px] hover:bg-secondary-container/50 transition-colors">Machine Learning Lead</button>
              <button className="px-3 py-1 bg-secondary-container/30 text-secondary dark:text-secondary-fixed-dim border border-secondary-container rounded-full font-label-caps text-[10px] hover:bg-secondary-container/50 transition-colors">DevOps Engineer</button>
            </div>
          </div>
          <div className="absolute -top-24 -right-24 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>
        </div>
      </section>

      {/* Results Header */}
      <div className="flex justify-between items-end mb-6">
        <div>
          <span className="font-label-caps text-label-caps text-primary dark:text-primary-fixed-dim tracking-widest uppercase">Query Results</span>
          <h4 className="font-title-sm text-title-sm text-on-surface dark:text-slate-100">128 Candidates Found</h4>
        </div>
        <div className="flex gap-stack-sm">
          <button className="flex items-center gap-2 px-4 py-2 border border-outline-variant dark:border-slate-700 rounded-lg font-label-caps text-label-caps text-secondary dark:text-slate-400 hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors">
            <span className="material-symbols-outlined text-[18px]" data-icon="filter_list">filter_list</span>
            Filters
          </button>
        </div>
      </div>

      {/* Candidate Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-stack-lg">
        {/* Candidate Card 1 */}
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-outline-variant dark:border-slate-700 hover:border-primary/40 dark:hover:border-primary-fixed-dim/40 hover:shadow-lg transition-all duration-300 group">
          <div className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex gap-4">
                <div className="relative">
                  <img alt="Candidate 1 Avatar" className="w-12 h-12 rounded-lg object-cover bg-surface-container-high" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCogmCw6EZLnxky5DEcUAi0z7ppZP6Pa-PHNIiuLPgl6E_xUq5h6XC3KX6o8GZOO-np8eTFcFHY5dgBDzLnnz6tyrK4orijoSMoSmEsVWEyH_U2VRYmKrvxbq5geWnUVo0JNEwm0krjZhFlO0JvMgPlGMz_a_CzrdjxzXmQGLEGRr34mrLtXaA2IPXv8D6VIDso08E8SlP2QieR6sIAe5zzScjBl4-MS7iJ2AbsMUl0LdRQLXqDogsP7in9dO7uaE7N0WS_sKvAE_0N"/>
                  <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white dark:border-surface-dim rounded-full" title="Available"></div>
                </div>
                <div>
                  <h5 className="font-title-sm text-title-sm text-on-surface dark:text-slate-100 group-hover:text-primary dark:group-hover:text-primary-fixed-dim transition-colors">Sarah K. Jenkins</h5>
                  <p className="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400">Principal Software Engineer</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-label-caps text-[10px] text-outline mt-1">High Velocity</p>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-2 mb-6">
              <div className="bg-surface-container-low dark:bg-slate-800 p-2 rounded-lg">
                <p className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase">Tech Fit</p>
                <div className="w-full bg-surface-variant dark:bg-slate-800-highest h-1 rounded-full overflow-hidden">
                  <div className="bg-primary h-full" style={{ width: '95%' }}></div>
                </div>
              </div>
              <div className="bg-surface-container-low dark:bg-slate-800 p-2 rounded-lg">
                <p className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase">Leadership</p>
                <div className="w-full bg-surface-variant dark:bg-slate-800-highest h-1 rounded-full overflow-hidden">
                  <div className="bg-primary h-full" style={{ width: '88%' }}></div>
                </div>
              </div>
              <div className="bg-surface-container-low dark:bg-slate-800 p-2 rounded-lg">
                <p className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase">Growth</p>
                <div className="w-full bg-surface-variant dark:bg-slate-800-highest h-1 rounded-full overflow-hidden">
                  <div className="bg-primary h-full" style={{ width: '92%' }}></div>
                </div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-6">
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">Rust</span>
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">Distributed Systems</span>
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">Kubernetes</span>
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">Kafka</span>
            </div>
            
            <div className="flex gap-3">
              <button className="flex-1 bg-primary-container/10 dark:bg-primary-container/20 text-primary dark:text-primary-fixed-dim border border-primary-container/20 py-2.5 rounded-lg font-label-caps text-label-caps hover:bg-primary-container/20 transition-colors flex items-center justify-center gap-2">
                <span className="material-symbols-outlined text-[18px]" data-icon="description">description</span>
                View Resume
              </button>
              <button className="p-2.5 border border-outline-variant dark:border-slate-700 rounded-lg text-secondary dark:text-slate-400 hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]" data-icon="bookmark">bookmark</span>
              </button>
            </div>
          </div>
        </div>

        {/* Candidate Card 2 */}
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-outline-variant dark:border-slate-700 hover:border-primary/40 dark:hover:border-primary-fixed-dim/40 hover:shadow-lg transition-all duration-300 group">
          <div className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex gap-4">
                <div className="relative">
                  <img alt="Candidate 2 Avatar" className="w-12 h-12 rounded-lg object-cover bg-surface-container-high" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAG3GF9Dv0OU3IKbfcuZE03VAzuivbnBqh8rUXKP0vaSlUIYG9zarwAsCjiFIP6_ff_rcoHzFVjD2VqLVfo_zTbp4KhaKzGVwp5KDk7w6i4TrhFJV6Zk-hdddo1iD-bIsNQ2VIBUrZMUmCL-63BAyays-AMjiSIa2o_185tF4yHcY9a_mGlMZPUPMLdDYXe6R22ihSgwHrOtc-q-ci74ivxr9TfNMuOx7IxG6ub_QtEJtwTOhSZFP-QwOuKa2hJVANOLbtvFtGXMp5B"/>
                  <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-orange-500 border-2 border-white dark:border-surface-dim rounded-full" title="In Interview"></div>
                </div>
                <div>
                  <h5 className="font-title-sm text-title-sm text-on-surface dark:text-slate-100 group-hover:text-primary dark:group-hover:text-primary-fixed-dim transition-colors">Marcus Rivera</h5>
                  <p className="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400">Senior Distributed Systems Lead</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-label-caps text-[10px] text-outline mt-1">Expert Level</p>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-2 mb-6">
              <div className="bg-surface-container-low dark:bg-slate-800 p-2 rounded-lg">
                <p className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase">Tech Fit</p>
                <div className="w-full bg-surface-variant dark:bg-slate-800-highest h-1 rounded-full overflow-hidden">
                  <div className="bg-primary h-full" style={{ width: '90%' }}></div>
                </div>
              </div>
              <div className="bg-surface-container-low dark:bg-slate-800 p-2 rounded-lg">
                <p className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase">Leadership</p>
                <div className="w-full bg-surface-variant dark:bg-slate-800-highest h-1 rounded-full overflow-hidden">
                  <div className="bg-primary h-full" style={{ width: '95%' }}></div>
                </div>
              </div>
              <div className="bg-surface-container-low dark:bg-slate-800 p-2 rounded-lg">
                <p className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase">Growth</p>
                <div className="w-full bg-surface-variant dark:bg-slate-800-highest h-1 rounded-full overflow-hidden">
                  <div className="bg-primary h-full" style={{ width: '75%' }}></div>
                </div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-6">
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">Go</span>
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">C++</span>
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">AWS</span>
              <span className="px-2 py-1 bg-surface-container dark:bg-slate-800-highest text-on-surface-variant rounded font-label-caps text-[10px]">NoSQL</span>
            </div>
            
            <div className="flex gap-3">
              <button className="flex-1 bg-primary-container/10 dark:bg-primary-container/20 text-primary dark:text-primary-fixed-dim border border-primary-container/20 py-2.5 rounded-lg font-label-caps text-label-caps hover:bg-primary-container/20 transition-colors flex items-center justify-center gap-2">
                <span className="material-symbols-outlined text-[18px]" data-icon="description">description</span>
                View Resume
              </button>
              <button className="p-2.5 border border-outline-variant dark:border-slate-700 rounded-lg text-secondary dark:text-slate-400 hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]" data-icon="bookmark">bookmark</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Pagination / Load More */}
      <div className="mt-12 flex justify-center mb-20">
        <button className="px-12 py-4 bg-white dark:bg-surface border border-outline-variant dark:border-slate-700 text-primary dark:text-primary-fixed-dim font-label-caps text-label-caps rounded-xl hover:bg-surface-container-low dark:hover:bg-slate-700 hover:border-primary transition-all flex items-center gap-2 shadow-sm">
          Load More Candidates
          <span className="material-symbols-outlined text-[18px]" data-icon="keyboard_arrow_down">keyboard_arrow_down</span>
        </button>
      </div>

      {/* FAB */}
      <div className="fixed bottom-8 right-8 z-50">
        <button className="w-14 h-14 bg-primary text-on-primary rounded-full shadow-2xl flex items-center justify-center hover:scale-105 active:scale-95 transition-all group">
          <span className="material-symbols-outlined" data-icon="chat">chat</span>
          <span className="absolute right-16 bg-inverse-surface text-inverse-on-surface px-4 py-2 rounded-lg font-label-caps text-[11px] opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">Ask AI Recruiter</span>
        </button>
      </div>
    </div>
  );
}
