document.addEventListener("DOMContentLoaded", function () {
    const priceRange = document.getElementById("priceRange");
    const priceValue = document.getElementById("priceValue");

    if (priceRange && priceValue) {
        const updatePrice = () => {
            priceValue.textContent = `$${priceRange.value}`;
        };

        priceRange.addEventListener("input", updatePrice);
        updatePrice();
    }
});