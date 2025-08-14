import React, { useState, useEffect } from 'react';
import {
  Card,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Container,
  SelectChangeEvent,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { PowerChart } from './components/PowerChart.tsx';
import { apiService } from './services/apiService.ts';

// Styled components
const AppCard = styled(Card)(({ theme }) => ({
  minHeight: '100vh',
  padding: theme.spacing(3),
  backgroundColor: '#f5f5f5',
  borderRadius: 0,
}));

const HeaderBox = styled(Box)(({ theme }) => ({
  textAlign: 'center',
  marginBottom: theme.spacing(4),
  paddingBottom: theme.spacing(2),
  borderBottom: `2px solid ${theme.palette.primary.main}`,
}));

const FilterBox = styled(Box)(({ theme }) => ({
  backgroundColor: 'white',
  padding: theme.spacing(2),
  borderRadius: theme.spacing(1),
  marginBottom: theme.spacing(3),
  boxShadow: theme.shadows[2],
}));

const ChartBox = styled(Box)(({ theme }) => ({
  backgroundColor: 'white',
  padding: theme.spacing(3),
  borderRadius: theme.spacing(1),
  minHeight: '400px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  boxShadow: theme.shadows[2],
}));

const App: React.FC = () => {
  const [selectedRegion, setSelectedRegion] = useState<string>('');
  const [selectedPowerType, setSelectedPowerType] = useState<string>('');
  const [selectedDataType, setSelectedDataType] = useState<string>('generation');
  const [powerTypes, setPowerTypes] = useState<PowerTypeMapping[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [chartData, setChartData] = useState<{
    timestamp: string;
    wattage: number;
    region: string;
    power_type_name: string;
  }[]>([]);

  // Fetch initial data from API
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [powerTypesData, regionsData] = await Promise.all([
          apiService.getPowerTypes(),
          apiService.getRegions()
        ]);
        setPowerTypes(powerTypesData);
        setRegions(regionsData);
      } catch (error) {
        console.error('Error fetching initial data:', error);
        // Fallback to mock data if API fails
        setPowerTypes([
          { power_type_id: 1, power_type_name: 'Solar' },
          { power_type_id: 2, power_type_name: 'Wind' },
        ]);
        setRegions(['Nord', 'Süd']);
      }
    };
    
    fetchInitialData();
  }, []);

  // Update chart data when filters change
  useEffect(() => {
    // In a real app, this would fetch filtered data from API
    const mockChartData: {
      timestamp: string;
      wattage: number;
      region: string;
      power_type_name: string;
    }[] = [];
    const now = new Date();
    for (let i = 0; i < 10; i++) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      mockChartData.push({
        timestamp: date.toISOString(),
        wattage: Math.random() * 1000 + 500,
        region: selectedRegion || 'All',
        power_type_name: powerTypes.find(t => t.power_type_id.toString() === selectedPowerType)?.power_type_name || 'All'
      });
    }
    setChartData(mockChartData.reverse());
  }, [selectedRegion, selectedPowerType, selectedDataType, powerTypes]);

  const handleRegionChange = (event: SelectChangeEvent) => {
    setSelectedRegion(event.target.value);
  };

  const handlePowerTypeChange = (event: SelectChangeEvent) => {
    setSelectedPowerType(event.target.value);
  };

  const handleDataTypeChange = (event: SelectChangeEvent) => {
    setSelectedDataType(event.target.value);
  };

  return (
    <Container maxWidth={false} disableGutters>
      <AppCard>
        <HeaderBox>
          <Typography variant="h3" component="h1" color="primary" fontWeight="bold">
            Strom App
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mt: 1 }}>
            Power Generation & Consumption Dashboard
          </Typography>
        </HeaderBox>

        <FilterBox>
          <Typography variant="h6" gutterBottom>
            Filter Data
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>Data Type</InputLabel>
                <Select
                  value={selectedDataType}
                  label="Data Type"
                  onChange={handleDataTypeChange}
                >
                  <MenuItem value="generation">Generation</MenuItem>
                  <MenuItem value="consumption">Consumption</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>Region</InputLabel>
                <Select
                  value={selectedRegion}
                  label="Region"
                  onChange={handleRegionChange}
                >
                  <MenuItem value="">All Regions</MenuItem>
                  {regions.map((region) => (
                    <MenuItem key={region} value={region}>
                      {region}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>Power Type</InputLabel>
                <Select
                  value={selectedPowerType}
                  label="Power Type"
                  onChange={handlePowerTypeChange}
                >
                  <MenuItem value="">All Types</MenuItem>
                  {powerTypes.map((type) => (
                    <MenuItem key={type.power_type_id} value={type.power_type_id.toString()}>
                      {type.power_type_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </FilterBox>

        <ChartBox>
          <PowerChart 
            data={chartData} 
            title={`${selectedDataType.charAt(0).toUpperCase() + selectedDataType.slice(1)} Data`}
          />
        </ChartBox>
      </AppCard>
    </Container>
  );
};

export default App;