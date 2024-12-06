document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');

    if (searchInput) {
        searchInput.addEventListener('keydown', function(event) {
            console.log("Key pressed:", event.key);  // Debug: tuşun adı console'a yazdırılacak
            if (event.key === 'Enter') {
                event.preventDefault();  // Formun submit olmasını engeller
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

    console.log("Redirecting to:", url);  // Debug: yönlendirme yapılacak URL'yi console'a yazdır
    window.location.href = url; // URL'yi güncelleyerek arama sonuçlarını göster
}