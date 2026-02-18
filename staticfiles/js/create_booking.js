document.addEventListener("DOMContentLoaded", function () {
  const priceData = document.getElementById("booking-price-data");
  const totalPreview = document.getElementById("booking-total-preview");

  // Works even if crispy changes IDs/prefixes
  const checkIn =
    document.querySelector('input[name="check_in"]') ||
    document.querySelector('input[name$="-check_in"]');

  const checkOut =
    document.querySelector('input[name="check_out"]') ||
    document.querySelector('input[name$="-check_out"]');

  const totalInput =
    document.querySelector('input[name="total_price"]') ||
    document.querySelector('input[name$="-total_price"]');

  const pricePerNight = document.getElementById("price-per-night").textContent.replace("£", "").trim();

  function updateTotal() {
    if (!checkIn || !checkOut || !totalPreview) return;

    if (!checkIn.value || !checkOut.value) {
      totalPreview.textContent = "0.00";
      if (totalInput) totalInput.value = "";
      return;
    }

    const nights = Math.floor(
      (new Date(checkOut.value) - new Date(checkIn.value)) / (1000 * 60 * 60 * 24)
    );

    if (nights > 0) {
      const total = nights * pricePerNight;
      totalPreview.textContent = total.toFixed(2);
      if (totalInput) totalInput.value = total.toFixed(2);
    } else {
      totalPreview.textContent = "0.00";
      if (totalInput) totalInput.value = "";
    }
  }

  checkIn?.addEventListener("change", updateTotal);
  checkOut?.addEventListener("change", updateTotal);
  updateTotal();
});