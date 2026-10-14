import React, { useState } from 'react';
import { Sparkles, ArrowRight, BookOpen, Clock, PenTool, HelpCircle, AlertCircle } from 'lucide-react';

const SUGGESTED_TOPICS = [
  'Neuroplasticity & Brain Learning',
  'Quantum Computing Fundamentals',
  'Autonomous Artificial Intelligence Agents',
  'The James Webb Space Telescope Discoveries',
  'Behavioral Economics & Decision Biases',
];

export default function SetupPhase({ config, onStartChallenge, isLoading, error }) {
  const [topic, setTopic] = useState('');
  const [wordLimit, setWordLimit] = useState(150);
  const [difficulty, setDifficulty] = useState('Medium');
  const [readingTime, setReadingTime] = useState(1);
  const [writingTime, setWritingTime] = useState(2);
  const [validationError, setValidationError] = useState('');

  const wordLimits = config?.word_limits || [50, 100, 150, 250, 350, 500];
  const difficulties = config?.difficulties || ['Easy', 'Medium', 'Hard'];
  const readingTimes = config?.reading_times || [0.5, 1, 2, 3, 5];
  const writingTimes = config?.writing_times || [1, 2, 3, 5];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic.trim()) {
      setValidationError('Please enter a topic to generate your reading passage.');
      return;
    }
    setValidationError('');
    onStartChallenge({
      topic: topic.trim(),
      word_limit: Number(wordLimit),
      difficulty,
      reading_time: Number(readingTime),
      writing_time: Number(writingTime),
    });
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-fadeIn">
      {/* Hero Welcome */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Agentic Cognitive Recall Benchmark</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
          Challenge Your Working Memory & Comprehension
        </h1>
        <p className="text-slate-400 text-base max-w-xl mx-auto leading-relaxed">
          Test your cognitive retention. Read an AI-crafted technical passage, write your recall under time constraints, and receive a multi-dimensional LangGraph evaluation.
        </p>
      </div>

      {/* Main Form Card */}
      <div className="bg-slate-900/70 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Topic Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label htmlFor="topic" className="block text-sm font-semibold text-slate-200">
                1. Select or Enter a Topic
              </label>
              <span className="text-xs text-slate-400">Any subject or scientific field</span>
            </div>
            <input
              id="topic"
              type="text"
              value={topic}
              onChange={(e) => {
                setTopic(e.target.value);
                if (validationError) setValidationError('');
              }}
              placeholder="e.g. Artificial Intelligence, Photosynthesis, Black Holes..."
              className="w-full px-4 py-3 bg-slate-950/70 border border-slate-700/80 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm"
            />

            {/* Quick Topic Pills */}
            <div className="pt-2">
              <span className="text-xs text-slate-400 block mb-2 font-medium">Quick suggestions:</span>
              <div className="flex flex-wrap gap-2">
                {SUGGESTED_TOPICS.map((suggested) => (
                  <button
                    key={suggested}
                    type="button"
                    onClick={() => {
                      setTopic(suggested);
                      if (validationError) setValidationError('');
                    }}
                    className="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition-colors"
                  >
                    {suggested}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2 border-t border-slate-800">
            {/* Word Limit */}
            <div className="space-y-2">
              <label htmlFor="wordLimit" className="block text-sm font-semibold text-slate-200">
                2. Target Word Count
              </label>
              <select
                id="wordLimit"
                value={wordLimit}
                onChange={(e) => setWordLimit(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 bg-slate-950/70 border border-slate-700/80 rounded-xl text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              >
                {wordLimits.map((limit) => (
                  <option key={limit} value={limit}>
                    {limit} words
                  </option>
                ))}
              </select>
              <p className="text-xs text-slate-400">Length of the generated passage</p>
            </div>

            {/* Difficulty */}
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-slate-200">
                3. Difficulty Level
              </label>
              <div className="grid grid-cols-3 gap-2">
                {difficulties.map((diff) => {
                  const isSelected = difficulty === diff;
                  return (
                    <button
                      key={diff}
                      type="button"
                      onClick={() => setDifficulty(diff)}
                      className={`py-2 px-3 text-xs font-semibold rounded-xl border transition-all text-center ${
                        isSelected
                          ? diff === 'Easy'
                            ? 'bg-emerald-600/20 text-emerald-300 border-emerald-500/50 shadow-sm'
                            : diff === 'Medium'
                            ? 'bg-amber-600/20 text-amber-300 border-amber-500/50 shadow-sm'
                            : 'bg-rose-600/20 text-rose-300 border-rose-500/50 shadow-sm'
                          : 'bg-slate-950/50 text-slate-400 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      {diff}
                    </button>
                  );
                })}
              </div>
              <p className="text-xs text-slate-400">Controls conceptual depth & vocabulary</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2 border-t border-slate-800">
            {/* Reading Time */}
            <div className="space-y-2">
              <div className="flex items-center space-x-1.5">
                <BookOpen className="w-4 h-4 text-indigo-400" />
                <label htmlFor="readingTime" className="block text-sm font-semibold text-slate-200">
                  4. Reading Time
                </label>
              </div>
              <select
                id="readingTime"
                value={readingTime}
                onChange={(e) => setReadingTime(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 bg-slate-950/70 border border-slate-700/80 rounded-xl text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              >
                {readingTimes.map((time) => (
                  <option key={time} value={time}>
                    {time === 0.5 ? '30 seconds (0.5 min)' : `${time} minute${time > 1 ? 's' : ''}`}
                  </option>
                ))}
              </select>
              <p className="text-xs text-slate-400">Time allowed to read the passage</p>
            </div>

            {/* Writing Time */}
            <div className="space-y-2">
              <div className="flex items-center space-x-1.5">
                <PenTool className="w-4 h-4 text-purple-400" />
                <label htmlFor="writingTime" className="block text-sm font-semibold text-slate-200">
                  5. Recall Time
                </label>
              </div>
              <select
                id="writingTime"
                value={writingTime}
                onChange={(e) => setWritingTime(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 bg-slate-950/70 border border-slate-700/80 rounded-xl text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              >
                {writingTimes.map((time) => (
                  <option key={time} value={time}>
                    {time} minute{time > 1 ? 's' : ''}
                  </option>
                ))}
              </select>
              <p className="text-xs text-slate-400">Time to type your recall from memory</p>
            </div>
          </div>

          {/* Validation or Error Message */}
          {(validationError || error) && (
            <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{validationError || error}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 hover:from-indigo-500 hover:via-purple-500 hover:to-indigo-500 text-white font-bold text-base shadow-lg shadow-indigo-600/30 flex items-center justify-center space-x-2 transition-all transform active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Generating & Validating Challenge with AI...</span>
              </>
            ) : (
              <>
                <span>Start Challenge</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
