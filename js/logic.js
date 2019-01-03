var Gematch = {};
// global variables


//functions

Gematch.init = function () {
    $(document).ready(function () {
        Gematch.bindLogout();
        Gematch.bindAddProduct();
        Gematch.renderCategories();
        Gematch.bindSearchButton();
        Gematch.renderCountries();
        Gematch.renderCities();
        Gematch.renderMyProducts();
        Gematch.bindProgressAlgorithm();
        Gematch.bindAddAlert();
        Gematch.bindFilters();
        Gematch.renderFooter();
    });
};
Gematch.bindFilters = function() {
    var categoryFilter = $('#category_filter');
    $.get('/categories', function (result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            var categories = result['categories'];
            for (var i = 0; i < categories.length; i++) {
                var o = new Option(categories[i]['category_name'], categories[i]['category_id']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(categories[i]['category_name']);
                categoryFilter.append(o);
            }
        }
    });
    cityFilter = $('#location_filter');
    $.get('/cities', function (result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            var cities = result['cities'];
            for (var i = 0; i < cities.length; i++) {
                var o = new Option(cities[i]['city_name'], cities[i]['city_id']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(cities[i]['city_name']);
                cityFilter.append(o);
            }
            cityFilter.val('10125');
        }
    });  
}
Gematch.bindProgressAlgorithm = function() {
    var progressBar = $('#algorithm_progress');
    progressBar.on('click', function() {
        var progressCommentry = $('<h1/>').attr('id', 'commentry').html('DepthFirstSearch algorithm working...');
        progressCommentry.insertBefore($(this));
        $(this).addClass('not_clickable');
        var selfProgress = $(this);
        var circleDiv = $('<div/>').addClass('circle_of_matches');
        var listOfMatches = [];
        var wantedItem = $('#thumbnail-title').html();
        $.get('/algorithm', {'item_requested': wantedItem}, function(result) {
            if (result['STATUS'] == 'ERROR') {
                alert(result['MSG']);
            }
            else {
                listOfMatches = result['matches'];
                for (var i=0; i < listOfMatches.length; i++) {
                    var oneMatch = $('<div/>').addClass('match_container');
                    var userName = $('<h3/>').html(listOfMatches[i]['nickname']);
                    var locationItem = $('<h3/>').html(listOfMatches[i]['city_name']);
                    var itemTitle = $('<h3/>').html(listOfMatches[i]['title']);
                    var itemImage = $('<img/>').attr('src', listOfMatches[i]['images']).css('width', '100px').css('height','100px');
                    oneMatch.append(userName).append(itemTitle).append(locationItem).append(itemImage);
                    circleDiv.append(oneMatch);
                }
                
            }
        });
        var progressInterval = setInterval(function() {
            clickedBar = selfProgress;
            clickedBar.val(clickedBar.val()+1);
            if (clickedBar.val() == 100) {
                clearInterval(progressInterval);
                $('#commentry').remove();
                if (listOfMatches.length != 0) {
                    var finishedImage = $('<img/>').attr('alt', 'match found').attr('src', '../images/match_found.gif');
                    var finishedComment = $('<h1/>').html('Match found. Please check your email.');    
                } else {
                    var finishedImage = $('<img/>').attr('alt', 'no match').attr('src', '../images/confused-man.jpg');
                    var finishedComment = $('<h1/>').html("Sorry. We didn't find a match this time. add more items");    
                }
                var modal = $('<div/>').addClass('modal');
                var modalCloseButton = $('<div/>').html('X').addClass('modal_close').css('font-size','32px').on('click', function() {
                   $('.modal').remove();
                });
                // var arrow = $('<div/>').addClass('arrow');
                // var line = $('<div/>').addClass('line');
                // var point = $('<div/>').addClass('point');
                // arrow.append(line).append(point);
                modal.append(modalCloseButton).append(finishedComment).append(finishedImage).append(circleDiv);
                $('body').append(modal);
            }
        }, 20);
    });
}
Gematch.renderMyProducts = function() {
    selectMyProducts = $('#my_products_select');
    $.get('/my_products', function (result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            var myProducts = result['my_products'];
            for (var i = 0; i < myProducts.length; i++) {
                var o = new Option(myProducts[i]['item_id'], myProducts[i]['title']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(myProducts[i]['title']);
                $(o).attr('src', myProducts[i]['images']);
                selectMyProducts.append(o);
            }
            var defaultImage = $('<img/>').css('height', '100%').css('width', '100%').attr('src', $("#my_products_select option:selected").attr('src'));
            $('#my_product_image').append(defaultImage);
            $('#my_prouct_title').html($("#my_products_select option:selected").html());
            selectMyProducts.on('change', function () {
                $('#my_product_image').empty();
                var itemImageOnChange = $('<img/>').css('height', '100%').css('width', '100%').attr('src', $("#my_products_select option:selected").attr('src'));
                $('#my_product_image').append(itemImageOnChange);
                $('#my_prouct_title').html($("#my_products_select option:selected").html());
            });
        }
    });   
}
Gematch.renderFooter = function() {
    $('footer').addClass('footer');
}
Gematch.renderCountries = function() {
    countryList = $('select#country');
    $.get('/countries', function (result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            var countries = result['countries'];
            for (var i = 0; i < countries.length; i++) {
                var o = new Option(countries[i]['country_name'], countries[i]['country_id']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(countries[i]['country_name']);
                countryList.append(o);
            }
        }
    });    
}
Gematch.renderCities = function () {
    cityList = $('select#city');
    $.get('/cities', function (result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            var cities = result['cities'];
            for (var i = 0; i < cities.length; i++) {
                var o = new Option(cities[i]['city_name'], cities[i]['city_id']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(cities[i]['city_name']);
                cityList.append(o);
            }
        }
    });
}
Gematch.bindLogout = function() {
    $('#logout').on('click', function() {
        $.post('/logout',function(result) {
            alert(result['msg']);
        })
    });
}
Gematch.bindAddProduct = function() {
    var addProductForm = $("form#add_product");
    addProductForm.submit(function (e) {
        e.preventDefault();
        var submittedForm = $(this);
        $.post("/add", submittedForm.serialize(), function (result) {
            if (result["STATUS"] == "ERROR") {
                alert(result["MSG"]);
            } else {
                alert(result["MSG"]);
                Gematch.clearProductForm();
            }
        }, "json");
        return false;
    });
}
Gematch.clearProductForm = function () {
    var addProductForm = $("form#add_product");
    addProductForm.find("input, textarea").each(function () {
        $(this).val("");
    });
    addProductForm.find("input[type='submit']").val('Add Product');
};
Gematch.clearAlertForm = function () {
    var addProductForm = $("form#add_alert");
    addProductForm.find("input, textarea").each(function () {
        $(this).val("");
    });
    addProductForm.find("input[type='submit']").val('Update Alert');
};
Gematch.renderCategories = function() {
    var selectParent = $('select#category');
    $.get('/categories', function(result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            var categories = result['categories'];
            for (var i=0; i < categories.length ; i++) {
                var o = new Option(categories[i]['category_name'], categories[i]['category_id']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(categories[i]['category_name']);
                selectParent.append(o);
            }
        }
    });   
}
Gematch.bindSearchButton = function() {
    var searchForm = $('form#search');
    var thumbnailsContainer = $('#thumbnails_container');
    thumbnailsContainer.empty(); 
    searchForm.submit(function (e) {
        e.preventDefault();
        var submittedForm = $(this);
        Gematch.renderThumbnails(submittedForm.serialize());
        submittedForm.find("input[type='text']").val("");
        return false;
    });

}
Gematch.renderThumbnails = function(userText) {
    var thumbnailsContainer = $('#thumbnails_container');
    $.post('/search', userText, function (result) {
        if (result['STATUS'] == 'ERROR') {
            alert(result['MSG']);
        }
        else {
            thumbnailsContainer.empty();
            var items = result['items'];
            for (var i = 0; i < items.length; i++) {
                var image = $('<img/>').attr('src', items[i]['images']).attr('alt', 'product image');
                var imageContainer = $('<div/>').addClass('thumbnail_image');
                imageContainer.append(image);
                var title = $('<div/>').addClass('thumbnail_title').html(items[i]['title']);
                var thumbnail = $('<a/>').addClass('thumbnail').attr('id', items[i]['item_id']);
                var url = "/view/thumbnail?id=" + items[i]['item_id'];
                thumbnail.attr("href", url)
                thumbnail.append(title).append(imageContainer);
                thumbnailsContainer.append(thumbnail)
            }
            if (items.length == 0) {
                thumbnailsContainer.html('No products found')
            }
        }
    });   
}

Gematch.bindAddAlert = function() {
    var addProductForm = $("form#add_alert");
    addProductForm.submit(function (e) {
        e.preventDefault();
        var submittedForm = $(this);
        $.post("/add_alert", submittedForm.serialize(), function (result) {
            if (result["STATUS"] == "ERROR") {
                alert(result["MSG"]);
            } else {
                alert(result["MSG"]);
                Gematch.clearAlertForm();
            }
        }, "json");
        return false;
    });
}


//run the logic
Gematch.init();