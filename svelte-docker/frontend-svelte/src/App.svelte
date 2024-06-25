<script>
  import Router from 'svelte-spa-router'
  import Home from './routes/Home.svelte'
  import Detail from "./routes/Detail.svelte"
  import PostCreate from "./routes/PostCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import PostUpdate from "./routes/PostUpdate.svelte"
  import CommentUpdate from "./routes/CommentUpdate.svelte"

  import UserUpdate from './routes/UserUpdate.svelte'
  import UserUpdateName from './routes/UserUpdate_name.svelte'
  import UserUpdatePassword from './routes/UserUpdate_password.svelte'
  import OAuthCallback from './routes/OAuthCallback.svelte'

  const routes = {
    '/': Home,
    '/detail/:post_id': Detail,
    '/post-create': PostCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/user-update': UserUpdate,
    '/user-update/name': UserUpdateName,
    '/user-update/password': UserUpdatePassword,
    '/post/update/:post_id': PostUpdate,
    '/comment/update/:comment_id': CommentUpdate,
    '/oauth/callback': OAuthCallback,
  }

</script>


<Navigation />
<Router {routes}/>

<ul>


</ul>
