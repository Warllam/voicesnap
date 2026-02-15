import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from './store/useAppStore';
import { api } from './lib/api';
import Sidebar from './components/Sidebar';
import RecordingOverlay from './components/RecordingOverlay';
import TranscriptionsPage from './pages/TranscriptionsPage';
import SettingsPage from './pages/SettingsPage';
import AboutPage from './pages/AboutPage';

function App() {
  const { currentPage, setServerHealthy, setConfig, setTranscriptions, setError } = useAppStore();

  useEffect(() => {
    // Check server health on mount
    const checkHealth = async () => {
      try {
        const healthy = await api.checkServerHealth();
        setServerHealthy(healthy);
        
        if (healthy) {
          // Load initial data
          const [config, transcriptions] = await Promise.all([
            api.getConfig(),
            api.getTranscriptions(100),
          ]);
          
          setConfig(config);
          setTranscriptions(transcriptions);
        }
      } catch (error) {
        console.error('Failed to check server health:', error);
        setServerHealthy(false);
        setError('Failed to connect to backend server. Please make sure Python server is running.');
      }
    };

    checkHealth();

    // Poll server health every 30 seconds
    const interval = setInterval(checkHealth, 30000);

    return () => clearInterval(interval);
  }, [setServerHealthy, setConfig, setTranscriptions, setError]);

  const renderPage = () => {
    switch (currentPage) {
      case 'transcriptions':
        return <TranscriptionsPage />;
      case 'settings':
        return <SettingsPage />;
      case 'about':
        return <AboutPage />;
      default:
        return <TranscriptionsPage />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      
      <main className="flex-1 overflow-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentPage}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="h-full"
          >
            {renderPage()}
          </motion.div>
        </AnimatePresence>
      </main>

      <RecordingOverlay />
    </div>
  );
}

export default App;
