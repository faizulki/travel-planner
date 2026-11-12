'use client';

import Link from 'next/link';
import Image from 'next/image';
import brandLogo from './brand-logo.png';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center gap-3">
              <Image
                src={brandLogo}
                alt=""
                width={36}
                height={36}
                priority
                unoptimized
                className="w-9 h-9 rounded-lg"
              />
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                TravelPlanner<span className="text-blue-600 dark:text-blue-400">Bro</span>
                <span className="ml-2 text-sm font-medium text-gray-500 dark:text-gray-400">Admin</span>
              </h1>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                href="/"
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                  pathname === '/'
                    ? 'border-blue-500 text-gray-900 dark:text-white'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                Dashboard
              </Link>
              <Link
                href="/blogs"
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                  pathname === '/blogs' || pathname?.startsWith('/blogs/')
                    ? 'border-blue-500 text-gray-900 dark:text-white'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                Blog Posts
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

