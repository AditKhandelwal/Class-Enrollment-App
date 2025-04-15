const API_BASE_URL = 'http://localhost:5000/api';

export async function getHelloMessage() {
  try {
    const response = await fetch(`${API_BASE_URL}/hello`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching from backend:', error);
    return { message: "Error" };
  }
}
