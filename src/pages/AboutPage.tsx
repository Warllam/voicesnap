import { motion } from 'framer-motion';
import { Activity, Github, Heart, Zap, Shield, Globe } from 'lucide-react';

export default function AboutPage() {
  const features = [
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Built with Tauri and Rust for native performance',
    },
    {
      icon: Shield,
      title: 'Private & Secure',
      description: 'All transcription happens locally on your machine',
    },
    {
      icon: Globe,
      title: 'Multi-language',
      description: 'Support for 99+ languages with Whisper AI',
    },
  ];

  return (
    <div className="h-full overflow-auto">
      <div className="max-w-4xl mx-auto px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', damping: 15 }}
            className="inline-flex items-center justify-center w-24 h-24 rounded-3xl bg-gradient-to-br from-accent to-accent-hover mb-6"
          >
            <Activity className="w-12 h-12 text-white" />
          </motion.div>

          <h1 className="text-4xl font-bold text-text mb-3">VoiceSnap</h1>
          <p className="text-xl text-text-muted mb-2">Modern Voice Transcription</p>
          <p className="text-sm text-text-muted">Version 3.0.0 (Tauri Edition)</p>
        </div>

        {/* Features */}
        <div className="grid grid-cols-3 gap-6 mb-12">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-surface rounded-xl p-6 border border-border text-center"
              >
                <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center mx-auto mb-4">
                  <Icon className="w-6 h-6 text-accent" />
                </div>
                <h3 className="font-semibold text-text mb-2">{feature.title}</h3>
                <p className="text-sm text-text-muted">{feature.description}</p>
              </motion.div>
            );
          })}
        </div>

        {/* Description */}
        <div className="bg-surface rounded-xl p-8 border border-border mb-8">
          <h2 className="text-2xl font-bold text-text mb-4">What is VoiceSnap?</h2>
          <div className="space-y-4 text-text-muted leading-relaxed">
            <p>
              VoiceSnap is a modern voice transcription application powered by OpenAI's Whisper AI.
              It allows you to quickly transcribe speech to text with a simple keyboard shortcut.
            </p>
            <p>
              This is the <strong className="text-accent">Tauri Edition</strong> – a complete rebuild
              with React + TypeScript + Tailwind CSS for a beautiful, modern interface.
            </p>
            <p>
              All transcription happens locally on your machine using Whisper models. Your voice data
              never leaves your computer, ensuring complete privacy.
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="bg-surface rounded-xl p-8 border border-border mb-8">
          <h2 className="text-2xl font-bold text-text mb-4">Technology Stack</h2>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-text mb-3">Frontend</h3>
              <ul className="space-y-2 text-sm text-text-muted">
                <li>• Tauri 2.x (Rust)</li>
                <li>• React 18</li>
                <li>• TypeScript</li>
                <li>• Tailwind CSS</li>
                <li>• Framer Motion</li>
                <li>• Zustand</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-text mb-3">Backend</h3>
              <ul className="space-y-2 text-sm text-text-muted">
                <li>• Python 3.11+</li>
                <li>• Flask (HTTP bridge)</li>
                <li>• OpenAI Whisper</li>
                <li>• SQLite database</li>
                <li>• SoundDevice (audio)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Keyboard Shortcuts */}
        <div className="bg-surface rounded-xl p-8 border border-border mb-8">
          <h2 className="text-2xl font-bold text-text mb-4">Keyboard Shortcuts</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-text-muted">Start/Stop Recording</span>
              <kbd className="px-3 py-2 rounded-lg bg-surface-elevated border border-border text-text font-mono">
                Ctrl + Space
              </kbd>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-text-muted">
          <p className="flex items-center justify-center gap-2 mb-4">
            Made with <Heart className="w-4 h-4 text-red-500 fill-red-500" /> by Warllam
          </p>
          <a
            href="https://github.com/Warllam/voicesnap"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-surface-elevated hover:bg-accent/20 text-text rounded-xl transition-colors"
          >
            <Github className="w-5 h-5" />
            View on GitHub
          </a>
        </div>
      </div>
    </div>
  );
}
