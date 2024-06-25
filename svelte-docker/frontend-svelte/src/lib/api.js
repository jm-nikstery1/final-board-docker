/*
지금 보니 
일부 create 는 합칠수 있겠는데
그냥 둘까
*/
import qs from 'qs';
import { access_token, refresh_token, username, is_login, oauth_check } from './store';
import { retryRequest } from './token';

const django = (operation, url, params, success_callback, failure_callback) => {
  let method = operation;
  let content_type = 'application/json';
  let body = JSON.stringify(params);

  let actualAccessToken;
  access_token.subscribe(value => {
    actualAccessToken = value;
  });

  let actualRefreshToken;
  refresh_token.subscribe(value => {
    actualRefreshToken = value;
  });

  let actualUsername;
  username.subscribe(value => {
    actualUsername = value;
  });

  let headers_dict = {
    'Content-Type': content_type,
  };

  if (operation === 'login') {
    method = 'post';
    content_type = 'application/x-www-form-urlencoded';
    body = qs.stringify(params);
    headers_dict['Content-Type'] = content_type;
  }

  if (operation === 'logout') {
    method = 'post';
    content_type = 'application/json';
    body = JSON.stringify(params);
  }

  if (operation === 'postcreate') {
    method = 'post';
    content_type = 'application/json';
    body = JSON.stringify(params);
    headers_dict['Authorization'] = `Bearer ${actualAccessToken}`;
  }

  if (operation === 'commentcreate') {
    method = 'post';
    content_type = 'application/json';
    body = JSON.stringify(params);
    headers_dict['Authorization'] = `Bearer ${actualAccessToken}`;
  }

  if (operation === 'like') {
    method = 'post';
    headers_dict['Authorization'] = `Bearer ${actualAccessToken}`;
  }

  if (operation === 'update') {
    method = 'put';
    content_type = 'application/json';
    body = JSON.stringify(params);
    headers_dict['Authorization'] = `Bearer ${actualAccessToken}`;
  }

  if (operation === 'delete') {
    method = 'delete';
    headers_dict['Authorization'] = `Bearer ${actualAccessToken}`;
  }

  let _url = import.meta.env.VITE_SERVER_URL + url;
  if (method === 'get') {
    _url += '?' + new URLSearchParams(params);
  }

  let options = {
    method: method,
    headers: headers_dict,
  };

  if (method !== 'get') {
    options['body'] = body;
  }

  fetch(_url, options).then(response => {
    if (response.status === 204) {
      if (success_callback) {
        success_callback();
      }
      return;
    }


    response
      .json()
      .then(json => {
        if (response.status >= 200 && response.status < 300) {
          // 200 ~ 299
          if (success_callback) {
            success_callback(json);
          }
        } else if (response.status === 401) {
          if (json.code) {
            if (json.code === 'token_not_valid') {

              json = ''; 
              retryRequest(operation, _url, params, success_callback, failure_callback, options);
            } else {

              json = '';
              alert('로그인 후 이용해주세요');
            }
          } else {

            json = '';
            alert('로그인 정보가 틀립니다.');
          }
          if (failure_callback) {
            failure_callback(json);
          }
        } else {
          if (failure_callback) {
            failure_callback(json);
          } else {
            alert(JSON.stringify(json));
          }
        }
      })
      .catch(error => {
        alert(JSON.stringify(error));
      });
  });
};

export default django;
