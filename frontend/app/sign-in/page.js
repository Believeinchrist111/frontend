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

  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   if (!username || !password) {
  //     setError("Username and password are required");
  //     return;
  //   }

  //   setLoading(true);
  //   try {
  //     const response = await fetch("http://127.0.0.1:8000/sign-in", {
  //       method: "POST",
  //       headers: { "Content-Type": "application/x-www-form-urlencoded" },
  //       body: new URLSearchParams({ username, password }),
  //     });

  //     setLoading(false);

  //     if (response.ok) {
  //       const data = await response.json();
  //       console.log(data)
  //       Cookies.set("token", data.access_token,);
  //       router.push("/"); // middleware allows now since there is a token
  //     } else {
  //       const errorData = await response.json();
  //       setError(errorData.detail || "Authentication failed!");
  //     }
  //   } catch {
  //     setLoading(false);
  //     setError("An error occurred. Please try again.");
  //   }
  // };

  async function handleSubmit(e) {
    e.preventDefault();
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
        const data = await res.json();
        alert(data.detail || "Login failed");
      }
    } catch (error) {
      console.error(error);
      alert("Something went wrong");
    } finally {
      setLoading(false);
    }
  }


  return (

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
  );
}
