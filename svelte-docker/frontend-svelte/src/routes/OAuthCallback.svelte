<script>
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { access_token, refresh_token, is_login, username, oauth_check } from '../lib/store';


  let isLoading = true;
  let error = null;

  onMount(async () => {
      try {
        const cookies_check = document.cookie
          // 쿠키를 파싱하여 객체로 변환
          const cookies = document.cookie.split(';').reduce((acc, cookie) => {
              const [name, value] = cookie.trim().split('=');
              acc[name] = value;
              return acc;
          }, {});

          // 쿠키에서 토큰과 회원 이름 읽기
          const accessToken = cookies.access_token;
          const refreshToken = cookies.refresh_token;
          const user_name = cookies.username;

          if (accessToken && refreshToken) {
              // 스토어에 토큰과 회원 이름 저장
              access_token.set(accessToken);
              refresh_token.set(refreshToken);
              username.set(user_name);
              is_login.set(true);
              oauth_check.set(true);

              // 로딩 상태 해제
              isLoading = false;

              // 2초 후에 로그인 페이지로 리다이렉트
              setTimeout(() => {
                  push('/');
              }, 2000);
          } else {
              throw new Error('토큰 정보가 제공되지 않음');
          }
      } catch (err) {
          
          console.error('인증 처리 중 오류 발생:', err);
          error = err.message;
      }
  });
</script>

<style>
  .centered-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; 
    text-align: center; 
  }
</style>

<div class="centered-container">
{#if isLoading}
  <h5>Loading...</h5>
{:else if error}
  <div>{error}</div>
{:else}
  <div>
    <h5>구글 OAuth 성공!!!</h5>
    <h5>2초후 홈화면으로 진입</h5>
  </div>
{/if}
</div>