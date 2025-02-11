/** Load Plotly charts **/

const config = {
    responsive: true,
    scrollZoom: true,
};

['load', 'resize'].forEach(event => window.addEventListener(event, function () {
    Plotly.newPlot('chart_summer_rainfall', graphs_summer_rainfall, {}, config);
    Plotly.newPlot('chart_averages', graphs_averages, {}, config);
    Plotly.newPlot('chart_linreg', graphs_linreg, {}, config);
    Plotly.newPlot('chart_relative_distance_to_normal', graphs_relative_distance_to_normal, {}, config);
}))

/** Enable drop-down menus when device is tablet or phone **/

/** Scroll to top button **/

const scrollToTopBtn = document.getElementById('scrollToTop');

const toggleScrollToTopButton = () => {
    if (window.scrollY > 250) {
        scrollToTopBtn.classList.add('visible');
    } else {
        scrollToTopBtn.classList.remove('visible');
    }
};

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

window.addEventListener('scroll', toggleScrollToTopButton);