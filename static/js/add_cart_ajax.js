

$(document).ready(function(){
    //add to cart here worked on single product in template product_ajax.html
    $(".add-to-cart-ajax").on('click', function (){
        var _vm = $(this);
        var _index = _vm.attr('data-index');
        var _qty = $(".product-quantity-one-"+_index).val();
        var _productId = $(".product-id-one-"+_index).val();
        var _productImage = $(".product-image-one-"+_index).val();
        var _productTitle = $(".product-title-one-"+_index).val();
        var _productPrice = $(".product-price-one-"+_index).val();

        // ajax

        $.ajax({
            url: '/add-to-cart-ajax',
            data: {
                'id': _productId,
                'qty': _qty,
                'title': _productTitle,
                'image': _productImage,
                'price': _productPrice,
            },
            dataType: 'json',
            beforeSend: function (){
                _vm.attr('disabled', true);
            },
            success: function (res){
                $(".cart-list-ajax").text(res.totalitems);
                _vm.attr('disabled', false);

            }
        });


        // end
    });
    // end

    // delete item from cart in session
    $(document).on('click', '.delete-item-ajax', function (){
        var _pId = $(this).attr('data-item'); // all are behind the delete button in the list_cart_ajax.html
        var _vm = $(this);
        $.ajax({
            url: '/delete-from-cart-ajax',
            data: {
                'id': _pId,
            },
            dataType: 'json',
            beforeSend: function (){
                _vm.attr('disabled', true);
            },
            success: function (res){
                $(".cart-list-ajax").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartListAjax").html(res.data);

            }
        });
    })

    // update item quantity from cart

    $(document).on('click', '.update-item-ajax', function (){
        var _pId = $(this).attr('data-item'); // all are behind the delete button in the list_cart_ajax.html
        var _pqty = $('.product-qty-'+_pId).val();
        var _vm = $(this);
        $.ajax({
            url: '/update-from-cart-ajax',
            data: {
                'id': _pId,
                'qty': _pqty
            },
            dataType: 'json',
            beforeSend: function (){
                _vm.attr('disabled', true);
            },
            success: function (res){
                // $(".cart-list-ajax").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartListAjax").html(res.data);

            }
        });
    });
});