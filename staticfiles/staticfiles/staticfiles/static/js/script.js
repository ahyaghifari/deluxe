$(document).ready(function () {
    
    // AOS
     AOS.init();

    //DARK MODE
    $('.theme-toggle').click(function () {
        $.ajax({
            type: "GET",
            url: "/changetheme/",
            dataType: "json",
            success: function (response) {
                if($('html').hasClass('dark')){
                    $('.theme-toggle').removeAttr('checked')
                    $('html').removeClass('dark')
                } else {
                    $('.theme-toggle').attr('checked', 'checked')
                    $('html').addClass('dark')
                }
            }
        });
    });
    
    // CONVERT TO IDR
     let IDR = new Intl.NumberFormat("id-ID", {
            style: 'currency',
            currency: 'IDR'
        })

    if ($('.prices').length) {
        $('.prices').each(function () {
            getprices = parseFloat($(this).html().toString())
            $(this).html(IDR.format(getprices))
            
        })
    }

    // TRIX
    //news
    $('textarea#id_body').focus()
    $('textarea#id_body').tinymce({
        height: 500,
        menubar: 'edit insert format view',
        // inline: true,
        // theme: 'silver',
        plugins: [
          'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
          'anchor', 'searchreplace', 'visualblocks', 'fullscreen',
          'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
        ],
    })

    $('textarea#about-text').tinymce({
        height: 300,
        menubar: false,
    })
    
    //NAV
    $('.menu-toggle').click(function () {
        $('nav').toggleClass('nav-anim');
    });

        
    // ------------------------ ALL  CRUD --------------------------------

    // ------------------------ CART -------------------------------------
    const cartcount = async () => {
        $.ajax({
            type: "GET",
            url: "/cart/count/",
            dataType: "json",
            success: function (response) {
                $('#cart-count').html(response.count)
            }
        });
    }

    if($('#cart-count').length){
        cartcount()
    }


    const allcarttotal = async () => {
            var p = []
            var total = 0
            $('.total-carts-menu').each(function (i, obj) {
                gettext = parseFloat(obj.innerHTML.slice(8).replace(".", ""))
                p.push(gettext)
            })
            p.forEach(element => {
            total += element
            });

            $('#all-total-cart').html(IDR.format(total.toFixed(2)).toString())
    }

    allcarttotal()
    
    $('.btn-add-cart').click(function () {
        var slug = $(this).attr('id')
        var name = $(this).attr('data-name')

        $.ajax({
            type: "POST",
            url: "/cart/add/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                slug : slug
            },
            dataType: "json",
            success: function (response) {
                if (response.confirm == '200') {
                    Swal.fire({
                        customClass: {
                        container: 'swal-cont',
                        popup: 'swal-popup'
                        },  
                        showClass: {
                            popup: 'animate__animated animate__fadeInDown animate__faster'
                        },
                        position: 'top',
                        color: '#84563C',
                        showConfirmButton: false,
                        background: '#EDE6D6',
                        backdrop: false,
                        html: `<span class="font-bold">${name}</span> success to cart`,
                        timer: 1500,
                        customClass: {
                            container: 'cart-swal-custom',
                            popup: 'cart-swal-popup',
                        }
                    })
                    cartcount()
                } else {
                    Swal.fire({
                        customClass: {
                        container: 'swal-cont',
                        popup: 'swal-popup'
                        },
                        showClass: {
                            popup: 'animate__animated animate__fadeInDown animate__faster'
                        },
                        position: 'top',
                        color: '#84563C',
                        showConfirmButton: false,
                        background: '#EDE6D6',
                        backdrop: false,
                        html: `<span class="font-bold">${name} </span> failed add to cart`,
                        timer: 1500
                    })
                }
            }
        });

    });

    $('.qty-btn').on('click', function () {
        var value = parseInt($(this).siblings('.qty-cart').val())
        if ($(this).hasClass('plus')) {
           $(this).prev()[0].stepUp()
        } else {
            $(this).next()[0].stepDown()
        }
        $(this).siblings('.qty-cart').trigger('change')
    });

    $('.qty-cart').on('change', function () {
        // console.log("a")
            var slug = $(this).attr('id')
            var getprice = parseFloat($(this).attr('data-price'))
            var price = getprice.toFixed(2)
            var qty = $(this).val()

            $('#total-menu-' + slug).html(IDR.format(parseFloat(price * qty)))
            $.ajax({
                type: "POST",
                url: "/cart/qty/",
                data: {
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    slug: slug,
                    qty: qty
                },
                dataType: "json",
                success: function (response) {
                    if (response.confirm = '200') {
                        allcarttotal()
                    }        
                }
            });
    });

    $('.btn-delete-menu-cart').on('click', function () {
        var slug = $(this).attr('id');
        $(this).attr('disabled', '')
            $.ajax({
                type: "POST",
                url: "/cart/deletemenu/",
                data: {
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    slug : slug
                },
                dataType: "json",
                success: function (response) {
                    if (response.confirm == '200') {
                        if (response.count > 0) {
                            $('#carts-' + slug).fadeOut("slow", () => {
                                cartcount()
                                $('#carts-'+slug).remove() 
                                allcarttotal()
                            });
                        } else {   
                            location.reload()
                        }
                    }
                }
            });
    })
    
    $('#delete-cart-btn').on('click', function (e) {
        e.preventDefault()
        let form = $('#form-cart-delete')
         Swal.fire({
            html: `<span>Are you sure?</span>`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#EDE6D6',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton:'delete-menu-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
                form.submit()
            } else {
                return false;
            }
        })
    })

    //-------------------------CHECKOUT------------------------------------
    $('.checkout-change').on('click', function () {
        var form = $(this).siblings('#receiver-address-form')
        form.toggleClass('active')
    })

    $('.checkout-inputs').on('keyup', function () {
        var id = $(this).attr('id'); 
        $('#text-'+id).html($(this).val())
    });

    const checkoutalltotal = async () => {
        a = []
        total = 0
        $('.subtotals').each(function (i, obj) {
            getsubtotals = parseFloat(obj.innerHTML.slice(8).replace(".", ""))
            a.push(getsubtotals)
        })
        a.forEach(element => {
            total += element
        });
        // console.log(parseFloat(total).toFixed(2))
        $('#checkoutalltotal').html(IDR.format(total.toFixed(2)).toString())
        $('#alltotalpayment').val(total.toFixed(2))
    }
    checkoutalltotal()

    $('#payment-method').on('change', function () {
        var slug = $(this).val()
        $.ajax({
            type: "GET",
            url: "/order/payment-method",
            data: {
                slug : slug
            },
            dataType: "json",
            success: function (response) {
                if (response.confirm = '200') {
                    getfee = parseFloat(response.fee)
                    $('.handling-fee').html(IDR.format(getfee.toFixed()).toString())
                    checkoutalltotal()
                }
            }  
        });
    })
        
    // ------------------------ MENU -------------------------------------
    $('.menu-forms #id_name').on('change', function () {
        var val = $(this).val()

        var context = $('#btn-form-menu').attr('data-context')
        var data = {}

        if (context == "Create") {
            data = {
                val : val
            }
        } else if (context == "Update") {
            slug = $('#menu').val()
            data = {
                val: val,
                slug: slug,
            }
        }

        $.ajax({
            type: "GET",
            url: "/menu/checkslug/",
            data: data,
            dataType: "json",
            success: function (response) {
                if (response.confirm == '200') {
                    $('#btn-form-menu').removeAttr('disabled')
                    $('#id_slug').removeAttr('disabled')
                    $('#id_slug').val(response.slug)
                    $('#slug-menu-confirmation').remove()
                    $('#id_slug').before(`<p  id="slug-menu-confirmation" class="text-[12px] text-green-800">${response.slug} is available</p>`)
                } else {
                    $('#btn-form-menu').attr('disabled', 'disabled')
                    $('#id_slug').attr('disabled', 'disabled')
                    $('#id_slug').val(response.slug)
                    $('#slug-menu-confirmation').remove()
                    $('#id_slug').before(`<p id="slug-menu-confirmation" class="text-[12px] text-red-800">${response.slug} is not available</p>`)
                 }
                // console.log(response)
            }
        });
    });

    $('#delete-menu-btn').on('click',function (e) {
        e.preventDefault()
        var name = $('.btn-delete-menu').attr('id');
        let form = $('#form-delete-menu')

        Swal.fire({
            html: `<span>Are you sure?</span>`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#EDE6D6',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton:'delete-menu-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
                form.submit()
            } else {
                return false;
            }
        })

    });

    $('#delete-menu-rate').on('click', function (e) {
        e.preventDefault()

        let form = $('#form-delete-rate')

        Swal.fire({
            html: `<span>Are you sure?</span>`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#EDE6D6',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton:'delete-menu-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
                form.submit()
            } else {
                return false;
            }
        })
    })


    //COMMENT
    var commentform = $('.comment-accordion-form').hide()
    $('.comment-accordion-btn').on('click', function () {
        $('#menu-comment-comment').val('')
        commentform.toggle(300)
        $(this).toggleClass('rotate-45')
        $('.comment-accordion-form').attr('action', '/menu/comment/')
        $('.comment-accordion-form #idcomment').remove()
        $('.comment-accordion-form button').html('Post')
    });
    $('.comment-edit-btn').on('click', function () {
        var id = $(this).attr('id')
        $('.comment-accordion-btn').toggleClass('rotate-45')
        $.ajax({
            type: "GET",
            url: "/menu/comment/edit/",
            data: {
                id: id
            },
            dataType: "json",
            success: function (response) {
                if (response.confirm == '200') {
                    $('#menu-comment-comment').val(response.comment)
                    commentform.show(200)
                    $('.comment-accordion-form').attr('action', '/menu/comment/update/')
                    $('.comment-accordion-form #idcomment').remove()
                    $('.comment-accordion-form').append(`<input type="hidden" id="idcomment" name="id" value=${id} />`)
                    $('.comment-accordion-form button').html('Update')
                }
            }
        });
    });
    $('.comment-delete-btn').on('click', function () {
        var id = $(this).attr('id')
        var next = $(this).attr('data-next')
        Swal.fire({
            html: `<span>Are you sure to delete this comment ?`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#fafafa',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton: 'delete-comment-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "POST",
                    url: "/menu/comment/delete/",
                    data: {
                        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                        id: id,
                        next: next
                        
                    },
                    dataType: "json",
                    success: function (response) {
                        if (response.confirm == "200") {
                            location.reload()
                        }
                    }
                });
            } else {
                return false;
            }
        })
    });

    // ------------------------ ORDER --------------------------------------
    $('#order-menu-container .menus').each(function (i, obj) {
        $(this).siblings('.menus').remove()
    });
    $('#order-cancel-btn').on('click', function (e) {
        e.preventDefault()
        let form = $('#form-order-cancel')
        
        Swal.fire({
            html: `<span>Are you sure to cancel this order ?`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#fafafa',
            confirmButtonColor: '#b91c1c',
            cancelButtonColor: '#7C3C21',

        }).then((result) => {
            if (result.isConfirmed) {
                form.submit()
            } else {
                return false;
            }
        })
    });

    $('.order-status-select').on('change', function () {
        // $(this).siblings('button').removeAttr('disabled')
        if ($(this).val() == $(this).attr('data-status')) {
            $(this).siblings('button').attr('disabled', 'disabled')
        } else {
            $(this).siblings('button').removeAttr('disabled')
        }
    });


    // ------------------------ NEWS --------------------------------------
    $('#delete-news-btn').on('click', function (e) {
        e.preventDefault()
        let form = $('#form-delete-news')

        Swal.fire({
            html: `<span>You sure to delete this news?`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#EDE6D6',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton:'delete-news-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
              form.submit()
            } else {
                return false;
            }
        })



        
    })


    // ------------------------ SUBSCRIBE --------------------------------------
    $('#newsletter-form').on('submit', function (e) {
        e.preventDefault()
        var email = $('#newsletter-email').val()
        $.ajax({
            type: "POST",
            url: "/contact/subscribe/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                email : email
            },
            dataType: "json",
            success: function (response) {
                $('#newsletter-email').val('')
                $('#newsletter-confirm').removeClass('p-1')
                $('#newsletter-confirm').removeClass('bg-red-600')
                $('#newsletter-confirm').removeClass('bg-green-600')
                
                $('#newsletter-confirm').addClass('p-1')
                if (response.confirm == "200") {
                    $('#newsletter-confirm').addClass('bg-green-600')
                } else if (response.confirm == "400") {
                    $('#newsletter-confirm').addClass('bg-red-600')
                } 
                $('#newsletter-confirm').html(response.message)
            }
        });
    });

    $('#delete-subscriber-btn').on('click', function (e) {
        e.preventDefault()
        let form = $('#form-subscriber-delete')
         Swal.fire({
            html: `<span>Are you sure?</span>`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#EDE6D6',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton:'delete-menu-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
                form.submit()
            } else {
                return false;
            }
        })
    })


    // USERS
    $('#delete-account-btn').on('click', function (e) {
        e.preventDefault()
        let form = $("#form-delete-account")

        Swal.fire({
            html: `<span>Are you sure to delete your account ?`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#fafafa',
            confirmButtonColor: '#b91c1c',
            cancelButtonColor: '#7C3C21',

        }).then((result) => {
            if (result.isConfirmed) {
                form.submit()
            } else {
                return false;
            }
        })

    })


    //ADDRESS 
    $('#delete-address-btn').on('click', function (e) {
        e.preventDefault()
        let form = $('#form-delete-address')

        Swal.fire({
            html: `<span>You sure to delete this address?`,
            showCancelButton: true,
            color: '#7C3C21',
            backdrop: true,
            reverseButtons: true,
            background: '#EDE6D6',
            cancelButtonColor: '#7C3C21',
            customClass: {
                confirmButton:'delete-news-swal',
            }

        }).then((result) => {
            if (result.isConfirmed) {
              form.submit()
            } else {
                return false;
            }
        })
    });

    // ------------------------------DASHBOARD------------------------------
    $('.dashboard-sidebar-toggle').on('click', function () {
        $('#dashboard-sidebar').toggleClass('show')
    })


    //ACCORDION
    $('.accordion-btn').on('click', function () {
        $(this).siblings('.accordion-content').toggleClass('active');
    })


    //ANIMATIONS with GSAP
    if ($('#home').length) {   
        //DELUXE
        gsap.from('#deluxe', {
            duration: 2,
            text: {
                value: ""
            },
            ease: "power2"
        });

        gsap.from('#welcome img', {
            duration: 1,
            rotate: 45,
            opacity: 0,
            x : 300
        });
    }
    //Animation
    var tl = gsap.timeline()
    if ($('#menu-detail').length){ 
        tl.from('#menu-image-detail', {
            width: 0,
            opacity: 0,
            transformOrigin: "left",
            duration: 0.5
        })
        tl.from('#menu-detail-name', {
            duration: 0.5,
            text: {
                value : ""
            }
        })
        tl.from('#menu-detail-stars', {
            transformOrigin: "left",
            width: 0.3,
            duration: 0.3
        })
        tl.from('#menu-detail-desription', {
            duration: 0.3,
            height: 0
        })
    }

    //IMAGE PREVIEW
    if ($('form').length) {
        var image = $('#id_image').val();
        if (image != "") {
            $('#image-preview > img').attr('src', image)
        }
    }
    
    $('#id_image').on('change', function () {
        var image = $(this).val()
        $('#image-preview > img').attr('src', image)
    })

    //MESSAGES
    $('.messages-close-btn').on('click', function () {
       $('#messages').remove() 
    });

     

});