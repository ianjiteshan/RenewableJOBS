import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Zap, 
  Wind, 
  Leaf, 
  Droplets, 
  Mountain, 
  TrendingUp, 
  BarChart3, 
  PieChart, 
  Download,
  Sun,
  Moon,
  Sparkles,
  Activity,
  Target,
  Calendar,
  Users,
  Factory,
  Recycle,
  Wheat
} from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import apiService from './services/api.js'
import './App.css'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
)

const sectorIcons = {
  'Solar': Sun,
  'Wind': Wind,
  'Biomass': Leaf,
  'Hydroelectric': Droplets,
  'Geothermal': Mountain,
  'Small Hydro': Droplets,
  'Waste-to-Energy': Recycle,
  'Bagasse Cogeneration': Wheat
}

const sectorColors = {
  'Solar': '#f59e0b',
  'Wind': '#06b6d4',
  'Biomass': '#10b981',
  'Hydroelectric': '#3b82f6',
  'Geothermal': '#ef4444',
  'Small Hydro': '#8b5cf6',
  'Waste-to-Energy': '#f97316',
  'Bagasse Cogeneration': '#84cc16'
}

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [sectors, setSectors] = useState([])
  const [years, setYears] = useState([])
  const [selectedSector, setSelectedSector] = useState('')
  const [selectedYear, setSelectedYear] = useState('')
  const [trendsData, setTrendsData] = useState(null)
  const [insights, setInsights] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('overview')
  
  // MW prediction states
  const [mwCapacity, setMwCapacity] = useState('')
  const [mwPrediction, setMwPrediction] = useState(null)
  const [mwSelectedSector, setMwSelectedSector] = useState('')

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode)
  }, [darkMode])

  useEffect(() => {
    loadInitialData()
  }, [])

  useEffect(() => {
    if (selectedSector) {
      loadSectorData()
    }
  }, [selectedSector])

  const loadInitialData = async () => {
    try {
      setLoading(true)
      const [sectorsResponse, yearsResponse] = await Promise.all([
        apiService.fetchSectors(),
        apiService.fetchYears()
      ])
      
      // Define the desired sector order
      const sectorOrder = ['Solar', 'Wind', 'Hydroelectric', 'Geothermal', 'Biomass']
      
      // Sort sectors according to the defined order
      const orderedSectors = sectorsResponse.sectors.sort((a, b) => {
        const indexA = sectorOrder.indexOf(a)
        const indexB = sectorOrder.indexOf(b)
        
        // If both sectors are in the order array, sort by their position
        if (indexA !== -1 && indexB !== -1) {
          return indexA - indexB
        }
        // If only one is in the order array, prioritize it
        if (indexA !== -1) return -1
        if (indexB !== -1) return 1
        // If neither is in the order array, sort alphabetically
        return a.localeCompare(b)
      })
      
      setSectors(orderedSectors)
      setYears(yearsResponse.years)
      
      // Set Solar as default if available, otherwise use first sector
      const defaultSector = orderedSectors.includes('Solar') ? 'Solar' : orderedSectors[0]
      if (defaultSector) {
        setSelectedSector(defaultSector)
      }
    } catch (err) {
      setError('Failed to load initial data')
    } finally {
      setLoading(false)
    }
  }

  const loadSectorData = async () => {
    if (!selectedSector) return
    
    try {
      setLoading(true)
      const [trendsResponse, insightsResponse] = await Promise.all([
        apiService.fetchTrends(selectedSector),
        apiService.fetchInsights(selectedSector)
      ])
      setTrendsData(trendsResponse)
      setInsights(insightsResponse)
    } catch (err) {
      setError('Failed to load sector data')
    } finally {
      setLoading(false)
    }
  }

  const handlePredict = async () => {
    if (!selectedSector || !selectedYear) return
    
    try {
      setLoading(true)
      const predictionResponse = await apiService.predictJobs(selectedSector, parseInt(selectedYear))
      setPrediction(predictionResponse)
    } catch (err) {
      setError('Failed to generate prediction')
    } finally {
      setLoading(false)
    }
  }

  const handleMwPredict = async () => {
    if (!mwSelectedSector || !mwCapacity) return
    
    try {
      setLoading(true)
      const predictionResponse = await apiService.predictJobsByMw(mwSelectedSector, parseFloat(mwCapacity))
      setMwPrediction(predictionResponse)
    } catch (err) {
      setError('Failed to generate MW-based prediction')
    } finally {
      setLoading(false)
    }
  }

  const exportData = () => {
    if (!trendsData) return
    
    const csvContent = [
      ['Year', 'Estimated Jobs', 'Actual Jobs', 'Installed Capacity (MW)'],
      ...trendsData.years.map((year, index) => [
        year,
        trendsData.estimated_jobs[index],
        trendsData.actual_jobs[index],
        trendsData.installed_capacity[index]
      ])
    ].map(row => row.join(',')).join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedSector}_employment_data.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const getChartData = () => {
    if (!trendsData) return null
    
    return {
      labels: trendsData.years,
      datasets: [
        {
          label: 'Estimated Jobs',
          data: trendsData.estimated_jobs,
          borderColor: sectorColors[selectedSector] || '#3b82f6',
          backgroundColor: `${sectorColors[selectedSector] || '#3b82f6'}20`,
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 8,
        },
        {
          label: 'Actual Jobs',
          data: trendsData.actual_jobs,
          borderColor: '#10b981',
          backgroundColor: '#10b98120',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 8,
        }
      ]
    }
  }

  const getBarChartData = () => {
    if (!trendsData) return null
    
    const recentYears = trendsData.years.slice(-5)
    const recentEstimated = trendsData.estimated_jobs.slice(-5)
    const recentActual = trendsData.actual_jobs.slice(-5)
    
    return {
      labels: recentYears,
      datasets: [
        {
          label: 'Estimated Jobs',
          data: recentEstimated,
          backgroundColor: `${sectorColors[selectedSector] || '#3b82f6'}80`,
          borderColor: sectorColors[selectedSector] || '#3b82f6',
          borderWidth: 2,
          borderRadius: 8,
        },
        {
          label: 'Actual Jobs',
          data: recentActual,
          backgroundColor: '#10b98180',
          borderColor: '#10b981',
          borderWidth: 2,
          borderRadius: 8,
        }
      ]
    }
  }

  const getSectorDistributionData = () => {
    if (!insights) return null
    
    // Mock data for sector distribution
    const mockDistribution = {
      'Solar': 35,
      'Wind': 25,
      'Hydroelectric': 15,
      'Biomass': 10,
      'Geothermal': 8,
      'Small Hydro': 4,
      'Waste-to-Energy': 2,
      'Bagasse Cogeneration': 1
    }
    
    return {
      labels: Object.keys(mockDistribution),
      datasets: [
        {
          data: Object.values(mockDistribution),
          backgroundColor: Object.keys(mockDistribution).map(sector => sectorColors[sector] || '#3b82f6'),
          borderWidth: 0,
          hoverOffset: 10,
        }
      ]
    }
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12,
            weight: '500'
          }
        }
      },
      tooltip: {
        backgroundColor: darkMode ? '#1f2937' : '#ffffff',
        titleColor: darkMode ? '#f9fafb' : '#111827',
        bodyColor: darkMode ? '#f9fafb' : '#111827',
        borderColor: darkMode ? '#374151' : '#e5e7eb',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
      }
    },
    scales: {
      x: {
        grid: {
          color: darkMode ? '#374151' : '#f3f4f6',
        },
        ticks: {
          color: darkMode ? '#9ca3af' : '#6b7280',
        }
      },
      y: {
        grid: {
          color: darkMode ? '#374151' : '#f3f4f6',
        },
        ticks: {
          color: darkMode ? '#9ca3af' : '#6b7280',
          callback: function(value) {
            return value.toLocaleString()
          }
        }
      }
    }
  }

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          usePointStyle: true,
          padding: 15,
          font: {
            size: 11,
            weight: '500'
          }
        }
      },
      tooltip: {
        backgroundColor: darkMode ? '#1f2937' : '#ffffff',
        titleColor: darkMode ? '#f9fafb' : '#111827',
        bodyColor: darkMode ? '#f9fafb' : '#111827',
        borderColor: darkMode ? '#374151' : '#e5e7eb',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        callbacks: {
          label: function(context) {
            return `${context.label}: ${context.parsed}%`
          }
        }
      }
    },
    cutout: '60%',
  }

  const SectorIcon = selectedSector ? sectorIcons[selectedSector] : Zap

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-all duration-500">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="p-2 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                  Renewable Energy Jobs Tracker
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">India Employment Analytics</p>
              </div>
            </motion.div>
            
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                onClick={exportData}
                disabled={!trendsData}
                className="hidden sm:flex"
              >
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setDarkMode(!darkMode)}
                className="p-2"
              >
                {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        {/* Controls */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">Select Sector</CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={selectedSector} onValueChange={setSelectedSector}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Choose a sector" />
                </SelectTrigger>
                <SelectContent>
                  {sectors.map((sector) => {
                    const Icon = sectorIcons[sector] || Zap
                    return (
                      <SelectItem key={sector} value={sector}>
                        <div className="flex items-center space-x-2">
                          <Icon className="h-4 w-4" style={{ color: sectorColors[sector] }} />
                          <span>{sector}</span>
                        </div>
                      </SelectItem>
                    )
                  })}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">Prediction Year</CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={selectedYear} onValueChange={setSelectedYear}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Choose a year" />
                </SelectTrigger>
                <SelectContent>
                  {[2026, 2027, 2028, 2029, 2030].map((year) => (
                    <SelectItem key={year} value={year.toString()}>
                      {year}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">Prediction</CardTitle>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={handlePredict}
                disabled={!selectedSector || !selectedYear || loading}
                className="w-full bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600"
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Predicting...</span>
                  </div>
                ) : (
                  <>
                    <Target className="h-4 w-4 mr-2" />
                    Predict Jobs
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </motion.div>

        {/* Stats Cards */}
        {insights && (
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Growth</p>
                    <p className="text-2xl font-bold text-green-600">
                      +{insights.total_growth_percentage}%
                    </p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-green-500" />
                </div>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Latest Jobs</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {insights.latest_jobs?.toLocaleString()}
                    </p>
                  </div>
                  <Users className="h-8 w-8 text-blue-500" />
                </div>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Capacity (MW)</p>
                    <p className="text-2xl font-bold text-purple-600">
                      {insights.latest_capacity?.toLocaleString()}
                    </p>
                  </div>
                  <Factory className="h-8 w-8 text-purple-500" />
                </div>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Accuracy</p>
                    <p className="text-2xl font-bold text-orange-600">
                      {insights.accuracy_percentage?.toFixed(1)}%
                    </p>
                  </div>
                  <Activity className="h-8 w-8 text-orange-500" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Prediction Result */}
        <AnimatePresence>
          {prediction && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.3 }}
              className="mb-8"
            >
              <Card className="backdrop-blur-sm bg-gradient-to-r from-green-500/10 to-blue-500/10 border-green-200 dark:border-green-800 shadow-xl">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="p-3 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl">
                        <Sparkles className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">Prediction for {prediction.year}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {selectedSector} sector employment forecast
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                        {prediction.predicted_jobs?.toLocaleString()}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">jobs</p>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center space-x-4">
                    <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                      Growth: +{prediction.growth_rate}%
                    </Badge>
                    <Badge variant="outline">
                      Model: {prediction.model_type}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Charts */}
        {selectedSector && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="grid w-full grid-cols-5 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <TabsTrigger value="overview" className="flex items-center space-x-2">
                  <BarChart3 className="h-4 w-4" />
                  <span className="hidden sm:inline">Overview</span>
                </TabsTrigger>
                <TabsTrigger value="trends" className="flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span className="hidden sm:inline">Trends</span>
                </TabsTrigger>
                <TabsTrigger value="comparison" className="flex items-center space-x-2">
                  <BarChart3 className="h-4 w-4" />
                  <span className="hidden sm:inline">Comparison</span>
                </TabsTrigger>
                <TabsTrigger value="distribution" className="flex items-center space-x-2">
                  <PieChart className="h-4 w-4" />
                  <span className="hidden sm:inline">Distribution</span>
                </TabsTrigger>
                <TabsTrigger value="mw-prediction" className="flex items-center space-x-2">
                  <Factory className="h-4 w-4" />
                  <span className="hidden sm:inline">MW Predict</span>
                </TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <SectorIcon className="h-5 w-5" style={{ color: sectorColors[selectedSector] }} />
                        <span>Employment Trends - {selectedSector}</span>
                      </CardTitle>
                      <CardDescription>
                        Historical employment data from 2014-2025
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="h-80">
                        {trendsData && (
                          <Line data={getChartData()} options={chartOptions} />
                        )}
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                    <CardHeader>
                      <CardTitle>Key Insights</CardTitle>
                      <CardDescription>
                        Statistical analysis for {selectedSector}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      {insights && (
                        <>
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span>Growth Rate</span>
                              <span className="font-medium">+{insights.total_growth_percentage}%</span>
                            </div>
                            <Progress value={Math.min(insights.total_growth_percentage, 100)} className="h-2" />
                          </div>
                          
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span>Prediction Accuracy</span>
                              <span className="font-medium">{insights.accuracy_percentage?.toFixed(1)}%</span>
                            </div>
                            <Progress value={insights.accuracy_percentage} className="h-2" />
                          </div>
                          
                          <Separator />
                          
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                              <p className="text-gray-600 dark:text-gray-400">Data Years</p>
                              <p className="font-semibold">{insights.years_of_data}</p>
                            </div>
                            <div>
                              <p className="text-gray-600 dark:text-gray-400">Latest Year</p>
                              <p className="font-semibold">{insights.latest_year}</p>
                            </div>
                          </div>
                        </>
                      )}
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="trends">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <TrendingUp className="h-5 w-5 text-blue-500" />
                      <span>Employment Trends - {selectedSector}</span>
                    </CardTitle>
                    <CardDescription>
                      Detailed view of estimated vs actual employment over time
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="h-96">
                      {trendsData && (
                        <Line data={getChartData()} options={chartOptions} />
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="comparison">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BarChart3 className="h-5 w-5 text-green-500" />
                      <span>Recent Years Comparison</span>
                    </CardTitle>
                    <CardDescription>
                      Estimated vs actual jobs for the last 5 years
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="h-96">
                      {trendsData && (
                        <Bar data={getBarChartData()} options={chartOptions} />
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="distribution">
                <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <PieChart className="h-5 w-5 text-purple-500" />
                      <span>Sector Distribution</span>
                    </CardTitle>
                    <CardDescription>
                      Employment distribution across renewable energy sectors
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="h-96">
                      <Doughnut data={getSectorDistributionData()} options={doughnutOptions} />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="mw-prediction">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <Factory className="h-5 w-5 text-purple-500" />
                        <span>MW Capacity Prediction</span>
                      </CardTitle>
                      <CardDescription>
                        Predict job numbers based on installed MW capacity
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div className="space-y-4">
                        <div>
                          <label className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2 block">
                            Select Sector
                          </label>
                          <Select value={mwSelectedSector} onValueChange={setMwSelectedSector}>
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Choose a sector" />
                            </SelectTrigger>
                            <SelectContent>
                              {sectors.map((sector) => {
                                const Icon = sectorIcons[sector] || Zap
                                return (
                                  <SelectItem key={sector} value={sector}>
                                    <div className="flex items-center space-x-2">
                                      <Icon className="h-4 w-4" style={{ color: sectorColors[sector] }} />
                                      <span>{sector}</span>
                                    </div>
                                  </SelectItem>
                                )
                              })}
                            </SelectContent>
                          </Select>
                        </div>

                        <div>
                          <label className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2 block">
                            MW Capacity
                          </label>
                          <input
                            type="number"
                            value={mwCapacity}
                            onChange={(e) => setMwCapacity(e.target.value)}
                            placeholder="Enter MW capacity"
                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            min="0"
                            step="0.1"
                          />
                        </div>

                        <Button 
                          onClick={handleMwPredict}
                          disabled={!mwSelectedSector || !mwCapacity || loading}
                          className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                        >
                          {loading ? (
                            <div className="flex items-center space-x-2">
                              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                              <span>Predicting...</span>
                            </div>
                          ) : (
                            <>
                              <Factory className="h-4 w-4 mr-2" />
                              Predict Jobs by MW
                            </>
                          )}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="backdrop-blur-sm bg-white/70 dark:bg-gray-800/70 border-0 shadow-xl">
                    <CardHeader>
                      <CardTitle>Prediction Result</CardTitle>
                      <CardDescription>
                        Jobs prediction based on MW capacity
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      {mwPrediction ? (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="space-y-6"
                        >
                          <div className="text-center p-6 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-xl border border-purple-200 dark:border-purple-800">
                            <div className="flex items-center justify-center mb-4">
                              <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl">
                                <Users className="h-6 w-6 text-white" />
                              </div>
                            </div>
                            <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                              {mwPrediction.predicted_jobs?.toLocaleString()}
                            </h3>
                            <p className="text-gray-600 dark:text-gray-400">jobs</p>
                          </div>

                          <div className="space-y-3">
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-600 dark:text-gray-400">Sector:</span>
                              <span className="font-medium">{mwPrediction.sector}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-600 dark:text-gray-400">MW Capacity:</span>
                              <span className="font-medium">{mwPrediction.mw_capacity} MW</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-600 dark:text-gray-400">Model:</span>
                              <span className="font-medium">{mwPrediction.model_type}</span>
                            </div>
                          </div>

                          <Badge variant="secondary" className="w-full justify-center bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                            Based on historical MW-to-jobs correlation
                          </Badge>
                        </motion.div>
                      ) : (
                        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                          <Factory className="h-12 w-12 mx-auto mb-4 opacity-50" />
                          <p>Enter MW capacity and select a sector to get job predictions</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </motion.div>
        )}

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mt-6"
            >
              <Card className="border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
                <CardContent className="p-4">
                  <p className="text-red-600 dark:text-red-400">{error}</p>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
       {/* Footer */}
      <footer className="container mx-auto px-6 py-6 text-center text-sm text-gray-500 dark:text-gray-400">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          Built With ❤️ For A Sustainable Future - Anjitesh Shandilya
        </motion.div>
      </footer>
    </div>
  )
}

export default App

