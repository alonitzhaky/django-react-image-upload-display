import React, { useState, useEffect } from 'react';

function MyComponent() {
  const [images, setImages] = useState([]);
  const MYSERVER = "http://127.0.0.1:8000/images/"
  const fetchServer = 'http://127.0.0.1:8000/get_all_images'
  useEffect(() => {
    fetch(fetchServer)
      .then(response => response.json())
      .then(data => setImages(data))
  }, []);

  return (
    <div>
      {images.map((image, i) => (
        <img key={i} src={MYSERVER + image.image} alt={image.description} style={{ width: '350px', height: '150px' }} />
      ))}
    </div>
  );
}

export default MyComponent;
