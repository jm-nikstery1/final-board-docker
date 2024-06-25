<script>
    import django from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from "svelte-spa-router"
    import {is_login, username} from "../lib/store"
    import moment from "moment/min/moment-with-locales";

    moment.locale('ko')

    export let params = {}
    let post_id = params.post_id
    let post = {comments:[], likes:[]}
    let content = ""
    let text = ""

    let error = {detail:[]}

    // 게시글 생성
    function get_post() {
        django("get", "/board/post/get/" + post_id + "/" , {}, (json) => {
            post = json
        })
    }


    get_post()

    // 게시글 댓글 생성
    function post_comment_create(event) {
        event.preventDefault()
        let url = "/board/comment/create/" + post_id + "/"
        let params = {
            text: text
        }
        django('commentcreate', url, params, 
            (json) => {
                text = ''
                error = {detail:[]}
                get_post()
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    
    //게시글 삭제
    function delete_post(post_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/board/post/delete/" + post_id + "/"
            let params = {
                post_id: post_id
            }
            django('delete', url, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    //게시글 댓글 삭제
    function delete_comment(comment_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/board/comment/delete/" + comment_id + "/"
            let params = {
                comment_id: comment_id
            }
            django('delete', url, params, 
                (json) => {
                    get_post()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }



    function like_post(post_id) {        
        let url = '/board/post/likes/' + post_id + '/'  
        let params = {
            post_id: post_id
        }
        django('like', url, params, 
            (json) => {
                get_post()
            },
            (err_json) => {
                error = err_json
            }
        )
        
    }


    function like_comment(comment_id) {        
        let url = '/board/comment/likes/' + comment_id + '/' 
        let params = {
            comment_id: comment_id
        }
        django('like', url, params, 
            (json) => {
                get_post()
            },
            (err_json) => {
                error = err_json
            }
        )
        
    }

</script>



<div class="container my-3">
    <!-- 게시글 -->
    <h2 class="border-bottom py-2">{post.subject}</h2>
    <Error error={error} />
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{post.content}</div>
            <div class="d-flex justify-content-end">
                {#if post.modify_date != post.create_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">수정한 날짜</div>
                    <div>{moment(post.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start ">
                    <div class="mb-2">{post.user ? post.user.username: ""}</div>
                    
                    <div>{moment(post.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click="{like_post(post.id)}"> 
                    추천
                    <span class="badge rounded-pill bg-success">{ post.likes.length }</span>
                </button>

                <a use:link href = "/post/update/{post_id}" 
                class= "btn btn-sm btn-outline-secondary">수정</a>

                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_post(post.id)}>삭제</button>
                
            </div>
        </div>
    </div>

    <button class="btn-secondary" on:click="{() => {
        push('/')
    }}">목록으로</button>

    <!-- 댓글 목록 -->
    <h5 class="border-bottom my-3 py-2">{post.comments.length}개의 답변이 있습니다.</h5>
    {#each post.comments as comment}
    <div class="card my-3">
        <div class="card-body">

            <div class="card-text" style="white-space: pre-line;">{comment.text}</div>
            <div class="d-flex justify-content-end">
                {#if comment.modify_date != comment.create_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">수정한 날짜</div>
                    <div>{moment(comment.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start ">
                    <div class="mb-2">{comment.user.username ? comment.user.username: ""}</div>

                    <div>{moment(comment.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click="{like_comment(comment.id)}"> 
                    추천
                    <span class="badge rounded-pill bg-success">{ comment.likes.length }</span>
                </button>

                <a use:link href="/comment/update/{comment.id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_comment(comment.id) }>삭제</button>
            </div>
        </div>
    </div>
    {/each}
    <!-- 댓글 등록 -->
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={text} class="form-control" />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary" on:click="{post_comment_create}" />

    </form>
</div>