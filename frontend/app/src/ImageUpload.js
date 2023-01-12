import React, { useState } from 'react';
import axios from 'axios';

function ImageUpload() {
  const [image, setImage] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [uploadedImages, setUploadedImages] = useState([]);
  const MYSERVER ="http://127.0.0.1:8000/"

  const handleImageChange = (e) => {
    e.preventDefault();

    let reader = new FileReader();
    let file = e.target.files[0];

    reader.onloadend = () => {
      setImage(file);
      setImagePreviewUrl(reader.result);
    }

    reader.readAsDataURL(file);
  }

  const handleImageUpload = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', image);
    formData.append('title', "waga");
    formData.append('description', "baga");
    formData.append('completed', true);


    axios.post(MYSERVER + 'upload_image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then((response) => {
      setUploadedImages([...uploadedImages, response.data.imageUrl]);
    })
    .catch((error) => {
      console.log(error);
    });
  }

  return (
    <div>
      <form>
        <input type="file" onChange={handleImageChange} />
        <button onClick={handleImageUpload}>Upload</button>
      </form>
      <div>
        <h2>Gallery</h2>
        {uploadedImages.map((imageUrl, index) => (
          <div key={index}>
            <img src={`http://127.0.0.1:8000/get_images/${imageUrl.image}`} alt="a"></img>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ImageUpload;
