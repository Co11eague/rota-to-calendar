document.addEventListener('DOMContentLoaded', function () {
    const option = document.getElementById("sorting")
    const searchField = document.getElementById("searchField")


    const urlParams = new URLSearchParams(window.location.search)
    const sortValue = urlParams.get("sort")
    const searchValue = urlParams.get("search")

    if (sortValue) {
        option.value = sortValue;
    }

    if (searchValue){
        searchField.value = searchValue
    }

})