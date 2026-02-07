document.addEventListener("DOMContentLoaded", function () {

    /* ================= SLIDER ================= */

    const slides = document.querySelectorAll(".slide");
    const nextBtn = document.querySelector(".slider-btn.next");
    const prevBtn = document.querySelector(".slider-btn.prev");

    let currentSlide = 0;
    let sliderInterval;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[index].classList.add("active");
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }

    function startAutoSlide() {
        sliderInterval = setInterval(nextSlide, 7000);
    }

    function resetInterval() {
        clearInterval(sliderInterval);
        startAutoSlide();
    }

    if (slides.length > 0) {
        showSlide(currentSlide);
        startAutoSlide();
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            nextSlide();
            resetInterval();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            prevSlide();
            resetInterval();
        });
    }

    /* ================= NAVBAR SHRINK ====================================================== */

    const navbar = document.querySelector(".navbar");

    if (navbar) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 80) {
                navbar.classList.add("shrink");
            } else {
                navbar.classList.remove("shrink");
            }
        });
    }

});
const slides = document.querySelectorAll(".service-slide");
let index = 0;

document.getElementById("next").addEventListener("click", () => {
    slides[index].classList.remove("active");
    index = (index + 1) % slides.length;
    slides[index].classList.add("active");
});

document.getElementById("prev").addEventListener("click", () => {
    slides[index].classList.remove("active");
    index = (index - 1 + slides.length) % slides.length;
    slides[index].classList.add("active");
});
document.addEventListener("DOMContentLoaded", () => {

    const slides = document.querySelectorAll(".service-slide");
    const nextBtn = document.getElementById("next");
    const prevBtn = document.getElementById("prev");

    let currentIndex = 0;
    let autoSlideInterval;

    // SHOW SLIDE
    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[index].classList.add("active");
    }

    // NEXT
    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    // PREVIOUS
    function prevSlide() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    }

    // AUTO SLIDE (10 sec)
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 10000); // 👈 10 seconds
    }

    // RESET TIMER ON MANUAL CLICK
    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // INIT
    showSlide(currentIndex);
    startAutoSlide();

    // BUTTON EVENTS
    nextBtn.addEventListener("click", () => {
        nextSlide();
        resetAutoSlide();
    });

    prevBtn.addEventListener("click", () => {
        prevSlide();
        resetAutoSlide();
    });

});

