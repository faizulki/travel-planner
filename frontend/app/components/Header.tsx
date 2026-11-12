'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useTheme } from './ThemeProvider';
import brandLogo from './brand-logo.png';

export default function Header() {
  const { theme, setTheme } = useTheme();

  const cycleTheme = () => {
    // Only toggle between light and dark
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const getThemeIcon = () => {
    if (theme === 'light') {
      return (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          style={{ color: 'var(--header-text)' }}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
          />
        </svg>
      );
    } else {
      // dark theme
      return (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          style={{ color: 'var(--header-text)' }}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
          />
        </svg>
      );
    }
  };

  return (
    <header 
      className="sticky top-0 z-50 w-full transition-colors"
      style={{
        backgroundColor: 'var(--header-bg)',
        borderBottomColor: 'var(--header-border)',
        borderBottomWidth: '1px',
        borderBottomStyle: 'solid'
      }}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/home" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <Image
              src={brandLogo}
              alt=""
              width={40}
              height={40}
              priority
              unoptimized
              className="w-10 h-10 rounded-lg"
            />
            <span
              className="text-xl font-bold tracking-tight transition-colors"
              style={{ color: 'var(--header-text)' }}
            >
              TravelPlanner<span style={{ color: '#7cc0ff' }}>Bro</span>
            </span>
          </Link>

          {/* Theme Toggle Button */}
          <div className="flex items-center gap-4">
            <button
              onClick={cycleTheme}
              className="p-2 rounded-lg transition-colors"
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.15)',
                color: 'var(--header-text)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.25)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
              }}
              aria-label={`Current theme: ${theme}. Click to toggle theme`}
              title={`Theme: ${theme}`}
            >
              {getThemeIcon()}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
