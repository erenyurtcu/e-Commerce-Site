document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('keydown', function(event) {
            console.log("Key pressed:", event.key);
            if (event.key === 'Enter') {
                event.preventDefault();
                searchProducts();
            }
        });
    }
});
function searchProducts() {
    const query = document.getElementById('search').value;
    const category = document.getElementById('category').value;

    let url = window.location.pathname + '?search=' + encodeURIComponent(query);
    if (category) {
        url += '&category=' + encodeURIComponent(category);
    }
    console.log("Redirecting to:", url);
    window.location.href = url;
}


function smoothScrollToTop(triggerId) {
    const triggerElement = document.getElementById(triggerId);
    if (triggerElement) {
        triggerElement.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // Smooth scroll effect
            });
        });
    }
}
