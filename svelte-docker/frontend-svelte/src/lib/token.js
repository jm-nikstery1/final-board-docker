import { access_token, refresh_token, username, is_login, oauth_check } from './store';

const refreshAccessToken = async () => {
  let actualRefreshToken;
  refresh_token.subscribe(value => {
    actualRefreshToken = value;
  });

  // refresh 토큰 전송
  const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/users/token/refresh/`, {
    method: 'POST',
    headers:{
    'Content-Type':'application/json',
  },
    body: JSON.stringify({ refresh: `${actualRefreshToken}` }),
  });



  if (response.status == 200) {

    const json = await response.json();
    access_token.set(json.access);
    return json.access;
  } else {

    refresh_token.set('');
    access_token.set('');
    username.set('');
    is_login.set(false);
    oauth_check.set(false);
    return null;
  }
};

const retryRequest = async (operation, url, params, success_callback, failure_callback, originalOptions) => {
  const newAccessToken = await refreshAccessToken();
  if (newAccessToken) {
    originalOptions.headers['Authorization'] = `Bearer ${newAccessToken}`;
    const response = await fetch(url, originalOptions);
    let json;
    
    try {
      json = await response.json();
    } catch (error) {
      json = null;
    }
    

    if (response.status >= 200 && response.status < 300) {
      if (success_callback) success_callback(json);
    } else if (failure_callback) {
      failure_callback(json);
    }
  } else {
    if (failure_callback) failure_callback(alert('다시 로그인을 진행해 주세요'));   // refresh 토큰 만료
  }
};

export { refreshAccessToken, retryRequest };
