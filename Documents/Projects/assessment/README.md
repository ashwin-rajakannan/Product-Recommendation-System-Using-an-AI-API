# AI Product Recommendation System

A React-based product recommendation system that uses OpenAI's GPT API to provide intelligent product suggestions based on user preferences.

## Features

- **AI-Powered Recommendations**: Uses OpenAI GPT to understand user requirements and recommend suitable products
- **Product Catalog**: Browse a curated selection of electronics including phones, laptops, tablets, headphones, and smartwatches
- **Natural Language Search**: Describe what you're looking for in plain English (e.g., "I want a phone under $500")
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Results**: Get instant recommendations with loading states and error handling

## Technologies Used

- **React 19** with TypeScript
- **Vite** for fast development and building
- **OpenAI API** for AI-powered recommendations
- **CSS3** for responsive styling
- **Axios** for API requests

## Project Structure

```
src/
├── components/          # React components
│   ├── ProductCard.tsx  # Individual product display
│   └── SearchBox.tsx    # Search input and examples
├── data/
│   └── products.ts      # Product catalog data
├── services/
│   └── aiService.ts     # OpenAI API integration
├── types/
│   └── Product.ts       # TypeScript interfaces
├── App.tsx              # Main application component
├── App.css              # Application styles
└── main.tsx             # Application entry point
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- pnpm (or npm/yarn)
- OpenAI API key

### Installation

1. **Clone and navigate to the project**:
   ```bash
   cd assessment
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local` and add your OpenAI API key:
   ```
   VITE_OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Start the development server**:
   ```bash
   pnpm run dev
   ```

5. **Open your browser** and visit `http://localhost:5173`

### Building for Production

```bash
pnpm run build
```

The built files will be in the `dist/` directory.

## Usage

1. **Browse Products**: The app loads with all available products displayed
2. **Search with AI**: Use the search box to describe what you're looking for
   - Example: "I want a phone under $500"
   - Example: "Best laptop for programming"
   - Example: "Noise-canceling headphones"
3. **Get Recommendations**: The AI will analyze your request and show matching products
4. **View Details**: Each product card shows price, description, rating, and key features

## API Configuration

The app uses OpenAI's GPT-3.5-turbo model for generating recommendations. If the API is unavailable, it falls back to simple text matching.

### Getting an OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Create a new API key
4. Add it to your `.env.local` file

**Important**: Keep your API key secure and never commit it to version control.

## Development

### Available Scripts

- `pnpm run dev` - Start development server
- `pnpm run build` - Build for production
- `pnpm run preview` - Preview production build
- `pnpm run lint` - Run ESLint

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the application
5. Submit a pull request

## License

This project is for educational purposes as part of a technical assessment.

## Troubleshooting

### Common Issues

- **API Key Error**: Make sure your OpenAI API key is correctly set in `.env.local`
- **Build Errors**: Run `pnpm install` to ensure all dependencies are installed
- **CORS Issues**: The OpenAI client is configured with `dangerouslyAllowBrowser: true` for development

### Fallback Mode

If the OpenAI API is unavailable, the app automatically falls back to text-based search using product names, descriptions, categories, and brands.
