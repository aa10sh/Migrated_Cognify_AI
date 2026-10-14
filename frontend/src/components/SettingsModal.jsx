import React, { useState } from 'react';
import { X, Key, Cpu, Check, AlertCircle, Sparkles } from 'lucide-react';

const MODEL_OPTIONS = [
  'gpt-4o-mini',
  'gpt-4o',
  'gpt-4-turbo',
  'gpt-3.5-turbo',
];

export default function SettingsModal({ isOpen, onClose, config, onSaveSettings }) {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState(config?.model_name || 'gpt-4o-mini');
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setErrorMsg('');
    try {
      await onSaveSettings({
        openai_api_key: apiKey ? apiKey.trim() : undefined,
        openai_model: model,
      });
      setSaveSuccess(true);
      setTimeout(() => {
        setSaveSuccess(false);
        onClose();
      }, 1200);
    } catch (err) {
      setErrorMsg(err.message || 'Failed to update settings');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-6 relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-1.5 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="space-y-1">
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-4 h-4" />
            <span>AI Backend Configuration</span>
          </div>
          <h3 className="text-xl font-bold text-white tracking-tight">System Settings</h3>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          {/* OpenAI API Key */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-300">
              OpenAI API Key
            </label>
            <div className="relative">
              <Key className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-500" />
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={config?.has_api_key ? '••••••••••••••••••••••••' : 'sk-...'}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm font-mono"
              />
            </div>
            <p className="text-[11px] text-slate-400">
              {config?.has_api_key
                ? 'An API key is currently saved. Leave blank to keep existing key.'
                : 'CognifyAI works out of the box with offline NLP models, or enter your OpenAI key for dynamic LLM generation.'}
            </p>
          </div>

          {/* Model Selection */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-300">
              OpenAI Model Name
            </label>
            <div className="relative">
              <Cpu className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-500" />
              <select
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              >
                {MODEL_OPTIONS.map((m) => (
                  <option key={m} value={m}>
                    {m} {m === 'gpt-4o-mini' ? '(Recommended)' : ''}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {errorMsg && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {saveSuccess && (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center space-x-2">
              <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <span>Settings updated successfully!</span>
            </div>
          )}

          <div className="pt-2 flex items-center justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSaving}
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center space-x-1.5 shadow-md shadow-indigo-600/30 transition-all cursor-pointer disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Save Configuration'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
