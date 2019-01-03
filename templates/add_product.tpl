
<div class="page_title">
    <h2>Add a New Product</h2>
</div>
<br>
<div class="product_form">
    <form id="add_product" action="/add" method="post">
        <label for="title">Title:</label>
        <input name="title" type="text"/><br>
        <br>
        <label for="category">Category:</label>
        <select id="category" name="category">
            <!--renders dynamically-->
        </select>
        <br>
        <br>
        <textarea id="description" name="description" rows="10" cols="70" placeholder="Enter description"></textarea><br>
        <br>
        <label for="image">Image:</label>
        <input name="image" type="text"/><br>
        <br>
        <div class="is_grouped">
            <input class="button" value="Add Product" type="submit"/>
            <a class="button" href="/dashboard">Cancel</a>
        </div>
        <span class="err">{{result['msg']}}</span>
    </form>
</div>