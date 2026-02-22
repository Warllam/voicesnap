import { invoke } from "@tauri-apps/api/core";

export interface TranscriptionResult {
  id?: number;
  text: string;
  language: string | null;
  duration: number;
  audio_file: string | null;
}

export interface Transcription {
  id: number;
  timestamp: string;
  text: string;
  language: string | null;
  detected_language: string | null;
  model: string | null;
  duration: number | null;
  audio_file: string | null;
  pasted: boolean;
  metadata: string | null;
  created_at: string;
}

export interface AudioDevice {
  index: number;
  name: string;
  channels: number;
  sample_rate: number;
}

export interface AppConfig {
  version: string;
  audio: {
    sample_rate: number;
    channels: number;
    device_index: number | null;
    max_duration: number;
  };
  whisper: {
    model: string;
    language: string | null;
    task: string;
  };
  hotkey: {
    modifiers: string[];
    key: string;
    toggle_mode: boolean;
  };
  behavior: {
    auto_paste: boolean;
    copy_to_clipboard: boolean;
    minimize_to_tray: boolean;
    start_minimized: boolean;
    run_on_startup: boolean;
  };
  ui: {
    theme: string;
    overlay_position: string;
    overlay_style: string;
    overlay_height: number;
    show_notifications: boolean;
  };
}

// Tauri command wrappers
export const api = {
  checkServerHealth: async (): Promise<boolean> => {
    return await invoke<boolean>("check_server_health");
  },

  startRecording: async (): Promise<boolean> => {
    console.log('[API] 📥 Calling Tauri command: start_recording');
    const result = await invoke<boolean>("start_recording");
    console.log('[API] ✅ start_recording response:', result);
    return result;
  },

  stopRecording: async (): Promise<TranscriptionResult> => {
    console.log('[API] 📥 Calling Tauri command: stop_recording');
    const result = await invoke<TranscriptionResult>("stop_recording");
    console.log('[API] ✅ stop_recording response:', result);
    return result;
  },

  getAudioDevices: async (): Promise<AudioDevice[]> => {
    return await invoke<AudioDevice[]>("get_audio_devices");
  },

  getTranscriptions: async (limit?: number): Promise<Transcription[]> => {
    return await invoke<Transcription[]>("get_transcriptions", { limit });
  },

  deleteTranscription: async (id: number): Promise<boolean> => {
    return await invoke<boolean>("delete_transcription", { id });
  },

  getConfig: async (): Promise<AppConfig> => {
    return await invoke<AppConfig>("get_config");
  },

  updateConfig: async (config: Partial<AppConfig>): Promise<boolean> => {
    return await invoke<boolean>("update_config", { config });
  },

  pasteText: async (text: string): Promise<boolean> => {
    return await invoke<boolean>("paste_text", { text });
  },
};

// WebSocket for real-time waveform data
export class WaveformStream {
  private ws: WebSocket | null = null;
  private reconnectTimeout: number | null = null;
  private onDataCallback: ((data: number[][]) => void) | null = null;

  connect(onData: (data: number[][]) => void) {
    this.onDataCallback = onData;
    this.connectWebSocket();
  }

  private connectWebSocket() {
    try {
      // Connect to Python backend WebSocket for waveform data
      this.ws = new WebSocket('ws://localhost:8765/ws/waveform');
      
      this.ws.onopen = () => {
        console.log('Waveform WebSocket connected');
        if (this.reconnectTimeout) {
          clearTimeout(this.reconnectTimeout);
          this.reconnectTimeout = null;
        }
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (this.onDataCallback && data.waveform) {
            this.onDataCallback(data.waveform);
          }
        } catch (e) {
          console.error('Failed to parse waveform data:', e);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket closed, reconnecting...');
        this.reconnectTimeout = window.setTimeout(() => {
          this.connectWebSocket();
        }, 2000);
      };
    } catch (e) {
      console.error('Failed to connect WebSocket:', e);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }
}
