import { PowerTypeMapping, GenerationData, ConsumptionData } from '../types';

// Use environment variable or fallback to localhost
const API_BASE_URL = (window as any)?.env?.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiService {
  private async fetchData<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API fetch error:', error);
      throw error;
    }
  }

  // Get all power type mappings
  async getPowerTypes(): Promise<PowerTypeMapping[]> {
    return this.fetchData<PowerTypeMapping[]>('/power-types');
  }

  // Get all unique regions
  async getRegions(): Promise<string[]> {
    return this.fetchData<string[]>('/regions');
  }

  // Get generation data with optional filters
  async getGenerationData(filters?: {
    region?: string;
    power_type?: number;
    start_date?: string;
    end_date?: string;
    limit?: number;
  }): Promise<GenerationData[]> {
    const params = new URLSearchParams();
    if (filters?.region) params.append('region', filters.region);
    if (filters?.power_type) params.append('power_type', filters.power_type.toString());
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    if (filters?.limit) params.append('limit', filters.limit.toString());
    
    const query = params.toString() ? `?${params.toString()}` : '';
    return this.fetchData<GenerationData[]>(`/generation${query}`);
  }

  // Get consumption data with optional filters
  async getConsumptionData(filters?: {
    region?: string;
    power_type?: number;
    start_date?: string;
    end_date?: string;
    limit?: number;
  }): Promise<ConsumptionData[]> {
    const params = new URLSearchParams();
    if (filters?.region) params.append('region', filters.region);
    if (filters?.power_type) params.append('power_type', filters.power_type.toString());
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    if (filters?.limit) params.append('limit', filters.limit.toString());
    
    const query = params.toString() ? `?${params.toString()}` : '';
    return this.fetchData<ConsumptionData[]>(`/consumption${query}`);
  }
}

export const apiService = new ApiService();
