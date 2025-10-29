/**
 * API client for communicating with the Django backend.
 */
import axios from 'axios';
import type { Deal, DealListResponse } from '../types';

const API_BASE = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload a pitch deck PDF file.
 */
export async function uploadDeal(file: File): Promise<Deal> {
  const formData = new FormData();
  formData.append('pitch_deck', file);
  
  const response = await api.post<Deal>('/deals/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
}

/**
 * Fetch list of all deals with pagination.
 */
export async function fetchDeals(): Promise<DealListResponse> {
  const response = await api.get<DealListResponse>('/deals/');
  return response.data;
}

/**
 * Fetch a single deal by ID.
 */
export async function fetchDealById(id: string): Promise<Deal> {
  const response = await api.get<Deal>(`/deals/${id}/`);
  return response.data;
}

/**
 * Check the processing status of a deal.
 */
export async function fetchDealStatus(id: string): Promise<any> {
  const response = await api.get(`/deals/${id}/status/`);
  return response.data;
}


