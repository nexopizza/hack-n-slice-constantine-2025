// services/planningAPI.js
const API_BASE_URL = 'http://localhost:3000/api';

export const planningApi = {
  // Save planning data
  savePlanning: async (planningData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/planning/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(planningData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to save planning');
      }
      
      return await response.json();
    } catch (error) {
      throw new Error(`Error saving planning: ${error.message}`);
    }
  },

  // Get planning for a specific date
  getPlanning: async (date) => {
    try {
      const response = await fetch(`${API_BASE_URL}/planning?date=${date}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch planning');
      }
      
      return await response.json();
    } catch (error) {
      throw new Error(`Error fetching planning: ${error.message}`);
    }
  },

  // Update individual assignment
  updateAssignment: async (assignmentData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/planning/assignment`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assignmentData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to update assignment');
      }
      
      return await response.json();
    } catch (error) {
      throw new Error(`Error updating assignment: ${error.message}`);
    }
  },

  // Get available shifts
  getShifts: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/planning/shifts`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch shifts');
      }
      
      return await response.json();
    } catch (error) {
      throw new Error(`Error fetching shifts: ${error.message}`);
    }
  },

  // Get available tasks
  getTasks: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/planning/tasks`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }
      
      return await response.json();
    } catch (error) {
      throw new Error(`Error fetching tasks: ${error.message}`);
    }
  }
};