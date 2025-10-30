const SESSION_KEY = 'frantai_session_id';

export const getSessionId = () => {
  return localStorage.getItem(SESSION_KEY);
};

export const setSessionId = (sessionId) => {
  localStorage.setItem(SESSION_KEY, sessionId);
};

export const clearSession = () => {
  localStorage.removeItem(SESSION_KEY);
};

export const hasSession = () => {
  return localStorage.getItem(SESSION_KEY) !== null;
};
