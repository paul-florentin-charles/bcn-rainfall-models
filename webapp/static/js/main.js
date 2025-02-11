/** Load Plotly charts **/

const config = {
    responsive: true,
    scrollZoom: true,
};

const graph_div_id_to_graph_json = {
    chart_summer_rainfall: graphs_summer_rainfall,
    chart_averages: graphs_averages,
    chart_linreg: graphs_linreg,
    chart_relative_distance_to_normal: graphs_relative_distance_to_normal,
};

['load', 'resize'].forEach(event => window.addEventListener(event, function () {
    if (window.screen.width < 768) {
        Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
            graph_json.layout.font.size = 9;
        })
    } else {
        Object.values(graph_div_id_to_graph_json).forEach((graph_json) => {
            graph_json.layout.font.size = 11;
        })
    }

    Object.entries(graph_div_id_to_graph_json).forEach(([graph_div_id, graph_json]) => {
        Plotly.newPlot(graph_div_id, graph_json, {}, config);
    })
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