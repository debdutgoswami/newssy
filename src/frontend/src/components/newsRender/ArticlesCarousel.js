import React from 'react'

export default function ArticlesCarousel(props) {
    const { details } = props;
    return (
        <div>
            <div id="carouselExampleControls" className="carousel slide" data-ride="carousel">
                <div className="carousel-inner">
                    { details.map(news => (
                    <div class="carousel-item active">
                        <img className="d-block w-50" src={news.urlToImage} alt="First slide" />
                    </div>
                    ))}
                </div>
                    <a className="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
                        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span className="sr-only">Previous</span>
                    </a>
                    <a className="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
                        <span className="carousel-control-next-icon" aria-hidden="true"></span>
                        <span className="sr-only">Next</span>
                    </a>
            </div>
        </div>
    )
}
