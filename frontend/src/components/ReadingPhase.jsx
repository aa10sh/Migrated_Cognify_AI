import React, { useState, useEffect } from 'react';
import { Clock, BookOpen, ArrowRight, AlertTriangle, Sparkles } from 'lucide-react';

export default function ReadingPhase({ challenge, readingTimeMinutes, onFinishReading }) {
  const totalSeconds = Math.round(readingTimeMinutes * 60);
  const [secondsRemaining, setSecondsRemaining] = useState(totalSeconds);

  useEffect(() => {
    if (secondsRemaining <= 0) {
      onFinishReading();
      return;
    }

    const timer = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          onFinishReading();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [secondsRemaining, onFinishReading]);

  const minutes = Math.floor(secondsRemaining / 60);
  const seconds = secondsRemaining % 60;
  const progressPercent = Math.max(0, Math.min(100, (secondsRemaining / totalSeconds) * 100));

  const isLowTime = secondsRemaining <= 15;

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fadeIn">
      {/* Sticky Countdown Header */}
      <div className={`p-4 rounded-2xl border backdrop-blur-md transition-all shadow-lg ${
        isLowTime
          ? 'bg-rose-950/40 border-rose-500/40 animate-pulse'
          : 'bg-slate-900/80 border-slate-800'
      }`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`p-2.5 rounded-xl ${
              isLowTime ? 'bg-rose-500/20 text-rose-400' : 'bg-indigo-500/20 text-indigo-400'
            }`}>
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">
                Reading Time Remaining
              </span>
              <div className="text-2xl font-mono font-bold text-white">
                {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
              </div>
            </div>
          </div>

          <button
            onClick={onFinishReading}
            className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs sm:text-sm font-semibold flex items-center space-x-1.5 shadow-md shadow-indigo-600/20 transition-all cursor-pointer"
          >
            <span>Done Reading</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Horizontal Progress Bar */}
        <div className="w-full bg-slate-800 h-2 rounded-full mt-3 overflow-hidden">
          <div
            className={`h-full transition-all duration-1000 rounded-full ${
              isLowTime ? 'bg-rose-500' : 'bg-indigo-500'
            }`}
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Reading Notice */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-slate-800/40 border border-slate-700/50 rounded-xl text-xs text-slate-300">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-amber-400 flex-shrink-0" />
          <span>
            Read carefully! Once time expires, the passage will disappear completely and you will recall it from memory.
          </span>
        </div>
        <div className="flex items-center space-x-2 pl-4">
          <span className="text-slate-400">Length:</span>
          <span className="font-semibold text-white">{challenge.word_count || challenge.content.split(' ').length} words</span>
        </div>
      </div>

      {/* Passage Display Card */}
      <div className="bg-slate-900/70 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl space-y-6">
        <div className="border-b border-slate-800 pb-4 flex flex-wrap items-center justify-between gap-2">
          <div>
            <span className="text-xs font-semibold uppercase text-indigo-400 tracking-wider">
              Topic
            </span>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              {challenge.topic}
            </h2>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-medium">
              Difficulty: {challenge.difficulty}
            </span>
          </div>
        </div>

        {/* Formatted Passage Content */}
        <div className="prose prose-invert max-w-none">
          <p className="text-slate-200 text-base sm:text-lg leading-relaxed font-normal whitespace-pre-line tracking-wide">
            {challenge.content}
          </p>
        </div>
      </div>
    </div>
  );
}
