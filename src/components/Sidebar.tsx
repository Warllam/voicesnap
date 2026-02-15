import { motion } from 'framer-motion';
import { Home, Settings, Info, Activity } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { cn } from '@/lib/utils';

interface NavItem {
  id: 'transcriptions' | 'settings' | 'about';
  icon: any;
  label: string;
}

const navItems: NavItem[] = [
  { id: 'transcriptions', icon: Home, label: 'Transcriptions' },
  { id: 'settings', icon: Settings, label: 'Settings' },
  { id: 'about', icon: Info, label: 'About' },
];

export default function Sidebar() {
  const { currentPage, setCurrentPage, serverHealthy } = useAppStore();

  return (
    <aside className="w-16 bg-surface border-r border-border flex flex-col items-center py-4 gap-2">
      {/* Logo / Status */}
      <div className="mb-4 relative">
        <motion.div
          className={cn(
            'w-10 h-10 rounded-xl flex items-center justify-center',
            'bg-gradient-to-br from-accent to-accent-hover',
            'shadow-lg'
          )}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Activity className="w-5 h-5 text-white" />
        </motion.div>
        
        {/* Server status indicator */}
        <div className={cn(
          'absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-surface',
          serverHealthy ? 'bg-green-500' : 'bg-red-500'
        )} />
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 flex flex-col gap-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;

          return (
            <motion.button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={cn(
                'w-12 h-12 rounded-xl flex items-center justify-center',
                'transition-colors relative group',
                isActive
                  ? 'bg-accent/20 text-accent'
                  : 'text-text-muted hover:bg-surface-elevated hover:text-text'
              )}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              title={item.label}
            >
              <Icon className="w-5 h-5" />
              
              {/* Active indicator */}
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-accent rounded-r-full"
                  transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                />
              )}
              
              {/* Tooltip */}
              <div className="absolute left-full ml-2 px-2 py-1 bg-surface-elevated border border-border rounded-lg text-sm whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
                {item.label}
              </div>
            </motion.button>
          );
        })}
      </nav>

      {/* Keyboard shortcut hint */}
      <div className="text-xs text-text-muted text-center mt-auto">
        <div className="w-12 h-12 rounded-xl bg-surface-elevated flex items-center justify-center">
          <div className="text-[10px] font-mono">
            Ctrl+
            <br />
            Space
          </div>
        </div>
      </div>
    </aside>
  );
}
