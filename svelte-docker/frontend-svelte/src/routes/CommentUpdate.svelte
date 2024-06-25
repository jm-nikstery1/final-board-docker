<script>
    import django from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push } from 'svelte-spa-router'

    export let params = {}
    const comment_id = params.comment_id
    

    let error = {detail:[]}
    let post_id = 0
    let text = ''

    django("get", "/board/comment/get/" + comment_id + "/", {}, (json) => {
        post_id = json.post
        text = json.text
    })

    function update_comment(event) {
        event.preventDefault()
        let url = "/board/comment/update/" + comment_id + "/"
        let params = {
            comment_id: comment_id,
            text: text,
        }
        django('update', url, params, 
            (json) => {
                push('/detail/'+post_id)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">답변 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{text}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_comment}">수정하기</button>
    </form>
</div>

