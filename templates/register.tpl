
<div class="page_title">
    <h2>Register</h2>
</div>
<br>
<div class="register">
    <form class="register_form" action="/register" method="post">
        Username: <input name="nickname" type="text"/>
        <br>
        <br>
        Password: <input name="password" type="password"/>
        <br>
        <br>
        Repeat Password: <input name="password2" type="password"/>
        <br>
        <br>
        <label for="country">Country:</label>
        <select id="country" name="country">
            <!--renders dynamically-->
        </select>
              <label for="city">City:</label>
        <select id="city" name="city">
            <!--renders dynamically-->
        </select>
        <br>
        <br>
        Address: <input name="address" type="text"/>
        <br>
        <br>
        Phone: <input name="phone" type="text"/>
        <br>
        <br>
        Email: <input name="email" type="text"/>
        <br>
        <br>
        <input type="hidden" name="next_url" value="{{result['next_url']}}"/>
        <input class="button" value="register" type="submit"/>
        <span class="err">{{result['err_msg']}}</span>
    </form>
</div>