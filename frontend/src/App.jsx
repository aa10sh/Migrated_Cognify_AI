import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import SetupPhase from './components/SetupPhase';
import ReadingPhase from './components/ReadingPhase';
import RecallPhase from './components/RecallPhase';
import EvaluationPhase from './components/EvaluationPhase';
import ResultPhase from './components/ResultPhase';
import SettingsModal from './components/SettingsModal';

export default function App() {
  const [stage, setStage] = useState('setup');
  const [config, setConfig] = useState(null);
  const [challengeConfig, setChallengeConfig] = useState(null);
  const [challenge, setChallenge] = useState(null);
  const [userRecall, setUserRecall] = useState('');
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Fetch initial backend configuration
  const fetchConfig = async () => {
    try {
      const res = await fetch('/api/config');
      if (res.ok) {
        const data = await res.json();
        setConfig(data);
      }
    } catch (err) {
      console.warn('Could not connect to /api/config, will retry:', err);
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  // 1. Start Challenge -> generate content via API
  const handleStartChallenge = async (params) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/challenge/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: params.topic,
          word_limit: params.word_limit,
          difficulty: params.difficulty,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to generate challenge');
      }

      const challengeData = await res.json();
      setChallenge(challengeData);
      setChallengeConfig({
        ...params,
        key_concepts: challengeData.key_concepts,
      });

      // Advance to reading phase
      setStage('reading');
    } catch (err) {
      setError(err.message || 'An error occurred while generating your challenge.');
    } finally {
      setIsLoading(false);
    }
  };

  // 2. Reading Finished -> transition to recall phase
  const handleFinishReading = () => {
    setStage('recall');
  };

  // 3. Submit Recall -> invoke LangGraph evaluation
  const handleSubmitRecall = async (text) => {
    setUserRecall(text);
    setStage('evaluation');
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/challenge/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          original_text: challenge.content,
          key_concepts: challenge.key_concepts || [],
          recall_text: text,
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to evaluate recall');
      }

      const evalData = await res.json();
      setEvaluationResult(evalData);
      setStage('result');
    } catch (err) {
      setError(err.message || 'Evaluation failed. Please try again.');
      setStage('recall');
    } finally {
      setIsLoading(false);
    }
  };

  // 4. Reset & start a new challenge
  const handleNewChallenge = () => {
    setChallenge(null);
    setChallengeConfig(null);
    setUserRecall('');
    setEvaluationResult(null);
    setError(null);
    setStage('setup');
  };

  // 5. Save settings
  const handleSaveSettings = async (settings) => {
    const res = await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
    if (!res.ok) {
      throw new Error('Failed to save settings');
    }
    await fetchConfig();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Top Navbar */}
      <Navbar
        onOpenSettings={() => setIsSettingsOpen(true)}
        config={config}
      />

      {/* Main Workspace Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row items-start gap-8">
          {/* Left Sidebar */}
          <Sidebar
            stage={stage}
            challengeConfig={challengeConfig}
            onNewChallenge={handleNewChallenge}
          />

          {/* Center Main Stage Area */}
          <section className="flex-1 w-full min-w-0">
            {stage === 'setup' && (
              <SetupPhase
                config={config}
                onStartChallenge={handleStartChallenge}
                isLoading={isLoading}
                error={error}
              />
            )}

            {stage === 'reading' && challenge && (
              <ReadingPhase
                challenge={challenge}
                readingTimeMinutes={challengeConfig.reading_time}
                onFinishReading={handleFinishReading}
              />
            )}

            {stage === 'recall' && (
              <RecallPhase
                writingTimeMinutes={challengeConfig.writing_time}
                onSubmitRecall={handleSubmitRecall}
                isSubmitting={isLoading}
              />
            )}

            {stage === 'evaluation' && (
              <EvaluationPhase />
            )}

            {stage === 'result' && (
              <ResultPhase
                evaluationResult={evaluationResult}
                onNewChallenge={handleNewChallenge}
              />
            )}
          </section>
        </div>
      </main>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        config={config}
        onSaveSettings={handleSaveSettings}
      />
    </div>
  );
}
