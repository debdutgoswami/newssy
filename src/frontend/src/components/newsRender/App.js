import React, { Component } from 'react';
import SelectCat from './SelectCat';

class App extends Component {

  render() {
    return (
      <div>
        <div className="container text-center">
          <SelectCat/>
        </div>
      </div>
    );
  }
}

export default App;
