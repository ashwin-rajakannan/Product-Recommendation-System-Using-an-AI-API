import OpenAI from 'openai';
import type { Product } from '../types/Product';

// Check if API key is available
const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
let openai: OpenAI | null = null;

if (apiKey && apiKey !== 'your_openai_api_key_here') {
  openai = new OpenAI({
    apiKey: apiKey,
    dangerouslyAllowBrowser: true
  });
}

export async function getAIRecommendations(
  userQuery: string,
  products: Product[]
): Promise<Product[]> {
  try {
    // If no API key is available, use fallback immediately
    if (!openai) {
      console.warn('OpenAI API key not configured, using fallback search');
      return getFallbackRecommendations(userQuery, products);
    }

    const productList = products.map(p => 
      `${p.id}. ${p.name} - ${p.brand} - $${p.price} - ${p.description}`
    ).join('\n');

    const prompt = `
      You are a product recommendation assistant. Based on the user's request, recommend the most suitable products from the following list.
      
      User request: "${userQuery}"
      
      Available products:
      ${productList}
      
      Please respond with ONLY the product IDs (numbers) of the recommended products, separated by commas. 
      For example: "1,3,5" if you recommend products with IDs 1, 3, and 5.
      
      Consider factors like:
      - Price requirements
      - Category preferences
      - Brand preferences
      - Features mentioned
      - Use cases described
      
      Recommend 3-5 products that best match the user's needs.
    `;

    const completion = await openai.chat.completions.create({
      messages: [{ role: "user", content: prompt }],
      model: "gpt-3.5-turbo",
      max_tokens: 100,
      temperature: 0.3,
    });

    const response = completion.choices[0]?.message?.content?.trim();
    
    if (!response) {
      throw new Error('No response from AI');
    }

    // Parse the response to get product IDs
    const productIds = response
      .split(',')
      .map(id => parseInt(id.trim()))
      .filter(id => !isNaN(id));

    // Return the matching products
    return products.filter(product => productIds.includes(product.id));
    
  } catch (error) {
    console.error('Error getting AI recommendations:', error);
    return getFallbackRecommendations(userQuery, products);
  }
}

function getFallbackRecommendations(query: string, products: Product[]): Product[] {
  const queryLower = query.toLowerCase();
  
  // Enhanced fallback matching
  return products.filter(product => {
    const searchText = `
      ${product.name} 
      ${product.description} 
      ${product.category} 
      ${product.brand} 
      ${product.features.join(' ')}
    `.toLowerCase();
    
    // Check for price mentions
    const priceMatch = query.match(/under\s+\$?(\d+)/i);
    if (priceMatch) {
      const maxPrice = parseInt(priceMatch[1]);
      if (product.price > maxPrice) return false;
    }
    
    return searchText.includes(queryLower) || 
           queryLower.split(' ').some(word => searchText.includes(word));
  }).slice(0, 5);
}