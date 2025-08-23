const API_BASE_URL = 'https://renewable-jobs-backend.onrender.com/api/jobs';

class ApiService {
  async fetchSectors() {
    try {
      const response = await fetch(`${API_BASE_URL}/sectors`)
      if (!response.ok) throw new Error('Failed to fetch sectors')
      return await response.json()
    } catch (error) {
      console.error('Error fetching sectors:', error)
      throw error
    }
  }

  async fetchYears() {
    try {
      const response = await fetch(`${API_BASE_URL}/years`)
      if (!response.ok) throw new Error('Failed to fetch years')
      return await response.json()
    } catch (error) {
      console.error('Error fetching years:', error)
      throw error
    }
  }

  async fetchTrends(sector) {
    try {
      const response = await fetch(`${API_BASE_URL}/trends?sector=${encodeURIComponent(sector)}`)
      if (!response.ok) throw new Error('Failed to fetch trends')
      return await response.json()
    } catch (error) {
      console.error('Error fetching trends:', error)
      throw error
    }
  }

  async fetchInsights(sector) {
    try {
      const response = await fetch(`${API_BASE_URL}/insights?sector=${encodeURIComponent(sector)}`)
      if (!response.ok) throw new Error('Failed to fetch insights')
      return await response.json()
    } catch (error) {
      console.error('Error fetching insights:', error)
      throw error
    }
  }

  async predictJobs(sector, year, installedCapacity = 0) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sector,
          year,
          installed_capacity: installedCapacity,
        }),
      })
      if (!response.ok) throw new Error('Failed to predict jobs')
      return await response.json()
    } catch (error) {
      console.error('Error predicting jobs:', error)
      throw error
    }
  }

  async predictJobsByMw(sector, mwCapacity) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict-mw`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sector,
          mw_capacity: mwCapacity,
        }),
      })
      if (!response.ok) throw new Error('Failed to predict jobs by MW')
      return await response.json()
    } catch (error) {
      console.error('Error predicting jobs by MW:', error)
      throw error
    }
  }

  async fetchData(sector = null, year = null) {
    try {
      let url = `${API_BASE_URL}/data`
      const params = new URLSearchParams()
      if (sector) params.append('sector', sector)
      if (year) params.append('year', year)
      if (params.toString()) url += `?${params.toString()}`
      
      const response = await fetch(url)
      if (!response.ok) throw new Error('Failed to fetch data')
      return await response.json()
    } catch (error) {
      console.error('Error fetching data:', error)
      throw error
    }
  }
}

export default new ApiService()

