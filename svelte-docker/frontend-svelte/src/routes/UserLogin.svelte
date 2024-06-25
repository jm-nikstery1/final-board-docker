<script>
    import { push } from 'svelte-spa-router'
    import django from "../lib/api"
    import Error from "../components/Error.svelte"
    import { access_token, refresh_token, username, is_login, myuser_id, oauth_check } from "../lib/store"    
    import { onMount } from "svelte";

    let error = {detail:[]}
    let login_email = ""
    let login_password = ""

    function login(event) {
        event.preventDefault()
        let url = "/users/login/"
        let params = {
            email: login_email,            
            password: login_password,
        }
        django('login', url, params, 
            (json) => {
                $access_token = json.access;  
                $refresh_token = json.refresh;
                $username = json.username;  
                $myuser_id = json.myuser_id;                                         
                $is_login = true

                push("/")
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    onMount(() => {
        if ($is_login) {
            setTimeout(() => {
                push("/")
            }, 2000);
        }
    });


</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">로그인</h5>
    <Error error={error} />
    {#if $is_login && $oauth_check }
    <h5>이미 구글 OAuth 2.0 로그인 된 상태입니다</h5>
    <h5>2초후 홈화면으로 진입</h5>

    {:else if $is_login && !$oauth_check }
    <h5>이미 일반 로그인 된 상태</h5>
    <h5>2초후 홈화면으로 진입</h5>

    {:else}
    <form method="post">
        <div class="mb-3">
            <label for="username">회원 이메일</label>
            <input type="text" class="form-control" id="email" bind:value="{login_email}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" id="password" bind:value="{login_password}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{login}">로그인</button>
    </form>
    {/if}
</div>
