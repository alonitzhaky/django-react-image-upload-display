import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
    const MYSERVER ="http://127.0.0.1:8000/upload_image/"
  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleImageUpload = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', image);
    formData.append('title', "waga");
    formData.append('description', "baga");
    formData.append('completed', true);

    try {
      const res = await axios.post(MYSERVER, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setImageUrl(res.data.imageUrl);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <form onSubmit={handleImageUpload}>
        <input type="file" onChange={handleImageChange} />
        <button type="submit">Upload Image</button>
      </form>
      
      {imageUrl && <img src={imageUrl} alt="Uploaded Image" />}
    </div>
  );
};

export default ImageUpload;
