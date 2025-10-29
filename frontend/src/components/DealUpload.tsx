/**
 * Component for uploading pitch deck PDFs.
 */
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { uploadDeal } from '../api/client';

export function DealUpload() {
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const uploadMutation = useMutation({
    mutationFn: uploadDeal,
    onSuccess: (data) => {
      navigate(`/deals/${data.id}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file) {
      uploadMutation.mutate(file);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-6">Upload Pitch Deck</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select PDF File
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
              disabled={uploadMutation.isPending}
            />
          </div>

          {uploadMutation.isError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              <p className="font-medium">Upload Failed</p>
              <p className="text-sm mt-1">
                {(uploadMutation.error as any)?.response?.data?.error || 
                 'Error uploading file. Please try again.'}
              </p>
            </div>
          )}

          <button
            type="submit"
            disabled={!file || uploadMutation.isPending}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md
              hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed
              font-medium transition-colors"
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Upload & Analyze'}
          </button>
        </form>

        <div className="mt-6 p-4 bg-blue-50 rounded-md">
          <h3 className="text-sm font-medium text-blue-900 mb-2">What happens next?</h3>
          <ol className="text-sm text-blue-700 space-y-1 list-decimal list-inside">
            <li>Your pitch deck will be uploaded to the server</li>
            <li>AI will extract company information and founder details</li>
            <li>The system will generate an investment assessment</li>
            <li>Results will be displayed (usually takes 1-2 minutes)</li>
          </ol>
        </div>
      </div>
    </div>
  );
}


