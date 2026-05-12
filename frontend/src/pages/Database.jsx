import React, { useState } from 'react';

export default function Database() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [evaluationReport, setEvaluationReport] = useState('');
  const [matchLimit, setMatchLimit] = useState(5);
  const [searched, setSearched] = useState(false);

  const handleFileUpload = (e) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files);
      setUploadedFiles(prev => [...prev, ...newFiles]);
    }
  };

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleMatch = async () => {
    if (uploadedFiles.length === 0 || !jobDescription.trim()) {
      alert("Please upload at least one resume and provide a job description.");
      return;
    }

    setLoading(true);
    setSearched(false);
    setResults([]);
    setEvaluationReport('');
    
    try {
      const formData = new FormData();
      formData.append('input', jobDescription);
      uploadedFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch('/api/v2/match_cvs', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Matching failed');
      }

      const data = await response.json();
      setResults(data.results || []);
      setEvaluationReport(data.evaluation_report || '');
      setSearched(true);
    } catch (error) {
      console.error(error);
      alert('Failed to process and match CVs.');
    } finally {
      setLoading(false);
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
              <p className="font-body-sm text-body-sm text-on-surface-variant">Upload PDF/DOCX resumes to evaluate against job criteria.</p>
            </div>
            
            <div className="flex-1 border-2 border-dashed border-outline-variant dark:border-slate-700 rounded-lg flex flex-col items-center justify-center p-stack-lg hover:border-primary dark:hover:border-primary-fixed-dim hover:bg-primary/5 transition-all group relative min-h-[200px]">
              <input type="file" multiple accept=".pdf,.docx,.txt" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" onChange={handleFileUpload} />
              <div className="w-12 h-12 bg-primary-fixed dark:bg-primary-container rounded-full flex items-center justify-center mb-stack-md group-hover:scale-110 transition-transform">
                <span className="material-symbols-outlined text-primary dark:text-primary-fixed-dim" data-icon="upload">upload</span>
              </div>
              <p className="font-body-md text-body-md font-semibold text-primary dark:text-primary-fixed-dim">
                Drop resumes here or click
              </p>
              <p className="font-label-caps text-label-caps text-on-surface-variant mt-1">PDF, DOCX up to 10MB</p>
            </div>

            {uploadedFiles.length > 0 && (
              <div className="mt-4 max-h-32 overflow-y-auto pr-2">
                <p className="font-label-caps text-label-caps text-on-surface-variant mb-2">{uploadedFiles.length} File(s) Ready</p>
                <div className="flex flex-col gap-2">
                  {uploadedFiles.map((f, i) => (
                    <div key={i} className="flex items-center justify-between bg-surface dark:bg-slate-700 px-3 py-2 rounded border border-outline-variant dark:border-slate-600">
                      <span className="font-body-sm text-body-sm truncate max-w-[200px] text-on-surface dark:text-slate-200">{f.name}</span>
                      <button onClick={() => removeFile(i)} className="text-error hover:text-error-hover transition-colors flex items-center justify-center">
                        <span className="material-symbols-outlined text-[16px]" data-icon="close">close</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          {/* Job Description (Right) */}
          <div className="flex-[1.5] bg-surface-container-lowest dark:bg-slate-800 p-stack-lg rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm transition-colors duration-200 flex flex-col">
            <div className="flex justify-between items-center mb-stack-md">
              <div>
                <h2 className="font-headline-md text-headline-md text-primary dark:text-primary-fixed-dim mb-1">Job Description</h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Define core competencies and requirements.</p>
              </div>
            </div>
            <div className="relative flex-1 flex flex-col">
              <textarea 
                className="flex-1 w-full min-h-[200px] bg-surface dark:bg-slate-800 border border-outline-variant dark:border-slate-700 rounded-lg p-stack-md font-body-md text-body-md focus:ring-2 focus:ring-primary dark:text-slate-100 transition-all resize-none" 
                placeholder="Paste the job description or specific key requirements here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              ></textarea>
              <div className="absolute bottom-3 right-3 flex items-center gap-stack-sm pointer-events-none">
                <span className="font-label-caps text-label-caps text-on-surface-variant">{jobDescription.length} / 5000 characters</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Action Bar */}
        <div className="mt-stack-lg flex justify-center">
          <button 
            onClick={handleMatch}
            disabled={loading}
            className="bg-primary text-on-primary px-stack-lg py-4 rounded-lg flex items-center gap-stack-md hover:shadow-lg transition-all active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span className="material-symbols-outlined" data-icon={loading ? "hourglass_empty" : "auto_awesome"}>
              {loading ? "hourglass_empty" : "auto_awesome"}
            </span>
            <span className="font-title-sm text-title-sm">{loading ? "Processing..." : "Match Resumes"}</span>
          </button>
        </div>
      </section>

      {/* Results Section */}
      {searched && (
        <>
          <section className="bg-surface-container-lowest dark:bg-slate-800 rounded-xl border border-outline-variant dark:border-slate-700 shadow-sm overflow-hidden transition-colors duration-200 mb-8">
            <div className="px-gutter py-stack-md border-b border-outline-variant dark:border-slate-700 flex justify-between items-center bg-surface-container-low/30 dark:bg-slate-800/30">
              <div className="flex items-center gap-4">
                <h3 className="font-title-sm text-title-sm text-primary dark:text-primary-fixed-dim">Matching Results</h3>
              </div>
              <div className="flex items-center gap-stack-md">
                <span className="font-label-caps text-label-caps text-on-surface-variant">Sorted by: Highest Match</span>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-surface-container-low/20 dark:bg-slate-800/20">
                  <tr>
                    <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant w-16">Rank</th>
                    <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant">Candidate File</th>
                    <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant">Match Distance</th>
                    <th className="px-gutter py-4 font-label-caps text-label-caps text-on-surface-variant">Context Snippet</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-outline-variant/30 dark:divide-outline/30">
                  {results.length > 0 ? (
                    results.map((candidate, idx) => (
                      <tr key={idx} className="hover:bg-surface-container-low/40 dark:hover:bg-slate-700/40 transition-colors">
                        <td className="px-gutter py-4 font-body-md text-body-md font-bold dark:text-slate-100 text-center">#{candidate.rank}</td>
                        <td className="px-gutter py-4">
                          <div className="flex items-center gap-stack-md">
                            <div className="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary font-bold uppercase">
                              {candidate.filename.charAt(0)}
                            </div>
                            <div>
                              <p className="font-body-md text-body-md font-bold dark:text-slate-100 max-w-[200px] truncate" title={candidate.filename}>{candidate.filename}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-gutter py-4 font-body-sm text-body-sm text-on-surface-variant">
                          <span className="px-2 py-1 bg-secondary-container/30 dark:bg-secondary-container/10 text-secondary dark:text-secondary-fixed-dim rounded font-semibold text-[12px]">
                            {candidate.distance.toFixed(4)}
                          </span>
                        </td>
                        <td className="px-gutter py-4">
                          <p className="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 line-clamp-2 max-w-md" title={candidate.snippet}>
                            {candidate.snippet}
                          </p>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="4" className="px-gutter py-8 text-center text-on-surface-variant">
                        No candidates matched perfectly.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            
            <div className="px-gutter py-4 bg-surface-container-low/30 dark:bg-slate-800/30 border-t border-outline-variant dark:border-slate-700 flex justify-between items-center">
              <p className="font-body-sm text-body-sm text-on-surface-variant">Showing {results.length} candidates</p>
            </div>
          </section>

          {/* AI Intelligence Summary */}
          {evaluationReport && (
            <section className="mb-20">
              <div className="bg-primary-container text-on-primary-container p-stack-lg rounded-xl relative overflow-hidden group border border-primary/20 dark:border-slate-700 dark:bg-slate-800">
                <div className="relative z-10">
                  <h4 className="font-headline-md text-headline-md mb-4 flex items-center gap-2 dark:text-primary-fixed-dim">
                    <span className="material-symbols-outlined">auto_awesome</span>
                    Intelligence Summary
                  </h4>
                  <div className="font-body-md text-body-md opacity-90 max-w-4xl whitespace-pre-wrap leading-relaxed dark:text-slate-300">
                    {evaluationReport}
                  </div>
                </div>
                <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-on-primary-container/10 rounded-full blur-3xl group-hover:scale-110 transition-transform"></div>
              </div>
            </section>
          )}
        </>
      )}

      {/* FAB */}
      <button className="fixed bottom-8 right-8 w-14 h-14 bg-primary text-on-primary rounded-full shadow-xl flex items-center justify-center hover:scale-105 active:scale-95 transition-all z-50">
        <span className="material-symbols-outlined" data-icon="chat">chat</span>
      </button>
    </div>
  );
}
