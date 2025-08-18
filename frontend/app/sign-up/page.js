"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from 'next/link';

import "./sign-up.css"

export default function SignUp() {
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [email, setEmail] = useState("");
  const [dateOfbirth, setDateOfBirth] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();


  async function handleSubmit(e) {
    e.preventDefault();
    if (!firstname || !lastname || !email || !dateOfbirth) {
      setError("All fields are required");
      return;
    }
    setLoading(true);

    const formData = new FormData();
    formData.append("username", username);
    formData.append("lastname", lastname);
    formData.append("email", email);
    formData.append("dateOfbirth", dateOfbirth);

    try {
      const res = await fetch("/api/sign-up", {
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
      <div id="signup-card">
        <button className="previous-page-button" onClick={() => router.push("/sign-up-in")}>
          <svg viewBox="0 0 24 24" ><g><path d="M10.59 12L4.54 5.96l1.42-1.42L12 10.59l6.04-6.05 1.42 1.42L13.41 12l6.05 6.04-1.42 1.42L12 13.41l-6.04 6.05-1.42-1.42L10.59 12z"></path></g></svg>
        </button>

        <h1>Create your account</h1>
        <input
          id='firstname-input'
          type='text'
          placeholder='Firstname'
          value={firstname}
          onChange={(e) => setFirstname(e.target.value)}
        />

        <input
          id='lastname-input'
          type='text'
          placeholder='Lastname'
          value={lastname}
          onChange={(e) => setLastname(e.target.value)}
        />

        <input
          id='email-input'
          type='email'
          placeholder='Email'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          id='dateofbirth-input'
          type='date'
          placeholder='Date of birth'
          value={dateOfbirth}
          onChange={(e) => setDateOfBirth(e.target.value)}
        />



        <button className='next-button'>Next</button>

      </div>
    </form>
  );
}
