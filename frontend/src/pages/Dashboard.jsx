import { useState } from 'react';

export default function Dashboard() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [evaluationReport, setEvaluationReport] = useState('');
  const [totalCvs, setTotalCvs] = useState(0);
  const [searched, setSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setEvaluationReport('');
    setResults([]);
    try {
      const formData = new FormData();
      formData.append('input', query);

      const response = await fetch('http://localhost:8000/api/v2/search', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      setResults(data.results || []);
      setEvaluationReport(data.evaluation_report || '');
      setTotalCvs(data.total_cvs_in_db || 0);
      setSearched(true);
    } catch (error) {
      console.error(error);
      alert('Search failed. Ensure the backend is running and CVs are uploaded.');
    } finally {
      setLoading(false);
    }
  };

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
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                ></textarea>
                <div className="absolute bottom-1 right-2 flex items-center gap-stack-sm">
                  <span className="font-label-caps text-label-caps text-on-surface-variant">{query.length} / 5000 characters</span>
                </div>
              </div>
              <div className="flex justify-end pt-2 border-t border-outline-variant/50 dark:border-slate-700/50">
                <button 
                  onClick={handleSearch}
                  disabled={loading}
                  className="bg-primary text-on-primary px-8 py-3 rounded-lg font-label-caps text-label-caps flex items-center gap-2 hover:opacity-95 shadow-md active:scale-95 transition-all disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  <span className="material-symbols-outlined" data-icon={loading ? "hourglass_empty" : "search"}>
                    {loading ? "hourglass_empty" : "search"}
                  </span>
                  {loading ? 'Searching...' : 'Search Database'}
                </button>
              </div>
            </div>
            
            <div className="mt-4 flex gap-2 overflow-x-auto pb-2">
              <span className="font-label-caps text-label-caps text-on-surface-variant flex items-center py-1">SUGGESTED:</span>
              <button onClick={() => setQuery("Frontend Architect with React and Node.js experience")} className="px-3 py-1 bg-secondary-container/30 text-secondary dark:text-secondary-fixed-dim border border-secondary-container rounded-full font-label-caps text-[10px] hover:bg-secondary-container/50 transition-colors">Frontend Architect</button>
              <button onClick={() => setQuery("Machine Learning Lead with PyTorch and Transformers experience")} className="px-3 py-1 bg-secondary-container/30 text-secondary dark:text-secondary-fixed-dim border border-secondary-container rounded-full font-label-caps text-[10px] hover:bg-secondary-container/50 transition-colors">Machine Learning Lead</button>
              <button onClick={() => setQuery("DevOps Engineer with Kubernetes and AWS")} className="px-3 py-1 bg-secondary-container/30 text-secondary dark:text-secondary-fixed-dim border border-secondary-container rounded-full font-label-caps text-[10px] hover:bg-secondary-container/50 transition-colors">DevOps Engineer</button>
            </div>
          </div>
          <div className="absolute -top-24 -right-24 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>
        </div>
      </section>

      {/* Evaluation Report (if any) */}
      {searched && evaluationReport && (
        <div className="mb-12 p-6 bg-primary-container/10 dark:bg-slate-800 rounded-xl border border-primary/20 dark:border-slate-700">
          <h4 className="font-title-md text-title-md text-primary dark:text-primary-fixed-dim mb-4 flex items-center gap-2">
            <span className="material-symbols-outlined">auto_awesome</span>
            AI Evaluation Report
          </h4>
          <div className="font-body-md text-body-md text-on-surface dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
            {evaluationReport}
          </div>
        </div>
      )}

      {/* Results Header */}
      {searched && (
        <div className="flex justify-between items-end mb-6">
          <div>
            <span className="font-label-caps text-label-caps text-primary dark:text-primary-fixed-dim tracking-widest uppercase">Query Results</span>
            <h4 className="font-title-sm text-title-sm text-on-surface dark:text-slate-100">{results.length} Candidates Found</h4>
          </div>
          <div className="flex gap-stack-sm">
            <button className="flex items-center gap-2 px-4 py-2 border border-outline-variant dark:border-slate-700 rounded-lg font-label-caps text-label-caps text-secondary dark:text-slate-400 hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors">
              <span className="material-symbols-outlined text-[18px]" data-icon="filter_list">filter_list</span>
              Filters
            </button>
          </div>
        </div>
      )}

      {/* Candidate Grid */}
      {searched && results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-stack-lg mb-20">
          {results.map((candidate, idx) => (
            <div key={idx} className="bg-white dark:bg-slate-800 rounded-xl border border-outline-variant dark:border-slate-700 hover:border-primary/40 dark:hover:border-primary-fixed-dim/40 hover:shadow-lg transition-all duration-300 group flex flex-col">
              <div className="p-6 flex-1 flex flex-col">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex gap-4">
                    <div className="relative">
                      <div className="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center text-primary font-bold text-xl uppercase">
                        {candidate.filename.charAt(0)}
                      </div>
                    </div>
                    <div>
                      <h5 className="font-title-sm text-title-sm text-on-surface dark:text-slate-100 group-hover:text-primary dark:group-hover:text-primary-fixed-dim transition-colors truncate max-w-[200px]" title={candidate.filename}>
                        {candidate.filename}
                      </h5>
                      <p className="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400">Rank: #{candidate.rank}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-label-caps text-[10px] text-outline mt-1">Dist: {candidate.distance.toFixed(4)}</p>
                  </div>
                </div>
                
                <div className="mb-6 flex-1 overflow-hidden">
                  <p className="font-body-sm text-body-sm text-on-surface dark:text-slate-300 line-clamp-4 leading-relaxed">
                    {candidate.snippet}
                  </p>
                </div>
                
                <div className="flex gap-3 mt-auto">
                  <button className="flex-1 bg-primary-container/10 dark:bg-primary-container/20 text-primary dark:text-primary-fixed-dim border border-primary-container/20 py-2.5 rounded-lg font-label-caps text-label-caps hover:bg-primary-container/20 transition-colors flex items-center justify-center gap-2">
                    <span className="material-symbols-outlined text-[18px]" data-icon="description">description</span>
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {searched && results.length === 0 && !loading && (
        <div className="text-center py-12 text-on-surface-variant">
          <p>No candidates found for this query.</p>
        </div>
      )}

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
