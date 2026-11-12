'use client';

interface Stay22MapProps {
  /** Full embed URL built by the backend (includes our affiliate AID). */
  src: string;
  location?: string | null;
}

/**
 * Stay22 interactive accommodation map (affiliate).
 * Docs: https://dev.stay22.com/docs/maps/parameters
 */
export default function Stay22Map({ src, location }: Stay22MapProps) {
  return (
    <div className="mt-10">
      <h2
        className="text-2xl font-bold mb-2 transition-colors"
        style={{ color: 'var(--foreground)' }}
      >
        {location ? `Explore more stays in ${location}` : 'Explore more stays'}
      </h2>
      <p
        className="text-sm mb-4 transition-colors"
        style={{ color: 'var(--card-text-secondary)' }}
      >
        Compare hotels and rentals across Booking.com, Expedia, Vrbo and more.
      </p>
      <div
        className="rounded-lg overflow-hidden"
        style={{ border: '1px solid var(--card-border)' }}
      >
        <iframe
          src={src}
          title={location ? `Accommodation map for ${location}` : 'Accommodation map'}
          className="w-full block h-[420px] md:h-[520px]"
          style={{ border: 'none' }}
          loading="lazy"
        />
      </div>
    </div>
  );
}
