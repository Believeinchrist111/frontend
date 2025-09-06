import ProfileNav from "../ui/profile-nav.js";
import ProfileInfoSection from "../ui/profile-info.js"
import TweetCard from "../ui/tweet-card.js";
import FooterNav from "../ui/footer-nav.js"
import SideNav from "../ui/side-nav.js";
import "./profile.css"

export default function Profile() {
  return (
    <>
      <div id="profile-body">
        <div id="profile-wrapper">
        <ProfileNav />
          <ProfileInfoSection />
          <TweetCard />
          <TweetCard />
          <TweetCard />
          <TweetCard />
          <TweetCard />
        </div>
        <SideNav />
        <FooterNav />
      </div>
    </>
  );
}
