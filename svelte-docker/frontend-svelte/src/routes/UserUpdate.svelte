<script>
  import { link, push } from 'svelte-spa-router'
  import { username, is_login, myuser_id, oauth_check } from "../lib/store"    


  import django from "../lib/api"
  import Error from "../components/Error.svelte"
  import { onMount } from "svelte";


  export let params = {}         
  const post_id = params.post_id  

  let error = {detail:[]}
  

</script>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .mb-3 {
    margin: 10px 0;
  }
</style>

<div class="container">
  {#if $is_login && !$oauth_check }
    <h5 class="my-3 border-bottom pb-2">회원 정보 수정</h5>

      <div class="mb-3">
        <button type="button" class="btn btn-outline-primary btn-lg" on:click={() => push('/user-update/name')}>회원 이름 수정</button>
      </div>
      <div class="mb-3">
        <button type="button" class="btn btn-outline-primary btn-lg" on:click={() => push('/user-update/password')}>회원 비밀번호 수정</button>
    </div>
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