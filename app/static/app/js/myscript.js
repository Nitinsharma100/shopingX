$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
});

// Add to Cart Functionality
$('.plus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    $.ajax({
        type: 'GET',
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
        },
        error: function(error) {
            console.log("Error:", error);
        }
    });
});

// Minus from Cart Functionality
$('.minus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    $.ajax({
        type: 'GET',
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
        },
        error: function(error) {
            console.log("Error:", error);
        }
    });
});

// Remove from Cart Functionality
$('.remove-cart').click(function(e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString();
    var eml = $(this); 

    $.ajax({
        type: 'GET',
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("Data received:", data); // Debug statement
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;

            // Check if the closest cart-item exists before removing
            var cartItem = eml.closest('.cart-item');
            if (cartItem.length) {
                cartItem.remove();
            } else {
                console.error("No cart item found");
            }

            if (data.amount === 0) {
                window.location.href = ''; 
            }
        },
        error: function(error) {
            console.log("Error:", error);
        }
    });
});
