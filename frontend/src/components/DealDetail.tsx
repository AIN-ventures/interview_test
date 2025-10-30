/**
 * Enhanced Deal Detail View - Comprehensive Investment Analysis Dashboard
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
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {deal.company_name || 'Processing...'}
            </h1>
            {deal.website && (
              <a
                href={deal.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline text-sm mt-1 inline-block"
              >
                {deal.website}
              </a>
            )}
            {deal.location && (
              <p className="text-gray-600 text-sm mt-1">📍 {deal.location}</p>
            )}
          </div>
          <div className="flex items-center gap-4">
            <StatusBadge status={deal.status} />
            {deal.assessment && (
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {deal.assessment.investment_score}/10
                </div>
                <div className="text-xs text-gray-500">Investment Score</div>
              </div>
            )}
          </div>
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
      </div>

      {deal.status === 'completed' && deal.assessment && (
        <>
          {/* Investment Analysis Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Market Analysis */}
            <AnalysisCard
              title="Market Analysis"
              icon="📊"
              content={deal.assessment.market_analysis}
            />

            {/* Product Analysis */}
            <AnalysisCard
              title="Product Analysis"
              icon="🚀"
              content={deal.assessment.product_analysis}
            />

            {/* Business Model */}
            <AnalysisCard
              title="Business Model"
              icon="💼"
              content={deal.assessment.business_model}
            />
          </div>

          {/* Traction */}
          {deal.assessment.traction_analysis && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                📈 Traction & Metrics
              </h3>
              <p className="text-gray-700 whitespace-pre-line">
                {deal.assessment.traction_analysis}
              </p>
            </div>
          )}

          {/* Founders */}
          {deal.founders && deal.founders.length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                👥 Team & Founders
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {deal.founders.map((founder, idx) => (
                  <div
                    key={idx}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                  >
                    <h4 className="font-semibold text-gray-900">{founder.name}</h4>
                    <p className="text-sm text-gray-600 mt-1 whitespace-pre-line">
                      {founder.bio}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Strengths and Concerns */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Strengths */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-green-900 mb-3 flex items-center gap-2">
                ✅ Key Strengths
              </h3>
              <div className="text-gray-800 whitespace-pre-line space-y-2">
                {deal.assessment.strengths.split('\n').map((strength, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    {strength.trim().startsWith('*') ? (
                      <>
                        <span className="text-green-600 mt-1">•</span>
                        <span>{strength.replace(/^\*\s*/, '')}</span>
                      </>
                    ) : (
                      <span>{strength}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Concerns */}
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-red-900 mb-3 flex items-center gap-2">
                ⚠️ Key Concerns & Risks
              </h3>
              <div className="text-gray-800 whitespace-pre-line space-y-2">
                {deal.assessment.concerns.split('\n').map((concern, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    {concern.trim().startsWith('*') ? (
                      <>
                        <span className="text-red-600 mt-1">•</span>
                        <span>{concern.replace(/^\*\s*/, '')}</span>
                      </>
                    ) : (
                      <span>{concern}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Investment Score Visualization */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              🎯 Investment Assessment
            </h3>
            <div className="flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl font-bold text-blue-600 mb-2">
                  {deal.assessment.investment_score}
                  <span className="text-3xl text-gray-400">/10</span>
                </div>
                <div className="w-64 bg-gray-200 rounded-full h-3 mb-2">
                  <div
                    className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${(deal.assessment.investment_score / 10) * 100}%` }}
                  ></div>
                </div>
                <p className="text-gray-600 text-sm">
                  {deal.assessment.investment_score >= 8
                    ? '🔥 Strong Investment Opportunity'
                    : deal.assessment.investment_score >= 6
                    ? '✓ Worth Considering'
                    : '⚡ High Risk / Early Stage'}
                </p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

// Reusable Analysis Card Component
function AnalysisCard({ title, icon, content }: { title: string; icon: string; content: string }) {
  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
        <span>{icon}</span>
        {title}
      </h3>
      <p className="text-gray-700 whitespace-pre-line leading-relaxed">{content}</p>
    </div>
  );
}

// Status Badge Component
function StatusBadge({ status }: { status: string }) {
  const styles = {
    pending: 'bg-gray-100 text-gray-800',
    uploaded: 'bg-blue-100 text-blue-800',
    processing: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-medium ${
        styles[status as keyof typeof styles] || styles.pending
      }`}
    >
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}
