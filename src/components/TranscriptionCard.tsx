import { useState } from 'react';
import { motion } from 'framer-motion';
import { Copy, Trash2, Clock, Languages, Check } from 'lucide-react';
import { Transcription } from '@/lib/api';
import { formatDate, formatDuration, copyToClipboard } from '@/lib/utils';
import { cn } from '@/lib/utils';

interface TranscriptionCardProps {
  transcription: Transcription;
  onDelete: (id: number) => void;
}

export default function TranscriptionCard({ transcription, onDelete }: TranscriptionCardProps) {
  const [copied, setCopied] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleCopy = async () => {
    await copyToClipboard(transcription.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDelete = async () => {
    if (confirm('Delete this transcription?')) {
      setIsDeleting(true);
      onDelete(transcription.id);
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className={cn(
        'bg-surface rounded-xl p-5 border border-border',
        'hover:border-accent/50 transition-all group',
        isDeleting && 'opacity-50'
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3 text-sm text-text-muted">
          <div className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            <span>{formatDate(transcription.created_at)}</span>
          </div>
          
          {transcription.duration && (
            <div className="flex items-center gap-1">
              <span>•</span>
              <span>{formatDuration(transcription.duration)}</span>
            </div>
          )}
          
          {transcription.detected_language && (
            <div className="flex items-center gap-1">
              <Languages className="w-4 h-4" />
              <span className="uppercase">{transcription.detected_language}</span>
            </div>
          )}
        </div>

        {/* Actions - visible on hover */}
        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <motion.button
            onClick={handleCopy}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={cn(
              'p-2 rounded-lg transition-colors',
              copied
                ? 'bg-green-500/20 text-green-400'
                : 'bg-surface-elevated hover:bg-accent/20 text-text-muted hover:text-accent'
            )}
            title="Copy to clipboard"
          >
            {copied ? (
              <Check className="w-4 h-4" />
            ) : (
              <Copy className="w-4 h-4" />
            )}
          </motion.button>

          <motion.button
            onClick={handleDelete}
            disabled={isDeleting}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="p-2 rounded-lg bg-surface-elevated hover:bg-red-500/20 text-text-muted hover:text-red-400 transition-colors disabled:opacity-50"
            title="Delete transcription"
          >
            <Trash2 className="w-4 h-4" />
          </motion.button>
        </div>
      </div>

      {/* Transcription text */}
      <p className="text-text leading-relaxed">
        {transcription.text}
      </p>

      {/* Model info */}
      {transcription.model && (
        <div className="mt-3 pt-3 border-t border-border">
          <span className="text-xs text-text-muted">
            Model: <span className="font-mono">{transcription.model}</span>
          </span>
        </div>
      )}
    </motion.div>
  );
}
