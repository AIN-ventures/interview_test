import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DealUpload } from './components/DealUpload';
import { DealList } from './components/DealList';
import { DealDetail } from './components/DealDetail';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16 items-center">
                <div className="flex space-x-8">
                  <Link to="/" className="text-xl font-bold text-gray-900">
                    Pitch Deck Analyzer
                  </Link>
                  <Link to="/upload" className="text-gray-600 hover:text-gray-900">
                    Upload
                  </Link>
                  <Link to="/deals" className="text-gray-600 hover:text-gray-900">
                    All Deals
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<DealList />} />
              <Route path="/upload" element={<DealUpload />} />
              <Route path="/deals" element={<DealList />} />
              <Route path="/deals/:id" element={<DealDetail />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}


