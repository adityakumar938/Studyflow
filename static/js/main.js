/* StudyFlow — shared behaviour (Member 2). Vanilla JS; Bootstrap bundle loads first. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  // Navbar shadow once the page scrolls
  const nav = document.querySelector(".sf-nav");
  const onScroll = () => nav && nav.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Gentle one-time reveals; skipped for reduced motion / old browsers
  const items = document.querySelectorAll("[data-reveal]");
  if (!items.length) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("revealed"));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("revealed"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    items.forEach((el) => io.observe(el));
  }
})();