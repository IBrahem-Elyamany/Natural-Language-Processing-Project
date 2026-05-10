import React, { useState } from 'react';

export default function Dashboard() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [matchLimit, setMatchLimit] = useState(5);

  const handleFileUpload = (e) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files);
      setUploadedFiles(prev => [...prev, ...newFiles]);
    }
  };
  return (
    <div className="max-w-[1200px] mx-auto p-container-margin">
      {/* Hero Section / Upload Area */}
      <section className="mb-stack-lg">
        <div className="flex flex-col md:flex-row gap-gutter">
          {/* Resume Upload (Left) */}
          <div className="flex-1 bg-surface-container-lowest dark:bg-slate-800 p-stack-lg rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm flex flex-col transition-colors duration-200">
            <div className="mb-stack-md">
              <h2 className="font-headline-md text-headline-md text-primary dark:text-primary-fixed-dim mb-1">Resume Batch</h2>
              <p className="font-body-sm text-body-sm text-on-surface-variant">Upload PDF resumes to evaluate against job criteria.</p>
            </div>
            <div className="flex-1 border-2 border-dashed border-outline-variant dark:border-slate-700 rounded-lg flex flex-col items-center justify-center p-stack-lg hover:border-primary dark:hover:border-primary-fixed-dim hover:bg-primary/5 transition-all group cursor-pointer relative">
              <input type="file" multiple className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" onChange={handleFileUpload} />
              <div className="w-12 h-12 bg-primary-fixed dark:bg-primary-container rounded-full flex items-center justify-center mb-stack-md group-hover:scale-110 transition-transform">
                <span className="material-symbols-outlined text-primary dark:text-primary-fixed-dim" data-icon="upload">upload</span>
              </div>
              <p className="font-body-md text-body-md font-semibold text-primary dark:text-primary-fixed-dim">
                {uploadedFiles.length > 0 ? `${uploadedFiles.length} Resumes Uploaded` : "Drop resumes here"}
              </p>
              <p className="font-label-caps text-label-caps text-on-surface-variant mt-1">PDF, DOCX up to 10MB</p>
            </div>
          </div>
          
          {/* Job Description (Right) */}
          <div className="flex-[1.5] bg-surface-container-lowest dark:bg-slate-800 p-stack-lg rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm transition-colors duration-200">
            <div className="flex justify-between items-center mb-stack-md">
              <div>
                <h2 className="font-headline-md text-headline-md text-primary dark:text-primary-fixed-dim mb-1">Job Description</h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Define core competencies and requirements.</p>
              </div>
              <button className="flex items-center gap-1 text-primary dark:text-primary-fixed-dim font-semibold hover:underline">
                <span className="material-symbols-outlined text-sm" data-icon="history">history</span>
                <span className="font-label-caps text-label-caps">Recent Drafts</span>
              </button>
            </div>
            <div className="relative">
              <textarea 
                className="w-full h-40 bg-surface dark:bg-slate-800 border border-outline-variant dark:border-slate-700 rounded-lg p-stack-md font-body-md text-body-md focus:ring-2 focus:ring-primary dark:text-slate-100 transition-all resize-none" 
                placeholder="Paste the job description or specific key requirements here..."
              ></textarea>
              <div className="absolute bottom-3 right-3 flex items-center gap-stack-sm">
                <span className="font-label-caps text-label-caps text-on-surface-variant">0 / 5000 characters</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Action Bar */}
        <div className="mt-stack-lg flex justify-center">
          <button className="bg-primary text-on-primary px-stack-lg py-4 rounded-lg flex items-center gap-stack-md hover:shadow-lg transition-all active:scale-[0.98]">
            <span className="material-symbols-outlined" data-icon="auto_awesome">auto_awesome</span>
            <span className="font-title-sm text-title-sm">Match Resumes</span>
          </button>
        </div>
      </section>

      {/* Results Section */}
      <section className="bg-surface-container-lowest dark:bg-slate-800 rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm overflow-hidden transition-colors duration-200">
        <div className="px-gutter py-stack-md border-b border-outline-variant dark:border-slate-700 flex justify-between items-center bg-surface-container-low/30 dark:bg-slate-800/30">
          <div className="flex items-center gap-4">
            <h3 className="font-title-sm text-title-sm text-primary dark:text-primary-fixed-dim">Matching Results</h3>
            <div className="flex items-center gap-2">
              <span className="text-sm text-on-surface-variant dark:text-slate-300">Top</span>
              <input 
                type="number" 
                min="1"
                value={matchLimit} 
                onChange={(e) => setMatchLimit(Number(e.target.value))}
                className="w-16 bg-surface dark:bg-slate-700 border border-outline-variant dark:border-slate-600 rounded text-sm text-on-surface-variant dark:text-slate-100 py-1 px-2 focus:ring-primary focus:border-primary outline-none"
              />
              <span className="text-sm text-on-surface-variant dark:text-slate-300">Matches</span>
            </div>
          </div>
          <div className="flex items-center gap-stack-md">
            <span className="font-label-caps text-label-caps text-on-surface-variant">Sorted by: Highest Match</span>
            <button className="p-2 text-on-surface-variant hover:bg-surface-variant/50 dark:hover:bg-inverse-surface/20 rounded-full transition-all flex items-center justify-center">
              <span className="material-symbols-outlined" data-icon="filter_list">filter_list</span>
            </button>
            <button className="p-2 text-on-surface-variant hover:bg-surface-variant/50 dark:hover:bg-inverse-surface/20 rounded-full transition-all flex items-center justify-center">
              <span className="material-symbols-outlined" data-icon="download">download</span>
            </button>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-surface-container-low/20 dark:bg-slate-800/20">
              <tr>
                <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant">Candidate</th>
                <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant">Top Skills</th>
                <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant">Experience</th>
                <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/30 dark:divide-outline/30">
              {/* Candidate Row 1 */}
              <tr className="hover:bg-surface-container-low/40 dark:hover:bg-slate-700/40 transition-colors cursor-pointer">
                <td className="px-gutter py-4">
                  <div className="flex items-center gap-stack-md">
                    <div className="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary font-bold">SM</div>
                    <div>
                      <p className="font-body-md text-body-md font-bold dark:text-slate-100">Sarah Miller</p>
                      <p className="font-label-caps text-label-caps text-on-surface-variant">San Francisco, CA</p>
                    </div>
                  </div>
                </td>
                <td className="px-gutter py-4">
                  <div className="flex flex-wrap gap-1">
                    <span className="px-2 py-0.5 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim text-[11px] font-semibold rounded-md border border-outline-variant/20">React.js</span>
                    <span className="px-2 py-0.5 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim text-[11px] font-semibold rounded-md border border-outline-variant/20">Node.js</span>
                    <span className="px-2 py-0.5 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim text-[11px] font-semibold rounded-md border border-outline-variant/20">AWS</span>
                  </div>
                </td>
                <td className="px-gutter py-4 font-body-sm text-body-sm text-on-surface-variant">8 Years</td>
                <td className="px-gutter py-4 text-right">
                  <button className="p-2 text-primary dark:text-primary-fixed-dim hover:bg-primary/10 rounded-lg transition-all flex items-center justify-center ml-auto">
                    <span className="material-symbols-outlined" data-icon="visibility">visibility</span>
                  </button>
                </td>
              </tr>
              
              {/* Candidate Row 2 */}
              <tr className="hover:bg-surface-container-low/40 dark:hover:bg-slate-700/40 transition-colors cursor-pointer">
                <td className="px-gutter py-4">
                  <div className="flex items-center gap-stack-md">
                    <div className="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary font-bold">JK</div>
                    <div>
                      <p className="font-body-md text-body-md font-bold dark:text-slate-100">James Knight</p>
                      <p className="font-label-caps text-label-caps text-on-surface-variant">London, UK</p>
                    </div>
                  </div>
                </td>
                <td className="px-gutter py-4">
                  <div className="flex flex-wrap gap-1">
                    <span className="px-2 py-0.5 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim text-[11px] font-semibold rounded-md border border-outline-variant/20">Python</span>
                    <span className="px-2 py-0.5 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim text-[11px] font-semibold rounded-md border border-outline-variant/20">Django</span>
                    <span className="px-2 py-0.5 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim text-[11px] font-semibold rounded-md border border-outline-variant/20">PostgreSQL</span>
                  </div>
                </td>
                <td className="px-gutter py-4 font-body-sm text-body-sm text-on-surface-variant">5 Years</td>
                <td className="px-gutter py-4 text-right">
                  <button className="p-2 text-primary dark:text-primary-fixed-dim hover:bg-primary/10 rounded-lg transition-all flex items-center justify-center ml-auto">
                    <span className="material-symbols-outlined" data-icon="visibility">visibility</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div className="px-gutter py-4 bg-surface-container-low/30 dark:bg-slate-800/30 border-t border-outline-variant dark:border-slate-700 flex justify-between items-center">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Showing 2 of 42 candidates</p>
          <div className="flex items-center gap-stack-sm">
            <button className="px-3 py-1 bg-surface dark:bg-slate-800 border border-outline-variant dark:border-slate-700 rounded-md font-body-sm text-body-sm hover:bg-surface-variant/20 dark:hover:bg-slate-700-high transition-all disabled:opacity-50 dark:text-slate-100" disabled>Previous</button>
            <button className="px-3 py-1 bg-surface dark:bg-slate-800 border border-outline-variant dark:border-slate-700 rounded-md font-body-sm text-body-sm hover:bg-surface-variant/20 dark:hover:bg-slate-700-high transition-all dark:text-slate-100">Next</button>
          </div>
        </div>
      </section>

      {/* Asymmetric Bento Insights */}
      <section className="mt-stack-lg grid grid-cols-1 md:grid-cols-3 gap-gutter mb-20">
        <div className="md:col-span-2 bg-primary-container text-on-primary-container p-stack-lg rounded-xl relative overflow-hidden group">
          <div className="relative z-10">
            <h4 className="font-headline-md text-headline-md mb-2">Intelligence Summary</h4>
            <p className="font-body-md text-body-md opacity-90 max-w-lg mb-stack-md">AI identified a high correlation between "React" and "Scalability" in your JD. Sarah Miller stands out for her recent work in micro-frontends which matches your growth goals.</p>
            <button className="font-label-caps text-label-caps bg-on-primary-container text-primary-container px-stack-md py-2 rounded-lg hover:brightness-110 transition-all">Full AI Report</button>
          </div>
          <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-on-primary-container/10 rounded-full blur-3xl group-hover:scale-110 transition-transform"></div>
        </div>
        
        <div className="bg-surface-container-highest dark:bg-slate-800 p-stack-lg rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm flex flex-col items-center justify-center text-center transition-colors duration-200">
          <div className="w-16 h-16 bg-primary-fixed dark:bg-primary-container rounded-full flex items-center justify-center mb-stack-md">
            <span className="material-symbols-outlined text-primary dark:text-primary-fixed-dim text-3xl" data-icon="trending_up">trending_up</span>
          </div>
          <h4 className="font-title-sm text-title-sm text-primary dark:text-primary-fixed-dim">Market Pulse</h4>
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-2">Candidate demand for your listed skills is <span className="text-error font-bold dark:text-[#ffb4ab]">High</span>.</p>
          <p className="font-label-caps text-label-caps text-primary dark:text-primary-fixed-dim mt-4 cursor-pointer hover:underline">View Salary Benchmarks</p>
        </div>
      </section>

      {/* FAB */}
      <button className="fixed bottom-8 right-8 w-14 h-14 bg-primary text-on-primary rounded-full shadow-xl flex items-center justify-center hover:scale-105 active:scale-95 transition-all z-50">
        <span className="material-symbols-outlined" data-icon="add">add</span>
      </button>
    </div>
  );
}
