import { writable } from 'svelte/store';

import { onMount } from 'svelte'; // test용 프론트 jwt 받기 - oauth
import { push } from 'svelte-spa-router'; // test용 프론트 jwt 받기 - oauth


const persist_storage = (key, initValue) => {
  const storedValueStr = localStorage.getItem(key);
  let parsedValue;
  try {
    parsedValue = JSON.parse(storedValueStr);
  } catch (e) {
    parsedValue = initValue; 
  }
  const store = writable(parsedValue != null ? parsedValue : initValue);
  store.subscribe(val => {
    localStorage.setItem(key, JSON.stringify(val));
  });
  return store;
};

export const page = persist_storage('page', 0);
export const access_token = persist_storage('access', '');
export const refresh_token = persist_storage('refresh', '');
export const is_login = persist_storage('is_login', false);
export const oauth_check = persist_storage('oauth_check', false);
export const username = persist_storage('username', '');
export const myuser_id = persist_storage('myuser_id', '');
