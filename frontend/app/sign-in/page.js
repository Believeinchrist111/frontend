"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from 'next/link';

import "./sign-in.css";

export default function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();


  async function handleSubmit(e) {
    e.preventDefault();
    if (!username || !password) {
      setError("Username and password are required");
      return;
    }
    setLoading(true);

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const res = await fetch("/api/sign-in", {
        method: "POST",
        body: formData,
        credentials: "include", // important: store cookie
      });
      if (res.ok) {
        router.push("/"); // Middleware will detect cookie and allow
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Authentication failed!");
      }
    } catch (error) {
      setError("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  }


  return (

    <form onSubmit={handleSubmit}>
      <div id="signin-card">
        <button className="previous-page-button" onClick={() => router.push("/sign-up-in")}>
          <svg viewBox="0 0 24 24" ><g><path d="M10.59 12L4.54 5.96l1.42-1.42L12 10.59l6.04-6.05 1.42 1.42L13.41 12l6.05 6.04-1.42 1.42L12 13.41l-6.04 6.05-1.42-1.42L10.59 12z"></path></g></svg>
        </button>

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
  );
}
