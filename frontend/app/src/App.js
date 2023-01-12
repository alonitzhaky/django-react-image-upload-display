import './App.css';
import ImageUpload from './ImageUpload';
import Logger from './Logger';
import MyComponent from './MyComponent';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Logger/>
        <ImageUpload/>
        <MyComponent/> {/* Image Display */}
      </header>
    </div>
  );
}

export default App;
