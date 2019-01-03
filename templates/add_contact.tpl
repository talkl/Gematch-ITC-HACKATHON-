
<div class="page_title">
    <h2>Add a New Product</h2>
</div>

<form action="/add" method="post">
    <select>
      <option value="email">Email</option>
      <option value="phone">Phone</option>
    </select>
    <label for="contact_value">Value:</label>
    <input name="contact_value" type="text"/><br>
    <input value="Add Contact Details" type="submit"/>
    <span class="err">{{result['msg']}}</span>
</form>