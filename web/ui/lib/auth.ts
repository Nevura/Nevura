const TOKEN_KEY = '';
const DEVICE_KEY = '';

export function saveToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function saveDevice(device: string) {
  localStorage.setItem(DEVICE_KEY, device);
}

export function getDevice(): string | null {
  return localStorage.getItem(DEVICE_KEY);
}

export function clearAuth() {
  removeToken();
  localStorage.removeItem(DEVICE_KEY);
}
