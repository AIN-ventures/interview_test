/**
 * TypeScript type definitions for the application.
 */

export interface Founder {
  id: string;
  name: string;
  title: string;
  background: string;
  linkedin_url?: string;
  order: number;
}

export interface Assessment {
  team_strength: number;
  market_opportunity: number;
  product_innovation: number;
  business_model: number;
  overall_score: number;
  strengths: string[];
  concerns: string[];
  investment_thesis: string;
}

export interface Deal {
  id: string;
  status: 'pending' | 'uploaded' | 'processing' | 'completed' | 'failed';
  company_name: string;
  website: string;
  location: string;
  technology_description: string;
  funding_ask: string;
  founders: Founder[];
  assessment?: Assessment;
  created_at: string;
  updated_at: string;
  processed_at: string;
  error_message?: string;
}

export interface DealListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Deal[];
}


