;
$(document).ready(function() {
    var $select_collection = $('#select-collection')
    var $select_list = $('#select-list')
    var $select_category = $('#select-category')
    var $select_binary_file = $('#select-binary-file')

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

    var init_select_collection = function(data) {
        $select_collection.select2({
            placeholder: "Select a collection",
            data: data
        }).on("change", function(e) {
            var collection = $select_collection.val()
            $.ajax({
                url: "/list?collection=" + collection,
                type: "GET",
                success: function(data) {
                    data = JSON.parse(data)
                    var temp = []
                    for (var i = 0; i < data.length; i++) {
                        temp.push({ id: data[i], text: data[i] })
                    }
                    init_select_list(temp)
                }
            })

            $.ajax({
                url: "/categories?collection=" + collection,
                type: "GET",
                success: function(data) {
                    data = JSON.parse(data)
                    init_select_category(data)
                }
            })

            $.ajax({
                url: "/binaryfile?collection=" + collection,
                type: "GET",
                success: function(data) {
                    data = JSON.parse(data)
                    init_select_binary_file(data)
                }
            })

        })
    }

    $.ajax({
        url: "/collections",
        type: "GET",
        success: function(data) {
            data = JSON.parse(data)
            var temp = []
            for (var i = 0; i < data.length; i++) {
                temp.push({ id: data[i], text: data[i] })
            }

            init_select_collection(temp)

            $select_category.select2({
                placeholder: "Select a category",
                disabled: true
            })

            $select_list.select2({
                placeholder: "Select a list",
                disabled: true
            })

            $select_binary_file.select2({
                placeholder: "Select a binary file",
                disabled: true
            })
        },
    });



    // console.log($select_collection)
})
