<script>
    export let error  

    // error 객체의 키를 배열로 가져오기
    $: keys = error ? Object.keys(error) : [];
    
    // 에러 디테일이 유효한지 확인하는 조건 추가
    $: isValidError = keys.length > 0 && keys.some(key =>
        (Array.isArray(error[key]) && error[key].length > 0) ||
        (typeof error[key] === 'string' && error[key].trim() !== '')
    );
</script>



{#if isValidError}
    <div class="alert alert-info" role="alert">
        <h4> </h4>
        {#each keys as key}
            {#if Array.isArray(error[key]) && error[key].length > 0}
                {#each error[key] as message}  <!-- {user : []} 이런 응답대응용 -->
                    <div>
                        <strong>{key}:</strong> {JSON.stringify(message)}
                    </div>
                {/each}
            {:else if typeof error[key] === 'string' && error[key].trim() !== ''}   <!-- {detail: ""} 이런 응답 대응용 -->
                <div>
                    <strong>{key}:</strong> {JSON.stringify(error[key])}
                </div>
            {:else}
                <div>
                    <strong>{key}:</strong> {JSON.stringify(error[key], null, 2)}
                </div>
            {/if}
        {/each}
    </div>
{:else}
    <!-- 에러 디테일이 없을 때는 아무 것도 표시하지 않음 -->
{/if}

