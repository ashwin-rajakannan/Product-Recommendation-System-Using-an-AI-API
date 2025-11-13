import { useState, useEffect } from 'react';
import ProductCard from './components/ProductCard';
import SearchBox from './components/SearchBox';
import { products } from './data/products';
import { getAIRecommendations } from './services/aiService';
import type { Product } from './types/Product';
import './App.css';

function App() {
  const [displayedProducts, setDisplayedProducts] = useState<Product[]>(products);
  const [isLoading, setIsLoading] = useState(false);
  const [lastQuery, setLastQuery] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [apiStatus, setApiStatus] = useState<'checking' | 'available' | 'fallback'>('checking');

  // Check API status on mount
  useEffect(() => {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    if (!apiKey || apiKey === 'your_openai_api_key_here') {
      setApiStatus('fallback');
    } else {
      setApiStatus('available');
    }
  }, []);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setError('');
    setLastQuery(query);
    
    try {
      const recommendations = await getAIRecommendations(query, products);
      setDisplayedProducts(recommendations);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const showAllProducts = () => {
    setDisplayedProducts(products);
    setLastQuery('');
    setError('');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AI Product Recommendations</h1>
        <p>Tell us what you're looking for and get personalized product recommendations</p>
      </header>

      <main className="main">
        {apiStatus === 'fallback' && (
          <div className="api-status-warning">
            <p>
              ⚠️ <strong>Demo Mode:</strong> OpenAI API key not configured. 
              Using text-based search instead. 
              <a href="#setup" onClick={() => {
                const setup = document.createElement('div');
                setup.innerHTML = 'Add your OpenAI API key to .env.local file to enable AI recommendations';
                alert('Setup: Copy .env.example to .env.local and add your OpenAI API key');
              }}>
                Setup AI recommendations
              </a>
            </p>
          </div>
        )}
        
        <SearchBox onSearch={handleSearch} isLoading={isLoading} />
        
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        <div className="results-section">
          <div className="results-header">
            {lastQuery ? (
              <div className="search-results-info">
                <h2>AI Recommendations for: "{lastQuery}"</h2>
                <p>{displayedProducts.length} products found</p>
                <button onClick={showAllProducts} className="show-all-btn">
                  Show All Products
                </button>
              </div>
            ) : (
              <h2>All Products ({displayedProducts.length})</h2>
            )}
          </div>

          {isLoading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>Getting AI recommendations...</p>
            </div>
          ) : (
            <div className="products-grid">
              {displayedProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
              
              {displayedProducts.length === 0 && lastQuery && (
                <div className="no-results">
                  <h3>No products found</h3>
                  <p>Try adjusting your search or browse all products</p>
                  <button onClick={showAllProducts} className="show-all-btn">
                    Show All Products
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>Product Recommendation System powered by OpenAI</p>
      </footer>
    </div>
  );
}

export default App;
