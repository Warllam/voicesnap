import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Save, Mic, Brain, Keyboard, Monitor, Loader2 } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { api, AudioDevice } from '@/lib/api';

export default function SettingsPage() {
  const { config, setConfig } = useAppStore();
  const [devices, setDevices] = useState<AudioDevice[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Local state for form
  const [formData, setFormData] = useState({
    audioDevice: config?.audio.device_index ?? null,
    whisperModel: config?.whisper.model ?? 'base',
    language: config?.whisper.language ?? 'fr',
    autoPaste: config?.behavior.auto_paste ?? true,
    theme: config?.ui.theme ?? 'dark',
  });

  // Load audio devices
  useEffect(() => {
    const loadDevices = async () => {
      try {
        const deviceList = await api.getAudioDevices();
        setDevices(deviceList);
      } catch (error) {
        console.error('Failed to load audio devices:', error);
      }
    };

    loadDevices();
  }, []);

  // Update form when config changes
  useEffect(() => {
    if (config) {
      setFormData({
        audioDevice: config.audio.device_index ?? null,
        whisperModel: config.whisper.model,
        language: config.whisper.language ?? 'fr',
        autoPaste: config.behavior.auto_paste,
        theme: config.ui.theme,
      });
    }
  }, [config]);

  const handleSave = async () => {
    setIsSaving(true);
    setSaveSuccess(false);

    try {
      const updatedConfig = {
        audio: {
          ...config?.audio,
          device_index: formData.audioDevice,
        },
        whisper: {
          ...config?.whisper,
          model: formData.whisperModel,
          language: formData.language,
        },
        behavior: {
          ...config?.behavior,
          auto_paste: formData.autoPaste,
        },
        ui: {
          ...config?.ui,
          theme: formData.theme,
        },
      };

      await api.updateConfig(updatedConfig as any);
      const newConfig = await api.getConfig();
      setConfig(newConfig);

      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const Section = ({ icon: Icon, title, children }: any) => (
    <div className="bg-surface rounded-xl p-6 border border-border">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-lg bg-accent/20 flex items-center justify-center">
          <Icon className="w-5 h-5 text-accent" />
        </div>
        <h2 className="text-xl font-semibold text-text">{title}</h2>
      </div>
      <div className="space-y-4">
        {children}
      </div>
    </div>
  );

  const FormField = ({ label, children }: any) => (
    <div>
      <label className="block text-sm font-medium text-text mb-2">{label}</label>
      {children}
    </div>
  );

  return (
    <div className="h-full overflow-auto">
      <div className="max-w-4xl mx-auto px-8 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text mb-2">Settings</h1>
          <p className="text-text-muted">Configure VoiceSnap to your preferences</p>
        </div>

        {/* Settings sections */}
        <div className="space-y-6">
          {/* Audio Settings */}
          <Section icon={Mic} title="Audio Settings">
            <FormField label="Input Device">
              <select
                value={formData.audioDevice ?? ''}
                onChange={(e) => setFormData({ ...formData, audioDevice: e.target.value ? parseInt(e.target.value) : null })}
                className="w-full px-4 py-2 bg-surface-elevated border border-border rounded-lg text-text focus:outline-none focus:border-accent transition-colors"
              >
                <option value="">Default Device</option>
                {devices.map((device) => (
                  <option key={device.index} value={device.index}>
                    {device.name} ({device.channels} channels, {device.sample_rate}Hz)
                  </option>
                ))}
              </select>
            </FormField>
          </Section>

          {/* Whisper Settings */}
          <Section icon={Brain} title="Transcription Settings">
            <FormField label="Whisper Model">
              <select
                value={formData.whisperModel}
                onChange={(e) => setFormData({ ...formData, whisperModel: e.target.value })}
                className="w-full px-4 py-2 bg-surface-elevated border border-border rounded-lg text-text focus:outline-none focus:border-accent transition-colors"
              >
                <option value="tiny">Tiny (~75 MB, Very fast)</option>
                <option value="base">Base (~150 MB, Fast) ✨ Recommended</option>
                <option value="small">Small (~500 MB, Moderate)</option>
                <option value="medium">Medium (~1.5 GB, Slower)</option>
                <option value="large">Large (~3 GB, Best quality)</option>
              </select>
              <p className="text-xs text-text-muted mt-1">
                Smaller models are faster but less accurate. Larger models require more VRAM.
              </p>
            </FormField>

            <FormField label="Language">
              <select
                value={formData.language ?? ''}
                onChange={(e) => setFormData({ ...formData, language: e.target.value === '' ? 'fr' : e.target.value })}
                className="w-full px-4 py-2 bg-surface-elevated border border-border rounded-lg text-text focus:outline-none focus:border-accent transition-colors"
              >
                <option value="">Auto-detect</option>
                <option value="en">English</option>
                <option value="fr">French</option>
                <option value="es">Spanish</option>
                <option value="de">German</option>
                <option value="it">Italian</option>
                <option value="pt">Portuguese</option>
                <option value="ru">Russian</option>
                <option value="zh">Chinese</option>
                <option value="ja">Japanese</option>
                <option value="ko">Korean</option>
              </select>
            </FormField>
          </Section>

          {/* Behavior Settings */}
          <Section icon={Keyboard} title="Behavior">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-text">Auto-paste transcription</div>
                <div className="text-sm text-text-muted">Automatically paste transcribed text after recording</div>
              </div>
              <button
                onClick={() => setFormData({ ...formData, autoPaste: !formData.autoPaste })}
                className={`relative w-14 h-8 rounded-full transition-colors ${
                  formData.autoPaste ? 'bg-accent' : 'bg-surface-elevated'
                }`}
              >
                <motion.div
                  animate={{ x: formData.autoPaste ? 26 : 2 }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  className="absolute top-1 w-6 h-6 bg-white rounded-full shadow-md"
                />
              </button>
            </div>

            <div className="p-4 bg-surface-elevated rounded-lg border border-border">
              <div className="flex items-center gap-2 text-sm">
                <Keyboard className="w-4 h-4 text-accent" />
                <span className="text-text-muted">
                  Global hotkey: <kbd className="px-2 py-1 rounded bg-surface border border-border text-text">Ctrl+Space</kbd>
                </span>
              </div>
              <p className="text-xs text-text-muted mt-2">
                Press to toggle recording (works even when app is in background)
              </p>
            </div>
          </Section>

          {/* UI Settings */}
          <Section icon={Monitor} title="Appearance">
            <FormField label="Theme">
              <select
                value={formData.theme}
                onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
                className="w-full px-4 py-2 bg-surface-elevated border border-border rounded-lg text-text focus:outline-none focus:border-accent transition-colors"
              >
                <option value="dark">Dark (Default)</option>
                <option value="light">Light</option>
              </select>
              <p className="text-xs text-text-muted mt-1">
                Light theme coming soon in v3.1
              </p>
            </FormField>
          </Section>
        </div>

        {/* Save button */}
        <div className="mt-8 flex items-center gap-4">
          <motion.button
            onClick={handleSave}
            disabled={isSaving}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="px-8 py-3 bg-accent hover:bg-accent-hover text-white rounded-xl font-medium flex items-center gap-2 disabled:opacity-50 transition-colors"
          >
            {isSaving ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-5 h-5" />
                Save Settings
              </>
            )}
          </motion.button>

          {saveSuccess && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }}
              className="text-green-400 font-medium"
            >
              ✓ Settings saved successfully
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
