import "./page.css";
import TweetCard from "./ui/tweet-card.js"
import HomeNav from "./ui/home-nav.js"
import HomeFooterNav from "./ui/home-footer-nav.js"
import SideNav from "./ui/side-nav";

export default function Home() {
  return (
    <>
      <HomeNav/>
      <TweetCard/>
      <HomeFooterNav/>
      <SideNav/>
    </>
  );
}






















































//  <div className="sign-card">
//     <h1>Happening now</h1>
//     <h2>Join today.</h2>
//     <form>
//       <input type="text" placeholder="Sign up with Google" />
//       <input type="text" placeholder="Sign up with Apple" />
//       <div className="divider"><hr />OR<hr /></div>
//       <button className="create-account" type="button">Create Account</button>
//     </form>
//     <p className="terms">By signing up, you agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>, including <a href="#">Cookie Use</a></p>
//     <p className="already-para">Already have an account?</p>
//     <button className="sign-in" type="button">Sign in</button>
//   </div>