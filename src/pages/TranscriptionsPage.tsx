import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { Search, Trash2, AlertCircle } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { api } from '@/lib/api';
import TranscriptionCard from '@/components/TranscriptionCard';

export default function TranscriptionsPage() {
  const { transcriptions, setTranscriptions, deleteTranscription, serverHealthy } = useAppStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Refresh transcriptions
  const refreshTranscriptions = async () => {
    setIsLoading(true);
    try {
      const data = await api.getTranscriptions(100);
      setTranscriptions(data);
    } catch (error) {
      console.error('Failed to fetch transcriptions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (serverHealthy) {
      refreshTranscriptions();
    }
  }, [serverHealthy]);

  // Handle delete
  const handleDelete = async (id: number) => {
    try {
      await api.deleteTranscription(id);
      deleteTranscription(id);
    } catch (error) {
      console.error('Failed to delete transcription:', error);
    }
  };

  // Filter transcriptions by search query
  const filteredTranscriptions = searchQuery
    ? transcriptions.filter(t =>
        t.text.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : transcriptions;

  if (!serverHealthy) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-text mb-2">Server Not Connected</h2>
          <p className="text-text-muted">
            Please make sure the Python backend server is running.
          </p>
          <button
            onClick={refreshTranscriptions}
            className="mt-6 px-6 py-2 bg-accent hover:bg-accent-hover text-white rounded-lg transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="px-8 py-6 border-b border-border">
        <h1 className="text-3xl font-bold text-text mb-6">Transcriptions</h1>

        {/* Search bar */}
        <div className="relative max-w-2xl">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" />
          <input
            type="text"
            placeholder="Search transcriptions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-3 bg-surface border border-border rounded-xl text-text placeholder-text-muted focus:outline-none focus:border-accent transition-colors"
          />
        </div>

        {/* Stats */}
        <div className="mt-4 flex items-center gap-6 text-sm text-text-muted">
          <span>
            <span className="font-semibold text-text">{transcriptions.length}</span> total transcriptions
          </span>
          {searchQuery && (
            <span>
              <span className="font-semibold text-text">{filteredTranscriptions.length}</span> matching
            </span>
          )}
        </div>
      </div>

      {/* Transcription list */}
      <div className="flex-1 overflow-auto px-8 py-6">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-text-muted">Loading transcriptions...</div>
          </div>
        ) : filteredTranscriptions.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-text-muted">
            {searchQuery ? (
              <>
                <Search className="w-12 h-12 mb-4 opacity-50" />
                <p>No transcriptions match your search</p>
              </>
            ) : (
              <>
                <Trash2 className="w-12 h-12 mb-4 opacity-50" />
                <p>No transcriptions yet</p>
                <p className="text-sm mt-2">Press <kbd className="px-2 py-1 rounded bg-surface border border-border">Ctrl+Space</kbd> to start recording</p>
              </>
            )}
          </div>
        ) : (
          <div className="space-y-4 max-w-4xl">
            <AnimatePresence mode="popLayout">
              {filteredTranscriptions.map((transcription) => (
                <TranscriptionCard
                  key={transcription.id}
                  transcription={transcription}
                  onDelete={handleDelete}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}
