// Types based on the database models from app/models.py

export interface PowerTypeMapping {
  power_type_id: number;
  power_type_name: string;
}

export interface GenerationData {
  id: number;
  wattage: number;
  timestamp: string;
  power_type: number;
  region: string;
}

export interface ConsumptionData {
  id: number;
  wattage: number;
  timestamp: string;
  power_type: number;
  region: string;
}

export interface ChartDataPoint {
  timestamp: string;
  wattage: number;
  power_type_name?: string;
  region: string;
}

export interface ApiResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}
