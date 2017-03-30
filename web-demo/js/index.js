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

    // init select 2
    var init = function() {
        $select_list.empty().append("<option></option>").select2({
            placeholder: "Select a list",
            disabled: true
        })

        $select_dataset.empty().append("<option></option>").select2({
            placeholder: "Select a dataset",
            disabled: true
        })

        $select_category.empty().append("<option></option>").select2({
            placeholder: "Select a category",
            disabled: true
        })

        $select_binary_file.empty().append("<option></option>").select2({
            placeholder: "Select a binary file",
            disabled: true
        })
    }

    init()

    var init_select_list = function(data) {
        $select_list.empty().append("<option></option>").select2({
            placeholder: "Select a list",
            data: data,
            disabled: false
        })
    }

    var init_select_category = function(data) {
        $select_category.empty().append("<option></option>").select2({
            placeholder: "Select a category",
            disabled: false,
            data: data
        })
    }

    var init_select_binary_file = function(data) {
        $select_binary_file.empty().append("<option></option>").select2({
            placeholder: "Select a binary file",
            disabled: false,
            data: data
        })
    }

    var init_select_dataset = function(data) {
        $select_dataset.empty().append("<option></option>").select2({
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
        var root_path = window.location.href.toString().split(window.location.host.toString())[1].replace('/web-demo/index.html','')

        res = '<div class="col-sm-2 col-lg-2 col-md-2">' +
            '<div class="thumbnail">' +
            '<img class="lazy" data-original="'+root_path+'/collections/' + collection + '/JPG/images/' + image.name + '" alt="">' +
            '<div class="caption">' +
            '<meter style="100px" max="1" low="0" high="0.75" optimum="0.9" value="' + (parseFloat(image.prob).toFixed(4)) + '"></meter>' +
            '<span> ' + (parseFloat(image.prob).toFixed(4)) + '</span>' +
            '</div>' +
            '</div>' +
            '</div>'
        return res
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
                params: collection +','+ u_list +','+ dataset +','+ category +','+binaryfile
            },
            success: function(data) {
                data = JSON.parse(data)
                $image_res.empty()
                // generate images elements
                var html_string = ''
                for (var i = 0, len = data.length; i < len; i++) {
                    html_string += generate_image_html_string(data[i], collection)
                }
                $image_res.append(html_string)
                $("img.lazy").lazyload({
                    threshold: 200
                });
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
