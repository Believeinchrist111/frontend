import "./page.css";

export default function Home() {
  return (
    <div className="sign-card">
      <h1>Happening now</h1>
      <h2>Join today.</h2>
      <form>
        <input type="text" placeholder="Sign up with Google" />
        <input type="text" placeholder="Sign up with Apple" />
        <div className="divider"><hr />OR<hr /></div>
        <button className="create-account" type="button">Create Account</button>
      </form>
      <p className="terms">By signing up, you agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>, including <a href="#">Cookie Use</a></p>
      <p className="already-para">Already have an account?</p>
      <button className="sign-in" type="button">Sign in</button>
    </div>
  );
}
