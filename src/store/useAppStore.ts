import { create } from 'zustand';
import { Transcription, AppConfig } from '@/lib/api';

interface AppState {
  // Recording state
  isRecording: boolean;
  recordingDuration: number;
  
  // Transcriptions
  transcriptions: Transcription[];
  selectedTranscription: Transcription | null;
  
  // Config
  config: AppConfig | null;
  
  // UI state
  currentPage: 'transcriptions' | 'settings' | 'about';
  serverHealthy: boolean;
  loading: boolean;
  error: string | null;
  
  // Actions
  setIsRecording: (isRecording: boolean) => void;
  setRecordingDuration: (duration: number) => void;
  setTranscriptions: (transcriptions: Transcription[]) => void;
  addTranscription: (transcription: Transcription) => void;
  deleteTranscription: (id: number) => void;
  setSelectedTranscription: (transcription: Transcription | null) => void;
  setConfig: (config: AppConfig) => void;
  setCurrentPage: (page: 'transcriptions' | 'settings' | 'about') => void;
  setServerHealthy: (healthy: boolean) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  isRecording: false,
  recordingDuration: 0,
  transcriptions: [],
  selectedTranscription: null,
  config: null,
  currentPage: 'transcriptions',
  serverHealthy: false,
  loading: false,
  error: null,
  
  // Actions
  setIsRecording: (isRecording) => set({ isRecording }),
  setRecordingDuration: (recordingDuration) => set({ recordingDuration }),
  setTranscriptions: (transcriptions) => set({ transcriptions }),
  addTranscription: (transcription) => set((state) => ({ 
    transcriptions: [transcription, ...state.transcriptions] 
  })),
  deleteTranscription: (id) => set((state) => ({
    transcriptions: state.transcriptions.filter(t => t.id !== id)
  })),
  setSelectedTranscription: (selectedTranscription) => set({ selectedTranscription }),
  setConfig: (config) => set({ config }),
  setCurrentPage: (currentPage) => set({ currentPage }),
  setServerHealthy: (serverHealthy) => set({ serverHealthy }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
