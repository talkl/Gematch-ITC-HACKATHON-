<div id="input_search">
    <form id="search" action="/search" method="post">
        <input type="text" name="user_input" placeholder="search for your needed product" size="50"/>
        <br>
        <label for="category_filter">Filter By Category</label>
        <select id="category_filter" name="category_filter">
            <!--dynamically created-->
        </select><br>
        <label for="location_filter">Filter By Location</label>
        <select id="location_filter" name="location_filter">
            <!--dynamically created-->
        </select><br>
        <input value="search" type="submit"/>
        <span class="err">{{result['msg']}}</span>
    </form>
</div>
    <div id="thumbnails_container">
    <!--dynamically created-->
</div>
