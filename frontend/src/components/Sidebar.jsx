import React from 'react';
import { CheckCircle2, Circle, Clock, BookOpen, PenTool, Award, Sliders, Layers } from 'lucide-react';

const PHASES = [
  { id: 'setup', label: 'Setup', icon: Sliders, desc: 'Configure challenge' },
  { id: 'reading', label: 'Reading', icon: BookOpen, desc: 'Absorb the passage' },
  { id: 'recall', label: 'Recall', icon: PenTool, desc: 'Write what you remember' },
  { id: 'evaluation', label: 'Evaluation', icon: Layers, desc: 'Multi-agent LangGraph analysis' },
  { id: 'result', label: 'Result', icon: Award, desc: 'Score & feedback' },
];

export default function Sidebar({ stage, challengeConfig, onNewChallenge }) {
  const currentStageIndex = PHASES.findIndex((p) => p.id === stage);

  return (
    <aside className="w-full lg:w-72 flex-shrink-0 space-y-6">
      {/* Progress Card */}
      <div className="bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-800 p-5 shadow-sm">
        <div className="flex items-center space-x-2 pb-3 mb-4 border-b border-slate-800">
          <Clock className="w-4 h-4 text-indigo-400" />
          <h2 className="text-sm font-semibold tracking-wide uppercase text-slate-300">
            Challenge Progress
          </h2>
        </div>

        <nav className="space-y-3">
          {PHASES.map((p, idx) => {
            const isCompleted = idx < currentStageIndex;
            const isCurrent = idx === currentStageIndex;
            const Icon = p.icon;

            return (
              <div
                key={p.id}
                className={`flex items-start space-x-3 p-2.5 rounded-xl transition-all ${
                  isCurrent
                    ? 'bg-indigo-600/10 border border-indigo-500/30 shadow-sm'
                    : isCompleted
                    ? 'text-slate-400'
                    : 'text-slate-500 opacity-60'
                }`}
              >
                <div className="mt-0.5 flex-shrink-0">
                  {isCompleted ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <div className="w-4 h-4 rounded-full border-2 border-indigo-400 flex items-center justify-center">
                      <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
                    </div>
                  ) : (
                    <Circle className="w-4 h-4 text-slate-600" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-sm font-medium ${
                        isCurrent
                          ? 'text-indigo-300 font-semibold'
                          : isCompleted
                          ? 'text-slate-200'
                          : 'text-slate-500'
                      }`}
                    >
                      {p.label}
                    </span>
                    {isCurrent && (
                      <span className="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
                        Active
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 truncate">{p.desc}</p>
                </div>
              </div>
            );
          })}
        </nav>
      </div>

      {/* Challenge Configuration Details */}
      {challengeConfig?.topic && stage !== 'setup' && (
        <div className="bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-800 p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Active Parameters
            </h3>
            <span
              className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${
                challengeConfig.difficulty === 'Easy'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : challengeConfig.difficulty === 'Medium'
                  ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
              }`}
            >
              {challengeConfig.difficulty}
            </span>
          </div>

          <div className="space-y-2.5 text-xs">
            <div>
              <span className="text-slate-400">Topic</span>
              <p className="font-semibold text-slate-200 truncate">{challengeConfig.topic}</p>
            </div>
            <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-800/60">
              <div>
                <span className="text-slate-400">Word Target</span>
                <p className="font-medium text-slate-200">{challengeConfig.word_limit} words</p>
              </div>
              <div>
                <span className="text-slate-400">Key Concepts</span>
                <p className="font-medium text-slate-200">
                  {challengeConfig.key_concepts?.length || 'N/A'} defined
                </p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-800/60">
              <div>
                <span className="text-slate-400">Reading Time</span>
                <p className="font-medium text-slate-200">{challengeConfig.reading_time} min</p>
              </div>
              <div>
                <span className="text-slate-400">Writing Time</span>
                <p className="font-medium text-slate-200">{challengeConfig.writing_time} min</p>
              </div>
            </div>
          </div>

          {stage === 'result' && (
            <button
              onClick={onNewChallenge}
              className="w-full mt-3 py-2 px-3 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 transition-colors"
            >
              Start New Challenge
            </button>
          )}
        </div>
      )}
    </aside>
  );
}
