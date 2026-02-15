"""Database manager for transcription history"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class TranscriptionDB:
    """Manages SQLite database for transcription history"""
    
    def __init__(self, db_path: str):
        """Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Transcriptions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transcriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                text TEXT NOT NULL,
                language TEXT,
                detected_language TEXT,
                model TEXT,
                duration REAL,
                audio_file TEXT,
                pasted BOOLEAN DEFAULT 0,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON transcriptions(timestamp DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON transcriptions(created_at DESC)
        """)
        
        # Full-text search (FTS5) for text search
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS transcriptions_fts 
            USING fts5(text, content='transcriptions', content_rowid='id')
        """)
        
        # Trigger to keep FTS in sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS transcriptions_ai 
            AFTER INSERT ON transcriptions BEGIN
                INSERT INTO transcriptions_fts(rowid, text) 
                VALUES (new.id, new.text);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS transcriptions_ad 
            AFTER DELETE ON transcriptions BEGIN
                DELETE FROM transcriptions_fts WHERE rowid = old.id;
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS transcriptions_au 
            AFTER UPDATE ON transcriptions BEGIN
                UPDATE transcriptions_fts 
                SET text = new.text 
                WHERE rowid = new.id;
            END
        """)
        
        self.conn.commit()
    
    def add_transcription(
        self,
        text: str,
        language: Optional[str] = None,
        detected_language: Optional[str] = None,
        model: Optional[str] = None,
        duration: Optional[float] = None,
        audio_file: Optional[str] = None,
        pasted: bool = False,
        metadata: Optional[Dict] = None
    ) -> int:
        """Add a new transcription to the database
        
        Args:
            text: Transcribed text
            language: Requested language
            detected_language: Language detected by Whisper
            model: Whisper model used
            duration: Audio duration in seconds
            audio_file: Path to audio file (if saved)
            pasted: Whether text was auto-pasted
            metadata: Additional metadata as dict
            
        Returns:
            ID of the inserted row
        """
        cursor = self.conn.cursor()
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO transcriptions 
            (text, language, detected_language, model, duration, audio_file, pasted, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (text, language, detected_language, model, duration, audio_file, pasted, metadata_json))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_transcriptions(self, limit: int = 100) -> List[Dict]:
        """Get recent transcriptions
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of transcription dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM transcriptions 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def search_transcriptions(self, query: str, limit: int = 100) -> List[Dict]:
        """Search transcriptions by text content
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching transcription dictionaries
        """
        cursor = self.conn.cursor()
        
        # Use FTS for full-text search
        cursor.execute("""
            SELECT t.* 
            FROM transcriptions t
            INNER JOIN transcriptions_fts fts ON t.id = fts.rowid
            WHERE transcriptions_fts MATCH ?
            ORDER BY t.timestamp DESC
            LIMIT ?
        """, (query, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_transcription(self, transcription_id: int) -> Optional[Dict]:
        """Get a specific transcription by ID
        
        Args:
            transcription_id: Transcription ID
            
        Returns:
            Transcription dictionary or None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transcriptions WHERE id = ?", (transcription_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def delete_transcription(self, transcription_id: int) -> bool:
        """Delete a transcription
        
        Args:
            transcription_id: Transcription ID
            
        Returns:
            True if deleted, False if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transcriptions WHERE id = ?", (transcription_id,))
        self.conn.commit()
        
        return cursor.rowcount > 0
    
    def get_statistics(self) -> Dict:
        """Get database statistics
        
        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()
        
        # Total transcriptions
        cursor.execute("SELECT COUNT(*) FROM transcriptions")
        total = cursor.fetchone()[0]
        
        # Total audio duration
        cursor.execute("SELECT SUM(duration) FROM transcriptions WHERE duration IS NOT NULL")
        total_duration = cursor.fetchone()[0] or 0
        
        # Most used language
        cursor.execute("""
            SELECT detected_language, COUNT(*) as count 
            FROM transcriptions 
            WHERE detected_language IS NOT NULL
            GROUP BY detected_language 
            ORDER BY count DESC 
            LIMIT 1
        """)
        most_used_lang = cursor.fetchone()
        
        return {
            "total_transcriptions": total,
            "total_audio_duration": total_duration,
            "most_used_language": most_used_lang[0] if most_used_lang else None,
            "database_size": self.db_path.stat().st_size if self.db_path.exists() else 0
        }
    
    def clear_all(self):
        """Clear all transcriptions (use with caution!)"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transcriptions")
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
