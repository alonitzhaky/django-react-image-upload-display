import React, { useState } from 'react';
import axios from 'axios';

const Logger = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const loginServer  ="http://127.0.0.1:8000/login/"
  function handleSubmit(event) {
    event.preventDefault();

    axios.post(loginServer, {
      username: username,
      password: password
    })
    .then(response => {
      console.log(response.data)
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      setError(null);
    })
    .catch(error => {
      setError("Invalid username or password.");
    });
  }

  return (
    <div>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </label>
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Logger;