// Price ticker infinite scroll
document.addEventListener('DOMContentLoaded', function() {
    const content = document.querySelector('.price-ticker .ticker-content');
    if (content) {
        const items = content.innerHTML;
        // Double the content for smooth infinite scroll
        content.innerHTML = items + items;
    }
});
