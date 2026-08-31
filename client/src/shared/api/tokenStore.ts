export class TokenStore {
  private accessToken: string | null = null;
  private isInitialized = false;
  private onTokenChange:
    | ((token: string | null, isInit: boolean) => void)
    | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
    this.isInitialized = true;
    this.onTokenChange?.(token, true);
  }

  removeAccessToken() {
    this.accessToken = null;
    this.isInitialized = true;
    this.onTokenChange?.(null, true);
  }

  setInitialized() {
    this.isInitialized = true;
    this.onTokenChange?.(this.accessToken, true);
  }

  subscribe(callback: (token: string | null, isInit: boolean) => void) {
    this.onTokenChange = callback;
  }

  getIsInitialized() {
    return this.isInitialized;
  }
  getAccessToken() {
    return this.accessToken;
  }
  hasRefreshToken() {
    return document.cookie.includes('refresh_token');
  }
}
export const tokenStore = new TokenStore();
