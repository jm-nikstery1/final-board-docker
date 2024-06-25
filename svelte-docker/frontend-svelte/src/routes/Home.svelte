<script>
    import django from "../lib/api"
    import { link } from 'svelte-spa-router'
    import {page, is_login} from "../lib/store"
    import moment from "moment/min/moment-with-locales";

    moment.locale('ko')

    let post_list = []
    let size = 10
    let total = 0
    let keyword = ''
    $: total_page = Math.ceil(total/size)

  
    function get_post_list(_page) {
        let params = {
            page: _page,
            size: size,
            keyword: keyword,
        }
        django('get', '/board/post/list/', params, (json) => {
            post_list = json.posts;
            $page = _page
            total = json.total
        })
    }
  
    $: get_post_list($page);  

  </script>
  

  <div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/post-create" 
                class="btn btn-primary">게시글 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{keyword}">
                <button class="btn btn-outline-secondary" on:click={() => get_post_list(0)}>
                    검색하기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>작성자</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each post_list as post, i}
        <tr class="text-center">
            <td>{ total - ($page * size) - i }</td>
            <td class="text-start">
                <a use:link href="/detail/{post.id}">{post.subject}</a>

                {#if post.comments.length > 0 }
                <span class="text-danger small mx-2">{post.comments.length}</span>
                {/if}                        
            </td>
            <td>{post.user ? post.user.username: ""}</td>   

            <td>{moment(post.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
     <!-- 페이징처리 시작 -->
     <ul class="pagination justify-content-center">

        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => get_post_list($page-1)}">이전</button>
        </li>

        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5} 
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => get_post_list(loop_page)}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}

        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_post_list($page+1)}">다음</button>
        </li>
    </ul>

</div>