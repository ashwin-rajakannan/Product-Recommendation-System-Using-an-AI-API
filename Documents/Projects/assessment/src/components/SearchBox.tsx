import { useState } from 'react';

interface SearchBoxProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export default function SearchBox({ onSearch, isLoading }: SearchBoxProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const exampleQueries = [
    "I want a phone under $500",
    "Best laptop for programming",
    "Noise-canceling headphones",
    "Tablet for digital art",
    "Budget-friendly smartwatch"
  ];

  return (
    <div className="search-box">
      <form onSubmit={handleSubmit}>
        <div className="search-input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe what you're looking for... (e.g., 'I want a phone under $500')"
            className="search-input"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="search-button"
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? 'Searching...' : 'Get AI Recommendations'}
          </button>
        </div>
      </form>
      
      <div className="example-queries">
        <p>Try these examples:</p>
        <div className="example-tags">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              className="example-tag"
              onClick={() => setQuery(example)}
              disabled={isLoading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}