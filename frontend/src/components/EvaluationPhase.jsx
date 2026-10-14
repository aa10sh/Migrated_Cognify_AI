import React, { useEffect, useState } from 'react';
import { Layers, Brain, CheckCircle2, Cpu, FileCheck, ShieldCheck, Sparkles } from 'lucide-react';

const AGENTS = [
  {
    id: 'semantic',
    name: 'Semantic Understanding Agent',
    desc: 'Generates SentenceTransformer embeddings and computes high-dimensional cosine similarity.',
    icon: Brain,
    color: 'from-blue-500 to-cyan-500',
    delay: 400,
  },
  {
    id: 'coverage',
    name: 'Concept Coverage Agent',
    desc: 'Evaluates recall coverage across essential key concepts from the source text.',
    icon: FileCheck,
    color: 'from-emerald-500 to-teal-500',
    delay: 800,
  },
  {
    id: 'faithfulness',
    name: 'Faithfulness & NLI Agent',
    desc: 'Runs Cross-Encoder Natural Language Inference to identify supported claims & contradictions.',
    icon: ShieldCheck,
    color: 'from-amber-500 to-orange-500',
    delay: 1200,
  },
  {
    id: 'coherence',
    name: 'Language & Coherence Agent',
    desc: 'Analyzes grammatical integrity, structural coherence, and clarity of expression.',
    icon: Cpu,
    color: 'from-purple-500 to-pink-500',
    delay: 1600,
  },
];

export default function EvaluationPhase() {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev < 4 ? prev + 1 : prev));
    }, 900);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold">
          <Layers className="w-3.5 h-3.5 animate-spin" />
          <span>LangGraph Parallel Execution</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white tracking-tight">
          Evaluating Your Recall
        </h2>
        <p className="text-slate-400 text-sm max-w-lg mx-auto">
          LangGraph has orchestrated 4 parallel NLP evaluation agents and is synthesizing your final multi-dimensional score.
        </p>
      </div>

      {/* LangGraph Architecture Visualizer */}
      <div className="bg-slate-900/70 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-ping" />
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">
              Parallel Graph Topology (StateGraph)
            </span>
          </div>
          <span className="text-xs text-indigo-400 font-mono">START → 4 Agents in Parallel → Synthesis</span>
        </div>

        {/* 4 Parallel Nodes Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {AGENTS.map((agent, idx) => {
            const Icon = agent.icon;
            const isCompleted = activeStep > idx;
            const isProcessing = activeStep === idx;

            return (
              <div
                key={agent.id}
                className={`p-4 rounded-2xl border transition-all duration-300 ${
                  isProcessing
                    ? 'bg-indigo-950/40 border-indigo-500/60 shadow-lg shadow-indigo-500/10 scale-[1.02]'
                    : isCompleted
                    ? 'bg-slate-900/90 border-slate-700/80'
                    : 'bg-slate-950/40 border-slate-800/60 opacity-60'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2.5 rounded-xl bg-gradient-to-tr ${agent.color} text-white shadow-sm`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-100">{agent.name}</h4>
                      <span className="text-[11px] font-mono text-slate-400">
                        {isCompleted ? (
                          <span className="text-emerald-400 flex items-center space-x-1">
                            <CheckCircle2 className="w-3 h-3 inline" />
                            <span>Analysis complete</span>
                          </span>
                        ) : isProcessing ? (
                          <span className="text-indigo-400 animate-pulse">Running agent node...</span>
                        ) : (
                          'Queued in graph'
                        )}
                      </span>
                    </div>
                  </div>
                </div>
                <p className="text-xs text-slate-400 mt-3 leading-relaxed">{agent.desc}</p>
              </div>
            );
          })}
        </div>

        {/* Fan-in Final Evaluator Node */}
        <div className="mt-6 pt-4 border-t border-slate-800">
          <div className="p-4 rounded-2xl bg-gradient-to-r from-slate-900 to-indigo-950/40 border border-indigo-500/30 flex items-center space-x-4">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md">
              <Sparkles className="w-5 h-5 animate-pulse" />
            </div>
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-white">Final Evaluator Synthesis Node</h4>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300">
                  Weighted Engine
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Calculates weighted rubric: Semantic (25%) + Coverage (35%) + Faithfulness (25%) + Coherence (15%)
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
