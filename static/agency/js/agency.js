(() => {
  const navbar = document.querySelector('#mainNav');
  if (!navbar) {
    return;
  }

  const handleNavbarShrink = () => {
    if (window.scrollY > 80) {
      navbar.classList.add('navbar-shrink');
    } else {
      navbar.classList.remove('navbar-shrink');
    }
  };

  handleNavbarShrink();
  document.addEventListener('scroll', handleNavbarShrink);
})();
