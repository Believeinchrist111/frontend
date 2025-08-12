import Link from 'next/link'

import "./sign.css"
import SignUp from '../sign-up/page'


export default function SignUpOrIn() {
  return (
    <>
      <div id="sign-card">
        <h1>Happening now</h1>
        <h2>Join today.</h2>
        <input type="text" placeholder="Sign up with Google" />
        <input type="text" placeholder="Sign up with Apple" />
        <div className="divider"><hr />OR<hr /></div>
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
    </>
  );
}   