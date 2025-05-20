const hostname = window.location.hostname;
export const apiBaseUrl =
  (hostname === 'artloom.ru' || hostname === 'www.artloom.ru')
    ? 'https://artloom.ru/api'
    : 'http://127.0.0.1:8000';
