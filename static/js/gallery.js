document.addEventListener('DOMContentLoaded', function () {
  if (typeof Swiper === 'undefined') return; // fail-safe if CDN fails

  new Swiper('.mySwiper', {
    loop: true,
    autoHeight: true,
    spaceBetween: 16,
    slidesPerView: 1,
    breakpoints: {
      768: { slidesPerView: 2 },
      992: { slidesPerView: 3 }
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    }
  });
});
