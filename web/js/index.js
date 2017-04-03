;
$(document).ready(function() {
    var $select_collection = $('#select-collection')
    var $select_list = $('#select-list')
    var $select_dataset = $('#select-dataset')
    var $select_category = $('#select-category')
    var $select_binary_file = $('#select-binary-file')
    var $start_number = $("#start-number")
    var $end_number = $("#end-number")
    var $image_res = $('#image-res')
    var $search_btn = $('#search-btn')
    var $error = $('#error')
    var $prob_list = $('#prob-list')
    var $full_image = $('#full-image')
    var $pagination = $('.pagination')

    var list_image_data = null
    var number_of_image_per_page = 100

    // init select 2
    var init = function() {
        $select_list.empty().select2({
            placeholder: "Select a list",
            disabled: true
        })

        $select_dataset.empty().select2({
            placeholder: "Select a dataset",
            disabled: true
        })

        $select_category.empty().select2({
            placeholder: "Select a category",
            disabled: true
        })

        $select_binary_file.empty().select2({
            placeholder: "Select a binary file",
            disabled: true
        })
    }

    init()

    var init_select_list = function(data) {
        $select_list.empty().select2({
            placeholder: "Select a list",
            data: data,
            disabled: false
        })
    }

    var init_select_category = function(data) {
        $select_category.empty().select2({
            placeholder: "Select a category",
            disabled: false,
            data: data
        })
    }

    var init_select_binary_file = function(data) {
        $select_binary_file.empty().select2({
            placeholder: "Select a binary file",
            disabled: false,
            data: data
        })
    }

    var init_select_dataset = function(data) {
        $select_dataset.empty().select2({
            placeholder: "Select a dataset",
            data: data,
            disabled: false
        }).on("change", function(e) {
            var dataset = $select_dataset.val()
            var collection = $select_collection.val()
            $.ajax({
                url: "middleman.php",
                type: "POST",
                data: {
                    type: 0,
                    func: 3,
                    params: collection + ',' + dataset
                },
                success: function(data) {
                    data = JSON.parse(data)
                    init_select_category(data)
                }
            })

            $.ajax({
                url: "middleman.php",
                type: "POST",
                data: {
                    type: 0,
                    func: 4,
                    params: collection + ',' + dataset
                },
                success: function(data) {
                    data = JSON.parse(data)
                    init_select_binary_file(data)
                }
            })
        })
    }

    var init_select_collection = function(data) {
        $select_collection.select2({
            placeholder: "Select a collection",
            data: data
        }).on("change", function(e) {
            init()
            var collection = $select_collection.val()
            $.ajax({
                url: "middleman.php",
                type: "POST",
                data: {
                    type: 0,
                    func: 1,
                    params: collection
                },
                success: function(data) {
                    data = JSON.parse(data)
                    init_select_list(data)
                }
            })

            $.ajax({
                url: "middleman.php",
                type: "POST",
                data: {
                    type: 0,
                    func: 2,
                    params: collection
                },
                success: function(data) {
                    data = JSON.parse(data)
                    init_select_dataset(data)
                }
            })
        })
    }

    var generate_image_html_string = function(image, collection) {
        var root_path = window.location.href.toString().split(window.location.host.toString())[1].replace('/web/index.html', '')

        res = '<div class="col-sm-2 col-lg-2 col-md-2">' +
            '<div class="thumbnail">' +
            '<a href="#" data-toggle="modal" data-target="#detail">' +
            '<span class="hidden">' + image.id + '</span>' +
            '<img class="lazy" data-original="' + root_path + '/collections/' + collection + '/JPG/images/' + image.name + '" alt="">' +
            '</a>' +
            '<div class="caption">' +
            '<meter style="100px" max="1" low="0" high="0.75" optimum="0.9" value="' + (parseFloat(image.prob).toFixed(4)) + '"></meter>' +
            '<span> ' + (parseFloat(image.prob).toFixed(4)) + '</span>' +
            '</div></div></div>'
        return res
    }

    var set_click_event_each_image = function(collection, dataset, binaryfile) {
        $image_res.find("a").each(function() {
            $(this).on("click", function(event) {
                event.preventDefault()
                image_position = $(this).find("span").text()
                image_src = $(this).find("img")[0].getAttribute('src')
                $full_image.attr('src', image_src);
                $.ajax({
                    url: "middleman.php",
                    type: "POST",
                    data: {
                        type: 3,
                        params: collection + ',' + dataset + ',' + binaryfile + ',' + image_position
                    },
                    success: function(data) {
                        data = JSON.parse(data)
                        html_string = ''
                        for (var i = 0, len = data.length; i < len; i++) {
                            html_string += '<tr><td class="col-xs-8">' + data[i].name + '</td>'
                            html_string += '<td class="col-xs-4">' + (parseFloat(data[i].prob).toFixed(4)) + '</td></tr>'
                        }
                        $prob_list.empty().append(html_string)
                    },
                });
            })
        })
    }

    var paging_image_list = function(page, number_of_image, collection, dataset, binaryfile){
        $image_res.empty()
            // generate images elements
        var html_string = ''
        var start = (page - 1)*number_of_image_per_page
        var end = Math.min(page*number_of_image_per_page, number_of_image)
        for (var i = start; i < end; i++) {
            html_string += generate_image_html_string(list_image_data[i], collection)
        }
        $image_res.append(html_string)
        $("img.lazy").lazyload({
            threshold: 200
        });
        set_click_event_each_image(collection, dataset, binaryfile)
    }

    $search_btn.on("click", function(e) {

        var error_html_string = ''

        var collection = $select_collection.val()
        if (collection == '') {
            error_html_string += '<li>' + 'Collection must be selected!' + '</li>'
        }
        var u_list = $select_list.val()
        if (u_list == '') {
            error_html_string += '<li>' + 'List must be selected!' + '</li>'
        }
        var dataset = $select_dataset.val()
        if (dataset == '') {
            error_html_string += '<li>' + 'Dataset must be selected!' + '</li>'
        }
        var category = $select_category.val()
        if (category == '') {
            error_html_string += '<li>' + 'Category must be selected!' + '</li>'
        }
        var binaryfile = $select_binary_file.val()
        if (binaryfile == '') {
            error_html_string += '<li>' + 'Binary file must be selected!' + '</li>'
        }

        if (error_html_string != '') {
            $error.empty().append(error_html_string)
            $error.parent().removeClass("hidden")
            return
        }

        $error.parent().addClass("hidden")

        var url = '/search?' + 'collection=' + collection + '&list=' + u_list + '&dataset=' + dataset + '&category=' + category + '&binaryfile=' + binaryfile

        $.ajax({
            url: "middleman.php",
            type: "POST",
            data: {
                type: 1,
                params: collection + ',' + u_list + ',' + dataset + ',' + category + ',' + binaryfile
            },
            success: function(data) {
                list_image_data = JSON.parse(data)
                number_of_image = list_image_data.length
                surplus = number_of_image % number_of_image_per_page
                if (surplus == 0) {
                    max_page_number = (number_of_image - surplus)/number_of_image_per_page
                } else {
                    max_page_number = (number_of_image - surplus)/number_of_image_per_page + 1
                }

                paging_image_list(1, number_of_image, collection, dataset, binaryfile)

                $pagination.removeClass('hidden')
                $pagination.jqPagination({
                    max_page: max_page_number,
                    paged: function(page){
                        paging_image_list(page, number_of_image, collection, dataset, binaryfile)
                    }
                })
            },
        });
    })



    $.ajax({
        url: "middleman.php",
        type: "POST",
        data: {
            type: 0,
            func: 0,
            params: ''
        },
        success: function(data) {
            data = JSON.parse(data)
            var temp = []
            for (var i = 0; i < data.length; i++) {
                temp.push({ id: data[i], text: data[i] })
            }
            init_select_collection(temp)
        },
    });



});
