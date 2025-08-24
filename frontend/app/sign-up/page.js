"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
// import Link from 'next/link';

import "./sign-up.css"

export default function SignUp() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);



  // async function handleSubmit(e) {
  //   e.preventDefault();
  //   if (!firstname || !lastname || !email || !dateOfbirth) {
  //     setError("All fields are required");
  //     return;
  //   }
  //   setLoading(true);

  //   const formData = new FormData();
  //   formData.append("username", username);
  //   formData.append("lastname", lastname);
  //   formData.append("email", email);
  //   formData.append("dateOfbirth", dateOfbirth);

  //   try {
  //     const res = await fetch("/api/sign-up", {
  //       method: "POST",
  //       body: formData,
  //       credentials: "include", // important: store cookie
  //     });
  //     if (res.ok) {
  //       router.push("/"); // Middleware will detect cookie and allow
  //     } else {
  //       const errorData = await response.json();
  //       setError(errorData.detail || "Authentication failed!");
  //     }
  //   } catch (error) {
  //     setError("An error occurred. Please try again.");
  //   } finally {
  //     setLoading(false);
  //   }
  // }

  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    firstname: "",
    lastname: "",
    email: "",
    code: "",
    dateOfbirth: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleNext = async (e) => {
    e.preventDefault();

    if (step === 1) {
      // Call /send-code
      const res = await fetch("/api/send-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ firstname: form.firstname, lastname: form.lastname, email: form.email }),
      });

      if (res.ok) {
        alert("A code has been sent to your email (check backend console for demo)");
        setStep(2);
      } else {
        alert("Failed to send verification code");
      }
    } else if (step === 2) {
      // Call /verify-code
      const res = await fetch("/api/verify-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: form.email, code: form.code }),
      });

      if (res.ok) {
        alert("Email has been successfully verified");
        setStep(3);
      } else {
        alert("Invalid verification code");
      }
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        firstname: form.firstname,
        lastname: form.lastname,
        email: form.email,
        date_of_birth: form.dateOfbirth, 
        password: form.password,
      }),
    });

    if (res.ok) {
      alert("User registered successfully!");
      setStep(1);
      setForm({
        name: "",
        email: "",
        code: "",
        password: "",
        confirmPassword: "",
      });
      router.push('/')
    } else {
      const data = await res.json();
      alert(data.detail || "Registration failed");
    }
  };

  return (

    <form className="signup-form" onSubmit={step === 3 ? handleRegister : handleNext}>
      <div id="signup-card">
        {step === 1 ? (
          <button className="previous-page-button" onClick={() => router.push("/sign-up-in")}>
            <svg viewBox="0 0 24 24" ><g><path d="M10.59 12L4.54 5.96l1.42-1.42L12 10.59l6.04-6.05 1.42 1.42L13.41 12l6.05 6.04-1.42 1.42L12 13.41l-6.04 6.05-1.42-1.42L10.59 12z"></path></g></svg>
          </button>) : (
          <button className="previous-page-button" onClick={() => setStep(step - 1)}>
            <svg viewBox="0 0 24 24"><g><path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path></g></svg>
          </button>
        )}


        {step === 1 && (
          <>
            <h1>Create your account</h1>
            <input
              id='firstname-input'
              name="firstname"
              type='text'
              placeholder='Firstname'
              value={form.firstname}
              onChange={handleChange}
              required
            />

            <input
              id='lastname-input'
              name="lastname"
              type='text'
              placeholder='Lastname'
              value={form.lastname}
              onChange={handleChange}
              required
            />

            <input
              id='email-input'
              name="email"
              type='email'
              placeholder='Email'
              value={form.email}
              onChange={handleChange}
              required
            />

            <div id='date-of-birth-label'><b>Date of birth</b><br /><span>This will not be shown publicly. Confirm your own age, even if this account is for a church.</span></div>

            <input
              id='dateofbirth-input'
              type='date'
              placeholder='Date of birth'
              name="dateOfbirth"
              value={form.dateOfbirth}
              onChange={handleChange}
              required
            />
            <button className='next-button'>Next</button>
          </>
        )}

        {step === 2 && (
          <div>
            <h2>We sent you a code.</h2>
            <p className="subtitle">Enter it below to verify {form.email}.</p>
            <input
              type="text"
              name="code"
              placeholder="Verification code"
              value={form.code}
              onChange={handleChange}
              required
            />
            <button className='next-button' type="submit">Next</button>
          </div>
        )}

        {step === 3 && (
          <div>
            <h2>You&apos;ll need a password.</h2>
            <p className="subtitle">Make sure it&apos;s 8 characters or more.</p>

            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              required
            />

            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={form.confirmPassword}
              onChange={handleChange}
              required
            />

            <p>By signing up, you agree to the Terms of Service and Privacy Policy, including Cookie Use. X may use your contact information, including your email address and phone number for purposes outlined in our Privacy Policy, such as keeping your account secure and personalising our services, including ads. Learn more. Others will be able to find you by email address or phone number, when provided, unless you choose otherwise here.</p>

            <button className='signup-button' type="submit">Sign up</button>
          </div>
        )}
      </div>
    </form >
  );
}
