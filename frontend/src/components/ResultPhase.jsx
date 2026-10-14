import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import {
  Award,
  CheckCircle,
  XCircle,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Brain,
  FileCheck,
  ShieldAlert,
  Cpu,
  RotateCcw,
  BarChart3,
  Check,
  X,
  AlertTriangle,
} from 'lucide-react';

export default function ResultPhase({ evaluationResult, onNewChallenge }) {
  const [activeTab, setActiveTab] = useState('summary');
  const [showRawDetails, setShowRawDetails] = useState(false);

  const finalResult = evaluationResult?.final_result || {};
  const semantic = evaluationResult?.semantic_result || {};
  const coverage = evaluationResult?.concept_coverage_result || {};
  const faithfulness = evaluationResult?.faithfulness_result || {};
  const language = evaluationResult?.language_coherence_result || {};

  const finalScore = Number(finalResult.final_score || 0);
  const performanceLevel = finalResult.performance_level || 'Evaluated';

  // Confetti on good score
  useEffect(() => {
    if (finalScore >= 70) {
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
      } catch (e) {
        // Safe fallback if canvas is unavailable
      }
    }
  }, [finalScore]);

  // Color scheme based on score
  const getScoreColor = (score) => {
    if (score >= 85) return 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10';
    if (score >= 70) return 'text-indigo-400 border-indigo-500/40 bg-indigo-500/10';
    if (score >= 50) return 'text-amber-400 border-amber-500/40 bg-amber-500/10';
    return 'text-rose-400 border-rose-500/40 bg-rose-500/10';
  };

  const getBadgeStyle = (level) => {
    switch (level?.toLowerCase()) {
      case 'excellent':
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      case 'strong':
        return 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40';
      case 'moderate':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fadeIn">
      {/* Blank Recall Edge Case Alert */}
      {finalScore === 0 && (
        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-start space-x-3 text-amber-300 text-sm shadow-lg">
          <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-400 mt-0.5" />
          <div>
            <h4 className="font-bold text-amber-200">You did not type anything</h4>
            <p className="text-xs text-amber-300/80 mt-0.5">
              No recall response was captured during the writing phase. You can review the key concepts you missed below and start a new challenge to test your memory!
            </p>
          </div>
        </div>
      )}

      {/* Hero Score Card */}
      <div className="relative overflow-hidden bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-60 h-60 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pb-6 border-b border-slate-800">
          <div className="text-center sm:text-left space-y-2">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-300">
              <Award className="w-3.5 h-3.5 text-amber-400" />
              <span>Recall Assessment Complete</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Your Recall Result
            </h1>
            <p className="text-slate-400 text-sm">
              Comprehensive multi-agent NLP benchmark across semantic, conceptual, and grammatical dimensions.
            </p>
          </div>

          {/* Big Score Dial */}
          <div className="flex flex-col items-center">
            <div className="relative flex items-center justify-center">
              <svg className="w-32 h-32 transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="52"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="transparent"
                  className="text-slate-800"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="52"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="transparent"
                  strokeDasharray={326.7}
                  strokeDashoffset={326.7 - (326.7 * finalScore) / 100}
                  strokeLinecap="round"
                  className={`transition-all duration-1000 ${
                    finalScore >= 80 ? 'text-emerald-400' : finalScore >= 60 ? 'text-indigo-400' : 'text-amber-400'
                  }`}
                />
              </svg>
              <div className="absolute flex flex-col items-center justify-center">
                <span className="text-3xl font-extrabold text-white font-mono">
                  {finalScore.toFixed(1)}
                </span>
                <span className="text-[10px] uppercase font-semibold text-slate-400">out of 100</span>
              </div>
            </div>

            <div className={`mt-2 px-3.5 py-1 rounded-full text-xs font-bold border uppercase tracking-wider ${getBadgeStyle(performanceLevel)}`}>
              {performanceLevel}
            </div>
          </div>
        </div>

        {/* 4 Core Dimensions Overview Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-6">
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <Brain className="w-3.5 h-3.5 text-blue-400" />
              <span>Semantic</span>
            </div>
            <div className="mt-1 flex items-baseline justify-between">
              <span className="text-lg font-bold text-white font-mono">
                {Number(semantic.score || 0).toFixed(1)}%
              </span>
              <span className="text-[11px] text-slate-500">Weight: 25%</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <FileCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Coverage</span>
            </div>
            <div className="mt-1 flex items-baseline justify-between">
              <span className="text-lg font-bold text-white font-mono">
                {Number(coverage.score || 0).toFixed(1)}%
              </span>
              <span className="text-[11px] text-slate-500">Weight: 35%</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              <span>Faithfulness</span>
            </div>
            <div className="mt-1 flex items-baseline justify-between">
              <span className="text-lg font-bold text-white font-mono">
                {Number(faithfulness.score || 0).toFixed(1)}%
              </span>
              <span className="text-[11px] text-slate-500">Weight: 25%</span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <Cpu className="w-3.5 h-3.5 text-purple-400" />
              <span>Coherence</span>
            </div>
            <div className="mt-1 flex items-baseline justify-between">
              <span className="text-lg font-bold text-white font-mono">
                {Number(language.overall_score || 0).toFixed(1)}%
              </span>
              <span className="text-[11px] text-slate-500">Weight: 15%</span>
            </div>
          </div>
        </div>
      </div>

      {/* AI Qualitative Feedback Banner */}
      {finalResult.feedback && (
        <div className="p-6 rounded-3xl bg-indigo-950/30 border border-indigo-500/20 backdrop-blur-md space-y-2">
          <div className="flex items-center space-x-2 text-indigo-300 font-semibold text-sm">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span>AI Feedback Summary</span>
          </div>
          <p className="text-slate-200 text-sm leading-relaxed">{finalResult.feedback}</p>
        </div>
      )}

      {/* Strengths & Missed Areas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths Card */}
        <div className="p-6 rounded-3xl bg-slate-900/70 border border-slate-800 space-y-4">
          <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
            <CheckCircle className="w-5 h-5 text-emerald-400" />
            <h3 className="text-base font-bold text-slate-100">What You Remembered Well</h3>
          </div>
          <ul className="space-y-2.5">
            {finalResult.strengths?.length ? (
              finalResult.strengths.map((pt, idx) => (
                <li key={idx} className="flex items-start space-x-2.5 text-xs sm:text-sm text-slate-300">
                  <span className="mt-0.5 w-1.5 h-1.5 rounded-full bg-emerald-400 flex-shrink-0" />
                  <span>{pt}</span>
                </li>
              ))
            ) : (
              <li className="text-xs text-slate-500 italic">No specific strengths captured.</li>
            )}
          </ul>
        </div>

        {/* Missed Areas Card */}
        <div className="p-6 rounded-3xl bg-slate-900/70 border border-slate-800 space-y-4">
          <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
            <XCircle className="w-5 h-5 text-rose-400" />
            <h3 className="text-base font-bold text-slate-100">Areas For Improvement</h3>
          </div>
          <ul className="space-y-2.5">
            {finalResult.missed_areas?.length ? (
              finalResult.missed_areas.map((pt, idx) => (
                <li key={idx} className="flex items-start space-x-2.5 text-xs sm:text-sm text-slate-300">
                  <span className="mt-0.5 w-1.5 h-1.5 rounded-full bg-rose-400 flex-shrink-0" />
                  <span>{pt}</span>
                </li>
              ))
            ) : (
              <li className="text-xs text-slate-500 italic">None noted; strong concept coverage!</li>
            )}
          </ul>
        </div>
      </div>

      {/* Deep-Dive Multi-Agent Breakdown Accordion / Tabs */}
      <div className="bg-slate-900/70 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-white">Evaluation Details & Agent Inspector</h3>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setActiveTab('semantic')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                activeTab === 'semantic' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              Semantic
            </button>
            <button
              onClick={() => setActiveTab('coverage')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                activeTab === 'coverage' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              Coverage
            </button>
            <button
              onClick={() => setActiveTab('faithfulness')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                activeTab === 'faithfulness' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              Faithfulness
            </button>
            <button
              onClick={() => setActiveTab('coherence')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                activeTab === 'coherence' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              Language
            </button>
          </div>
        </div>

        {/* Tab 1: Semantic */}
        {activeTab === 'semantic' && (
          <div className="space-y-4 animate-fadeIn">
            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div>
                <span className="text-xs text-slate-400">Model: all-MiniLM-L6-v2</span>
                <h4 className="text-base font-bold text-white">Overall Semantic Similarity</h4>
                <p className="text-xs text-slate-300 mt-1">{semantic.interpretation || 'Evaluated'}</p>
              </div>
              <div className="text-right">
                <span className="text-2xl font-bold font-mono text-blue-400">
                  {Number(semantic.score || 0).toFixed(1)} / 100
                </span>
                <span className="block text-xs text-slate-500 font-mono">
                  cosine sim: {semantic.semantic_similarity}
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Measures how closely the deep semantic vector of your recalled text aligns with the vector of the original passage in latent embedding space.
            </p>
          </div>
        )}

        {/* Tab 2: Coverage */}
        {activeTab === 'coverage' && (
          <div className="space-y-4 animate-fadeIn">
            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div>
                <span className="text-xs text-slate-400">Concept Match Engine</span>
                <h4 className="text-base font-bold text-white">Essential Concept Coverage</h4>
              </div>
              <div className="text-right">
                <span className="text-2xl font-bold font-mono text-emerald-400">
                  {Number(coverage.score || 0).toFixed(1)} / 100
                </span>
                <span className="block text-xs text-slate-500">
                  {coverage.covered_concepts?.length || 0} / {(coverage.covered_concepts?.length || 0) + (coverage.missed_concepts?.length || 0)} recalled
                </span>
              </div>
            </div>

            {/* Covered Concepts */}
            {coverage.covered_concepts?.length > 0 && (
              <div>
                <span className="text-xs font-semibold uppercase text-emerald-400 tracking-wider block mb-2">
                  ✓ Successfully Captured Concepts
                </span>
                <div className="flex flex-wrap gap-2">
                  {coverage.covered_concepts.map((concept, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 text-xs font-medium flex items-center space-x-1"
                    >
                      <Check className="w-3 h-3 text-emerald-400" />
                      <span>{concept}</span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Missed Concepts */}
            {coverage.missed_concepts?.length > 0 && (
              <div className="pt-2">
                <span className="text-xs font-semibold uppercase text-rose-400 tracking-wider block mb-2">
                  ✕ Missed Core Concepts
                </span>
                <div className="flex flex-wrap gap-2">
                  {coverage.missed_concepts.map((concept, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 rounded-full bg-rose-500/10 text-rose-300 border border-rose-500/20 text-xs font-medium flex items-center space-x-1"
                    >
                      <X className="w-3 h-3 text-rose-400" />
                      <span>{concept}</span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Concept Scores Table */}
            {coverage.concept_scores?.length > 0 && (
              <div className="pt-3">
                <span className="text-xs font-semibold text-slate-400 block mb-2">Individual Similarity Matches</span>
                <div className="border border-slate-800 rounded-xl overflow-hidden text-xs">
                  <table className="w-full text-left">
                    <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                      <tr>
                        <th className="py-2 px-3 font-semibold">Concept</th>
                        <th className="py-2 px-3 font-semibold text-right">Similarity</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      {coverage.concept_scores.map((cs, idx) => (
                        <tr key={idx} className="hover:bg-slate-800/20">
                          <td className="py-2 px-3 text-slate-200">{cs.concept}</td>
                          <td className="py-2 px-3 text-right font-mono text-slate-300">
                            {cs.similarity}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Faithfulness */}
        {activeTab === 'faithfulness' && (
          <div className="space-y-4 animate-fadeIn">
            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div>
                <span className="text-xs text-slate-400">CrossEncoder NLI Model: nli-MiniLM2-L6-H768</span>
                <h4 className="text-base font-bold text-white">Factuality & Entailment Score</h4>
              </div>
              <div className="text-right">
                <span className="text-2xl font-bold font-mono text-amber-400">
                  {Number(faithfulness.score || 0).toFixed(1)} / 100
                </span>
                <span className="block text-xs text-slate-500">
                  {faithfulness.contradictions?.length || 0} contradictions
                </span>
              </div>
            </div>

            {/* Contradictions */}
            {faithfulness.contradictions?.length > 0 ? (
              <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 space-y-2">
                <span className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center space-x-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Contradictory Claims Detected</span>
                </span>
                {faithfulness.contradictions.map((c, idx) => (
                  <div key={idx} className="text-xs text-slate-300 space-y-1 bg-slate-950/40 p-2.5 rounded-lg">
                    <p className="text-rose-200">"{c.statement}"</p>
                    <p className="text-slate-400 text-[11px]">Contradicts: "{c.source_sentence}"</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 flex items-center space-x-2">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Zero factual contradictions detected. Your recalled statements remain faithful to the passage.</span>
              </div>
            )}

            {/* Entailments */}
            {faithfulness.entailments?.length > 0 && (
              <div className="pt-2">
                <span className="text-xs font-semibold text-slate-400 block mb-2">Supported Sentences (Entailments)</span>
                <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                  {faithfulness.entailments.map((e, idx) => (
                    <div key={idx} className="p-2.5 rounded-xl bg-slate-950/40 border border-slate-800 text-xs text-slate-300 flex items-center justify-between">
                      <span className="truncate pr-2">"{e.statement}"</span>
                      <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full flex-shrink-0">
                        {Math.round((e.confidence || 0) * 100)}% conf
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 4: Language & Coherence */}
        {activeTab === 'coherence' && (
          <div className="space-y-4 animate-fadeIn">
            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div>
                <span className="text-xs text-slate-400">Linguistic Quality Engine</span>
                <h4 className="text-base font-bold text-white">Overall Language & Coherence</h4>
              </div>
              <div className="text-right">
                <span className="text-2xl font-bold font-mono text-purple-400">
                  {Number(language.overall_score || 0).toFixed(1)} / 100
                </span>
              </div>
            </div>

            {/* 4 Rubric Dimensions */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 text-center">
                <span className="text-xs text-slate-400 block">Grammar</span>
                <span className="text-base font-bold text-white font-mono mt-1 block">
                  {language.grammar_score || 0}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 text-center">
                <span className="text-xs text-slate-400 block">Clarity</span>
                <span className="text-base font-bold text-white font-mono mt-1 block">
                  {language.clarity_score || 0}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 text-center">
                <span className="text-xs text-slate-400 block">Coherence</span>
                <span className="text-base font-bold text-white font-mono mt-1 block">
                  {language.coherence_score || 0}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 text-center">
                <span className="text-xs text-slate-400 block">Organization</span>
                <span className="text-base font-bold text-white font-mono mt-1 block">
                  {language.organization_score || 0}
                </span>
              </div>
            </div>

            {language.feedback && (
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300">
                <span className="text-slate-400 font-semibold block mb-1">Writing Quality Feedback:</span>
                <p>{language.feedback}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Start New Challenge Action */}
      <div className="flex justify-center pt-2">
        <button
          onClick={onNewChallenge}
          className="py-4 px-8 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-base shadow-xl shadow-indigo-600/30 flex items-center space-x-2 transition-all transform active:scale-95 cursor-pointer"
        >
          <RotateCcw className="w-5 h-5" />
          <span>Start a New Challenge</span>
        </button>
      </div>
    </div>
  );
}
