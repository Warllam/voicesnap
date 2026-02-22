import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Square, Loader2 } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { api } from '@/lib/api';
import { formatDuration, copyToClipboard } from '@/lib/utils';
import Waveform from './Waveform';

export default function RecordingOverlay() {
  const { isRecording, recordingDuration, setIsRecording, setRecordingDuration, addTranscription, setError } = useAppStore();
  const [audioData, setAudioData] = useState<number[][]>([]);
  const [isTranscribing, setIsTranscribing] = useState(false);

  // Update recording duration
  useEffect(() => {
    if (!isRecording) {
      setRecordingDuration(0);
      setAudioData([]);
      return;
    }

    const startTime = Date.now();
    const interval = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      setRecordingDuration(elapsed);
    }, 100);

    return () => clearInterval(interval);
  }, [isRecording, setRecordingDuration]);

  // Simulate audio data for waveform (in production, get from WebSocket)
  useEffect(() => {
    if (!isRecording) return;

    const interval = setInterval(() => {
      // Generate random audio data for visualization
      // In production, this would come from the Python backend via WebSocket
      const newData = Array.from({ length: 50 }, () =>
        Array.from({ length: 100 }, () => (Math.random() - 0.5) * 2)
      );
      setAudioData(newData);
    }, 50);

    return () => clearInterval(interval);
  }, [isRecording]);

  const handleToggleRecording = async () => {
    console.log('[RecordingOverlay] handleToggleRecording called, isRecording:', isRecording);
    
    try {
      if (isRecording) {
        console.log('[RecordingOverlay] Stopping recording...');
        // Stop recording
        setIsTranscribing(true);
        const result = await api.stopRecording();
        console.log('[RecordingOverlay] Stop recording result:', result);
        setIsRecording(false);
        setIsTranscribing(false);

        // Add transcription to list
        if (result.text) {
          console.log('[RecordingOverlay] Adding transcription to store');
          addTranscription({
            id: result.id || Date.now(),
            text: result.text,
            language: result.language,
            detected_language: result.language,
            duration: result.duration,
            audio_file: result.audio_file,
            timestamp: new Date().toISOString(),
            created_at: new Date().toISOString(),
            model: null,
            pasted: false,
            metadata: null,
          });

          // Copy to clipboard
          console.log('[RecordingOverlay] Copying to clipboard');
          await copyToClipboard(result.text);

          // Show success notification
          // TODO: Add toast notification
          console.log('[RecordingOverlay] ✅ Transcription complete!');
        }
      } else {
        console.log('[RecordingOverlay] Starting recording...');
        // Start recording
        await api.startRecording();
        console.log('[RecordingOverlay] Recording started successfully');
        setIsRecording(true);
        setAudioData([]);
      }
    } catch (error: any) {
      console.error('[RecordingOverlay] ❌ Recording error:', error);
      setIsRecording(false);
      setIsTranscribing(false);
      setError(error.message || 'Failed to toggle recording');
    }
  };

  // Global hotkey listener (Ctrl+Space via Tauri)
  useEffect(() => {
    console.log('[RecordingOverlay] Setting up hotkey listener');
    
    import('@tauri-apps/api/event').then(({ listen }) => {
      const unlisten = listen('hotkey-pressed', () => {
        console.log('[RecordingOverlay] 🔥 hotkey-pressed event received!');
        handleToggleRecording();
      });
      
      return () => {
        console.log('[RecordingOverlay] Cleaning up hotkey listener');
        unlisten.then(fn => fn());
      };
    });
  }, [isRecording, handleToggleRecording]);

  return (
    <AnimatePresence>
      {(isRecording || isTranscribing) && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className="fixed top-12 left-1/2 -translate-x-1/2 z-50"
        >
          <div className="glass rounded-2xl px-8 py-6 shadow-2xl glow min-w-[600px]">
            <div className="flex items-center gap-6">
              {/* Recording indicator */}
              <div className="flex items-center gap-3">
                {isTranscribing ? (
                  <Loader2 className="w-6 h-6 text-accent animate-spin" />
                ) : (
                  <motion.div
                    className="w-3 h-3 rounded-full bg-red-500"
                    animate={{ opacity: [1, 0.5, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  />
                )}
                
                <span className="text-lg font-medium text-text">
                  {isTranscribing ? 'Transcribing...' : 'Recording'}
                </span>
              </div>

              {/* Timer */}
              <div className="text-2xl font-mono text-accent font-bold">
                {formatDuration(recordingDuration)}
              </div>

              {/* Waveform */}
              <div className="flex-1 h-16">
                <Waveform
                  audioData={audioData}
                  isRecording={isRecording}
                  className="w-full h-full"
                />
              </div>

              {/* Stop button */}
              <motion.button
                onClick={handleToggleRecording}
                disabled={isTranscribing}
                className="w-12 h-12 rounded-xl bg-red-500 hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-colors"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Square className="w-6 h-6 text-white" fill="currentColor" />
              </motion.button>
            </div>

            {/* Hint */}
            <div className="mt-3 text-xs text-text-muted text-center">
              Press <kbd className="px-2 py-0.5 rounded bg-surface-elevated border border-border">Ctrl+Space</kbd> to stop
            </div>
          </div>
        </motion.div>
      )}

      {/* Floating record button when not recording */}
      {!isRecording && !isTranscribing && (
        <motion.button
          onClick={handleToggleRecording}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="fixed bottom-8 right-8 w-16 h-16 rounded-full bg-gradient-to-br from-accent to-accent-hover shadow-2xl glow flex items-center justify-center z-50"
        >
          <Mic className="w-7 h-7 text-white" />
        </motion.button>
      )}
    </AnimatePresence>
  );
}
