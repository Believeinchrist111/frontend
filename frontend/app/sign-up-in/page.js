"use client";
import Link from 'next/link'

import "./sign.css"
// import SignUp from '../sign-up/page'


export default function SignUpOrIn() {
  return (
    <>
      <div id="sign-up-in-container">
        <div id="sign-card">
          <h1>Happening now</h1>
          <h2>Join today.</h2>
          <button
            type="button"
            className="signup-google"
            onClick={() =>  window.location.href = "http://localhost:8000/signup/google"}
          >
            <img
              src={'/Google.png'}
              alt="Google logo"
              style={{ width: "18px", marginRight: "8px" }}
            />
            Sign up with Google
          </button>

          <button
            type="button"
            className="signup-apple"
            onClick={() => {}}
            >
              <img
                src={'/Apple_logo.png'}
                alt="Apple logo"
                style={{ width: "18px", marginRight: "8px" }}
              />
            Sign up with Apple
          </button>

          <div className="divider"><div /> OR <div /></div>
          <Link
            href='../sign-up'
            className="create-account"
          >
            Create Account
          </Link>

          <p className="terms">
            By signing up, you agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>, including <a href="#">Cookie Use</a>
          </p>

          <p className="already-para">Already have an account?</p>
          <Link
            href='../sign-in'
            className="sign-in"
          >
            Sign in
          </Link>
        </div>
      </div>
    </>
  );
}