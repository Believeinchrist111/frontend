'use client'

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import Link from 'next/link';

import "./sign-in.css";


export default function SignUpOrIn() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setloading] = useState(false)

  const navigate = useRouter()

  const validateForm = () => {
    if (!username || !password) {
      setError('Username and password are required')
      return false;
    }
    setError('')
    return true;
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setloading(true);

    const formDetails = new URLSearchParams();
    formDetails.append('username', username)
    formDetails.append('password', password)

    try {
      const response = await fetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formDetails,
      });

      setloading(false);

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token)
        console.log(data.access_token)
        navigate.push('../');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Authentication failed!');
      }
    } catch (error) {
      setloading(false);
      setError('An error occured. Please try again later.');  
    }
  }



  return (
    <>
      <form onSubmit={handleSubmit}>
        <div id="signin-card">
          <h1>Sign in to Believe</h1>
          <input type="text" placeholder="Sign up with Google" />
          <input type="text" placeholder="Sign up with Apple" />
          <div className="divider"><div /> OR <div /></div>

          <input
            className='login-input'
            type='text'
            placeholder='Phone, email address, or username'
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            className='login-input'
            type='password'
            placeholder='Password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className='submit' type='submit' disabled={loading}>{loading ? 'logging in...' : 'Log in'}</button>

          <p className="dont-para">Don't have an account?<Link href='../sign-up'> Sign-up</Link></p>
        </div>
      </form>
    </>
  );
}   