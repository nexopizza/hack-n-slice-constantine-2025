const API_BASE_URL = 'http://localhost:3000';

export const employeesApi = {

  async getEmployees() {
    try {
      const response = await fetch(`${API_BASE_URL}/employees`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching employees:', error);
      throw error;
    }
  },

  async deleteEmployee(employeeId) {
    try {
      const response = await fetch(`${API_BASE_URL}/employees/${employeeId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error deleting employee:', error);
      throw error;
    }
  },

  async addEmployee(employeeData) {
    try {
      const response = await fetch(`${API_BASE_URL}/employees`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(employeeData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error adding employee:', error);
      throw error;
    }
  }
};