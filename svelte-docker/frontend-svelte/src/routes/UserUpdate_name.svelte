<script>
  import { link, push } from 'svelte-spa-router'
  import { username, is_login, myuser_id, oauth_check, access_token, refresh_token } from "../lib/store"    

  import django from "../lib/api"
  import Error from "../components/Error.svelte"

  let error = {detail:[]} 
  let password = ''
  let new_username = ''


  function update_username(event){
    event.preventDefault()
    let url = "/users/username-update/" + $myuser_id + "/"
    let params = {
      username: new_username,
      password: password,

    }

    django('update', url, params,
      (json) => {
        $username = new_username  

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
    <h5 class = "my-3 border-bottom pb-2">회원 이름 기준</h5>
    <Error error={error}/>
    <form method="post">
      <div class="mb-3">
        <label for="password">현재 비밀 번호 확인</label>
        <input type="password" class="form-control" id="password" bind:value={password}>
      </div>
      <div class="mb-3">
          <label for="username">새로운 회원 이름</label>
          <input type="text" class="form-control" id="username" bind:value={new_username}>
      </div>
      <button type="submit" on:click={update_username} class="btn btn-primary" >변경하기</button>
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
