const API_BASE_URL = 'http://localhost:3000'; 

export const worktimeApi = {
  // Save work time 
  async saveWorkTime(workTimeData) {
    const response = await fetch(`${API_BASE_URL}/worktime`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workTimeData),
    });
    
    if (!response.ok) throw new Error('Failed to save work time');
    return await response.json();
  },

  // Get work times by employee 
  async getWorkTimesByEmployee(employeeId) {
    const response = await fetch(`${API_BASE_URL}/worktime/employee/${employeeId}`);
    if (!response.ok) throw new Error('Failed to fetch work times');
    return await response.json();
  },

  // Update work time
  async updateWorkTime(id, workTimeData) {
    const response = await fetch(`${API_BASE_URL}/worktime/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workTimeData),
    });
    
    if (!response.ok) throw new Error('Failed to update work time');
    return await response.json();
  },


   async getWorkTimesByDate(date) {
    const response = await fetch(`${API_BASE_URL}/worktime/date/${date}`);
    if (!response.ok) throw new Error('Failed to fetch work times by date');
    return await response.json();
  },

  async getWorkTimesByDateQuery(date) {
    const response = await fetch(`${API_BASE_URL}/worktime?date=${date}`);
    if (!response.ok) throw new Error('Failed to fetch work times by date');
    return await response.json();
  }
};