import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Profile API
export const profileAPI = {
  getProfile: () => apiClient.get('/profile'),
};

// Chat API
export const chatAPI = {
  createSession: () => apiClient.post('/chat/session/new'),

  getSession: (sessionId) =>
    apiClient.get(`/chat/session/${sessionId}`),

  sendMessage: async function* (message, sessionId = null) {
    const response = await fetch('/api/v1/chat/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            yield data;
          }
        }
      }

      // Process any remaining buffer
      if (buffer.trim() && buffer.startsWith('data: ')) {
        const data = JSON.parse(buffer.slice(6));
        yield data;
      }
    } finally {
      reader.releaseLock();
    }
  },
};

export default apiClient;
