import { useEffect, useRef } from 'react';

interface WaveformProps {
  audioData: number[][];
  isRecording: boolean;
  className?: string;
}

export default function Waveform({ audioData, isRecording, className = '' }: WaveformProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      const width = canvas.width;
      const height = canvas.height;

      // Clear canvas
      ctx.clearRect(0, 0, width, height);

      if (!audioData || audioData.length === 0) {
        // Draw flat line when no data
        ctx.strokeStyle = 'rgba(139, 148, 158, 0.3)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        ctx.lineTo(width, height / 2);
        ctx.stroke();
        return;
      }

      // Flatten audio data
      const flatData: number[] = [];
      audioData.forEach(chunk => {
        chunk.forEach(sample => flatData.push(sample));
      });

      // Downsample to fit canvas width
      const barCount = 80;
      const samplesPerBar = Math.max(1, Math.floor(flatData.length / barCount));
      const bars: number[] = [];

      for (let i = 0; i < barCount; i++) {
        const start = i * samplesPerBar;
        const end = Math.min(start + samplesPerBar, flatData.length);
        let sum = 0;
        let count = 0;

        for (let j = start; j < end; j++) {
          sum += Math.abs(flatData[j] || 0);
          count++;
        }

        const avg = count > 0 ? sum / count : 0;
        bars.push(avg);
      }

      // Normalize bars
      const maxAmplitude = Math.max(...bars, 0.1);
      const normalizedBars = bars.map(bar => bar / maxAmplitude);

      // Draw bars
      const barWidth = width / barCount;
      const gapWidth = barWidth * 0.2;
      const actualBarWidth = barWidth - gapWidth;

      normalizedBars.forEach((amplitude, i) => {
        const x = i * barWidth + gapWidth / 2;
        const barHeight = Math.max(4, amplitude * height * 0.8);
        const y = (height - barHeight) / 2;

        // Create gradient
        const gradient = ctx.createLinearGradient(x, y, x, y + barHeight);
        if (isRecording) {
          gradient.addColorStop(0, 'rgba(99, 102, 241, 0.8)');
          gradient.addColorStop(0.5, 'rgba(99, 102, 241, 1)');
          gradient.addColorStop(1, 'rgba(79, 70, 229, 0.8)');
        } else {
          gradient.addColorStop(0, 'rgba(139, 148, 158, 0.5)');
          gradient.addColorStop(0.5, 'rgba(139, 148, 158, 0.7)');
          gradient.addColorStop(1, 'rgba(139, 148, 158, 0.5)');
        }

        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, actualBarWidth, barHeight);

        // Glow effect for active recording
        if (isRecording && amplitude > 0.3) {
          ctx.shadowBlur = 10;
          ctx.shadowColor = 'rgba(99, 102, 241, 0.5)';
          ctx.fillRect(x, y, actualBarWidth, barHeight);
          ctx.shadowBlur = 0;
        }
      });

      // Continue animation if recording
      if (isRecording) {
        animationRef.current = requestAnimationFrame(draw);
      }
    };

    draw();

    if (isRecording) {
      const interval = setInterval(draw, 1000 / 60); // 60 FPS
      return () => {
        clearInterval(interval);
        if (animationRef.current) {
          cancelAnimationFrame(animationRef.current);
        }
      };
    }
  }, [audioData, isRecording]);

  // Set canvas size on mount
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const updateSize = () => {
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      }
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className={className}
      style={{ width: '100%', height: '100%' }}
    />
  );
}
