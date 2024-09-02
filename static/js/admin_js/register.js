$(document).ready(function() {
    $('#countrycode').select2({
        placeholder: "Select a country",
        ajax: {
            url: '/admins/search-country',  // URL to your search view
            dataType: 'json',
            delay: 250,  // Delay for debounce
            data: function (params) {
                return {
                    search: params.term  // Pass the search term to the server
                };
            },
            processResults: function (data) {
                return {
                    results: $.map(data.results, function(country) {
                        return {
                            id: country.country,  // Unique ID for each country
                            text: country.country,  // Text to display in the dropdown
                        }
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 1  // Start searching after one character input
    });
});
