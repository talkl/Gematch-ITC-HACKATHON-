
<div class="page_title">
    <h2>User Dashboard</h2>
     <hr />
</div>
<div class="Dashboard_Links">
    <a href="/add">Add a Product</a>
    <a href="/add_alert">Change Alert</a>
    <a href="/register">Update Details</a>
</div>
<br>
<hr style="width: 80%;margin: auto;" />
<br>
<div class="user_details">
    <table class="product_details">
      <tr>
        <th><strong>Desired Product Alert</strong></th>
        % if result.get('alert_keyword', None) is not None:
        <th><p style="text-align:left">{{result['alert_keyword']}}</p></th>
        % else:
        <th><p style="text-align:left">Not Set</p></th>
        % end
      </tr>
      <tr>
        <th><strong>Phone</strong></th>
        <th><p>{{result['phone_number']}}</p></th>
      </tr>
      <tr>
        <td><strong>Email:</strong></td>
        <td><p>{{result['email']}}</p></td>
      </tr>
      <tr>
        <td><strong>Country:</strong></td>
        <td><p>{{result['address']}}</p></div></td>
      </tr>
      <tr>
        <td><strong>City:</strong></td>
        <td><p>{{result['city_name']}}</p></td>
      </tr>
      <tr>
        <td><strong>Address:</strong></td>
        <td><p>{{result['country_name']}}</p></td>
      </tr>
    </table>
</div>
<br>
<br>
<div class="page_title">
    <h2>Products</h2>
</div>
<br>
% if result['products'] is None:
<p>
    You have no products currently available
</p>
% else:
    <div class="user_details">
        <table class="product_details">
        % for item in result['products']:
          <tr>
                <th><p>{{item['title']}}</p></th>
                <th><a href="/add_product">Change/Remove</a></th>
          </tr>
        % end
        </table>
    </div>
% end
