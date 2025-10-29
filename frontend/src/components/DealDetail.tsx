/**
 * BASIC deal detail view - Shows minimal information
 * 
 * TODO (CANDIDATE): Redesign this component to show richer investment analysis
 * 
 * Consider displaying:
 * - Detailed company information
 * - Founder backgrounds and experience
 * - Market analysis and opportunity size
 * - Investment assessment scores/ratings
 * - Key strengths and risks
 * - Visual charts or metrics
 * - Any other insights relevant for VC decision-making
 * 
 * The design and information architecture is up to you!
 */
import { useQuery } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import { fetchDealById } from '../api/client';

export function DealDetail() {
  const { id } = useParams<{ id: string }>();
  
  const { data: deal, isLoading } = useQuery({
    queryKey: ['deal', id],
    queryFn: () => fetchDealById(id!),
    refetchInterval: (data) => {
      // Poll while processing
      return data?.status === 'processing' || data?.status === 'uploaded' ? 2000 : false;
    },
  });

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Loading deal...</p>
      </div>
    );
  }

  if (!deal) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Deal not found</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold">
            {deal.company_name || 'Processing...'}
          </h2>
          <StatusBadge status={deal.status} />
        </div>

        {deal.status === 'failed' && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            <p className="font-medium">Processing Failed</p>
            <p className="text-sm mt-1">{deal.error_message}</p>
          </div>
        )}

        {(deal.status === 'processing' || deal.status === 'uploaded') && (
          <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded mb-4">
            <div className="flex items-center">
              <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-700 mr-3"></div>
              <p>Processing pitch deck... This may take 1-2 minutes.</p>
            </div>
          </div>
        )}

        {deal.status === 'completed' && (
          <div className="space-y-4">
            {/* BASIC DISPLAY - Candidates should enhance this! */}
            
            {deal.website && (
              <div>
                <p className="text-sm text-gray-500">Website</p>
                <a 
                  href={deal.website} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-blue-600 hover:underline"
                >
                  {deal.website}
                </a>
              </div>
            )}

            {deal.location && (
              <div>
                <p className="text-sm text-gray-500">Location</p>
                <p className="text-gray-900">{deal.location}</p>
              </div>
            )}

            {deal.technology_description && (
              <div>
                <p className="text-sm text-gray-500">Description</p>
                <p className="text-gray-700">{deal.technology_description}</p>
              </div>
            )}

            {/* TODO: Display founders, assessment, metrics, etc. */}
            {/* Design your own layout and visualizations here! */}
            
            <div className="mt-8 p-4 bg-gray-50 rounded border-2 border-dashed border-gray-300">
              <p className="text-gray-600 text-sm">
                <strong>TODO:</strong> Enhance this view to display comprehensive investment analysis.
                Consider adding visualizations, metrics, founder details, market analysis, etc.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles = {
    pending: 'bg-gray-100 text-gray-800',
    uploaded: 'bg-blue-100 text-blue-800',
    processing: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-medium ${styles[status as keyof typeof styles] || styles.pending}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}
