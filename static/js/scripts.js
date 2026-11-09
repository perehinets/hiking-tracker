/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*
* Adapted for the Trailhead hiking tracker: the shrink-on-scroll and scrollspy
* behaviour only applies to the one-page landing, so the app screens (which use
* a permanently solid navbar) are left alone.
*/
//
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

    const mainNav = document.body.querySelector('#mainNav');
    const isSolidNav = mainNav && mainNav.classList.contains('navbar-solid');

    // Navbar shrink function
    var navbarShrink = function () {
        if (!mainNav) {
            return;
        }
        if (window.scrollY === 0) {
            mainNav.classList.remove('navbar-shrink')
        } else {
            mainNav.classList.add('navbar-shrink')
        }

    };

    // Only the transparent landing navbar shrinks on scroll
    if (mainNav && !isSolidNav) {
        navbarShrink();
        document.addEventListener('scroll', navbarShrink);
    }

    // Activate Bootstrap scrollspy on the landing page, which has in-page sections
    if (mainNav && !isSolidNav && document.body.querySelector('.masthead')) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link:not(.dropdown-toggle)')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (navbarToggler && window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});
