<script>
  import { push } from 'svelte-spa-router'
  import django from "../lib/api"
  import Error from "../components/Error.svelte"
  import { is_login, oauth_check } from "../lib/store"
  import { onMount } from "svelte";


  let error = {detail:[]}
  let username = ''
  let password = ''
  let password2 = ''
  let email = ''

  function create_user(event){
    event.preventDefault()
    let url = "/users/sign-up/"

    let params = {
      username: username,
      password: password,
      password2: password2,
      email: email,
    }
    django('post', url, params, 
    (json) =>{
      
      push('/')  

    },
    (json_error) => {
      error = json_error
    }
  )
  }


</script>

<div class="container">
  {#if $is_login} 
  이미 회원가입을 한 상태입니다
  <button type="button" class="btn btn-outline-primary btn-lg" on:click={() => push('/')}>홈으로 가기</button>
  {:else if !$is_login }
  <h5 class="my-3 border-bottom pb-2">일반 회원 가입</h5>
  <Error error={error} />
  <form method="post">
      <div class="mb-3">
          <label for="username">회원 이름</label>
          <input type="text" class="form-control" id="username" bind:value="{username}">
      </div>
      <div class="mb-3">
          <label for="password">비밀번호</label>
          <input type="password" class="form-control" id="password" bind:value="{password}">
      </div>
      <div class="mb-3">
          <label for="password2">비밀번호 확인</label>
          <input type="password" class="form-control" id="password2" bind:value="{password2}">
      </div>
      <div class="mb-3">
          <label for="email">이메일</label>
          <input type="text" class="form-control" id="email" bind:value="{email}">
      </div>
      <button type="submit" class="btn btn-primary" on:click="{create_user}">생성하기</button>
  </form>
  {/if}
</div>
