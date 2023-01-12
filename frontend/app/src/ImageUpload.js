import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState(0);
  const [myToken, setMyToken] = useState('');
  const [imageUrl, setImageUrl] = useState('');
    const MYSERVER ="http://127.0.0.1:8000/upload_image/"
  const handleImageChange = (e) => {
    setImage(e.target.files[0])
  };

  useEffect(() => {
    setMyToken(localStorage.getItem("access_token"))
  }, [])
  
  const handleImageUpload = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', image);
    formData.append('title', title);
    formData.append('description', description);
    formData.append('price', price);

    try {
      const res = await axios.post(MYSERVER, formData, {
        headers: {
          Authorization: `Bearer ${myToken}`,
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
      <hr/>
      <form onSubmit={handleImageUpload}>
        <input type="file" onChange={handleImageChange} /><br/>
        price : <input type={"number"} onChange={(e) => setPrice(e.target.value)}/><br/>
        description: <input type={"text"} onChange={(e) => setDescription(e.target.value)} /><br/>
        title: <input type={"text"} onChange={(e) => setTitle(e.target.value)}/><br/>
        <button type="submit">Upload product</button>
      </form><br/>
      {imageUrl && <img src={imageUrl} alt="Uploaded Image" />}
    </div>
  );
};

export default ImageUpload;
