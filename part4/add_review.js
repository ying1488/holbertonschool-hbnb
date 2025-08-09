document.addEventListener("DOMContentLoaded", () => {
    // Check authentication
    const token = getCookie("jwt");
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    // Get Place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get("place_id");
    if (!placeId) {
        alert("No place specified for review.");
        window.location.href = "index.html";
        return;
    }

    // Handle form submission
    const form = document.getElementById("reviewForm");
    const reviewInput = document.getElementById("reviewText");
    const messageBox = document.getElementById("message");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const reviewText = reviewInput.value.trim();
        if (!reviewText) {
            showMessage("Please enter your review before submitting.", "error");
            return;
        }

        try {
            const response = await fetch("/api/reviews", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    place_id: placeId,
                    review: reviewText
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.message || "Failed to submit review.");
            }

            // Success
            showMessage("Review submitted successfully!", "success");
            reviewInput.value = "";
        } catch (error) {
            showMessage(error.message, "error");
        }
    });

    // Helper functions
    function showMessage(text, type) {
        messageBox.textContent = text;
        messageBox.className = type;
    }

    function getCookie(name) {
        const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
        return match ? match[2] : null;
    }
});
