<div>
    <h2>Sign In</h2>
</div>
<br>
<form action="/login" method="post">
    Username: <input name="nickname" type="text"/>
    <br>
    <br>
    Password: <input name="password" type="password"/>
    <br>
    <br>
    <input type="hidden" name="next_url" value="{{result['next_url']}}"/>
    <div class="is_grouped">
        <input class="button" value="Login" type="submit"/>
        <a href="/register">No User? Register Here</a>
    </div>
    <span class="err">{{result['err_msg']}}</span>
</form>
