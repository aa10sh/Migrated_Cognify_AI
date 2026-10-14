import React, { useState, useEffect, useRef } from 'react';
import { Clock, PenTool, Send, AlertCircle, ShieldAlert } from 'lucide-react';

export default function RecallPhase({ writingTimeMinutes, onSubmitRecall, isSubmitting }) {
  const totalSeconds = Math.round(writingTimeMinutes * 60);
  const [secondsRemaining, setSecondsRemaining] = useState(totalSeconds);
  const [recallText, setRecallText] = useState('');
  const [startTime] = useState(Date.now());
  const textareaRef = useRef(null);

  // Auto-focus textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  }, []);

  // Timer countdown
  useEffect(() => {
    if (secondsRemaining <= 0) {
      handleFinalSubmit();
      return;
    }

    const timer = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleFinalSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [secondsRemaining]);

  const handleFinalSubmit = () => {
    if (isSubmitting) return;
    onSubmitRecall(recallText);
  };

  const minutes = Math.floor(secondsRemaining / 60);
  const seconds = secondsRemaining % 60;
  const progressPercent = Math.max(0, Math.min(100, (secondsRemaining / totalSeconds) * 100));

  const words = recallText.trim() ? recallText.trim().split(/\s+/).length : 0;
  const characters = recallText.length;
  const elapsedMinutes = Math.max(0.1, (Date.now() - startTime) / 60000);
  const wpm = Math.round(words / elapsedMinutes);

  const isLowTime = secondsRemaining <= 20;

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
              isLowTime ? 'bg-rose-500/20 text-rose-400' : 'bg-purple-500/20 text-purple-400'
            }`}>
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">
                Recall Time Remaining
              </span>
              <div className="text-2xl font-mono font-bold text-white">
                {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
              </div>
            </div>
          </div>

          <button
            onClick={handleFinalSubmit}
            disabled={isSubmitting}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs sm:text-sm font-semibold flex items-center space-x-2 shadow-md shadow-purple-600/20 transition-all cursor-pointer disabled:opacity-50"
          >
            {isSubmitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Submitting...</span>
              </>
            ) : (
              <>
                <span>Submit Recall</span>
                <Send className="w-4 h-4" />
              </>
            )}
          </button>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-800 h-2 rounded-full mt-3 overflow-hidden">
          <div
            className={`h-full transition-all duration-1000 rounded-full ${
              isLowTime ? 'bg-rose-500' : 'bg-purple-500'
            }`}
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Info Pill */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-slate-800/40 border border-slate-700/50 rounded-xl text-xs text-slate-300">
        <div className="flex items-center space-x-2">
          <PenTool className="w-4 h-4 text-purple-400 flex-shrink-0" />
          <span>The passage is now hidden. Write down everything you remember from memory.</span>
        </div>
      </div>

      {/* Writing Area */}
      <div className="bg-slate-900/70 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-4">
        <div className="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-3">
          <span className="font-semibold text-slate-300 uppercase tracking-wider">Your Recalled Summary</span>
          <div className="flex items-center space-x-4">
            <span>
              <strong className="text-white font-mono">{words}</strong> words
            </span>
            <span>
              <strong className="text-white font-mono">{characters}</strong> chars
            </span>
            <span>
              <strong className="text-purple-400 font-mono">{wpm}</strong> wpm
            </span>
          </div>
        </div>

        <textarea
          ref={textareaRef}
          value={recallText}
          onChange={(e) => setRecallText(e.target.value)}
          placeholder="Start typing everything you remember from the passage: main concepts, supporting details, key relationships, facts, and conclusions..."
          rows={12}
          className="w-full p-4 bg-slate-950/60 border border-slate-800 focus:border-purple-500/80 rounded-2xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 text-base leading-relaxed resize-y font-normal transition-all"
        />

        <div className="flex flex-wrap items-center justify-between pt-2 gap-2 text-xs text-slate-400">
          <span className="flex items-center space-x-1.5">
            <AlertCircle className="w-3.5 h-3.5 text-slate-400" />
            <span>Response will auto-submit when the countdown reaches 00:00.</span>
          </span>

          <button
            type="button"
            onClick={handleFinalSubmit}
            disabled={isSubmitting}
            className="sm:hidden w-full py-3 rounded-xl bg-purple-600 text-white font-semibold flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <span>Submit Recall</span>
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
