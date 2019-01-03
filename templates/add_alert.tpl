<div>
    <h2>Add Alert</h2>
</div>
<br>
<form id="add_alert" action="/add_alert" method="post">
    Keyword: <input name="keyword" type="text"/>
    <br>
    <br>
    <input type="hidden" name="next_url" value="{{result['next_url']}}"/>
    <div class="is_grouped">
        <input class="button" value="Submit" type="submit"/>
        <a href="/dashboard">Cancel</a>
    </div>
    <span class="err">{{result['msg']}}</span>
</form>
