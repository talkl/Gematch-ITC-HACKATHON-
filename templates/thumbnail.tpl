<progress id="algorithm_progress" value="0" max="100"></progress>
<div class="left_side_other_product">
    <h1 class="attractive_header">You will get</h1>
    <h2 id="thumbnail-title">{{result['title']}}</h2><br>
    <img class="thumbnail_image_big" src={{result['images']}} alt="product image"/>
    <p>{{result['description']}}</p>
    <h4>Contact Details</h4>
    <span>Phone: {{result['phone_number']}}</span>
    <span>Email: {{result['email']}}</span>
    <h4>Location</h4>
    <span>City: {{result['city']}}</span>
    <span>Country: {{result['country']}}</span>
</div>
<div class="right_side_my_product">
    <h1 class="attractive_header">Your Offer</h1>
    <h2 id="my_prouct_title">
        <!--renders dynamically-->
    </h2>
    <select id="my_products_select">
        <!--renders dynamically-->
    </select>
    <div id="my_product_image">
        <!--renders dynamically-->
    </div>
</div>
