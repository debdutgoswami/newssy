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
                            <li>Kolkata, India</li>
                            <li><a style={{textDecoration: "none", color: "white"}}href="mailto:newssy.app@gmail.com">newssy.app@gmail.com</a></li>
                        </ul>
                    </div>
                    <div className="col" >
                        <h6>Tech Stack</h6>
                        <ul className="list-unstyled">
                        <li >Reactjs</li>
                        <li >Flask</li>
                        <li>GCP</li>
                        <li>Docker</li>
                        </ul>
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
