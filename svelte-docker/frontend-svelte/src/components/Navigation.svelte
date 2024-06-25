<script>
    import { link, push } from 'svelte-spa-router'
    import django from "../lib/api"
    import { page, access_token, refresh_token, username, is_login, oauth_check, myuser_id } from "../lib/store"

    let error = { detail: [] };

    function logout(event) {
        event.preventDefault();
        let url = "/users/logout/";
        let params = {
            refresh: $refresh_token,
        };
        django('logout', url, params, 
            (json) => {
                $access_token = ''
                $username = ''
                $is_login = false
                $oauth_check = false
                $refresh_token = ''
                $myuser_id = ''                
                
                push("/") 
            },
            (json_error) => {
                error = json_error
            }
        )
    }


</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/" on:click="{() => {$page = 0}}">게시판 프로젝트</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                {#if $is_login && $oauth_check }
                    <li class="nav-item">
                         <button class="nav-link" on:click={logout}>OAuth 로그아웃 ({$username})</button>
                    </li>
                {:else if $is_login && !$oauth_check }
                    <li class="nav-item">
                        <button class="nav-link" on:click={logout}>로그아웃 ({$username})</button>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-update">회원 수정</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                    <body>
                        <div class="login-container">
                          <a
                            href="https://accounts.google.com/o/oauth2/v2/auth?scope=profile%20email&client_id=779384489050-lj1i11epe7k9gh05digdu7otcdijqjov.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fapi%2Fusers%2Fgoogle%2Flogin%2Fcallback%2F&response_type=code"
                            class="google-login-btn"
                          >
                            <img
                              src="https://developers.google.com/identity/images/btn_google_signin_dark_normal_web.png"
                              alt="Google Login"
                            />
                          </a>
                        </div>
                        
                      </body>
                {/if}
            </ul>
        </div>
    </div>
</nav>
