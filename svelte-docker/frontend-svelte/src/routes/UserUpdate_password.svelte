<script>
  import { link, push } from 'svelte-spa-router'
  import { username, is_login, myuser_id, oauth_check, access_token, refresh_token } from "../lib/store"    

  import django from "../lib/api"
  import Error from "../components/Error.svelte"
  import { onMount } from "svelte";

  let error = {detail:[]} 
  let old_password = ''
  let password = ''
  let password2 = ''

  function update_password(event){
    event.preventDefault()
    let url = "/users/password-update/" + $myuser_id + "/"
    let params = {
      old_password: old_password,
      password: password,
      password2: password2,

    }

    django('update', url, params,
      (json) => {
        push('/user-update')
      },
      (json_error) => {
        error = json_error
      }
    )


  }

</script>



<div class="container">
  {#if $is_login && !$oauth_check }
    <h5 class = "my-3 border-bottom pb-2">회원 비밀번호 기준</h5>
    <Error error={error}/>
    <form method="post">
      <div class="mb-3">
        <label for="old_password">현재 비밀 번호 확인</label>
        <input type="password" class="form-control" id="old_password" bind:value={old_password} >
      </div>
      <div class="mb-3">
          <label for="password">새로운 비밀 번호 </label>
          <input type="password" class="form-control" id="password" bind:value={password}>
      </div>
      <div class="mb-3">
        <label for="password2">새로운 비밀 번호 확인</label>
        <input type="password" class="form-control" id="password2" bind:value={password2}>
    </div>
      <button type="submit" on:click="{update_password}" class="btn btn-primary" >변경하기</button>
  </form>

  {:else if $is_login && $oauth_check }
    {#await Promise.resolve() then _}
      {alert('OAuth 회원은 회원 정보 수정은 예외입니다')}
      {push('/')}
    {/await}
  {:else}
    {#await Promise.resolve() then _}
      {alert('회원 정보 수정은 로그인 후 이용해주세요')}
      {push('/')}
    {/await}

  {/if}

</div>
