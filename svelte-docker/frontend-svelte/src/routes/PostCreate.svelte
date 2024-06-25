<script>
    import { push } from 'svelte-spa-router'
    import django from "../lib/api"
    import Error from "../components/Error.svelte"
    import { page, access_token, refresh_token, username, is_login } from "../lib/store"



    let error = {detail:[]}
    let subject = ''
    let content = ''

    function post_create(event) {        
        event.preventDefault()
        let url = "/board/post/create/"
        let params = {
            subject: subject,
            content: content,            
        }
        django('postcreate', url, params, 
            (json) => {              
                push("/")
            },
            (json_error) => {
                error = json_error
            }
        )
    }


</script>


<div class="container">
    <h5 class="my-3 border-bottom pb-2">게시글 등록</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{post_create}">저장하기</button>
    </form>
</div>
