import React from 'react'
import "./Footer.css";

export default function footer() {
    return (
        <div className="main-footer">
            <div className="container">
                <div className="row" style={{textAlign: "center"}}>
                    <div className="col" style={{display: "inline-block"}}>
                        <h4>Newssy</h4>
                        <ul className=" list-unstyled">
                            <li>+910000000000</li>
                            <li>West Bengal, India</li>
                            <li>newssy@gmail.com</li>
                        </ul>
                    </div>
                    <div className="col" >
                        <ul className=" list-unstyled"></ul>
                        <li>Reactjs</li>
                        <li>flask</li>
                    </div>    
                </div>
                <hr/>
                <div className="row">
                    <p className="col-sm" style={{textAlign: "center"}}>
                        &copy;{new Date().getFullYear()} Newssy | All Rights Reserved
                    </p>
                </div>
                <div className="row">
                <p className="col-sm" style={{textAlign: "center"}}>Made in India With ❤</p>
                </div>
            </div>
        </div>
    )
}
